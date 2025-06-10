run:
	poetry run uvicorn main:app --reload

install:
	poetry install

migration:
	alembic revision --autogenerate -m "add times to stops"