#!/usr/bin/env python3
"""
Database Explorer Script for Japan Trade Statistics

This script explores SQLite databases to understand their structure and contents.
Usage: python explore_database.py <database_file>
Example: python explore_database.py input-data/ym_2020.db
"""

import sqlite3
import sys
import argparse
import pandas as pd
from pathlib import Path


def get_table_info(cursor, table_name):
    """Get detailed information about a table."""
    print(f"\n{'='*60}")
    print(f"TABLE: {table_name}")
    print('='*60)
    
    # Get table schema
    cursor.execute(f"PRAGMA table_info({table_name})")
    schema = cursor.fetchall()
    
    print("SCHEMA:")
    print("-" * 50)
    for col in schema:
        col_id, name, data_type, not_null, default, pk = col
        pk_info = " (PRIMARY KEY)" if pk else ""
        null_info = " NOT NULL" if not_null else ""
        default_info = f" DEFAULT {default}" if default else ""
        print(f"  {name}: {data_type}{pk_info}{null_info}{default_info}")
    
    # Get row count
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    row_count = cursor.fetchone()[0]
    print(f"\nROW COUNT: {row_count:,}")
    
    if row_count > 0:
        # Get sample data
        print(f"\nSAMPLE DATA (first 5 rows):")
        print("-" * 50)
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
        sample_data = cursor.fetchall()
        
        # Get column names for header
        column_names = [description[0] for description in cursor.description]
        
        # Create a simple table display
        if sample_data:
            # Print header
            header = " | ".join(f"{col[:15]:15}" for col in column_names)
            print(header)
            print("-" * len(header))
            
            # Print sample rows
            for row in sample_data:
                row_str = " | ".join(f"{str(val)[:15]:15}" for val in row)
                print(row_str)
        
        # Get some basic statistics for numeric columns
        print(f"\nCOLUMN STATISTICS:")
        print("-" * 50)
        for col_info in schema:
            col_name = col_info[1]
            data_type = col_info[2].upper()
            
            if any(t in data_type for t in ['INT', 'REAL', 'NUMERIC', 'DECIMAL', 'FLOAT']):
                try:
                    cursor.execute(f"SELECT MIN({col_name}), MAX({col_name}), AVG({col_name}) FROM {table_name}")
                    min_val, max_val, avg_val = cursor.fetchone()
                    if avg_val is not None:
                        print(f"  {col_name}: MIN={min_val}, MAX={max_val}, AVG={avg_val:.2f}")
                except:
                    print(f"  {col_name}: Unable to calculate statistics")
            elif 'TEXT' in data_type or 'CHAR' in data_type:
                try:
                    cursor.execute(f"SELECT COUNT(DISTINCT {col_name}) FROM {table_name}")
                    distinct_count = cursor.fetchone()[0]
                    print(f"  {col_name}: {distinct_count:,} distinct values")
                except:
                    print(f"  {col_name}: Unable to calculate distinct count")


def explore_database(db_path):
    """Explore the given database file."""
    db_file = Path(db_path)
    
    if not db_file.exists():
        print(f"Error: Database file '{db_path}' does not exist.")
        return
    
    print(f"Exploring database: {db_path}")
    print(f"File size: {db_file.stat().st_size / (1024*1024):.1f} MB")
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"\nFound {len(tables)} tables:")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Explore each table
        for table in tables:
            table_name = table[0]
            get_table_info(cursor, table_name)
        
        # Check for indexes
        print(f"\n{'='*60}")
        print("INDEXES:")
        print('='*60)
        cursor.execute("SELECT name, tbl_name, sql FROM sqlite_master WHERE type='index'")
        indexes = cursor.fetchall()
        
        if indexes:
            for idx in indexes:
                print(f"  {idx[0]} on table {idx[1]}")
                if idx[2]:  # SQL definition
                    print(f"    {idx[2]}")
        else:
            print("  No custom indexes found")
        
        # Database metadata
        print(f"\n{'='*60}")
        print("DATABASE INFO:")
        print('='*60)
        cursor.execute("PRAGMA database_list")
        db_info = cursor.fetchall()
        for db in db_info:
            print(f"  Database: {db[1]} (file: {db[2]})")
        
        # Check SQLite version
        cursor.execute("SELECT sqlite_version()")
        sqlite_version = cursor.fetchone()[0]
        print(f"  SQLite version: {sqlite_version}")
        
        # Check if there are any foreign keys
        cursor.execute("PRAGMA foreign_key_list")
        print(f"  Foreign keys enabled: {len(cursor.fetchall()) > 0}")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"Error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Explore SQLite database structure and contents",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python explore_database.py input-data/ym_2020.db
  python explore_database.py input-data/ym_2021.db
        """
    )
    
    parser.add_argument(
        'database',
        help='Path to the SQLite database file'
    )
    
    parser.add_argument(
        '--sample-size',
        type=int,
        default=5,
        help='Number of sample rows to display (default: 5)'
    )
    
    args = parser.parse_args()
    
    explore_database(args.database)


if __name__ == "__main__":
    main()