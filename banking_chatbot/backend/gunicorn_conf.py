# Gunicorn production configuration for Replit Autoscale
import multiprocessing
import os

# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker processes
workers = int(os.getenv("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
max_requests = 1000  # Restart workers after this many requests (prevents memory leaks)
max_requests_jitter = 50  # Add randomness to max_requests to avoid all workers restarting at once

# Timeouts
timeout = 120  # Worker timeout (2 minutes for long-running requests)
graceful_timeout = 30  # Time to finish processing before forcefully killing
keepalive = 5  # Seconds to wait for requests on a Keep-Alive connection

# Process naming
proc_name = "joxai-banking-chatbot"

# Logging
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr
loglevel = os.getenv("LOG_LEVEL", "info")
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (if needed in future)
keyfile = None
certfile = None

# Performance tuning
preload_app = True  # Load application before forking workers (saves memory)
reuse_port = True   # Enable SO_REUSEPORT for better load balancing

def on_starting(server):
    """Called just before the master process is initialized."""
    server.log.info("Gunicorn is starting JoxAI Banking Chatbot...")

def when_ready(server):
    """Called just after the server is started."""
    server.log.info(f"Gunicorn is ready. Listening on: {bind}")
    server.log.info(f"Workers: {workers}, Worker class: {worker_class}")

def on_exit(server):
    """Called just before exiting Gunicorn."""
    server.log.info("Gunicorn is shutting down...")

def worker_int(worker):
    """Called when a worker receives the SIGINT or SIGQUIT signal."""
    worker.log.info(f"Worker {worker.pid} received SIGINT/SIGQUIT")

def pre_fork(server, worker):
    """Called just before a worker is forked."""
    pass

def post_fork(server, worker):
    """Called just after a worker has been forked."""
    server.log.info(f"Worker spawned (pid: {worker.pid})")

def worker_abort(worker):
    """Called when a worker times out."""
    worker.log.error(f"Worker timeout (pid: {worker.pid})")
