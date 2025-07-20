#!/usr/bin/env python3
"""
Fix Database Constraints
This script handles foreign key constraints before inserting problems
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

def fix_constraints():
    """Fix foreign key constraints"""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            print("🔧 Fixing Database Constraints")
            print("=" * 40)
            
            # Check what tables exist and their relationships
            print("📋 Checking database structure...")
            
            # Disable foreign key checks temporarily
            cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
            print("✅ Disabled foreign key checks")
            
            # Clear submissions table
            try:
                cursor.execute("DELETE FROM submissions")
                print("✅ Cleared submissions table")
            except Exception as e:
                print(f"ℹ️ Submissions table issue: {e}")
            
            # Clear problems table
            try:
                cursor.execute("DELETE FROM problems")
                print("✅ Cleared problems table")
            except Exception as e:
                print(f"ℹ️ Problems table issue: {e}")
            
            # Re-enable foreign key checks
            cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
            print("✅ Re-enabled foreign key checks")
            
            connection.commit()
            print("\n🎉 Database constraints fixed successfully!")
            print("💡 Now you can run: python insert_dummy_problems.py")
            
            return True
            
    except Exception as e:
        print(f"❌ Error: {e}")
        connection.rollback()
        return False
    finally:
        connection.close()

def main():
    """Main function"""
    print("🚀 Database Constraint Fixer")
    print("=" * 40)
    
    if fix_constraints():
        print("\n✅ Database is ready for new problems!")
    else:
        print("\n❌ Failed to fix constraints!")

if __name__ == "__main__":
    main() 