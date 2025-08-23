#!/usr/bin/env python3
"""
Demo Script for Concern-Based Chat Domain Model
This script demonstrates the DDD implementation with sample data
"""

import pandas as pd
from typing import Dict
import sys
import os

# Add the current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from value_objects import *
from entities import *
from aggregates import *
from domain_services import *
from repositories import *
from application_service import *
from domain_events import *


def create_sample_csv_data() -> Dict[str, pd.DataFrame]:
    """Create sample CSV data for testing"""
    
    # Sample concerns data
    concerns_data = {
        'concern_id': ['acne', 'dryness', 'oily', 'aging', 'dark_spots'],
        'name': ['Acne', 'Dryness', 'Oily Skin', 'Aging', 'Dark Spots'],
        'category': ['SKIN', 'SKIN', 'SKIN', 'SKIN', 'SKIN'],
        'keywords': [
            'acne,pimples,breakouts,spots,blemishes',
            'dry,dehydrated,flaky,tight,rough',
            'oily,greasy,shiny,excess oil',
            'wrinkles,fine lines,aging,anti-aging',
            'dark spots,hyperpigmentation,age spots'
        ]
    }
    
    # Sample ingredients data
    ingredients_data = {
        'ingredient_id': ['salicylic_acid', 'hyaluronic_acid', 'niacinamide', 'retinol', 'vitamin_c'],
        'name': ['Salicylic Acid', 'Hyaluronic Acid', 'Niacinamide', 'Retinol', 'Vitamin C'],
        'benefits': [
            'Unclogs pores,Reduces acne',
            'Hydrates skin,Plumps skin',
            'Controls oil,Minimizes pores',
            'Reduces wrinkles,Improves texture',
            'Brightens skin,Fades dark spots'
        ],
        'safety_rating': ['SAFE', 'SAFE', 'SAFE', 'CAUTION', 'SAFE'],
        'safety_notes': ['', '', '', 'Use at night only', '']
    }
    
    # Sample concern-ingredient mappings
    mappings_data = {
        'concern_id': ['acne', 'acne', 'dryness', 'oily', 'oily', 'aging', 'dark_spots'],
        'ingredient_id': ['salicylic_acid', 'niacinamide', 'hyaluronic_acid', 'niacinamide', 'salicylic_acid', 'retinol', 'vitamin_c']
    }
    
    # Sample educational content
    educational_data = {
        'concern_id': ['acne', 'dryness', 'oily', 'aging', 'dark_spots'],
        'title': [
            'Understanding Acne',
            'Dealing with Dry Skin',
            'Managing Oily Skin',
            'Anti-Aging Skincare',
            'Treating Dark Spots'
        ],
        'description': [
            'Acne occurs when pores become clogged with oil and dead skin cells.',
            'Dry skin lacks moisture and can feel tight and uncomfortable.',
            'Oily skin produces excess sebum, leading to shine and enlarged pores.',
            'Aging skin shows signs of wrinkles, fine lines, and loss of elasticity.',
            'Dark spots are areas of hyperpigmentation caused by sun damage or acne.'
        ],
        'explanation': [
            'Regular cleansing and targeted treatments can help manage acne effectively.',
            'Gentle moisturizing and avoiding harsh products can restore skin barrier.',
            'Oil control and pore-minimizing ingredients can balance oily skin.',
            'Retinoids and antioxidants can help reduce signs of aging.',
            'Brightening ingredients and sun protection can fade dark spots.'
        ],
        'tips': [
            'Use gentle cleansers|Avoid over-washing|Apply spot treatments',
            'Use cream-based products|Avoid alcohol-based toners|Apply moisturizer while damp',
            'Use oil-free products|Blot excess oil|Use clay masks weekly',
            'Start retinoids slowly|Always use sunscreen|Be patient with results',
            'Use vitamin C serum|Apply sunscreen daily|Consider professional treatments'
        ]
    }
    
    # Sample products data
    products_data = {
        'product_id': ['prod_001', 'prod_002', 'prod_003', 'prod_004', 'prod_005'],
        'name': [
            'Clear Skin Cleanser',
            'Hydrating Serum',
            'Oil Control Moisturizer',
            'Anti-Aging Cream',
            'Brightening Serum'
        ],
        'price': [25.99, 45.00, 32.50, 89.99, 55.00],
        'rating': [4.2, 4.5, 4.1, 4.7, 4.3],
        'category': ['skincare', 'skincare', 'skincare', 'skincare', 'skincare'],
        'image_url': [
            'https://example.com/cleanser.jpg',
            'https://example.com/serum.jpg',
            'https://example.com/moisturizer.jpg',
            'https://example.com/cream.jpg',
            'https://example.com/brightening.jpg'
        ]
    }
    
    # Sample reviews data
    reviews_data = {
        'review_id': ['rev_001', 'rev_002', 'rev_003', 'rev_004', 'rev_005'],
        'product_id': ['prod_001', 'prod_002', 'prod_003', 'prod_004', 'prod_005'],
        'review_text': [
            'Great cleanser for acne-prone skin! Really helped clear my breakouts.',
            'Amazing hydrating serum. My dry skin feels so much better.',
            'Perfect for oily skin. Controls shine without over-drying.',
            'Expensive but worth it. Noticed reduction in fine lines after 6 weeks.',
            'Effective brightening serum. Dark spots are fading gradually.'
        ],
        'rating': [4.0, 5.0, 4.0, 5.0, 4.0],
        'reviewer_info': ['Sarah, 25', 'Mike, 35', 'Lisa, 28', 'Jennifer, 42', 'David, 30']
    }
    
    # Sample product-ingredient mappings
    product_ingredients_data = {
        'product_id': ['prod_001', 'prod_001', 'prod_002', 'prod_003', 'prod_004', 'prod_005'],
        'ingredient_id': ['salicylic_acid', 'niacinamide', 'hyaluronic_acid', 'niacinamide', 'retinol', 'vitamin_c']
    }
    
    return {
        'concerns': pd.DataFrame(concerns_data),
        'ingredients': pd.DataFrame(ingredients_data),
        'concern_ingredient_mapping': pd.DataFrame(mappings_data),
        'educational_content': pd.DataFrame(educational_data),
        'products': pd.DataFrame(products_data),
        'reviews': pd.DataFrame(reviews_data),
        'product_ingredients': pd.DataFrame(product_ingredients_data)
    }


def setup_application_service() -> ConcernChatApplicationService:
    """Set up the application service with repositories and sample data"""
    
    # Create repositories
    conversation_repo = InMemoryConcernConversationRepository()
    knowledge_repo = InMemoryConcernKnowledgeRepository()
    product_repo = InMemoryProductRepository()
    event_store = InMemoryEventStore()
    
    # Create application service
    app_service = ConcernChatApplicationService(
        conversation_repo=conversation_repo,
        knowledge_repo=knowledge_repo,
        product_repo=product_repo,
        event_store=event_store
    )
    
    # Load sample data
    csv_data = create_sample_csv_data()
    app_service.load_concern_data(csv_data)
    
    return app_service


def demo_basic_conversation():
    """Demonstrate basic conversation flow"""
    print("=== Demo: Basic Conversation Flow ===")
    
    app_service = setup_application_service()
    
    # Start conversation
    conversation_id = app_service.start_concern_conversation(user_id="user_123")
    print(f"Started conversation: {conversation_id}")
    
    # Test messages
    test_messages = [
        "I have acne problems on my face",
        "My skin is very dry and flaky",
        "I'm dealing with oily skin and large pores"
    ]
    
    for message in test_messages:
        print(f"\nUser: {message}")
        
        response = app_service.process_concern_message(conversation_id, message)
        
        print(f"Bot: {response.bot_message}")
        print(f"Concerns detected: {response.concerns_detected}")
        print(f"Confidence scores: {response.confidence_scores}")
        print(f"Has educational content: {response.has_educational_content}")
        print(f"Has natural remedies: {response.has_natural_remedies}")
    
    # Get conversation summary
    summary = app_service.get_conversation_summary(conversation_id)
    print(f"\nConversation Summary:")
    print(f"- Total messages: {summary.total_messages}")
    print(f"- Concerns discussed: {summary.concerns_discussed}")
    print(f"- Is active: {summary.is_active}")
    
    # End conversation
    app_service.end_conversation(conversation_id)
    print(f"\nConversation ended")


def demo_concern_detection():
    """Demonstrate concern detection capabilities"""
    print("\n=== Demo: Concern Detection ===")
    
    app_service = setup_application_service()
    knowledge_base = app_service.knowledge_base
    detection_service = app_service.concern_detection_service
    
    test_messages = [
        "I have terrible acne and pimples all over my face",
        "My skin feels so dry and tight after washing",
        "I have an oily T-zone with visible pores",
        "I'm starting to see fine lines around my eyes",
        "I have dark spots from old acne scars"
    ]
    
    for message in test_messages:
        print(f"\nMessage: '{message}'")
        
        message_content = MessageContent(message)
        detected_concerns = detection_service.detect_concerns(message_content)
        
        if detected_concerns:
            for concern in detected_concerns:
                print(f"- Concern: {concern.concern_type.name}")
                print(f"  Category: {concern.concern_type.category}")
                print(f"  Confidence: {concern.confidence_score.value:.2f}")
                print(f"  Keywords: {[kw.word for kw in concern.extracted_keywords[:3]]}")
        else:
            print("- No concerns detected")


def demo_product_search():
    """Demonstrate product search functionality"""
    print("\n=== Demo: Product Search ===")
    
    app_service = setup_application_service()
    
    concerns = ['acne', 'dryness', 'oily', 'aging', 'dark spots']
    
    for concern in concerns:
        print(f"\nSearching products for '{concern}':")
        products = app_service.search_products_by_concern(concern, limit=3)
        
        if products:
            for product in products:
                print(f"- {product['name']} (${product['price']:.2f}) - {product['rating']}/5 stars")
        else:
            print("- No products found")


def demo_educational_content():
    """Demonstrate educational content retrieval"""
    print("\n=== Demo: Educational Content ===")
    
    app_service = setup_application_service()
    
    concerns = ['acne', 'dryness', 'aging']
    
    for concern in concerns:
        print(f"\nEducational content for '{concern}':")
        content = app_service.get_educational_content_for_concern(concern)
        
        if content:
            print(f"- Title: {content['title']}")
            print(f"- Description: {content['description']}")
            print(f"- Tips: {', '.join(content['tips'][:2])}")
        else:
            print("- No educational content found")


def demo_analytics():
    """Demonstrate analytics capabilities"""
    print("\n=== Demo: Analytics ===")
    
    app_service = setup_application_service()
    
    # Create some sample conversations
    for i in range(3):
        conv_id = app_service.start_concern_conversation(f"user_{i}")
        app_service.process_concern_message(conv_id, "I have acne problems")
        app_service.process_concern_message(conv_id, "My skin is also very dry")
        if i < 2:  # End some conversations
            app_service.end_conversation(conv_id)
    
    # Get analytics
    analytics = app_service.get_analytics_summary()
    print(f"Analytics Summary:")
    print(f"- Total conversations: {analytics.get('total_conversations', 0)}")
    print(f"- Total messages: {analytics.get('total_messages', 0)}")
    print(f"- Total concerns detected: {analytics.get('total_concerns_detected', 0)}")
    print(f"- Average messages per conversation: {analytics.get('average_messages_per_conversation', 0):.1f}")
    
    # Get active conversations
    active_convs = app_service.get_active_conversations()
    print(f"- Active conversations: {len(active_convs)}")


def demo_system_health():
    """Demonstrate system health validation"""
    print("\n=== Demo: System Health Check ===")
    
    app_service = setup_application_service()
    
    health_status = app_service.validate_system_health()
    
    print("System Health Status:")
    for component, status in health_status.items():
        status_text = "✓ OK" if status else "✗ FAILED"
        print(f"- {component}: {status_text}")


def main():
    """Run all demo scenarios"""
    print("🚀 Beauty Recommendation Chatbot - DDD Domain Model Demo")
    print("=" * 60)
    
    try:
        # Run all demos
        demo_basic_conversation()
        demo_concern_detection()
        demo_product_search()
        demo_educational_content()
        demo_analytics()
        demo_system_health()
        
        print("\n" + "=" * 60)
        print("✅ All demos completed successfully!")
        print("\nThe DDD domain model is working correctly and ready for integration.")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
