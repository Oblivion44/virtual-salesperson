#!/usr/bin/env python3
"""
Deployment Script for DDD Beauty Chatbot Integration
This script deploys the new DDD implementation alongside the existing chatbot
"""

import os
import sys
import shutil
from pathlib import Path

def create_deployment_structure():
    """Create the deployment directory structure"""
    print("🏗️ Creating deployment structure...")
    
    # Create main deployment directory
    deploy_dir = Path("/home/ec2-user/beauty_chatbot_ddd")
    deploy_dir.mkdir(exist_ok=True)
    
    # Create subdirectories
    subdirs = [
        "core",
        "ddd_domain", 
        "legacy",
        "data",
        "tests",
        "docs"
    ]
    
    for subdir in subdirs:
        (deploy_dir / subdir).mkdir(exist_ok=True)
    
    print(f"✅ Created deployment structure at {deploy_dir}")
    return deploy_dir

def copy_ddd_implementation(deploy_dir):
    """Copy the DDD implementation to deployment directory"""
    print("📦 Copying DDD implementation...")
    
    source_dir = Path("/home/ec2-user/construction/concern_based_chat")
    target_dir = deploy_dir / "ddd_domain"
    
    # Copy all DDD files
    ddd_files = [
        "__init__.py",
        "value_objects.py",
        "entities.py", 
        "aggregates.py",
        "domain_services.py",
        "repositories.py",
        "domain_events.py",
        "application_service.py",
        "integration_demo.py",
        "simple_test.py",
        "IMPLEMENTATION_SUMMARY.md"
    ]
    
    for file_name in ddd_files:
        source_file = source_dir / file_name
        if source_file.exists():
            shutil.copy2(source_file, target_dir / file_name)
            print(f"  ✅ Copied {file_name}")
        else:
            print(f"  ⚠️ Missing {file_name}")
    
    print("✅ DDD implementation copied successfully")

def copy_existing_chatbot(deploy_dir):
    """Copy existing chatbot files to deployment directory"""
    print("📦 Copying existing chatbot...")
    
    legacy_dir = deploy_dir / "legacy"
    
    # Copy existing chatbot files
    existing_files = [
        "/home/ec2-user/beauty_chatbot_core.py",
        "/home/ec2-user/beauty_chatbot_ui.py", 
        "/home/ec2-user/beauty_chatbot_main.ipynb",
        "/home/ec2-user/README.md"
    ]
    
    for file_path in existing_files:
        source_file = Path(file_path)
        if source_file.exists():
            shutil.copy2(source_file, legacy_dir / source_file.name)
            print(f"  ✅ Copied {source_file.name}")
        else:
            print(f"  ⚠️ Missing {source_file.name}")
    
    print("✅ Existing chatbot copied successfully")

if __name__ == "__main__":
    print("🚀 Starting DDD Beauty Chatbot Deployment")
    print("=" * 50)
    
    try:
        # Step 1: Create deployment structure
        deploy_dir = create_deployment_structure()
        
        # Step 2: Copy DDD implementation
        copy_ddd_implementation(deploy_dir)
        
        # Step 3: Copy existing chatbot
        copy_existing_chatbot(deploy_dir)
        
        print("\n" + "=" * 50)
        print("✅ Phase 1 deployment completed successfully!")
        print(f"📁 Deployment directory: {deploy_dir}")
        
    except Exception as e:
        print(f"\n❌ Deployment failed: {str(e)}")
        sys.exit(1)
