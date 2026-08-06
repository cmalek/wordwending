VERSION = 0.1.0

PACKAGE = wordwending

#======================================================================


clean:
	rm -rf *.tar.gz dist *.egg-info *.rpm
	find . -name "*.pyc" -exec rm '{}' ';'
	find . -name "*.pyo" -exec rm '{}' ';'
	find . -name "*.pyd" -exec rm '{}' ';'
	find . -name "__pycache__" -exec rm -rf '{}' ';'
	rm -rf .pytest_cache
	rm -rf build
	rm -rf dist

dist: clean
	@python -m build --sdist --wheel

compile:
	@uv pip compile --extra docs pyproject.toml -o requirements.txt

release:
	@bin/release.sh

docs:
	@echo "Generating docs..."
	@cd doc && rm -rf build && make html
	@open doc/build/html/index.html

napoleon-gate:
	@.venv/bin/python bin/check_napoleon_gate.py

napoleon-gate-strict:
	@.venv/bin/python bin/check_napoleon_gate.py --strict

napoleon-gate-baseline:
	@.venv/bin/python bin/check_napoleon_gate.py --write-baseline


.PHONY: docs release compile dist clean list napoleon-gate napoleon-gate-strict napoleon-gate-baseline
list:
	@$(MAKE) -pRrq -f $(lastword $(MAKEFILE_LIST)) : 2>/dev/null | awk -v RS= -F: '/^# File/,/^# Finished Make data base/ {if ($$1 !~ "^[#.]") {print $$1}}' | sort | egrep -v -e '^[^[:alnum:]]' -e '^$@$$' | xargs
