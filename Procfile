web: gunicorn urlcounter:app
worker: celery worker -A urlcounter.celery --beat --loglevel=info
