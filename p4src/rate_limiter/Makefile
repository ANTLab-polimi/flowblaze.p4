include ../../util/docker/Makefile.vars

curr_dir := $(shell pwd)

start:
	docker run --privileged -it -d --rm --name rate_limiter \
	-v ${curr_dir}/../../p4build/rate_limiter:/p4build \
	-v ${curr_dir}:/rate_limiter \
	--entrypoint /rate_limiter/topo.py \
	${P4MN_IMG}

stop:
	docker stop -t0 rate_limiter

attach-mininet:
	$(info ******* To detach CTRL+P followed by CTRL+Q *******)
	@docker attach rate_limiter

s1-CLI:
	$(info *** Opening S1 Switch runtime CLI \(THRIFT\))
	@docker exec -it rate_limiter /bin/sh -c 'simple_switch_CLI --thrift-port $$(cat /tmp/bmv2-s1-thrift-port)'

h1-shell:
	$(info *** Opening H1 shell)
	@docker exec -it rate_limiter /mininet/util/m h1

h2-shell:
	$(info *** Opening H2 shell)
	@docker exec -it rate_limiter /mininet/util/m h2