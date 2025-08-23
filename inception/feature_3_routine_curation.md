# Feature 3: Personalized Beauty Routine Curation

## Overview
This feature creates customized beauty routines (skincare/haircare/makeup) based on customer profile, concerns, age, and budget, with product recommendations and visual presentations.

## Feature Components

### 1. Routine Request Detection

#### Trigger Identification System
```python
class RoutineRequestDetector:
    def __init__(self):
        self.routine_keywords = {
            'skincare': ['skincare routine', 'daily routine', 'morning routine', 'night routine', 'skin regimen'],
            'haircare': ['hair routine', 'hair care', 'hair regimen', 'hair schedule'],
            'makeup': ['makeup routine', 'makeup look', 'daily makeup', 'makeup regimen']
        }
        
        self.routine_triggers = [
            'create routine', 'build routine', 'suggest routine',
            'daily regimen', 'step by step', 'complete routine',
            'morning and night', 'what should I use', 'routine for'
        ]
    
    def detect_routine_request(self, user_input, conversation_context):
        # Check for explicit routine requests
        for trigger in self.routine_triggers:
            if trigger in user_input.lower():
                return self.determine_routine_type(user_input)
        
        # Check context - offer routine after multiple product recommendations
        if conversation_context.product_recommendations_count >= 3:
            return 'suggest_routine'
        
        return None
    
    def determine_routine_type(self, user_input):
        for routine_type, keywords in self.routine_keywords.items():
            if any(keyword in user_input.lower() for keyword in keywords):
                return routine_type
        
        return 'general'  # Let customer choose
```

### 2. Routine Architecture System

#### Comprehensive Routine Structure
```python
class RoutineArchitect:
    def __init__(self):
        self.routine_templates = {
            'skincare': {
                'morning': ['cleanser', 'toner', 'serum', 'moisturizer', 'sunscreen'],
                'evening': ['cleanser', 'treatment', 'serum', 'moisturizer', 'night_cream']
            },
            'haircare': {
                'weekly': ['shampoo', 'conditioner', 'hair_mask', 'leave_in_treatment'],
                'daily': ['leave_in_conditioner', 'styling_product', 'hair_oil']
            },
            'makeup': {
                'daily': ['primer', 'foundation', 'concealer', 'powder', 'blush', 'mascara', 'lipstick'],
                'evening': ['primer', 'foundation', 'concealer', 'powder', 'contour', 'eyeshadow', 'eyeliner', 'mascara', 'lipstick']
            }
        }
    
    def create_personalized_routine(self, customer_profile, routine_type):
        base_template = self.routine_templates[routine_type]
        
        # Customize based on customer profile
        personalized_routine = self.customize_routine(base_template, customer_profile)
        
        # Add product recommendations for each step
        routine_with_products = self.add_product_recommendations(personalized_routine, customer_profile)
        
        # Calculate total cost and adjust for budget
        budget_optimized_routine = self.optimize_for_budget(routine_with_products, customer_profile.budget)
        
        return budget_optimized_routine
    
    def customize_routine(self, base_template, customer_profile):
        customized = {}
        
        for time_period, steps in base_template.items():
            customized[time_period] = []
            
            for step in steps:
                # Customize based on concerns and type
                customized_step = self.customize_step(step, customer_profile)
                if customized_step:
                    customized[time_period].append(customized_step)
        
        return customized
    
    def customize_step(self, step, customer_profile):
        # Age-based customization
        if customer_profile.age_group == 'Teens (13-19)':
            if step in ['anti_aging_serum', 'retinol', 'intensive_treatment']:
                return None  # Skip advanced treatments for teens
        
        # Concern-based customization
        if 'acne' in customer_profile.concerns:
            if step == 'serum':
                return 'acne_treatment_serum'
        
        if 'aging' in customer_profile.concerns:
            if step == 'serum':
                return 'anti_aging_serum'
        
        return step
```

### 3. Product Matching Engine

#### Intelligent Product Selection for Routines
```python
class RoutineProductMatcher:
    def __init__(self, product_catalogue, recommendation_engine):
        self.products = product_catalogue
        self.recommender = recommendation_engine
    
    def match_products_to_routine(self, routine_structure, customer_profile):
        routine_with_products = {}
        
        for time_period, steps in routine_structure.items():
            routine_with_products[time_period] = []
            
            for step in steps:
                # Find suitable products for this step
                step_products = self.find_step_products(step, customer_profile)
                
                # Select best product for this step
                selected_product = self.select_best_product(step_products, customer_profile, step)
                
                routine_with_products[time_period].append({
                    'step': step,
                    'product': selected_product,
                    'alternatives': step_products[:3],  # Top 3 alternatives
                    'usage_instructions': self.get_usage_instructions(selected_product, step),
                    'step_explanation': self.explain_step_purpose(step, customer_profile)
                })
        
        return routine_with_products
    
    def find_step_products(self, step, customer_profile):
        # Map routine steps to product categories
        step_category_map = {
            'cleanser': 'Cleanser',
            'toner': 'Toner',
            'serum': 'Serum',
            'moisturizer': 'Moisturizer',
            'sunscreen': 'Sunscreen',
            'shampoo': 'Shampoo',
            'conditioner': 'Conditioner',
            'foundation': 'Foundation',
            'concealer': 'Concealer'
        }
        
        target_category = step_category_map.get(step)
        if not target_category:
            return []
        
        # Filter products by category and customer profile
        filtered_products = self.products.filter(
            canonical_l3=target_category,
            suitable_for_type=customer_profile.skin_type or customer_profile.hair_type,
            addresses_concerns=customer_profile.concerns
        )
        
        return self.recommender.rank_products(filtered_products, customer_profile)
    
    def explain_step_purpose(self, step, customer_profile):
        explanations = {
            'cleanser': f"Removes dirt, oil, and impurities. Essential for {customer_profile.skin_type} skin.",
            'toner': f"Balances skin pH and prepares for treatments. Helps with {', '.join(customer_profile.concerns)}.",
            'serum': f"Delivers concentrated active ingredients to target {', '.join(customer_profile.concerns)}.",
            'moisturizer': f"Hydrates and protects {customer_profile.skin_type} skin barrier.",
            'sunscreen': "Protects against UV damage and prevents premature aging."
        }
        
        return explanations.get(step, f"Important step for your {customer_profile.skin_type} skin routine.")
```

### 4. Routine Customization Engine

#### Interactive Routine Modification
```python
class RoutineCustomizer:
    def __init__(self, llm_service):
        self.llm_service = llm_service
    
    def handle_customization_request(self, routine, modification_request, customer_profile):
        modification_type = self.analyze_modification_request(modification_request)
        
        if modification_type == 'remove_step':
            return self.remove_routine_step(routine, modification_request)
        elif modification_type == 'add_step':
            return self.add_routine_step(routine, modification_request, customer_profile)
        elif modification_type == 'replace_product':
            return self.replace_product(routine, modification_request, customer_profile)
        elif modification_type == 'adjust_timing':
            return self.adjust_routine_timing(routine, modification_request)
        else:
            return self.handle_general_modification(routine, modification_request, customer_profile)
    
    def analyze_modification_request(self, request):
        request_lower = request.lower()
        
        if any(word in request_lower for word in ['remove', 'skip', 'don\'t need', 'without']):
            return 'remove_step'
        elif any(word in request_lower for word in ['add', 'include', 'also need', 'plus']):
            return 'add_step'
        elif any(word in request_lower for word in ['replace', 'instead of', 'substitute', 'different']):
            return 'replace_product'
        elif any(word in request_lower for word in ['morning only', 'evening only', 'twice a day']):
            return 'adjust_timing'
        else:
            return 'general'
    
    def generate_routine_alternatives(self, base_routine, customer_profile):
        alternatives = {
            'minimal': self.create_minimal_routine(base_routine, customer_profile),
            'comprehensive': self.create_comprehensive_routine(base_routine, customer_profile),
            'budget_friendly': self.create_budget_routine(base_routine, customer_profile),
            'time_efficient': self.create_quick_routine(base_routine, customer_profile)
        }
        
        return alternatives
    
    def create_minimal_routine(self, base_routine, customer_profile):
        # Essential steps only
        essential_steps = {
            'skincare': ['cleanser', 'moisturizer', 'sunscreen'],
            'haircare': ['shampoo', 'conditioner'],
            'makeup': ['foundation', 'mascara', 'lipstick']
        }
        
        routine_type = self.determine_routine_type(base_routine)
        essential = essential_steps.get(routine_type, [])
        
        minimal_routine = {}
        for time_period, steps in base_routine.items():
            minimal_routine[time_period] = [step for step in steps if step['step'] in essential]
        
        return minimal_routine
```

### 5. Budget Optimization System

#### Smart Budget Allocation
```python
class RoutineBudgetOptimizer:
    def __init__(self):
        self.priority_weights = {
            'cleanser': 0.2,
            'moisturizer': 0.25,
            'sunscreen': 0.2,
            'serum': 0.15,
            'treatment': 0.1,
            'toner': 0.1
        }
    
    def optimize_routine_for_budget(self, routine, budget_amount):
        if not budget_amount:
            return routine  # No budget constraints
        
        # Calculate current total cost
        total_cost = self.calculate_routine_cost(routine)
        
        if total_cost <= budget_amount:
            return routine  # Within budget
        
        # Need to optimize
        optimized_routine = self.reduce_routine_cost(routine, budget_amount)
        
        return optimized_routine
    
    def reduce_routine_cost(self, routine, target_budget):
        # Strategy 1: Replace expensive products with budget alternatives
        cost_reduced_routine = self.replace_with_alternatives(routine, target_budget)
        
        if self.calculate_routine_cost(cost_reduced_routine) <= target_budget:
            return cost_reduced_routine
        
        # Strategy 2: Remove non-essential steps
        essential_routine = self.remove_non_essential_steps(cost_reduced_routine, target_budget)
        
        return essential_routine
    
    def suggest_budget_phases(self, routine, budget_amount):
        # Suggest building routine in phases
        phases = {
            'phase_1': self.get_essential_products(routine, budget_amount * 0.4),
            'phase_2': self.get_treatment_products(routine, budget_amount * 0.3),
            'phase_3': self.get_enhancement_products(routine, budget_amount * 0.3)
        }
        
        return phases
    
    def calculate_cost_per_use(self, product, usage_frequency):
        # Calculate cost efficiency
        product_size = product.get('size_ml', 50)  # Default 50ml
        uses_per_ml = self.estimate_uses_per_ml(product.canonical_l3)
        total_uses = product_size * uses_per_ml
        
        return product.mrp / total_uses
```

### 6. Routine Presentation System

#### Visual Routine Display
```python
class RoutinePresenter:
    def __init__(self, nykaa_integration):
        self.nykaa = nykaa_integration
    
    def create_routine_presentation(self, routine, customer_profile):
        presentation = {
            'routine_overview': self.create_routine_overview(routine),
            'step_by_step_guide': self.create_step_guide(routine),
            'product_showcase': self.create_product_showcase(routine),
            'timing_guide': self.create_timing_guide(routine),
            'cost_breakdown': self.create_cost_breakdown(routine),
            'customization_options': self.get_customization_options(routine)
        }
        
        return presentation
    
    def create_routine_overview(self, routine):
        html = """
        <div class="routine-overview">
            <h2>Your Personalized Beauty Routine</h2>
            <div class="routine-summary">
        """
        
        for time_period, steps in routine.items():
            html += f"""
            <div class="time-period">
                <h3>{time_period.title()} Routine</h3>
                <div class="steps-count">{len(steps)} steps</div>
            </div>
            """
        
        html += "</div></div>"
        return html
    
    def create_step_guide(self, routine):
        html = '<div class="step-by-step-guide">'
        
        for time_period, steps in routine.items():
            html += f'<div class="time-period-guide"><h3>{time_period.title()}</h3>'
            
            for i, step_data in enumerate(steps, 1):
                product = step_data['product']
                html += f"""
                <div class="routine-step">
                    <div class="step-number">{i}</div>
                    <div class="step-content">
                        <h4>{step_data['step'].replace('_', ' ').title()}</h4>
                        <div class="product-info">
                            <img src="{self.nykaa.generate_product_image_url(product)}" 
                                 alt="{product.name}" class="product-thumb">
                            <div class="product-details">
                                <p class="product-name">{product.name}</p>
                                <p class="product-brand">{product.brand}</p>
                                <p class="product-price">₹{product.mrp}</p>
                            </div>
                        </div>
                        <p class="step-explanation">{step_data['step_explanation']}</p>
                        <p class="usage-instructions">{step_data['usage_instructions']}</p>
                        <a href="{self.nykaa.generate_product_page_url(product)}" 
                           target="_blank" class="product-link">View Product</a>
                    </div>
                </div>
                """
            
            html += '</div>'
        
        html += '</div>'
        return html
    
    def create_cost_breakdown(self, routine):
        total_cost = 0
        cost_by_period = {}
        
        for time_period, steps in routine.items():
            period_cost = sum(step['product'].mrp for step in steps)
            cost_by_period[time_period] = period_cost
            total_cost += period_cost
        
        html = f"""
        <div class="cost-breakdown">
            <h3>Investment Breakdown</h3>
            <div class="total-cost">Total: ₹{total_cost}</div>
            <div class="period-costs">
        """
        
        for period, cost in cost_by_period.items():
            html += f'<div class="period-cost">{period.title()}: ₹{cost}</div>'
        
        html += """
            </div>
            <div class="cost-notes">
                <p>💡 This is a one-time investment. Most products last 2-3 months.</p>
                <p>💰 Cost per day: ₹{:.2f}</p>
            </div>
        </div>
        """.format(total_cost / 90)  # Assuming 3-month usage
        
        return html
```

### 7. Routine Effectiveness Tracking

#### Success Metrics and Optimization
```python
class RoutineTracker:
    def __init__(self):
        self.routine_metrics = {}
    
    def track_routine_adoption(self, routine_id, customer_profile, adoption_data):
        if routine_id not in self.routine_metrics:
            self.routine_metrics[routine_id] = {
                'created_count': 0,
                'adopted_count': 0,
                'customization_requests': 0,
                'satisfaction_scores': [],
                'completion_rates': []
            }
        
        metrics = self.routine_metrics[routine_id]
        
        if adoption_data['action'] == 'created':
            metrics['created_count'] += 1
        elif adoption_data['action'] == 'adopted':
            metrics['adopted_count'] += 1
        elif adoption_data['action'] == 'customized':
            metrics['customization_requests'] += 1
    
    def analyze_routine_effectiveness(self, routine_type, customer_segment):
        # Analyze which routines work best for different customer segments
        effective_routines = []
        
        for routine_id, metrics in self.routine_metrics.items():
            adoption_rate = metrics['adopted_count'] / max(metrics['created_count'], 1)
            avg_satisfaction = sum(metrics['satisfaction_scores']) / max(len(metrics['satisfaction_scores']), 1)
            
            if adoption_rate > 0.7 and avg_satisfaction > 4.0:
                effective_routines.append(routine_id)
        
        return effective_routines
    
    def suggest_routine_improvements(self, routine_id):
        metrics = self.routine_metrics.get(routine_id, {})
        
        improvements = []
        
        if metrics.get('customization_requests', 0) > metrics.get('adopted_count', 0) * 0.5:
            improvements.append("Consider making routine more flexible by default")
        
        if len(metrics.get('satisfaction_scores', [])) > 0:
            avg_satisfaction = sum(metrics['satisfaction_scores']) / len(metrics['satisfaction_scores'])
            if avg_satisfaction < 3.5:
                improvements.append("Review product selections and step explanations")
        
        return improvements
```

## Implementation Flow

### 1. Routine Creation Journey
```
1. User: "Can you create a skincare routine for me?"
2. AI: "I'd love to create a personalized skincare routine for you! Based on your dry skin and concerns about aging, I'll design both morning and evening routines."
3. AI: [Generates routine with 5 morning steps, 6 evening steps]
4. AI: "Here's your routine with total cost ₹3,200. Would you like to see budget-friendly alternatives or modify any steps?"
5. User: "Can we make it under ₹2000?"
6. AI: [Optimizes routine] "Here's your budget-optimized routine for ₹1,850!"
```

### 2. Customization Example
```
User: "I don't have time for 6 steps in the morning"
AI: "I understand! Let me create a quick 3-step morning routine that still addresses your main concerns..."
```

### 3. Technical Integration Points
- **Product Database**: Routine-product matching
- **Budget Engine**: Cost optimization algorithms
- **Nykaa Integration**: Product images and links
- **AWS Bedrock**: Routine explanations and customizations
- **Analytics**: Routine effectiveness tracking

## Success Metrics
- **Adoption**: 60%+ customers adopt suggested routines
- **Satisfaction**: 85%+ satisfaction with routine recommendations
- **Customization**: Handle 90%+ customization requests successfully
- **Budget Compliance**: 95%+ routines stay within specified budgets
