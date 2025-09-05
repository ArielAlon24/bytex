test:
    pytest .

lint:
    black .

check_lint:
    black --check .

ruff:
    ruff check .

mypy:
    mypy .
