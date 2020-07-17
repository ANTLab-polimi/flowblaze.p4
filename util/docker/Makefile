include Makefile.vars

build: build_flask build_p4mn

build_flask:
	cd flask && docker build -t ${FLASK_IMG} .

build_p4mn:
	cd p4mn && docker build -t ${P4MN_IMG} .

push: push_flask push_p4mn

push_flask:
	docker push ${FLASK_IMG}

push_p4mn:
	docker push ${P4MN_IMG}
