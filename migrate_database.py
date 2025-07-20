#!/usr/bin/env python3
"""
Database Migration Script for CodeZone Platform
Adds new columns for flexible output checking to the problems table.
"""

import pymysql.cursors
import sys

def get_db_connection():
    return pymysql.connect(
        host='127.0.0.1',
        user="rishab",
        password="SouL123@",
        database="practice",
        cursorclass=pymysql.cursors.DictCursor
    )

def check_column_exists(cursor, table_name, column_name):
    """Check if a column exists in a table"""
    cursor.execute("""
        SELECT COLUMN_NAME 
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = 'practice' 
        AND TABLE_NAME = %s 
        AND COLUMN_NAME = %s
    """, (table_name, column_name))
    return cursor.fetchone() is not None

def migrate_database():
    """Add new columns to problems table if they don't exist"""
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            print("🔍 Checking database structure...")
            
            # Check if problems table exists
            cursor.execute("""
                SELECT TABLE_NAME 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_SCHEMA = 'practice' 
                AND TABLE_NAME = 'problems'
            """)
            if not cursor.fetchone():
                print("❌ Error: 'problems' table does not exist!")
                return False
            
            # Check if checker_type column exists
            checker_type_exists = check_column_exists(cursor, 'problems', 'checker_type')
            custom_checker_exists = check_column_exists(cursor, 'problems', 'custom_checker_code')
            
            print(f"📊 Current status:")
            print(f"   - checker_type column: {'✅ Exists' if checker_type_exists else '❌ Missing'}")
            print(f"   - custom_checker_code column: {'✅ Exists' if custom_checker_exists else '❌ Missing'}")
            
            # Add missing columns
            if not checker_type_exists:
                print("🔧 Adding checker_type column...")
                cursor.execute("""
                    ALTER TABLE problems 
                    ADD COLUMN checker_type ENUM('exact', 'ignore_whitespace', 'custom', 'multiple_outputs') 
                    DEFAULT 'exact' AFTER expected_output
                """)
                print("✅ checker_type column added successfully!")
            
            if not custom_checker_exists:
                print("🔧 Adding custom_checker_code column...")
                cursor.execute("""
                    ALTER TABLE problems 
                    ADD COLUMN custom_checker_code TEXT NULL AFTER checker_type
                """)
                print("✅ custom_checker_code column added successfully!")
            
            # Commit changes
            connection.commit()
            
            # Verify the changes
            print("\n🔍 Verifying changes...")
            checker_type_exists = check_column_exists(cursor, 'problems', 'checker_type')
            custom_checker_exists = check_column_exists(cursor, 'problems', 'custom_checker_code')
            
            print(f"📊 Final status:")
            print(f"   - checker_type column: {'✅ Exists' if checker_type_exists else '❌ Missing'}")
            print(f"   - custom_checker_code column: {'✅ Exists' if custom_checker_exists else '❌ Missing'}")
            
            if checker_type_exists and custom_checker_exists:
                print("\n🎉 Database migration completed successfully!")
                return True
            else:
                print("\n❌ Database migration failed!")
                return False
                
    except Exception as e:
        print(f"❌ Error during migration: {e}")
        connection.rollback()
        return False
    finally:
        connection.close()

def test_database_connection():
    """Test if we can connect to the database"""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            if result:
                print("✅ Database connection successful!")
                return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
    finally:
        connection.close()

def main():
    """Main migration function"""
    print("🚀 CodeZone Database Migration Tool")
    print("=" * 50)
    
    # Test database connection
    if not test_database_connection():
        print("❌ Cannot proceed without database connection.")
        sys.exit(1)
    
    # Run migration
    if migrate_database():
        print("\n✅ Migration completed successfully!")
        print("🎯 Your CodeZone platform is now ready with flexible output checking!")
    else:
        print("\n❌ Migration failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 