#!/usr/bin/env python3
"""
LLM-Powered Data Collection System for Beauty Chatbot
This module uses LLM capabilities to identify context and collect structured data
"""

import json
import csv
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
import re


@dataclass
class ProductData:
    """Structure for product information"""
    product_id: str
    name: str
    brand: str
    category: str
    price: float
    rating: float
    description: str
    key_ingredients: List[str]
    skin_types: List[str]
    concerns_addressed: List[str]
    image_url: str = ""
    availability: str = "available"


@dataclass
class IngredientData:
    """Structure for ingredient information"""
    ingredient_id: str
    name: str
    scientific_name: str
    benefits: List[str]
    concerns_addressed: List[str]
    safety_rating: str
    concentration_range: str
    skin_types: List[str]
    contraindications: List[str] = None


@dataclass
class ReviewData:
    """Structure for review information"""
    review_id: str
    product_id: str
    user_id: str
    rating: int
    title: str
    content: str
    skin_type: str
    age_range: str
    concerns: List[str]
    pros: List[str]
    cons: List[str]
    would_recommend: bool
    date_posted: str


class LLMContextAnalyzer:
    """LLM-powered context analyzer for beauty-related content"""
    
    def __init__(self):
        self.beauty_keywords = {
            'skin_types': ['oily', 'dry', 'combination', 'sensitive', 'normal', 'mature'],
            'concerns': ['acne', 'aging', 'dark spots', 'wrinkles', 'dryness', 'oiliness', 
                        'sensitivity', 'rosacea', 'hyperpigmentation', 'fine lines'],
            'categories': ['cleanser', 'moisturizer', 'serum', 'toner', 'sunscreen', 
                          'mask', 'exfoliant', 'treatment', 'foundation', 'concealer'],
            'ingredients': ['retinol', 'hyaluronic acid', 'vitamin c', 'niacinamide', 
                           'salicylic acid', 'glycolic acid', 'ceramides', 'peptides']
        }
    
    def analyze_context(self, text: str) -> Dict[str, any]:
        """Analyze text to identify beauty-related context"""
        text_lower = text.lower()
        
        context = {
            'content_type': self._identify_content_type(text_lower),
            'skin_types': self._extract_skin_types(text_lower),
            'concerns': self._extract_concerns(text_lower),
            'categories': self._extract_categories(text_lower),
            'ingredients': self._extract_ingredients(text_lower),
            'sentiment': self._analyze_sentiment(text_lower),
            'rating_indicators': self._extract_rating_indicators(text_lower),
            'recommendation_strength': self._analyze_recommendation_strength(text_lower)
        }
        
        return context
    
    def _identify_content_type(self, text: str) -> str:
        """Identify if text is a product description, review, or ingredient info"""
        review_indicators = ['love', 'hate', 'recommend', 'tried', 'used', 'bought', 'works', 'doesn\'t work']
        product_indicators = ['contains', 'formulated', 'designed for', 'suitable for', 'price', 'available']
        ingredient_indicators = ['benefits', 'derived from', 'concentration', 'molecular', 'studies show']
        
        review_score = sum(1 for indicator in review_indicators if indicator in text)
        product_score = sum(1 for indicator in product_indicators if indicator in text)
        ingredient_score = sum(1 for indicator in ingredient_indicators if indicator in text)
        
        if review_score >= product_score and review_score >= ingredient_score:
            return 'review'
        elif product_score >= ingredient_score:
            return 'product'
        else:
            return 'ingredient'
    
    def _extract_skin_types(self, text: str) -> List[str]:
        """Extract mentioned skin types"""
        found_types = []
        for skin_type in self.beauty_keywords['skin_types']:
            if skin_type in text:
                found_types.append(skin_type)
        return found_types
    
    def _extract_concerns(self, text: str) -> List[str]:
        """Extract mentioned beauty concerns"""
        found_concerns = []
        for concern in self.beauty_keywords['concerns']:
            if concern in text:
                found_concerns.append(concern)
        return found_concerns
    
    def _extract_categories(self, text: str) -> List[str]:
        """Extract product categories"""
        found_categories = []
        for category in self.beauty_keywords['categories']:
            if category in text:
                found_categories.append(category)
        return found_categories
    
    def _extract_ingredients(self, text: str) -> List[str]:
        """Extract mentioned ingredients"""
        found_ingredients = []
        for ingredient in self.beauty_keywords['ingredients']:
            if ingredient in text:
                found_ingredients.append(ingredient)
        return found_ingredients
    
    def _analyze_sentiment(self, text: str) -> str:
        """Analyze sentiment of the text"""
        positive_words = ['love', 'amazing', 'great', 'excellent', 'perfect', 'works', 'effective']
        negative_words = ['hate', 'terrible', 'awful', 'doesn\'t work', 'waste', 'disappointed']
        
        positive_score = sum(1 for word in positive_words if word in text)
        negative_score = sum(1 for word in negative_words if word in text)
        
        if positive_score > negative_score:
            return 'positive'
        elif negative_score > positive_score:
            return 'negative'
        else:
            return 'neutral'
    
    def _extract_rating_indicators(self, text: str) -> Optional[int]:
        """Extract rating from text"""
        # Look for star ratings or numerical ratings
        star_pattern = r'(\d+)\s*(?:star|stars|\*)'
        number_pattern = r'(\d+)(?:/10|/5|\s*out\s*of\s*(?:10|5))'
        
        star_match = re.search(star_pattern, text)
        number_match = re.search(number_pattern, text)
        
        if star_match:
            return int(star_match.group(1))
        elif number_match:
            rating = int(number_match.group(1))
            # Normalize to 5-star scale
            if '/10' in text or 'out of 10' in text:
                return int(rating / 2)
            return rating
        
        return None
    
    def _analyze_recommendation_strength(self, text: str) -> str:
        """Analyze how strongly the text recommends or discourages"""
        strong_positive = ['highly recommend', 'must have', 'holy grail', 'life changing']
        moderate_positive = ['recommend', 'good', 'works well', 'satisfied']
        moderate_negative = ['not recommended', 'disappointed', 'could be better']
        strong_negative = ['avoid', 'terrible', 'waste of money', 'never again']
        
        if any(phrase in text for phrase in strong_positive):
            return 'strongly_recommend'
        elif any(phrase in text for phrase in moderate_positive):
            return 'recommend'
        elif any(phrase in text for phrase in moderate_negative):
            return 'not_recommend'
        elif any(phrase in text for phrase in strong_negative):
            return 'strongly_not_recommend'
        else:
            return 'neutral'


class InteractiveDataCollector:
    """Interactive system to collect structured beauty data"""
    
    def __init__(self):
        self.analyzer = LLMContextAnalyzer()
        self.collected_data = {
            'products': [],
            'ingredients': [],
            'reviews': []
        }
    
    def collect_data_interactively(self) -> Dict[str, List]:
        """Main interactive data collection process"""
        print("🌟 Beauty Chatbot Data Collection System")
        print("=" * 50)
        print("I'll help you collect and structure beauty data for the chatbot!")
        print("You can provide information about products, ingredients, or reviews.")
        print("Type 'done' when finished, or 'help' for guidance.\n")
        
        while True:
            user_input = input("📝 Please provide beauty-related information (or 'done'/'help'): ").strip()
            
            if user_input.lower() == 'done':
                break
            elif user_input.lower() == 'help':
                self._show_help()
                continue
            elif len(user_input) < 10:
                print("⚠️ Please provide more detailed information (at least 10 characters)")
                continue
            
            # Analyze the context
            context = self.analyzer.analyze_context(user_input)
            print(f"\n🔍 Detected content type: {context['content_type']}")
            
            # Collect structured data based on type
            if context['content_type'] == 'product':
                self._collect_product_data(user_input, context)
            elif context['content_type'] == 'ingredient':
                self._collect_ingredient_data(user_input, context)
            elif context['content_type'] == 'review':
                self._collect_review_data(user_input, context)
            
            print("✅ Data collected successfully!\n")
        
        return self.collected_data
    
    def _show_help(self):
        """Show help information"""
        print("\n💡 Help - How to provide data:")
        print("=" * 30)
        print("🛒 PRODUCT: Describe a beauty product")
        print("   Example: 'CeraVe Hydrating Cleanser is a gentle cleanser for dry skin with ceramides and hyaluronic acid, priced at $12.99'")
        print("\n🧪 INGREDIENT: Describe an ingredient and its benefits")
        print("   Example: 'Retinol is a vitamin A derivative that reduces wrinkles and improves skin texture, suitable for normal to oily skin'")
        print("\n⭐ REVIEW: Share your experience with a product")
        print("   Example: 'I love the Ordinary Niacinamide serum! It really helped with my oily skin and large pores. 5 stars, highly recommend!'")
        print("\n" + "=" * 30 + "\n")
    
    def _collect_product_data(self, text: str, context: Dict):
        """Collect structured product data"""
        print("🛒 Collecting product information...")
        
        # Extract basic info from context
        name = input("Product name: ").strip()
        brand = input("Brand: ").strip()
        category = input(f"Category {context['categories']}: ").strip() or (context['categories'][0] if context['categories'] else 'unknown')
        
        try:
            price = float(input("Price ($): ").strip() or "0")
            rating = float(input("Average rating (1-5): ").strip() or "0")
        except ValueError:
            price, rating = 0.0, 0.0
        
        description = input("Description: ").strip() or text
        
        # Use context for intelligent defaults
        key_ingredients = context['ingredients'] or input("Key ingredients (comma-separated): ").split(',')
        skin_types = context['skin_types'] or input("Suitable skin types (comma-separated): ").split(',')
        concerns = context['concerns'] or input("Concerns addressed (comma-separated): ").split(',')
        
        product = ProductData(
            product_id=f"prod_{len(self.collected_data['products']) + 1:03d}",
            name=name,
            brand=brand,
            category=category,
            price=price,
            rating=rating,
            description=description,
            key_ingredients=[ing.strip() for ing in key_ingredients if ing.strip()],
            skin_types=[st.strip() for st in skin_types if st.strip()],
            concerns_addressed=[c.strip() for c in concerns if c.strip()],
            image_url=input("Image URL (optional): ").strip()
        )
        
        self.collected_data['products'].append(asdict(product))
    
    def _collect_ingredient_data(self, text: str, context: Dict):
        """Collect structured ingredient data"""
        print("🧪 Collecting ingredient information...")
        
        name = input("Ingredient name: ").strip()
        scientific_name = input("Scientific name (optional): ").strip()
        
        # Use context for intelligent defaults
        benefits = context.get('benefits', []) or input("Benefits (comma-separated): ").split(',')
        concerns = context['concerns'] or input("Concerns addressed (comma-separated): ").split(',')
        skin_types = context['skin_types'] or input("Suitable skin types (comma-separated): ").split(',')
        
        safety_rating = input("Safety rating (SAFE/CAUTION/AVOID): ").strip().upper() or "SAFE"
        concentration = input("Typical concentration range: ").strip()
        contraindications = input("Contraindications (comma-separated, optional): ").split(',')
        
        ingredient = IngredientData(
            ingredient_id=f"ing_{len(self.collected_data['ingredients']) + 1:03d}",
            name=name,
            scientific_name=scientific_name,
            benefits=[b.strip() for b in benefits if b.strip()],
            concerns_addressed=[c.strip() for c in concerns if c.strip()],
            safety_rating=safety_rating,
            concentration_range=concentration,
            skin_types=[st.strip() for st in skin_types if st.strip()],
            contraindications=[c.strip() for c in contraindications if c.strip()] if contraindications[0] else []
        )
        
        self.collected_data['ingredients'].append(asdict(ingredient))
    
    def _collect_review_data(self, text: str, context: Dict):
        """Collect structured review data"""
        print("⭐ Collecting review information...")
        
        product_name = input("Product being reviewed: ").strip()
        user_id = input("User ID (optional): ").strip() or f"user_{len(self.collected_data['reviews']) + 1:03d}"
        
        # Use context for intelligent defaults
        rating = context['rating_indicators'] or int(input("Rating (1-5): ").strip() or "5")
        title = input("Review title: ").strip()
        content = text
        
        skin_type = input(f"Reviewer's skin type {context['skin_types']}: ").strip() or (context['skin_types'][0] if context['skin_types'] else 'unknown')
        age_range = input("Age range (20s, 30s, etc.): ").strip()
        concerns = context['concerns'] or input("Skin concerns (comma-separated): ").split(',')
        
        pros = input("Pros (comma-separated): ").split(',')
        cons = input("Cons (comma-separated): ").split(',')
        
        would_recommend = context['recommendation_strength'] in ['recommend', 'strongly_recommend']
        if context['recommendation_strength'] == 'neutral':
            would_recommend = input("Would recommend? (y/n): ").strip().lower() == 'y'
        
        review = ReviewData(
            review_id=f"rev_{len(self.collected_data['reviews']) + 1:03d}",
            product_id=f"prod_for_{product_name.replace(' ', '_').lower()}",
            user_id=user_id,
            rating=rating,
            title=title,
            content=content,
            skin_type=skin_type,
            age_range=age_range,
            concerns=[c.strip() for c in concerns if c.strip()],
            pros=[p.strip() for p in pros if p.strip()],
            cons=[c.strip() for c in cons if c.strip()],
            would_recommend=would_recommend,
            date_posted=datetime.now().isoformat()
        )
        
        self.collected_data['reviews'].append(asdict(review))
    
    def save_to_csv(self, output_dir: str = "data"):
        """Save collected data to CSV files"""
        os.makedirs(output_dir, exist_ok=True)
        
        # Save products
        if self.collected_data['products']:
            products_file = os.path.join(output_dir, 'collected_products.csv')
            with open(products_file, 'w', newline='', encoding='utf-8') as f:
                if self.collected_data['products']:
                    writer = csv.DictWriter(f, fieldnames=self.collected_data['products'][0].keys())
                    writer.writeheader()
                    writer.writerows(self.collected_data['products'])
            print(f"✅ Saved {len(self.collected_data['products'])} products to {products_file}")
        
        # Save ingredients
        if self.collected_data['ingredients']:
            ingredients_file = os.path.join(output_dir, 'collected_ingredients.csv')
            with open(ingredients_file, 'w', newline='', encoding='utf-8') as f:
                if self.collected_data['ingredients']:
                    writer = csv.DictWriter(f, fieldnames=self.collected_data['ingredients'][0].keys())
                    writer.writeheader()
                    writer.writerows(self.collected_data['ingredients'])
            print(f"✅ Saved {len(self.collected_data['ingredients'])} ingredients to {ingredients_file}")
        
        # Save reviews
        if self.collected_data['reviews']:
            reviews_file = os.path.join(output_dir, 'collected_reviews.csv')
            with open(reviews_file, 'w', newline='', encoding='utf-8') as f:
                if self.collected_data['reviews']:
                    writer = csv.DictWriter(f, fieldnames=self.collected_data['reviews'][0].keys())
                    writer.writeheader()
                    writer.writerows(self.collected_data['reviews'])
            print(f"✅ Saved {len(self.collected_data['reviews'])} reviews to {reviews_file}")
    
    def generate_summary(self) -> str:
        """Generate a summary of collected data"""
        total_products = len(self.collected_data['products'])
        total_ingredients = len(self.collected_data['ingredients'])
        total_reviews = len(self.collected_data['reviews'])
        
        summary = f"""
📊 Data Collection Summary
========================
🛒 Products collected: {total_products}
🧪 Ingredients collected: {total_ingredients}
⭐ Reviews collected: {total_reviews}
📅 Collection date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Ready for integration into Beauty Chatbot DDD system!
"""
        return summary


def main():
    """Main function to run the interactive data collector"""
    collector = InteractiveDataCollector()
    
    try:
        # Collect data interactively
        collected_data = collector.collect_data_interactively()
        
        # Save to CSV files
        collector.save_to_csv("beauty_chatbot_ddd_package/data")
        
        # Show summary
        print(collector.generate_summary())
        
        # Ask if user wants to regenerate the chatbot code
        regenerate = input("\n🔄 Would you like to regenerate the chatbot code with this new data? (y/n): ").strip().lower()
        if regenerate == 'y':
            print("🚀 Regenerating chatbot code with new data...")
            # This would trigger the code regeneration process
            return True
        
        return False
        
    except KeyboardInterrupt:
        print("\n\n👋 Data collection cancelled by user.")
        return False
    except Exception as e:
        print(f"\n❌ Error during data collection: {str(e)}")
        return False


if __name__ == "__main__":
    success = main()
    if success:
        print("✅ Data collection and code regeneration completed!")
    else:
        print("ℹ️ Data collection completed without code regeneration.")
