# Security Policy

This is a personal learning project, not production software, but I still take security reports seriously.

## Reporting a Vulnerability

If you find a security issue in this project, for example a way the network isolation could be bypassed, or a dependency with a known vulnerability, please open a GitHub issue rather than exploiting it.

## Scope

This project runs entirely on your own local machine and does not handle production data. The main security property it claims is network isolation between the agent container and the outside internet, verified using `scripts/verify_isolation.sh`. If you find a way around that isolation, that is the most useful thing to report.
