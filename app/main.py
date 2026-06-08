# app/main.py
# uvicorn main:app --reload --port 8000

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware, # cors는 지정된 IP에서만 접근이 가능하도록 할 수 있습니다.
    allow_origins=["*"],  # 또는 ['http://localhost:3000'] 등
    allow_credentials=True,
    allow_methods=["*"],  # 또는 ['POST']
    allow_headers=["*"],
)


""" 파일을 http url로 제공합니다.
app.mount(
    "/v1/video-download", 
    StaticFiles(directory="/mnt/remote_nfs"), 
    name="video-download"
)
"""



# 서버 시작 시 딱 한 번 실행
# 개념: @app.on_event("startup") → 서버가 켜지는 순간 자동으로 실행되는 함수
#       init_db() 를 여기서 호출해야 memo.db 파일과 테이블이 자동으로 만들어집니다.
from services_v2.write import init_db

@app.on_event("startup")
async def startup():
    init_db()


# 라우터 등록
from services_v1 import write, read
app.include_router(read.router)
app.include_router(write.router)

from services_v2 import write, read
app.include_router(read.router)
app.include_router(write.router)
