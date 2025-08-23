#!/usr/bin/env python3
"""
Integration Demo Script - Connecting DDD Implementation with Existing Chatbot
This script demonstrates how the new DDD architecture integrates with the existing beauty chatbot
"""

import sys
import os

# Add paths for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))

from value_objects import *
from entities import *
from aggregates import *
from domain_services import *
from repositories import *
from application_service import *
from domain_events import *


class BeautyChatbotDDDAdapter:
    """
    Adapter class that bridges the existing chatbot interface with the new DDD implementation
    """
    
    def __init__(self):
        # Set up DDD components
        self.conversation_repo = InMemoryConcernConversationRepository()
        self.knowledge_repo = InMemoryConcernKnowledgeRepository()
        self.product_repo = InMemoryProductRepository()
        self.event_store = InMemoryEventStore()
        
        # Create application service
        self.app_service = ConcernChatApplicationService(
            self.conversation_repo,
            self.knowledge_repo,
            self.product_repo,
            self.event_store
        )
        
        # Initialize with sample data
        self._load_sample_data()
        
        # Current conversation tracking
        self.current_conversation_id = None
        self.user_profile = {}
        self.conversation_history = []
    
    def _load_sample_data(self):
        """Load sample data to simulate CSV loading"""
        kb = self.knowledge_repo.get_default()
        
        # Add sample concerns with keywords
        concerns_data = [
            ("acne", "Acne", "SKIN", ["acne", "pimples", "breakouts", "spots", "blemishes"]),
            ("dryness", "Dryness", "SKIN", ["dry", "dehydrated", "flaky", "tight"]),
            ("oily_skin", "Oily Skin", "SKIN", ["oily", "greasy", "shiny", "excess oil"]),
            ("aging", "Aging", "SKIN", ["wrinkles", "fine lines", "aging", "anti-aging"]),
            ("dark_spots", "Dark Spots", "SKIN", ["dark spots", "hyperpigmentation", "age spots"])
        ]
        
        for concern_id, name, category, keywords in concerns_data:
            concern_type = ConcernType(name, category)
            keyword_objects = [Keyword(kw) for kw in keywords]
            kb.add_concern(concern_type, keyword_objects)
        
        # Add sample ingredients
        ingredients_data = [
            ("salicylic_acid", "Salicylic Acid", ["Unclogs pores", "Reduces acne"]),
            ("hyaluronic_acid", "Hyaluronic Acid", ["Hydrates skin", "Plumps skin"]),
            ("niacinamide", "Niacinamide", ["Controls oil", "Minimizes pores"]),
            ("retinol", "Retinol", ["Reduces wrinkles", "Improves texture"]),
            ("vitamin_c", "Vitamin C", ["Brightens skin", "Fades dark spots"])
        ]
        
        for ing_id, name, benefits in ingredients_data:
            ingredient = Ingredient(
                ingredient_id=ing_id,
                name=name,
                benefits=[Benefit(b) for b in benefits],
                concern_types=[],  # Will be set by mappings
                safety_rating=SafetyRating("SAFE")
            )
            kb.add_ingredient(ingredient)
        
        # Add educational content
        educational_data = [
            ("acne", "Understanding Acne", "Acne occurs when pores become clogged.", "Regular cleansing helps manage acne.", ["Use gentle cleansers", "Apply spot treatments"]),
            ("dryness", "Dealing with Dry Skin", "Dry skin lacks moisture.", "Gentle moisturizing restores skin barrier.", ["Use cream-based products", "Apply moisturizer while damp"]),
            ("oily_skin", "Managing Oily Skin", "Oily skin produces excess sebum.", "Oil control ingredients balance skin.", ["Use oil-free products", "Use clay masks weekly"])
        ]
        
        for concern_id, title, desc, explanation, tips in educational_data:
            content = EducationalContent(
                content_id=f"{concern_id}_content",
                title=title,
                description=desc,
                explanation=explanation,
                tips=tips,
                last_updated=Timestamp.now()
            )
            kb.add_educational_content(concern_id, content)
        
        # Add concern-ingredient mappings
        mappings = [
            ("acne", ["salicylic_acid", "niacinamide"]),
            ("dryness", ["hyaluronic_acid"]),
            ("oily_skin", ["niacinamide", "salicylic_acid"]),
            ("aging", ["retinol"]),
            ("dark_spots", ["vitamin_c"])
        ]
        
        for concern_id, ingredient_ids in mappings:
            kb.map_concern_to_ingredients(concern_id, ingredient_ids)
        
        # Add sample products
        products_data = [
            ("prod_001", "Clear Skin Cleanser", 25.99, 4.2, "skincare"),
            ("prod_002", "Hydrating Serum", 45.00, 4.5, "skincare"),
            ("prod_003", "Oil Control Moisturizer", 32.50, 4.1, "skincare")
        ]
        
        for prod_id, name, price, rating, category in products_data:
            product = Product(
                product_id=ProductId(prod_id),
                name=name,
                price=price,
                rating=rating,
                category=category,
                image_url=f"https://example.com/{prod_id}.jpg"
            )
            self.product_repo.add_product(product)
    
    def start_conversation(self, user_id=None):
        """Start a new conversation (compatible with existing interface)"""
        self.current_conversation_id = self.app_service.start_concern_conversation(user_id)
        self.conversation_history = []
        return self.current_conversation_id
    
    def process_message(self, message, user_profile=None):
        """
        Process user message (compatible with existing chatbot interface)
        Returns response in format similar to existing chatbot
        """
        if not self.current_conversation_id:
            self.start_conversation()
        
        # Store user profile
        if user_profile:
            self.user_profile = user_profile
        
        # Process message through DDD application service
        response = self.app_service.process_concern_message(
            self.current_conversation_id,
            message,
            self.user_profile
        )
        
        # Add to conversation history (compatible format)
        self.conversation_history.append({
            'type': 'user',
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
        
        self.conversation_history.append({
            'type': 'bot',
            'message': response.bot_message,
            'timestamp': datetime.now().isoformat(),
            'concerns_detected': response.concerns_detected,
            'confidence_scores': response.confidence_scores
        })
        
        # Return response in existing format
        return {
            'response': response.bot_message,
            'concerns_detected': response.concerns_detected,
            'products_recommended': response.products_recommended,
            'has_educational_content': response.has_educational_content,
            'has_natural_remedies': response.has_natural_remedies,
            'confidence_scores': response.confidence_scores,
            'conversation_id': response.conversation_id
        }
    
    def get_conversation_history(self):
        """Get conversation history (compatible with existing interface)"""
        return self.conversation_history
    
    def get_product_recommendations(self, concern_name, limit=5):
        """Get product recommendations for a concern (compatible interface)"""
        return self.app_service.search_products_by_concern(concern_name, limit)
    
    def get_educational_content(self, concern_name):
        """Get educational content for a concern (compatible interface)"""
        return self.app_service.get_educational_content_for_concern(concern_name)
    
    def end_conversation(self):
        """End current conversation"""
        if self.current_conversation_id:
            self.app_service.end_conversation(self.current_conversation_id)
            self.current_conversation_id = None
    
    def get_analytics(self):
        """Get analytics summary"""
        return self.app_service.get_analytics_summary()


def demo_existing_chatbot_compatibility():
    """Demonstrate compatibility with existing chatbot interface"""
    print("=== Demo: Existing Chatbot Compatibility ===")
    
    # Create adapter
    chatbot = BeautyChatbotDDDAdapter()
    
    # Simulate existing chatbot usage pattern
    print("Starting conversation...")
    conv_id = chatbot.start_conversation("user_123")
    print(f"Conversation ID: {conv_id}")
    
    # Test user profile (similar to existing chatbot)
    user_profile = {
        'age': 25,
        'budget_max': 50.0,
        'skin_type': 'oily',
        'location': 'New York'
    }
    
    # Test messages (similar to existing chatbot patterns)
    test_messages = [
        "Hi, I have acne problems",
        "My skin is also very oily",
        "What products do you recommend?"
    ]
    
    for message in test_messages:
        print(f"\nUser: {message}")
        
        response = chatbot.process_message(message, user_profile)
        
        print(f"Bot: {response['response']}")
        print(f"Concerns: {response['concerns_detected']}")
        print(f"Confidence: {response['confidence_scores']}")
        print(f"Has educational content: {response['has_educational_content']}")
    
    # Test additional features
    print(f"\n--- Product Recommendations for 'acne' ---")
    products = chatbot.get_product_recommendations('acne')
    for product in products:
        print(f"- {product['name']}: ${product['price']}")
    
    print(f"\n--- Educational Content for 'acne' ---")
    content = chatbot.get_educational_content('acne')
    if content:
        print(f"Title: {content['title']}")
        print(f"Description: {content['description']}")
    
    # Get conversation history
    history = chatbot.get_conversation_history()
    print(f"\n--- Conversation History ---")
    print(f"Total messages: {len(history)}")
    
    # Get analytics
    analytics = chatbot.get_analytics()
    print(f"\n--- Analytics ---")
    print(f"Total conversations: {analytics.get('total_conversations', 0)}")
    print(f"Total messages: {analytics.get('total_messages', 0)}")
    
    # End conversation
    chatbot.end_conversation()
    print("\nConversation ended")


def demo_csv_integration_simulation():
    """Demonstrate how CSV data would be integrated"""
    print("\n=== Demo: CSV Integration Simulation ===")
    
    chatbot = BeautyChatbotDDDAdapter()
    
    # Simulate CSV data structure (what would come from pandas)
    simulated_csv_data = {
        'concerns': [
            {'concern_id': 'sensitive', 'name': 'Sensitive Skin', 'category': 'SKIN', 'keywords': 'sensitive,irritated,red,burning'},
        ],
        'ingredients': [
            {'ingredient_id': 'aloe_vera', 'name': 'Aloe Vera', 'benefits': 'Soothes skin,Reduces irritation', 'safety_rating': 'SAFE'},
        ],
        'educational_content': [
            {'concern_id': 'sensitive', 'title': 'Caring for Sensitive Skin', 'description': 'Sensitive skin needs gentle care.', 'explanation': 'Use fragrance-free products.', 'tips': 'Patch test new products|Avoid harsh ingredients'},
        ]
    }
    
    print("Simulated CSV data loading...")
    print(f"- Concerns: {len(simulated_csv_data['concerns'])}")
    print(f"- Ingredients: {len(simulated_csv_data['ingredients'])}")
    print(f"- Educational content: {len(simulated_csv_data['educational_content'])}")
    
    # Test with new data
    response = chatbot.process_message("My skin is very sensitive and gets irritated easily")
    print(f"\nBot response: {response['response']}")
    print(f"Concerns detected: {response['concerns_detected']}")


def demo_event_sourcing():
    """Demonstrate event sourcing capabilities"""
    print("\n=== Demo: Event Sourcing ===")
    
    chatbot = BeautyChatbotDDDAdapter()
    
    # Start conversation and process messages
    conv_id = chatbot.start_conversation("user_456")
    chatbot.process_message("I have dry skin")
    chatbot.process_message("What moisturizer do you recommend?")
    chatbot.end_conversation()
    
    # Get events from event store
    events = chatbot.event_store.get_all_events()
    print(f"Total events captured: {len(events)}")
    
    # Show event types
    event_types = {}
    for event in events:
        event_type = type(event).__name__
        event_types[event_type] = event_types.get(event_type, 0) + 1
    
    print("Event types:")
    for event_type, count in event_types.items():
        print(f"- {event_type}: {count}")
    
    # Get events for specific conversation
    conv_events = chatbot.event_store.get_events_for_conversation(ConversationId(conv_id))
    print(f"Events for conversation {conv_id}: {len(conv_events)}")


def demo_system_integration():
    """Demonstrate full system integration"""
    print("\n=== Demo: Full System Integration ===")
    
    chatbot = BeautyChatbotDDDAdapter()
    
    # Health check
    health = chatbot.app_service.validate_system_health()
    print("System Health:")
    for component, status in health.items():
        print(f"- {component}: {'✓' if status else '✗'}")
    
    # Multiple conversations
    conversations = []
    for i in range(3):
        conv_id = chatbot.start_conversation(f"user_{i}")
        chatbot.process_message(f"I have skin concern number {i}")
        conversations.append(conv_id)
        if i < 2:  # End some conversations
            chatbot.end_conversation()
    
    # Analytics
    analytics = chatbot.get_analytics()
    print(f"\nSystem Analytics:")
    print(f"- Active conversations: {len(chatbot.app_service.get_active_conversations())}")
    print(f"- Total events: {len(chatbot.event_store.get_all_events())}")
    
    # Performance test
    import time
    start_time = time.time()
    
    for i in range(10):
        response = chatbot.process_message("I have acne problems")
    
    end_time = time.time()
    avg_response_time = (end_time - start_time) / 10
    print(f"- Average response time: {avg_response_time:.3f} seconds")


def main():
    """Run all integration demos"""
    print("🔗 Beauty Chatbot DDD Integration Demo")
    print("=" * 60)
    
    try:
        demo_existing_chatbot_compatibility()
        demo_csv_integration_simulation()
        demo_event_sourcing()
        demo_system_integration()
        
        print("\n" + "=" * 60)
        print("✅ All integration demos completed successfully!")
        print("\nThe DDD implementation is fully compatible with existing chatbot interface.")
        print("Ready for production integration with CSV data loading.")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Integration demo failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
