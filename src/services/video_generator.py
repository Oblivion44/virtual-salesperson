import asyncio
import aiohttp
import os
import uuid
import json
from datetime import datetime

class VideoGenerator:
    def __init__(self):
        self.api_key = os.getenv('NOVELAI_API_KEY')
        self.base_url = os.getenv('NOVELAI_REEL_ENDPOINT', 'https://api.novelai.net/ai/generate-video')
        self.video_storage_path = os.getenv('VIDEO_STORAGE_PATH', './videos')
        
        # Ensure video storage directory exists
        os.makedirs(self.video_storage_path, exist_ok=True)

    async def generate_video(self, options):
        """Generate video using NovelAI Reel API"""
        prompt = options.get('prompt', '')
        style = options.get('style', 'tutorial')
        duration = min(options.get('duration', 10), 30)  # Cap at 30 seconds
        user_id = options.get('userId', 'anonymous')
        aspect_ratio = options.get('aspectRatio', '16:9')
        quality = options.get('quality', 'high')
        
        try:
            # Generate unique video ID
            video_id = str(uuid.uuid4())
            
            # Prepare NovelAI Reel request
            request_data = {
                'prompt': self.enhance_prompt(prompt, style),
                'duration': duration,
                'aspect_ratio': aspect_ratio,
                'quality': quality,
                'style': self.get_style_preset(style),
                'seed': hash(prompt) % 1000000  # Deterministic seed based on prompt
            }
            
            print(f"Generating video for user {user_id}: {prompt}")
            
            if not self.api_key:
                # Return fallback content when no API key
                return {
                    'success': False,
                    'error': 'NovelAI API key not configured',
                    'fallback': self.get_fallback_content(prompt, style)
                }
            
            # Make request to NovelAI Reel API
            async with aiohttp.ClientSession() as session:
                headers = {
                    'Authorization': f'Bearer {self.api_key}',
                    'Content-Type': 'application/json'
                }
                
                async with session.post(
                    self.base_url, 
                    json=request_data, 
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=120)
                ) as response:
                    
                    if response.status == 200:
                        result = await response.json()
                        
                        # Handle the response based on NovelAI's API structure
                        if result.get('video_url'):
                            # Direct URL provided
                            video_url = result['video_url']
                        elif result.get('task_id'):
                            # Async generation - poll for completion
                            video_url = await self.poll_for_completion(result['task_id'])
                        else:
                            raise Exception('Unexpected API response format')
                        
                        # Download and save video locally (in a real implementation)
                        local_path = f"/videos/{video_id}.mp4"
                        
                        return {
                            'success': True,
                            'videoId': video_id,
                            'localPath': local_path,
                            'originalPrompt': prompt,
                            'enhancedPrompt': request_data['prompt'],
                            'duration': duration,
                            'style': style,
                            'metadata': {
                                'generatedAt': datetime.now().isoformat(),
                                'userId': user_id,
                                'fileSize': 0  # Would be actual file size
                            }
                        }
                    else:
                        error_text = await response.text()
                        raise Exception(f"API request failed: {response.status} - {error_text}")
            
        except Exception as e:
            print(f"Video generation error: {e}")
            
            # Return fallback response
            return {
                'success': False,
                'error': str(e),
                'fallback': self.get_fallback_content(prompt, style)
            }

    async def generate_tutorial(self, topic):
        """Generate tutorial video for specific topic"""
        tutorial_prompts = {
            'skincare_routine': 'A person demonstrating a gentle skincare routine, applying cleanser, toner, and moisturizer with proper techniques, clean aesthetic, natural lighting',
            'makeup_application': 'Professional makeup application tutorial showing foundation, concealer, and basic eye makeup techniques, clean beauty setup',
            'hair_styling': 'Hair styling tutorial showing how to create loose waves using a curling iron, professional salon setting',
            'ingredient_education': 'Close-up shots of skincare ingredients like hyaluronic acid serum, vitamin C, and retinol with text overlays explaining benefits'
        }
        
        prompt = tutorial_prompts.get(topic, f"Beauty tutorial about {topic}, professional, educational, clean aesthetic")
        
        return await self.generate_video({
            'prompt': prompt,
            'style': 'tutorial',
            'duration': 10
        })

    def enhance_prompt(self, original_prompt, style):
        """Enhance prompt with style-specific additions"""
        style_enhancements = {
            'tutorial': 'professional beauty tutorial, clean aesthetic, good lighting, educational, step-by-step demonstration',
            'product_demo': 'product demonstration, before and after, clean background, professional photography',
            'routine': 'beauty routine demonstration, natural movements, clean setup, lifestyle aesthetic',
            'ingredient_focus': 'close-up product shots, ingredient focus, clean aesthetic, professional photography'
        }
        
        base_enhancement = style_enhancements.get(style, style_enhancements['tutorial'])
        
        return f"{original_prompt}, {base_enhancement}, high quality, 4K, professional lighting, beauty content, no intro or outro, direct to content"

    def get_style_preset(self, style):
        """Get style preset for NovelAI"""
        presets = {
            'tutorial': 'educational',
            'product_demo': 'commercial',
            'routine': 'lifestyle',
            'ingredient_focus': 'macro'
        }
        
        return presets.get(style, 'educational')

    async def poll_for_completion(self, task_id, max_attempts=30):
        """Poll for video generation completion"""
        for attempt in range(max_attempts):
            try:
                async with aiohttp.ClientSession() as session:
                    headers = {'Authorization': f'Bearer {self.api_key}'}
                    
                    async with session.get(
                        f"{self.base_url}/status/{task_id}",
                        headers=headers
                    ) as response:
                        
                        if response.status == 200:
                            result = await response.json()
                            
                            if result.get('status') == 'completed':
                                return result.get('video_url')
                            elif result.get('status') == 'failed':
                                raise Exception('Video generation failed')
                        
                        # Wait 4 seconds before next poll
                        await asyncio.sleep(4)
                        
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise e
        
        raise Exception('Video generation timeout')

    def get_fallback_content(self, prompt, style):
        """Return text-based tutorial content when video generation fails"""
        return {
            'type': 'text_tutorial',
            'title': f'Tutorial: {prompt}',
            'steps': self.generate_text_steps(prompt, style),
            'message': 'Video generation is temporarily unavailable. Here\'s a detailed text tutorial instead!'
        }

    def generate_text_steps(self, prompt, style):
        """Generate basic text steps based on the prompt"""
        prompt_lower = prompt.lower()
        
        if 'skin' in prompt_lower or 'face' in prompt_lower:
            return [
                'Start with clean hands and a clean face',
                'Apply products from thinnest to thickest consistency',
                'Use gentle upward motions when applying',
                'Allow each product to absorb before applying the next',
                'Don\'t forget your neck and décolletage'
            ]
        elif 'makeup' in prompt_lower:
            return [
                'Start with a clean, moisturized face',
                'Apply primer and let it set',
                'Use the right tools for each product',
                'Build coverage gradually',
                'Set with powder or setting spray'
            ]
        elif 'hair' in prompt_lower:
            return [
                'Start with clean, towel-dried hair',
                'Apply products evenly from mid-length to ends',
                'Use heat protectant before styling',
                'Work in sections for best results',
                'Finish with a light hold product'
            ]
        else:
            return [
                'Prepare your workspace and tools',
                'Follow the steps in order',
                'Take your time and be gentle',
                'Practice makes perfect',
                'Clean up and store products properly'
            ]
