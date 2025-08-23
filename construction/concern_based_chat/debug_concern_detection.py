#!/usr/bin/env python3
"""
Debug script to fix concern detection issues
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from value_objects import *
from entities import *
from aggregates import *
from domain_services import *
from repositories import *


def debug_concern_detection():
    """Debug concern detection step by step"""
    print("=== Debugging Concern Detection ===")
    
    # Create knowledge base
    kb = ConcernKnowledgeBase("debug_kb")
    
    # Add a simple concern
    concern_type = ConcernType("Acne", "SKIN")
    keywords = [Keyword("acne"), Keyword("pimples"), Keyword("breakouts")]
    
    print(f"Adding concern: {concern_type.name}")
    print(f"Keywords: {[kw.word for kw in keywords]}")
    
    kb.add_concern(concern_type, keywords)
    
    # Check if concern was added
    print(f"Concerns in KB: {list(kb.concerns.keys())}")
    print(f"Keywords in KB: {list(kb.concern_keywords.keys())}")
    
    # Create detection service
    detection_service = ConcernDetectionService(kb)
    
    # Test message
    test_message = "I have acne problems"
    message_content = MessageContent(test_message)
    
    print(f"\nTesting message: '{test_message}'")
    print(f"Clean text: '{message_content.get_clean_text()}'")
    
    # Extract keywords
    keywords_extracted = detection_service.extract_keywords(message_content.get_clean_text())
    print(f"Extracted keywords: {[kw.word for kw in keywords_extracted]}")
    
    # Test concern detection
    detected_concerns = detection_service.detect_concerns(message_content)
    print(f"Detected concerns: {len(detected_concerns)}")
    
    for concern in detected_concerns:
        print(f"- {concern.concern_type.name}: {concern.confidence_score.value:.2f}")
    
    # Debug the scoring process
    print(f"\n--- Debug Scoring ---")
    concern_id = "acne"
    concern_keywords_in_kb = kb.concern_keywords.get(concern_id, [])
    print(f"Concern keywords in KB: {[kw.word for kw in concern_keywords_in_kb]}")
    
    # Manual confidence calculation
    confidence = detection_service.calculate_confidence(keywords_extracted, concern_type)
    print(f"Manual confidence calculation: {confidence.value}")


def debug_knowledge_base_structure():
    """Debug knowledge base structure"""
    print("\n=== Debugging Knowledge Base Structure ===")
    
    kb = ConcernKnowledgeBase("debug_kb")
    
    # Add concern with proper ID
    concern_type = ConcernType("Acne", "SKIN")
    keywords = [Keyword("acne"), Keyword("pimples")]
    
    kb.add_concern(concern_type, keywords)
    
    print(f"Concerns dict: {kb.concerns}")
    print(f"Concern keywords dict: {kb.concern_keywords}")
    
    # Test find_concerns_by_keywords
    found_concerns = kb.find_concerns_by_keywords(["acne"])
    print(f"Found concerns for 'acne': {[c.name for c in found_concerns]}")


def debug_full_flow():
    """Debug the full concern detection flow"""
    print("\n=== Debugging Full Flow ===")
    
    # Set up repositories
    knowledge_repo = InMemoryConcernKnowledgeRepository()
    kb = knowledge_repo.get_default()
    
    # Add concern properly
    concern_type = ConcernType("Acne", "SKIN")
    keywords = [Keyword("acne"), Keyword("pimples"), Keyword("breakouts")]
    kb.add_concern(concern_type, keywords)
    
    print(f"KB after adding concern:")
    print(f"- Concerns: {list(kb.concerns.keys())}")
    print(f"- Keywords: {list(kb.concern_keywords.keys())}")
    
    # Create detection service
    detection_service = ConcernDetectionService(kb)
    
    # Test detection
    message = MessageContent("I have terrible acne and pimples")
    detected = detection_service.detect_concerns(message)
    
    print(f"\nMessage: '{message.text}'")
    print(f"Detected concerns: {len(detected)}")
    
    for concern in detected:
        print(f"- {concern.concern_type.name}: {concern.confidence_score.value:.2f}")
        print(f"  Keywords: {[kw.word for kw in concern.extracted_keywords]}")


if __name__ == "__main__":
    debug_concern_detection()
    debug_knowledge_base_structure()
    debug_full_flow()
