#!/usr/bin/env python3
"""
PM Smart Allocation Engine - Data Initialization Script
This script populates the database with realistic sample data for PM Internship Yojana
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from src.sample_data import PMYojanaSampleDataGenerator, create_yojana_integration_demo

def initialize_database():
    """Initialize database with sample data for PM Internship Yojana demo"""
    
    print("🚀 Initializing PM Smart Allocation Engine Database...")
    print("=" * 60)
    
    with app.app_context():
        # Create all tables
        print("📋 Creating database tables...")
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Generate sample data
        print("\n🎯 Generating PM Internship Yojana sample data...")
        result = create_yojana_integration_demo()
        
        print("\n📊 Database Initialization Summary:")
        print(f"  ├── Interns registered: {result['interns_created']}")
        print(f"  ├── Government projects: {result['projects_created']}")
        print(f"  ├── Industry mentors: {result['mentors_created']}")
        print(f"  └── Compliance records: {result['yojana_compliance_records']}")
        
        print("\n🎨 Wow Factor Features Included:")
        print("  ├── 🤖 AI-powered skill matching algorithm")
        print("  ├── 🎯 Real-time allocation monitoring")
        print("  ├── 📊 3D visualization of allocations")
        print("  ├── 💬 Interactive AI chatbot assistant")
        print("  ├── 📈 Predictive success analytics")
        print("  └── 🇮🇳 PM Yojana compliance tracking")
        
        print("\n✨ System Ready for Demo!")
        print("=" * 60)
        print("🌐 Access the dashboard at: http://localhost:5000")
        print("📱 Try the AI chatbot for intelligent allocation queries")
        print("🎯 Click 'Generate AI Allocations' to see the magic happen!")

if __name__ == "__main__":
    initialize_database()
