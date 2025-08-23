# Budget Handling Logic

## Overview
This document defines how the AI virtual salesperson handles customer budget constraints, from detection to product filtering and alternative suggestions.

## Budget Detection System

### 1. Budget Question Strategy
```python
class BudgetDetector:
    def __init__(self):
        self.budget_question = "Do you have any budget constraints?"
        self.follow_up_questions = [
            "What's your budget range for these products?",
            "Are you looking for budget-friendly options?",
            "What would you like to spend on your beauty routine?"
        ]
    
    def ask_budget_question(self, conversation_context):
        # Ask at appropriate time in conversation
        if conversation_context.profile_completion > 0.7:
            return self.budget_question
        
        return None
    
    def detect_budget_mention(self, user_input):
        budget_indicators = [
            'budget', 'price', 'cost', 'expensive', 'cheap', 'affordable',
            'spend', 'money', 'rupees', '₹', 'under', 'below', 'maximum'
        ]
        
        return any(indicator in user_input.lower() for indicator in budget_indicators)
```

### 2. Budget Response Analysis
```python
class BudgetAnalyzer:
    def __init__(self, llm_service):
        self.llm_service = llm_service
    
    def analyze_budget_response(self, user_response):
        # Use LLM to understand budget intent
        analysis_prompt = f"""
        Analyze this customer's budget response and extract key information:
        
        Customer response: "{user_response}"
        
        Determine:
        1. Has budget constraints: Yes/No
        2. Specific amount mentioned: Extract number if any
        3. Budget type: specific_amount/range/descriptive/no_constraints
        4. Budget sentiment: tight/moderate/flexible/luxury
        
        Return as JSON:
        {{
            "has_constraints": boolean,
            "amount": number or null,
            "type": "specific_amount|range|descriptive|no_constraints",
            "sentiment": "tight|moderate|flexible|luxury",
            "raw_response": "original text"
        }}
        """
        
        return self.llm_service.generate_structured_response(analysis_prompt)
    
    def extract_budget_amount(self, text):
        import re
        
        # Pattern matching for Indian currency
        patterns = [
            r'₹\s*(\d+(?:,\d+)*)',  # ₹1000, ₹1,000
            r'(\d+(?:,\d+)*)\s*rupees?',  # 1000 rupees
            r'under\s*₹?\s*(\d+(?:,\d+)*)',  # under ₹1000
            r'below\s*₹?\s*(\d+(?:,\d+)*)',  # below 1000
            r'maximum\s*₹?\s*(\d+(?:,\d+)*)',  # maximum ₹1000
            r'up\s*to\s*₹?\s*(\d+(?:,\d+)*)',  # up to ₹1000
            r'around\s*₹?\s*(\d+(?:,\d+)*)',  # around ₹1000
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                amount_str = match.group(1).replace(',', '')
                return int(amount_str)
        
        return None
    
    def handle_descriptive_budget(self, description):
        budget_mapping = {
            'tight': {'max': 1000, 'preference': 'budget_friendly'},
            'limited': {'max': 1500, 'preference': 'value_for_money'},
            'moderate': {'max': 3000, 'preference': 'mid_range'},
            'flexible': {'max': 5000, 'preference': 'quality_focused'},
            'no_limit': {'max': None, 'preference': 'premium'}
        }
        
        description_lower = description.lower()
        
        for budget_type, constraints in budget_mapping.items():
            if budget_type in description_lower:
                return constraints
        
        # Default to moderate if unclear
        return budget_mapping['moderate']
```

## Budget Application System

### 1. Product Filtering Logic
```python
class BudgetProductFilter:
    def __init__(self):
        self.price_categories = {
            'budget': {'min': 0, 'max': 500},
            'affordable': {'min': 501, 'max': 1000},
            'mid_range': {'min': 1001, 'max': 2500},
            'premium': {'min': 2501, 'max': 5000},
            'luxury': {'min': 5001, 'max': float('inf')}
        }
    
    def filter_by_budget(self, products, budget_constraints):
        if not budget_constraints.get('has_constraints'):
            # No budget constraints - show top sellers
            return self.get_top_sellers(products)
        
        max_amount = budget_constraints.get('amount')
        if max_amount:
            return [p for p in products if p.mrp <= max_amount]
        
        # Handle descriptive budget
        sentiment = budget_constraints.get('sentiment', 'moderate')
        price_range = self.get_price_range_for_sentiment(sentiment)
        
        return [p for p in products if price_range['min'] <= p.mrp <= price_range['max']]
    
    def get_top_sellers(self, products):
        # When no budget specified, show top-rated products
        return sorted(products, key=lambda p: (p.average_rating, p.review_count), reverse=True)
    
    def get_price_range_for_sentiment(self, sentiment):
        sentiment_mapping = {
            'tight': self.price_categories['budget'],
            'moderate': self.price_categories['affordable'],
            'flexible': self.price_categories['mid_range'],
            'luxury': self.price_categories['premium']
        }
        
        return sentiment_mapping.get(sentiment, self.price_categories['affordable'])
```

### 2. Budget-Aware Recommendations
```python
class BudgetRecommendationEngine:
    def __init__(self, product_filter, alternative_finder):
        self.filter = product_filter
        self.alternative_finder = alternative_finder
    
    def recommend_with_budget(self, products, customer_profile, budget_constraints):
        # Filter products by budget
        budget_filtered = self.filter.filter_by_budget(products, budget_constraints)
        
        if len(budget_filtered) < 3:
            # Not enough options in budget - suggest alternatives
            return self.handle_insufficient_options(products, budget_constraints, customer_profile)
        
        # Rank filtered products
        ranked_products = self.rank_by_value(budget_filtered, customer_profile)
        
        return {
            'primary_recommendations': ranked_products[:3],
            'budget_info': self.calculate_budget_summary(ranked_products, budget_constraints),
            'alternatives': self.get_budget_alternatives(products, budget_constraints)
        }
    
    def handle_insufficient_options(self, all_products, budget_constraints, customer_profile):
        # Suggest budget increase or alternative approach
        closest_options = self.find_closest_price_options(all_products, budget_constraints)
        
        return {
            'message': self.generate_budget_guidance_message(budget_constraints, closest_options),
            'closest_options': closest_options,
            'budget_alternatives': self.suggest_budget_alternatives(budget_constraints),
            'phased_approach': self.suggest_phased_purchase(all_products, budget_constraints)
        }
    
    def generate_budget_guidance_message(self, budget_constraints, closest_options):
        max_budget = budget_constraints.get('amount', 0)
        closest_price = min(closest_options, key=lambda p: p.mrp).mrp if closest_options else 0
        
        if closest_price > max_budget:
            difference = closest_price - max_budget
            return f"""
            I understand your budget is ₹{max_budget}. The closest option for your needs is ₹{closest_price} 
            (₹{difference} more). Would you like to:
            1. See budget-friendly alternatives that might work
            2. Consider a phased approach to build your routine
            3. Look at multi-purpose products to maximize value
            """
        
        return "Let me find the best options within your budget!"
```

### 3. Alternative Suggestion System
```python
class BudgetAlternativeFinder:
    def __init__(self):
        self.alternative_strategies = [
            'lower_price_same_brand',
            'different_brand_same_function',
            'multi_purpose_products',
            'smaller_sizes',
            'drugstore_alternatives'
        ]
    
    def find_alternatives(self, target_product, budget_constraints, all_products):
        alternatives = []
        
        for strategy in self.alternative_strategies:
            strategy_alternatives = self.apply_strategy(strategy, target_product, budget_constraints, all_products)
            alternatives.extend(strategy_alternatives)
        
        # Remove duplicates and rank by relevance
        unique_alternatives = list({p.product_id: p for p in alternatives}.values())
        return sorted(unique_alternatives, key=lambda p: p.mrp)[:5]
    
    def apply_strategy(self, strategy, target_product, budget_constraints, all_products):
        max_budget = budget_constraints.get('amount', float('inf'))
        
        if strategy == 'lower_price_same_brand':
            return [p for p in all_products 
                   if p.brand == target_product.brand 
                   and p.canonical_l3 == target_product.canonical_l3 
                   and p.mrp <= max_budget]
        
        elif strategy == 'different_brand_same_function':
            return [p for p in all_products 
                   if p.canonical_l3 == target_product.canonical_l3 
                   and p.mrp <= max_budget 
                   and p.brand != target_product.brand]
        
        elif strategy == 'multi_purpose_products':
            # Find products that address multiple concerns
            return [p for p in all_products 
                   if len(p.concerns.split(',')) > 1 
                   and p.mrp <= max_budget]
        
        return []
    
    def suggest_value_maximization(self, budget_amount, customer_concerns):
        suggestions = []
        
        # Prioritize essential products
        essential_products = self.get_essential_products_for_concerns(customer_concerns)
        essential_cost = sum(p.mrp for p in essential_products)
        
        if essential_cost <= budget_amount:
            remaining_budget = budget_amount - essential_cost
            suggestions.append({
                'approach': 'essentials_first',
                'products': essential_products,
                'remaining_budget': remaining_budget,
                'message': f"Start with essentials (₹{essential_cost}), then add treatments with remaining ₹{remaining_budget}"
            })
        
        # Suggest phased approach
        phases = self.create_budget_phases(customer_concerns, budget_amount)
        suggestions.append({
            'approach': 'phased_purchase',
            'phases': phases,
            'message': "Build your routine gradually with this phased approach"
        })
        
        return suggestions
```

### 4. Top Sellers System (No Budget Constraints)
```python
class TopSellerEngine:
    def __init__(self, analytics_service):
        self.analytics = analytics_service
    
    def get_top_sellers(self, category, customer_profile):
        # When customer has no budget constraints, show top performers
        
        # Get products for category
        category_products = self.get_category_products(category, customer_profile)
        
        # Rank by multiple factors
        top_sellers = self.rank_by_popularity(category_products, customer_profile)
        
        return {
            'top_sellers': top_sellers[:5],
            'ranking_factors': ['customer_ratings', 'review_count', 'repurchase_rate', 'expert_recommendations'],
            'message': "Since you don't have budget constraints, here are our top-rated products for your needs!"
        }
    
    def rank_by_popularity(self, products, customer_profile):
        def calculate_popularity_score(product):
            # Weighted scoring system
            rating_score = (product.average_rating / 5.0) * 0.3
            review_score = min(product.review_count / 1000, 1.0) * 0.25
            concern_match = self.calculate_concern_match(product, customer_profile.concerns) * 0.25
            age_relevance = self.calculate_age_relevance(product, customer_profile.age_group) * 0.2
            
            return rating_score + review_score + concern_match + age_relevance
        
        return sorted(products, key=calculate_popularity_score, reverse=True)
    
    def calculate_concern_match(self, product, customer_concerns):
        product_concerns = set(product.concerns.lower().split(','))
        customer_concerns_set = set(concern.lower() for concern in customer_concerns)
        
        if not customer_concerns_set:
            return 0.5  # Neutral score if no concerns specified
        
        overlap = len(product_concerns.intersection(customer_concerns_set))
        return overlap / len(customer_concerns_set)
```

### 5. Budget Communication System
```python
class BudgetCommunicator:
    def __init__(self, llm_service):
        self.llm_service = llm_service
    
    def generate_budget_response(self, budget_analysis, recommendations):
        if not budget_analysis.get('has_constraints'):
            return self.generate_no_budget_response(recommendations)
        
        budget_amount = budget_analysis.get('amount')
        if budget_amount:
            return self.generate_specific_budget_response(budget_amount, recommendations)
        else:
            return self.generate_descriptive_budget_response(budget_analysis, recommendations)
    
    def generate_no_budget_response(self, recommendations):
        return f"""
        Perfect! Since you don't have specific budget constraints, I can show you our absolute best products for your needs. 
        Here are our top-rated recommendations that customers love:
        
        {self.format_recommendations(recommendations['top_sellers'])}
        
        These are our most popular products with excellent reviews and proven results!
        """
    
    def generate_specific_budget_response(self, budget_amount, recommendations):
        total_cost = sum(p.mrp for p in recommendations['primary_recommendations'])
        
        if total_cost <= budget_amount:
            savings = budget_amount - total_cost
            return f"""
            Great news! I found excellent products within your ₹{budget_amount} budget:
            
            {self.format_recommendations(recommendations['primary_recommendations'])}
            
            Total: ₹{total_cost} (₹{savings} under budget!)
            """
        else:
            return f"""
            I've found some great options close to your ₹{budget_amount} budget. 
            Let me show you a few approaches:
            
            {self.format_budget_alternatives(recommendations)}
            """
    
    def generate_value_proposition_message(self, product, budget_context):
        prompt = f"""
        Create a value-focused message for this product considering the customer's budget:
        
        Product: {product.name} - ₹{product.mrp}
        Customer Budget Context: {budget_context}
        
        Emphasize:
        1. Value for money
        2. Cost per use
        3. Long-term benefits
        4. Why it's worth the investment
        
        Keep it encouraging and helpful, not pushy.
        """
        
        return self.llm_service.generate_text(prompt)
```

## Implementation Flow Examples

### 1. Budget Detection Flow
```
AI: "Do you have any budget constraints?"

Scenario A - Specific Amount:
User: "I can spend up to ₹2000"
AI: [Filters products ≤ ₹2000] "Perfect! Here are excellent options within ₹2000..."

Scenario B - No Constraints:
User: "No, not really"
AI: [Shows top sellers] "Great! Here are our top-rated products for your needs..."

Scenario C - Descriptive:
User: "I'm on a tight budget"
AI: [Filters budget-friendly options] "I understand! Here are some excellent budget-friendly options..."
```

### 2. Budget Optimization Flow
```
User: "These seem expensive"
AI: "I understand! Let me show you some alternatives:
     1. Budget-friendly options with similar benefits
     2. Multi-purpose products for better value
     3. A phased approach to build your routine gradually"
```

### 3. Value Communication
```
AI: "This serum is ₹1500, which works out to just ₹16 per day over 3 months. 
    Given your anti-aging concerns, the peptides and retinol make it excellent value 
    compared to salon treatments!"
```

## Success Metrics
- **Budget Compliance**: 95%+ recommendations stay within stated budget
- **Alternative Acceptance**: 70%+ customers accept budget alternatives when needed
- **Value Communication**: 80%+ customers understand cost-per-use explanations
- **No-Budget Conversion**: 60%+ customers without budget constraints make purchases
