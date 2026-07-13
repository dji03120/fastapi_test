<div align="center">

![Header](https://capsule-render.vercel.app/api?type=waving&color=0:0F172A,100:1E3A8A&height=150&section=header&text=fastapi_test&fontSize=36&fontColor=E2E8F0&animation=fadeIn&fontAlignY=38)

**FastAPI playground for API structure design and Docker deployment practice**

[![FastAPI](https://img.shields.io/badge/FastAPI-0F172A?style=for-the-badge&logo=fastapi&logoColor=00C7B7)](#)
[![Python](https://img.shields.io/badge/Python-0F172A?style=for-the-badge&logo=python&logoColor=3776AB)](#)
[![Docker](https://img.shields.io/badge/Docker-0F172A?style=for-the-badge&logo=docker&logoColor=2496ED)](#)
[![SQLite](https://img.shields.io/badge/SQLite-0F172A?style=for-the-badge&logo=sqlite&logoColor=003B57)](#)

</div>

<br>

## Overview

A learning repository for getting comfortable with how a real FastAPI service is structured and how to ship it in a container. Rather than one throwaway script, it covers pieces used on the job: versioned routing, a small CRUD backend, real-time communication, cross-origin setup, and containerization.

<br>

<details>
<summary><b>⚡ Project Details</b></summary>
<br>

| Category | Detail |
|:---|:---|
| **Stack** | FastAPI, Python, SQLite, Docker |
| **Scope** | API structure practice, not a production service |
| **Key Areas** | Versioned routers, CRUD, WebSocket, CORS, containerization |

**Key Features**
- Versioned routers (e.g. `/v1`) for clean, extensible structure
- SQLite-backed CRUD endpoints
- WebSocket endpoint for real-time bidirectional communication
- CORS configuration for front-end integration
- Dockerfile for consistent, reproducible runs

</details>

<br>

## What I Learned

- Structuring a FastAPI project with routers, dependencies, and versioning instead of a flat file
- Basic CRUD design and request/response modeling with Pydantic
- How WebSocket differs from request/response, and when to use it
- Packaging a Python service into a Docker image

<br>

## Getting Started

```bash
uvicorn app.main:app --reload
# or
docker build -t fastapi_test .
docker run -p 8000:8000 fastapi_test
```

API 문서: `http://localhost:8000/docs`

<br>

<div align="center">

![Footer](https://capsule-render.vercel.app/api?type=waving&color=0:1E3A8A,100:0F172A&height=90&section=footer)

</div>
