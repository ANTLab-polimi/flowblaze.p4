include util/docker/Makefile.vars

curr_dir := $(shell pwd)

deps: _docker_pull

_docker_pull:
	docker pull ${P4C_IMG}
	docker pull ${FLASK_IMG}
	docker pull ${P4MN_IMG}

start_gui_docker:
	$(info *** Starting GUI Docker container...)
	@docker run --rm -d --name gui_flowblaze \
		-v ${curr_dir}/gui:/flowblazeGui \
		-v ${curr_dir}/p4src:/p4src \
		-p 8000:8000 \
		-w /flowblazeGui ${FLASK_IMG} \
		sh -c 'python gui.py --p4_file /p4src/rate_limiter/rate_limiter.p4 --json_file /p4src/rate_limiter/p4build/bmv2.json'
	@echo "*** The GUI is accessible from http://localhost:8000"

stop_gui_docker:
	$(info *** Stopping GUI Docker container...)
	@docker stop -t0 gui_flowblaze

start_gui_local:
	$(info *** Starting GUI without Docker container...)
	cd gui/; \
	python3 gui.py --p4_file ../p4src/rate_limiter/rate_limiter.p4 --json_file ../p4src/rate_limiter/p4build/bmv2.json

test_efsm_interpreter:
	$(info *** Running EFSM interpreter with rate_limiter JSON example...)
	@docker run --rm --name test_efsm_interpreter \
		-v ${curr_dir}/:/flowblaze \
		-w /flowblaze ${FLASK_IMG} \
		python ./gui/efsm_interpreter.py --input_file ./gui/examples/rate_limiter.json --output_file /dev/null --debug

test_p4_json_parser:
	$(info *** Running P4 JSON parser with rate_limiter...)
	@docker run --rm --name test_efsm_interpreter \
		-v ${curr_dir}/:/flowblaze \
		-w /flowblaze ${FLASK_IMG} \
		sh -c 'cd ./gui && python p4_json_parser.py ../p4src/rate_limiter/rate_limiter.p4 ../p4src/rate_limiter/p4build/bmv2.json'

gui-test:
	docker run --rm --name test_gui \
		-v ${curr_dir}/gui:/gui \
		-w /gui/tests ${FLASK_IMG} \
		sh -c 'python -m unittest efsm_interpreter_test'