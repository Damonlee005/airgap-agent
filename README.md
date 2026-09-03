# airgap-agent

![tests](https://github.com/Damonlee005/airgap-agent/actions/workflows/tests.yml/badge.svg)
![license](https://img.shields.io/github/license/Damonlee005/airgap-agent)

## What this is
A local AI agent that runs inside a Docker container with zero internet access. The model runs on my machine through Ollama (MacBook M2, Apple Silicon), and the agent that talks to it runs fully isolated inside a container. The container can reach the model running on my host machine, but it cannot reach anything outside of that. No outbound internet, no external API calls, nothing leaving the box unless I explicitly let it.

<img width="742" height="62" alt="Screenshot 2026-06-14 at 3 03 13 PM" src="https://github.com/user-attachments/assets/11034c27-2dcb-4968-866d-04193e2a7fc7" />

## Why I built it
I built this on my own time, outside of any class, because I kept noticing the same requirement show up over and over while looking at cybersecurity roles at aerospace and defense contractors. The ability to build and work with secure AI infrastructure that runs completely offline. Containerized AI agents, locally hosted LLMs, air gapped environments.

That requirement made sense to me once I actually thought about it. Organizations handling sensitive or classified data cannot just plug into cloud AI tools the way everyone else does. They still want the capability AI gives them, they just need it fully contained, with no path for data to slip out.

That is the part that actually pulled me in. It sits right at the intersection of two things I care about separately, cybersecurity and AI tooling. I wanted to understand that intersection by building something that lived in it, not just by reading about it.

## How it works
- Ollama runs on the host machine and serves the model locally. It is never exposed to the outside internet, only to the host itself.
- The agent, written in Python, runs inside a Docker container that has no outbound network access, enforced by a Docker network with `internal: true`.
- A `host.docker.internal` mapping is the one address allowed through, so the agent inside the container can still reach the model running on the host without opening any other path out.
- Retry logic with exponential backoff handles transient connection failures without hammering a broken connection.
- Custom exception types (`ModelUnreachableError`, `ModelResponseError`) separate "the network is down" from "the response was garbage," instead of catching a generic exception everywhere.
- Conversation history is kept in memory and automatically trimmed so a long session does not blow past the model's context window.

## Supported models
Any model pulled with `ollama pull <name>` will work. Tested against:
- `llama3`
- `mistral`

Switch models without restarting: start with `--model mistral`, or type `model mistral` during a session.

## How to run this on your own device
Requires Docker and Ollama installed locally.

1. Install Docker Desktop and make sure it is running.
2. Install Ollama and pull at least one model:
3. Clone this repository.
4. Copy the env template:
5. Build and start the container:
6. Talk to it. Type `exit` to quit, `clear` to reset history, `model <name>` to switch models.

To verify the isolation yourself, in another terminal while the container is running:
You should see it fail to reach the public internet and succeed in reaching Ollama on the host.

## Running the tests
18 tests, all mocked, none of them touch a real network. CI runs these automatically on every push, see the badge at the top.

## What I verified
- Docker and Ollama running together with the model fully local.
- The agent working end to end, including switching between two different models in the same session.
- Network isolation confirmed directly through live traffic inspection, not assumed.
- Zero outbound internet connections from the container while the agent stayed fully functional.

## Where I want to take this
Right now it is running on test prompts and basic inputs. Next I want to feed it real engineering data, simulation files, and technical documentation, and see if it can actually do something useful inside a real workflow instead of just responding to simple test cases. The whole point of building it this way is that it could realistically get dropped into a sensitive environment where cloud AI is not an option. That is what I am building toward.
