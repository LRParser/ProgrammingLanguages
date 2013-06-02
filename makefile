PYTHON=python

INTERPRET=interpreterext.py
PROGRAMEXT=programext.py

OBJS=$(INTERPRET) $(PROGRAMEXT)

DYN_INTERPET=$(INTERPRET) --dynamic-scope

TEST_DIR=test
STATIC_TEST_DIR=$(TEST_DIR)/static_tests/
DYNAMIC_TEST_DIR=$(TEST_DIR)/dyn_tests/


TOP ?= $(shell pwd)

HOST=$(shell hostname)
ASSIGNMENT=A6

RELEASE_DIR=release
RELEASE_FILE=$(ASSIGNMENT).tar.gz


.PHONY : clean test view compile-static compile-dynamic TAGS release

run-test =                                        \
	@for file in $(2)*;                       \
	do                                        \
		echo "\n*** Running $$file";      \
		$(1) < $$file;                    \
	done;



view: clean
	@more $(OBJS)

compile-static: clean

compile-dynamic: clean

run-static: clean
	@$(PYTHON) $(INTERPRET)

run-dynamic: clean
	@$(PYTHON) $(DYN_INTERPET)

TAGS:
	@etags $(OBJS)


test: clean
	@echo "********************"
	@echo "Running Static Tests"
	@echo "********************"
	$(call run-test, $(PYTHON) $(INTERPRET), $(STATIC_TEST_DIR))

	@echo "********************"
	@echo "Running Dynamic Tests"
	@echo "********************"
	$(call run-test, $(PYTHON) $(DYN_INTERPET), $(DYNAMIC_TEST_DIR))



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
