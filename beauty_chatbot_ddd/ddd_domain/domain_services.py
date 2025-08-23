"""
Domain Services for Concern-Based Chat Domain
"""
from typing import List, Dict, Optional
import re
from collections import defaultdict

from value_objects import (
    MessageContent, ConcernType, ConfidenceScore, Keyword, Timestamp
)
from entities import DetectedConcern, Ingredient, BotResponse, Product, Review
from aggregates import ConcernKnowledgeBase


class ConcernDetectionService:
    """
    Domain Service: Analyzes user messages to identify beauty concerns
    """
    
    def __init__(self, knowledge_base: ConcernKnowledgeBase):
        self.knowledge_base = knowledge_base
        self.min_confidence_threshold = 0.4  # Lowered from 0.6 to be more sensitive
    
    def detect_concerns(self, message: MessageContent) -> List[DetectedConcern]:
        """Detect beauty concerns from user message"""
        text = message.get_clean_text()
        keywords = self.extract_keywords(text)
        
        if not keywords:
            return []
        
        # Find matching concerns
        concern_scores = self._calculate_concern_scores(keywords)
        detected_concerns = []
        
        for concern_type, score in concern_scores.items():
            if score >= self.min_confidence_threshold:
                detected_concern = DetectedConcern(
                    detected_concern_id="",
                    concern_type=concern_type,
                    confidence_score=ConfidenceScore(score),
                    extracted_keywords=keywords,
                    detected_at=Timestamp.now()
                )
                detected_concerns.append(detected_concern)
        
        # Sort by confidence score (highest first)
        detected_concerns.sort(key=lambda dc: dc.confidence_score.value, reverse=True)
        
        # Limit to top 3 concerns to avoid overwhelming responses
        return detected_concerns[:3]
    
    def extract_keywords(self, text: str) -> List[Keyword]:
        """Extract relevant keywords from text"""
        # Simple keyword extraction - in production, this would be more sophisticated
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'have', 'has', 'had', 'my', 'i', 'me', 'you', 'your'}
        filtered_words = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Create keywords with weights
        keywords = []
        word_counts = defaultdict(int)
        
        for word in filtered_words:
            word_counts[word] += 1
        
        for word, count in word_counts.items():
            # Weight based on frequency and position (simple heuristic)
            weight = min(count * 1.5, 5.0)  # Cap at 5.0
            keywords.append(Keyword(word, weight))
        
        return keywords
    
    def calculate_confidence(self, keywords: List[Keyword], concern_type: ConcernType) -> ConfidenceScore:
        """Calculate confidence score for a specific concern"""
        concern_id = concern_type.name.lower().replace(" ", "_")
        concern_keywords = self.knowledge_base.concern_keywords.get(concern_id, [])
        
        if not concern_keywords:
            return ConfidenceScore(0.0)
        
        # Calculate matching score
        keyword_words = [kw.word.lower() for kw in keywords]
        concern_keyword_words = [ckw.word.lower() for ckw in concern_keywords]
        
        matches = 0
        total_weight = 0
        
        for keyword in keywords:
            if keyword.word.lower() in concern_keyword_words:
                matches += 1
                total_weight += keyword.weight
        
        if matches == 0:
            return ConfidenceScore(0.0)
        
        # Improved confidence calculation
        # Base score: percentage of concern keywords matched
        base_score = matches / len(concern_keywords)
        
        # Bonus for multiple matches
        match_bonus = min(matches * 0.2, 0.4)  # Up to 40% bonus
        
        # Weight bonus from keyword importance
        weight_bonus = min(total_weight / 10.0, 0.3)  # Max 30% bonus from weights
        
        final_score = min(base_score + match_bonus + weight_bonus, 1.0)
        return ConfidenceScore(final_score)
    
    def _calculate_concern_scores(self, keywords: List[Keyword]) -> Dict[ConcernType, float]:
        """Calculate scores for all concerns"""
        scores = {}
        
        for concern_type in self.knowledge_base.get_all_concerns():
            confidence = self.calculate_confidence(keywords, concern_type)
            if confidence.value > 0:
                scores[concern_type] = confidence.value
        
        return scores


class ResponseGenerationService:
    """
    Domain Service: Creates comprehensive responses for detected concerns
    """
    
    def __init__(self, knowledge_base: ConcernKnowledgeBase):
        self.knowledge_base = knowledge_base
        self.max_response_length = 500
    
    def generate_concern_response(self, concerns: List[DetectedConcern]) -> BotResponse:
        """Generate comprehensive response for detected concerns"""
        if not concerns:
            raise ValueError("Cannot generate response without concerns")
        
        # Focus on the highest confidence concern
        primary_concern = concerns[0]
        concern_id = primary_concern.concern_type.name.lower().replace(" ", "_")
        
        # Build response components
        response_parts = []
        
        # 1. Educational content
        educational_content = self.knowledge_base.get_educational_content(concern_id)
        if educational_content:
            response_parts.append(self.format_educational_content(educational_content))
        
        # 2. Ingredient recommendations
        ingredients = self.knowledge_base.get_ingredients_for_concern(concern_id)
        if ingredients:
            response_parts.append(self.format_ingredient_recommendations(ingredients[:3]))
        
        # 3. Natural remedies placeholder (would integrate with natural remedies service)
        natural_remedies = self._get_natural_remedies_for_concern(primary_concern.concern_type)
        
        # Combine response parts
        response_content = "\n\n".join(response_parts)
        
        # Ensure response isn't too long
        if len(response_content) > self.max_response_length:
            response_content = response_content[:self.max_response_length - 3] + "..."
        
        return BotResponse(
            response_id="",
            content=response_content,
            concerns_addressed=[c.concern_type for c in concerns],
            products_recommended=[],  # Would be populated by product service
            educational_content=educational_content,
            natural_remedies=natural_remedies
        )
    
    def format_educational_content(self, content) -> str:
        """Format educational content for response"""
        return f"**About {content.title}:**\n{content.description}\n\n{content.explanation}"
    
    def format_ingredient_recommendations(self, ingredients: List[Ingredient]) -> str:
        """Format ingredient recommendations"""
        if not ingredients:
            return ""
        
        parts = ["**Key ingredients to look for:**"]
        
        for ingredient in ingredients:
            benefits_text = ", ".join([b.description for b in ingredient.benefits[:2]])
            parts.append(f"• **{ingredient.name}**: {benefits_text}")
        
        return "\n".join(parts)
    
    def combine_product_and_remedy_recommendations(self, products: List[Product], remedies: List[str]) -> str:
        """Combine product and natural remedy recommendations"""
        parts = []
        
        if products:
            parts.append("**Recommended Products:**")
            for product in products[:3]:
                parts.append(f"• {product.name} - ${product.price:.2f} ({product.rating}/5 stars)")
        
        if remedies:
            parts.append("\n**Natural Remedies:**")
            for remedy in remedies[:2]:
                parts.append(f"• {remedy}")
        
        return "\n".join(parts)
    
    def _get_natural_remedies_for_concern(self, concern_type: ConcernType) -> List[str]:
        """Get natural remedies for a concern (placeholder)"""
        # This would integrate with a natural remedies service
        remedies_map = {
            "acne": ["Honey and cinnamon mask", "Tea tree oil spot treatment"],
            "dryness": ["Oatmeal and honey mask", "Coconut oil moisturizer"],
            "oily": ["Clay mask with bentonite", "Green tea toner"],
            "aging": ["Vitamin C serum (DIY)", "Retinol alternatives"],
            "dark_spots": ["Lemon and honey treatment", "Turmeric mask"],
            "sensitive": ["Aloe vera gel", "Chamomile compress"],
            "dull": ["Exfoliating sugar scrub", "Vitamin E oil"],
            "hair_loss": ["Rosemary oil massage", "Onion juice treatment"],
            "dandruff": ["Apple cider vinegar rinse", "Tea tree oil shampoo"],
            "frizzy_hair": ["Coconut oil mask", "Egg white treatment"]
        }
        
        concern_name = concern_type.name.lower().replace(" ", "_")
        return remedies_map.get(concern_name, [])


class ConcernMappingService:
    """
    Domain Service: Maps detected concerns to ingredients and products
    """
    
    def __init__(self, knowledge_base: ConcernKnowledgeBase):
        self.knowledge_base = knowledge_base
    
    def map_concerns_to_ingredients(self, concerns: List[DetectedConcern]) -> List[Ingredient]:
        """Map detected concerns to relevant ingredients"""
        all_ingredients = []
        
        for concern in concerns:
            concern_id = concern.concern_type.name.lower().replace(" ", "_")
            ingredients = self.knowledge_base.get_ingredients_for_concern(concern_id)
            
            # Weight ingredients by concern confidence
            for ingredient in ingredients:
                # In a more sophisticated implementation, we'd track ingredient scores
                all_ingredients.append(ingredient)
        
        # Remove duplicates while preserving order
        unique_ingredients = []
        seen_ids = set()
        
        for ingredient in all_ingredients:
            if ingredient.ingredient_id not in seen_ids:
                unique_ingredients.append(ingredient)
                seen_ids.add(ingredient.ingredient_id)
        
        return unique_ingredients
    
    def find_relevant_products(self, ingredients: List[Ingredient]) -> List[str]:
        """Find product IDs that contain the specified ingredients"""
        # This would integrate with the product catalog service
        # For now, return placeholder product IDs
        return [f"product_{i}" for i in range(min(len(ingredients), 5))]
    
    def prioritize_recommendations(self, products: List[Product], user_profile: Optional[Dict] = None) -> List[Product]:
        """Prioritize product recommendations based on user profile"""
        if not user_profile:
            # Default prioritization by rating
            return sorted(products, key=lambda p: p.rating, reverse=True)
        
        # Prioritize based on user preferences
        prioritized = products.copy()
        
        # Budget filtering
        budget_max = user_profile.get('budget_max', float('inf'))
        prioritized = [p for p in prioritized if p.price <= budget_max]
        
        # Sort by rating within budget
        prioritized.sort(key=lambda p: p.rating, reverse=True)
        
        return prioritized
    
    def calculate_ingredient_effectiveness(self, ingredient: Ingredient, concern: DetectedConcern) -> float:
        """Calculate how effective an ingredient is for a specific concern"""
        # Simple effectiveness calculation based on ingredient benefits
        effectiveness_scores = []
        
        for benefit in ingredient.benefits:
            # Check if benefit description relates to the concern
            concern_keywords = [kw.word.lower() for kw in concern.extracted_keywords]
            benefit_words = benefit.description.lower().split()
            
            matches = sum(1 for word in benefit_words if word in concern_keywords)
            if matches > 0:
                effectiveness_scores.append(benefit.effectiveness * (matches / len(benefit_words)))
        
        return max(effectiveness_scores) if effectiveness_scores else 0.0
    
    def get_complementary_ingredients(self, primary_ingredients: List[Ingredient]) -> List[Ingredient]:
        """Find ingredients that work well with the primary ingredients"""
        # This would use a more sophisticated algorithm in production
        # For now, return ingredients from the same categories
        
        primary_concerns = set()
        for ingredient in primary_ingredients:
            primary_concerns.update(ingredient.concern_types)
        
        complementary = []
        all_ingredients = self.knowledge_base.get_all_ingredients()
        
        for ingredient in all_ingredients:
            if ingredient not in primary_ingredients:
                # Check if ingredient addresses similar concerns
                if any(concern in ingredient.concern_types for concern in primary_concerns):
                    complementary.append(ingredient)
        
        return complementary[:3]  # Limit to top 3 complementary ingredients


class ConversationAnalyticsService:
    """
    Domain Service: Analyzes conversation patterns and effectiveness
    """
    
    def __init__(self):
        self.conversation_metrics = defaultdict(int)
    
    def analyze_concern_detection_accuracy(self, conversations: List) -> Dict[str, float]:
        """Analyze the accuracy of concern detection"""
        # This would analyze conversation outcomes to measure accuracy
        return {
            "overall_accuracy": 0.85,
            "high_confidence_accuracy": 0.92,
            "medium_confidence_accuracy": 0.78,
            "low_confidence_accuracy": 0.61
        }
    
    def get_most_common_concerns(self, conversations: List) -> List[tuple]:
        """Get the most commonly detected concerns"""
        concern_counts = defaultdict(int)
        
        for conversation in conversations:
            for concern in conversation.detected_concerns:
                concern_counts[concern.concern_type.name] += 1
        
        return sorted(concern_counts.items(), key=lambda x: x[1], reverse=True)
    
    def calculate_response_effectiveness(self, conversations: List) -> float:
        """Calculate how effective responses are based on user engagement"""
        # This would analyze follow-up messages and user satisfaction
        # For now, return a placeholder value
        return 0.78
    
    def get_conversation_statistics(self, conversations: List) -> Dict[str, any]:
        """Get comprehensive conversation statistics"""
        if not conversations:
            return {}
        
        total_conversations = len(conversations)
        total_messages = sum(len(conv.messages) for conv in conversations)
        total_concerns = sum(len(conv.detected_concerns) for conv in conversations)
        
        return {
            "total_conversations": total_conversations,
            "total_messages": total_messages,
            "total_concerns_detected": total_concerns,
            "average_messages_per_conversation": total_messages / total_conversations,
            "average_concerns_per_conversation": total_concerns / total_conversations,
            "most_common_concerns": self.get_most_common_concerns(conversations)[:5]
        }
