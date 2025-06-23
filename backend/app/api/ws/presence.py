from fastapi import APIRouter, WebSocket

router = APIRouter()

# Example WebSocket endpoint for presence (replace with real logic later)
@router.websocket("/presence")
async def websocket_presence(websocket: WebSocket):
    """
    Example WebSocket endpoint for user presence.
    Accepts a connection and echoes messages back.
    """
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Echo: {data}")
    except Exception as e:
        # Connection closed or error
        pass