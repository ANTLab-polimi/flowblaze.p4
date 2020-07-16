## Requirements

- `Docker`
- `make`
- `Python3` (to run GUI without Docker)

## Before running

```bash
make deps
```

## Compile OPP examples
### Rate Limiter

Run
```bash
make build-rate_limiter
```
Outputs are in folder `./p4build/rate_limiter`

## Run GUI
Run with Docker container:
```bash
make start_gui_docker
```
The GUI is then accessible from [http://localhost:8000](http://localhost:8000).
To stop the GUI run:
```bash
make stop_gui_docker
```

### Run GUI without Docker
Install the needed requirements from `gui/requirements.txt`, then run `make start_gui_local`, the GUI is then accessible 
from [http://localhost:8000](http://localhost:8000).

## TODOs
### OPP.p4:
- Look at `OPP_loop.p4` for TODOs
- Move `pkt_action` table inside OPP_loop control and expose a DEFINE to define arbitrary actions
- Add PTFs for OPP examples (issue: not able to read counters from PTFs due to [p4lang/PI#376](https://github.com/p4lang/PI/issues/376))

### EFSM interpreter:
- divide parse function in sub-function to ease testing
- add unit testing

### GUI:
- Parse P4 or JSON for BMv2 to extract parser information to compile drop-down matchFields menu and possible actions
- find a way to deal with actions parameters in state change actions
- push geneated rules directly on a switch