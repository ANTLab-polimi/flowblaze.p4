#!/usr/bin/env bash
# Copyright 2018-present Open Networking Foundation
# SPDX-License-Identifier: Apache-2.0

# From: https://github.com/opennetworkinglab/stratum-onos-demo/blob/master/mininet/topo/entrypoint.sh

# Start mininet in a screen session so we can attach to its CLI later.
screen -dmS cli -L -Logfile screen.log python $1

# Print CLI outoput to stdout as container log. Make sure to tail on an existing
# file if screen hasn't created it yet...
touch screen.log
tail -f screen.log