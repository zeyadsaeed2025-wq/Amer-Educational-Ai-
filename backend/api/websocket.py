import logging
from fastapi import WebSocket, WebSocketDisconnect
from typing import List, Dict
import json
from core.quality_engine import QualityEngine

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections with stability features."""
    
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.connection_counter = 0
    
    async def connect(self, websocket: WebSocket) -> str:
        """Connect a new WebSocket client."""
        await websocket.accept()
        conn_id = str(self.connection_counter)
        self.connection_counter += 1
        self.active_connections[conn_id] = websocket
        logger.info(f"WebSocket client connected: {conn_id}")
        return conn_id
    
    def disconnect(self, conn_id: str):
        """Disconnect a WebSocket client."""
        if conn_id in self.active_connections:
            del self.active_connections[conn_id]
            logger.info(f"WebSocket client disconnected: {conn_id}")
    
    async def send_json(self, message: dict, websocket: WebSocket):
        """Send JSON message to WebSocket."""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"WebSocket send error: {e}")
    
    def get_connection_count(self) -> int:
        """Get number of active connections."""
        return len(self.active_connections)


manager = ConnectionManager()
quality_engine = QualityEngine()


class WebSocketSession:
    """WebSocket session handler with debounce support."""
    
    def __init__(self, websocket: WebSocket):
        self.websocket = websocket
        self.last_analysis = ""
        self.analysis_count = 0
    
    async def handle_message(self, data: str) -> bool:
        """Handle incoming WebSocket message. Returns False to close connection."""
        try:
            message = json.loads(data)
            msg_type = message.get("type", "")
            
            if msg_type == "ping":
                await self._send({"type": "pong"})
                
            elif msg_type == "analyze":
                text = message.get("text", "")
                tab = message.get("tab", "standard")
                
                # Skip if same content (debounce)
                if text == self.last_analysis:
                    return True
                
                self.last_analysis = text
                self.analysis_count += 1
                
                if len(text) < 5:
                    await self._send({
                        "type": "error",
                        "message": "Text too short for analysis"
                    })
                    return True
                
                # Analyze content
                metrics = quality_engine.analyze(text, tab)
                
                response = {
                    "type": "quality_update",
                    "score": metrics.score,
                    "readability": metrics.readability,
                    "interactivity": metrics.interactivity,
                    "engagement": metrics.engagement,
                    "alerts": [{"type": a.type, "msg": a.msg} for a in metrics.alerts],
                    "suggestions": metrics.suggestions,
                    "analysis_count": self.analysis_count,
                }
                
                await self._send(response)
                
            elif msg_type == "clear":
                self.last_analysis = ""
                await self._send({"type": "cleared"})
                
            else:
                await self._send({
                    "type": "error",
                    "message": f"Unknown message type: {msg_type}"
                })
                
            return True
            
        except json.JSONDecodeError:
            await self._send({
                "type": "error",
                "message": "Invalid JSON format"
            })
            return True
            
        except Exception as e:
            logger.error(f"WebSocket message error: {e}")
            await self._send({
                "type": "error",
                "message": "Internal server error"
            })
            return False
    
    async def _send(self, message: dict):
        """Send message to client."""
        try:
            await self.websocket.send_json(message)
        except Exception as e:
            logger.error(f"Failed to send WebSocket message: {e}")


async def websocket_endpoint(websocket: WebSocket):
    """
    WebSocket endpoint for real-time content analysis.
    
    Features:
    - Debounce: Skips analysis if content unchanged
    - Rate limiting: Counts analysis requests
    - Error handling: Graceful error responses
    - Session tracking: Unique session per connection
    
    Client sends:
    - {"type": "ping"} → server sends {"type": "pong"}
    - {"type": "analyze", "text": "...", "tab": "..."} → server sends quality_update
    - {"type": "clear"} → server sends {"type": "cleared"}
    
    Server sends:
    - {"type": "quality_update", score, readability, ...}
    - {"type": "error", "message": "..."}
    """
    conn_id = await manager.connect(websocket)
    session = WebSocketSession(websocket)
    
    try:
        while True:
            try:
                # Wait for message with timeout
                data = await websocket.receive_text()
                
                # Handle message
                should_continue = await session.handle_message(data)
                if not should_continue:
                    break
                    
            except Exception as e:
                logger.error(f"WebSocket receive error: {e}")
                break
                
    except WebSocketDisconnect:
        logger.info(f"WebSocket client disconnected gracefully: {conn_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        manager.disconnect(conn_id)
