import multiprocessing

# gunicorn -c gunicorn.conf.py app:server

bind = "0.0.0.0:8000"

workers = 1

# Worker timeout in seconds
timeout = 300