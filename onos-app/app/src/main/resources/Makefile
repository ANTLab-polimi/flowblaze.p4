all: copy_flowblaze_lib fabric-flowblaze

copy_flowblaze_lib:
	$(info ## Copy FlowBlaze lib... )
	@cp -r ../../../../../p4src/flowblaze_lib .

fabric-flowblaze:
	@./bmv2-compile.sh "fabric-flowblaze" ""

clean:
	rm -rf p4c-out/*/bmv2
	rm -rf flowblaze_lib
