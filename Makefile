install:
	pip install --upgrade pip &&\
		pip install -r req.txt

test:
	python -m pytest -vv ./test/test_main.py
