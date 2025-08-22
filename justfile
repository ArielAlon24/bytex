test:
    pytest -vv .

lint:
    black .

check_lint:
    black --check .

ruff:
    ruff check .

mypy:
    mypy .
