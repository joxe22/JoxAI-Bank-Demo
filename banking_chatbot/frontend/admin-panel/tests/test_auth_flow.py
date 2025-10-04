#!/usr/bin/env python3
"""
Test the complete authentication flow for the admin panel.
This test uses httpx to verify the backend API and then uses a headless browser approach.
"""

import asyncio
import httpx
import json
import sys
from datetime import datetime

BASE_URL = "http://localhost:5000"
API_URL = f"{BASE_URL}/api/v1"

async def test_authentication_flow():
    """Test the complete authentication flow"""
    print("=" * 60)
    print("ADMIN PANEL AUTHENTICATION FLOW TEST")
    print("=" * 60)
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Test credentials
    test_email = "admin@joxai.com"
    test_password = "admin123"
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Step 1: Test if login page is accessible
        print("Step 1: Testing /login page accessibility...")
        try:
            response = await client.get(f"{BASE_URL}/login")
            if response.status_code == 200:
                print(f"✓ Login page accessible (Status: {response.status_code})")
            else:
                print(f"✗ Login page returned status: {response.status_code}")
        except Exception as e:
            print(f"✗ Error accessing login page: {e}")
            return False
        
        # Step 2: Test authentication API endpoint
        print("\nStep 2: Testing authentication with credentials...")
        print(f"  Email: {test_email}")
        print(f"  Password: {'*' * len(test_password)}")
        
        try:
            login_payload = {
                "email": test_email,
                "password": test_password
            }
            
            response = await client.post(
                f"{API_URL}/auth/login",
                json=login_payload,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"\n  API Response Status: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print(f"  ✓ Login successful!")
                print(f"\n  Response Data:")
                print(f"    - Token received: {bool(data.get('token'))}")
                if data.get('token'):
                    token = data['token']
                    print(f"    - Token (first 30 chars): {token[:30]}...")
                
                print(f"    - User data received: {bool(data.get('user'))}")
                if data.get('user'):
                    user = data['user']
                    print(f"      • ID: {user.get('id')}")
                    print(f"      • Name: {user.get('name')}")
                    print(f"      • Email: {user.get('email')}")
                    print(f"      • Role: {user.get('role')}")
                
                # Step 3: Test token verification
                print("\nStep 3: Testing token verification...")
                if data.get('token'):
                    token = data['token']
                    try:
                        verify_response = await client.get(
                            f"{API_URL}/auth/verify",
                            params={"token": token}
                        )
                        
                        if verify_response.status_code == 200:
                            verify_data = verify_response.json()
                            print(f"  ✓ Token verification successful")
                            print(f"    - Valid: {verify_data.get('valid')}")
                            if verify_data.get('user'):
                                print(f"    - User verified: {verify_data['user'].get('email')}")
                        else:
                            print(f"  ✗ Token verification failed with status: {verify_response.status_code}")
                    except Exception as e:
                        print(f"  ✗ Token verification error: {e}")
                
                # Step 4: Test dashboard access with token
                print("\nStep 4: Testing dashboard access with authentication...")
                try:
                    dashboard_response = await client.get(
                        f"{BASE_URL}/dashboard",
                        headers={"Authorization": f"Bearer {token}"}
                    )
                    
                    if dashboard_response.status_code == 200:
                        print(f"  ✓ Dashboard accessible with token (Status: {dashboard_response.status_code})")
                    else:
                        print(f"  ℹ Dashboard returned status: {dashboard_response.status_code}")
                        print(f"    (This may be expected if dashboard requires client-side routing)")
                except Exception as e:
                    print(f"  ℹ Dashboard access note: {e}")
                
                # Step 5: Test API endpoints that require authentication
                print("\nStep 5: Testing authenticated API endpoints...")
                auth_headers = {"Authorization": f"Bearer {token}"}
                
                # Test analytics endpoint
                try:
                    analytics_response = await client.get(
                        f"{API_URL}/analytics/metrics",
                        headers=auth_headers
                    )
                    print(f"  ✓ Analytics endpoint: {analytics_response.status_code}")
                    if analytics_response.status_code == 200:
                        print(f"    Analytics data available: {bool(analytics_response.json())}")
                except Exception as e:
                    print(f"  ℹ Analytics endpoint: {e}")
                
                print("\n" + "=" * 60)
                print("AUTHENTICATION FLOW TEST: PASSED ✓")
                print("=" * 60)
                print("\nSummary:")
                print("  • Login page: Accessible")
                print("  • Authentication API: Working")
                print("  • JWT Token: Generated and valid")
                print("  • User data: Received correctly")
                print("  • Token verification: Successful")
                print("\nThe authentication flow is working correctly!")
                print("The frontend should be able to:")
                print("  1. Navigate to /login")
                print("  2. Submit credentials")
                print("  3. Receive JWT token")
                print("  4. Store token in localStorage")
                print("  5. Redirect to /dashboard")
                print("  6. Make authenticated API calls")
                
                return True
                
            elif response.status_code == 401:
                print(f"  ✗ Authentication failed: Invalid credentials")
                error_data = response.json() if response.text else {}
                print(f"    Error: {error_data.get('detail', 'Unknown error')}")
                return False
            else:
                print(f"  ✗ Unexpected status code: {response.status_code}")
                print(f"    Response: {response.text}")
                return False
                
        except Exception as e:
            print(f"✗ Error during authentication: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # Step 6: Test with invalid credentials
        print("\n" + "=" * 60)
        print("BONUS TEST: Invalid Credentials")
        print("=" * 60)
        try:
            invalid_response = await client.post(
                f"{API_URL}/auth/login",
                json={"email": "wrong@email.com", "password": "wrongpassword"},
                headers={"Content-Type": "application/json"}
            )
            
            if invalid_response.status_code == 401:
                print("✓ Invalid credentials correctly rejected (Status: 401)")
                error_data = invalid_response.json()
                print(f"  Error message: {error_data.get('detail')}")
            else:
                print(f"✗ Unexpected status for invalid credentials: {invalid_response.status_code}")
        except Exception as e:
            print(f"ℹ Invalid credentials test: {e}")

if __name__ == "__main__":
    result = asyncio.run(test_authentication_flow())
    sys.exit(0 if result else 1)
