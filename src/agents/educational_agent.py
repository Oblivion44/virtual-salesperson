import asyncio
import json
import os
import random
from anthropic import Anthropic

class EducationalAgent:
    def __init__(self):
        self.anthropic = None
        if os.getenv('ANTHROPIC_API_KEY'):
            self.anthropic = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    async def provide(self, message, session):
        """Provide educational content based on user request"""
        try:
            # Determine what type of educational content is needed
            content_type = await self.analyze_educational_request(message, session)
            
            # Generate appropriate educational response
            return await self.generate_educational_content(content_type, message, session)
        except Exception as e:
            print(f"Error in educational agent: {e}")
            return {
                'message': "I'd love to teach you about beauty! What specific topic would you like to learn about?",
                'type': 'clarification'
            }

    async def analyze_educational_request(self, message, session):
        """Analyze what type of educational content is needed"""
        if self.anthropic:
            try:
                prompt = f"""Analyze this message to determine what type of educational beauty content the user wants.

Message: "{message}"
User Profile: {json.dumps(session.get('profile', {}))}

Types of educational content:
- tutorial: Step-by-step how-to guides
- ingredient_education: Information about skincare/makeup ingredients
- technique_tips: Application techniques and tips
- routine_explanation: How to build and follow routines
- product_knowledge: Understanding different product types
- skin_science: Scientific explanations about skin/hair

Respond with JSON: {{"type": "content_type", "topic": "specific_topic", "format": "video|text|both"}}"""

                response = await asyncio.to_thread(
                    self.anthropic.messages.create,
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=200,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                return json.loads(response.content[0].text)
            except Exception as e:
                print(f"Error in educational analysis: {e}")
        
        # Fallback analysis
        return self.fallback_educational_analysis(message, session)

    def fallback_educational_analysis(self, message, session):
        """Simple rule-based educational content analysis"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['tutorial', 'how to', 'show me', 'demonstrate']):
            return {'type': 'tutorial', 'topic': 'general_beauty', 'format': 'video'}
        elif any(word in message_lower for word in ['ingredient', 'what is', 'explain']):
            return {'type': 'ingredient_education', 'topic': 'ingredients', 'format': 'text'}
        elif any(word in message_lower for word in ['technique', 'apply', 'use']):
            return {'type': 'technique_tips', 'topic': 'application', 'format': 'both'}
        elif any(word in message_lower for word in ['routine', 'schedule', 'order']):
            return {'type': 'routine_explanation', 'topic': 'routine', 'format': 'text'}
        else:
            return {'type': 'tutorial', 'topic': 'general_beauty', 'format': 'text'}

    async def generate_educational_content(self, content_type, message, session):
        """Generate educational content"""
        if self.anthropic:
            try:
                prompt = f"""You are Bella, a beauty education expert. Create educational content based on the request.

Content Type: {content_type['type']}
Topic: {content_type['topic']}
User Message: "{message}"
User Profile: {json.dumps(session.get('profile', {}))}

Create engaging, informative content that:
- Is appropriate for their age group and experience level
- Addresses their specific concerns
- Includes practical tips they can use
- Is encouraging and supportive

If video content is requested, also provide a detailed description for video generation."""

                response = await asyncio.to_thread(
                    self.anthropic.messages.create,
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=500,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                content = response.content[0].text
            except Exception as e:
                print(f"Error generating educational content: {e}")
                content = self.get_fallback_educational_content(content_type, session)
        else:
            content = self.get_fallback_educational_content(content_type, session)

        # Determine if video should be offered
        should_offer_video = (content_type['format'] == 'video' or 
                            content_type['format'] == 'both' or 
                            content_type['type'] == 'tutorial')

        return {
            'message': content,
            'type': 'video_tutorial_request' if should_offer_video else 'educational_content',
            'data': {
                'contentType': content_type['type'],
                'topic': content_type['topic'],
                'videoPrompt': self.generate_video_prompt(content_type, session) if should_offer_video else None
            },
            'suggestions': self.generate_educational_suggestions(content_type, session)
        }

    def get_fallback_educational_content(self, content_type, session):
        """Generate fallback educational content"""
        profile = session.get('profile', {})
        category = profile.get('category', 'skincare')
        
        content_templates = {
            'tutorial': {
                'skincare': "Here's a basic skincare tutorial! Start with a gentle cleanser to remove dirt and oil. Apply it with lukewarm water using circular motions, then rinse thoroughly. Next, apply a toner if you have one, followed by any serums or treatments. Finally, moisturize to lock in hydration and don't forget sunscreen during the day!",
                'hair': "Let me guide you through basic hair care! Start by choosing a shampoo suited to your hair type. Focus on cleansing your scalp, not the ends. Follow with conditioner from mid-length to ends, leave for 2-3 minutes, then rinse. For styling, always use heat protectant before any hot tools!",
                'makeup': "Here's a simple makeup tutorial! Start with a clean, moisturized face. Apply primer, then foundation using a damp beauty sponge or brush. Conceal any blemishes, set with powder, add some blush, define your brows, apply mascara, and finish with lip color. Remember, practice makes perfect!"
            },
            'ingredient_education': "Let me explain some key beauty ingredients! Hyaluronic Acid is amazing for hydration - it can hold 1000x its weight in water! Vitamin C brightens skin and fights free radicals. Retinol helps with anti-aging and acne. Niacinamide reduces pore appearance and controls oil. Always patch test new ingredients!",
            'technique_tips': "Here are some pro application tips! For skincare, always apply products from thinnest to thickest consistency. Pat, don't rub, to avoid irritation. For makeup, use a damp beauty sponge for flawless foundation application. Blend eyeshadow in windshield wiper motions. Set your makeup with setting spray for longevity!"
        }
        
        content_type_key = content_type['type']
        if content_type_key in content_templates and category in content_templates[content_type_key]:
            return content_templates[content_type_key][category]
        elif content_type_key in content_templates:
            return content_templates[content_type_key].get('skincare', "I'd love to help you learn more about beauty! What specific topic interests you?")
        else:
            return "I'm here to help you learn about beauty! Whether it's skincare, haircare, or makeup, I can provide tutorials, tips, and ingredient information. What would you like to know more about?"

    def generate_video_prompt(self, content_type, session):
        """Generate video prompt for NovelAI"""
        profile = session.get('profile', {})
        category = profile.get('category', 'skincare')
        age_group = profile.get('ageGroup', 'young_adults')
        
        prompts = {
            'tutorial': {
                'skincare': f"Professional skincare tutorial for {age_group}, demonstrating proper cleansing, toning, and moisturizing techniques, clean aesthetic, natural lighting",
                'hair': f"Hair care tutorial showing proper washing, conditioning, and styling techniques for {age_group}, professional salon setting",
                'makeup': f"Makeup application tutorial for {age_group}, showing foundation, concealer, and basic eye makeup, clean beauty setup"
            },
            'ingredient_education': "Close-up shots of skincare ingredients with text overlays explaining benefits, professional product photography, educational style",
            'technique_tips': "Beauty technique demonstration showing proper application methods, professional lighting, step-by-step visual guide"
        }
        
        content_type_key = content_type['type']
        if content_type_key in prompts and isinstance(prompts[content_type_key], dict):
            return prompts[content_type_key].get(category, prompts[content_type_key]['skincare'])
        else:
            return prompts.get(content_type_key, prompts['tutorial']['skincare'])

    def generate_educational_suggestions(self, content_type, session):
        """Generate contextual educational suggestions"""
        profile = session.get('profile', {})
        category = profile.get('category')
        
        if category == 'skin':
            return [
                'Show me skincare routine video',
                'Explain skincare ingredients',
                'Application techniques',
                'Skin science basics'
            ]
        elif category == 'hair':
            return [
                'Hair styling tutorial',
                'Hair care ingredients',
                'Styling techniques',
                'Hair health tips'
            ]
        elif category == 'makeup':
            return [
                'Makeup tutorial video',
                'Color theory basics',
                'Application techniques',
                'Product knowledge'
            ]
        else:
            return [
                'Show me a video tutorial',
                'Tell me about ingredients',
                'Give me more tips',
                'Explain the science behind it'
            ]
