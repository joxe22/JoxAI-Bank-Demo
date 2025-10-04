#!/usr/bin/env python3
"""Test WebSocket connection with JWT authentication"""

import asyncio
import websockets
import json
import httpx

async def test_websocket():
    print("=== Testing WebSocket Connection ===\n")
    
    print("1. Getting JWT token...")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:5000/api/v1/auth/login",
            json={"email": "admin@joxai.com", "password": "admin123"}
        )
        token = response.json()["token"]
        print(f"   ✓ Got token: {token[:20]}...\n")
    
    print("2. Connecting to WebSocket...")
    ws_url = f"ws://localhost:5000/api/v1/ws?token={token}"
    
    try:
        async with websockets.connect(ws_url) as websocket:
            print("   ✓ Connected successfully!\n")
            
            print("3. Waiting for connection_established message...")
            message = await websocket.recv()
            data = json.loads(message)
            print(f"   ✓ Received: {json.dumps(data, indent=2)}\n")
            
            print("4. Sending ping...")
            await websocket.send(json.dumps({
                "type": "ping",
                "timestamp": "2025-10-04T19:30:00"
            }))
            
            print("5. Waiting for pong...")
            message = await websocket.recv()
            data = json.loads(message)
            print(f"   ✓ Received: {json.dumps(data, indent=2)}\n")
            
            print("6. Requesting connection stats (admin only)...")
            await websocket.send(json.dumps({"type": "get_stats"}))
            
            message = await websocket.recv()
            data = json.loads(message)
            print(f"   ✓ Stats: {json.dumps(data, indent=2)}\n")
            
            print("✅ All WebSocket tests passed!\n")
            
    except websockets.exceptions.WebSocketException as e:
        print(f"   ✗ WebSocket error: {e}\n")
    except Exception as e:
        print(f"   ✗ Error: {e}\n")

if __name__ == "__main__":
    asyncio.run(test_websocket())
