#!/usr/bin/env python3
"""
Database initialization script for JoxAI Banking Chatbot.
Creates demo users for testing: Admin, Supervisor, and Agent roles.
"""

import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from app.models import DBUser, UserRole
from app.core.security import get_password_hash

def init_database():
    """Initialize database with demo users"""
    
    # Get database URL from environment
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ ERROR: DATABASE_URL not found in environment")
        sys.exit(1)
    
    print("🔄 Connecting to database...")
    try:
        engine = create_engine(database_url)
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
        
        # Create session
        with Session(engine) as session:
            print("\n🔄 Checking for existing users...")
            
            # Check if admin exists
            admin = session.query(DBUser).filter_by(email="admin@joxaibank.com").first()
            
            if admin:
                print("✅ Users already exist in database")
                print("\n📋 Existing Demo Users:")
                users = session.query(DBUser).all()
                for user in users:
                    print(f"  • {user.role.value:12} - {user.email:30} (Password: admin123)")
                return
            
            print("🔄 Creating demo users...")
            
            # Create demo users
            demo_users = [
                {
                    "username": "admin",
                    "email": "admin@joxaibank.com",
                    "full_name": "Admin User",
                    "role": UserRole.ADMIN,
                    "is_active": True
                },
                {
                    "username": "supervisor",
                    "email": "supervisor@joxaibank.com",
                    "full_name": "Supervisor User",
                    "role": UserRole.SUPERVISOR,
                    "is_active": True
                },
                {
                    "username": "agent",
                    "email": "agent@joxaibank.com",
                    "full_name": "Agent User",
                    "role": UserRole.AGENT,
                    "is_active": True
                }
            ]
            
            # Password for all demo users
            hashed_password = get_password_hash("admin123")
            
            created_users = []
            for user_data in demo_users:
                user = DBUser(
                    username=user_data["username"],
                    email=user_data["email"],
                    full_name=user_data["full_name"],
                    hashed_password=hashed_password,
                    role=user_data["role"],
                    is_active=user_data["is_active"]
                )
                session.add(user)
                created_users.append(user)
            
            session.commit()
            
            print("✅ Successfully created demo users!\n")
            print("📋 Demo User Credentials:")
            print("=" * 70)
            for user in created_users:
                print(f"  Role:     {user.role.value}")
                print(f"  Email:    {user.email}")
                print(f"  Password: admin123")
                print("-" * 70)
            
            print("\n🎉 Database initialization complete!")
            print("💡 You can now login to the admin panel with any of the above credentials")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        print("\n💡 TROUBLESHOOTING:")
        print("   1. Check if Neon database is enabled (may auto-suspend)")
        print("   2. Go to Neon dashboard: https://console.neon.tech")
        print("   3. Enable the database endpoint")
        print("   4. Run this script again")
        sys.exit(1)

if __name__ == "__main__":
    print("=" * 70)
    print("  JoxAI Banking Chatbot - Database Initialization")
    print("=" * 70)
    init_database()
