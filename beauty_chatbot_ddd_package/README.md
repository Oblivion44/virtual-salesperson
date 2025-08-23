# Beauty Recommendation Chatbot - DDD Enhanced Version

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
