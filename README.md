## Requirements

- `docker`
- `make`
- `python3` (to run GUI without Docker)

## Before running

```bash
make deps
```

## OPP examples
### Packet Limiter
**Go to [Packet Limiter](./p4src/rate_limiter/README.md)**

## TODOs
### OPP.p4:
- Look at `OPP_loop.p4` for TODOs
- Move `pkt_action` table inside OPP_loop control and expose a DEFINE to define arbitrary actions
- Add PTFs for OPP examples (issue: not able to read counters from PTFs due to [p4lang/PI#376](https://github.com/p4lang/PI/issues/376))

### EFSM interpreter:
- divide parse function in sub-function to ease testing
- add unit testing