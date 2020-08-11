#!/bin/sh

set -e
echo "*** Opening iperf server on H10"
/mininet/util/m h10 iperf -s -u -p 5002 > /dev/null &
SERVER_PID=$!
echo "    PID: ${SERVER_PID}"
echo "*** Opening iperf client on H2"
/mininet/util/m h2 iperf -c 10.10.10.1 -p 5002 -u -b 2500Kbps -t 60
echo "*** Killing iperf server on H10"
kill -9 ${SERVER_PID}