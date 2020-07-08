curr_dir := $(shell pwd)
P4C_IMG := opennetworking/p4c:latest

docker_pull:
	docker pull ${P4C_IMG}

build-rate_limiter:
	$(info *** Compiling Rate Limiter...)
	@mkdir -p ./p4build/rate_limiter
	@docker run --rm -v ${curr_dir}:/opp -w /opp ${P4C_IMG} \
		p4c-bm2-ss --arch v1model -o ./p4build/rate_limiter/bmv2.json \
		--p4runtime-files ./p4build/rate_limiter/p4info.txt,p4build/rate_limiter/p4info.bin \
		--Wdisable=unsupported \
		./p4src/rate_limiter/rate_limiter.p4
	@echo "*** P4 program compiled successfully! Output files are in p4build/rate_limiter"
