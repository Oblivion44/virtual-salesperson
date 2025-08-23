# Feature 1: Skin/Hair Concern Analysis & Product Recommendations

## Overview
This feature enables the AI to analyze customer concerns, collect beauty profile data, and provide personalized product recommendations with compelling sales pitches.

## Feature Components

### 1. Conversation Flow Design

#### Initial Greeting & Category Detection
```
AI: "Hello! I'm your personal beauty consultant. I'm here to help you with all your beauty needs - whether it's skincare, haircare, or makeup. What's on your mind today?"

User Response Analysis:
- Skin keywords: "skin", "face", "acne", "dry", "oily", "wrinkles", "aging", "cleanser", "moisturizer"
- Hair keywords: "hair", "scalp", "dandruff", "frizzy", "damaged", "shampoo", "conditioner"
- Makeup keywords: "makeup", "foundation", "lipstick", "eyeshadow", "concealer", "color"
```

#### Progressive Data Collection
```python
class ProfileCollector:
    def collect_skin_profile(self, user_input):
        questions = [
            "What's your skin type? (Dry, Oily, Combination, or Balanced)",
            "What are your main skin concerns?",
            "What's your age group?",
            "Do you have any budget constraints?"
        ]
        
    def collect_hair_profile(self, user_input):
        questions = [
            "What's your hair type? (Straight, Wavy, or Curly)",
            "How would you describe your scalp? (Dry, Balanced, or Oily)",
            "What are your main hair concerns?",
            "What's your age group?",
            "Do you have any budget constraints?"
        ]
```

### 2. Concern Analysis Engine

#### Natural Language Processing
```python
class ConcernAnalyzer:
    def __init__(self):
        self.skin_concerns_map = {
            "acne": ["acne", "pimples", "breakouts", "blemishes"],
            "dryness": ["dry", "flaky", "tight", "dehydrated"],
            "oiliness": ["oily", "greasy", "shiny", "excess oil"],
            "aging": ["wrinkles", "fine lines", "aging", "sagging"],
            "pigmentation": ["dark spots", "pigmentation", "uneven tone", "melasma"],
            "pores": ["large pores", "blackheads", "whiteheads", "clogged pores"],
            "dark_circles": ["dark circles", "under eye", "puffy eyes"],
            "dull_skin": ["dull", "lackluster", "tired looking", "no glow"]
        }
        
        self.hair_concerns_map = {
            "damaged_hair": ["damaged", "brittle", "broken", "weak"],
            "dry_hair": ["dry hair", "frizzy", "coarse", "rough"],
            "hairfall": ["hair fall", "thinning", "hair loss", "shedding"],
            "dandruff": ["dandruff", "flakes", "itchy scalp", "dry scalp"],
            "oily_scalp": ["oily scalp", "greasy roots", "flat hair"],
            "dull_hair": ["dull hair", "lifeless", "no shine", "lackluster"],
            "split_ends": ["split ends", "damaged ends", "rough ends"]
        }
    
    def analyze_concerns(self, user_input, category):
        # Use AWS Bedrock to analyze and map concerns
        # Return structured concern data
        pass
```

### 3. Product Recommendation Algorithm

#### Multi-Factor Filtering System
```python
class ProductRecommendationEngine:
    def __init__(self, product_catalogue, reviews_data):
        self.products = product_catalogue
        self.reviews = reviews_data
    
    def recommend_products(self, customer_profile):
        # Step 1: Category filtering
        filtered_products = self.filter_by_category(customer_profile.detected_category)
        
        # Step 2: Concern-based filtering
        concern_matched = self.filter_by_concerns(filtered_products, customer_profile.concerns)
        
        # Step 3: Skin/Hair type matching
        type_matched = self.filter_by_type(concern_matched, customer_profile)
        
        # Step 4: Age-appropriate filtering
        age_appropriate = self.filter_by_age(type_matched, customer_profile.age_group)
        
        # Step 5: Budget filtering (if provided)
        budget_filtered = self.apply_budget_filter(age_appropriate, customer_profile.budget)
        
        # Step 6: Ranking and scoring
        ranked_products = self.rank_products(budget_filtered, customer_profile)
        
        return ranked_products[:5]  # Top 5 recommendations
    
    def rank_products(self, products, customer_profile):
        scoring_factors = {
            'concern_relevance': 0.4,
            'ingredient_match': 0.3,
            'review_score': 0.2,
            'age_appropriateness': 0.1
        }
        # Calculate composite scores and rank
        pass
```

### 4. Product Presentation System

#### Comprehensive Product Display
```python
class ProductPresenter:
    def __init__(self, llm_service, review_analyzer):
        self.llm_service = llm_service
        self.review_analyzer = review_analyzer
    
    def create_product_presentation(self, product, customer_profile):
        presentation = {
            'product_info': self.format_product_info(product),
            'nykaa_image': self.generate_nykaa_image_url(product),
            'nykaa_link': self.generate_nykaa_product_url(product),
            'relevant_reviews': self.get_filtered_reviews(product, customer_profile),
            'sales_pitch': self.generate_sales_pitch(product, customer_profile),
            'ingredient_benefits': self.explain_ingredients(product, customer_profile),
            'usage_instructions': self.generate_usage_guide(product)
        }
        return presentation
    
    def generate_sales_pitch(self, product, customer_profile):
        prompt = f"""
        Create a compelling sales pitch for this product:
        
        Product: {product.name} by {product.brand}
        Price: ₹{product.mrp}
        Key Ingredients: {product.ingredients}
        Addresses: {product.concerns}
        
        Customer Profile:
        - Age: {customer_profile.age_group}
        - Type: {customer_profile.skin_type or customer_profile.hair_type}
        - Main Concerns: {customer_profile.concerns}
        - Budget: {customer_profile.budget or 'Not specified'}
        
        Create a 2-3 sentence pitch that:
        1. Directly addresses their concerns
        2. Highlights key benefits
        3. Emphasizes value proposition
        4. Creates desire to purchase
        
        Keep it natural, persuasive, and customer-focused.
        """
        
        return self.llm_service.generate_text(prompt)
```

### 5. Review Integration & Filtering

#### Intelligent Review Selection
```python
class ReviewAnalyzer:
    def __init__(self, nlp_service):
        self.nlp_service = nlp_service
    
    def filter_reviews_for_customer(self, product_id, customer_profile):
        product_reviews = self.get_product_reviews(product_id)
        
        filtered_reviews = []
        for review in product_reviews:
            # Filter by sentiment (positive only)
            if review.sentiment != "Positive":
                continue
            
            # Filter by relevance to customer profile
            if self.is_relevant_to_customer(review, customer_profile):
                filtered_reviews.append(review)
        
        # Sort by relevance and rating
        return sorted(filtered_reviews, key=lambda r: (r.rating, r.relevance_score), reverse=True)[:3]
    
    def is_relevant_to_customer(self, review, customer_profile):
        relevance_factors = []
        
        # Age group match
        if review.reviewer_age_group == customer_profile.age_group:
            relevance_factors.append(0.3)
        
        # Skin/Hair type match
        if hasattr(customer_profile, 'skin_type') and review.skin_type == customer_profile.skin_type:
            relevance_factors.append(0.4)
        
        # Concern mention in review
        for concern in customer_profile.concerns:
            if concern.lower() in review.text.lower():
                relevance_factors.append(0.3)
        
        return sum(relevance_factors) > 0.5
```

### 6. Nykaa Integration

#### Image and Link Generation
```python
class NykaaIntegration:
    def __init__(self):
        self.base_url = "https://www.nykaa.com"
    
    def generate_product_image_url(self, product):
        # Generate Nykaa product image URL
        # Format: https://www.nykaa.com/productimages/{product_id}/1.jpg
        return f"{self.base_url}/productimages/{product.product_id}/1.jpg"
    
    def generate_product_page_url(self, product):
        # Generate Nykaa product page URL
        # Format: https://www.nykaa.com/{brand-name}/{product-name}/p/{product_id}
        brand_slug = product.brand_name.lower().replace(' ', '-')
        product_slug = product.product_name.lower().replace(' ', '-')
        return f"{self.base_url}/{brand_slug}/{product_slug}/p/{product.product_id}"
    
    def create_product_card_html(self, product, presentation_data):
        return f"""
        <div class="product-card">
            <img src="{presentation_data['nykaa_image']}" alt="{product.name}" class="product-image">
            <h3>{product.name}</h3>
            <p class="brand">{product.brand}</p>
            <p class="price">₹{product.mrp}</p>
            <p class="sales-pitch">{presentation_data['sales_pitch']}</p>
            <div class="reviews">
                {self.format_reviews(presentation_data['relevant_reviews'])}
            </div>
            <a href="{presentation_data['nykaa_link']}" target="_blank" class="buy-button">
                View on Nykaa
            </a>
        </div>
        """
```

### 7. Budget Handling Logic

#### Smart Budget Processing
```python
class BudgetHandler:
    def process_budget_input(self, budget_input):
        if not budget_input or budget_input.lower() in ['no', 'none', 'no constraints']:
            return {'has_budget': False, 'show_top_sellers': True}
        
        # Extract budget amount using NLP
        budget_amount = self.extract_budget_amount(budget_input)
        
        if budget_amount:
            return {
                'has_budget': True,
                'max_amount': budget_amount,
                'show_top_sellers': False
            }
        else:
            # Handle descriptive budget (tight, limited, etc.)
            return self.handle_descriptive_budget(budget_input)
    
    def extract_budget_amount(self, text):
        # Use regex to find currency amounts
        import re
        patterns = [
            r'₹\s*(\d+(?:,\d+)*)',
            r'(\d+(?:,\d+)*)\s*rupees?',
            r'under\s*₹?\s*(\d+(?:,\d+)*)',
            r'below\s*₹?\s*(\d+(?:,\d+)*)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return int(match.group(1).replace(',', ''))
        
        return None
    
    def get_top_sellers(self, category, subcategory=None):
        # Return top-selling products when no budget specified
        # Sort by review ratings and sales volume
        pass
```

## Implementation Flow

### 1. User Journey Example
```
1. AI: "Hello! I'm your personal beauty consultant..."
2. User: "I have really dry skin and it's getting worse"
3. AI: [Detects: Skin category, Concern: Dryness]
   "I understand dry skin can be frustrating! Let me help you find the perfect products. 
    What's your skin type - would you say it's dry, oily, combination, or balanced?"
4. User: "Definitely dry, and I'm 28"
5. AI: [Collects: Age group - Young Adults, Skin type - Dry]
   "Perfect! Do you have any budget constraints for skincare products?"
6. User: "I can spend up to ₹2000"
7. AI: [Processes budget, generates recommendations]
   "Great! I've found some excellent products for dry skin within your budget..."
```

### 2. Technical Integration Points
- **AWS Bedrock**: Conversation handling, concern analysis, sales pitch generation
- **Product Database**: Filtering and matching algorithms
- **Review System**: Sentiment analysis and relevance scoring
- **Nykaa API**: Image and link generation
- **UI Components**: Product cards, review displays, conversation interface

### 3. Success Metrics
- **Accuracy**: 85%+ correct concern detection
- **Relevance**: 90%+ customer satisfaction with recommendations
- **Conversion**: Clear path to Nykaa product pages
- **Engagement**: Natural conversation flow maintenance

## Next Steps for Implementation
1. Set up AWS Bedrock conversation engine
2. Implement concern analysis algorithms
3. Build product recommendation system
4. Create Nykaa integration layer
5. Design product presentation components
6. Test with sample data and conversations
