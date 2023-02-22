migrate:
	python src/manage.py db upgrade head

run_server:
	gunicorn -b 0.0.0.0:5000 --workers 4 src.pywsgi:app

run_func_tests:
	pytest tests/functional/src/
