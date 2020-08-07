#!/bin/sh

set -e
echo "*** Opening iperf server on H1"
/mininet/util/m h1 iperf -s > /dev/null &
SERVER_PID=$!
echo "    PID: ${SERVER_PID}"
echo "*** Opening iperf client on H2"
/mininet/util/m h2 iperf -c 10.0.0.1
echo "*** Killing iperf server on H1"
kill -9 ${SERVER_PID}