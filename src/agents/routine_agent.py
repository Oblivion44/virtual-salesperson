import asyncio
import json
import os
import random
from anthropic import Anthropic

class RoutineAgent:
    def __init__(self):
        self.anthropic = None
        if os.getenv('ANTHROPIC_API_KEY'):
            self.anthropic = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))

    async def build(self, message, session):
        """Build personalized beauty routine"""
        try:
            # Analyze what type of routine is needed
            routine_type = await self.analyze_routine_request(message, session)
            
            # Generate personalized routine
            routine = await self.generate_routine(routine_type, session)
            
            # Format response
            return self.format_routine_response(routine, session)
        except Exception as e:
            print(f"Error in routine agent: {e}")
            return {
                'message': "I'd love to create a personalized routine for you! Tell me about your current routine and what you'd like to improve.",
                'type': 'clarification'
            }

    async def analyze_routine_request(self, message, session):
        """Analyze what type of routine is needed"""
        if self.anthropic:
            try:
                prompt = f"""Analyze this message to understand what type of beauty routine the user wants.

Message: "{message}"
User Profile: {json.dumps(session.get('profile', {}))}

Determine:
- Routine type (morning, evening, weekly, full_regimen)
- Category (skincare, haircare, makeup)
- Complexity level (beginner, intermediate, advanced)
- Time constraints (quick, standard, comprehensive)
- Special focus areas

Respond with JSON: {{
  "type": "routine_type",
  "category": "category",
  "complexity": "level",
  "timeframe": "duration",
  "focus": ["area1", "area2"]
}}"""

                response = await asyncio.to_thread(
                    self.anthropic.messages.create,
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=300,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                return json.loads(response.content[0].text)
            except Exception as e:
                print(f"Error in routine analysis: {e}")
        
        # Fallback analysis
        return self.fallback_routine_analysis(message, session)

    def fallback_routine_analysis(self, message, session):
        """Simple rule-based routine analysis"""
        message_lower = message.lower()
        profile = session.get('profile', {})
        
        routine_type = {
            'type': 'full_regimen',
            'category': profile.get('category', 'skincare'),
            'complexity': 'beginner',
            'timeframe': 'standard',
            'focus': profile.get('concerns', [])
        }
        
        # Routine type detection
        if 'morning' in message_lower:
            routine_type['type'] = 'morning'
        elif 'evening' in message_lower or 'night' in message_lower:
            routine_type['type'] = 'evening'
        elif 'weekly' in message_lower:
            routine_type['type'] = 'weekly'
        
        # Complexity detection
        if any(word in message_lower for word in ['simple', 'basic', 'beginner', 'easy']):
            routine_type['complexity'] = 'beginner'
        elif any(word in message_lower for word in ['advanced', 'detailed', 'comprehensive']):
            routine_type['complexity'] = 'advanced'
        else:
            routine_type['complexity'] = 'intermediate'
        
        # Time constraints
        if any(word in message_lower for word in ['quick', 'fast', 'short', '5 minute']):
            routine_type['timeframe'] = 'quick'
        elif any(word in message_lower for word in ['detailed', 'comprehensive', 'thorough']):
            routine_type['timeframe'] = 'comprehensive'
        
        return routine_type

    async def generate_routine(self, routine_type, session):
        """Generate personalized routine"""
        if self.anthropic:
            try:
                prompt = f"""Create a personalized beauty routine based on the user's profile and requirements.

User Profile: {json.dumps(session.get('profile', {}))}
Routine Requirements: {json.dumps(routine_type)}

Create a detailed routine that includes:
- Step-by-step instructions
- Product recommendations
- Timing and frequency
- Tips for success
- Budget-conscious alternatives if budget is mentioned

Make it practical, achievable, and tailored to their specific needs and lifestyle.

Format as JSON with structure:
{{
  "title": "Routine Name",
  "description": "Brief description",
  "steps": [
    {{
      "step": 1,
      "name": "Step Name",
      "description": "What to do",
      "products": ["product suggestions"],
      "timing": "when to do it",
      "tips": "helpful tips"
    }}
  ],
  "frequency": "how often",
  "totalTime": "estimated time",
  "budgetTips": "cost-saving suggestions"
}}"""

                response = await asyncio.to_thread(
                    self.anthropic.messages.create,
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=800,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                return json.loads(response.content[0].text)
            except Exception as e:
                print(f"Error generating routine: {e}")
        
        # Fallback routine
        return self.get_fallback_routine(routine_type, session)

    def get_fallback_routine(self, routine_type, session):
        """Generate fallback routine"""
        category = routine_type.get('category', 'skincare')
        complexity = routine_type.get('complexity', 'beginner')
        
        routines = {
            'skincare': {
                'beginner': {
                    'title': 'Basic Skincare Routine',
                    'description': 'A gentle, effective routine suitable for most skin types',
                    'steps': [
                        {
                            'step': 1,
                            'name': 'Cleanse',
                            'description': 'Gently cleanse your face with a mild cleanser',
                            'products': ['Gentle facial cleanser'],
                            'timing': 'Morning and evening',
                            'tips': 'Use lukewarm water and pat dry'
                        },
                        {
                            'step': 2,
                            'name': 'Moisturize',
                            'description': 'Apply a suitable moisturizer for your skin type',
                            'products': ['Facial moisturizer'],
                            'timing': 'After cleansing',
                            'tips': 'Apply while skin is still slightly damp'
                        },
                        {
                            'step': 3,
                            'name': 'Sun Protection',
                            'description': 'Apply broad-spectrum SPF 30+ sunscreen',
                            'products': ['Sunscreen SPF 30+'],
                            'timing': 'Morning only',
                            'tips': 'Reapply every 2 hours if outdoors'
                        }
                    ],
                    'frequency': 'Daily',
                    'totalTime': '5-10 minutes',
                    'budgetTips': 'Start with drugstore brands - they can be just as effective!'
                },
                'intermediate': {
                    'title': 'Complete Skincare Routine',
                    'description': 'A comprehensive routine for better skin health',
                    'steps': [
                        {
                            'step': 1,
                            'name': 'Double Cleanse',
                            'description': 'Use oil cleanser first, then water-based cleanser',
                            'products': ['Oil cleanser', 'Gentle foam cleanser'],
                            'timing': 'Evening',
                            'tips': 'Massage oil cleanser for 1 minute'
                        },
                        {
                            'step': 2,
                            'name': 'Tone',
                            'description': 'Apply toner to balance skin pH',
                            'products': ['Alcohol-free toner'],
                            'timing': 'After cleansing',
                            'tips': 'Pat gently, don\'t rub'
                        },
                        {
                            'step': 3,
                            'name': 'Treat',
                            'description': 'Apply serums or treatments',
                            'products': ['Vitamin C serum (AM)', 'Retinol (PM)'],
                            'timing': 'Before moisturizer',
                            'tips': 'Start with lower concentrations'
                        },
                        {
                            'step': 4,
                            'name': 'Moisturize',
                            'description': 'Hydrate and seal in treatments',
                            'products': ['Day moisturizer', 'Night moisturizer'],
                            'timing': 'Morning and evening',
                            'tips': 'Use different formulas for day/night'
                        },
                        {
                            'step': 5,
                            'name': 'Protect',
                            'description': 'Apply sunscreen every morning',
                            'products': ['Broad-spectrum SPF 30+'],
                            'timing': 'Morning only',
                            'tips': 'Wait 15 minutes before makeup'
                        }
                    ],
                    'frequency': 'Daily',
                    'totalTime': '10-15 minutes',
                    'budgetTips': 'Invest in a good cleanser and sunscreen first!'
                }
            },
            'haircare': {
                'beginner': {
                    'title': 'Basic Hair Care Routine',
                    'description': 'Simple routine to keep your hair healthy',
                    'steps': [
                        {
                            'step': 1,
                            'name': 'Shampoo',
                            'description': 'Cleanse scalp and hair with appropriate shampoo',
                            'products': ['Shampoo for your hair type'],
                            'timing': '2-3 times per week',
                            'tips': 'Focus on the scalp, not the ends'
                        },
                        {
                            'step': 2,
                            'name': 'Condition',
                            'description': 'Apply conditioner to mid-lengths and ends',
                            'products': ['Conditioner'],
                            'timing': 'After every shampoo',
                            'tips': 'Leave on for 2-3 minutes before rinsing'
                        },
                        {
                            'step': 3,
                            'name': 'Protect',
                            'description': 'Use heat protectant before styling',
                            'products': ['Heat protectant spray'],
                            'timing': 'Before heat styling',
                            'tips': 'Apply to damp hair for best protection'
                        }
                    ],
                    'frequency': '2-3 times per week',
                    'totalTime': '10-15 minutes',
                    'budgetTips': 'A good conditioner makes the biggest difference!'
                }
            }
        }
        
        return routines.get(category, {}).get(complexity, routines['skincare']['beginner'])

    def format_routine_response(self, routine, session):
        """Format routine response"""
        message = self.generate_routine_message(routine, session)
        
        return {
            'message': message,
            'type': 'routine_created',
            'data': {
                'routine': routine,
                'customized': True
            },
            'suggestions': [
                'Show me product recommendations',
                'Create a shopping list',
                'Modify this routine',
                'Show me tutorials for these steps'
            ]
        }

    def generate_routine_message(self, routine, session):
        """Generate routine message"""
        profile = session.get('profile', {})
        
        message = f"🌟 Perfect! I've created a personalized \"{routine['title']}\" just for you!\n\n"
        message += f"{routine['description']}\n\n"
        
        message += "📋 **Your Routine Steps:**\n"
        for step in routine['steps']:
            message += f"\n**{step['step']}. {step['name']}**\n"
            message += f"{step['description']}\n"
            if step.get('products'):
                message += f"*Recommended products: {', '.join(step['products'])}*\n"
            if step.get('timing'):
                message += f"*Timing: {step['timing']}*\n"
        
        message += f"\n⏰ **Frequency:** {routine['frequency']}"
        message += f"\n🕐 **Total Time:** {routine['totalTime']}"
        
        if routine.get('budgetTips'):
            message += f"\n\n💡 **Budget Tips:** {routine['budgetTips']}"
        
        message += "\n\nI can help you find specific products for each step or show you tutorial videos! What would you like to explore first?"
        
        return message
