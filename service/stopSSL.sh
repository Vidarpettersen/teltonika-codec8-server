#!/bin/bash
for KILLPID in `ps ax | grep 'device-import.py' | awk '{print $1;}` do
kill -9 $KILLPID;
done
