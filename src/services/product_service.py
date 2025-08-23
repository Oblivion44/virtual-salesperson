import pandas as pd
import json
import os
import re
from textblob import TextBlob
import random

class ProductService:
    def __init__(self):
        self.products = []
        self.reviews = []
        self.nykaa_base_url = os.getenv('NYKAA_API_BASE_URL', 'https://www.nykaa.com')
        self.affiliate_id = os.getenv('NYKAA_AFFILIATE_ID')
        
        # Initialize product data
        self.load_product_data()

    def load_product_data(self):
        """Load product data from CSV or use sample data"""
        try:
            # In a real implementation, you would load from CSV files
            # For now, we'll use sample data
            self.products = self.get_sample_products()
            self.reviews = self.get_sample_reviews()
            
            print(f"Loaded {len(self.products)} products and {len(self.reviews)} reviews")
        except Exception as e:
            print(f"Error loading product data: {e}")
            self.products = self.get_sample_products()

    def search_products(self, query, filters=None):
        """Search products based on query and filters"""
        if filters is None:
            filters = {}
        
        try:
            filtered_products = self.products.copy()

            # Text search
            if query:
                search_terms = query.lower().split()
                filtered_products = [
                    product for product in filtered_products
                    if any(
                        term in f"{product['name']} {product['brand']} {product['category']} {product['description']}".lower()
                        for term in search_terms
                    )
                ]

            # Apply filters
            if filters.get('category'):
                filtered_products = [
                    p for p in filtered_products 
                    if p['category'].lower() == filters['category'].lower()
                ]

            if filters.get('skinType'):
                filtered_products = [
                    p for p in filtered_products 
                    if p.get('suitableFor') and filters['skinType'] in p['suitableFor']
                ]

            if filters.get('concerns'):
                filtered_products = [
                    p for p in filtered_products 
                    if p.get('concerns') and any(
                        concern in p['concerns'] for concern in filters['concerns']
                    )
                ]

            if filters.get('priceRange'):
                min_price, max_price = filters['priceRange']
                filtered_products = [
                    p for p in filtered_products 
                    if min_price <= p['price'] <= max_price
                ]

            if filters.get('ageGroup'):
                filtered_products = [
                    p for p in filtered_products 
                    if p.get('ageGroups') and filters['ageGroup'] in p['ageGroups']
                ]

            # Sort by relevance and rating
            filtered_products.sort(key=lambda x: (x['rating'], x['reviewCount']), reverse=True)

            # Limit results
            return filtered_products[:20]
        except Exception as e:
            print(f"Error searching products: {e}")
            return []

    def get_product_details(self, product_ids):
        """Get detailed product information"""
        try:
            products = []
            for product_id in product_ids:
                product = next((p for p in self.products if p['id'] == product_id or p['name'] == product_id), None)
                if product:
                    enhanced_product = product.copy()
                    enhanced_product['nykaaUrl'] = self.generate_nykaa_url(product)
                    enhanced_product['reviews'] = self.get_product_reviews(product['id'])
                    enhanced_product['sentiment'] = self.analyze_product_sentiment(product['id'])
                    products.append(enhanced_product)
            
            return products
        except Exception as e:
            print(f"Error getting product details: {e}")
            return []

    def get_product_reviews(self, product_id, limit=5):
        """Get positive reviews for a product"""
        try:
            product_reviews = [r for r in self.reviews if r['productId'] == product_id]
            
            # Filter for positive sentiment reviews
            positive_reviews = []
            for review in product_reviews:
                sentiment = TextBlob(review['text']).sentiment.polarity
                if sentiment > 0:
                    positive_reviews.append(review)
            
            return positive_reviews[:limit]
        except Exception as e:
            print(f"Error getting reviews: {e}")
            return []

    def analyze_product_sentiment(self, product_id):
        """Analyze sentiment of product reviews"""
        try:
            product_reviews = [r for r in self.reviews if r['productId'] == product_id]
            
            if not product_reviews:
                return {'score': 0, 'positive': 0, 'negative': 0, 'neutral': 0}

            total_score = 0
            positive = 0
            negative = 0
            neutral = 0

            for review in product_reviews:
                sentiment = TextBlob(review['text']).sentiment.polarity
                total_score += sentiment
                
                if sentiment > 0.1:
                    positive += 1
                elif sentiment < -0.1:
                    negative += 1
                else:
                    neutral += 1

            total_reviews = len(product_reviews)
            return {
                'score': total_score / total_reviews,
                'positive': (positive / total_reviews) * 100,
                'negative': (negative / total_reviews) * 100,
                'neutral': (neutral / total_reviews) * 100
            }
        except Exception as e:
            print(f"Error analyzing sentiment: {e}")
            return {'score': 0, 'positive': 0, 'negative': 0, 'neutral': 0}

    def generate_nykaa_url(self, product):
        """Generate Nykaa URL with affiliate tracking"""
        slug = product.get('slug') or product['name'].lower().replace(' ', '-').replace('\'', '')
        base_url = f"{self.nykaa_base_url}/product/{slug}"
        
        if self.affiliate_id:
            return f"{base_url}?affiliate={self.affiliate_id}"
        
        return base_url

    def get_recommendations(self, user_profile, limit=5):
        """Get product recommendations based on user profile"""
        try:
            filters = {
                'category': user_profile.get('category'),
                'skinType': user_profile.get('skinType'),
                'concerns': user_profile.get('concerns'),
                'ageGroup': user_profile.get('ageGroup')
            }

            # If budget is specified, add price filter
            if user_profile.get('budget'):
                budget_range = self.parse_budget(user_profile['budget'])
                if budget_range:
                    filters['priceRange'] = budget_range

            recommendations = self.search_products('', filters)
            return recommendations[:limit]
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return self.get_sample_products()[:limit]

    def parse_budget(self, budget_string):
        """Parse budget strings like 'under 1000', '500-1500', 'around 800'"""
        try:
            budget_lower = budget_string.lower()
            
            if 'under' in budget_lower:
                match = re.search(r'under\s+(\d+)', budget_lower)
                if match:
                    return [0, int(match.group(1))]
            
            if 'around' in budget_lower or 'about' in budget_lower:
                match = re.search(r'(?:around|about)\s+(\d+)', budget_lower)
                if match:
                    amount = int(match.group(1))
                    return [int(amount * 0.7), int(amount * 1.3)]  # ±30%
            
            # Range format: "500-1500"
            range_match = re.search(r'(\d+)\s*-\s*(\d+)', budget_lower)
            if range_match:
                return [int(range_match.group(1)), int(range_match.group(2))]
            
            return None
        except Exception as e:
            print(f"Error parsing budget: {e}")
            return None

    def get_sample_products(self):
        """Get sample product data"""
        return [
            {
                'id': 'p1',
                'name': 'Cetaphil Gentle Skin Cleanser',
                'brand': 'Cetaphil',
                'category': 'skincare',
                'subcategory': 'cleanser',
                'price': 599,
                'rating': 4.5,
                'reviewCount': 1250,
                'image': '/images/cetaphil-cleanser.jpg',
                'description': 'Gentle, non-irritating cleanser for all skin types',
                'suitableFor': ['sensitive', 'dry', 'normal', 'combination'],
                'concerns': ['sensitivity', 'dryness'],
                'ageGroups': ['teens', 'young_adults', 'adults', 'mature'],
                'slug': 'cetaphil-gentle-skin-cleanser'
            },
            {
                'id': 'p2',
                'name': 'The Ordinary Hyaluronic Acid 2% + B5',
                'brand': 'The Ordinary',
                'category': 'skincare',
                'subcategory': 'serum',
                'price': 849,
                'rating': 4.7,
                'reviewCount': 2100,
                'image': '/images/ordinary-hyaluronic.jpg',
                'description': 'Intense hydration serum with hyaluronic acid',
                'suitableFor': ['dry', 'normal', 'combination', 'oily'],
                'concerns': ['dryness', 'dehydration', 'fine_lines'],
                'ageGroups': ['young_adults', 'adults', 'mature'],
                'slug': 'the-ordinary-hyaluronic-acid-2-b5'
            },
            {
                'id': 'p3',
                'name': 'Maybelline Fit Me Foundation',
                'brand': 'Maybelline',
                'category': 'makeup',
                'subcategory': 'foundation',
                'price': 499,
                'rating': 4.3,
                'reviewCount': 890,
                'image': '/images/maybelline-fitme.jpg',
                'description': 'Natural coverage foundation for all skin tones',
                'suitableFor': ['normal', 'combination', 'oily'],
                'concerns': ['uneven_tone', 'coverage'],
                'ageGroups': ['teens', 'young_adults', 'adults'],
                'slug': 'maybelline-fit-me-foundation'
            },
            {
                'id': 'p4',
                'name': 'L\'Oréal Paris Total Repair 5 Shampoo',
                'brand': 'L\'Oréal Paris',
                'category': 'haircare',
                'subcategory': 'shampoo',
                'price': 399,
                'rating': 4.4,
                'reviewCount': 756,
                'image': '/images/loreal-shampoo.jpg',
                'description': 'Repairing shampoo for damaged hair',
                'suitableFor': ['damaged', 'dry', 'normal'],
                'concerns': ['damage', 'dryness', 'breakage'],
                'ageGroups': ['teens', 'young_adults', 'adults', 'mature'],
                'slug': 'loreal-paris-total-repair-5-shampoo'
            },
            {
                'id': 'p5',
                'name': 'Neutrogena Ultra Sheer Sunscreen SPF 50+',
                'brand': 'Neutrogena',
                'category': 'skincare',
                'subcategory': 'sunscreen',
                'price': 699,
                'rating': 4.6,
                'reviewCount': 1450,
                'image': '/images/neutrogena-sunscreen.jpg',
                'description': 'Broad spectrum sun protection with lightweight formula',
                'suitableFor': ['all', 'sensitive', 'oily', 'combination'],
                'concerns': ['sun_protection', 'aging_prevention'],
                'ageGroups': ['teens', 'young_adults', 'adults', 'mature'],
                'slug': 'neutrogena-ultra-sheer-sunscreen-spf-50'
            },
            {
                'id': 'p6',
                'name': 'Lakme Absolute Lip Color',
                'brand': 'Lakme',
                'category': 'makeup',
                'subcategory': 'lipstick',
                'price': 650,
                'rating': 4.1,
                'reviewCount': 654,
                'image': '/images/lakme-lipstick.jpg',
                'description': 'Long-lasting lip color with rich pigmentation',
                'suitableFor': ['all'],
                'concerns': ['color', 'longevity'],
                'ageGroups': ['teens', 'young_adults', 'adults'],
                'slug': 'lakme-absolute-lip-color'
            }
        ]

    def get_sample_reviews(self):
        """Get sample review data"""
        return [
            {
                'id': 'r1',
                'productId': 'p1',
                'rating': 5,
                'text': 'Amazing cleanser! So gentle on my sensitive skin and removes makeup perfectly.',
                'helpful': 45,
                'verified': True
            },
            {
                'id': 'r2',
                'productId': 'p1',
                'rating': 4,
                'text': 'Good for daily use, doesn\'t dry out my skin like other cleansers.',
                'helpful': 32,
                'verified': True
            },
            {
                'id': 'r3',
                'productId': 'p2',
                'rating': 5,
                'text': 'This serum is a game changer! My skin feels so plump and hydrated.',
                'helpful': 67,
                'verified': True
            },
            {
                'id': 'r4',
                'productId': 'p3',
                'rating': 4,
                'text': 'Great coverage and matches my skin tone perfectly. Lasts all day.',
                'helpful': 28,
                'verified': True
            },
            {
                'id': 'r5',
                'productId': 'p4',
                'rating': 4,
                'text': 'Really helps with my damaged hair. Noticed less breakage after a month.',
                'helpful': 41,
                'verified': True
            },
            {
                'id': 'r6',
                'productId': 'p5',
                'rating': 5,
                'text': 'Best sunscreen I\'ve used! Doesn\'t leave white cast and feels lightweight.',
                'helpful': 89,
                'verified': True
            }
        ]
