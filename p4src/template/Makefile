include ../../util/docker/Makefile.vars

curr_dir := $(shell pwd)
project_name := $(shell basename "${curr_dir}")

gui_docker_name := "${project_name}_gui"
mn_docker_name := "${project_name}_mn"

clear: stop-mn stop-gui
	rm -rf ./p4build

start-mn: stop-mn
	$(info *** Running topo.py Mininet topology)
	docker run --privileged -it -d --rm --name ${mn_docker_name} \
	-v ${curr_dir}/../../p4build/${project_name}:/p4build \
	-v ${curr_dir}:/${project_name} \
	--entrypoint /${project_name}/topo.py \
	${P4MN_IMG}

stop-mn:
	@docker stop -t0 ${mn_docker_name} | true

attach-mininet:
	$(info ******* To detach CTRL+P followed by CTRL+Q *******)
	@docker attach ${mn_docker_name}

# Here some examples of some useful target you can modify for your specific Mininet topology

# To load configuration to the BMv2 switch S1
s1-load-config:
	$(info *** Loading config on S1)
	@docker exec -it ${mn_docker_name} /bin/sh -c 'simple_switch_CLI --thrift-port $$(cat /tmp/bmv2-s1-thrift-port) < /${project_name}/flowblaze_config.cli'
	@docker exec -it ${mn_docker_name} /bin/sh -c 'simple_switch_CLI --thrift-port $$(cat /tmp/bmv2-s1-thrift-port) < /${project_name}/other_tables_config.cli'

# To open LOG of BMv2 switch S1
s1-log:
	docker exec -it ${mn_docker_name} /bin/sh -c "tail -f /tmp/bmv2-s1-log"

# To open CLI of BMv2 switch S1
s1-CLI:
	$(info *** Opening S1 Switch runtime CLI \(THRIFT\))
	@docker exec -it ${mn_docker_name} /bin/sh -c 'simple_switch_CLI --thrift-port $$(cat /tmp/bmv2-s1-thrift-port)'

# To clear register of BMv2 switch S1
s1-clear-reg:
	$(info *** Clear registers for S1)
	@echo "    reg_state"
	@docker exec -it ${mn_docker_name} /bin/sh -c 'echo "register_reset reg_state" | simple_switch_CLI --thrift-port $$(cat /tmp/bmv2-s1-thrift-port) > /dev/null'
	@echo "    reg_R0"
	@docker exec -it ${mn_docker_name} /bin/sh -c 'echo "register_reset reg_R0" | simple_switch_CLI --thrift-port $$(cat /tmp/bmv2-s1-thrift-port) > /dev/null'
	@echo "    reg_R1"
	@docker exec -it ${mn_docker_name} /bin/sh -c 'echo "register_reset reg_R1" | simple_switch_CLI --thrift-port $$(cat /tmp/bmv2-s1-thrift-port) > /dev/null'
	@echo "    reg_R2"
	@docker exec -it ${mn_docker_name} /bin/sh -c 'echo "register_reset reg_R2" | simple_switch_CLI --thrift-port $$(cat /tmp/bmv2-s1-thrift-port) > /dev/null'
	@echo "    reg_R3"
	@docker exec -it ${mn_docker_name} /bin/sh -c 'echo "register_reset reg_R3" | simple_switch_CLI --thrift-port $$(cat /tmp/bmv2-s1-thrift-port) > /dev/null'
	@echo "    reg_G"
	@docker exec -it ${mn_docker_name} /bin/sh -c 'echo "register_reset reg_G" | simple_switch_CLI --thrift-port $$(cat /tmp/bmv2-s1-thrift-port) > /dev/null'

# To clear the FlowBlaze tables of BMv2 switch S1
s1-clear-flowblaze:
	$(info *** Clear FlowBlaze state for S1)
	@echo "    EFSM Table"
	@docker exec -it ${mn_docker_name} /bin/sh -c 'echo "table_clear ingress.FlowBlazeLoop.EFSM_table" | simple_switch_CLI --thrift-port $$(cat /tmp/bmv2-s1-thrift-port) > /dev/null'
	@echo "    Condition Table"
	@docker exec -it ${mn_docker_name} /bin/sh -c 'echo "table_set_default ingress.FlowBlazeLoop.condition_table NoAction" | simple_switch_CLI --thrift-port $$(cat /tmp/bmv2-s1-thrift-port) > /dev/null'
	@echo "    Packet Action"
	@docker exec -it ${mn_docker_name} /bin/sh -c 'echo "table_clear ingress.FlowBlazeLoop.pkt_action" | simple_switch_CLI --thrift-port $$(cat /tmp/bmv2-s1-thrift-port) > /dev/null'

# To open shell of host H1
h1-shell:
	$(info *** Opening H1 shell)
	@docker exec -it ${mn_docker_name} /mininet/util/m h1

# To ping from host h1
h1-ping:
	$(info *** Opening H1 shell and ping H2)
	@echo 'ping 10.0.0.2 -c 12'
	@docker exec -it ${mn_docker_name} /bin/sh -c '/mininet/util/m h1 ping 10.0.0.2 -c 12'


start-gui: stop-gui build-p4
	$(info *** Starting GUI Docker container...)
	@docker run --rm -d --name ${gui_docker_name} \
		-v ${curr_dir}/../../gui:/flowblazeGui \
		-v ${curr_dir}/../../p4src:/p4src \
		-p 8000:8000 \
		-w /flowblazeGui ${FLASK_IMG} \
		/bin/sh -c 'python gui.py --p4_file /p4src/${project_name}/template.p4 --json_file /p4src/${project_name}/p4build/bmv2.json'
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
		p4c-bm2-ss --arch v1model -o ./${project_name}/p4build/bmv2.json \
		--p4runtime-files ./${project_name}/p4build/p4info.txt,${project_name}/p4build/p4info.bin \
		--Wdisable=unsupported \
		./${project_name}/template.p4
	@echo "*** P4 program compiled successfully! Output files are in p4build"

status:
	echo ${project_name}
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
