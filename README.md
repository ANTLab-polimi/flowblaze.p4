# FlowBlaze.p4

FlowBlaze.p4 is a library for the quick prototyping of stateful SDN applications in P4.

This repository contains the open-source implementation of FlowBlaze.p4 together with some demo applications.

Folders in the `p4src` directory include a per-application README file.

## Pre-requisites

- `docker`
- `make`

Before running the demo applications, build the required dependencies

```bash
make deps
```
## FlowBlaze demo applications

- [Packet Limiter](p4src/packet_limiter)
- [Rate Limiter](p4src/class_rate_limiter)

## FlowBlaze template application

- [Template](p4src/template)

## Reference

If you use FlowBlaze.p4 for your research and/or other publications, please cite
```
FlowBlaze.p4: a library for quick prototyping of stateful SDN applications in P4
D. Moro, D. Sanvito, A. Capone
IEEE NFV-SDN 2020
```

## Contact

### Support

If you have any questions, please use GitHub's [issue system](https://github.com/ANTLab-polimi/flowblaze.p4/issues)

### Contribute

Your contributions are very welcome! Please fork the GitHub repository and create a pull request.

### Lead developers

Daniele Moro
* Mail <daniele (dot) moro (at) polimi (dot) it>
* Github: [@daniele-moro](https://github.com/daniele-moro)

Davide Sanvito
* Mail: <davide (dot) sanvito (at) neclab (dot) eu>
* GitHub: [@DavideSanvito](https://github.com/DavideSanvito)
