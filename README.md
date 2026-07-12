# fastapi_test

A hands-on FastAPI playground for learning how to structure a backend API and deploy it with Docker. Built while working through the basics of routing, versioned service modules, database access, real-time communication, and containerized deployment.

## What It Covers

- **Versioned routers** — `services_v1` and `services_v2` split endpoints into separate router modules, registered in `main.py` with `include_router`.
- **SQLite CRUD** — a simple memo table (`init_db()`) is created automatically on server startup, used to practice basic create/read/update/delete flows.
- **WebSocket server** — `wsserver.py` demonstrates session creation and a real-time echo endpoint using a connection manager.
- **CORS middleware** — configured so the API can be called from a separate frontend.
- **Docker deployment** — the `sample/` folder contains a `Dockerfile`, `docker-compose.yaml`, and `Jenkinsfile` for building and running the API in a container and testing remote access.

## Tech Stack

FastAPI · Uvicorn · SQLite · WebSocket · Docker / docker-compose

## Project Structure

```
app/
  main.py                FastAPI entry point, CORS + router registration
    config.py
      services_v1/           v1 routers (read, write, websocket server)
        services_v2/           v2 routers + SQLite CRUD (init_db, memos table)
          utils/                 shared helpers, logger, WebSocket manager
            sample/                Docker / docker-compose / Jenkins deploy examples
            ```

            ## Run Locally

            ```bash
            pip install -r app/sample/requirements.txt
            cd app
            uvicorn main:app --reload --port 8000
            ```

            Then open `http://localhost:8000/docs` for the auto-generated Swagger UI.

            ## Run with Docker

            ```bash
            cd app/sample
            docker compose up --build
            ```

            ## Notes

            This is a learning/experimentation repository, not a production service. The goal was to get comfortable with FastAPI's structure and the Docker deployment workflow before building larger API projects.
            
