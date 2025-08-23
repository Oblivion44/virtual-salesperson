"""
Repositories for Concern-Based Chat Domain
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from datetime import datetime

from value_objects import ConversationId, UserId, ConcernType, Timestamp
from aggregates import ConcernConversation, ConcernKnowledgeBase
from entities import Product, Review, Ingredient, EducationalContent
from value_objects import Keyword, Benefit, SafetyRating, ProductId


class ConcernConversationRepository(ABC):
    """Repository interface for concern-based conversations"""
    
    @abstractmethod
    def save(self, conversation: ConcernConversation) -> None:
        """Save a conversation"""
        pass
    
    @abstractmethod
    def find_by_id(self, conversation_id: ConversationId) -> Optional[ConcernConversation]:
        """Find conversation by ID"""
        pass
    
    @abstractmethod
    def find_active_conversations(self) -> List[ConcernConversation]:
        """Find all active conversations"""
        pass
    
    @abstractmethod
    def find_by_user_id(self, user_id: UserId) -> List[ConcernConversation]:
        """Find conversations by user ID"""
        pass
    
    @abstractmethod
    def delete(self, conversation_id: ConversationId) -> None:
        """Delete a conversation"""
        pass


class ConcernKnowledgeRepository(ABC):
    """Repository interface for concern knowledge base"""
    
    @abstractmethod
    def save(self, knowledge_base: ConcernKnowledgeBase) -> None:
        """Save knowledge base"""
        pass
    
    @abstractmethod
    def find_by_id(self, knowledge_base_id: str) -> Optional[ConcernKnowledgeBase]:
        """Find knowledge base by ID"""
        pass
    
    @abstractmethod
    def find_concerns_by_keywords(self, keywords: List[str]) -> List[ConcernType]:
        """Find concerns matching keywords"""
        pass
    
    @abstractmethod
    def find_ingredients_by_concern(self, concern_id: str) -> List[Ingredient]:
        """Find ingredients for a concern"""
        pass
    
    @abstractmethod
    def find_educational_content(self, concern_id: str) -> Optional[EducationalContent]:
        """Find educational content for a concern"""
        pass
    
    @abstractmethod
    def load_from_csv(self, csv_data: Dict[str, any]) -> ConcernKnowledgeBase:
        """Load knowledge base from CSV data"""
        pass


class ProductRepository(ABC):
    """Repository interface for products"""
    
    @abstractmethod
    def find_by_id(self, product_id: ProductId) -> Optional[Product]:
        """Find product by ID"""
        pass
    
    @abstractmethod
    def find_by_ingredients(self, ingredient_ids: List[str]) -> List[Product]:
        """Find products containing specific ingredients"""
        pass
    
    @abstractmethod
    def find_by_category(self, category: str) -> List[Product]:
        """Find products by category"""
        pass
    
    @abstractmethod
    def find_reviews(self, product_id: ProductId) -> List[Review]:
        """Find reviews for a product"""
        pass


# In-Memory Implementations

class InMemoryConcernConversationRepository(ConcernConversationRepository):
    """In-memory implementation of conversation repository"""
    
    def __init__(self):
        self._conversations: Dict[str, ConcernConversation] = {}
    
    def save(self, conversation: ConcernConversation) -> None:
        """Save a conversation"""
        self._conversations[conversation.conversation_id.value] = conversation
    
    def find_by_id(self, conversation_id: ConversationId) -> Optional[ConcernConversation]:
        """Find conversation by ID"""
        return self._conversations.get(conversation_id.value)
    
    def find_active_conversations(self) -> List[ConcernConversation]:
        """Find all active conversations"""
        return [conv for conv in self._conversations.values() if conv.is_active()]
    
    def find_by_user_id(self, user_id: UserId) -> List[ConcernConversation]:
        """Find conversations by user ID"""
        return [
            conv for conv in self._conversations.values() 
            if conv.user_id and conv.user_id.value == user_id.value
        ]
    
    def delete(self, conversation_id: ConversationId) -> None:
        """Delete a conversation"""
        if conversation_id.value in self._conversations:
            del self._conversations[conversation_id.value]
    
    def get_all(self) -> List[ConcernConversation]:
        """Get all conversations (for testing/analytics)"""
        return list(self._conversations.values())
    
    def clear(self) -> None:
        """Clear all conversations (for testing)"""
        self._conversations.clear()


class InMemoryConcernKnowledgeRepository(ConcernKnowledgeRepository):
    """In-memory implementation of knowledge repository"""
    
    def __init__(self):
        self._knowledge_bases: Dict[str, ConcernKnowledgeBase] = {}
        self._default_kb_id = "default"
    
    def save(self, knowledge_base: ConcernKnowledgeBase) -> None:
        """Save knowledge base"""
        self._knowledge_bases[knowledge_base.knowledge_base_id] = knowledge_base
    
    def find_by_id(self, knowledge_base_id: str) -> Optional[ConcernKnowledgeBase]:
        """Find knowledge base by ID"""
        return self._knowledge_bases.get(knowledge_base_id)
    
    def get_default(self) -> ConcernKnowledgeBase:
        """Get or create default knowledge base"""
        if self._default_kb_id not in self._knowledge_bases:
            self._knowledge_bases[self._default_kb_id] = ConcernKnowledgeBase(self._default_kb_id)
        return self._knowledge_bases[self._default_kb_id]
    
    def find_concerns_by_keywords(self, keywords: List[str]) -> List[ConcernType]:
        """Find concerns matching keywords"""
        kb = self.get_default()
        return kb.find_concerns_by_keywords(keywords)
    
    def find_ingredients_by_concern(self, concern_id: str) -> List[Ingredient]:
        """Find ingredients for a concern"""
        kb = self.get_default()
        return kb.get_ingredients_for_concern(concern_id)
    
    def find_educational_content(self, concern_id: str) -> Optional[EducationalContent]:
        """Find educational content for a concern"""
        kb = self.get_default()
        return kb.get_educational_content(concern_id)
    
    def load_from_csv(self, csv_data: Dict[str, any]) -> ConcernKnowledgeBase:
        """Load knowledge base from CSV data"""
        kb = self.get_default()
        
        # Load concerns
        if 'concerns' in csv_data:
            self._load_concerns_from_csv(kb, csv_data['concerns'])
        
        # Load ingredients
        if 'ingredients' in csv_data:
            self._load_ingredients_from_csv(kb, csv_data['ingredients'])
        
        # Load educational content
        if 'educational_content' in csv_data:
            self._load_educational_content_from_csv(kb, csv_data['educational_content'])
        
        # Load concern-ingredient mappings
        if 'concern_ingredient_mapping' in csv_data:
            self._load_mappings_from_csv(kb, csv_data['concern_ingredient_mapping'])
        
        self.save(kb)
        return kb
    
    def _load_concerns_from_csv(self, kb: ConcernKnowledgeBase, data: any) -> None:
        """Load concerns from CSV data"""
        # Simplified implementation for testing
        pass
    
    def _load_ingredients_from_csv(self, kb: ConcernKnowledgeBase, data: any) -> None:
        """Load ingredients from CSV data"""
        # Simplified implementation for testing
        pass
    
    def _load_educational_content_from_csv(self, kb: ConcernKnowledgeBase, data: any) -> None:
        """Load educational content from CSV data"""
        # Simplified implementation for testing
        pass
    
    def _load_mappings_from_csv(self, kb: ConcernKnowledgeBase, data: any) -> None:
        """Load concern-ingredient mappings from CSV data"""
        # Simplified implementation for testing
        pass


class InMemoryProductRepository(ProductRepository):
    """In-memory implementation of product repository"""
    
    def __init__(self):
        self._products: Dict[str, Product] = {}
        self._reviews: Dict[str, List[Review]] = {}
        self._product_ingredients: Dict[str, List[str]] = {}  # product_id -> ingredient_ids
    
    def find_by_id(self, product_id: ProductId) -> Optional[Product]:
        """Find product by ID"""
        return self._products.get(product_id.value)
    
    def find_by_ingredients(self, ingredient_ids: List[str]) -> List[Product]:
        """Find products containing specific ingredients"""
        matching_products = []
        
        for product_id, product_ingredient_ids in self._product_ingredients.items():
            if any(ing_id in product_ingredient_ids for ing_id in ingredient_ids):
                product = self._products.get(product_id)
                if product:
                    matching_products.append(product)
        
        return matching_products
    
    def find_by_category(self, category: str) -> List[Product]:
        """Find products by category"""
        return [
            product for product in self._products.values() 
            if product.category.lower() == category.lower()
        ]
    
    def find_reviews(self, product_id: ProductId) -> List[Review]:
        """Find reviews for a product"""
        return self._reviews.get(product_id.value, [])
    
    def add_product(self, product: Product) -> None:
        """Add a product (for testing/setup)"""
        self._products[product.product_id.value] = product
    
    def add_review(self, review: Review) -> None:
        """Add a review (for testing/setup)"""
        product_id = review.product_id.value
        if product_id not in self._reviews:
            self._reviews[product_id] = []
        self._reviews[product_id].append(review)
    
    def set_product_ingredients(self, product_id: str, ingredient_ids: List[str]) -> None:
        """Set ingredients for a product (for testing/setup)"""
        self._product_ingredients[product_id] = ingredient_ids
    
    def load_from_csv(self, csv_data: Dict[str, any]) -> None:
        """Load products from CSV data"""
        # Simplified implementation for testing
        pass
    
    def _load_products_from_csv(self, data: any) -> None:
        """Load products from CSV data"""
        # Simplified implementation for testing
        pass
    
    def _load_reviews_from_csv(self, data: any) -> None:
        """Load reviews from CSV data"""
        # Simplified implementation for testing
        pass
    
    def _load_product_ingredients_from_csv(self, data: any) -> None:
        """Load product-ingredient mappings from CSV data"""
        # Simplified implementation for testing
        pass
    
    def clear(self) -> None:
        """Clear all data (for testing)"""
        self._products.clear()
        self._reviews.clear()
        self._product_ingredients.clear()
    
    def get_all_products(self) -> List[Product]:
        """Get all products (for testing/analytics)"""
        return list(self._products.values())
