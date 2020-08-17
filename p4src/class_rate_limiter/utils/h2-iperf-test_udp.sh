#!/bin/sh

# Copyright 2020 Daniele Moro <daniele.moro@polimi.it>
#                Davide Sanvito <davide.sanvito@neclab.eu>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -e
echo "*** Opening iperf server on H10"
/mininet/util/m h10 iperf -s -u -p 5002 > /dev/null &
SERVER_PID=$!
echo "    PID: ${SERVER_PID}"
echo "*** Opening iperf client on H2"
/mininet/util/m h2 iperf -c 10.10.10.1 -p 5002 -u -b 2500Kbps -t 60
echo "*** Killing iperf server on H10"
kill -9 ${SERVER_PID}