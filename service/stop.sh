#!/bin/bash
for KILLPID in `ps ax | grep 'teltonika-codec8-server.service' | awk '{print $1;}` do
kill -9 $KILLPID;
done
