import multiprocessing

bind = "0.0.0.0:8000"

workers = multiprocessing.cpu_count()

# Type of worker process (e.g., 'sync', 'eventlet', 'gevent')
worker_class = "sync"

# Access log file (use '-' for stdout)
accesslog = "-"

# Error log file (use '-' for stderr)
errorlog = "-"

# Restart workers after a certain number of requests (to mitigate memory leaks)
max_requests = 1000
max_requests_jitter = 50

# Worker timeout in seconds
timeout = 300