"""
Simplified Integrated Beauty Chatbot with DDD Architecture
This module combines the existing chatbot functionality with the new DDD implementation
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import random

# Add DDD domain to path
ddd_path = str(Path(__file__).parent.parent / "ddd_domain")
sys.path.append(ddd_path)

# Import DDD components
from application_service import ConcernChatApplicationService
from repositories import (
    InMemoryConcernConversationRepository,
    InMemoryConcernKnowledgeRepository, 
    InMemoryProductRepository
)
from domain_events import InMemoryEventStore
from value_objects import *
from entities import *


class SimplifiedBeautyChatbot:
    """
    Simplified Beauty Chatbot that integrates DDD architecture with basic functionality
    """
    
    def __init__(self):
        print("🚀 Initializing Simplified Beauty Chatbot with DDD...")
        
        # Initialize DDD components
        self._setup_ddd_components()
        
        # Conversation state
        self.current_conversation_id = None
        self.user_profile = {}
        self.conversation_history = []
        self.cart = []
        
        # Load sample data
        self._load_sample_data()
        
        print("✅ Chatbot initialized successfully!")
    
    def _setup_ddd_components(self):
        """Initialize DDD architecture components"""
        # Create repositories
        self.conversation_repo = InMemoryConcernConversationRepository()
        self.knowledge_repo = InMemoryConcernKnowledgeRepository()
        self.product_repo = InMemoryProductRepository()
        self.event_store = InMemoryEventStore()
        
        # Create application service
        self.ddd_service = ConcernChatApplicationService(
            self.conversation_repo,
            self.knowledge_repo,
            self.product_repo,
            self.event_store
        )
    
    def _load_sample_data(self):
        """Load sample data into DDD system"""
        kb = self.knowledge_repo.get_default()
        
        # Sample concerns with keywords
        concerns_data = [
            ("acne", "Acne", "SKIN", ["acne", "pimples", "breakouts", "spots", "blemishes"]),
            ("dryness", "Dryness", "SKIN", ["dry", "dehydrated", "flaky", "tight"]),
            ("oily_skin", "Oily Skin", "SKIN", ["oily", "greasy", "shiny", "excess oil"]),
            ("aging", "Aging", "SKIN", ["wrinkles", "fine lines", "aging", "anti-aging"]),
            ("dark_spots", "Dark Spots", "SKIN", ["dark spots", "hyperpigmentation", "age spots"]),
            ("sensitive", "Sensitive Skin", "SKIN", ["sensitive", "irritated", "red", "burning"]),
            ("hair_loss", "Hair Loss", "HAIR", ["hair loss", "thinning", "balding", "hair fall"]),
            ("dandruff", "Dandruff", "HAIR", ["dandruff", "flaky scalp", "itchy scalp"])
        ]
        
        for concern_id, name, category, keywords in concerns_data:
            concern_type = ConcernType(name, category)
            keyword_objects = [Keyword(kw) for kw in keywords]
            kb.add_concern(concern_type, keyword_objects)
        
        # Sample ingredients
        ingredients_data = [
            ("salicylic_acid", "Salicylic Acid", ["Unclogs pores", "Reduces acne"]),
            ("hyaluronic_acid", "Hyaluronic Acid", ["Hydrates skin", "Plumps skin"]),
            ("niacinamide", "Niacinamide", ["Controls oil", "Minimizes pores"]),
            ("retinol", "Retinol", ["Reduces wrinkles", "Improves texture"]),
            ("vitamin_c", "Vitamin C", ["Brightens skin", "Fades dark spots"]),
            ("ceramides", "Ceramides", ["Repairs barrier", "Locks in moisture"])
        ]
        
        for ing_id, name, benefits in ingredients_data:
            ingredient = Ingredient(
                ingredient_id=ing_id,
                name=name,
                benefits=[Benefit(b) for b in benefits],
                concern_types=[],
                safety_rating=SafetyRating("SAFE")
            )
            kb.add_ingredient(ingredient)
        
        # Educational content (only for concerns that exist)
        educational_data = [
            ("acne", "Understanding Acne", "Acne occurs when pores become clogged with oil and dead skin cells.", "Regular cleansing with salicylic acid can help manage acne effectively.", ["Use gentle cleansers", "Apply spot treatments", "Don't over-wash"]),
            ("dryness", "Dealing with Dry Skin", "Dry skin lacks moisture and can feel tight and uncomfortable.", "Gentle moisturizing and avoiding harsh products can restore skin barrier.", ["Use cream-based products", "Apply moisturizer while damp", "Avoid alcohol-based toners"]),
            ("oily_skin", "Managing Oily Skin", "Oily skin produces excess sebum, leading to shine and enlarged pores.", "Oil control and pore-minimizing ingredients can balance oily skin.", ["Use oil-free products", "Blot excess oil", "Use clay masks weekly"]),
            ("aging", "Anti-Aging Skincare", "Aging skin shows signs of wrinkles, fine lines, and loss of elasticity.", "Retinoids and antioxidants can help reduce signs of aging.", ["Start retinoids slowly", "Always use sunscreen", "Be patient with results"])
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
        
        # Concern-ingredient mappings (only for existing concerns)
        mappings = [
            ("acne", ["salicylic_acid", "niacinamide"]),
            ("dryness", ["hyaluronic_acid", "ceramides"]),
            ("oily_skin", ["niacinamide", "salicylic_acid"]),
            ("aging", ["retinol", "vitamin_c"]),
            ("dark_spots", ["vitamin_c", "niacinamide"])
        ]
        
        for concern_id, ingredient_ids in mappings:
            kb.map_concern_to_ingredients(concern_id, ingredient_ids)
        
        # Sample products
        products_data = [
            ("prod_001", "Clear Skin Cleanser", 25.99, 4.2, "skincare"),
            ("prod_002", "Hydrating Serum", 45.00, 4.5, "skincare"),
            ("prod_003", "Oil Control Moisturizer", 32.50, 4.1, "skincare"),
            ("prod_004", "Anti-Aging Cream", 89.99, 4.7, "skincare"),
            ("prod_005", "Brightening Serum", 55.00, 4.3, "skincare")
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
        """Start a new conversation"""
        self.current_conversation_id = self.ddd_service.start_concern_conversation(user_id)
        self.conversation_history = []
        self.cart = []
        return self.current_conversation_id
    
    def detect_prompt_type(self, message):
        """Detect the type of user prompt"""
        message_lower = message.lower()
        
        # Check for concern-based keywords
        concern_keywords = [
            'acne', 'pimples', 'breakouts', 'dry', 'oily', 'wrinkles', 
            'dark spots', 'sensitive', 'hair loss', 'dandruff', 'aging'
        ]
        
        if any(keyword in message_lower for keyword in concern_keywords):
            return "concern"
        
        # Check for exploration keywords
        exploration_keywords = [
            'recommend', 'suggest', 'looking for', 'need', 'want', 'show me',
            'best', 'good', 'products', 'skincare', 'makeup', 'haircare'
        ]
        
        if any(keyword in message_lower for keyword in exploration_keywords):
            return "exploration"
        
        # Default to chitchat
        return "chitchat"
    
    def process_message(self, message, user_profile=None):
        """Process user message with integrated DDD functionality"""
        if user_profile:
            self.user_profile = user_profile
        
        if not self.current_conversation_id:
            self.start_conversation()
        
        # Detect prompt type
        prompt_type = self.detect_prompt_type(message)
        
        # Add to conversation history
        self.conversation_history.append({
            'type': 'user',
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Process based on type
        if prompt_type == "concern":
            response = self._handle_concern_based_chat(message)
        elif prompt_type == "exploration":
            response = self._handle_exploration_chat(message)
        else:
            response = self._handle_chitchat(message)
        
        # Add bot response to history
        self.conversation_history.append({
            'type': 'bot',
            'message': response['response'],
            'timestamp': datetime.now().isoformat(),
            'prompt_type': prompt_type
        })
        
        return response
    
    def _handle_concern_based_chat(self, message):
        """Handle concern-based conversations using DDD service"""
        try:
            ddd_response = self.ddd_service.process_concern_message(
                self.current_conversation_id,
                message,
                self.user_profile
            )
            
            # Add natural remedies
            natural_remedies = self._get_natural_remedies(ddd_response.concerns_detected)
            
            return {
                'response': ddd_response.bot_message,
                'concerns_detected': ddd_response.concerns_detected,
                'confidence_scores': ddd_response.confidence_scores,
                'has_educational_content': ddd_response.has_educational_content,
                'has_natural_remedies': len(natural_remedies) > 0,
                'natural_remedies': natural_remedies,
                'products_recommended': ddd_response.products_recommended,
                'prompt_type': 'concern'
            }
            
        except Exception as e:
            return {
                'response': f"I'd be happy to help with your beauty concerns! Could you tell me more about what specific issues you're experiencing? (Error: {str(e)})",
                'concerns_detected': [],
                'confidence_scores': {},
                'has_educational_content': False,
                'has_natural_remedies': False,
                'natural_remedies': [],
                'products_recommended': [],
                'prompt_type': 'concern'
            }
    
    def _handle_exploration_chat(self, message):
        """Handle exploration-based conversations"""
        response_text = """I'd love to help you explore beauty products! Here are some popular categories:

**Skincare Essentials:**
• Cleansers for daily cleansing
• Moisturizers for hydration  
• Serums for targeted treatments
• Sunscreen for protection

**Popular Products:**
• Clear Skin Cleanser ($25.99) - Great for acne-prone skin
• Hydrating Serum ($45.00) - Perfect for dry skin
• Oil Control Moisturizer ($32.50) - Ideal for oily skin

What specific category interests you most? I can provide personalized recommendations!"""
        
        return {
            'response': response_text,
            'concerns_detected': [],
            'confidence_scores': {},
            'has_educational_content': False,
            'has_natural_remedies': False,
            'natural_remedies': [],
            'products_recommended': ['prod_001', 'prod_002', 'prod_003'],
            'prompt_type': 'exploration'
        }
    
    def _handle_chitchat(self, message):
        """Handle general chitchat"""
        chitchat_responses = [
            "Hello! I'm your beauty expert assistant. I'm here to help you with skincare, haircare, and makeup questions. What beauty concerns can I help you with today?",
            "Hi there! I love talking about beauty and skincare. Do you have any specific skin or hair concerns you'd like to discuss?",
            "Great to chat with you! I'm passionate about helping people find the right beauty products. What's on your mind regarding your beauty routine?",
            "Hello! I'm here to provide personalized beauty advice. Whether it's skincare, haircare, or makeup, I'm ready to help. What would you like to know?"
        ]
        
        response_text = random.choice(chitchat_responses)
        
        return {
            'response': response_text,
            'concerns_detected': [],
            'confidence_scores': {},
            'has_educational_content': False,
            'has_natural_remedies': False,
            'natural_remedies': [],
            'products_recommended': [],
            'prompt_type': 'chitchat'
        }
    
    def _get_natural_remedies(self, concerns):
        """Get natural remedies for detected concerns"""
        remedies = []
        
        remedy_map = {
            'Acne': ['Honey & Cinnamon Mask: Mix 2 tbsp honey with 1 tsp cinnamon powder. Apply for 15 minutes.'],
            'Dryness': ['Oatmeal & Honey Mask: Mix oatmeal, honey, and milk into paste. Apply for 15 minutes.'],
            'Oily Skin': ['Clay Mask: Use bentonite clay with water. Apply weekly for oil control.'],
            'Dark Spots': ['Lemon & Honey Treatment: Mix lemon juice with honey. Apply to spots nightly.'],
            'Sensitive Skin': ['Aloe Vera Gel: Apply pure aloe vera gel to soothe irritated skin.']
        }
        
        for concern in concerns:
            if concern in remedy_map:
                remedies.extend(remedy_map[concern])
        
        return remedies
    
    def get_conversation_history(self):
        """Get conversation history"""
        return self.conversation_history
    
    def add_to_cart(self, product_info):
        """Add product to cart"""
        self.cart.append({
            'product': product_info,
            'added_at': datetime.now().isoformat()
        })
    
    def get_cart(self):
        """Get current cart contents"""
        return self.cart
    
    def clear_cart(self):
        """Clear cart contents"""
        self.cart = []
    
    def get_analytics(self):
        """Get analytics from DDD system"""
        try:
            ddd_analytics = self.ddd_service.get_analytics_summary()
            return {
                **ddd_analytics,
                'cart_items': len(self.cart),
                'conversation_messages': len(self.conversation_history)
            }
        except:
            return {
                'total_conversations': 1 if self.current_conversation_id else 0,
                'total_messages': len(self.conversation_history),
                'cart_items': len(self.cart)
            }
    
    def end_conversation(self):
        """End current conversation"""
        if self.current_conversation_id:
            try:
                self.ddd_service.end_conversation(self.current_conversation_id)
            except:
                pass
            self.current_conversation_id = None


def create_chatbot():
    """Factory function to create chatbot instance"""
    return SimplifiedBeautyChatbot()


if __name__ == "__main__":
    # Test the simplified chatbot
    print("🧪 Testing Simplified Beauty Chatbot with DDD")
    print("=" * 50)
    
    try:
        chatbot = create_chatbot()
        
        # Test different message types
        test_messages = [
            "Hi there!",
            "I have acne problems on my face",
            "My skin is very dry and flaky", 
            "Can you recommend some good skincare products?",
            "What's the best moisturizer for oily skin?"
        ]
        
        for message in test_messages:
            print(f"\nUser: {message}")
            response = chatbot.process_message(message)
            print(f"Bot ({response['prompt_type']}): {response['response'][:150]}...")
            if response['concerns_detected']:
                print(f"Concerns: {response['concerns_detected']}")
            if response['natural_remedies']:
                print(f"Natural Remedies: {len(response['natural_remedies'])} available")
        
        # Test analytics
        analytics = chatbot.get_analytics()
        print(f"\n📊 Analytics:")
        print(f"- Conversations: {analytics.get('total_conversations', 0)}")
        print(f"- Messages: {analytics.get('total_messages', 0)}")
        print(f"- Cart items: {analytics.get('cart_items', 0)}")
        
        # Test cart functionality
        chatbot.add_to_cart({'name': 'Clear Skin Cleanser', 'price': 25.99})
        print(f"- Cart after adding item: {len(chatbot.get_cart())} items")
        
        print("\n✅ Simplified chatbot test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
