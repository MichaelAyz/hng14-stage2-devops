# HNG Stage 2 DevOps App

A simple Job Processing system. It has four main parts:
- A Node.js Express frontend
- A FastAPI Python API
- A Python background worker
- A Redis database

Everything is containerized and fully orchestrated using Docker Compose.

## Prerequisites
- Docker Engine installed (v20.10 or newer)
- Docker Compose installed (v2.0 or newer)

## Startup Instructions
To run this project on your computer:

1. Clone the repository and go into the folder:
   ```bash
   git clone https://github.com/MichaelAyz/hng14-stage2-devops.git
   cd hng14-stage2-devops
   ```

2. Create a `.env` file by copying the example file:
   ```bash
   cp .env.example .env
   ```

3. Build and start the containers:
   ```bash
   docker-compose up -d --build
   ```

## Checking the Status
To make sure everything is working, run:
```bash
docker-compose ps
```

You should see an output that looks like this:
```text
NAME                     IMAGE                       COMMAND                  SERVICE    STATUS
hng14-stage2-redis-1     redis:7-alpine             "docker-entrypoint.s…"   redis      Up 2 minutes (healthy)
hng14-stage2-api-1       hng14-stage2-devops-api    "uvicorn main:app --…"   api        Up 2 minutes (healthy)
hng14-stage2-worker-1    hng14-stage2-devops-worker "python worker.py"       worker     Up 2 minutes (healthy)
hng14-stage2-frontend-1  hng14-stage2-devops-frontend "node app.js"          frontend   Up 2 minutes (healthy)
```

Wait until all 4 containers (`redis`, `api`, `worker`, `frontend`) show as `(healthy)`.

## How to Test
1. Open your browser and go to `http://localhost:3000` or run this command:
   ```bash
   curl -X POST http://localhost:3000/submit
   ```
2. You will get a `job_id`. You can check the status of your job at:
   `http://localhost:3000/status/<job_id>`
