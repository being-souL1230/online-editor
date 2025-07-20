#!/usr/bin/env python3
"""
Check Database Schema
This script checks the actual database structure
"""

import pymysql.cursors

def get_db_connection():
    return pymysql.connect(
        host='127.0.0.1',
        user="rishab",
        password="SouL123@",
        database="practice",
        cursorclass=pymysql.cursors.DictCursor
    )

def check_schema():
    """Check database schema"""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            print("🔍 Checking Database Schema")
            print("=" * 40)
            
            # Check problems table structure
            print("\n📋 Problems Table Structure:")
            cursor.execute("DESCRIBE problems")
            columns = cursor.fetchall()
            
            for col in columns:
                print(f"  {col['Field']} - {col['Type']} - {col['Null']} - {col['Key']} - {col['Default']}")
            
            # Check users table structure
            print("\n👥 Users Table Structure:")
            cursor.execute("DESCRIBE users")
            user_columns = cursor.fetchall()
            
            for col in user_columns:
                print(f"  {col['Field']} - {col['Type']} - {col['Null']} - {col['Key']} - {col['Default']}")
            
            # Check if there are any users
            print("\n👤 Checking Users:")
            cursor.execute("SELECT * FROM users LIMIT 3")
            users = cursor.fetchall()
            
            if users:
                print(f"  Found {len(users)} users:")
                for user in users:
                    print(f"    ID: {user.get('id', 'N/A')}, Name: {user.get('username', 'N/A')}")
            else:
                print("  No users found!")
            
            # Check if there are any problems
            print("\n📝 Checking Problems:")
            cursor.execute("SELECT COUNT(*) as count FROM problems")
            problem_count = cursor.fetchone()
            if problem_count:
                print(f"  Total problems: {problem_count['count']}")
            else:
                print("  Could not count problems")
            
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        connection.close()

def main():
    """Main function"""
    print("🚀 Database Schema Checker")
    print("=" * 40)
    
    if check_schema():
        print("\n✅ Schema check completed!")
    else:
        print("\n❌ Failed to check schema!")

if __name__ == "__main__":
    main() 
    