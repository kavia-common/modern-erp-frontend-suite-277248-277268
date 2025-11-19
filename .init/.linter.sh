#!/bin/bash
cd /home/kavia/workspace/code-generation/modern-erp-frontend-suite-277248-277268/backend
source venv/bin/activate
flake8 .
LINT_EXIT_CODE=$?
if [ $LINT_EXIT_CODE -ne 0 ]; then
  exit 1
fi

