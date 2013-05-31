PYTHON=python

INTERPRET=interpreterext.py
DYN_INTERP=dyn_interpret.py

PROGRAMEXT=programext.py
DYN_PROGRAM=dyn_program.py

OBJS=$(INTERPRET) $(PROGRAMEXT)
DYN_OBJS=$(DYN_INTERP) $(DYN_PROGRAM)

TEST_DIR=test
TEST_OUTPUT_DIR1=$(TEST_DIR)/output1
TEST_ANSWER_DIR1=$(TEST_DIR)/answers1
TEST_INPUT_DIR1=$(TEST_DIR)/SampleInputs1


TESTER1=runtest1.py

RUN_TEST1=$(PYTHON) $(TEST_DIR)/$(TESTER1)

FUNC1=$(TEST_INPUT_DIR1)/recLen.p
FUNC2=$(TEST_INPUT_DIR1)/iterList.p

TOP ?= $(shell pwd)

HOST=$(shell hostname)
ASSIGNMENT=A6

RELEASE_DIR=release
RELEASE_FILE=$(ASSIGNMENT).tar.gz

.PHONY : clean test view compile-static compile-dynamic TAGS release

view: clean
	@more $(OBJS) $(DYN_OBJS)

compile-static: clean

compile-dynamic: clean

run-static: clean
	@$(PYTHON) $(INTERPRET)

run-dynamic: clean
	@$(PYTHON) $(DYN_INTERP)

TAGS:
	@etags $(OBJS)

# This is the idea... but it needs to be cleaned up to handle a growing number of tests
test-part1: clean
	@$(RUN_TEST1)
	@echo "Checking answers"
	@diff $(TEST_ANSWER_DIR1) $(TEST_OUTPUT_DIR1)

test-part2: clean
	@$(RUN_TEST2)
	@echo "Checking answers"
	@diff $(TEST_ANSWER_DIR2) $(TEST_OUTPUT_DIR2)


test: test-part1 test-part2

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
