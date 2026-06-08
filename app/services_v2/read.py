from utils.utils import *
import sqlite3  # sqlite3가 없으면 DB 연결 자체가 안 됨!


DB_PATH = "memo.db"  # write.py 와 같은 파일을 바라봐야 같은 DB 사용

router = APIRouter( prefix="/v2/read", tags=["user"])



# ------------------------------------------------------------------
class Example(BaseModel):
    param1: str
@router.post("/example")
@safe_exec
async def example(req: Example):
    return {"result": req.param1}


#1. sqllite3 : crud

# ── READ ALL : 전체 메모 조회 ─────────────────────────────────────
# 개념: DB에 저장된 메모를 전부 가져옵니다.
#       fetchall() → 조건에 맞는 행 전부 → 리스트로 반환
#
# 요청: GET /v2/read/memos
# 응답: [{"id":1, "title":"...", ...}, {"id":2, ...}, ...]

@router.get("/memos")
@safe_exec
async def get_all_memos():
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, title, content, created_at FROM memos ORDER BY id DESC"
        # ORDER BY id DESC → id가 큰 순서 (최신순) 으로 정렬
    )
    rows = cursor.fetchall()
    # rows = [(1, "제목", "내용", "2026-06-04"), (2, ...), ...]
    conn.close()

    return [
        {"id": r[0], "title": r[1], "content": r[2], "created_at": r[3]}
        for r in rows
        # r[0], r[1]... → SELECT 한 순서대로 인덱스로 접근
    ]


# ── READ ONE : 특정 메모 1개 조회 ────────────────────────────────
# 개념: id를 URL에서 받아서 그 행만 가져옵니다.
#       fetchone() → 조건에 맞는 행 1개만 → 튜플 or None 반환
#
# 요청: GET /v2/read/memo/1   (← URL 끝에 id 숫자를 붙임)
# 응답: {"id":1, "title":"...", "content":"...", "created_at":"..."}

@router.get("/memo/{memo_id}")
@safe_exec
async def get_memo(memo_id: int):
    # {memo_id} → URL에서 자동으로 받아옴
    # 예: GET /v2/read/memo/3  →  memo_id = 3
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, title, content, created_at FROM memos WHERE id=?",
        (memo_id,)
    )
    row = cursor.fetchone()  # 없으면 None 반환
    conn.close()

    if row is None:
        return {"message": f"id {memo_id} 메모 없음"}
    return {"id": row[0], "title": row[1], "content": row[2], "created_at": row[3]}