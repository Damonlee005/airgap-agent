# airgap-agent

![tests](https://github.com/Damonlee005/airgap-agent/actions/workflows/tests.yml/badge.svg)
![license](https://img.shields.io/github/license/Damonlee005/airgap-agent)

## What this is
A local AI agent that runs inside a Docker container with zero internet access. The model runs on my machine through Ollama (MacBook M2, Apple Silicon), and the agent that talks to it runs fully isolated inside a container. The container can reach the model running on my host machine, but it cannot reach anything outside of that. No outbound internet, no external API calls, nothing leaving the box unless I explicitly let it.

<img width="742" height="62" alt="Screenshot 2026-06-14 at 3 03 13 PM" src="https://github.com/user-attachments/assets/11034c27-2dcb-4968-866d-04193e2a7fc7" />

# airgap-agent

![tests](https://github.com/Damonlee005/airgap-agent/actions/workflows/tests.yml/badge.svg)
![license](https://img.shields.io/github/license/Damonlee005/airgap-agent)

## Why I built it
I built this on my own time because I kept seeing the same requirement in cybersecurity roles at aerospace and defense contractors: secure AI that runs completely offline.

It made sense once I thought about it. Companies handling sensitive data can't paste it into cloud AI tools, because that data ends up on someone else's servers. They still want AI, they just need it fully contained.

That sits right between two things I care about, cybersecurity and AI. I didn't want to just read about air gapped systems. I wanted to build one and actually understand how it works.

## Architecture

```
            Your computer (Docker host)
 ┌───────────────────────────────────────────────┐
 │   Private Docker network (internal: true)     │
 │  ┌─────────────────────────────────────────┐  │
 │  │  ┌──────────────┐    ┌──────────────┐   │  │
 │  │  │ airgap-agent │◀──▶│ airgap-ollama│   │  │
 │  │  │   (Python)   │    │   (model)    │   │  │
 │  │  └──────────────┘    └──────────────┘   │  │
 │  └─────────────────────────────────────────┘  │
 └─────────────────────╳─────────────────────────┘
                       ╳  no route out
                    Internet
```

Docker normally gives every network a route to the internet. Setting `internal: true` takes it away.

## How it works
- Ollama runs in its own container and serves the model.
- The Python agent runs in a second container and reaches the model at `http://ollama:11434`. That's the only address it can reach.
- The agent waits for Ollama to pass a health check before starting.
- It checks which models are actually installed and falls back to one that is if you ask for one that isn't.
- Connection failures get retried up to 3 times with increasing wait times.
- Custom errors tell you whether the network failed or the model gave a bad response.
- Chat history is saved so the model remembers context, and old messages get trimmed so long sessions don't overload it.
- You can switch models mid conversation without restarting.

## Project structure

```
airgap-agent/
├── agent.py               # main loop and commands
├── ollama_client.py       # talks to the Ollama API
├── conversation.py        # chat history
├── exceptions.py          # custom errors
├── config.py              # settings from .env
├── utils/retry.py         # retry logic
├── scripts/verify_isolation.sh  # proves it's offline
├── tests/                 # 18 unit tests
├── Dockerfile
└── docker-compose.yml     # containers + isolated network
```

## Supported models
Tested with `llama3` and `mistral`, but any Ollama model works. Start with `--model mistral` or type `model mistral` mid session to switch.

## How to run it
You just need Docker Desktop running.

**1. Clone the repo**
```bash
git clone https://github.com/Damonlee005/airgap-agent.git
cd airgap-agent
cp .env.example .env
```

**2. Download a model.** This is the only step that uses the internet. The isolated network can't download anything, so I load the model into storage first with a temporary container, kind of like loading a USB drive before walking it into a secure room.
```bash
docker volume create airgap-agent_ollama_data
docker run -d --name ollama-setup -v airgap-agent_ollama_data:/root/.ollama ollama/ollama
docker exec ollama-setup ollama pull llama3
docker rm -f ollama-setup
```

**3. Start it up**
```bash
docker compose up -d --build
docker attach airgap-agent
```

**4. Talk to it.** Type a prompt and hit enter. Use `clear` to reset, `model <name>` to switch, or `exit` to quit.

## Verifying the isolation
Saying something is isolated is easy. Proving it is the real work. So I wrote a script that tests it from inside the container:
```bash
docker exec airgap-agent bash scripts/verify_isolation.sh
```
It tries to reach Google, which should fail, and then tries to reach Ollama, which should work. You want to see two PASS results. I also watched live network traffic while the agent was running to make sure nothing was getting out.

## Running the tests
18 tests, all mocked, so they don't need a network or a real model. GitHub Actions runs them with a lint check on every push, and Dependabot watches for vulnerable dependencies.
```bash
pip install -r requirements.txt -r requirements-dev.txt
pytest tests/ -v
```

## Design decisions
- **Docker over a VM:** It's lighter, and the whole isolation setup lives in one config file anyone can read.
- **Ollama:** It makes running models locally easy and works well on my M2 Mac.
- **Ollama in its own container:** I originally ran it on my Mac directly, but a fully internal network can't reach the host. Putting both on the same private network kept things locked down.
- **Mocked tests:** The tests check my logic, not whether a model happens to be running.

## Challenges
- Getting the network right took a lot of trial and error. Every fix either broke the isolation or broke the connection to the model.
- Once the network was locked down, Ollama couldn't download models. I had to figure out how to load them in first.
- Ollama names models like `llama3:latest`, but people type `llama3`, so the agent kept saying models didn't exist. I added name matching to fix it.
- Early on, every error looked the same, which made debugging painful. Custom error types fixed that.

## Limitations
This is a learning project, and I want to be upfront about what it doesn't do yet:
- It's not a true physical air gap. The host machine is still online.
- The containers use default settings. Running as non root with a read only filesystem would make them stronger.
- There's no audit log of prompts and responses.
- The Ollama image isn't pinned to a specific version.

If you find a way around the isolation, see [SECURITY.md](SECURITY.md).

## What I learned
- How Docker networking really works, and how one setting decides whether a container can reach the internet.
- How to run AI models locally without depending on any cloud service.
- Security has to be tested, not assumed. Writing the verify script changed how I think about building things.
- How retries, custom errors, and logging make problems way easier to track down.
- How to set up CI, automated tests, and dependency scanning. This was my first project with all of that running on every push.
- Writing the limitations section made me think like an attacker, which is a big part of cybersecurity.

## What's next
- Test it with real engineering data, simulation files, and technical docs
- Let it read local documents without them ever leaving the machine
- Harden the containers
- Add audit logging
- Pin image versions

The goal is something that could realistically be used in a sensitive environment where cloud AI isn't an option. That's what I'm working toward.
