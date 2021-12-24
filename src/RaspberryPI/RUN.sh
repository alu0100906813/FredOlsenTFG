
# NOTA: SOLO FUNCIONA BIEN CON UN WORKER
gunicorn --bind 0.0.0.0:5000 wsgi:app