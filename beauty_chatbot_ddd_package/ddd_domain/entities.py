"""
Entities for Concern-Based Chat Domain
"""
from dataclasses import dataclass, field
from typing import List, Optional
import uuid
from datetime import datetime

from value_objects import (
    ConversationId, MessageContent, ConcernType, ConfidenceScore,
    MessageType, Keyword, Benefit, SafetyRating, ProcessingStatus,
    ProductId, Timestamp
)


@dataclass
class Message:
    """Individual message in a conversation"""
    message_id: str
    content: MessageContent
    message_type: MessageType
    timestamp: Timestamp
    processing_status: ProcessingStatus = field(default_factory=lambda: ProcessingStatus("PENDING"))
    
    def __post_init__(self):
        if not self.message_id:
            self.message_id = str(uuid.uuid4())
    
    def mark_as_processed(self):
        """Mark message as successfully processed"""
        object.__setattr__(self, 'processing_status', ProcessingStatus("PROCESSED"))
    
    def mark_as_failed(self, error_message: str):
        """Mark message as failed with error"""
        object.__setattr__(self, 'processing_status', ProcessingStatus("FAILED", error_message))
    
    def is_user_message(self) -> bool:
        return self.message_type.is_user_message()
    
    def is_bot_message(self) -> bool:
        return self.message_type.is_bot_message()


@dataclass
class DetectedConcern:
    """Beauty concern detected from user input"""
    detected_concern_id: str
    concern_type: ConcernType
    confidence_score: ConfidenceScore
    extracted_keywords: List[Keyword]
    detected_at: Timestamp
    
    def __post_init__(self):
        if not self.detected_concern_id:
            self.detected_concern_id = str(uuid.uuid4())
        if not self.extracted_keywords:
            raise ValueError("DetectedConcern must have at least one keyword")
    
    def is_high_confidence(self) -> bool:
        return self.confidence_score.is_high_confidence()
    
    def get_primary_keywords(self) -> List[str]:
        """Get the most important keywords"""
        sorted_keywords = sorted(self.extracted_keywords, key=lambda k: k.weight, reverse=True)
        return [k.word for k in sorted_keywords[:3]]
    
    def matches_category(self, category: str) -> bool:
        return self.concern_type.category == category


@dataclass
class Ingredient:
    """Beauty ingredient that addresses concerns"""
    ingredient_id: str
    name: str
    benefits: List[Benefit]
    concern_types: List[ConcernType]
    safety_rating: SafetyRating
    
    def __post_init__(self):
        if not self.ingredient_id:
            self.ingredient_id = str(uuid.uuid4())
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("Ingredient name cannot be empty")
        if not self.benefits:
            raise ValueError("Ingredient must have at least one benefit")
    
    def addresses_concern(self, concern_type: ConcernType) -> bool:
        """Check if ingredient addresses a specific concern"""
        return concern_type in self.concern_types
    
    def is_safe_to_use(self) -> bool:
        return self.safety_rating.is_safe()
    
    def get_effectiveness_for_concern(self, concern_type: ConcernType) -> float:
        """Get effectiveness score for a specific concern"""
        for benefit in self.benefits:
            # Simple matching - in real implementation, this would be more sophisticated
            if any(ct.name.lower() in benefit.description.lower() for ct in self.concern_types):
                return benefit.effectiveness
        return 0.0


@dataclass
class EducationalContent:
    """Educational information about beauty concerns"""
    content_id: str
    title: str
    description: str
    explanation: str
    tips: List[str]
    last_updated: Timestamp
    
    def __post_init__(self):
        if not self.content_id:
            self.content_id = str(uuid.uuid4())
        if not self.title or len(self.title.strip()) == 0:
            raise ValueError("Educational content title cannot be empty")
        if not self.description or len(self.description.strip()) == 0:
            raise ValueError("Educational content description cannot be empty")
    
    def get_summary(self) -> str:
        """Get a brief summary of the content"""
        return f"{self.title}: {self.description[:100]}..."
    
    def is_recent(self, days: int = 30) -> bool:
        """Check if content was updated recently"""
        diff = datetime.now() - self.last_updated.value
        return diff.days <= days


@dataclass
class Product:
    """Product entity for recommendations"""
    product_id: ProductId
    name: str
    price: float
    rating: float
    category: str
    image_url: str
    ingredients: List[Ingredient] = field(default_factory=list)
    
    def __post_init__(self):
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("Product name cannot be empty")
        if self.price < 0:
            raise ValueError("Product price cannot be negative")
        if not 0.0 <= self.rating <= 5.0:
            raise ValueError("Product rating must be between 0.0 and 5.0")
    
    def contains_ingredient(self, ingredient: Ingredient) -> bool:
        """Check if product contains a specific ingredient"""
        return ingredient in self.ingredients
    
    def is_suitable_for_concern(self, concern_type: ConcernType) -> bool:
        """Check if product is suitable for a concern"""
        return any(ing.addresses_concern(concern_type) for ing in self.ingredients)
    
    def get_effectiveness_score(self, concern_type: ConcernType) -> float:
        """Calculate effectiveness score for a concern"""
        scores = [ing.get_effectiveness_for_concern(concern_type) for ing in self.ingredients]
        return max(scores) if scores else 0.0


@dataclass
class Review:
    """Product review entity"""
    review_id: str
    product_id: ProductId
    review_text: str
    rating: float
    reviewer_info: str
    created_at: Timestamp
    
    def __post_init__(self):
        if not self.review_id:
            self.review_id = str(uuid.uuid4())
        if not self.review_text or len(self.review_text.strip()) == 0:
            raise ValueError("Review text cannot be empty")
        if not 1.0 <= self.rating <= 5.0:
            raise ValueError("Review rating must be between 1.0 and 5.0")
    
    def is_positive(self) -> bool:
        return self.rating >= 4.0
    
    def is_recent(self, days: int = 90) -> bool:
        """Check if review is recent"""
        diff = datetime.now() - self.created_at.value
        return diff.days <= days
    
    def get_summary(self) -> str:
        """Get a brief summary of the review"""
        return f"{self.rating}/5 - {self.review_text[:100]}..."


@dataclass
class BotResponse:
    """Response generated by the bot"""
    response_id: str
    content: str
    concerns_addressed: List[ConcernType]
    products_recommended: List[ProductId]
    educational_content: Optional[EducationalContent] = None
    natural_remedies: List[str] = field(default_factory=list)
    generated_at: Timestamp = field(default_factory=Timestamp.now)
    
    def __post_init__(self):
        if not self.response_id:
            self.response_id = str(uuid.uuid4())
        if not self.content or len(self.content.strip()) == 0:
            raise ValueError("Bot response content cannot be empty")
    
    def has_product_recommendations(self) -> bool:
        return len(self.products_recommended) > 0
    
    def has_educational_content(self) -> bool:
        return self.educational_content is not None
    
    def has_natural_remedies(self) -> bool:
        return len(self.natural_remedies) > 0
    
    def get_response_summary(self) -> str:
        """Get a summary of what the response contains"""
        parts = []
        if self.has_educational_content():
            parts.append("educational content")
        if self.has_product_recommendations():
            parts.append(f"{len(self.products_recommended)} product recommendations")
        if self.has_natural_remedies():
            parts.append(f"{len(self.natural_remedies)} natural remedies")
        
        return f"Response includes: {', '.join(parts)}" if parts else "Basic response"
