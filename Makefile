default: run

install:
	python3 -m venv env
	env/bin/pip install -r requirements.txt

clean:
	rm -rf env

run:
	env/bin/python src/main.py

run-v:
	env/bin/python src/main.py -v

run-vv:
	env/bin/python src/main.py -vv
