#!/usr/bin/env python3
"""
LLM-Enhanced Beauty Chatbot System
Main orchestrator for data collection, code regeneration, and Git integration
"""

import os
import sys
from datetime import datetime
from typing import Dict, List, Optional

# Import our custom modules
from llm_data_collector import InteractiveDataCollector
from code_regenerator import BeautyChatbotCodeRegenerator
from git_integration import GitIntegrationManager


class LLMEnhancedBeautySystem:
    """Main system orchestrator for LLM-enhanced beauty chatbot"""
    
    def __init__(self):
        self.data_collector = InteractiveDataCollector()
        self.code_regenerator = BeautyChatbotCodeRegenerator("beauty_chatbot_ddd_package/data")
        self.git_manager = GitIntegrationManager()
        self.session_summary = []
    
    def run_complete_workflow(self) -> bool:
        """Run the complete LLM-enhanced workflow"""
        print("🌟 LLM-Enhanced Beauty Chatbot System")
        print("=" * 60)
        print("🤖 Using LLM to collect data, regenerate code, and update Git")
        print("=" * 60)
        
        try:
            # Step 1: Data Collection
            print("\n🔍 STEP 1: LLM-Powered Data Collection")
            print("-" * 40)
            collected_data = self.data_collector.collect_data_interactively()
            
            if not any(collected_data.values()):
                print("⚠️ No data collected. Exiting workflow.")
                return False
            
            # Save collected data
            self.data_collector.save_to_csv("beauty_chatbot_ddd_package/data")
            self.session_summary.append(f"✅ Collected {sum(len(v) for v in collected_data.values())} data items")
            
            # Step 2: Code Regeneration
            print("\n🔄 STEP 2: Automatic Code Regeneration")
            print("-" * 40)
            
            # Reload code regenerator with new data
            self.code_regenerator = BeautyChatbotCodeRegenerator("beauty_chatbot_ddd_package/data")
            
            if self.code_regenerator.regenerate_chatbot_code():
                self.session_summary.append("✅ Enhanced chatbot code generated")
                print("🎉 Enhanced chatbot code generated successfully!")
            else:
                print("❌ Code regeneration failed")
                return False
            
            # Step 3: Git Integration
            print("\n📤 STEP 3: Git Integration")
            print("-" * 40)
            
            if self.git_manager.full_integration_workflow(collected_data):
                self.session_summary.append("✅ Changes committed and pushed to Git")
                print("🎉 Git integration completed successfully!")
            else:
                print("⚠️ Git integration completed with issues")
            
            # Step 4: Final Summary
            self._show_final_summary(collected_data)
            
            return True
            
        except KeyboardInterrupt:
            print("\n\n👋 Workflow cancelled by user.")
            return False
        except Exception as e:
            print(f"\n❌ Workflow failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return False
    
    def run_data_collection_only(self) -> Dict[str, List]:
        """Run only the data collection phase"""
        print("🔍 LLM-Powered Data Collection Only")
        print("=" * 40)
        
        collected_data = self.data_collector.collect_data_interactively()
        
        if any(collected_data.values()):
            self.data_collector.save_to_csv("beauty_chatbot_ddd_package/data")
            print(self.data_collector.generate_summary())
        
        return collected_data
    
    def run_code_regeneration_only(self) -> bool:
        """Run only the code regeneration phase"""
        print("🔄 Code Regeneration Only")
        print("=" * 30)
        
        return self.code_regenerator.regenerate_chatbot_code()
    
    def run_git_integration_only(self, collected_data: Dict[str, List] = None) -> bool:
        """Run only the Git integration phase"""
        print("📤 Git Integration Only")
        print("=" * 25)
        
        if collected_data is None:
            collected_data = {'products': [], 'ingredients': [], 'reviews': []}
        
        return self.git_manager.full_integration_workflow(collected_data)
    
    def _show_final_summary(self, collected_data: Dict[str, List]):
        """Show final workflow summary"""
        print("\n" + "=" * 60)
        print("🎉 LLM-Enhanced Beauty System - Workflow Complete!")
        print("=" * 60)
        
        # Data summary
        total_products = len(collected_data.get('products', []))
        total_ingredients = len(collected_data.get('ingredients', []))
        total_reviews = len(collected_data.get('reviews', []))
        
        print(f"\n📊 Data Collection Results:")
        print(f"  🛒 Products: {total_products}")
        print(f"  🧪 Ingredients: {total_ingredients}")
        print(f"  ⭐ Reviews: {total_reviews}")
        print(f"  📅 Collection Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # System enhancements
        print(f"\n🚀 System Enhancements:")
        for summary_item in self.session_summary:
            print(f"  {summary_item}")
        
        # Files created/updated
        print(f"\n📁 Files Created/Updated:")
        if os.path.exists("beauty_chatbot_ddd_package/data/collected_products.csv"):
            print("  ✅ beauty_chatbot_ddd_package/data/collected_products.csv")
        if os.path.exists("beauty_chatbot_ddd_package/data/collected_ingredients.csv"):
            print("  ✅ beauty_chatbot_ddd_package/data/collected_ingredients.csv")
        if os.path.exists("beauty_chatbot_ddd_package/data/collected_reviews.csv"):
            print("  ✅ beauty_chatbot_ddd_package/data/collected_reviews.csv")
        if os.path.exists("beauty_chatbot_ddd_package/core/beauty_chatbot_enhanced.py"):
            print("  ✅ beauty_chatbot_ddd_package/core/beauty_chatbot_enhanced.py")
        
        # Usage instructions
        print(f"\n🎯 Next Steps:")
        print("  1. Test the enhanced chatbot:")
        print("     cd beauty_chatbot_ddd_package/core")
        print("     python3 beauty_chatbot_enhanced.py")
        print("  2. Use in Google Colab with enhanced features")
        print("  3. Continue collecting more data to improve the system")
        
        # Git status
        print(f"\n📤 Git Status:")
        print("  ✅ All changes committed and pushed to repository")
        print("  🌐 Available at: https://github.com/Oblivion44/virtual-salesperson")
        
        print("\n" + "=" * 60)
        print("🌟 Your Beauty Chatbot is now enhanced with LLM-powered data!")
        print("💄 Ready to provide even better beauty recommendations!")
        print("=" * 60)
    
    def show_menu(self):
        """Show interactive menu"""
        while True:
            print("\n🌟 LLM-Enhanced Beauty Chatbot System")
            print("=" * 45)
            print("1. 🔄 Run Complete Workflow (Collect → Generate → Push)")
            print("2. 🔍 Data Collection Only")
            print("3. 🚀 Code Regeneration Only")
            print("4. 📤 Git Integration Only")
            print("5. 📊 Show System Status")
            print("6. 👋 Exit")
            print("=" * 45)
            
            choice = input("Select option (1-6): ").strip()
            
            if choice == '1':
                self.run_complete_workflow()
            elif choice == '2':
                self.run_data_collection_only()
            elif choice == '3':
                self.run_code_regeneration_only()
            elif choice == '4':
                self.run_git_integration_only()
            elif choice == '5':
                self._show_system_status()
            elif choice == '6':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please select 1-6.")
    
    def _show_system_status(self):
        """Show current system status"""
        print("\n📊 System Status")
        print("=" * 20)
        
        # Check data files
        data_dir = "beauty_chatbot_ddd_package/data"
        print(f"📁 Data Directory: {data_dir}")
        
        if os.path.exists(f"{data_dir}/collected_products.csv"):
            print("  ✅ collected_products.csv exists")
        else:
            print("  ❌ collected_products.csv missing")
        
        if os.path.exists(f"{data_dir}/collected_ingredients.csv"):
            print("  ✅ collected_ingredients.csv exists")
        else:
            print("  ❌ collected_ingredients.csv missing")
        
        if os.path.exists(f"{data_dir}/collected_reviews.csv"):
            print("  ✅ collected_reviews.csv exists")
        else:
            print("  ❌ collected_reviews.csv missing")
        
        # Check enhanced code
        enhanced_file = "beauty_chatbot_ddd_package/core/beauty_chatbot_enhanced.py"
        if os.path.exists(enhanced_file):
            print("  ✅ Enhanced chatbot code exists")
        else:
            print("  ❌ Enhanced chatbot code missing")
        
        # Git status
        git_status = self.git_manager.check_git_status()
        print(f"\n📤 Git Status:")
        print(f"  Modified files: {len(git_status['modified'])}")
        print(f"  Untracked files: {len(git_status['untracked'])}")
        
        if git_status['modified'] or git_status['untracked']:
            print("  ⚠️ Uncommitted changes present")
        else:
            print("  ✅ Repository is clean")


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        # Command line mode
        command = sys.argv[1].lower()
        system = LLMEnhancedBeautySystem()
        
        if command == 'collect':
            system.run_data_collection_only()
        elif command == 'generate':
            system.run_code_regeneration_only()
        elif command == 'push':
            system.run_git_integration_only()
        elif command == 'all':
            system.run_complete_workflow()
        else:
            print("❌ Invalid command. Use: collect, generate, push, or all")
    else:
        # Interactive mode
        system = LLMEnhancedBeautySystem()
        system.show_menu()


if __name__ == "__main__":
    main()
