"""
Database seeding script to initialize default users.
Replaces hardcoded users from data_store.py
"""

import bcrypt
from sqlalchemy.orm import Session

from app.models import DBUser, UserRole
from app.repositories import UserRepository
from app.database import get_db_context


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def seed_default_users(db: Session) -> None:
    """
    Seed default users into the database.
    These replace the hardcoded users in data_store.py:
    - Admin User (admin@joxai.com)
    - Agent Smith (agent@joxai.com)
    - Supervisor Rodriguez (supervisor@joxai.com)
    """
    user_repo = UserRepository(db)
    
    default_users = [
        {
            "email": "admin@joxai.com",
            "username": "admin",
            "full_name": "Admin User",
            "hashed_password": hash_password("admin123"),
            "role": UserRole.ADMIN,
            "is_active": True,
            "is_online": False,
        },
        {
            "email": "agent@joxai.com",
            "username": "agent",
            "full_name": "Agent Smith",
            "hashed_password": hash_password("admin123"),
            "role": UserRole.AGENT,
            "is_active": True,
            "is_online": False,
        },
        {
            "email": "supervisor@joxai.com",
            "username": "supervisor",
            "full_name": "Supervisor Rodriguez",
            "hashed_password": hash_password("admin123"),
            "role": UserRole.SUPERVISOR,
            "is_active": True,
            "is_online": False,
        },
    ]
    
    created_count = 0
    for user_data in default_users:
        # Check if user already exists
        if not user_repo.email_exists(user_data["email"]):
            user_repo.create(**user_data)
            created_count += 1
            print(f"✅ Created user: {user_data['email']} ({user_data['role'].value})")
        else:
            print(f"⏭️  User already exists: {user_data['email']}")
    
    return created_count


def seed_database() -> None:
    """Main seeding function"""
    print("🌱 Starting database seeding...")
    
    with get_db_context() as db:
        created = seed_default_users(db)
        print(f"\n✅ Seeding complete! Created {created} new users.")


if __name__ == "__main__":
    seed_database()
