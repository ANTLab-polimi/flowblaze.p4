curr_dir := $(shell pwd)
P4C_IMG := opennetworking/p4c:latest
FLASK_IMG := "dmoro92/flask:latest"
PYTHON_IMG := python:3.5-alpine3.11

docker_build_flask:
	cd gui/Docker && docker build -t ${FLASK_IMG} .

docker_push_flask:
	docker push ${FLASK_IMG}

docker_pull:
	docker pull ${P4C_IMG}
	docker pull ${FLASK_IMG}

build-rate_limiter:
	$(info *** Compiling Rate Limiter...)
	@mkdir -p ./p4build/rate_limiter
	@docker run --rm -v ${curr_dir}:/opp -w /opp ${P4C_IMG} \
		p4c-bm2-ss --arch v1model -o ./p4build/rate_limiter/bmv2.json \
		--p4runtime-files ./p4build/rate_limiter/p4info.txt,p4build/rate_limiter/p4info.bin \
		--Wdisable=unsupported \
		./p4src/rate_limiter/rate_limiter.p4
	@echo "*** P4 program compiled successfully! Output files are in p4build/rate_limiter"

start_gui_docker:
	$(info *** Starting GUI Docker container...)
	@docker run --rm --name gui_opp -v ${curr_dir}/gui:/oppGui -p 8000:8000 -w /oppGui -d ${FLASK_IMG} \
		python main_flask.py

stop_gui_docker:
	$(info *** Stopping GUI Docker container...)
	@docker stop -t0 gui_opp

start_gui_local:
	$(info *** Starting GUI without Docker container...)
	cd gui/; \
	python3 main_flask.py


