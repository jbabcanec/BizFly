#!/bin/bash
echo "Stopping BizFly services..."
kill 33618 33619 2>/dev/null || true
pkill -f 'uvicorn' 2>/dev/null || true
pkill -f 'npm.*dev' 2>/dev/null || true
echo "Services stopped."
