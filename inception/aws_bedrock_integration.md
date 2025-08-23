# AWS Bedrock LLM Integration Requirements

## Overview
This document defines the requirements and architecture for integrating AWS Bedrock LLM services into the AI virtual salesperson chatbot for Google Colab deployment.

## AWS Bedrock Service Requirements

### 1. Model Selection
**Primary Model**: Claude 3 (Anthropic)
- **Reasoning**: Excellent for conversational AI, safety, and instruction following
- **Use Cases**: Main conversation handling, product recommendations, content generation

**Secondary Model**: Titan Text (Amazon)
- **Reasoning**: Cost-effective for simple tasks
- **Use Cases**: Content summarization, basic text processing

**Image Generation**: Titan Image Generator
- **Reasoning**: For educational content and tutorial images
- **Use Cases**: Product demonstration images, tutorial visuals

### 2. Authentication & Setup
```python
import boto3
from botocore.config import Config

# AWS Bedrock client configuration
def setup_bedrock_client():
    config = Config(
        region_name='us-east-1',  # or preferred region
        retries={'max_attempts': 3}
    )
    
    bedrock_client = boto3.client(
        service_name='bedrock-runtime',
        config=config
    )
    
    return bedrock_client
```

### 3. Required Permissions
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-sonnet-*",
                "arn:aws:bedrock:*::foundation-model/amazon.titan-text-*",
                "arn:aws:bedrock:*::foundation-model/amazon.titan-image-*"
            ]
        }
    ]
}
```

## Integration Architecture

### 1. Core LLM Service Class
```python
class BedrockLLMService:
    def __init__(self):
        self.client = setup_bedrock_client()
        self.claude_model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
        self.titan_text_model_id = "amazon.titan-text-express-v1"
        self.titan_image_model_id = "amazon.titan-image-generator-v1"
    
    def generate_conversation_response(self, prompt, context):
        # Use Claude for main conversations
        pass
    
    def generate_product_description(self, product_data):
        # Generate compelling product descriptions
        pass
    
    def analyze_customer_input(self, user_input):
        # Analyze and extract customer intent and category
        pass
    
    def detect_beauty_category(self, user_input):
        # Detect if user is interested in Skin, Hair, or Makeup
        prompt = f"""
        Analyze this customer message and detect their primary beauty interest category.
        
        Customer message: "{user_input}"
        
        Categories:
        - Skin: skincare, facial concerns, cleansers, moisturizers, serums, acne, aging, etc.
        - Hair: haircare, scalp issues, shampoo, conditioner, styling, hair problems, etc.
        - Makeup: cosmetics, foundation, lipstick, eyeshadow, color matching, etc.
        - Mixed: mentions multiple categories
        - Unclear: not enough information to determine
        
        Return only the category name: Skin, Hair, Makeup, Mixed, or Unclear
        """
        
        return self.generate_text(prompt).strip()
    
    def generate_educational_content(self, topic):
        # Create educational content about ingredients/techniques
        pass
    
    def generate_tutorial_image(self, description):
        # Generate tutorial images using Titan Image
        pass
```

### 2. Prompt Engineering Templates

#### Conversation Prompt Template
```python
CONVERSATION_PROMPT = """
You are a professional beauty consultant and virtual salesperson. Your role is to:
1. Start with a warm, general greeting about beauty
2. Detect customer interests from their responses (skin/hair/makeup)
3. Help customers with their beauty concerns
4. Recommend appropriate products from the catalogue
5. Provide educational content about beauty and skincare
6. Maintain a friendly, knowledgeable, and helpful tone

Initial Greeting (if first interaction):
"Hello! I'm your personal beauty consultant. I'm here to help you with all your beauty needs - whether it's skincare, haircare, or makeup. What's on your mind today?"

Customer Profile (if available):
- Age Group: {age_group}
- Detected Category: {detected_category}
- Skin Type: {skin_type}
- Concerns: {concerns}
- Budget: {budget_constraints}

Conversation History:
{conversation_history}

Customer Message: {user_input}

Guidelines:
- Detect category from user responses naturally
- Stay focused on beauty topics only
- Provide specific product recommendations when appropriate
- Ask clarifying questions if needed
- Be encouraging and positive
- Redirect off-topic questions politely back to beauty

Response:
"""
```

#### Product Recommendation Prompt
```python
PRODUCT_RECOMMENDATION_PROMPT = """
Based on the customer profile and available products, recommend the most suitable products.

Customer Profile:
- Age Group: {age_group}
- Skin/Hair Type: {skin_hair_type}
- Primary Concerns: {concerns}
- Budget: {budget}

Available Products:
{filtered_products}

For each recommended product, provide:
1. Why it's suitable for this customer
2. Key benefits for their concerns
3. How to use it effectively
4. A compelling sales pitch

Format as JSON with product_id, recommendation_reason, benefits, usage_tips, sales_pitch.
"""
```

#### Educational Content Prompt
```python
EDUCATIONAL_CONTENT_PROMPT = """
Create educational content about {topic} for a {age_group} customer with {skin_type} skin.

Content should include:
1. Simple explanation of the topic
2. Benefits and importance
3. Practical tips
4. Common mistakes to avoid
5. Product recommendations if relevant

Keep the tone friendly, informative, and age-appropriate.
Limit to 200 words for easy reading.
"""
```

### 3. Response Processing Pipeline

#### Main Conversation Flow
```python
class ConversationProcessor:
    def __init__(self, llm_service):
        self.llm_service = llm_service
        self.guardrails = GuardrailsEngine()
    
    def process_user_input(self, user_input, customer_profile, conversation_history):
        # 1. Check if this is first interaction
        if not conversation_history:
            # Start with greeting and category detection
            detected_category = self.llm_service.detect_beauty_category(user_input)
            customer_profile.detected_category = detected_category
            
            if detected_category == "Unclear":
                return "I'd love to help you with your beauty needs! Could you tell me a bit more about what you're looking for - are you interested in skincare, haircare, or makeup?"
        
        # 2. Input validation and guardrails
        if not self.guardrails.is_appropriate_input(user_input):
            return self.guardrails.get_redirection_response(user_input)
        
        # 3. Intent analysis
        intent = self.llm_service.analyze_customer_input(user_input)
        
        # 4. Generate appropriate response based on intent
        if intent == "product_recommendation":
            return self.handle_product_recommendation(user_input, customer_profile)
        elif intent == "educational_query":
            return self.handle_educational_query(user_input, customer_profile)
        elif intent == "routine_request":
            return self.handle_routine_request(user_input, customer_profile)
        else:
            return self.handle_general_conversation(user_input, customer_profile, conversation_history)
    
    def handle_product_recommendation(self, user_input, customer_profile):
        # Filter products based on profile
        filtered_products = self.product_service.filter_products(customer_profile)
        
        # Generate recommendations using LLM
        recommendations = self.llm_service.generate_product_recommendations(
            customer_profile, filtered_products
        )
        
        return self.format_product_response(recommendations)
```

### 4. Content Generation Services

#### Sales Pitch Generation
```python
def generate_sales_pitch(self, product, customer_profile):
    prompt = f"""
    Create a compelling sales pitch for this product:
    
    Product: {product.name}
    Brand: {product.brand}
    Key Ingredients: {product.ingredients}
    Price: ₹{product.mrp}
    
    Customer Profile:
    - Age: {customer_profile.age_group}
    - Concerns: {customer_profile.concerns}
    - Skin Type: {customer_profile.skin_type}
    
    Create a persuasive 2-3 sentence pitch that:
    1. Addresses their specific concerns
    2. Highlights relevant benefits
    3. Creates urgency or desire
    4. Mentions value proposition
    
    Keep it natural and conversational.
    """
    
    return self.llm_service.generate_text(prompt)
```

#### Educational Video Script Generation
```python
def generate_video_script(self, product, duration=10):
    prompt = f"""
    Create a 10-second tutorial video script for {product.name}.
    
    Script should focus entirely on demonstration - NO intro or outro needed:
    - Full 10 seconds of pure product application/demonstration
    - Show step-by-step usage clearly
    - Highlight key benefits through visual demonstration
    - Keep actions simple and clear for real human demonstration
    
    Format: [Second 1-2] Action, [Second 3-4] Action, etc.
    
    No anime or cartoon elements - realistic human demonstration only.
    No time wasted on introductions or conclusions.
    """
    
    return self.llm_service.generate_text(prompt)
```

### 5. Error Handling & Fallbacks

#### Rate Limiting & Retry Logic
```python
class BedrockRateLimiter:
    def __init__(self):
        self.request_count = 0
        self.last_reset = time.time()
        self.max_requests_per_minute = 50
    
    def can_make_request(self):
        current_time = time.time()
        if current_time - self.last_reset > 60:
            self.request_count = 0
            self.last_reset = current_time
        
        return self.request_count < self.max_requests_per_minute
    
    def make_request_with_retry(self, request_func, max_retries=3):
        for attempt in range(max_retries):
            try:
                if self.can_make_request():
                    self.request_count += 1
                    return request_func()
                else:
                    time.sleep(60)  # Wait for rate limit reset
            except Exception as e:
                if attempt == max_retries - 1:
                    return self.get_fallback_response()
                time.sleep(2 ** attempt)  # Exponential backoff
```

#### Fallback Responses
```python
FALLBACK_RESPONSES = {
    "general": "I'm here to help with your beauty needs! Let me know what specific concerns you'd like to address.",
    "product_recommendation": "Based on your profile, I'd recommend checking out our top-rated products for your skin type. Would you like me to show you some options?",
    "educational": "That's a great question about skincare! Let me provide you with some helpful information.",
    "routine": "I'd love to help you create a personalized routine. Let's start with your main concerns."
}
```

### 6. Performance Optimization

#### Caching Strategy
```python
class LLMResponseCache:
    def __init__(self):
        self.cache = {}
        self.cache_ttl = 3600  # 1 hour
    
    def get_cached_response(self, prompt_hash):
        if prompt_hash in self.cache:
            response, timestamp = self.cache[prompt_hash]
            if time.time() - timestamp < self.cache_ttl:
                return response
        return None
    
    def cache_response(self, prompt_hash, response):
        self.cache[prompt_hash] = (response, time.time())
```

#### Batch Processing
```python
def batch_generate_content(self, requests):
    # Process multiple requests efficiently
    # Useful for generating multiple product descriptions
    pass
```

### 7. Google Colab Integration

#### Environment Setup
```python
# Install required packages in Colab
!pip install boto3 botocore

# Set up AWS credentials in Colab
import os
from google.colab import userdata

os.environ['AWS_ACCESS_KEY_ID'] = userdata.get('AWS_ACCESS_KEY_ID')
os.environ['AWS_SECRET_ACCESS_KEY'] = userdata.get('AWS_SECRET_ACCESS_KEY')
os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
```

#### Memory Management
```python
class ColabMemoryManager:
    def __init__(self):
        self.max_conversation_history = 10
        self.max_cached_responses = 100
    
    def cleanup_memory(self):
        # Clear old conversation history
        # Limit cache size
        # Free unused resources
        pass
```

### 8. Monitoring & Logging

#### Usage Tracking
```python
class BedrockUsageTracker:
    def __init__(self):
        self.request_log = []
        self.token_usage = 0
        self.cost_estimate = 0.0
    
    def log_request(self, model_id, input_tokens, output_tokens):
        self.request_log.append({
            'timestamp': time.time(),
            'model': model_id,
            'input_tokens': input_tokens,
            'output_tokens': output_tokens
        })
        
        self.calculate_cost(model_id, input_tokens, output_tokens)
    
    def calculate_cost(self, model_id, input_tokens, output_tokens):
        # Calculate estimated cost based on Bedrock pricing
        pass
```

## Implementation Checklist

### Phase 1: Basic Integration
- [ ] Set up AWS Bedrock client
- [ ] Implement basic conversation handling
- [ ] Create prompt templates
- [ ] Add error handling and fallbacks

### Phase 2: Advanced Features
- [ ] Implement product recommendation generation
- [ ] Add educational content creation
- [ ] Create image generation for tutorials
- [ ] Implement caching and optimization

### Phase 3: Production Readiness
- [ ] Add comprehensive monitoring
- [ ] Implement rate limiting
- [ ] Optimize for Colab environment
- [ ] Add usage tracking and cost management
