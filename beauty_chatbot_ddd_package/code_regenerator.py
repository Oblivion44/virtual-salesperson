#!/usr/bin/env python3
"""
Code Regeneration System for Beauty Chatbot
Automatically updates the chatbot code based on collected data
"""

import os
import csv
import json
from typing import Dict, List, Any
from datetime import datetime


class BeautyChatbotCodeRegenerator:
    """Regenerates chatbot code based on collected data"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.collected_data = self._load_collected_data()
    
    def _load_collected_data(self) -> Dict[str, List[Dict]]:
        """Load collected data from CSV files"""
        data = {'products': [], 'ingredients': [], 'reviews': []}
        
        # Load products
        products_file = os.path.join(self.data_dir, 'collected_products.csv')
        if os.path.exists(products_file):
            with open(products_file, 'r', encoding='utf-8') as f:
                data['products'] = list(csv.DictReader(f))
        
        # Load ingredients
        ingredients_file = os.path.join(self.data_dir, 'collected_ingredients.csv')
        if os.path.exists(ingredients_file):
            with open(ingredients_file, 'r', encoding='utf-8') as f:
                data['ingredients'] = list(csv.DictReader(f))
        
        # Load reviews
        reviews_file = os.path.join(self.data_dir, 'collected_reviews.csv')
        if os.path.exists(reviews_file):
            with open(reviews_file, 'r', encoding='utf-8') as f:
                data['reviews'] = list(csv.DictReader(f))
        
        return data
    
    def generate_enhanced_concern_detection(self) -> str:
        """Generate enhanced concern detection based on collected data"""
        
        # Extract unique concerns from all data sources
        all_concerns = set()
        
        # From products
        for product in self.collected_data['products']:
            concerns = product.get('concerns_addressed', '').split(',')
            all_concerns.update([c.strip().lower() for c in concerns if c.strip()])
        
        # From ingredients
        for ingredient in self.collected_data['ingredients']:
            concerns = ingredient.get('concerns_addressed', '').split(',')
            all_concerns.update([c.strip().lower() for c in concerns if c.strip()])
        
        # From reviews
        for review in self.collected_data['reviews']:
            concerns = review.get('concerns', '').split(',')
            all_concerns.update([c.strip().lower() for c in concerns if c.strip()])
        
        # Generate concern detection code
        concern_detection_code = f'''
# Enhanced Concern Detection - Generated from collected data
# Generated on: {datetime.now().isoformat()}

ENHANCED_CONCERN_KEYWORDS = {{'''
        
        for concern in sorted(all_concerns):
            if concern:
                # Generate related keywords for each concern
                keywords = self._generate_concern_keywords(concern)
                concern_detection_code += f'''
    '{concern}': {keywords},'''
        
        concern_detection_code += '''
}

def detect_concerns_enhanced(message: str) -> List[str]:
    """Enhanced concern detection using collected data"""
    message_lower = message.lower()
    detected_concerns = []
    
    for concern, keywords in ENHANCED_CONCERN_KEYWORDS.items():
        if any(keyword in message_lower for keyword in keywords):
            detected_concerns.append(concern.title())
    
    return detected_concerns
'''
        
        return concern_detection_code
    
    def _generate_concern_keywords(self, concern: str) -> List[str]:
        """Generate related keywords for a concern"""
        keyword_map = {
            'acne': ['acne', 'pimples', 'breakouts', 'spots', 'blemishes', 'blackheads', 'whiteheads'],
            'aging': ['aging', 'wrinkles', 'fine lines', 'anti-aging', 'mature skin', 'age spots'],
            'dryness': ['dry', 'dehydrated', 'flaky', 'tight', 'rough', 'cracked'],
            'oily': ['oily', 'greasy', 'shiny', 'excess oil', 'sebum'],
            'sensitive': ['sensitive', 'irritated', 'red', 'burning', 'stinging', 'reactive'],
            'dark spots': ['dark spots', 'hyperpigmentation', 'melasma', 'age spots', 'sun spots'],
            'dull': ['dull', 'tired', 'lackluster', 'uneven tone', 'brightness'],
            'large pores': ['pores', 'large pores', 'enlarged pores', 'blackheads'],
            'rosacea': ['rosacea', 'redness', 'flushing', 'broken capillaries'],
            'eczema': ['eczema', 'dermatitis', 'itchy', 'inflamed']
        }
        
        return keyword_map.get(concern.lower(), [concern.lower()])
    
    def generate_enhanced_product_recommendations(self) -> str:
        """Generate product recommendation system based on collected data"""
        
        product_code = f'''
# Enhanced Product Recommendations - Generated from collected data
# Generated on: {datetime.now().isoformat()}

COLLECTED_PRODUCTS = ['''
        
        for product in self.collected_data['products']:
            product_code += f'''
    {{
        'id': '{product.get('product_id', '')}',
        'name': '{product.get('name', '')}',
        'brand': '{product.get('brand', '')}',
        'category': '{product.get('category', '')}',
        'price': {product.get('price', 0)},
        'rating': {product.get('rating', 0)},
        'description': '{product.get('description', '').replace("'", "\\'")}',
        'key_ingredients': {self._parse_list_field(product.get('key_ingredients', ''))},
        'skin_types': {self._parse_list_field(product.get('skin_types', ''))},
        'concerns_addressed': {self._parse_list_field(product.get('concerns_addressed', ''))},
        'image_url': '{product.get('image_url', '')}'
    }},'''
        
        product_code += '''
]

def get_product_recommendations(concerns: List[str], skin_type: str = None) -> List[Dict]:
    """Get product recommendations based on concerns and skin type"""
    recommendations = []
    
    for product in COLLECTED_PRODUCTS:
        # Check if product addresses any of the concerns
        product_concerns = [c.lower() for c in product['concerns_addressed']]
        user_concerns = [c.lower() for c in concerns]
        
        if any(concern in product_concerns for concern in user_concerns):
            # Check skin type compatibility if specified
            if skin_type:
                product_skin_types = [st.lower() for st in product['skin_types']]
                if skin_type.lower() not in product_skin_types and 'all' not in product_skin_types:
                    continue
            
            recommendations.append(product)
    
    # Sort by rating (highest first)
    recommendations.sort(key=lambda x: x['rating'], reverse=True)
    return recommendations[:5]  # Return top 5
'''
        
        return product_code
    
    def _parse_list_field(self, field_value: str) -> List[str]:
        """Parse comma-separated field into list"""
        if not field_value or field_value == '[]':
            return []
        
        # Handle both string and list formats
        if field_value.startswith('[') and field_value.endswith(']'):
            try:
                return eval(field_value)  # Safe for our controlled data
            except:
                pass
        
        return [item.strip() for item in field_value.split(',') if item.strip()]
    
    def generate_enhanced_ingredient_knowledge(self) -> str:
        """Generate ingredient knowledge base from collected data"""
        
        ingredient_code = f'''
# Enhanced Ingredient Knowledge - Generated from collected data
# Generated on: {datetime.now().isoformat()}

COLLECTED_INGREDIENTS = {{'''
        
        for ingredient in self.collected_data['ingredients']:
            ingredient_id = ingredient.get('ingredient_id', ingredient.get('name', '').lower().replace(' ', '_'))
            ingredient_code += f'''
    '{ingredient_id}': {{
        'name': '{ingredient.get('name', '')}',
        'scientific_name': '{ingredient.get('scientific_name', '')}',
        'benefits': {self._parse_list_field(ingredient.get('benefits', ''))},
        'concerns_addressed': {self._parse_list_field(ingredient.get('concerns_addressed', ''))},
        'safety_rating': '{ingredient.get('safety_rating', 'SAFE')}',
        'concentration_range': '{ingredient.get('concentration_range', '')}',
        'skin_types': {self._parse_list_field(ingredient.get('skin_types', ''))},
        'contraindications': {self._parse_list_field(ingredient.get('contraindications', ''))}
    }},'''
        
        ingredient_code += '''
}

def get_ingredient_info(ingredient_name: str) -> Dict:
    """Get detailed information about an ingredient"""
    ingredient_key = ingredient_name.lower().replace(' ', '_')
    return COLLECTED_INGREDIENTS.get(ingredient_key, {})

def get_ingredients_for_concern(concern: str) -> List[Dict]:
    """Get ingredients that address a specific concern"""
    matching_ingredients = []
    
    for ingredient_id, ingredient_data in COLLECTED_INGREDIENTS.items():
        concerns = [c.lower() for c in ingredient_data['concerns_addressed']]
        if concern.lower() in concerns:
            matching_ingredients.append({
                'id': ingredient_id,
                **ingredient_data
            })
    
    return matching_ingredients
'''
        
        return ingredient_code
    
    def generate_enhanced_chatbot_responses(self) -> str:
        """Generate enhanced chatbot responses based on collected reviews"""
        
        # Analyze reviews for common themes and responses
        positive_reviews = [r for r in self.collected_data['reviews'] if int(r.get('rating', 0)) >= 4]
        negative_reviews = [r for r in self.collected_data['reviews'] if int(r.get('rating', 0)) <= 2]
        
        response_code = f'''
# Enhanced Chatbot Responses - Generated from collected data
# Generated on: {datetime.now().isoformat()}

def generate_enhanced_response(concern: str, products: List[Dict], ingredients: List[Dict]) -> str:
    """Generate enhanced response based on collected data"""
    
    response = f"**About {{concern.title()}}:**\\n"
    
    # Add educational content based on ingredients
    if ingredients:
        response += "\\nThis concern can be addressed with these key ingredients:\\n"
        for ingredient in ingredients[:3]:  # Top 3 ingredients
            benefits = ", ".join(ingredient.get('benefits', [])[:2])  # Top 2 benefits
            response += f"• **{{ingredient['name']}}**: {{benefits}}\\n"
    
    # Add product recommendations
    if products:
        response += "\\n**Recommended Products:**\\n"
        for product in products[:3]:  # Top 3 products
            rating_stars = "⭐" * int(float(product.get('rating', 0)))
            response += f"• **{{product['name']}}** by {{product['brand']}} {{rating_stars}}\\n"
            response += f"  Price: ${{product['price']}} | {{product['description'][:100]}}...\\n"
    
    # Add tips based on review analysis
    response += "\\n**Pro Tips:**\\n"'''
        
        # Add tips based on positive reviews
        if positive_reviews:
            response_code += '''
    response += "• Consistency is key - users report best results after 4-6 weeks\\n"
    response += "• Start with lower concentrations and gradually increase\\n"
    response += "• Always patch test new products first\\n"'''
        
        response_code += '''
    
    return response

# Review-based insights
POSITIVE_REVIEW_INSIGHTS = ['''
        
        for review in positive_reviews[:5]:  # Top 5 positive reviews
            pros = self._parse_list_field(review.get('pros', ''))
            if pros:
                response_code += f'''
    "{{pros[0] if pros else 'Effective results'}}",'''
        
        response_code += '''
]

COMMON_CONCERNS_FROM_REVIEWS = ['''
        
        all_review_concerns = set()
        for review in self.collected_data['reviews']:
            concerns = self._parse_list_field(review.get('concerns', ''))
            all_review_concerns.update(concerns)
        
        for concern in sorted(all_review_concerns)[:10]:  # Top 10 concerns
            if concern:
                response_code += f'''
    "{concern}",'''
        
        response_code += '''
]
'''
        
        return response_code
    
    def regenerate_chatbot_code(self) -> bool:
        """Regenerate the main chatbot code with enhanced features"""
        try:
            # Generate all enhanced components
            concern_detection = self.generate_enhanced_concern_detection()
            product_recommendations = self.generate_enhanced_product_recommendations()
            ingredient_knowledge = self.generate_enhanced_ingredient_knowledge()
            chatbot_responses = self.generate_enhanced_chatbot_responses()
            
            # Create enhanced chatbot file
            enhanced_chatbot_code = f'''#!/usr/bin/env python3
"""
Enhanced Beauty Chatbot - Auto-generated with collected data
Generated on: {datetime.now().isoformat()}
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import random
from typing import List, Dict, Optional

# Add DDD domain to path
sys.path.append(str(Path(__file__).parent / "ddd_domain"))

# Import DDD components
from beauty_chatbot_simple import SimplifiedBeautyChatbot

{concern_detection}

{product_recommendations}

{ingredient_knowledge}

{chatbot_responses}

class EnhancedBeautyChatbot(SimplifiedBeautyChatbot):
    """Enhanced Beauty Chatbot with collected data integration"""
    
    def __init__(self):
        super().__init__()
        self.enhanced_data_loaded = True
        print("✅ Enhanced chatbot loaded with collected data!")
    
    def process_message(self, message, user_profile=None):
        """Enhanced message processing with collected data"""
        if user_profile:
            self.user_profile = user_profile
        
        if not self.current_conversation_id:
            self.start_conversation()
        
        # Use enhanced concern detection
        detected_concerns = detect_concerns_enhanced(message)
        
        # Get enhanced recommendations
        products = get_product_recommendations(detected_concerns, 
                                            user_profile.get('skin_type') if user_profile else None)
        
        # Get ingredient information
        ingredients = []
        for concern in detected_concerns:
            ingredients.extend(get_ingredients_for_concern(concern))
        
        # Generate enhanced response
        if detected_concerns:
            enhanced_response = generate_enhanced_response(detected_concerns[0], products, ingredients)
            
            response = {{
                'response': enhanced_response,
                'concerns_detected': detected_concerns,
                'confidence_scores': {{concern: 0.9 for concern in detected_concerns}},
                'has_educational_content': True,
                'has_natural_remedies': len(ingredients) > 0,
                'natural_remedies': [],
                'products_recommended': [p['id'] for p in products],
                'prompt_type': 'concern'
            }}
        else:
            # Fall back to original processing
            response = super().process_message(message, user_profile)
        
        # Add to conversation history
        self.conversation_history.append({{
            'type': 'user',
            'message': message,
            'timestamp': datetime.now().isoformat()
        }})
        
        self.conversation_history.append({{
            'type': 'bot',
            'message': response['response'],
            'timestamp': datetime.now().isoformat(),
            'prompt_type': response['prompt_type'],
            'concerns_detected': response['concerns_detected']
        }})
        
        return response

def create_enhanced_chatbot():
    """Factory function to create enhanced chatbot instance"""
    return EnhancedBeautyChatbot()

if __name__ == "__main__":
    # Test the enhanced chatbot
    print("🧪 Testing Enhanced Beauty Chatbot")
    print("=" * 40)
    
    chatbot = create_enhanced_chatbot()
    
    # Test with collected data
    test_messages = [
        "Hi there!",
        "I have acne problems on my face",
        "My skin is very dry and flaky", 
        "Can you recommend some good skincare products?",
        "What's the best moisturizer for oily skin?"
    ]
    
    for message in test_messages:
        print(f"\\nUser: {{message}}")
        response = chatbot.process_message(message)
        print(f"Bot ({{response['prompt_type']}}): {{response['response'][:100]}}...")
        if response['concerns_detected']:
            print(f"Enhanced Concerns: {{response['concerns_detected']}}")
        if response['products_recommended']:
            print(f"Products: {{len(response['products_recommended'])}} recommended")
    
    print(f"\\nConversation History: {{len(chatbot.get_conversation_history())}} messages")
    print(f"Analytics: {{chatbot.get_analytics()}}")
    
    print("\\n✅ Enhanced chatbot test completed!")
'''
            
            # Save enhanced chatbot
            enhanced_file = os.path.join("beauty_chatbot_ddd_package/core", "beauty_chatbot_enhanced.py")
            with open(enhanced_file, 'w', encoding='utf-8') as f:
                f.write(enhanced_chatbot_code)
            
            print(f"✅ Enhanced chatbot code generated: {enhanced_file}")
            return True
            
        except Exception as e:
            print(f"❌ Error regenerating code: {str(e)}")
            return False


def main():
    """Main function to regenerate chatbot code"""
    print("🔄 Beauty Chatbot Code Regeneration System")
    print("=" * 50)
    
    regenerator = BeautyChatbotCodeRegenerator("beauty_chatbot_ddd_package/data")
    
    # Check if collected data exists
    total_items = (len(regenerator.collected_data['products']) + 
                  len(regenerator.collected_data['ingredients']) + 
                  len(regenerator.collected_data['reviews']))
    
    if total_items == 0:
        print("⚠️ No collected data found. Please run the data collector first.")
        return False
    
    print(f"📊 Found collected data:")
    print(f"  - Products: {len(regenerator.collected_data['products'])}")
    print(f"  - Ingredients: {len(regenerator.collected_data['ingredients'])}")
    print(f"  - Reviews: {len(regenerator.collected_data['reviews'])}")
    
    # Regenerate code
    success = regenerator.regenerate_chatbot_code()
    
    if success:
        print("\n🎉 Code regeneration completed successfully!")
        print("📁 Enhanced chatbot available at: beauty_chatbot_ddd_package/core/beauty_chatbot_enhanced.py")
        return True
    else:
        print("\n❌ Code regeneration failed.")
        return False


if __name__ == "__main__":
    main()
