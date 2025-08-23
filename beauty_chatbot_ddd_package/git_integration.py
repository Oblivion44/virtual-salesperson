#!/usr/bin/env python3
"""
Git Integration System for Beauty Chatbot
Automatically commits and pushes enhanced code to Git repository
"""

import subprocess
import os
from datetime import datetime
from typing import List, Dict, Optional


class GitIntegrationManager:
    """Manages Git operations for the beauty chatbot project"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
        self.changes_made = []
    
    def check_git_status(self) -> Dict[str, List[str]]:
        """Check current Git status"""
        try:
            # Get status
            result = subprocess.run(['git', 'status', '--porcelain'], 
                                  cwd=self.repo_path, 
                                  capture_output=True, 
                                  text=True, 
                                  check=True)
            
            status_lines = result.stdout.strip().split('\n') if result.stdout.strip() else []
            
            modified = []
            added = []
            deleted = []
            untracked = []
            
            for line in status_lines:
                if line.startswith(' M '):
                    modified.append(line[3:])
                elif line.startswith('A  '):
                    added.append(line[3:])
                elif line.startswith(' D '):
                    deleted.append(line[3:])
                elif line.startswith('?? '):
                    untracked.append(line[3:])
                elif line.startswith('M  '):
                    modified.append(line[3:])
            
            return {
                'modified': modified,
                'added': added,
                'deleted': deleted,
                'untracked': untracked
            }
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error checking Git status: {e}")
            return {'modified': [], 'added': [], 'deleted': [], 'untracked': []}
    
    def add_files(self, files: List[str]) -> bool:
        """Add files to Git staging area"""
        try:
            for file in files:
                subprocess.run(['git', 'add', file], 
                             cwd=self.repo_path, 
                             check=True)
                self.changes_made.append(f"Added: {file}")
            
            print(f"✅ Added {len(files)} files to staging area")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error adding files to Git: {e}")
            return False
    
    def commit_changes(self, message: str, description: str = "") -> bool:
        """Commit staged changes with message"""
        try:
            # Create full commit message
            full_message = message
            if description:
                full_message += f"\n\n{description}"
            
            subprocess.run(['git', 'commit', '-m', full_message], 
                         cwd=self.repo_path, 
                         check=True)
            
            print(f"✅ Committed changes: {message}")
            self.changes_made.append(f"Committed: {message}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error committing changes: {e}")
            return False
    
    def push_to_remote(self, branch: str = "main") -> bool:
        """Push commits to remote repository"""
        try:
            subprocess.run(['git', 'push', 'origin', branch], 
                         cwd=self.repo_path, 
                         check=True)
            
            print(f"✅ Pushed changes to remote repository (branch: {branch})")
            self.changes_made.append(f"Pushed to remote: {branch}")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Error pushing to remote: {e}")
            return False
    
    def create_data_commit(self, collected_data: Dict[str, List]) -> bool:
        """Create commit for collected data"""
        # Check what data files exist
        data_files = []
        data_dir = "beauty_chatbot_ddd_package/data"
        
        if os.path.exists(f"{data_dir}/collected_products.csv"):
            data_files.append(f"{data_dir}/collected_products.csv")
        if os.path.exists(f"{data_dir}/collected_ingredients.csv"):
            data_files.append(f"{data_dir}/collected_ingredients.csv")
        if os.path.exists(f"{data_dir}/collected_reviews.csv"):
            data_files.append(f"{data_dir}/collected_reviews.csv")
        
        if not data_files:
            print("⚠️ No data files found to commit")
            return False
        
        # Add data files
        if not self.add_files(data_files):
            return False
        
        # Create commit message
        total_products = len(collected_data.get('products', []))
        total_ingredients = len(collected_data.get('ingredients', []))
        total_reviews = len(collected_data.get('reviews', []))
        
        commit_message = "📊 Add collected beauty data"
        commit_description = f"""✨ New Data Added:
- 🛒 Products: {total_products} items
- 🧪 Ingredients: {total_ingredients} items  
- ⭐ Reviews: {total_reviews} items

🎯 Data Collection Features:
- LLM-powered context analysis
- Intelligent data structuring
- Automated CSV generation
- Ready for chatbot integration

📅 Collection Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Ready for enhanced chatbot functionality!"""
        
        return self.commit_changes(commit_message, commit_description)
    
    def create_enhanced_code_commit(self) -> bool:
        """Create commit for enhanced chatbot code"""
        # Check what enhanced files exist
        enhanced_files = []
        
        if os.path.exists("beauty_chatbot_ddd_package/core/beauty_chatbot_enhanced.py"):
            enhanced_files.append("beauty_chatbot_ddd_package/core/beauty_chatbot_enhanced.py")
        if os.path.exists("beauty_chatbot_ddd_package/llm_data_collector.py"):
            enhanced_files.append("beauty_chatbot_ddd_package/llm_data_collector.py")
        if os.path.exists("beauty_chatbot_ddd_package/code_regenerator.py"):
            enhanced_files.append("beauty_chatbot_ddd_package/code_regenerator.py")
        if os.path.exists("beauty_chatbot_ddd_package/git_integration.py"):
            enhanced_files.append("beauty_chatbot_ddd_package/git_integration.py")
        
        if not enhanced_files:
            print("⚠️ No enhanced code files found to commit")
            return False
        
        # Add enhanced files
        if not self.add_files(enhanced_files):
            return False
        
        # Create commit message
        commit_message = "🚀 Add LLM-powered data collection and code regeneration"
        commit_description = f"""✨ New Features Added:
- 🤖 LLM-powered context analysis for beauty data
- 📊 Interactive data collection system
- 🔄 Automatic code regeneration based on collected data
- 🔗 Git integration for automated commits
- 🧠 Enhanced chatbot with collected data integration

🎯 LLM Capabilities:
- Intelligent content type detection (product/ingredient/review)
- Automatic sentiment analysis
- Context-aware data structuring
- Smart keyword extraction
- Rating and recommendation analysis

🔧 System Features:
- Interactive data collection interface
- Automated CSV generation
- Code regeneration with collected data
- Enhanced concern detection
- Improved product recommendations
- Git integration for seamless updates

📈 Enhanced Chatbot Features:
- Dynamic concern detection based on collected data
- Personalized product recommendations
- Ingredient knowledge base integration
- Review-based insights
- Improved response generation

🚀 Ready for:
- Production deployment with enhanced data
- Continuous data collection and improvement
- Automated system updates
- Scalable beauty recommendation system

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
        
        return self.commit_changes(commit_message, commit_description)
    
    def full_integration_workflow(self, collected_data: Dict[str, List]) -> bool:
        """Complete workflow: commit data, commit code, push to remote"""
        print("🔄 Starting full Git integration workflow...")
        print("=" * 50)
        
        success_steps = []
        
        # Step 1: Commit collected data
        print("\n📊 Step 1: Committing collected data...")
        if self.create_data_commit(collected_data):
            success_steps.append("data_commit")
            print("✅ Data committed successfully")
        else:
            print("⚠️ Data commit skipped (no new data files)")
        
        # Step 2: Commit enhanced code
        print("\n🚀 Step 2: Committing enhanced code...")
        if self.create_enhanced_code_commit():
            success_steps.append("code_commit")
            print("✅ Enhanced code committed successfully")
        else:
            print("⚠️ Code commit skipped (no new code files)")
        
        # Step 3: Push to remote
        if success_steps:
            print("\n📤 Step 3: Pushing to remote repository...")
            if self.push_to_remote():
                success_steps.append("push")
                print("✅ Changes pushed to remote successfully")
            else:
                print("❌ Failed to push to remote")
        
        # Summary
        print("\n" + "=" * 50)
        print("📋 Integration Summary:")
        for change in self.changes_made:
            print(f"  ✅ {change}")
        
        if len(success_steps) >= 2:  # At least one commit and push
            print("\n🎉 Full integration workflow completed successfully!")
            return True
        else:
            print("\n⚠️ Integration workflow completed with some steps skipped")
            return False
    
    def get_integration_summary(self) -> str:
        """Get summary of integration activities"""
        if not self.changes_made:
            return "No Git integration activities performed."
        
        summary = "Git Integration Summary:\n"
        summary += "=" * 30 + "\n"
        for change in self.changes_made:
            summary += f"✅ {change}\n"
        
        summary += f"\nIntegration completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        return summary


def main():
    """Main function for Git integration"""
    print("🔗 Beauty Chatbot Git Integration System")
    print("=" * 50)
    
    git_manager = GitIntegrationManager()
    
    # Check current status
    print("📋 Checking current Git status...")
    status = git_manager.check_git_status()
    
    print(f"Modified files: {len(status['modified'])}")
    print(f"Untracked files: {len(status['untracked'])}")
    
    if status['modified'] or status['untracked']:
        print("\n📁 Files ready for commit:")
        for file in status['modified'] + status['untracked']:
            print(f"  - {file}")
        
        # Ask user if they want to proceed
        proceed = input("\n🤔 Proceed with Git integration? (y/n): ").strip().lower()
        if proceed == 'y':
            # Mock collected data for demonstration
            mock_data = {'products': [], 'ingredients': [], 'reviews': []}
            
            success = git_manager.full_integration_workflow(mock_data)
            if success:
                print("\n🎉 Git integration completed successfully!")
            else:
                print("\n⚠️ Git integration completed with issues.")
        else:
            print("👋 Git integration cancelled by user.")
    else:
        print("✅ Repository is up to date. No changes to commit.")
    
    # Show summary
    print("\n" + git_manager.get_integration_summary())


if __name__ == "__main__":
    main()
