"""
Value Objects for Concern-Based Chat Domain
"""
from dataclasses import dataclass
from typing import List
from datetime import datetime
import uuid


@dataclass(frozen=True)
class ConversationId:
    """Unique identifier for conversations"""
    value: str
    
    def __post_init__(self):
        if not self.value or len(self.value) < 8:
            raise ValueError("ConversationId must be at least 8 characters")
    
    @classmethod
    def generate(cls):
        return cls(str(uuid.uuid4()))


@dataclass(frozen=True)
class MessageContent:
    """Content of a message with validation"""
    text: str
    
    def __post_init__(self):
        if not self.text or len(self.text.strip()) == 0:
            raise ValueError("Message content cannot be empty")
        if len(self.text) > 1000:
            raise ValueError("Message content too long (max 1000 characters)")
    
    def get_clean_text(self) -> str:
        """Return cleaned text for processing"""
        return self.text.strip().lower()


@dataclass(frozen=True)
class ConcernType:
    """Type of beauty concern with category"""
    name: str
    category: str  # SKIN, HAIR, GENERAL
    
    def __post_init__(self):
        valid_categories = ["SKIN", "HAIR", "GENERAL"]
        if self.category not in valid_categories:
            raise ValueError(f"Invalid category: {self.category}")
        if not self.name or len(self.name.strip()) == 0:
            raise ValueError("Concern name cannot be empty")


@dataclass(frozen=True)
class ConfidenceScore:
    """Confidence score for concern detection"""
    value: float
    
    def __post_init__(self):
        if not 0.0 <= self.value <= 1.0:
            raise ValueError("Confidence score must be between 0.0 and 1.0")
    
    def is_high_confidence(self) -> bool:
        return self.value >= 0.8
    
    def is_medium_confidence(self) -> bool:
        return 0.6 <= self.value < 0.8
    
    def is_low_confidence(self) -> bool:
        return self.value < 0.6


@dataclass(frozen=True)
class ConversationState:
    """Current state of a conversation"""
    status: str  # ACTIVE, ENDED, PAUSED
    last_intent: str  # CONCERN, EXPLORATION, CHITCHAT
    
    def __post_init__(self):
        valid_statuses = ["ACTIVE", "ENDED", "PAUSED"]
        valid_intents = ["CONCERN", "EXPLORATION", "CHITCHAT", "UNKNOWN"]
        
        if self.status not in valid_statuses:
            raise ValueError(f"Invalid status: {self.status}")
        if self.last_intent not in valid_intents:
            raise ValueError(f"Invalid intent: {self.last_intent}")
    
    def is_active(self) -> bool:
        return self.status == "ACTIVE"


@dataclass(frozen=True)
class MessageType:
    """Type of message in conversation"""
    value: str  # USER, BOT
    
    def __post_init__(self):
        valid_types = ["USER", "BOT"]
        if self.value not in valid_types:
            raise ValueError(f"Invalid message type: {self.value}")
    
    def is_user_message(self) -> bool:
        return self.value == "USER"
    
    def is_bot_message(self) -> bool:
        return self.value == "BOT"


@dataclass(frozen=True)
class Keyword:
    """Keyword extracted from user message"""
    word: str
    weight: float = 1.0
    
    def __post_init__(self):
        if not self.word or len(self.word.strip()) == 0:
            raise ValueError("Keyword cannot be empty")
        if not 0.0 <= self.weight <= 10.0:
            raise ValueError("Keyword weight must be between 0.0 and 10.0")


@dataclass(frozen=True)
class Benefit:
    """Benefit provided by an ingredient"""
    description: str
    effectiveness: float = 1.0
    
    def __post_init__(self):
        if not self.description or len(self.description.strip()) == 0:
            raise ValueError("Benefit description cannot be empty")
        if not 0.0 <= self.effectiveness <= 1.0:
            raise ValueError("Effectiveness must be between 0.0 and 1.0")


@dataclass(frozen=True)
class SafetyRating:
    """Safety rating for ingredients"""
    rating: str  # SAFE, CAUTION, AVOID
    notes: str = ""
    
    def __post_init__(self):
        valid_ratings = ["SAFE", "CAUTION", "AVOID"]
        if self.rating not in valid_ratings:
            raise ValueError(f"Invalid safety rating: {self.rating}")
    
    def is_safe(self) -> bool:
        return self.rating == "SAFE"


@dataclass(frozen=True)
class ProcessingStatus:
    """Status of message processing"""
    value: str  # PENDING, PROCESSED, FAILED
    error_message: str = ""
    
    def __post_init__(self):
        valid_statuses = ["PENDING", "PROCESSED", "FAILED"]
        if self.value not in valid_statuses:
            raise ValueError(f"Invalid processing status: {self.value}")
    
    def is_processed(self) -> bool:
        return self.value == "PROCESSED"
    
    def has_failed(self) -> bool:
        return self.value == "FAILED"


@dataclass(frozen=True)
class ProductId:
    """Unique identifier for products"""
    value: str
    
    def __post_init__(self):
        if not self.value or len(self.value.strip()) == 0:
            raise ValueError("ProductId cannot be empty")


@dataclass(frozen=True)
class UserId:
    """Unique identifier for users"""
    value: str
    
    def __post_init__(self):
        if not self.value or len(self.value.strip()) == 0:
            raise ValueError("UserId cannot be empty")


@dataclass(frozen=True)
class Timestamp:
    """Timestamp with utility methods"""
    value: datetime
    
    def __post_init__(self):
        if not isinstance(self.value, datetime):
            raise ValueError("Timestamp must be a datetime object")
    
    @classmethod
    def now(cls):
        return cls(datetime.now())
    
    def is_recent(self, minutes: int = 5) -> bool:
        """Check if timestamp is within recent minutes"""
        diff = datetime.now() - self.value
        return diff.total_seconds() <= (minutes * 60)
