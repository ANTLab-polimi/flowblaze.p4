# Copyright 2020 Daniele Moro <daniele.moro@polimi.it>
#                Davide Sanvito <davide.sanvito@neclab.eu>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
	$(info *** Stopping Mininet)
	@docker stop -t0 ${mn_docker_name} | true

s1-load-config:
	$(info *** Loading config on S1)
	@docker exec -it ${mn_docker_name} /bin/sh -c 'simple_switch_CLI --thrift-port $$(cat /tmp/bmv2-s1-thrift-port) < /${project_name}/flowblaze_config.cli'
	@docker exec -it ${mn_docker_name} /bin/sh -c 'simple_switch_CLI --thrift-port $$(cat /tmp/bmv2-s1-thrift-port) < /${project_name}/other_tables_config.cli'

s1-log:
	docker exec -it ${mn_docker_name} /bin/sh -c "tail -f /tmp/bmv2-s1-log"

s1-CLI:
	$(info *** Opening S1 Switch runtime CLI \(THRIFT\))
	@docker exec -it ${mn_docker_name} /bin/sh -c 'simple_switch_CLI --thrift-port $$(cat /tmp/bmv2-s1-thrift-port)'

s1-clear: s1-clear-reg s1-clear-flowblaze

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

s1-clear-flowblaze:
	$(info *** Clear FlowBlaze state for S1)
	@echo "    EFSM Table"
	@docker exec -it ${mn_docker_name} /bin/sh -c 'echo "table_clear FlowBlaze.EFSM_table" | simple_switch_CLI --thrift-port $$(cat /tmp/bmv2-s1-thrift-port) > /dev/null'
	@echo "    Condition Table"
	@docker exec -it ${mn_docker_name} /bin/sh -c 'echo "table_set_default FlowBlaze.condition_table NoAction" | simple_switch_CLI --thrift-port $$(cat /tmp/bmv2-s1-thrift-port) > /dev/null'
	@echo "    Packet Action"
	@docker exec -it ${mn_docker_name} /bin/sh -c 'echo "table_clear FlowBlaze.pkt_action" | simple_switch_CLI --thrift-port $$(cat /tmp/bmv2-s1-thrift-port) > /dev/null'

h1-shell:
	$(info *** Opening H1 shell)
	@docker exec -it ${mn_docker_name} /mininet/util/m h1

h1-test:
	$(info *** Opening H1 shell and ping H2)
	@echo 'ping 10.0.0.2 -c 12'
	@docker exec -it ${mn_docker_name} /bin/sh -c '/mininet/util/m h1 ping 10.0.0.2 -c 12'

h2-shell:
	$(info *** Opening H2 shell)
	@docker exec -it ${mn_docker_name} /mininet/util/m h2

h2-test:
	$(info *** Opening H2 shell and ping H1)
	@echo 'ping 10.0.0.1 -c 12 '
	@docker exec -it ${mn_docker_name} /bin/sh -c '/mininet/util/m h2 ping 10.0.0.1 -c 12'

attach-mininet:
	$(info ******* To detach CTRL+P followed by CTRL+Q *******)
	@docker attach ${mn_docker_name}

start-gui: stop-gui build-p4
	$(info *** Starting GUI Docker container...)
	@docker run --rm -d --name ${gui_docker_name} \
		-v ${curr_dir}/../../gui:/flowblazeGui \
		-v ${curr_dir}/../../p4src:/p4src \
		-p 8000:8000 \
		-w /flowblazeGui ${FLASK_IMG} \
		/bin/sh -c 'python gui.py --p4_file /p4src/${project_name}/packet_limiter.p4 --json_file /p4src/${project_name}/p4build/bmv2.json'
	@echo "*** The GUI is accessible from http://localhost:8000"

gui-log:
	@docker logs -f ${gui_docker_name}

stop-gui:
	$(info *** Stopping GUI Docker container...)
	@docker stop -t0 ${gui_docker_name} | true

build-p4:
	@echo "*** Compiling ${project_name}..."
	@mkdir -p ./p4build
	@docker run --rm -v ${curr_dir}/../:/p4src -w /p4src ${P4C_IMG} \
		p4c-bm2-ss --arch v1model -o ./${project_name}/p4build/bmv2.json \
		--p4runtime-files ./${project_name}/p4build/p4info.txt,${project_name}/p4build/p4info.bin \
		--Wdisable=unsupported \
		./${project_name}/packet_limiter.p4
	@echo "*** P4 program compiled successfully! Output files are in p4build"

status:
	@echo "PROJECT: ${project_name}"
	@echo "  GUI Status:"
	@docker ps | grep -q "${gui_docker_name}"; \
	if [ $$? -eq 0 ]; then \
	  echo "    Running"; \
	else \
	  echo "    NOT running"; \
	fi;
	@echo "Mininet Status:"
	@docker ps | grep -q "${mn_docker_name}"; \
	if [ $$? -eq 0 ]; then \
	  echo "    Running"; \
	else \
	  echo "    NOT running"; \
	fi;
