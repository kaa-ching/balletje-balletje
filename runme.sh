#!/usr/bin/env bash
set -euo pipefail

if [[ -x "./bin/python" ]]; then
	./bin/python game.py
elif [[ -x "./.venv/bin/python" ]]; then
	./.venv/bin/python game.py
elif command -v python3 >/dev/null 2>&1; then
	python3 game.py
else
	python game.py
fi
