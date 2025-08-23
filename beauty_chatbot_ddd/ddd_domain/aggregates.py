"""
Aggregates for Concern-Based Chat Domain
"""
from dataclasses import dataclass, field
from typing import List, Optional, Dict
from datetime import datetime
import uuid

from value_objects import (
    ConversationId, MessageContent, ConcernType, ConversationState,
    MessageType, UserId, Timestamp, Keyword, ConfidenceScore
)
from entities import (
    Message, DetectedConcern, Ingredient, EducationalContent, 
    Product, BotResponse
)
from domain_events import (
    ConversationStartedEvent, MessageReceivedEvent, ConcernDetectedEvent,
    ResponseGeneratedEvent, ConversationEndedEvent, DomainEvent
)


@dataclass
class ConcernConversation:
    """
    Aggregate Root: Manages the complete lifecycle of a concern-based conversation
    """
    conversation_id: ConversationId
    user_id: Optional[UserId]
    messages: List[Message] = field(default_factory=list)
    detected_concerns: List[DetectedConcern] = field(default_factory=list)
    conversation_state: ConversationState = field(
        default_factory=lambda: ConversationState("ACTIVE", "UNKNOWN")
    )
    created_at: Timestamp = field(default_factory=Timestamp.now)
    last_updated_at: Timestamp = field(default_factory=Timestamp.now)
    _domain_events: List[DomainEvent] = field(default_factory=list, init=False)
    
    def __post_init__(self):
        if not self.conversation_id:
            self.conversation_id = ConversationId.generate()
        
        # Fire conversation started event
        self._add_domain_event(
            ConversationStartedEvent(
                event_id="",
                occurred_at=self.created_at,
                conversation_id=self.conversation_id,
                user_id=self.user_id,
                started_at=self.created_at
            )
        )
    
    def add_user_message(self, content: str) -> str:
        """Add a user message to the conversation"""
        if not self.conversation_state.is_active():
            raise ValueError("Cannot add message to inactive conversation")
        
        message_content = MessageContent(content)
        message = Message(
            message_id="",
            content=message_content,
            message_type=MessageType("USER"),
            timestamp=Timestamp.now()
        )
        
        self.messages.append(message)
        self.last_updated_at = Timestamp.now()
        
        # Fire message received event
        self._add_domain_event(
            MessageReceivedEvent(
                event_id="",
                occurred_at=message.timestamp,
                conversation_id=self.conversation_id,
                message_content=message_content,
                user_id=self.user_id,
                received_at=message.timestamp
            )
        )
        
        return message.message_id
    
    def add_bot_response(self, response: BotResponse) -> str:
        """Add a bot response to the conversation"""
        if not self.conversation_state.is_active():
            raise ValueError("Cannot add response to inactive conversation")
        
        message = Message(
            message_id="",
            content=MessageContent(response.content),
            message_type=MessageType("BOT"),
            timestamp=Timestamp.now()
        )
        
        self.messages.append(message)
        self.last_updated_at = Timestamp.now()
        
        # Fire response generated event
        self._add_domain_event(
            ResponseGeneratedEvent(
                event_id="",
                occurred_at=message.timestamp,
                conversation_id=self.conversation_id,
                response_content=message.content,
                concerns_addressed=response.concerns_addressed,
                products_recommended=response.products_recommended,
                generated_at=message.timestamp
            )
        )
        
        return message.message_id
    
    def detect_concerns(self, message_content: str, concern_detection_service) -> List[DetectedConcern]:
        """Detect concerns from user message using domain service"""
        if not self.conversation_state.is_active():
            raise ValueError("Cannot detect concerns in inactive conversation")
        
        message_content_vo = MessageContent(message_content)
        detected_concerns = concern_detection_service.detect_concerns(message_content_vo)
        
        if detected_concerns:
            self.detected_concerns.extend(detected_concerns)
            self.last_updated_at = Timestamp.now()
            
            # Update conversation state
            self.conversation_state = ConversationState("ACTIVE", "CONCERN")
            
            # Fire concern detected event
            self._add_domain_event(
                ConcernDetectedEvent(
                    event_id="",
                    occurred_at=Timestamp.now(),
                    conversation_id=self.conversation_id,
                    detected_concerns=detected_concerns,
                    user_message=message_content_vo,
                    detected_at=Timestamp.now()
                )
            )
        
        return detected_concerns
    
    def generate_response(self, concerns: List[DetectedConcern], response_service) -> BotResponse:
        """Generate bot response for detected concerns"""
        if not self.conversation_state.is_active():
            raise ValueError("Cannot generate response for inactive conversation")
        
        if not concerns:
            raise ValueError("Cannot generate response without concerns")
        
        response = response_service.generate_concern_response(concerns)
        self.add_bot_response(response)
        
        return response
    
    def is_active(self) -> bool:
        """Check if conversation is active"""
        return self.conversation_state.is_active()
    
    def end_conversation(self) -> None:
        """End the conversation"""
        if not self.conversation_state.is_active():
            return  # Already ended
        
        self.conversation_state = ConversationState("ENDED", self.conversation_state.last_intent)
        self.last_updated_at = Timestamp.now()
        
        # Collect conversation statistics
        concerns_discussed = list(set(dc.concern_type for dc in self.detected_concerns))
        products_recommended = []
        
        # Extract product recommendations from bot messages
        for message in self.messages:
            if message.is_bot_message():
                # In a real implementation, we'd parse the message content
                # For now, we'll use a simple approach
                pass
        
        # Fire conversation ended event
        self._add_domain_event(
            ConversationEndedEvent(
                event_id="",
                occurred_at=self.last_updated_at,
                conversation_id=self.conversation_id,
                user_id=self.user_id,
                ended_at=self.last_updated_at,
                total_messages=len(self.messages),
                concerns_discussed=concerns_discussed,
                products_recommended=products_recommended
            )
        )
    
    def get_conversation_history(self) -> List[Message]:
        """Get all messages in chronological order"""
        return sorted(self.messages, key=lambda m: m.timestamp.value)
    
    def get_recent_concerns(self, minutes: int = 30) -> List[DetectedConcern]:
        """Get concerns detected in recent minutes"""
        cutoff_time = datetime.now()
        return [
            concern for concern in self.detected_concerns
            if (cutoff_time - concern.detected_at.value).total_seconds() <= (minutes * 60)
        ]
    
    def has_concerns_of_category(self, category: str) -> bool:
        """Check if conversation has concerns of specific category"""
        return any(concern.matches_category(category) for concern in self.detected_concerns)
    
    def get_message_count(self) -> int:
        """Get total number of messages"""
        return len(self.messages)
    
    def get_user_message_count(self) -> int:
        """Get number of user messages"""
        return len([m for m in self.messages if m.is_user_message()])
    
    def get_bot_message_count(self) -> int:
        """Get number of bot messages"""
        return len([m for m in self.messages if m.is_bot_message()])
    
    def _add_domain_event(self, event: DomainEvent) -> None:
        """Add domain event to be published"""
        self._domain_events.append(event)
    
    def get_domain_events(self) -> List[DomainEvent]:
        """Get all domain events for this aggregate"""
        return self._domain_events.copy()
    
    def clear_domain_events(self) -> None:
        """Clear domain events after publishing"""
        self._domain_events.clear()
    
    # Business Rules Validation
    def _validate_invariants(self) -> None:
        """Validate aggregate invariants"""
        # Must have at least one user message to be valid (except for new conversations)
        if len(self.messages) > 0:
            user_messages = [m for m in self.messages if m.is_user_message()]
            if not user_messages:
                raise ValueError("Conversation must have at least one user message")
        
        # Cannot have more than 100 messages per conversation
        if len(self.messages) > 100:
            raise ValueError("Conversation cannot have more than 100 messages")
        
        # Messages must be in chronological order
        timestamps = [m.timestamp.value for m in self.messages]
        if timestamps != sorted(timestamps):
            raise ValueError("Messages must be in chronological order")


@dataclass
class ConcernKnowledgeBase:
    """
    Aggregate Root: Manages the mapping between concerns, ingredients, and educational content
    """
    knowledge_base_id: str
    concerns: Dict[str, ConcernType] = field(default_factory=dict)
    ingredients: Dict[str, Ingredient] = field(default_factory=dict)
    educational_content: Dict[str, EducationalContent] = field(default_factory=dict)
    concern_ingredient_mappings: Dict[str, List[str]] = field(default_factory=dict)  # concern_id -> ingredient_ids
    concern_keywords: Dict[str, List[Keyword]] = field(default_factory=dict)  # concern_id -> keywords
    last_updated: Timestamp = field(default_factory=Timestamp.now)
    _domain_events: List[DomainEvent] = field(default_factory=list, init=False)
    
    def __post_init__(self):
        if not self.knowledge_base_id:
            self.knowledge_base_id = str(uuid.uuid4())
    
    def add_concern(self, concern: ConcernType, keywords: List[Keyword]) -> None:
        """Add a new concern with associated keywords"""
        concern_id = concern.name.lower().replace(" ", "_")
        
        if concern_id in self.concerns:
            raise ValueError(f"Concern {concern.name} already exists")
        
        self.concerns[concern_id] = concern
        self.concern_keywords[concern_id] = keywords
        self.last_updated = Timestamp.now()
    
    def add_ingredient(self, ingredient: Ingredient) -> None:
        """Add a new ingredient"""
        ingredient_id = ingredient.name.lower().replace(" ", "_")
        
        if ingredient_id in self.ingredients:
            raise ValueError(f"Ingredient {ingredient.name} already exists")
        
        self.ingredients[ingredient_id] = ingredient
        self.last_updated = Timestamp.now()
    
    def add_educational_content(self, concern_id: str, content: EducationalContent) -> None:
        """Add educational content for a concern"""
        if concern_id not in self.concerns:
            raise ValueError(f"Concern {concern_id} does not exist")
        
        self.educational_content[concern_id] = content
        self.last_updated = Timestamp.now()
    
    def map_concern_to_ingredients(self, concern_id: str, ingredient_ids: List[str]) -> None:
        """Map a concern to ingredients"""
        if concern_id not in self.concerns:
            raise ValueError(f"Concern {concern_id} does not exist")
        
        # Validate that all ingredients exist
        for ingredient_id in ingredient_ids:
            if ingredient_id not in self.ingredients:
                raise ValueError(f"Ingredient {ingredient_id} does not exist")
        
        self.concern_ingredient_mappings[concern_id] = ingredient_ids
        self.last_updated = Timestamp.now()
    
    def find_concerns_by_keywords(self, keywords: List[str]) -> List[ConcernType]:
        """Find concerns that match the given keywords"""
        matched_concerns = []
        keywords_lower = [k.lower() for k in keywords]
        
        for concern_id, concern_keywords in self.concern_keywords.items():
            keyword_matches = [kw.word.lower() for kw in concern_keywords]
            
            # Check if any of the input keywords match concern keywords
            if any(kw in keyword_matches for kw in keywords_lower):
                matched_concerns.append(self.concerns[concern_id])
        
        return matched_concerns
    
    def get_ingredients_for_concern(self, concern_id: str) -> List[Ingredient]:
        """Get ingredients that address a specific concern"""
        if concern_id not in self.concerns:
            raise ValueError(f"Concern {concern_id} does not exist")
        
        ingredient_ids = self.concern_ingredient_mappings.get(concern_id, [])
        return [self.ingredients[ing_id] for ing_id in ingredient_ids if ing_id in self.ingredients]
    
    def get_educational_content(self, concern_id: str) -> Optional[EducationalContent]:
        """Get educational content for a concern"""
        return self.educational_content.get(concern_id)
    
    def load_from_csv_data(self, csv_data: Dict[str, any]) -> None:
        """Load knowledge base from CSV data"""
        # This method would parse CSV data and populate the knowledge base
        # Implementation would depend on the specific CSV format
        
        # Example structure:
        # csv_data = {
        #     'concerns': DataFrame with concern data,
        #     'ingredients': DataFrame with ingredient data,
        #     'mappings': DataFrame with concern-ingredient mappings,
        #     'educational_content': DataFrame with educational content
        # }
        
        self.last_updated = Timestamp.now()
        # Detailed implementation would go here
    
    def get_all_concerns(self) -> List[ConcernType]:
        """Get all available concerns"""
        return list(self.concerns.values())
    
    def get_all_ingredients(self) -> List[Ingredient]:
        """Get all available ingredients"""
        return list(self.ingredients.values())
    
    def get_concerns_by_category(self, category: str) -> List[ConcernType]:
        """Get concerns filtered by category"""
        return [concern for concern in self.concerns.values() if concern.category == category]
    
    def search_ingredients_by_benefit(self, benefit_keyword: str) -> List[Ingredient]:
        """Search ingredients by benefit description"""
        matching_ingredients = []
        benefit_lower = benefit_keyword.lower()
        
        for ingredient in self.ingredients.values():
            for benefit in ingredient.benefits:
                if benefit_lower in benefit.description.lower():
                    matching_ingredients.append(ingredient)
                    break
        
        return matching_ingredients
    
    def _validate_invariants(self) -> None:
        """Validate aggregate invariants"""
        # Each concern must have at least one associated ingredient
        for concern_id in self.concerns.keys():
            if concern_id not in self.concern_ingredient_mappings:
                raise ValueError(f"Concern {concern_id} must have at least one associated ingredient")
        
        # Educational content must be present for each concern
        for concern_id in self.concerns.keys():
            if concern_id not in self.educational_content:
                raise ValueError(f"Educational content must be present for concern {concern_id}")
    
    def _add_domain_event(self, event: DomainEvent) -> None:
        """Add domain event to be published"""
        self._domain_events.append(event)
    
    def get_domain_events(self) -> List[DomainEvent]:
        """Get all domain events for this aggregate"""
        return self._domain_events.copy()
    
    def clear_domain_events(self) -> None:
        """Clear domain events after publishing"""
        self._domain_events.clear()
