IMAGE_NAME=my_app
CONTAINER_NAME=my_app_container

lint:
	flake8
	black --check --diff .
	isort --check --diff .
	make type-check

type-check:
	python -m mypy --config-file setup.cfg --pretty TO_MIGRATE_puzzle_*
	python -m mypy --config-file setup.cfg --pretty puzzles

test:
	pytest . -vv

dev-test:
	pytest . -vv -s
