# Analyze the given Python modules and compute Cyclomatic Complexity
cc_json = "$(shell radon cc --min C src --json)"
# Analyze the given Python modules and compute the Maintainability Index
mi_json = "$(shell radon mi --min B src --json)"

lint:
	pylint ./src

fmt:
	black ./src

test:
	python -m unittest discover -s tests -v

install:
	pip3 install pylint black radon
	pip3 install -r layers/reqs/requirements.txt && npm i

venv:
	virtualenv venv --python=python3.8

run:
	sls offline start

complexity:
	@echo "Complexity check..."

ifneq ($(cc_json), "{}")
	@echo
	@echo "Complexity issues"
	@echo "-----------------"
	@echo $(cc_json)
endif

ifneq ($(mi_json), "{}")
	@echo
	@echo "Maintainability issues"
	@echo "----------------------"
	@echo $(mi_json)
endif

ifneq ($(cc_json), "{}")
	@echo
	exit 1
else
ifneq ($(mi_json), "{}")
	@echo
	exit 1
endif
endif

	@echo "OK"
.PHONY: complexity
