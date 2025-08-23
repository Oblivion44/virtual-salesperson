#!/usr/bin/env python3
"""
Simple Test Script for Concern-Based Chat Domain Model
Tests core functionality without external dependencies
"""

import sys
import os

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from value_objects import *
from entities import *
from aggregates import *
from domain_services import *
from repositories import *
from domain_events import *


def test_value_objects():
    """Test value objects creation and validation"""
    print("Testing Value Objects...")
    
    # Test ConversationId
    conv_id = ConversationId.generate()
    assert len(conv_id.value) >= 8
    print(f"✓ ConversationId: {conv_id.value}")
    
    # Test MessageContent
    message = MessageContent("I have acne problems")
    assert message.text == "I have acne problems"
    assert message.get_clean_text() == "i have acne problems"
    print(f"✓ MessageContent: {message.text}")
    
    # Test ConcernType
    concern = ConcernType("Acne", "SKIN")
    assert concern.name == "Acne"
    assert concern.category == "SKIN"
    print(f"✓ ConcernType: {concern.name} ({concern.category})")
    
    # Test ConfidenceScore
    confidence = ConfidenceScore(0.85)
    assert confidence.value == 0.85
    assert confidence.is_high_confidence()
    print(f"✓ ConfidenceScore: {confidence.value}")
    
    print("Value Objects tests passed!\n")


def test_entities():
    """Test entities creation and behavior"""
    print("Testing Entities...")
    
    # Test Message
    message = Message(
        message_id="",
        content=MessageContent("Hello"),
        message_type=MessageType("USER"),
        timestamp=Timestamp.now()
    )
    assert message.is_user_message()
    print(f"✓ Message: {message.content.text}")
    
    # Test DetectedConcern
    concern = DetectedConcern(
        detected_concern_id="",
        concern_type=ConcernType("Acne", "SKIN"),
        confidence_score=ConfidenceScore(0.9),
        extracted_keywords=[Keyword("acne"), Keyword("pimples")],
        detected_at=Timestamp.now()
    )
    assert concern.is_high_confidence()
    print(f"✓ DetectedConcern: {concern.concern_type.name}")
    
    # Test Ingredient
    ingredient = Ingredient(
        ingredient_id="",
        name="Salicylic Acid",
        benefits=[Benefit("Unclogs pores")],
        concern_types=[ConcernType("Acne", "SKIN")],
        safety_rating=SafetyRating("SAFE")
    )
    assert ingredient.is_safe_to_use()
    print(f"✓ Ingredient: {ingredient.name}")
    
    print("Entities tests passed!\n")


def test_aggregates():
    """Test aggregates creation and business logic"""
    print("Testing Aggregates...")
    
    # Test ConcernConversation
    conversation = ConcernConversation(
        conversation_id=ConversationId.generate(),
        user_id=UserId("test_user")
    )
    
    # Add user message
    message_id = conversation.add_user_message("I have acne problems")
    assert len(conversation.messages) == 1
    assert conversation.is_active()
    print(f"✓ ConcernConversation: Added message {message_id}")
    
    # Test ConcernKnowledgeBase
    kb = ConcernKnowledgeBase("test_kb")
    
    # Add concern
    concern_type = ConcernType("Acne", "SKIN")
    keywords = [Keyword("acne"), Keyword("pimples")]
    kb.add_concern(concern_type, keywords)
    
    # Add ingredient
    ingredient = Ingredient(
        ingredient_id="salicylic_acid",
        name="Salicylic Acid",
        benefits=[Benefit("Unclogs pores")],
        concern_types=[concern_type],
        safety_rating=SafetyRating("SAFE")
    )
    kb.add_ingredient(ingredient)
    
    assert len(kb.concerns) == 1
    assert len(kb.ingredients) == 1
    print(f"✓ ConcernKnowledgeBase: Added concern and ingredient")
    
    print("Aggregates tests passed!\n")


def test_domain_services():
    """Test domain services"""
    print("Testing Domain Services...")
    
    # Create knowledge base with sample data
    kb = ConcernKnowledgeBase("test_kb")
    
    # Add sample concern
    concern_type = ConcernType("Acne", "SKIN")
    keywords = [Keyword("acne"), Keyword("pimples"), Keyword("breakouts")]
    kb.add_concern(concern_type, keywords)
    
    # Test ConcernDetectionService
    detection_service = ConcernDetectionService(kb)
    message = MessageContent("I have terrible acne and pimples")
    
    detected_concerns = detection_service.detect_concerns(message)
    print(f"✓ ConcernDetectionService: Detected {len(detected_concerns)} concerns")
    
    if detected_concerns:
        for concern in detected_concerns:
            print(f"  - {concern.concern_type.name}: {concern.confidence_score.value:.2f}")
    
    print("Domain Services tests passed!\n")


def test_repositories():
    """Test repository implementations"""
    print("Testing Repositories...")
    
    # Test ConversationRepository
    conv_repo = InMemoryConcernConversationRepository()
    
    conversation = ConcernConversation(
        conversation_id=ConversationId.generate(),
        user_id=UserId("test_user")
    )
    
    conv_repo.save(conversation)
    retrieved = conv_repo.find_by_id(conversation.conversation_id)
    
    assert retrieved is not None
    assert retrieved.conversation_id.value == conversation.conversation_id.value
    print(f"✓ ConversationRepository: Saved and retrieved conversation")
    
    # Test KnowledgeRepository
    kb_repo = InMemoryConcernKnowledgeRepository()
    kb = kb_repo.get_default()
    
    assert kb is not None
    print(f"✓ KnowledgeRepository: Retrieved default knowledge base")
    
    print("Repositories tests passed!\n")


def test_event_store():
    """Test event store functionality"""
    print("Testing Event Store...")
    
    event_store = InMemoryEventStore()
    
    # Create and store an event
    event = ConversationStartedEvent(
        event_id="",
        occurred_at=Timestamp.now(),
        conversation_id=ConversationId.generate(),
        user_id=UserId("test_user"),
        started_at=Timestamp.now()
    )
    
    event_store.append_event(event)
    
    # Retrieve events
    all_events = event_store.get_all_events()
    assert len(all_events) == 1
    
    conversation_events = event_store.get_events_for_conversation(event.conversation_id)
    assert len(conversation_events) == 1
    
    print(f"✓ EventStore: Stored and retrieved {len(all_events)} events")
    
    print("Event Store tests passed!\n")


def main():
    """Run all tests"""
    print("🧪 Running Simple Tests for DDD Domain Model")
    print("=" * 50)
    
    try:
        test_value_objects()
        test_entities()
        test_aggregates()
        test_domain_services()
        test_repositories()
        test_event_store()
        
        print("=" * 50)
        print("✅ All tests passed successfully!")
        print("\nThe DDD domain model implementation is working correctly.")
        print("Ready to proceed with Step 2.3 (Testing and Debugging).")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
