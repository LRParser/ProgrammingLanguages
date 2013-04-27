CC=python
INTERPRET=interpreterext.py
PROGRAMEXT=programext.py

TEST_DIR=test
TEST_OUTPUT_DIR=$(TEST_DIR)/output
TEST_ANSWER_DIR=$(TEST_DIR)/answers
TEST_INPUT_DIR=$(TEST_DIR)/SampleInputs
TESTER=runtest.py
RUN_TEST=$(CC) $(TEST_DIR)/$(TESTER)
LINT_FILE=pylint.rc


.PHONY : clean test lint


lint: clean
	-pylint $(INTERPRET) $(PROGRAMEXT) --rcfile $(TEST_DIR)/$(LINT_FILE)
	-pychecker $(INTERPRET) $(PROGRAMEXT)


# This is the idea... but it needs to be cleaned up to handle a growing number of tests
test: clean
	@$(RUN_TEST)
	@echo "Checking answers"
	for test in `ls $(TEST_INPUT_DIR)/`; do \
		diff $(TEST_ANSWER_DIR)/$(test) $(TEST_OUTPUT_DIR)/$(test); \
	done

clean:
	@rm -f *.pyc *.out parsetab.py
	@rm -rf $(TEST_OUTPUT_DIR)


