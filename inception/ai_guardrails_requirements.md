# AI Guardrails & Content Filtering Requirements

## Overview
This document defines the guardrails and content filtering mechanisms to ensure the AI virtual salesperson stays focused on beauty topics and provides appropriate, helpful responses.

## Core Guardrails

### 1. Topic Boundaries
**Allowed Topics:**
- Beauty and skincare concerns
- Hair care and styling
- Makeup application and products
- Ingredient education and benefits
- Product recommendations and reviews
- Beauty routines and regimens
- Home remedies for beauty concerns
- Age-appropriate beauty advice

**Restricted Topics:**
- Medical advice or diagnosis
- Non-beauty related products
- Personal/private information requests
- Inappropriate or adult content
- Financial advice beyond product pricing
- Political or controversial topics
- Competitor analysis or comparisons outside product scope

### 2. Response Guidelines

#### Professional Beauty Consultant Persona
```
- Maintain friendly, knowledgeable tone
- Focus on customer's beauty goals
- Provide educational content
- Suggest products based on concerns
- Encourage healthy beauty practices
- Avoid medical claims or promises
```

#### Redirection Strategies
```python
# Pseudo-code for topic detection and redirection
def handle_off_topic_query(user_input):
    if detect_medical_query(user_input):
        return "I'm a beauty consultant, not a medical professional. For skin conditions requiring medical attention, please consult a dermatologist. However, I can help you with beauty products that might complement your skincare routine!"
    
    elif detect_non_beauty_query(user_input):
        return "I specialize in beauty and personal care! Let me help you with skincare, haircare, or makeup instead. What beauty concerns can I assist you with today?"
    
    elif detect_inappropriate_content(user_input):
        return "Let's keep our conversation focused on beauty and personal care. How can I help you achieve your beauty goals today?"
```

## Content Filtering Mechanisms

### 1. Input Validation
```python
class InputValidator:
    def __init__(self):
        self.beauty_keywords = [
            "skin", "hair", "makeup", "beauty", "skincare", 
            "cosmetics", "routine", "product", "ingredient",
            "acne", "dry", "oily", "wrinkles", "aging"
        ]
        
        self.restricted_keywords = [
            "medical", "disease", "prescription", "diagnosis",
            "politics", "religion", "personal info"
        ]
    
    def is_beauty_related(self, text):
        # Check if input contains beauty-related keywords
        # Use NLP to determine topic relevance
        pass
    
    def contains_restricted_content(self, text):
        # Check for inappropriate or off-topic content
        pass
```

### 2. Response Filtering
```python
class ResponseFilter:
    def filter_medical_claims(self, response):
        # Remove or modify medical claims
        # Replace with beauty-focused alternatives
        pass
    
    def ensure_product_focus(self, response):
        # Ensure responses tie back to product recommendations
        pass
    
    def validate_age_appropriateness(self, response, age_group):
        # Ensure content is appropriate for user's age group
        pass
```

### 3. Review Content Filtering

#### Sentiment Analysis Pipeline
```python
def filter_reviews(reviews, customer_profile):
    filtered_reviews = []
    
    for review in reviews:
        # 1. Sentiment filtering
        if review.sentiment != "Positive":
            continue
            
        # 2. Relevance filtering
        if not is_relevant_to_profile(review, customer_profile):
            continue
            
        # 3. Content appropriateness
        if contains_inappropriate_content(review.text):
            continue
            
        # 4. Age appropriateness
        if not age_appropriate(review, customer_profile.age_group):
            continue
            
        filtered_reviews.append(review)
    
    return filtered_reviews
```

#### Review Quality Criteria
- **Positive Sentiment**: Rating ≥ 4 stars
- **Relevant Content**: Mentions customer's concerns or skin/hair type
- **Appropriate Language**: No inappropriate or offensive content
- **Helpful Information**: Contains specific product benefits or usage tips
- **Age Appropriate**: Suitable for customer's age group

## Conversation Flow Controls

### 1. Context Maintenance
```python
class ConversationManager:
    def __init__(self):
        self.conversation_history = []
        self.customer_profile = {}
        self.current_topic = None
    
    def maintain_beauty_focus(self):
        # Ensure conversation stays on beauty topics
        # Redirect if conversation drifts
        pass
    
    def track_customer_intent(self):
        # Understand what customer is trying to achieve
        # Guide conversation toward product recommendations
        pass
```

### 2. Escalation Handling
```python
def handle_complex_queries(user_input):
    if requires_medical_advice(user_input):
        return redirect_to_professional()
    
    elif requires_detailed_consultation(user_input):
        return offer_comprehensive_routine()
    
    elif customer_frustrated(user_input):
        return provide_alternative_approach()
```

## Safety Measures

### 1. Age-Appropriate Content
```python
def ensure_age_appropriate_content(content, age_group):
    if age_group == "Teens (13-19)":
        # Focus on gentle products, basic routines
        # Avoid anti-aging or mature skin concerns
        pass
    elif age_group == "Young Adults (20-29)":
        # Prevention-focused, trendy products
        pass
    elif age_group == "Adults (30-39)":
        # Targeted treatments, efficiency
        pass
    elif age_group == "Mature (40+)":
        # Anti-aging, intensive care
        pass
```

### 2. Budget Sensitivity
```python
def handle_budget_constraints(budget_info):
    if budget_info.lower() in ["tight", "limited", "cheap"]:
        # Focus on affordable options, drugstore brands
        # Emphasize value and multi-purpose products
        pass
    elif "expensive" in budget_info.lower():
        # Suggest premium options with justification
        pass
    else:
        # Provide range of options across price points
        pass
```

### 3. Ingredient Safety
```python
def check_ingredient_safety(ingredients, customer_profile):
    # Check for common allergens
    # Warn about potential sensitivities
    # Suggest patch testing for new ingredients
    pass
```

## Error Handling

### 1. Graceful Degradation
```python
def handle_unclear_input(user_input):
    return [
        "I want to make sure I give you the best recommendations. Could you tell me more about your specific beauty concerns?",
        "Let me help you find the perfect products. What's your main skin or hair concern right now?",
        "I'd love to help! Are you looking for skincare, haircare, or makeup recommendations today?"
    ]
```

### 2. Fallback Responses
```python
fallback_responses = [
    "I'm here to help with all your beauty needs! What would you like to know about skincare, haircare, or makeup?",
    "Let's focus on finding you the perfect beauty products. What concerns would you like to address?",
    "I specialize in beauty recommendations. How can I help you look and feel your best today?"
]
```

## Monitoring & Improvement

### 1. Conversation Quality Metrics
- Topic relevance score
- Customer satisfaction indicators
- Successful product recommendation rate
- Conversation completion rate

### 2. Content Quality Assurance
- Regular review of AI responses
- Customer feedback integration
- Continuous improvement of filtering algorithms
- Update guardrails based on edge cases

### 3. Compliance Monitoring
- Ensure no medical advice is given
- Verify age-appropriate content delivery
- Monitor for bias in recommendations
- Track adherence to beauty focus

## Implementation Priority

### Phase 1: Core Guardrails
1. Topic detection and redirection
2. Basic content filtering
3. Professional persona maintenance

### Phase 2: Advanced Filtering
1. Sophisticated sentiment analysis
2. Age-appropriate content filtering
3. Context-aware responses

### Phase 3: Optimization
1. Personalized filtering based on profile
2. Advanced conversation flow management
3. Predictive content appropriateness
