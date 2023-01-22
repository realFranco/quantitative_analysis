all:
	@ echo "You must define an option: 'install', 'test', 'tuning' or 'run'.\n"
.PHONY: all

install:
	@ cd web_service/backend && \
		python3 -m venv venv && \
		source venv/bin/activate && \
		pip3 install -r requirements.in
.PHONY: install

test:
	@ cd web_service/backend && \
		source venv/bin/activate && \
		python3 -m pytest test/
.PHONY: test

tuning:
	@ cd web_service/backend && \
		source venv/bin/activate && \
		python3 src/tuning.py
.PHONY: tuning

run:
	@ cd web_service/backend && \
		source venv/bin/activate && \
		uvicorn main:app --reload
.PHONY: run
