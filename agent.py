import argparse
import logging
import sys

from config import LOG_LEVEL, OLLAMA_MODEL
from conversation import Conversation
from exceptions import AgentError
from ollama_client import OllamaClient

logger = logging.getLogger("airgap_agent")


def setup_logging(verbose):
    level = logging.DEBUG if verbose else getattr(logging, LOG_LEVEL, logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def parse_args():
    parser = argparse.ArgumentParser(description="airgap-agent")
    parser.add_argument(
        "--model", default=OLLAMA_MODEL,
        help=f"model to start with (default: {OLLAMA_MODEL})",
    )
    parser.add_argument(
        "--list-models", action="store_true",
        help="list models available on the host and exit",
    )
    parser.add_argument("-v", "--verbose", action="store_true")
    return parser.parse_args()


def resolve_model(client, requested_model):
    # check the model is actually pulled before using it, otherwise
    # ollama just throws a confusing error mid-request
    try:
        available = client.list_models()
    except AgentError:
        available = []

    if requested_model in available:
        return requested_model

    if available:
        logger.warning(
            "'%s' isn't pulled on the host. available: %s",
            requested_model, ", ".join(available),
        )
        return available[0]

    logger.warning("couldn't check available models, using '%s' anyway", requested_model)
    return requested_model


def print_banner(model):
    print("=" * 50)
    print("airgap-agent")
    print(f"model: {model}")
    print("network: isolated container, host-only model access")
    print("=" * 50)


def main():
    args = parse_args()
    setup_logging(args.verbose)

    client = OllamaClient()

    if not client.is_reachable():
        logger.error("can't reach ollama on the host")
        logger.error("check ollama is running and host.docker.internal resolves")
        sys.exit(1)

    if args.list_models:
        try:
            models = client.list_models()
        except AgentError as exc:
            logger.error("couldn't list models: %s", exc)
            sys.exit(1)
        print("models available on host:")
        for m in models:
            print(f"  - {m}")
        return

    model = resolve_model(client, args.model)
    print_banner(model)
    print("type a prompt and hit enter.")
    print("'exit' to quit, 'clear' to reset, 'model <name>' to switch.\n")

    convo = Conversation(system_prompt="You are a helpful assistant running fully offline.")

    while True:
        try:
            prompt = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nexiting")
            break

        if not prompt:
            continue
        if prompt.lower() in ("exit", "quit"):
            break
        if prompt.lower() == "clear":
            convo.clear()
            print("history cleared\n")
            continue
        if prompt.lower().startswith("model "):
            model = resolve_model(client, prompt[6:].strip())
            print(f"switched to: {model}\n")
            continue

        convo.add_user(prompt)
        try:
            response = client.chat(model, convo.get_messages())
        except AgentError as exc:
            logger.error("request failed: %s", exc)
            continue

        convo.add_assistant(response)
        print(f"\n{response}\n")


if __name__ == "__main__":
    main()
