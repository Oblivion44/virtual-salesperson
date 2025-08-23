"""
Concern-Based Chat Domain Model Package

This package implements a Domain Driven Design (DDD) architecture for handling
beauty concern-based conversations in the Beauty Recommendation Chatbot.

Main Components:
- Value Objects: Immutable objects that represent concepts
- Entities: Objects with identity that can change over time
- Aggregates: Clusters of entities and value objects with consistency boundaries
- Domain Services: Stateless services that implement domain logic
- Repositories: Interfaces for data persistence
- Domain Events: Events that represent important business occurrences
- Application Service: Orchestrates domain operations

Usage:
    from concern_based_chat import ConcernChatApplicationService
    from concern_based_chat.repositories import (
        InMemoryConcernConversationRepository,
        InMemoryConcernKnowledgeRepository,
        InMemoryProductRepository
    )
    from concern_based_chat.domain_events import InMemoryEventStore
    
    # Set up repositories
    conversation_repo = InMemoryConcernConversationRepository()
    knowledge_repo = InMemoryConcernKnowledgeRepository()
    product_repo = InMemoryProductRepository()
    event_store = InMemoryEventStore()
    
    # Create application service
    app_service = ConcernChatApplicationService(
        conversation_repo, knowledge_repo, product_repo, event_store
    )
    
    # Load CSV data
    app_service.load_concern_data(csv_data)
    
    # Start conversation
    conversation_id = app_service.start_concern_conversation()
    
    # Process messages
    response = app_service.process_concern_message(conversation_id, "I have acne")
"""

# Import main classes for easy access
from .application_service import ConcernChatApplicationService, ChatResponse, ConversationSummary
from .aggregates import ConcernConversation, ConcernKnowledgeBase
from .domain_services import (
    ConcernDetectionService, ResponseGenerationService, 
    ConcernMappingService, ConversationAnalyticsService
)
from .repositories import (
    InMemoryConcernConversationRepository,
    InMemoryConcernKnowledgeRepository,
    InMemoryProductRepository
)
from .domain_events import InMemoryEventStore
from .value_objects import ConversationId, MessageContent, ConcernType
from .entities import DetectedConcern, BotResponse, Product, Review

__version__ = "1.0.0"
__author__ = "Beauty Chatbot Development Team"

__all__ = [
    # Application Service
    'ConcernChatApplicationService',
    'ChatResponse',
    'ConversationSummary',
    
    # Aggregates
    'ConcernConversation',
    'ConcernKnowledgeBase',
    
    # Domain Services
    'ConcernDetectionService',
    'ResponseGenerationService',
    'ConcernMappingService',
    'ConversationAnalyticsService',
    
    # Repositories
    'InMemoryConcernConversationRepository',
    'InMemoryConcernKnowledgeRepository',
    'InMemoryProductRepository',
    
    # Event Store
    'InMemoryEventStore',
    
    # Key Value Objects
    'ConversationId',
    'MessageContent',
    'ConcernType',
    
    # Key Entities
    'DetectedConcern',
    'BotResponse',
    'Product',
    'Review'
]
