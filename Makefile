SRC_DIR     = ./coi

.PHONY: test cover

cover:
	nosetests --with-coverage --cover-package=coi --cover-html --cover-inclusive .

test:
	cd test && nosetests
