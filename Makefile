PYTHON	=	python3

all:
	@${PYTHON} scripts/allinone.py
	@${PYTHON} -m py_compile Answer/Answer.py

test: all
	@${PYTHON} Answer/Answer.py < tests/7154468337707171000
