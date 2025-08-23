"""
Integrated Beauty Chatbot with DDD Architecture
This module combines the existing chatbot functionality with the new DDD implementation
"""

import sys
import os
from pathlib import Path

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

# Import existing chatbot components
sys.path.append(str(Path(__file__).parent.parent / "legacy"))

import re
import nltk
from collections import defaultdict
import pandas as pd
from datetime import datetime


class IntegratedBeautyChatbot:
    """
    Integrated Beauty Chatbot that combines existing functionality with DDD architecture
    """
    
    def __init__(self):
        # Initialize DDD components
        self._setup_ddd_components()
        
        # Initialize legacy components for backward compatibility
        self._setup_legacy_components()
        
        # Conversation state
        self.current_conversation_id = None
        self.user_profile = {}
        self.conversation_history = []
        self.cart = []
        
        # Load sample data
        self._load_sample_data()
    
    def _setup_ddd_components(self):
        """Initialize DDD architecture components"""
        print("🏗️ Setting up DDD components...")
        
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
        
        print("✅ DDD components initialized")
    
    def _setup_legacy_components(self):
        """Initialize legacy chatbot components for compatibility"""
        print("🔄 Setting up legacy components...")
        
        # Legacy concern keywords (for fallback)
        self.legacy_concern_keywords = {
            'acne': ['acne', 'pimples', 'breakouts', 'spots', 'blemishes', 'blackheads', 'whiteheads'],
            'dryness': ['dry', 'dehydrated', 'flaky', 'tight', 'rough', 'cracked'],
            'oily': ['oily', 'greasy', 'shiny', 'excess oil', 'sebum'],
            'aging': ['wrinkles', 'fine lines', 'aging', 'anti-aging', 'mature skin', 'sagging'],
            'dark_spots': ['dark spots', 'hyperpigmentation', 'melasma', 'age spots', 'sun spots'],
            'sensitive': ['sensitive', 'irritated', 'red', 'burning', 'stinging', 'reactive'],
            'dull': ['dull', 'tired', 'lackluster', 'uneven tone', 'brightness'],
            'hair_loss': ['hair loss', 'thinning', 'balding', 'hair fall', 'receding'],
            'dandruff': ['dandruff', 'flaky scalp', 'itchy scalp', 'dry scalp'],
            'frizzy_hair': ['frizzy', 'unmanageable', 'flyaways', 'humidity', 'coarse hair']
        }
        
        # Legacy natural remedies
        self.legacy_natural_remedies = {
            'acne': [
                {
                    'name': 'Honey & Cinnamon Mask',
                    'ingredients': ['2 tbsp raw honey', '1 tsp cinnamon powder'],
                    'instructions': 'Mix honey and cinnamon. Apply to clean face for 15 minutes. Rinse with warm water.',
                    'benefits': 'Honey has antibacterial properties, cinnamon reduces inflammation'
                }
            ],
            'dryness': [
                {
                    'name': 'Oatmeal & Honey Mask',
                    'ingredients': ['1/2 cup oatmeal', '2 tbsp honey', '2 tbsp milk'],
                    'instructions': 'Mix ingredients into paste. Apply for 15 minutes. Rinse gently.',
                    'benefits': 'Oatmeal soothes, honey moisturizes, milk provides lactic acid'
                }
            ]
        }
        
        print("✅ Legacy components initialized")
    
    def _load_sample_data(self):
        """Load sample data into DDD system"""
        print("📊 Loading sample data...")
        
        # Load sample data through DDD service
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
            ("ceramides", "Ceramides", ["Repairs barrier", "Locks in moisture"]),
            ("tea_tree_oil", "Tea Tree Oil", ["Antibacterial", "Reduces inflammation"])
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
        
        # Educational content
        educational_data = [
            ("acne", "Understanding Acne", "Acne occurs when pores become clogged with oil and dead skin cells.", "Regular cleansing with salicylic acid can help manage acne effectively.", ["Use gentle cleansers", "Apply spot treatments", "Don't over-wash"]),
            ("dryness", "Dealing with Dry Skin", "Dry skin lacks moisture and can feel tight and uncomfortable.", "Gentle moisturizing and avoiding harsh products can restore skin barrier.", ["Use cream-based products", "Apply moisturizer while damp", "Avoid alcohol-based toners"]),
            ("oily_skin", "Managing Oily Skin", "Oily skin produces excess sebum, leading to shine and enlarged pores.", "Oil control and pore-minimizing ingredients can balance oily skin.", ["Use oil-free products", "Blot excess oil", "Use clay masks weekly"]),
            ("sensitive", "Caring for Sensitive Skin", "Sensitive skin reacts easily to products and environmental factors.", "Use fragrance-free, gentle products and patch test new items.", ["Patch test new products", "Avoid harsh ingredients", "Use gentle cleansers"])
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
        
        # Concern-ingredient mappings
        mappings = [
            ("acne", ["salicylic_acid", "niacinamide", "tea_tree_oil"]),
            ("dryness", ["hyaluronic_acid", "ceramides"]),
            ("oily_skin", ["niacinamide", "salicylic_acid"]),
            ("aging", ["retinol", "vitamin_c"]),
            ("dark_spots", ["vitamin_c", "niacinamide"]),
            ("sensitive", ["ceramides", "hyaluronic_acid"])
        ]
        
        for concern_id, ingredient_ids in mappings:
            kb.map_concern_to_ingredients(concern_id, ingredient_ids)
        
        print("✅ Sample data loaded successfully")
    
    def start_conversation(self, user_id=None):
        """Start a new conversation"""
        self.current_conversation_id = self.ddd_service.start_concern_conversation(user_id)
        self.conversation_history = []
        self.cart = []
        return self.current_conversation_id
    
    def detect_prompt_type(self, message):
        """Detect the type of user prompt (concern, exploration, chitchat)"""
        message_lower = message.lower()
        
        # Check for concern-based keywords using DDD service
        try:
            if not self.current_conversation_id:
                self.start_conversation()
            
            response = self.ddd_service.process_concern_message(
                self.current_conversation_id, 
                message, 
                self.user_profile
            )
            
            if response.concerns_detected:
                return "concern", response.concerns_detected
        except:
            pass
        
        # Check for exploration keywords
        exploration_keywords = [
            'recommend', 'suggest', 'looking for', 'need', 'want', 'show me',
            'best', 'good', 'products', 'skincare', 'makeup', 'haircare'
        ]
        
        if any(keyword in message_lower for keyword in exploration_keywords):
            return "exploration", []
        
        # Default to chitchat
        return "chitchat", []
    
    def process_message(self, message, user_profile=None):
        """Process user message with integrated DDD and legacy functionality"""
        if user_profile:
            self.user_profile = user_profile
        
        if not self.current_conversation_id:
            self.start_conversation()
        
        # Detect prompt type
        prompt_type, detected_concerns = self.detect_prompt_type(message)
        
        # Add to conversation history
        self.conversation_history.append({
            'type': 'user',
            'message': message,
            'timestamp': datetime.now().isoformat()
        })
        
        # Process based on type
        if prompt_type == "concern":
            response = self._handle_concern_based_chat(message, detected_concerns)
        elif prompt_type == "exploration":
            response = self._handle_exploration_chat(message)
        else:
            response = self._handle_chitchat(message)
        
        # Add bot response to history
        self.conversation_history.append({
            'type': 'bot',
            'message': response['response'],
            'timestamp': datetime.now().isoformat(),
            'prompt_type': prompt_type,
            'concerns_detected': detected_concerns
        })
        
        return response
    
    def _handle_concern_based_chat(self, message, concerns):
        """Handle concern-based conversations using DDD service"""
        try:
            ddd_response = self.ddd_service.process_concern_message(
                self.current_conversation_id,
                message,
                self.user_profile
            )
            
            # Enhance with natural remedies from legacy system
            natural_remedies = []
            for concern in ddd_response.concerns_detected:
                concern_key = concern.lower().replace(" ", "_")
                if concern_key in self.legacy_natural_remedies:
                    natural_remedies.extend(self.legacy_natural_remedies[concern_key])
            
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
            # Fallback to legacy concern detection
            return self._legacy_concern_fallback(message)
    
    def _handle_exploration_chat(self, message):
        """Handle exploration-based conversations"""
        # Simple exploration response
        response_text = """I'd love to help you explore beauty products! Here are some popular categories:

**Skincare Essentials:**
• Cleansers for daily cleansing
• Moisturizers for hydration
• Serums for targeted treatments
• Sunscreen for protection

**Makeup Favorites:**
• Foundation for coverage
• Concealer for spot correction
• Mascara for lashes
• Lipstick for color

What specific category interests you most? I can provide personalized recommendations based on your skin type and concerns!"""
        
        return {
            'response': response_text,
            'concerns_detected': [],
            'confidence_scores': {},
            'has_educational_content': False,
            'has_natural_remedies': False,
            'natural_remedies': [],
            'products_recommended': [],
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
        
        import random
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
    
    def _legacy_concern_fallback(self, message):
        """Fallback to legacy concern detection if DDD fails"""
        message_lower = message.lower()
        detected_concerns = []
        
        for concern, keywords in self.legacy_concern_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                detected_concerns.append(concern.replace('_', ' ').title())
        
        if detected_concerns:
            response_text = f"I understand you're dealing with {', '.join(detected_concerns).lower()}. Let me help you with some recommendations and natural remedies."
        else:
            response_text = "I'd be happy to help with your beauty concerns! Could you tell me more about what specific issues you're experiencing?"
        
        return {
            'response': response_text,
            'concerns_detected': detected_concerns,
            'confidence_scores': {concern: 0.7 for concern in detected_concerns},
            'has_educational_content': False,
            'has_natural_remedies': len(detected_concerns) > 0,
            'natural_remedies': [],
            'products_recommended': [],
            'prompt_type': 'concern'
        }
    
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
            return self.ddd_service.get_analytics_summary()
        except:
            return {
                'total_conversations': len(self.conversation_history) // 2,
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


# Factory function for easy instantiation
def create_integrated_chatbot():
    """Factory function to create integrated chatbot instance"""
    return IntegratedBeautyChatbot()


if __name__ == "__main__":
    # Test the integrated chatbot
    print("🧪 Testing Integrated Beauty Chatbot")
    print("=" * 40)
    
    chatbot = create_integrated_chatbot()
    
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
        print(f"Bot ({response['prompt_type']}): {response['response'][:100]}...")
        if response['concerns_detected']:
            print(f"Concerns: {response['concerns_detected']}")
    
    print(f"\nConversation History: {len(chatbot.get_conversation_history())} messages")
    print(f"Analytics: {chatbot.get_analytics()}")
    
    print("\n✅ Integrated chatbot test completed!")
