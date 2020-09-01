
curr_dir := $(shell pwd)
APP_VERSION = 0.0.1-SNAPSHOT
APP_NAME = flowblaze-app
APP_OAR = app/target/${APP_NAME}-${APP_VERSION}.oar

build-app:
	mvn clean package

$(APP_OAR):
	$(error Missing app binary, run 'make app-build' first)

push-app: $(APP_OAR)
	$(info ************ RELOADING ONOS APP ************)
	onos-app localhost reinstall! ${APP_OAR}

push-netcfg:
	onos-netcfg localhost netcfg.json

start-onos:
	$(info *** Running ONOS ***)
	docker run -t --rm -d -p 8181:8181 -p 8101:8101 -p 5005:5005 -p 830:830 --name onos -e ONOS_APPS=drivers,gui,openflow,segmentrouting,drivers.stratum,pipelines.fabric onosproject/onos:2.2.3

stop-onos:
	docker stop -t0 onos

onos-cli:
	ssh -o "UserKnownHostsFile=/dev/null" -o "StrictHostKeyChecking=no" -p 8101 onos@localhost

start-mininet:
	$(info *** Running topo.py Mininet topology)
	docker run --privileged -it -d --rm --name mininet_onos \
    	-v ${curr_dir}:/mn_onos \
    	--entrypoint /mn_onos/topo.py \
    	dmoro92/p4mn:latest

stop-mininet:
	docker stop -t0 mininet_onos | true

attach-mininet:
	$(info ******* To detach CTRL+P followed by CTRL+Q *******)
	@docker attach mininet_onos

p4runtime_shell:
	docker run -ti p4lang/p4runtime-sh \
      --grpc-addr 172.17.0.2:50001 \
      --device-id 1 --election-id 0,1

