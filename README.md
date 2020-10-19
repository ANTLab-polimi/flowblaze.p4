# FlowBlaze.p4

FlowBlaze.p4 is a library for the quick prototyping of stateful SDN applications in P4.

This repository contains the open-source implementation of FlowBlaze.p4 together with some demo applications.

Folders in the `p4src` directory, includes a per-application README file.

## Pre-requisites

- `docker`
- `make`

Before running the demo applications, build the required dependencies

```bash
make deps
```
## FlowBlaze demo applications
### Packet Limiter
**Go to [Packet Limiter](p4src/packet_limiter/docs/README.md)**

### Rate Limiter
**Go to [Rate Limiter](p4src/class_rate_limiter/docs/README.md)**

## Reference

If you use FlowBlaze.p4 for your research and/or other publications, please cite
```
FlowBlaze.p4: a library for quick prototyping of stateful SDN applications in P4
D. Moro, D. Sanvito, A. Capone
IEEE NFV-SDN 2020, November 2020
```
