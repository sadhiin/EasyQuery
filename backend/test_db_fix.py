#!/usr/bin/env python3
"""
Test script to verify the database URL sanitization fix works correctly.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from app.api.v1.db.database import DatabaseManager

def test_url_sanitization():
    """Test various URL patterns to ensure channel_binding is properly removed."""
    
    test_cases = [
        {
            'original': 'postgresql://user:pass@host:5432/db?sslmode=require&channel_binding=require',
            'expected': 'postgresql://user:pass@host:5432/db?sslmode=require'
        },
        {
            'original': 'postgresql://user:pass@host:5432/db?channel_binding=require&sslmode=require',
            'expected': 'postgresql://user:pass@host:5432/db?sslmode=require'
        },
        {
            'original': 'postgresql://user:pass@host:5432/db?channel_binding=require',
            'expected': 'postgresql://user:pass@host:5432/db'
        },
        {
            'original': 'postgresql://user:pass@host:5432/db?sslmode=require&channel_binding=disable&application_name=myapp',
            'expected': 'postgresql://user:pass@host:5432/db?sslmode=require&application_name=myapp'
        },
        {
            'original': 'postgresql://user:pass@host:5432/db?sslmode=require',
            'expected': 'postgresql://user:pass@host:5432/db?sslmode=require'  # No change expected
        }
    ]
    
    print("Testing Database URL Sanitization...")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        db_manager = DatabaseManager(test_case['original'])
        result = db_manager._sanitize_db_url(test_case['original'])
        
        print(f"Test {i}:")
        print(f"  Original: {test_case['original']}")
        print(f"  Expected: {test_case['expected']}")
        print(f"  Result:   {result}")
        print(f"  Status:   {'✅ PASS' if result == test_case['expected'] else '❌ FAIL'}")
        print()

if __name__ == "__main__":
    test_url_sanitization()
