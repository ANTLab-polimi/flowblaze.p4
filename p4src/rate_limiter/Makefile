include ../../util/docker/Makefile.vars

curr_dir := $(shell pwd)

gui_docker_name := "rate_limiter_gui"
mn_docker_name := "rate_limiter_mn"

start-mn: stop-mn
	$(info *** Running topo.py Mininet topology)
	docker run --privileged -it -d --rm --name ${mn_docker_name} \
	-v ${curr_dir}/../../p4build/rate_limiter:/p4build \
	-v ${curr_dir}:/rate_limiter \
	--entrypoint /rate_limiter/topo.py \
	${P4MN_IMG}

stop-mn:
	docker stop -t0 ${mn_docker_name}

s1-load-config:
	$(info *** Loading config $1 on S1)
	@docker exec -it ${mn_docker_name} /bin/sh -c 'simple_switch_CLI --thrift-port $$(cat /tmp/bmv2-s1-thrift-port) < /rate_limiter/flowblaze_config.cli'
	@docker exec -it ${mn_docker_name} /bin/sh -c 'simple_switch_CLI --thrift-port $$(cat /tmp/bmv2-s1-thrift-port) < /rate_limiter/other_tables_config.cli'

s1-log:
	docker exec -it ${mn_docker_name} /bin/sh -c "tail -f /tmp/bmv2-s1-log"

s1-CLI:
	$(info *** Opening S1 Switch runtime CLI \(THRIFT\))
	@docker exec -it ${mn_docker_name} /bin/sh -c 'simple_switch_CLI --thrift-port $$(cat /tmp/bmv2-s1-thrift-port)'

h1-shell:
	$(info *** Opening H1 shell)
	@docker exec -it ${mn_docker_name} /mininet/util/m h1

h1-test:
	$(info *** Opening H1 shell and ping H2)
	@echo 'ping 10.0.0.2 -c 12'
	@docker exec -it ${mn_docker_name} /bin/sh -c 'echo "ping 10.0.0.2 -c 12 " | /mininet/util/m h1'

h2-shell:
	$(info *** Opening H2 shell)
	@docker exec -it ${mn_docker_name} /mininet/util/m h2

h2-test:
	$(info *** Opening H2 shell and ping H1)
	@echo 'ping 10.0.0.1 -c 12 '
	@docker exec -it ${mn_docker_name} /bin/sh -c 'echo "ping 10.0.0.1 -c 12" | /mininet/util/m h2'

attach-mininet:
	$(info ******* To detach CTRL+P followed by CTRL+Q *******)
	@docker attach ${mn_docker_name}

start-gui: stop-gui build-p4
	$(info *** Starting GUI Docker container...)
	@docker run --rm -d --name ${gui_docker_name} \
		-v ${curr_dir}/../../gui:/oppGui \
		-v ${curr_dir}/../../p4src:/p4src \
		-p 8000:8000 \
		-w /oppGui ${FLASK_IMG} \
		/bin/sh -c 'python gui.py --p4_file /p4src/rate_limiter/rate_limiter.p4 --json_file /p4src/rate_limiter/p4build/bmv2.json'
	@echo "*** The GUI is accessible from http://localhost:8000"

gui-log:
	@docker logs -f ${gui_docker_name}

stop-gui:
	$(info *** Stopping GUI Docker container...)
	@docker stop -t0 ${gui_docker_name} | true

build-p4:
	$(info *** Compiling Rate Limiter...)
	@mkdir -p ./p4build
	@docker run --rm -v ${curr_dir}/../:/p4src -w /p4src ${P4C_IMG} \
		p4c-bm2-ss --arch v1model -o ./rate_limiter/p4build/bmv2.json \
		--p4runtime-files ./rate_limiter/p4build/p4info.txt,rate_limiter/p4build/p4info.bin \
		--Wdisable=unsupported \
		./rate_limiter/rate_limiter.p4
	@echo "*** P4 program compiled successfully! Output files are in p4build"

status:
	@echo "GUI Status:"
	@docker ps | grep -q "${gui_docker_name}"; \
	if [ $$? -eq 0 ]; then \
	  echo "  GUI is running"; \
	else \
	  echo "  GUI NOT running"; \
	fi;
	@echo "Mininet Status:"
	@docker ps | grep -q "${mn_docker_name}"; \
	if [ $$? -eq 0 ]; then \
	  echo "  MININET is running"; \
	else \
	  echo "  MININET NOT running"; \
	fi;
