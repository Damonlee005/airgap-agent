# airgap-agent


## What this is
A local AI agent that runs inside a Docker container with no internet 
access. The model runs on my machine (MacBook Pro M2, Apple Silicon), 
the agent runs in the container, nothing leaves.

## Why I'm building it
I'm a student at UT. Going through internship postings 
in the Knoxville area I kept running into the same requirement across 
multiple aerospace and defense contractors, the ability to build and 
work with secure AI infrastructure that operates completely offline. 
Containerized AI agents, locally hosted LLMs, air gapped environments.
The demand for this kind of setup is growing fast 
because organizations handling sensitive data can not just plug into 
cloud AI tools the way everyone else does. They need the capability 
but they need it contained. 

## What I'm working toward
- Get Docker and Ollama working together in an isolated environment
- Build a Python agent that can handle basic engineering workflow tasks
- Actually verify the network isolation works
- Understand this architecture from the ground up

## Status
Still in progress. Pushing updates as I progress.

## Roadmap
- [ ] Docker setup
- [ ] Ollama and local LLM
- [ ] Python agent
- [ ] Network isolation testing
- [ ] Demo and writeup

## Author
Student at the University of Tennessee.  
