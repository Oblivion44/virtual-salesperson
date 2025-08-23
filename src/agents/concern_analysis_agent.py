import asyncio
import json
import os
from anthropic import Anthropic

class ConcernAnalysisAgent:
    def __init__(self):
        self.anthropic = None
        if os.getenv('ANTHROPIC_API_KEY'):
            self.anthropic = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    async def analyze(self, message, session):
        """Analyze beauty concerns and update user profile"""
        try:
            # Extract concerns and profile information
            analysis = await self.extract_concerns(message, session)
            
            # Update user profile with extracted information
            self.update_profile(session, analysis)
            
            # Generate response with follow-up questions or recommendations
            return await self.generate_response(analysis, session)
        except Exception as e:
            print(f"Error in concern analysis: {e}")
            return {
                'message': "I'd love to help you with your concerns! Could you tell me a bit more about what you're experiencing?",
                'type': 'clarification'
            }

    async def extract_concerns(self, message, session):
        """Extract concerns using Claude or fallback logic"""
        if self.anthropic:
            try:
                prompt = f"""Analyze this beauty-related message and extract key information:

Message: "{message}"
Current profile: {json.dumps(session.get('profile', {}))}

Extract and categorize:
1. Category (skin, hair, makeup)
2. Specific concerns (acne, dryness, frizz, etc.)
3. Age group (if mentioned)
4. Skin/hair type (if mentioned)
5. Current products used (if mentioned)
6. Budget mentions (if any)
7. Lifestyle factors (if mentioned)

Respond with JSON:
{{
  "category": "skin|hair|makeup",
  "concerns": ["concern1", "concern2"],
  "ageGroup": "teens|young_adults|adults|mature",
  "skinType": "oily|dry|combination|sensitive|normal",
  "hairType": "straight|wavy|curly|coily",
  "currentProducts": ["product1", "product2"],
  "budget": "budget_info_or_null",
  "lifestyle": ["factor1", "factor2"],
  "confidence": 0.8
}}"""

                response = await asyncio.to_thread(
                    self.anthropic.messages.create,
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=400,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                return json.loads(response.content[0].text)
            except Exception as e:
                print(f"Error in Claude analysis: {e}")
        
        # Fallback analysis
        return self.fallback_concern_analysis(message, session)

    def fallback_concern_analysis(self, message, session):
        """Simple rule-based concern analysis"""
        message_lower = message.lower()
        analysis = {
            'category': 'general',
            'concerns': [],
            'confidence': 0.5
        }
        
        # Category detection
        if any(word in message_lower for word in ['skin', 'face', 'acne', 'pimple', 'dry', 'oily']):
            analysis['category'] = 'skin'
            analysis['confidence'] = 0.7
        elif any(word in message_lower for word in ['hair', 'scalp', 'frizz', 'damage', 'curl']):
            analysis['category'] = 'hair'
            analysis['confidence'] = 0.7
        elif any(word in message_lower for word in ['makeup', 'foundation', 'lipstick', 'eyeshadow']):
            analysis['category'] = 'makeup'
            analysis['confidence'] = 0.7
        
        # Concern detection
        concerns = []
        if 'acne' in message_lower or 'pimple' in message_lower:
            concerns.append('acne')
        if 'dry' in message_lower:
            concerns.append('dryness')
        if 'oily' in message_lower:
            concerns.append('oiliness')
        if 'sensitive' in message_lower:
            concerns.append('sensitivity')
        if 'frizz' in message_lower:
            concerns.append('frizz')
        if 'damage' in message_lower:
            concerns.append('damage')
        
        analysis['concerns'] = concerns
        
        # Age group detection
        if any(word in message_lower for word in ['teen', '13', '14', '15', '16', '17', '18', '19']):
            analysis['ageGroup'] = 'teens'
        elif any(word in message_lower for word in ['20s', 'twenties', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29']):
            analysis['ageGroup'] = 'young_adults'
        elif any(word in message_lower for word in ['30s', 'thirties', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39']):
            analysis['ageGroup'] = 'adults'
        elif any(word in message_lower for word in ['40', '50', '60', 'mature', 'older']):
            analysis['ageGroup'] = 'mature'
        
        return analysis

    def update_profile(self, session, analysis):
        """Update user profile with analysis results"""
        if 'profile' not in session:
            session['profile'] = {}
        
        profile = session['profile']
        
        # Merge analysis results into user profile
        if analysis.get('category'):
            profile['category'] = analysis['category']
        
        if analysis.get('concerns'):
            existing_concerns = profile.get('concerns', [])
            profile['concerns'] = list(set(existing_concerns + analysis['concerns']))
        
        if analysis.get('ageGroup'):
            profile['ageGroup'] = analysis['ageGroup']
        
        if analysis.get('skinType'):
            profile['skinType'] = analysis['skinType']
        
        if analysis.get('hairType'):
            profile['hairType'] = analysis['hairType']
        
        if analysis.get('currentProducts'):
            existing_products = profile.get('currentProducts', [])
            profile['currentProducts'] = list(set(existing_products + analysis['currentProducts']))
        
        if analysis.get('budget'):
            profile['budget'] = analysis['budget']
        
        if analysis.get('lifestyle'):
            existing_lifestyle = profile.get('lifestyle', [])
            profile['lifestyle'] = list(set(existing_lifestyle + analysis['lifestyle']))
        
        # Update conversation step
        if analysis.get('confidence', 0) > 0.7:
            session['currentStep'] = 'recommendation_ready'
        else:
            session['currentStep'] = 'gathering_info'

    async def generate_response(self, analysis, session):
        """Generate empathetic response based on analysis"""
        if self.anthropic:
            try:
                prompt = f"""You are Bella, a beauty consultant. Based on the concern analysis, generate an empathetic and helpful response.

Analysis: {json.dumps(analysis)}
User Profile: {json.dumps(session.get('profile', {}))}

Guidelines:
- Acknowledge their concerns with empathy
- Ask clarifying questions if needed (confidence < 0.7)
- Offer to provide recommendations if you have enough info
- Be encouraging and supportive
- Keep response conversational and friendly

Generate a response that moves the conversation forward naturally."""

                response = await asyncio.to_thread(
                    self.anthropic.messages.create,
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=300,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                suggestions = self.generate_suggestions(analysis, session)
                
                return {
                    'message': response.content[0].text,
                    'type': 'concern_analysis',
                    'data': {
                        'analysis': analysis,
                        'profileUpdated': True
                    },
                    'suggestions': suggestions
                }
            except Exception as e:
                print(f"Error generating response: {e}")
        
        # Fallback response
        return self.generate_fallback_response(analysis, session)

    def generate_fallback_response(self, analysis, session):
        """Generate fallback response without Claude"""
        category = analysis.get('category', 'beauty')
        concerns = analysis.get('concerns', [])
        confidence = analysis.get('confidence', 0.5)
        
        if confidence > 0.7:
            if category == 'skin':
                message = f"I understand you're dealing with {', '.join(concerns) if concerns else 'skin concerns'}. That's very common and definitely manageable! I'd love to help you find the right products and create a routine that works for you."
            elif category == 'hair':
                message = f"Hair concerns like {', '.join(concerns) if concerns else 'the ones you mentioned'} can be frustrating, but there are great solutions available! Let me help you find products that will address these issues."
            elif category == 'makeup':
                message = f"I'm excited to help you with your makeup goals! Whether it's {', '.join(concerns) if concerns else 'finding the right products'}, I can guide you to the perfect solutions."
            else:
                message = "I'm here to help with all your beauty needs! Let me know what specific area you'd like to focus on."
        else:
            message = "I'd love to help you more! Could you tell me a bit more about your specific concerns? For example, what's your biggest beauty challenge right now?"
        
        suggestions = self.generate_suggestions(analysis, session)
        
        return {
            'message': message,
            'type': 'concern_analysis',
            'data': {
                'analysis': analysis,
                'profileUpdated': True
            },
            'suggestions': suggestions
        }

    def generate_suggestions(self, analysis, session):
        """Generate contextual suggestions based on analysis"""
        suggestions = []
        confidence = analysis.get('confidence', 0.5)
        category = analysis.get('category')
        profile = session.get('profile', {})
        
        if confidence > 0.7:
            suggestions.append('Show me product recommendations')
            suggestions.append('I want to see tutorials')
            
            if category == 'skin':
                suggestions.extend(['Build a skincare routine', 'Tell me about ingredients'])
            elif category == 'hair':
                suggestions.extend(['Create a hair routine', 'Show styling tips'])
            elif category == 'makeup':
                suggestions.extend(['Suggest makeup looks', 'Help with color matching'])
        else:
            # Need more information
            if not profile.get('ageGroup'):
                suggestions.extend(['I\'m a teenager', 'I\'m in my 20s', 'I\'m in my 30s', 'I\'m 40+'])
            
            if category == 'skin' and not profile.get('skinType'):
                suggestions.extend(['My skin is oily', 'My skin is dry', 'I have combination skin', 'I have sensitive skin'])
        
        return suggestions[:4]  # Limit to 4 suggestions
