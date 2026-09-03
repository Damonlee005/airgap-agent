#!/bin/bash
echo "checking outbound internet access..."
if curl -s --max-time 5 https://www.google.com > /dev/null; then
    echo "FAIL: reached the public internet, isolation isn't working"
else
    echo "PASS: no outbound internet access"
fi

echo ""
echo "checking access to ollama on the isolated network..."
if curl -s --max-time 5 http://ollama:11434/api/tags > /dev/null; then
    echo "PASS: can reach ollama"
else
    echo "FAIL: can't reach ollama, check the ollama container is running and healthy"
fi
