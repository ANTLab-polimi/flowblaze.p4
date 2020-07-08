## Requirements

- `Docker`
- `Python3` (to run GUI without Docker)

## Before running

```bash
make docker_pull
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
Some TODOs for OPP.p4 are in the `OPP_loop.p4` file.