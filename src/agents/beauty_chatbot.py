import asyncio
import json
import os
from datetime import datetime
from anthropic import Anthropic
from .concern_analysis_agent import ConcernAnalysisAgent
from .recommendation_agent import RecommendationAgent
from .educational_agent import EducationalAgent
from .routine_agent import RoutineAgent

class BeautyChatbot:
    def __init__(self):
        self.anthropic = None
        if os.getenv('ANTHROPIC_API_KEY'):
            self.anthropic = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        
        # Initialize specialized agents (Strand pattern)
        self.concern_agent = ConcernAnalysisAgent()
        self.recommendation_agent = RecommendationAgent()
        self.educational_agent = EducationalAgent()
        self.routine_agent = RoutineAgent()
        
        self.system_prompt = """You are Bella, an AI virtual salesperson for a beauty e-commerce company. You specialize in Skin, Hair, and Makeup products with access to 24K products.

Your personality:
- Friendly, knowledgeable, and enthusiastic about beauty
- Natural conversationalist who builds rapport
- Expert in skincare, haircare, and makeup
- Focused on personalized recommendations
- Educational and helpful

Your capabilities:
- Analyze skin/hair concerns and recommend products
- Provide educational content and tutorials
- Create personalized beauty routines
- Handle budget constraints intelligently
- Link to Nykaa.com products with images

Conversation flow:
1. Warm greeting and category detection (Skin/Hair/Makeup)
2. Progressive profile building (age, concerns, preferences)
3. Concern analysis and product recommendations
4. Educational content delivery when requested
5. Routine curation and budget-aware suggestions

Always be natural, avoid rigid forms, and focus on building trust through expertise."""

    async def process_message(self, message, session):
        """Process user message and route to appropriate agent"""
        try:
            # Determine intent and route to appropriate agent
            intent = await self.analyze_intent(message, session)
            
            if intent['type'] == 'greeting':
                return self.handle_greeting(message, session)
            elif intent['type'] == 'concern_analysis':
                return await self.concern_agent.analyze(message, session)
            elif intent['type'] == 'product_recommendation':
                return await self.recommendation_agent.recommend(message, session)
            elif intent['type'] == 'educational_request':
                return await self.educational_agent.provide(message, session)
            elif intent['type'] == 'routine_building':
                return await self.routine_agent.build(message, session)
            elif intent['type'] == 'general_chat':
                return await self.handle_general_chat(message, session)
            else:
                return self.handle_fallback(message, session)
                
        except Exception as e:
            print(f"Error in process_message: {e}")
            return {
                'message': "I'm sorry, I encountered an issue. Could you please rephrase your question?",
                'type': 'error'
            }

    async def analyze_intent(self, message, session):
        """Analyze user intent using Claude or fallback logic"""
        if self.anthropic:
            try:
                prompt = f"""Analyze the user's message and determine their intent. Consider the conversation history and current step.

User message: "{message}"
Current step: {session.get('currentStep', 'greeting')}
Conversation history: {json.dumps(session.get('conversationHistory', [])[-3:])}

Possible intents:
- greeting: Initial hello, introduction
- concern_analysis: Describing skin/hair issues, problems
- product_recommendation: Asking for product suggestions
- educational_request: Wanting tutorials, how-to content
- routine_building: Creating skincare/haircare routines
- general_chat: General beauty questions, chitchat

Respond with JSON: {{"type": "intent_name", "confidence": 0.9, "entities": {{}}}}"""

                response = await asyncio.to_thread(
                    self.anthropic.messages.create,
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=200,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                return json.loads(response.content[0].text)
            except:
                pass
        
        # Fallback intent analysis
        return self.fallback_intent_analysis(message, session)

    def fallback_intent_analysis(self, message, session):
        """Simple rule-based intent analysis"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['hello', 'hi', 'hey', 'start']):
            return {'type': 'greeting', 'confidence': 0.8}
        elif any(word in message_lower for word in ['skin', 'acne', 'dry', 'oily', 'hair', 'frizz', 'damage']):
            return {'type': 'concern_analysis', 'confidence': 0.7}
        elif any(word in message_lower for word in ['recommend', 'product', 'suggest', 'buy']):
            return {'type': 'product_recommendation', 'confidence': 0.7}
        elif any(word in message_lower for word in ['tutorial', 'how to', 'show me', 'teach']):
            return {'type': 'educational_request', 'confidence': 0.7}
        elif any(word in message_lower for word in ['routine', 'schedule', 'plan', 'regimen']):
            return {'type': 'routine_building', 'confidence': 0.7}
        else:
            return {'type': 'general_chat', 'confidence': 0.5}

    def handle_greeting(self, message, session):
        """Handle greeting messages"""
        session['currentStep'] = 'category_detection'
        
        greetings = [
            "Hi there! I'm Bella, your personal beauty consultant! ✨ I'm here to help you discover amazing products for your skin, hair, or makeup needs. What brings you here today?",
            "Hello beautiful! 💄 I'm Bella, and I'm excited to help you find the perfect beauty products! Are you looking for skincare, haircare, or makeup solutions?",
            "Hey there! Welcome to your personalized beauty journey! I'm Bella, and I specialize in helping you find products that work perfectly for YOU. What area would you like to focus on - skin, hair, or makeup?"
        ]
        
        import random
        return {
            'message': random.choice(greetings),
            'type': 'greeting',
            'suggestions': ['Skincare help', 'Hair concerns', 'Makeup advice', 'Build a routine']
        }

    async def handle_general_chat(self, message, session):
        """Handle general chat messages"""
        if self.anthropic:
            try:
                prompt = f"""{self.system_prompt}

User profile: {json.dumps(session.get('profile', {}))}
Conversation history: {json.dumps(session.get('conversationHistory', [])[-5:])}

User message: "{message}"

Respond as Bella, the beauty consultant. Be helpful, engaging, and try to guide the conversation toward beauty topics where you can provide value."""

                response = await asyncio.to_thread(
                    self.anthropic.messages.create,
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=300,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                return {
                    'message': response.content[0].text,
                    'type': 'general_chat',
                    'suggestions': self.generate_suggestions(session)
                }
            except Exception as e:
                print(f"Error in general chat: {e}")
        
        # Fallback response
        return {
            'message': "That's interesting! I'm here to help with all your beauty needs. What specific area would you like to focus on - skincare, haircare, or makeup?",
            'type': 'general_chat',
            'suggestions': ['Skincare advice', 'Hair problems', 'Makeup tips', 'Product recommendations']
        }

    def handle_fallback(self, message, session):
        """Handle fallback cases"""
        fallbacks = [
            "I want to make sure I give you the best advice! Could you tell me a bit more about what you're looking for?",
            "That's interesting! To help you better, could you share more details about your beauty concerns or goals?",
            "I'm here to help with all things beauty! What specific area would you like to focus on - skincare, haircare, or makeup?"
        ]
        
        import random
        return {
            'message': random.choice(fallbacks),
            'type': 'clarification',
            'suggestions': ['Skincare advice', 'Hair problems', 'Makeup tips', 'Product recommendations']
        }

    def generate_suggestions(self, session):
        """Generate contextual suggestions"""
        profile = session.get('profile', {})
        
        if profile.get('category') == 'skin':
            return ['Skincare routine', 'Product recommendations', 'Skin tutorials', 'Ingredient advice']
        elif profile.get('category') == 'hair':
            return ['Hair routine', 'Hair products', 'Styling tutorials', 'Hair health tips']
        elif profile.get('category') == 'makeup':
            return ['Makeup looks', 'Product suggestions', 'Makeup tutorials', 'Color matching']
        else:
            return ['Recommend products for me', 'Show me tutorials', 'Build a routine', 'What\'s trending?']
