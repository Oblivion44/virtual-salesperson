"""
Application Service for Concern-Based Chat Domain
"""
from typing import List, Optional, Dict
from dataclasses import dataclass

from value_objects import ConversationId, UserId, MessageContent
from aggregates import ConcernConversation, ConcernKnowledgeBase
from entities import BotResponse
from domain_services import (
    ConcernDetectionService, ResponseGenerationService, 
    ConcernMappingService, ConversationAnalyticsService
)
from repositories import (
    ConcernConversationRepository, ConcernKnowledgeRepository, ProductRepository
)
from domain_events import EventStore


@dataclass
class ChatResponse:
    """Response from the chat application service"""
    conversation_id: str
    bot_message: str
    concerns_detected: List[str]
    products_recommended: List[str]
    has_educational_content: bool
    has_natural_remedies: bool
    confidence_scores: Dict[str, float]


@dataclass
class ConversationSummary:
    """Summary of a conversation"""
    conversation_id: str
    user_id: Optional[str]
    total_messages: int
    concerns_discussed: List[str]
    is_active: bool
    created_at: str
    last_updated_at: str


class ConcernChatApplicationService:
    """
    Application Service: Orchestrates the concern-based chat workflow
    """
    
    def __init__(
        self,
        conversation_repo: ConcernConversationRepository,
        knowledge_repo: ConcernKnowledgeRepository,
        product_repo: ProductRepository,
        event_store: EventStore
    ):
        self.conversation_repo = conversation_repo
        self.knowledge_repo = knowledge_repo
        self.product_repo = product_repo
        self.event_store = event_store
        
        # Initialize domain services
        self.knowledge_base = knowledge_repo.get_default()
        self.concern_detection_service = ConcernDetectionService(self.knowledge_base)
        self.response_generation_service = ResponseGenerationService(self.knowledge_base)
        self.concern_mapping_service = ConcernMappingService(self.knowledge_base)
        self.analytics_service = ConversationAnalyticsService()
    
    def start_concern_conversation(self, user_id: Optional[str] = None) -> str:
        """Start a new concern-based conversation"""
        # Create new conversation
        conversation = ConcernConversation(
            conversation_id=ConversationId.generate(),
            user_id=UserId(user_id) if user_id else None
        )
        
        # Save conversation
        self.conversation_repo.save(conversation)
        
        # Publish domain events
        self._publish_domain_events(conversation)
        
        return conversation.conversation_id.value
    
    def process_concern_message(
        self, 
        conversation_id: str, 
        message: str,
        user_profile: Optional[Dict] = None
    ) -> ChatResponse:
        """Process a user message and generate appropriate response"""
        
        # Load conversation
        conv_id = ConversationId(conversation_id)
        conversation = self.conversation_repo.find_by_id(conv_id)
        
        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found")
        
        if not conversation.is_active():
            raise ValueError(f"Conversation {conversation_id} is not active")
        
        # Add user message
        message_id = conversation.add_user_message(message)
        
        # Detect concerns
        detected_concerns = conversation.detect_concerns(
            message, 
            self.concern_detection_service
        )
        
        # Generate response if concerns detected
        bot_response = None
        if detected_concerns:
            bot_response = conversation.generate_response(
                detected_concerns,
                self.response_generation_service
            )
            
            # Get product recommendations
            ingredients = self.concern_mapping_service.map_concerns_to_ingredients(detected_concerns)
            products = self.product_repo.find_by_ingredients([ing.ingredient_id for ing in ingredients])
            
            # Prioritize products based on user profile
            if products and user_profile:
                products = self.concern_mapping_service.prioritize_recommendations(products, user_profile)
        else:
            # Generate fallback response for no concerns detected
            bot_response = BotResponse(
                response_id="",
                content="I'd be happy to help with your beauty concerns! Could you tell me more about what specific issues you're experiencing with your skin or hair?",
                concerns_addressed=[],
                products_recommended=[]
            )
            conversation.add_bot_response(bot_response)
        
        # Save updated conversation
        self.conversation_repo.save(conversation)
        
        # Publish domain events
        self._publish_domain_events(conversation)
        
        # Build response
        return ChatResponse(
            conversation_id=conversation_id,
            bot_message=bot_response.content,
            concerns_detected=[c.concern_type.name for c in detected_concerns],
            products_recommended=[p.value for p in bot_response.products_recommended],
            has_educational_content=bot_response.has_educational_content(),
            has_natural_remedies=bot_response.has_natural_remedies(),
            confidence_scores={
                c.concern_type.name: c.confidence_score.value 
                for c in detected_concerns
            }
        )
    
    def end_conversation(self, conversation_id: str) -> None:
        """End a conversation"""
        conv_id = ConversationId(conversation_id)
        conversation = self.conversation_repo.find_by_id(conv_id)
        
        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found")
        
        conversation.end_conversation()
        self.conversation_repo.save(conversation)
        
        # Publish domain events
        self._publish_domain_events(conversation)
    
    def get_conversation_history(self, conversation_id: str) -> List[Dict]:
        """Get conversation message history"""
        conv_id = ConversationId(conversation_id)
        conversation = self.conversation_repo.find_by_id(conv_id)
        
        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found")
        
        messages = conversation.get_conversation_history()
        
        return [
            {
                "message_id": msg.message_id,
                "content": msg.content.text,
                "type": msg.message_type.value,
                "timestamp": msg.timestamp.value.isoformat(),
                "processing_status": msg.processing_status.value
            }
            for msg in messages
        ]
    
    def get_conversation_summary(self, conversation_id: str) -> ConversationSummary:
        """Get conversation summary"""
        conv_id = ConversationId(conversation_id)
        conversation = self.conversation_repo.find_by_id(conv_id)
        
        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found")
        
        return ConversationSummary(
            conversation_id=conversation_id,
            user_id=conversation.user_id.value if conversation.user_id else None,
            total_messages=conversation.get_message_count(),
            concerns_discussed=[c.concern_type.name for c in conversation.detected_concerns],
            is_active=conversation.is_active(),
            created_at=conversation.created_at.value.isoformat(),
            last_updated_at=conversation.last_updated_at.value.isoformat()
        )
    
    def get_active_conversations(self, user_id: Optional[str] = None) -> List[ConversationSummary]:
        """Get active conversations, optionally filtered by user"""
        if user_id:
            conversations = self.conversation_repo.find_by_user_id(UserId(user_id))
            conversations = [c for c in conversations if c.is_active()]
        else:
            conversations = self.conversation_repo.find_active_conversations()
        
        return [
            ConversationSummary(
                conversation_id=conv.conversation_id.value,
                user_id=conv.user_id.value if conv.user_id else None,
                total_messages=conv.get_message_count(),
                concerns_discussed=[c.concern_type.name for c in conv.detected_concerns],
                is_active=conv.is_active(),
                created_at=conv.created_at.value.isoformat(),
                last_updated_at=conv.last_updated_at.value.isoformat()
            )
            for conv in conversations
        ]
    
    def load_concern_data(self, csv_files: Dict[str, any]) -> None:
        """Load concern data from CSV files"""
        try:
            # Load knowledge base from CSV
            knowledge_base = self.knowledge_repo.load_from_csv(csv_files)
            
            # Update domain services with new knowledge base
            self.knowledge_base = knowledge_base
            self.concern_detection_service = ConcernDetectionService(knowledge_base)
            self.response_generation_service = ResponseGenerationService(knowledge_base)
            self.concern_mapping_service = ConcernMappingService(knowledge_base)
            
            # Load product data if provided
            if any(key in csv_files for key in ['products', 'reviews', 'product_ingredients']):
                self.product_repo.load_from_csv(csv_files)
            
        except Exception as e:
            raise ValueError(f"Failed to load CSV data: {str(e)}")
    
    def get_analytics_summary(self) -> Dict[str, any]:
        """Get analytics summary for all conversations"""
        all_conversations = self.conversation_repo.get_all()
        return self.analytics_service.get_conversation_statistics(all_conversations)
    
    def get_concern_detection_metrics(self) -> Dict[str, float]:
        """Get concern detection accuracy metrics"""
        all_conversations = self.conversation_repo.get_all()
        return self.analytics_service.analyze_concern_detection_accuracy(all_conversations)
    
    def search_products_by_concern(self, concern_name: str, limit: int = 10) -> List[Dict]:
        """Search products that address a specific concern"""
        # Find concern type
        concerns = self.knowledge_base.find_concerns_by_keywords([concern_name])
        
        if not concerns:
            return []
        
        concern = concerns[0]
        concern_id = concern.name.lower().replace(" ", "_")
        
        # Get ingredients for concern
        ingredients = self.knowledge_base.get_ingredients_for_concern(concern_id)
        
        if not ingredients:
            return []
        
        # Find products with these ingredients
        ingredient_ids = [ing.ingredient_id for ing in ingredients]
        products = self.product_repo.find_by_ingredients(ingredient_ids)
        
        # Sort by rating and limit results
        products.sort(key=lambda p: p.rating, reverse=True)
        products = products[:limit]
        
        return [
            {
                "product_id": product.product_id.value,
                "name": product.name,
                "price": product.price,
                "rating": product.rating,
                "category": product.category,
                "image_url": product.image_url
            }
            for product in products
        ]
    
    def get_educational_content_for_concern(self, concern_name: str) -> Optional[Dict]:
        """Get educational content for a specific concern"""
        concerns = self.knowledge_base.find_concerns_by_keywords([concern_name])
        
        if not concerns:
            return None
        
        concern = concerns[0]
        concern_id = concern.name.lower().replace(" ", "_")
        
        content = self.knowledge_base.get_educational_content(concern_id)
        
        if not content:
            return None
        
        return {
            "title": content.title,
            "description": content.description,
            "explanation": content.explanation,
            "tips": content.tips,
            "last_updated": content.last_updated.value.isoformat()
        }
    
    def _publish_domain_events(self, aggregate) -> None:
        """Publish domain events from aggregate"""
        events = aggregate.get_domain_events()
        
        for event in events:
            self.event_store.append_event(event)
        
        aggregate.clear_domain_events()
    
    def validate_system_health(self) -> Dict[str, bool]:
        """Validate that all system components are working"""
        health_status = {
            "conversation_repository": True,
            "knowledge_repository": True,
            "product_repository": True,
            "event_store": True,
            "concern_detection_service": True,
            "response_generation_service": True
        }
        
        try:
            # Test conversation repository
            test_conversations = self.conversation_repo.find_active_conversations()
            
            # Test knowledge repository
            test_kb = self.knowledge_repo.get_default()
            
            # Test concern detection
            test_message = MessageContent("I have dry skin")
            test_concerns = self.concern_detection_service.detect_concerns(test_message)
            
        except Exception as e:
            # In a real implementation, we'd log specific component failures
            health_status["system_error"] = str(e)
        
        return health_status
