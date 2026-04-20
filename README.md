# HNG Stage 2 DevOps App

A robust multi-service Job Processing system comprised of a Node.js Express frontend, a FastAPI python API, a python backend worker, and a shared Redis node natively containerized with Docker and fully orchestrated employing Docker-Compose.

## Prerequisites
- Docker Engine installed.
- Docker Compose installed.

## Startup Instructions
To bring the entire pristine stack up cleanly on a fresh machine:
1. Ensure your `.env` is initialized at the repository root mimicking `.env.example`:
   ```bash
   cp .env.example .env
   ```
2. Build and launch the cluster utilizing compose:
   ```bash
   docker-compose up -d --build
   ```

## What a Successful Startup Looks Like
Ensure all components correctly spun up:
```bash
docker-compose ps
```
The output should list 4 containers (`redis`, `api`, `worker`, `frontend`) transitioning gracefully from `(health: starting)` to `(healthy)`.
You can visit `http://localhost:3000` via your browser or seamlessly execute:
```bash
curl -X POST http://localhost:3000/submit
```
And continuously poll the generated identifier safely at `http://localhost:3000/status/<job_id>`.
