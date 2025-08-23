# Product Catalogue Structure

## Overview
This document defines the structure for the 24K product database and reviews integration for the AI virtual salesperson chatbot.

## Product Catalogue CSV Structure

### Required Fields
```csv
product_name,product_id,brand_name,canonical_l1,canonical_l3,ingredients,concerns,mrp
```

### Field Definitions

#### 1. product_name
- **Type**: String
- **Description**: Full product name as displayed to customers
- **Example**: "CeraVe Hydrating Foaming Oil Cleanser"
- **Usage**: Display name, search functionality

#### 2. product_id
- **Type**: Unique Identifier (String/Integer)
- **Description**: Unique identifier for linking with reviews
- **Example**: "PROD_12345" or "12345"
- **Usage**: Primary key, review matching, Nykaa URL generation

#### 3. brand_name
- **Type**: String
- **Description**: Brand/manufacturer name
- **Example**: "CeraVe", "The Ordinary", "Nykaa Cosmetics"
- **Usage**: Brand filtering, display, recommendations

#### 4. canonical_l1
- **Type**: Enum
- **Options**: ["Skin", "Hair", "Makeup"]
- **Description**: Primary category classification
- **Usage**: Main category filtering

#### 5. canonical_l3
- **Type**: String
- **Description**: Sub-category classification (acts as sub-category)
- **Examples**: 
  - Skin: "Cleanser", "Moisturizer", "Serum", "Sunscreen", "Toner"
  - Hair: "Shampoo", "Conditioner", "Hair Oil", "Hair Mask", "Styling"
  - Makeup: "Foundation", "Lipstick", "Eyeshadow", "Mascara", "Blush"
- **Usage**: Detailed product filtering, routine building

#### 6. ingredients
- **Type**: String (comma-separated or JSON)
- **Description**: Active ingredients and key components
- **Example**: "Hyaluronic Acid, Ceramides, Niacinamide"
- **Usage**: Ingredient matching, concern targeting, education

#### 7. concerns
- **Type**: String (comma-separated)
- **Description**: Beauty concerns this product addresses
- **Example**: "Acne, Oiliness, Pores"
- **Usage**: Concern-based filtering and recommendations

#### 8. mrp (Maximum Retail Price)
- **Type**: Decimal/Float
- **Description**: Product price in local currency
- **Example**: 1299.00
- **Usage**: Budget filtering, cost calculations

## Reviews CSV Structure

### Required Fields
```csv
product_id,review_text,rating,reviewer_age_group,skin_type,review_sentiment
```

### Field Definitions

#### 1. product_id
- **Type**: String/Integer (matches product catalogue)
- **Description**: Links review to specific product
- **Usage**: Review-product matching

#### 2. review_text
- **Type**: String
- **Description**: Customer review content
- **Usage**: Sentiment analysis, review display, AI summarization

#### 3. rating
- **Type**: Integer (1-5)
- **Description**: Star rating given by reviewer
- **Usage**: Product scoring, filtering positive reviews

#### 4. reviewer_age_group
- **Type**: Enum
- **Options**: ["Teens (13-19)", "Young Adults (20-29)", "Adults (30-39)", "Mature (40+)"]
- **Description**: Age group of reviewer
- **Usage**: Age-relevant review filtering

#### 5. skin_type
- **Type**: Enum
- **Options**: ["Dry", "Oily", "Combination", "Balanced", "Not Specified"]
- **Description**: Reviewer's skin type
- **Usage**: Skin-type specific review filtering

#### 6. review_sentiment
- **Type**: Enum
- **Options**: ["Positive", "Neutral", "Negative"]
- **Description**: Pre-computed or AI-analyzed sentiment
- **Usage**: Quick positive review filtering

## Data Integration Logic

### 1. Product-Review Linking
```python
# Pseudo-code for linking
products = load_csv("product_catalogue.csv")
reviews = load_csv("reviews.csv")

for product in products:
    product_reviews = reviews.filter(product_id == product.product_id)
    positive_reviews = product_reviews.filter(sentiment == "Positive")
    relevant_reviews = filter_by_customer_profile(positive_reviews)
```

### 2. Recommendation Algorithm
```
1. Filter products by canonical_l1 (category)
2. Filter by canonical_l3 (sub-category) based on concerns
3. Match ingredients to customer profile
4. Apply budget constraints (if provided)
5. Score products based on:
   - Concern relevance
   - Ingredient match
   - Age-appropriate reviews
   - Overall rating
6. Select top N products
7. Attach relevant positive reviews
```

### 3. Nykaa Integration
```python
# URL generation for product images and links
def generate_nykaa_url(product_id, product_name):
    base_url = "https://www.nykaa.com/"
    # Generate URL based on product_id and name
    return f"{base_url}product/{product_id}"
```

## Data Quality Requirements

### Product Catalogue
- All required fields must be populated
- canonical_l1 must be valid enum value
- canonical_l3 should be consistent within categories
- Ingredients should be properly formatted
- MRP should be valid positive number

### Reviews
- product_id must exist in product catalogue
- Rating must be 1-5 integer
- Review text should be meaningful (not empty)
- Sentiment should be pre-computed for performance

## Performance Considerations

### Indexing Strategy
- Index on product_id for fast lookups
- Index on canonical_l1 and canonical_l3 for filtering
- Index on concerns for concern-based search
- Index on MRP for budget filtering

### Caching Strategy
- Cache frequently accessed products
- Cache positive reviews by product
- Cache ingredient mappings
- Pre-compute recommendation scores

## Sample Data Structure

### Product Example
```csv
"CeraVe Hydrating Cleanser",PROD_001,"CeraVe","Skin","Cleanser","Hyaluronic Acid,Ceramides","Dryness,Dull skin",899.00
```

### Review Example
```csv
PROD_001,"Amazing cleanser! Perfect for my dry skin. Leaves skin soft and hydrated.",5,"Young Adults (20-29)","Dry","Positive"
```
