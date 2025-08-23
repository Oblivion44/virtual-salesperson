"""
Domain Events for Concern-Based Chat Domain
"""
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

from value_objects import ConversationId, MessageContent, ConcernType, ProductId, UserId, Timestamp
# Note: DetectedConcern import will be handled in the application layer to avoid circular imports


@dataclass(frozen=True)
class DomainEvent:
    """Base class for all domain events"""
    event_id: str
    occurred_at: Timestamp
    
    def __post_init__(self):
        if not self.event_id:
            import uuid
            object.__setattr__(self, 'event_id', str(uuid.uuid4()))


@dataclass(frozen=True)
class ConversationStartedEvent(DomainEvent):
    """Event fired when a new conversation begins"""
    conversation_id: ConversationId
    user_id: Optional[UserId]
    started_at: Timestamp
    
    def __post_init__(self):
        super().__post_init__()
        if not self.conversation_id:
            raise ValueError("ConversationStartedEvent must have a conversation_id")


@dataclass(frozen=True)
class MessageReceivedEvent(DomainEvent):
    """Event fired when a user sends a message"""
    conversation_id: ConversationId
    message_content: MessageContent
    user_id: Optional[UserId]
    received_at: Timestamp
    
    def __post_init__(self):
        super().__post_init__()
        if not self.conversation_id:
            raise ValueError("MessageReceivedEvent must have a conversation_id")
        if not self.message_content:
            raise ValueError("MessageReceivedEvent must have message content")


@dataclass(frozen=True)
class ConcernDetectedEvent(DomainEvent):
    """Event fired when beauty concerns are detected in user message"""
    conversation_id: ConversationId
    detected_concerns: List[any]  # DetectedConcern objects
    user_message: MessageContent
    detected_at: Timestamp
    
    def __post_init__(self):
        super().__post_init__()
        if not self.conversation_id:
            raise ValueError("ConcernDetectedEvent must have a conversation_id")
        if not self.detected_concerns:
            raise ValueError("ConcernDetectedEvent must have at least one detected concern")
    
    def get_primary_concern(self):
        """Get the concern with highest confidence"""
        return max(self.detected_concerns, key=lambda c: c.confidence_score.value)
    
    def has_high_confidence_concerns(self) -> bool:
        """Check if any concerns have high confidence"""
        return any(c.is_high_confidence() for c in self.detected_concerns)


@dataclass(frozen=True)
class ResponseGeneratedEvent(DomainEvent):
    """Event fired when bot generates a response"""
    conversation_id: ConversationId
    response_content: MessageContent
    concerns_addressed: List[ConcernType]
    products_recommended: List[ProductId]
    generated_at: Timestamp
    response_type: str = "CONCERN_BASED"  # CONCERN_BASED, EXPLORATION, CHITCHAT
    
    def __post_init__(self):
        super().__post_init__()
        if not self.conversation_id:
            raise ValueError("ResponseGeneratedEvent must have a conversation_id")
        if not self.response_content:
            raise ValueError("ResponseGeneratedEvent must have response content")
        
        valid_types = ["CONCERN_BASED", "EXPLORATION", "CHITCHAT"]
        if self.response_type not in valid_types:
            raise ValueError(f"Invalid response type: {self.response_type}")
    
    def has_product_recommendations(self) -> bool:
        return len(self.products_recommended) > 0
    
    def addresses_multiple_concerns(self) -> bool:
        return len(self.concerns_addressed) > 1


@dataclass(frozen=True)
class ConversationEndedEvent(DomainEvent):
    """Event fired when a conversation session ends"""
    conversation_id: ConversationId
    user_id: Optional[UserId]
    ended_at: Timestamp
    total_messages: int
    concerns_discussed: List[ConcernType]
    products_recommended: List[ProductId]
    
    def __post_init__(self):
        super().__post_init__()
        if not self.conversation_id:
            raise ValueError("ConversationEndedEvent must have a conversation_id")
        if self.total_messages < 0:
            raise ValueError("Total messages cannot be negative")
    
    def was_productive(self) -> bool:
        """Check if conversation resulted in recommendations"""
        return len(self.products_recommended) > 0 or len(self.concerns_discussed) > 0


@dataclass(frozen=True)
class ProductRecommendationRequestedEvent(DomainEvent):
    """Event fired when product recommendations are requested"""
    conversation_id: ConversationId
    concerns: List[ConcernType]
    user_profile: Optional[dict]  # User profile data
    requested_at: Timestamp
    
    def __post_init__(self):
        super().__post_init__()
        if not self.conversation_id:
            raise ValueError("ProductRecommendationRequestedEvent must have a conversation_id")
        if not self.concerns:
            raise ValueError("ProductRecommendationRequestedEvent must have at least one concern")


@dataclass(frozen=True)
class EducationalContentRequestedEvent(DomainEvent):
    """Event fired when educational content is requested"""
    conversation_id: ConversationId
    concern_type: ConcernType
    requested_at: Timestamp
    
    def __post_init__(self):
        super().__post_init__()
        if not self.conversation_id:
            raise ValueError("EducationalContentRequestedEvent must have a conversation_id")
        if not self.concern_type:
            raise ValueError("EducationalContentRequestedEvent must have a concern type")


@dataclass(frozen=True)
class NaturalRemedyRequestedEvent(DomainEvent):
    """Event fired when natural remedies are requested"""
    conversation_id: ConversationId
    concern_type: ConcernType
    requested_at: Timestamp
    
    def __post_init__(self):
        super().__post_init__()
        if not self.conversation_id:
            raise ValueError("NaturalRemedyRequestedEvent must have a conversation_id")
        if not self.concern_type:
            raise ValueError("NaturalRemedyRequestedEvent must have a concern type")


@dataclass(frozen=True)
class IntentDetectedEvent(DomainEvent):
    """Event fired when user intent is classified"""
    conversation_id: ConversationId
    detected_intent: str  # CONCERN, EXPLORATION, CHITCHAT
    confidence_score: float
    user_message: MessageContent
    detected_at: Timestamp
    
    def __post_init__(self):
        super().__post_init__()
        if not self.conversation_id:
            raise ValueError("IntentDetectedEvent must have a conversation_id")
        
        valid_intents = ["CONCERN", "EXPLORATION", "CHITCHAT"]
        if self.detected_intent not in valid_intents:
            raise ValueError(f"Invalid intent: {self.detected_intent}")
        
        if not 0.0 <= self.confidence_score <= 1.0:
            raise ValueError("Confidence score must be between 0.0 and 1.0")
    
    def is_high_confidence(self) -> bool:
        return self.confidence_score >= 0.8


@dataclass(frozen=True)
class ErrorOccurredEvent(DomainEvent):
    """Event fired when an error occurs during processing"""
    conversation_id: ConversationId
    error_type: str
    error_message: str
    user_message: Optional[MessageContent]
    occurred_at: Timestamp
    
    def __post_init__(self):
        super().__post_init__()
        if not self.conversation_id:
            raise ValueError("ErrorOccurredEvent must have a conversation_id")
        if not self.error_type:
            raise ValueError("ErrorOccurredEvent must have an error type")
        if not self.error_message:
            raise ValueError("ErrorOccurredEvent must have an error message")
    
    def is_critical_error(self) -> bool:
        """Check if this is a critical error that should stop processing"""
        critical_types = ["SYSTEM_ERROR", "DATA_CORRUPTION", "SECURITY_VIOLATION"]
        return self.error_type in critical_types


# Event Store Interface
class EventStore:
    """Interface for storing and retrieving domain events"""
    
    def append_event(self, event: DomainEvent) -> None:
        """Store a domain event"""
        raise NotImplementedError
    
    def get_events_for_conversation(self, conversation_id: ConversationId) -> List[DomainEvent]:
        """Get all events for a specific conversation"""
        raise NotImplementedError
    
    def get_events_by_type(self, event_type: type) -> List[DomainEvent]:
        """Get all events of a specific type"""
        raise NotImplementedError
    
    def get_all_events(self) -> List[DomainEvent]:
        """Get all stored events"""
        raise NotImplementedError


# In-Memory Event Store Implementation
class InMemoryEventStore(EventStore):
    """In-memory implementation of event store"""
    
    def __init__(self):
        self._events: List[DomainEvent] = []
    
    def append_event(self, event: DomainEvent) -> None:
        """Store a domain event"""
        self._events.append(event)
    
    def get_events_for_conversation(self, conversation_id: ConversationId) -> List[DomainEvent]:
        """Get all events for a specific conversation"""
        return [
            event for event in self._events 
            if hasattr(event, 'conversation_id') and event.conversation_id == conversation_id
        ]
    
    def get_events_by_type(self, event_type: type) -> List[DomainEvent]:
        """Get all events of a specific type"""
        return [event for event in self._events if isinstance(event, event_type)]
    
    def get_all_events(self) -> List[DomainEvent]:
        """Get all stored events"""
        return self._events.copy()
    
    def clear(self) -> None:
        """Clear all events (for testing)"""
        self._events.clear()
