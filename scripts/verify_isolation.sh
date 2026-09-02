#!/bin/bash
# run from the host while the container's up:
#   docker exec airgap-agent bash scripts/verify_isolation.sh

echo "checking outbound internet access..."
if curl -s --max-time 5 https://www.google.com > /dev/null; then
    echo "FAIL: reached the public internet, isolation isn't working"
else
    echo "PASS: no outbound internet access"
fi

echo ""
echo "checking access to ollama on the host..."
if curl -s --max-time 5 http://host.docker.internal:11434/api/tags > /dev/null; then
    echo "PASS: can reach ollama on the host"
else
    echo "FAIL: can't reach ollama, check it's running and host.docker.internal resolves"
fi
