#!/bin/bash
python3 run_web.py > /dev/null 2>&1 &
sleep 2
xdg-open http://localhost:5000 2>/dev/null || open http://localhost:5000 2>/dev/null
