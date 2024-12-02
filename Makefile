default: run

build:
	python -m venv .venv
	.venv/bin/pip install -r requirements.txt

run:
	.venv/bin/python src/main.py

run-info:
	.venv/bin/python src/main.py -v

run-debug:
	.venv/bin/python src/main.py -vv

clean:
	rm -rf .venv
