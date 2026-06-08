from utils.utils import *

router = APIRouter( prefix="/v2/write", tags=["user"])



# ------------------------------------------------------------------
class Example(BaseModel):
    param1: str
@router.post("/example")
@safe_exec
async def example(req: Example):
    return {"result": req.param1}



#1. sqllite3 : crud
import sqlite3

# DB 파일 경로 (서버 실행하면 이 파일이 자동 생성됩니다)
DB_PATH = "memo.db"


def init_db():
    """서버 시작 시 딱 한 번 실행 → 테이블이 없으면 만들어줌
    
    [테이블 구조]
    id         : 1, 2, 3... 자동으로 붙는 고유 번호
    title      : 메모 제목~
    content    : 메모 내용
    created_at : 저장된 시각 (자동 기록)
    """
    conn = sqlite3.connect(DB_PATH)   # DB 파일 열기 (없으면 자동 생성)
    cursor = conn.cursor()            # SQL 명령을 보내는 도구
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memos (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            title      TEXT    NOT NULL,
            content    TEXT    NOT NULL,
            created_at TEXT    DEFAULT (datetime('now','localtime'))
        )
    """)
    conn.commit()  # 변경사항 저장 (commit 안 하면 반영 안 됨!)
    conn.close()   # 연결 닫기


# ── CREATE : 메모 저장 ────────────────────────────────────────────
# 개념: 클라이언트가 POST /v2/write/memo 로 JSON을 보내면
#       DB에 새 행(row)을 INSERT 합니다.

class MemoCreate(BaseModel):
    title:   str
    content: str

@router.post("/memo")
@safe_exec
async def create_memo(req: MemoCreate):
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO memos (title, content) VALUES (?, ?)",
        (req.title, req.content)
        # ? 는 placeholder — 값을 직접 문자열로 넣으면 SQL Injection 위험!
        # 항상 ? 로 분리해서 넣어야 합니다.
    )
    conn.commit()
    new_id = cursor.lastrowid  # 방금 저장된 행의 id
    conn.close()
    return {"id": new_id, "message": "메모 저장 완료"}


# ── UPDATE : 메모 수정 ────────────────────────────────────────────
# 개념: id를 받아서 그 행만 UPDATE 합니다.
#       WHERE 없으면 전체 수정되니 조심!

class MemoUpdate(BaseModel):
    id:      int
    title:   str
    content: str

@router.post("/memo/update")
@safe_exec
async def update_memo(req: MemoUpdate):
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE memos SET title=?, content=? WHERE id=?",
        (req.title, req.content, req.id)
    )
    conn.commit()
    affected = cursor.rowcount  # 실제로 수정된 행 수 (0이면 id 없음)
    conn.close()
    if affected == 0:
        return {"message": f"id {req.id} 메모 없음"}
    return {"message": f"id {req.id} 수정 완료"}


# ── DELETE : 메모 삭제 ────────────────────────────────────────────
# 개념: id를 받아서 그 행만 DELETE 합니다.

class MemoDelete(BaseModel):
    id: int

@router.post("/memo/delete")
@safe_exec
async def delete_memo(req: MemoDelete):
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "DELETE FROM memos WHERE id=?",
        (req.id,)
        # (req.id,) ← 값이 1개인 튜플은 뒤에 , 를 붙여야 해요
    )
    conn.commit()
    affected = cursor.rowcount
    conn.close()
    if affected == 0:
        return {"message": f"id {req.id} 메모 없음"}
    return {"message": f"id {req.id} 삭제 완료"}