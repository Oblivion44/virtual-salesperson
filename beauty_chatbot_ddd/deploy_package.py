#!/usr/bin/env python3
"""
Beauty Chatbot DDD - Complete Deployment Package
This script creates a complete, self-contained deployment package
"""

import os
import sys
import shutil
import zipfile
from pathlib import Path

def create_deployment_package():
    """Create a complete deployment package"""
    print("📦 Creating Beauty Chatbot DDD Deployment Package")
    print("=" * 60)
    
    # Create package directory
    package_dir = Path("/home/ec2-user/beauty_chatbot_ddd_package")
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir()
    
    print(f"📁 Created package directory: {package_dir}")
    
    # Copy DDD domain files
    ddd_source = Path("/home/ec2-user/beauty_chatbot_ddd/ddd_domain")
    ddd_target = package_dir / "ddd_domain"
    shutil.copytree(ddd_source, ddd_target)
    print("✅ Copied DDD domain implementation")
    
    # Copy core files
    core_source = Path("/home/ec2-user/beauty_chatbot_ddd/core")
    core_target = package_dir / "core"
    shutil.copytree(core_source, core_target)
    print("✅ Copied core integration files")
    
    # Copy legacy files
    legacy_source = Path("/home/ec2-user/beauty_chatbot_ddd/legacy")
    legacy_target = package_dir / "legacy"
    shutil.copytree(legacy_source, legacy_target)
    print("✅ Copied legacy chatbot files")
    
    # Create main runner script
    create_main_runner(package_dir)
    print("✅ Created main runner script")
    
    # Create README
    create_readme(package_dir)
    print("✅ Created README documentation")
    
    # Create requirements file
    create_requirements(package_dir)
    print("✅ Created requirements.txt")
    
    # Create sample data
    create_sample_data(package_dir)
    print("✅ Created sample CSV data")
    
    # Create zip package
    create_zip_package(package_dir)
    print("✅ Created ZIP deployment package")
    
    print("\n" + "=" * 60)
    print("🎉 Deployment package created successfully!")
    print(f"📁 Package location: {package_dir}")
    print(f"📦 ZIP package: {package_dir.parent / 'beauty_chatbot_ddd_complete.zip'}")
    
    return package_dir

def create_main_runner(package_dir):
    """Create the main runner script"""
    runner_content = '''#!/usr/bin/env python3
"""
Beauty Recommendation Chatbot - DDD Enhanced Version
Main runner script for the deployed chatbot
"""

import sys
import os
from pathlib import Path

# Add paths
sys.path.append(str(Path(__file__).parent / "ddd_domain"))
sys.path.append(str(Path(__file__).parent / "core"))

# Import the simplified chatbot
from beauty_chatbot_simple import create_chatbot

def main():
    """Main function to run the chatbot"""
    print("🌟 Beauty Recommendation Chatbot - DDD Enhanced")
    print("=" * 50)
    print("Welcome to your AI Beauty Expert! 💄✨")
    print()
    
    try:
        # Create chatbot instance
        print("🚀 Initializing chatbot...")
        chatbot = create_chatbot()
        print("✅ Chatbot ready!")
        print()
        
        # Interactive chat loop
        print("💬 Start chatting! (type 'quit' to exit)")
        print("-" * 30)
        
        while True:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Thanks for using Beauty Chatbot! Goodbye!")
                break
            
            if not user_input:
                continue
            
            # Process message
            response = chatbot.process_message(user_input)
            
            print(f"Bot: {response['response']}")
            
            if response['concerns_detected']:
                print(f"🔍 Concerns detected: {', '.join(response['concerns_detected'])}")
            
            if response['natural_remedies']:
                print(f"🌿 Natural remedies available: {len(response['natural_remedies'])}")
            
            print()
    
    except KeyboardInterrupt:
        print("\\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
'''
    
    with open(package_dir / "run_chatbot.py", "w") as f:
        f.write(runner_content)

def create_readme(package_dir):
    """Create README documentation"""
    readme_content = '''# Beauty Recommendation Chatbot - DDD Enhanced Version

## 🌟 Overview

This is an enhanced version of the Beauty Recommendation Chatbot built with Domain Driven Design (DDD) architecture. It provides intelligent beauty advice, product recommendations, and natural remedies through natural language conversations.

## ✨ Features

- **🔍 Advanced Concern Detection** - AI-powered identification of beauty concerns
- **💬 Natural Conversations** - Three conversation types: Concern-based, Exploration, Chit-chat
- **📚 Educational Content** - Learn about beauty concerns and treatments
- **🌿 Natural Remedies** - Home remedies for common beauty issues
- **🛒 Smart Recommendations** - Personalized product suggestions
- **📊 Analytics** - Track conversations and interactions
- **🎯 Event Sourcing** - Complete audit trail of all interactions

## 🏗️ Architecture

Built with Domain Driven Design principles:
- **Value Objects** - Immutable data structures
- **Entities** - Objects with identity and behavior
- **Aggregates** - Consistency boundaries for business logic
- **Domain Services** - Complex business operations
- **Repositories** - Data access abstraction
- **Domain Events** - Event sourcing for audit trails
- **Application Services** - Workflow orchestration

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation

1. Extract the package:
```bash
unzip beauty_chatbot_ddd_complete.zip
cd beauty_chatbot_ddd_package
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the chatbot:
```bash
python run_chatbot.py
```

### Usage

Once started, you can chat with the bot using natural language:

**Concern-based conversations:**
- "I have acne problems"
- "My skin is very dry"
- "I'm dealing with hair loss"

**Exploration conversations:**
- "Can you recommend skincare products?"
- "What's good for oily skin?"
- "Show me anti-aging products"

**General chat:**
- "Hello!"
- "How are you?"
- "Tell me about skincare"

## 📊 CSV Data Integration

The chatbot supports loading data from CSV files. Place your CSV files in the `data/` directory:

- `concerns.csv` - Beauty concerns and keywords
- `ingredients.csv` - Active ingredients and benefits
- `products.csv` - Product information
- `reviews.csv` - Customer reviews
- `educational_content.csv` - Educational materials

## 🔧 Customization

### Adding New Concerns
1. Update `concerns.csv` with new concern data
2. Add corresponding ingredients and mappings
3. Create educational content
4. Restart the chatbot

### Modifying Responses
Edit the response templates in `core/beauty_chatbot_simple.py`

### Adding Features
Extend the DDD domain model in the `ddd_domain/` directory

## 📁 Project Structure

```
beauty_chatbot_ddd_package/
├── run_chatbot.py              # Main runner script
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── ddd_domain/                 # DDD implementation
│   ├── value_objects.py        # Immutable value objects
│   ├── entities.py             # Domain entities
│   ├── aggregates.py           # Aggregate roots
│   ├── domain_services.py      # Business logic services
│   ├── repositories.py         # Data access layer
│   ├── domain_events.py        # Event sourcing
│   └── application_service.py  # Application orchestration
├── core/                       # Integration layer
│   └── beauty_chatbot_simple.py # Simplified chatbot implementation
├── legacy/                     # Original chatbot files
│   ├── beauty_chatbot_core.py  # Original core logic
│   ├── beauty_chatbot_ui.py    # Original UI components
│   └── beauty_chatbot_main.ipynb # Original Colab notebook
└── data/                       # Sample data files
    ├── sample_concerns.csv     # Sample concerns data
    ├── sample_ingredients.csv  # Sample ingredients data
    └── sample_products.csv     # Sample products data
```

## 🧪 Testing

Run the test suite:
```bash
cd ddd_domain
python simple_test.py
```

Run integration tests:
```bash
cd ddd_domain
python integration_demo.py
```

## 📈 Analytics

The chatbot tracks:
- Total conversations
- Messages processed
- Concerns detected
- Products recommended
- User interactions

Access analytics through the chatbot API or check the event store.

## 🔒 Security

- Input validation on all user messages
- Safe handling of CSV data
- No sensitive data stored
- Event sourcing for audit trails

## 🤝 Contributing

1. Follow DDD principles when adding features
2. Add tests for new functionality
3. Update documentation
4. Maintain backward compatibility

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the DDD implementation documentation
3. Test with sample data first

## 📄 License

This project is provided as-is for educational and demonstration purposes.

---

**Ready to enhance your beauty routine with AI! 🌟💄**
'''
    
    with open(package_dir / "README.md", "w") as f:
        f.write(readme_content)

def create_requirements(package_dir):
    """Create requirements.txt file"""
    requirements = '''# Beauty Chatbot DDD - Python Dependencies

# Core dependencies (minimal for basic functionality)
# No external dependencies required for basic operation

# Optional dependencies for enhanced features:
# pandas>=1.3.0          # For CSV data processing
# ipywidgets>=7.6.0      # For Jupyter notebook UI
# nltk>=3.6              # For advanced NLP features

# Development dependencies:
# pytest>=6.0.0          # For testing
# black>=21.0.0          # For code formatting
# mypy>=0.910            # For type checking
'''
    
    with open(package_dir / "requirements.txt", "w") as f:
        f.write(requirements)

def create_sample_data(package_dir):
    """Create sample CSV data files"""
    data_dir = package_dir / "data"
    data_dir.mkdir()
    
    # Sample concerns
    concerns_csv = '''concern_id,name,category,keywords
acne,Acne,SKIN,"acne,pimples,breakouts,spots,blemishes"
dryness,Dryness,SKIN,"dry,dehydrated,flaky,tight"
oily_skin,Oily Skin,SKIN,"oily,greasy,shiny,excess oil"
aging,Aging,SKIN,"wrinkles,fine lines,aging,anti-aging"
dark_spots,Dark Spots,SKIN,"dark spots,hyperpigmentation,age spots"
hair_loss,Hair Loss,HAIR,"hair loss,thinning,balding,hair fall"
dandruff,Dandruff,HAIR,"dandruff,flaky scalp,itchy scalp"
'''
    
    # Sample ingredients
    ingredients_csv = '''ingredient_id,name,benefits,safety_rating
salicylic_acid,Salicylic Acid,"Unclogs pores,Reduces acne",SAFE
hyaluronic_acid,Hyaluronic Acid,"Hydrates skin,Plumps skin",SAFE
niacinamide,Niacinamide,"Controls oil,Minimizes pores",SAFE
retinol,Retinol,"Reduces wrinkles,Improves texture",CAUTION
vitamin_c,Vitamin C,"Brightens skin,Fades dark spots",SAFE
ceramides,Ceramides,"Repairs barrier,Locks in moisture",SAFE
'''
    
    # Sample products
    products_csv = '''product_id,name,price,rating,category,image_url
prod_001,Clear Skin Cleanser,25.99,4.2,skincare,https://example.com/cleanser.jpg
prod_002,Hydrating Serum,45.00,4.5,skincare,https://example.com/serum.jpg
prod_003,Oil Control Moisturizer,32.50,4.1,skincare,https://example.com/moisturizer.jpg
prod_004,Anti-Aging Cream,89.99,4.7,skincare,https://example.com/cream.jpg
prod_005,Brightening Serum,55.00,4.3,skincare,https://example.com/brightening.jpg
'''
    
    with open(data_dir / "sample_concerns.csv", "w") as f:
        f.write(concerns_csv)
    
    with open(data_dir / "sample_ingredients.csv", "w") as f:
        f.write(ingredients_csv)
    
    with open(data_dir / "sample_products.csv", "w") as f:
        f.write(products_csv)

def create_zip_package(package_dir):
    """Create ZIP package for distribution"""
    zip_path = package_dir.parent / "beauty_chatbot_ddd_complete.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = Path(root) / file
                arc_path = file_path.relative_to(package_dir.parent)
                zipf.write(file_path, arc_path)

if __name__ == "__main__":
    create_deployment_package()
