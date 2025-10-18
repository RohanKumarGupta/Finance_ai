#!/usr/bin/env python3
"""
Database Seeding Script for Finance AI Application
Run this script to populate the database with sample data.

Usage:
    python seed_database.py [--reset]

Options:
    --reset    Clear existing data before seeding (WARNING: This will delete all data!)
"""

import asyncio
import sys
from pathlib import Path

# Add the app directory to the path
sys.path.insert(0, str(Path(__file__).parent))

from app.seed.seed_data import run_seed
from app.db import get_db, connect_to_mongo, close_mongo_connection


async def clear_database():
    """Clear all collections in the database."""
    print("⚠️  Clearing existing database...")
    db = get_db()
    
    collections = ["parents", "students", "payments", "reminders"]
    for collection_name in collections:
        result = await db[collection_name].delete_many({})
        print(f"   - Deleted {result.deleted_count} documents from {collection_name}")
    
    print("✅ Database cleared successfully!\n")


async def main():
    """Main function to run the seeding process."""
    try:
        # Check for reset flag
        reset_db = "--reset" in sys.argv
        
        print("=" * 60)
        print("🌱 Finance AI Database Seeding Script")
        print("=" * 60)
        print()
        
        if reset_db:
            print("⚠️  WARNING: You are about to delete all existing data!")
            response = input("Are you sure you want to continue? (yes/no): ")
            if response.lower() != "yes":
                print("❌ Seeding cancelled.")
                return
            print()
            await connect_to_mongo()
            await clear_database()
        
        # Run the seed function
        print("🌱 Starting database seeding...\n")
        await run_seed()
        
        print("\n" + "=" * 60)
        print("✅ Database seeding completed successfully!")
        print("=" * 60)
        print("\n💡 You can now login with any of the above credentials.")
        print("   Password for all accounts: password123\n")
        
    except Exception as e:
        print(f"\n❌ Error during seeding: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
