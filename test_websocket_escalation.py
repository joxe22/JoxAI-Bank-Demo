#!/usr/bin/env python3
"""
Test script to verify WebSocket escalation notifications work end-to-end.
This demonstrates that when a chat conversation is escalated, admin clients
receive real-time WebSocket notifications.
"""
import asyncio
import websockets
import json
import httpx

async def test_escalation_notification():
    # Step 0: Login to get valid JWT token
    print("\n✅ Step 0: Getting admin JWT token...")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:5000/api/v1/auth/login",
            json={"email": "admin@joxai.com", "password": "admin123"}
        )
        login_data = response.json()
        token = login_data["token"]
        print(f"   Token obtained for: {login_data['user']['email']}")
    
    # Step 1: Start a new conversation
    print("\n✅ Step 1: Starting new chat conversation...")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:5000/api/v1/chat/start",
            json={"user_id": "ws_test_user", "metadata": {"source": "test"}}
        )
        start_data = response.json()
        conversation_id = start_data["conversation_id"]
        print(f"   Conversation started: {conversation_id}")
    
    # Step 2: Connect admin WebSocket (simulating admin panel)
    print("\n✅ Step 2: Connecting admin WebSocket...")
    uri = f"ws://localhost:5000/api/v1/ws?token={token}"
    
    escalation_received = asyncio.Event()
    escalation_data = {}
    
    async def websocket_listener(uri):
        try:
            async with websockets.connect(uri) as websocket:
                print("   WebSocket connected!")
                
                # Wait for connection established message
                msg = await websocket.recv()
                data = json.loads(msg)
                print(f"   Received: {data['type']}")
                
                # Step 3: Trigger escalation while WebSocket is listening
                print("\n✅ Step 3: Escalating conversation...")
                async with httpx.AsyncClient() as client:
                    await client.post(
                        "http://localhost:5000/api/v1/chat/escalate",
                        json={
                            "conversation_id": conversation_id,
                            "category": "test_category",
                            "priority": "high",
                            "description": "WebSocket notification test"
                        }
                    )
                    print("   Escalation triggered!")
                
                # Step 4: Listen for escalation notification
                print("\n✅ Step 4: Waiting for escalation notification...")
                while True:
                    msg = await asyncio.wait_for(websocket.recv(), timeout=5.0)
                    data = json.loads(msg)
                    print(f"   Received WebSocket message: {data['type']}")
                    
                    if data['type'] == 'conversation_escalated':
                        escalation_data.update(data)
                        escalation_received.set()
                        print(f"   ✅ ESCALATION NOTIFICATION RECEIVED!")
                        print(f"   Data: {json.dumps(data['data'], indent=2)}")
                        break
                    
                    if data['type'] == 'pong':
                        continue
        except asyncio.TimeoutError:
            print("   ❌ Timeout: No escalation notification received")
        except Exception as e:
            print(f"   ❌ WebSocket error: {e}")
    
    # Run WebSocket listener
    await websocket_listener(uri)
    
    # Verify results
    print("\n" + "="*60)
    if escalation_received.is_set():
        print("✅ TEST PASSED: WebSocket escalation notifications work!")
        print(f"   Ticket ID: {escalation_data['data'].get('ticket_id')}")
        print(f"   Conversation ID: {escalation_data['data'].get('conversation_id')}")
    else:
        print("❌ TEST FAILED: No escalation notification received")
    print("="*60 + "\n")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("WebSocket Escalation Notification Test")
    print("="*60)
    asyncio.run(test_escalation_notification())
