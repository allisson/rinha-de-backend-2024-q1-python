.PHONY: lint
lint:
	poetry run pre-commit run --all-files

.PHONY: build-image
build-image:
	docker build --rm -t allisson/rinha-2024-q1-python .

.PHONY: run-server
run-server:
	poetry run python rinha_2024_q1/main.py
