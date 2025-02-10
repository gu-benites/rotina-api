# gunicorn_conf.py

# Bind o servidor na porta 9011 e em todas as interfaces
bind = "0.0.0.0:9011"

# Número de workers (ajuste conforme a carga esperada)
workers = 2

# Define que o Gunicorn deverá usar os uvicorn workers para suportar ASGI (FastAPI)
worker_class = "uvicorn.workers.UvicornWorker"

# Tempo máximo de espera para uma resposta
timeout = 120

# Nível de log (opcional)
loglevel = "info" 