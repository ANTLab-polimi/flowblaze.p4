# RATE LIMITER

This use case is a small extension of the [Packet Limiter](/p4src/packet_limiter/docs/README.md)
## Run the GUI
Start the gui:
```bash
make start-gui
```
It will first compile the P4 program (the output is in `./p4build`) and then start the GUI.

Then click on **LOAD SAMPLE FSM 2**, and click on **GENERATE SWITCH CONFIG**. This will trigger the download of a switch configuration.
Now, you can override the file `flowblaze_config.cli` with the just downloaded file (make sure to keep the same name).

**TODO: add image of State Machine from GUI**

## Run Mininet
Topology: `h1 <--> s1 <--> h2`

Start Mininet by running: 
```bash
make start-mn
```
Load the switch config:
```bash
make s1-load-config
```

Run the `ping` test:
```bash
make iperf-test
```
and the obtained result should be similar to:
```bash
$ make iperf-test
*** Opening iperf server on H1
*** Opening iperf server on H1
    PID: 91
*** Opening iperf client on H2
------------------------------------------------------------
Client connecting to 10.0.0.1, TCP port 5001
TCP window size: 85.0 KByte (default)
------------------------------------------------------------
[  5] local 10.0.0.2 port 58984 connected with 10.0.0.1 port 5001
[ ID] Interval       Transfer     Bandwidth
[  5]  0.0-10.3 sec  1.25 MBytes  1.02 Mbits/sec
*** Killing iperf server on H1
```
The bandwidth shown by `iperf` should be around 1Mbps.

You can start the switch log with: `make s1-log` and interact with the BMv2 Thrift CLI with `make s1-CLI`.

You can find more `make` target to interact with the dockerized Mininet in the `Makefile`.

## Teardown
```bash
make stop-gui
make stop-mn
```
