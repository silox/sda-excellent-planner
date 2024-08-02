#!/bin/bash

cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/.."
~/.local/bin/poetry run python src/main.py
