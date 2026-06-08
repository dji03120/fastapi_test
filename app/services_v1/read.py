from utils.utils import *

router = APIRouter( prefix="/v1/read", tags=["user"])



# ------------------------------------------------------------------
class Example(BaseModel):
    param1: str
@router.post("/example")
@safe_exec
async def example(req: Example):
    return {"result": req.param1}

