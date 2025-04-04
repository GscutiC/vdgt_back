from flask import request

def request_logger():
    """Middleware to log incoming requests."""
    print(f"Incoming request: {request.method} {request.path}")