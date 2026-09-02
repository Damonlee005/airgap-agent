# airgap-agent


## What this is
A local AI agent that runs inside a Docker container with no internet 
access. The model runs on my machine (MacBook M2, Apple Silicon), 
the agent runs in the container.

<img width="742" height="62" alt="Screenshot 2026-06-14 at 3 03 13 PM" src="https://github.com/user-attachments/assets/11034c27-2dcb-4968-866d-04193e2a7fc7" />

## Why I'm building it
I kept running into the same skills set across 
multiple aerospace and defense contractors, the ability to build and 
work with secure AI infrastructure that operates completely offline. 
Containerized AI agents, locally hosted LLMs, air gapped environments.
The demand for this kind of setup is growing fast 
because organizations handling sensitive data can not just plug into 
cloud AI tools the way everyone else does. They need the capability 
but they need it contained. 

This is a collision of both worlds, it includes secuirty principles releavant to cybersecuty and it is a way for practice within AI tooling and buidling something that combines them both.

## What I'm working toward
- Get Docker and Ollama working together in an isolated environment
- Build a Python agent that can handle basic workflow tasks
- Actually verify the network isolation works
- Understand this architecture from the ground up

## Status
July 19th, 2026 pushing docker contanorized files for completed project. estimated completion by end of july doing part time work on project.

## Roadma0
- [ ] Docker setup
- [ ] Ollama and local LLM
- [ ] Python agent
- [ ] Network isolation testing
- [ ] Demo and writeup
## Where I want to take this
Right now this is running on test prompts and basic inputs. Eventually 
I want to feed it real engineering data, simulation files, and technical 
documentation and see if it can actually do something useful inside a 
real workflow. The whole point of building it this way is that it could 
realistically be dropped into a sensitive environment where cloud AI 
just isn't an option. That's what I'm building toward.  
