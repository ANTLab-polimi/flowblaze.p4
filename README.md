## Requirements

- `docker`
- `make`
- `python3` (to run GUI without Docker)

## Before running

```bash
make deps
```

## OPP examples
### Rate Limiter

#### Compile rate limiter
```bash
make build-rate_limiter
```
Outputs are in folder `./p4build/rate_limiter`

#### Run rate limiter
Topology: `h1 <--> s1 <--> h2`
```bash
cd p4src/rate_limiter
make start
```
to stop it run `make stop`. **N.B.: BMv2 switch is loaded without any configured pipeline.**

**Open BMv2 switch CLI** (Thrift CLI): `make s1-CLI`

**Open host h1 or h2 shell**: `make [h1-h2]-CLI`

**Attach mininet shell**: `make attach-mininet`.
To exit (detach mininet shell) use `CTRL+P` followed by `CTRL+Q`.


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
Install the needed requirements from `util/docker/flask/requirements.txt`, then run `make start_gui_local`, the GUI is then accessible 
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
- push generated rules directly on a switch
- use html template (es. Jinja2) https://flask.palletsprojects.com/en/1.1.x/quickstart/#rendering-templates