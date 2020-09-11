
curr_dir := $(shell pwd)
APP_VERSION = 0.0.1-SNAPSHOT
APP_NAME = flowblaze-app
APP_OAR = app/target/${APP_NAME}-${APP_VERSION}.oar

build-app:
	mvn clean install

$(APP_OAR):
	$(error Missing app binary, run 'make app-build' first)

push-app: $(APP_OAR)
	$(info ************ RELOADING ONOS APP ************)
	onos-app localhost reinstall! ${APP_OAR}

push-netcfg:
	onos-netcfg localhost topo/netcfg.json

start:
	docker-compose up -d

stop:
	docker-compose down

onos-log:
	docker-compose logs -f onos

mn-log:
	docker-compose logs -f mininet

onos-cli:
	ssh -o "UserKnownHostsFile=/dev/null" -o "StrictHostKeyChecking=no" -p 8101 onos@localhost

leaf1_shell:
	docker exec -it mininet_onos /bin/sh -c 'simple_switch_CLI --thrift-port $$(cat /tmp/bmv2-s1-thrift-port)'

mn-cli:
	$(info ******* Ctrl+A Ctrl+D to detach *******)
	docker-compose exec mininet screen -Urx -S cli

h1-cli:
	docker-compose exec mininet /mininet/util/m h1

h2-cli:
	docker-compose exec mininet /mininet/util/m h1

h1-test:
	@docker-compose exec mininet /bin/sh -c '/mn_onos/utils/h1-iperf-test_udp.sh'

h2-test:
	@docker-compose exec mininet /bin/sh -c '/mn_onos/utils/h2-iperf-test_udp.sh'

p4runtime_shell:
	docker run -ti --rm p4lang/p4runtime-sh \
      --grpc-addr 172.28.0.2:50001 \
      --device-id 1 --election-id 0,1
