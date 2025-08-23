import asyncio
import json
import os
import random
from anthropic import Anthropic

class RecommendationAgent:
    def __init__(self):
        self.anthropic = None
        if os.getenv('ANTHROPIC_API_KEY'):
            self.anthropic = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    async def recommend(self, message, session):
        """Generate product recommendations based on user profile"""
        try:
            # Generate product recommendations
            recommendations = await self.generate_recommendations(message, session)
            
            # Format response with product suggestions
            return self.format_recommendation_response(recommendations, session)
        except Exception as e:
            print(f"Error in recommendation agent: {e}")
            return {
                'message': "I'd love to recommend some products for you! Could you tell me more about your specific needs?",
                'type': 'clarification'
            }

    async def generate_recommendations(self, message, session):
        """Generate recommendations using Claude or fallback"""
        if self.anthropic:
            try:
                prompt = f"""Based on the user's profile and message, recommend specific beauty products.

User Profile: {json.dumps(session.get('profile', {}))}
User Message: "{message}"

Consider:
- User's concerns and skin/hair type
- Age group and lifestyle
- Budget constraints (if mentioned)
- Current products they use

Generate 3-5 specific product recommendations with:
- Product name and brand
- Why it's suitable for them
- Key benefits
- Price range
- Nykaa availability

Respond with JSON array of products."""

                response = await asyncio.to_thread(
                    self.anthropic.messages.create,
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=600,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                return json.loads(response.content[0].text)
            except Exception as e:
                print(f"Error in Claude recommendations: {e}")
        
        # Fallback recommendations
        return self.get_fallback_recommendations(session)

    def get_fallback_recommendations(self, session):
        """Get fallback product recommendations"""
        profile = session.get('profile', {})
        category = profile.get('category', 'skin')
        
        recommendations = {
            'skin': [
                {
                    'name': 'Cetaphil Gentle Skin Cleanser',
                    'brand': 'Cetaphil',
                    'price': '₹599',
                    'benefits': 'Gentle cleansing for all skin types',
                    'reason': 'Perfect for daily cleansing without irritation',
                    'rating': 4.5,
                    'reviews': 1250
                },
                {
                    'name': 'The Ordinary Hyaluronic Acid 2% + B5',
                    'brand': 'The Ordinary',
                    'price': '₹849',
                    'benefits': 'Intense hydration and plumping',
                    'reason': 'Great for maintaining skin moisture',
                    'rating': 4.7,
                    'reviews': 2100
                },
                {
                    'name': 'Neutrogena Ultra Sheer Sunscreen SPF 50+',
                    'brand': 'Neutrogena',
                    'price': '₹699',
                    'benefits': 'Broad spectrum sun protection',
                    'reason': 'Essential for preventing premature aging',
                    'rating': 4.6,
                    'reviews': 1450
                }
            ],
            'hair': [
                {
                    'name': 'L\'Oréal Paris Total Repair 5 Shampoo',
                    'brand': 'L\'Oréal Paris',
                    'price': '₹399',
                    'benefits': 'Repairs damaged hair',
                    'reason': 'Suitable for most hair types and concerns',
                    'rating': 4.4,
                    'reviews': 756
                },
                {
                    'name': 'Tresemmé Keratin Smooth Conditioner',
                    'brand': 'Tresemmé',
                    'price': '₹299',
                    'benefits': 'Smooths frizzy hair',
                    'reason': 'Great for managing unruly hair',
                    'rating': 4.2,
                    'reviews': 892
                }
            ],
            'makeup': [
                {
                    'name': 'Maybelline Fit Me Foundation',
                    'brand': 'Maybelline',
                    'price': '₹499',
                    'benefits': 'Natural coverage for all skin tones',
                    'reason': 'Popular choice for everyday wear',
                    'rating': 4.3,
                    'reviews': 890
                },
                {
                    'name': 'Lakme Absolute Lip Color',
                    'brand': 'Lakme',
                    'price': '₹650',
                    'benefits': 'Long-lasting color',
                    'reason': 'Perfect for Indian skin tones',
                    'rating': 4.1,
                    'reviews': 654
                }
            ]
        }
        
        return recommendations.get(category, recommendations['skin'])

    def format_recommendation_response(self, recommendations, session):
        """Format the recommendation response"""
        response_message = self.generate_recommendation_message(recommendations, session)
        
        return {
            'message': response_message,
            'type': 'product_recommendations',
            'data': {
                'products': recommendations,
                'productIds': [p.get('name', f'product_{i}') for i, p in enumerate(recommendations)]
            },
            'suggestions': [
                'Tell me more about these products',
                'Show me tutorials',
                'Build a routine with these',
                'Find similar products'
            ]
        }

    def generate_recommendation_message(self, recommendations, session):
        """Generate recommendation message"""
        profile = session.get('profile', {})
        category = profile.get('category', 'beauty')
        
        messages = [
            f"Perfect! I've found some amazing {category} products that would work wonderfully for you! ✨",
            f"Great news! Based on your needs, I have some fantastic {category} recommendations! 💄",
            f"I'm excited to share these {category} products that are perfect for your concerns! 🌟"
        ]
        
        base_message = random.choice(messages)
        
        if recommendations:
            return f"{base_message}\n\nI've selected {len(recommendations)} products that address your specific needs. Each one has been chosen based on your profile and will help you achieve your beauty goals. Check them out below!"
        
        return base_message
