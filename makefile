PYTHON=python

INTERPRET=interpreterext.py
PROGRAMEXT=programext.py
SCOPING=func_globals.py

SEMANTICS=semantics-description
IMPLEMENTATION=implementation-description

OBJS=$(INTERPRET) $(PROGRAMEXT) $(SCOPING)

TEST_DIR=test
CLASS_TEST_DIR=$(TEST_DIR)/class_tests/

TOP ?= $(shell pwd)

HOST=$(shell hostname)
ASSIGNMENT=Aoom

RELEASE_DIR=release
RELEASE_FILE=$(ASSIGNMENT).tar.gz


.PHONY : clean run view-code TAGS release view-tests

run-test =                                        \
	@for file in $(2)*;                       \
	do                                        \
		echo "\n*** Running $$file";      \
		$(1) < $$file;                    \
	done;

view-semantics:
	@more $(SEMANTICS)

view-implementation:
	@more $(IMPLEMENTATION)

view-tests:
	@more $(CLASS_TEST_DIR)* 

view-code: clean
	@more $(OBJS)

TAGS:
	@etags $(OBJS)


run: clean
	@echo "********************"
	@echo "Running Class Tests"
	@echo "********************"
	$(call run-test, $(PYTHON) $(INTERPRET), $(CLASS_TEST_DIR))



clean:
	@rm -f *.pyc *.out parsetab.py
	@rm -rf $(TEST_OUTPUT_DIR1)

release:
	@cd ..; \
	cp -R $(TOP) $(ASSIGNMENT); \
	tar -zcf $(RELEASE_FILE) --exclude .git $(ASSIGNMENT); \
	rm -rf $(ASSIGNMENT); \
	mkdir $(TOP)/$(RELEASE_DIR); \
	mv $(RELEASE_FILE) $(TOP)/$(RELEASE_DIR)
