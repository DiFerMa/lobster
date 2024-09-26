LOBSTER_ROOT:=../../..
LOBSTER_WIP:=$(LOBSTER_ROOT)/work-in-progress

PATH:=$(LOBSTER_ROOT)/test_install/bin:$(PATH)
PYTHONPATH:=$(wildcard $(LOBSTER_ROOT)/test_install/lib/python*/site-packages)

THIS_TEST:=$(shell realpath --relative-to $(LOBSTER_ROOT) $(PWD))
THIS_TEST_ESCAPED:=$(subst /,\\/,$(THIS_TEST))

html_report.html: gtests.lobster mcode.lobster system-requirements.lobster software-requirements.lobster lobster.conf pycode.lobster json.lobster
	@lobster-report
	@lobster-online-report
	@cp report.lobster report.reference_output
	@lobster-html-report
	@cp lobster_report.html ../../../docs/example_report.html
	@lobster-ci-report | tee ci_report.reference_output

gtests.lobster: foo.h foo.cpp test.cpp
	@bazel test foo_test --cxxopt='-std=c++14'
	-@coverage run -p --rcfile=$(LOBSTER_ROOT)/coverage.cfg --branch \
		--data-file $(LOBSTER_ROOT)/.coverage \
		$(LOBSTER_ROOT)/test_install/bin/lobster-gtest $(LOBSTER_ROOT)/bazel-out/*/testlogs/$(THIS_TEST) \
		--out="gtests.lobster"
	sed -i s/$(THIS_TEST_ESCAPED)\\///g gtests.lobster

mcode.lobster: nand.m nand_test.m exclusive_or.slx
	-@coverage run -p --rcfile=$(LOBSTER_ROOT)/coverage.cfg --branch \
		--data-file $(LOBSTER_ROOT)/.coverage \
		$(LOBSTER_ROOT)/test_install/bin/mh_trace *.m *.slx \
		--out-imp="mcode.lobster" \
		--out-act="mtests.lobster"

pycode.lobster: nor.py
	-@coverage run -p --rcfile=$(LOBSTER_ROOT)/coverage.cfg --branch \
		--data-file $(LOBSTER_ROOT)/.coverage \
		$(LOBSTER_ROOT)/test_install/bin/lobster-python *.py \
		--out="pycode.lobster" \
		--parse-decorator trlc_reference requirement

software-requirements.lobster: potato.rsl potato.check potato.trlc
	-@coverage run -p --rcfile=$(LOBSTER_ROOT)/coverage.cfg --branch \
		--data-file $(LOBSTER_ROOT)/.coverage \
		$(LOBSTER_ROOT)/test_install/bin/lobster-trlc *.rsl *.check *.trlc \
		--out="software-requirements.lobster"

json.lobster: example.json
	-@coverage run -p --rcfile=$(LOBSTER_ROOT)/coverage.cfg --branch \
		--data-file $(LOBSTER_ROOT)/.coverage \
		$(LOBSTER_ROOT)/test_install/bin/lobster-json example.json \
		--name-attribute "name" \
		--tag-attribute "tags" \
		--justification-attribute "justification" \
		--out="json.lobster"
