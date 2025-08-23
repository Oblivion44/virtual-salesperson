# Product Recommendation Unit

## Overview
This bounded context is responsible for product discovery, recommendation algorithms, and product information management. It provides personalized product suggestions based on user concerns, preferences, and exploration requests.

## Bounded Context Scope
- Product recommendation algorithms and ranking
- Concern-to-ingredient-to-product mapping
- Product filtering and personalization
- Product detail management and display
- Review and rating integration

## User Stories Included

### US-006: Concern-Based Product Recommendations
**As a** user with specific beauty concerns  
**I want to** receive targeted product recommendations  
**So that** I can find effective solutions for my problems  

**Acceptance Criteria:**
- [ ] System maps concerns to relevant ingredients (salicylic acid for acne, hyaluronic acid for dryness, etc.)
- [ ] System retrieves products containing appropriate ingredients
- [ ] System filters products based on user profile (budget, skin type, etc.)
- [ ] System displays product details (name, price, rating, image, reviews)
- [ ] System explains why each product is recommended

### US-007: Top Product Discovery
**As a** user exploring product categories  
**I want to** see the best-rated products in each category  
**So that** I can discover high-quality options  

**Acceptance Criteria:**
- [ ] System displays top 4 products per category
- [ ] Products are ranked by rating and relevance
- [ ] Each product shows customer reviews
- [ ] Products are filtered by user preferences when available
- [ ] System provides variety across different price points

### US-008: Product Detail Viewing
**As a** user interested in a specific product  
**I want to** view detailed information about the product  
**So that** I can make an informed purchase decision  

**Acceptance Criteria:**
- [ ] System displays product in split-screen detailed view
- [ ] Detail view shows enlarged product image
- [ ] Detail view includes comprehensive product information
- [ ] Detail view shows customer reviews and ratings
- [ ] User can add product to cart from detail view
- [ ] User can close detail view and return to main interface

### US-014: Visual Product Display
**As a** user viewing product recommendations  
**I want to** see products in an attractive, informative format  
**So that** I can quickly evaluate and compare options  

**Acceptance Criteria:**
- [ ] Products are displayed as visually appealing cards
- [ ] Each product card shows image, name, price, rating, and review
- [ ] Product images are properly sized and formatted
- [ ] Cards have consistent styling and layout
- [ ] Action buttons (Add to Cart, View Details) are clearly visible
- [ ] Display works well across different screen sizes

## Domain Concepts

### Core Entities
- **Product**: Complete product information including details, pricing, and availability
- **ProductRecommendation**: A recommended product with reasoning and relevance score
- **ProductCategory**: Grouping of products (skincare, haircare, makeup)
- **Ingredient**: Active ingredients that address specific beauty concerns

### Value Objects
- **ProductId**: Unique identifier for products
- **Price**: Product pricing with currency
- **Rating**: Customer rating (1-5 scale) with review count
- **RecommendationScore**: Calculated relevance score for recommendations
- **ProductImage**: Image URL and metadata
- **Review**: Customer review text and rating

### Aggregates
- **ProductCatalog**: Root aggregate managing all products and their relationships
- **RecommendationEngine**: Root aggregate for recommendation algorithms and logic

### Domain Services
- **ConcernMappingService**: Maps beauty concerns to effective ingredients
- **ProductFilteringService**: Filters products based on user preferences
- **RecommendationRankingService**: Ranks and scores product recommendations
- **ProductSearchService**: Searches products by various criteria

### Repositories
- **ProductRepository**: Manages product data persistence and retrieval
- **IngredientRepository**: Stores ingredient information and mappings
- **ReviewRepository**: Manages customer reviews and ratings

### Domain Events
- **ProductRecommendationRequested**: When recommendations are requested
- **ProductRecommendationGenerated**: When recommendations are calculated
- **ProductDetailViewed**: When user views detailed product information
- **ProductFiltered**: When products are filtered by criteria

## External Dependencies
- **User Profile Unit**: For user preferences and personalization data
- **Data Management Unit**: For product data and ingredient mappings
- **Shopping Cart Unit**: For cart operations when products are selected

## Interface Contracts

### Inbound
- `getRecommendationsForConcern(concern: string, userProfile: UserProfile): ProductRecommendation[]`
- `getTopProductsByCategory(categories: string[], limit: number, userProfile?: UserProfile): Product[]`
- `getProductDetails(productId: ProductId): ProductDetail`
- `searchProducts(criteria: SearchCriteria, userProfile?: UserProfile): Product[]`

### Outbound
- `getUserProfile(userId: UserId): UserProfile`
- `addToCart(productId: ProductId, userId: UserId): void`

## Business Rules
1. Concern-based recommendations must include ingredient explanations
2. Product recommendations must be filtered by user budget when profile exists
3. Top product lists must include variety across price ranges
4. Products must have minimum rating threshold for recommendations (>3.0)
5. Ingredient mappings must be validated and evidence-based
6. Product images must be validated URLs or default placeholders
7. Reviews displayed must be the highest-rated for each product
8. Recommendations must be limited to available products only

## Recommendation Algorithm Rules
1. **Concern-Based Scoring**:
   - Ingredient match: 40% weight
   - User profile compatibility: 30% weight
   - Product rating: 20% weight
   - Price fit within budget: 10% weight

2. **Exploration-Based Scoring**:
   - Product rating: 50% weight
   - Category relevance: 30% weight
   - User profile match: 20% weight

3. **Filtering Priority**:
   - Budget constraints (hard filter)
   - Skin type compatibility (soft filter)
   - Availability (hard filter)
   - Minimum rating threshold (hard filter)

## Quality Attributes
- **Performance**: Recommendations must be generated within 1 second
- **Accuracy**: Ingredient mappings must be scientifically validated
- **Scalability**: System must handle large product catalogs efficiently
- **Maintainability**: Recommendation algorithms must be easily tunable
