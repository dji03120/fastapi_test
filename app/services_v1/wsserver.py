# 실시간 통신이 필요할 경우 사용
from utils.utils import *
from utils.ws_manager import ws_manager

router = APIRouter( prefix="/ws", tags=["web_socket"])



@router.get("/create-session")
async def create_session():
    session_id = str(uuid.uuid4())
    await ws_manager.create_session(session_id=session_id)
    return JSONResponse(content={"session_id": session_id})





@router.websocket("/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    sess = await ws_manager.connect(websocket, session_id)
    if not sess:  await websocket.close(code=1001); return
    
    try:
        sess_data = sess['data']
        while True:
            data = await websocket.receive_text() 
            if sess_data['message'] == "quit": break
            await ws_manager.send_room_message(websocket, f"Echo: {data}")
            
    except WebSocketDisconnect:
        print(f"Client disconnected: {session_id}")
    finally:
        await ws_manager.disconnect(websocket, session_id)
    
    