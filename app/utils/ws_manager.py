
from fastapi import WebSocket
import asyncio
import time
from utils import safe_exec
# 실시간 통신이 필요할 경우 websocket 사용

class WebSocketManager:
    def __init__(self):
        self.sessions: dict = {}
        asyncio.create_task(self._cleanup)


    @safe_exec
    async def _cleanup(self):
        async def clean_room (self, session_id, timeout):
            session = self.sessions.get(session_id)
            current_time = time.time()
            if current_time - session['updated_time'] > timeout:
                for ws in session['connections']:
                    try: await ws.close(code=1000, reason="session_timeout")
                    except: pass
                if session_id in self.sessions:
                    del self.sessions[session_id]
                print(f"Cleanup: Timeout room {session_id} removed")
                
        while True:
            await asyncio.sleep(60)
            for session_id in list(self.sessions.keys()):
                session = self.sessions.get(session_id)
                if not session: continue
                
                num_conns = len(session['connections'])
                if   num_conns == 0: await clean_room(self, session_id, 1) # 0명, 즉시 방삭제
                elif num_conns == 1: await clean_room(self, session_id, 3600) # 1명, 1시간
                elif num_conns >  2: await clean_room(self, session_id, 3600*24) # 2명이상, 24시간




    @safe_exec
    async def create_session(self, session_id:str):
        print(session_id)
        if session_id not in self.sessions: # 새로운 세션(채팅방) 열기
            self.sessions[session_id] = {
                'connections':[], 'data':{}, 'session_id': session_id, 'updated_time': time.time()}
            print(f"room:{session_id} create")




    @safe_exec
    async def connect(self, websocket: WebSocket, session_id: str):
        await websocket.accept()
        if session_id in self.sessions: # 세션 검색
            self.sessions[session_id]['connections'].append(websocket) # 유저 추가
            print(f"room:{session_id} user connect {self.sessions[session_id]['connections']}")
            return self.sessions[session_id]
        else:
            print(f"room:{session_id} didn't created")
            return None




    @safe_exec
    async def disconnect(self, websocket: WebSocket, session_id: str):
        session = self.sessions.get(session_id)
        if session:
            if websocket in session['connections']:
                session['connections'].remove(websocket)
                print(f"room:{session_id} user removed")
        print(f"room:{session_id} {websocket} disconnect process complete")




    @safe_exec
    async def send_all_message (self, websocket: WebSocket, message: str):
        for session_id in self.sessions.keys():
            await self.send_room_message(websocket, message, session_id)




    @safe_exec
    async def send_room_message (self, websocket: WebSocket, message: any, session_id: str):
        self.sessions[session_id]['updated_time'] = time.time()
        connections = self.sessions[session_id]['connections']
        tasks = []
        for connection in connections: 
            if connection == websocket: continue
            if isinstance(message, str): tasks.append(connection.send_text(message))
            else: tasks.append(connection.send_bytes(message))
        if tasks: await asyncio.gather(*tasks, return_exceptions=True)
            



ws_manager = WebSocketManager()

