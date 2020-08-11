#!/bin/sh

set -e
echo "*** Opening iperf server on H10"
/mininet/util/m h10 iperf -s > /dev/null &
SERVER_PID=$!
echo "    PID: ${SERVER_PID}"
echo "*** Opening iperf client on H2"
/mininet/util/m h2 iperf -c 10.10.10.1 -t 60
echo "*** Killing iperf server on H10"
kill -9 ${SERVER_PID}