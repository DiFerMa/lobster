LOBSTER_ROOT:=../../..
LOBSTER_WIP:=$(LOBSTER_ROOT)/work-in-progress

PATH:=$(LOBSTER_ROOT)/test_install/bin:$(PATH)
PYTHONPATH:=$(wildcard $(LOBSTER_ROOT)/test_install/lib/python*/site-packages)

THIS_TEST:=$(shell realpath --relative-to $(LOBSTER_ROOT) $(PWD))
THIS_TEST_ESCAPED:=$(subst /,\\/,$(THIS_TEST))

html_report.html: requirements.lobster lobster.conf json.lobster
	@lobster-report
	@lobster-online-report
	@cp report.lobster report.reference_output
	@lobster-html-report

requirements.lobster: example.rsl softreq_example.trlc sysreq_example.trlc
	-@coverage run -p --rcfile=$(LOBSTER_ROOT)/coverage.cfg --branch \
		--data-file $(LOBSTER_ROOT)/.coverage \
		$(LOBSTER_ROOT)/test_install/bin/lobster-trlc example.rsl softreq_example.trlc sysreq_example.trlc \
		--out="requirements.lobster"

json.lobster: test_example.json
	-@coverage run -p --rcfile=$(LOBSTER_ROOT)/coverage.cfg --branch \
		--data-file $(LOBSTER_ROOT)/.coverage \
		$(LOBSTER_ROOT)/test_install/bin/lobster-json test_example.json \
		--name-attribute "name" \
		--tag-attribute "tags" \
		--justification-attribute "justification" \
		--out="json.lobster"
