# Core Beauty Chatbot Logic
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import defaultdict
import pandas as pd

class BeautyChatbot:
    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.user_profile = {}
        self.conversation_history = []
        self.cart = []
        self.stop_words = set(stopwords.words('english'))
        
        # Initialize concern keywords mapping
        self.concern_keywords = self._build_concern_keywords()
        
        # Natural remedies database
        self.natural_remedies = self._load_natural_remedies()
        
    def _build_concern_keywords(self):
        """Build keyword mapping for concern detection"""
        concern_keywords = {
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
        return concern_keywords
    
    def _load_natural_remedies(self):
        """Load natural remedies database"""
        remedies = {
            'acne': [
                {
                    'name': 'Honey & Cinnamon Mask',
                    'ingredients': ['2 tbsp raw honey', '1 tsp cinnamon powder'],
                    'instructions': 'Mix honey and cinnamon. Apply to clean face for 15 minutes. Rinse with warm water.',
                    'benefits': 'Honey has antibacterial properties, cinnamon reduces inflammation'
                },
                {
                    'name': 'Tea Tree Oil Spot Treatment',
                    'ingredients': ['2-3 drops tea tree oil', '1 tbsp carrier oil (coconut/jojoba)'],
                    'instructions': 'Dilute tea tree oil with carrier oil. Apply to spots with cotton swab.',
                    'benefits': 'Natural antiseptic that fights acne-causing bacteria'
                }
            ],
            'dryness': [
                {
                    'name': 'Oatmeal Honey Mask',
                    'ingredients': ['1/2 cup oats', '2 tbsp honey', '2 tbsp milk'],
                    'instructions': 'Blend oats, mix with honey and milk. Apply for 20 minutes, rinse gently.',
                    'benefits': 'Oats exfoliate gently, honey moisturizes, milk soothes'
                },
                {
                    'name': 'Avocado Face Mask',
                    'ingredients': ['1 ripe avocado', '1 tbsp olive oil', '1 tbsp honey'],
                    'instructions': 'Mash avocado, mix with oil and honey. Apply for 15-20 minutes.',
                    'benefits': 'Rich in healthy fats and vitamins for deep moisturizing'
                }
            ],
            'oily': [
                {
                    'name': 'Clay & Apple Cider Vinegar Mask',
                    'ingredients': ['2 tbsp bentonite clay', '1 tbsp apple cider vinegar', 'water as needed'],
                    'instructions': 'Mix clay with vinegar and water to paste consistency. Apply for 10-15 minutes.',
                    'benefits': 'Clay absorbs excess oil, vinegar balances pH'
                }
            ],
            'dark_spots': [
                {
                    'name': 'Lemon & Honey Treatment',
                    'ingredients': ['1 tbsp fresh lemon juice', '2 tbsp honey'],
                    'instructions': 'Mix and apply to dark spots. Leave for 20 minutes, rinse well.',
                    'benefits': 'Lemon has natural bleaching properties, honey moisturizes'
                }
            ],
            'dandruff': [
                {
                    'name': 'Apple Cider Vinegar Rinse',
                    'ingredients': ['1/4 cup apple cider vinegar', '1/4 cup water'],
                    'instructions': 'Mix and apply to scalp after shampooing. Leave 5 minutes, rinse.',
                    'benefits': 'Balances scalp pH and reduces fungal growth'
                }
            ]
        }
        return remedies
    
    def detect_prompt_type(self, user_input):
        """Detect the type of user prompt"""
        user_input_lower = user_input.lower()
        
        # Check for concern-based keywords
        for concern, keywords in self.concern_keywords.items():
            if any(keyword in user_input_lower for keyword in keywords):
                return 'concern', concern
        
        # Check for ambition/exploration keywords
        exploration_keywords = [
            'recommend', 'suggest', 'looking for', 'want to try', 'new product',
            'skincare routine', 'makeup', 'hair care', 'beauty', 'cosmetics'
        ]
        
        if any(keyword in user_input_lower for keyword in exploration_keywords):
            return 'exploration', None
        
        # Default to chit-chat
        return 'chitchat', None
    
    def handle_concern_based(self, concern, user_input):
        """Handle concern-based conversations"""
        response = {
            'type': 'concern',
            'concern': concern,
            'explanation': self._get_concern_explanation(concern),
            'products': self._get_products_for_concern(concern),
            'remedies': self.natural_remedies.get(concern, [])
        }
        return response
    
    def handle_exploration_based(self, user_input):
        """Handle exploration/ambition-based conversations"""
        # Extract product categories from input
        categories = self._extract_categories(user_input)
        
        response = {
            'type': 'exploration',
            'categories': categories,
            'products': self._get_top_products(categories, limit=4),
            'message': 'Here are some great products you might love!'
        }
        return response
    
    def handle_chitchat(self, user_input):
        """Handle general conversation"""
        chitchat_responses = [
            "That's interesting! Is there anything specific about beauty or skincare I can help you with?",
            "I'd love to help you with your beauty routine! What are you looking for today?",
            "Thanks for sharing! Do you have any skin, hair, or makeup concerns I can assist with?",
            "I'm here to help with all your beauty needs! What would you like to explore?"
        ]
        
        response = {
            'type': 'chitchat',
            'message': random.choice(chitchat_responses)
        }
        return response
    
    def _get_concern_explanation(self, concern):
        """Get explanation for a specific concern"""
        explanations = {
            'acne': 'Acne occurs when pores become clogged with oil and dead skin cells. Look for products with salicylic acid, benzoyl peroxide, or niacinamide.',
            'dryness': 'Dry skin lacks moisture and natural oils. Hyaluronic acid, ceramides, and glycerin are excellent hydrating ingredients.',
            'oily': 'Oily skin produces excess sebum. Niacinamide, salicylic acid, and clay-based products can help control oil production.',
            'aging': 'Signs of aging include fine lines and loss of elasticity. Retinol, vitamin C, and peptides are proven anti-aging ingredients.',
            'dark_spots': 'Hyperpigmentation can be treated with vitamin C, kojic acid, arbutin, and chemical exfoliants like glycolic acid.',
            'sensitive': 'Sensitive skin needs gentle, fragrance-free products. Look for soothing ingredients like aloe vera, chamomile, and niacinamide.'
        }
        return explanations.get(concern, 'Let me help you find the right products for your concern.')
    
    def _get_products_for_concern(self, concern):
        """Get products mapped to specific concern"""
        if not self.data_loader.data_loaded:
            return []
        
        # This would use your actual CSV data
        # For now, returning sample structure
        sample_products = [
            {
                'product_id': 'P001',
                'name': f'Solution for {concern.title()}',
                'price': 29.99,
                'rating': 4.5,
                'image_url': 'https://via.placeholder.com/200x200',
                'review': 'Amazing product! Really helped with my concerns.'
            }
        ]
        return sample_products
    
    def _extract_categories(self, user_input):
        """Extract product categories from user input"""
        categories = []
        category_keywords = {
            'skincare': ['skin', 'face', 'moisturizer', 'cleanser', 'serum'],
            'haircare': ['hair', 'shampoo', 'conditioner', 'scalp'],
            'makeup': ['makeup', 'foundation', 'lipstick', 'eyeshadow', 'mascara']
        }
        
        user_input_lower = user_input.lower()
        for category, keywords in category_keywords.items():
            if any(keyword in user_input_lower for keyword in keywords):
                categories.append(category)
        
        return categories if categories else ['skincare']  # Default to skincare
    
    def _get_top_products(self, categories, limit=4):
        """Get top products for given categories"""
        # This would use your actual CSV data
        # For now, returning sample structure
        sample_products = []
        for i in range(limit):
            sample_products.append({
                'product_id': f'P00{i+1}',
                'name': f'Top Product {i+1}',
                'category': categories[0] if categories else 'skincare',
                'price': 25.99 + (i * 5),
                'rating': 4.2 + (i * 0.1),
                'image_url': 'https://via.placeholder.com/200x200',
                'review': f'Excellent product! Highly recommended for {categories[0] if categories else "skincare"}.'
            })
        return sample_products
    
    def add_to_cart(self, product):
        """Add product to cart"""
        self.cart.append({
            'product_id': product['product_id'],
            'name': product['name'],
            'price': product['price'],
            'quantity': 1,
            'added_at': datetime.now()
        })
        return f"✅ {product['name']} added to cart!"
    
    def get_cart_total(self):
        """Calculate cart total"""
        return sum(item['price'] * item['quantity'] for item in self.cart)
    
    def process_message(self, user_input):
        """Main message processing function"""
        # Store conversation
        self.conversation_history.append({
            'user': user_input,
            'timestamp': datetime.now()
        })
        
        # Detect prompt type
        prompt_type, concern = self.detect_prompt_type(user_input)
        
        # Generate response based on type
        if prompt_type == 'concern':
            response = self.handle_concern_based(concern, user_input)
        elif prompt_type == 'exploration':
            response = self.handle_exploration_based(user_input)
        else:
            response = self.handle_chitchat(user_input)
        
        # Store bot response
        self.conversation_history.append({
            'bot': response,
            'timestamp': datetime.now()
        })
        
        return response
