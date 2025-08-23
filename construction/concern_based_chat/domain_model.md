# Concern-Based Chat Unit - Domain Model

## Domain Overview
The Concern-Based Chat Unit is responsible for handling user conversations related to specific beauty concerns. It processes natural language input, detects beauty-related concerns, and provides targeted product recommendations along with educational content and natural remedies.

## Bounded Context Definition
This bounded context focuses on:
- Processing concern-based user messages
- Mapping beauty concerns to ingredients and products
- Generating educational responses about beauty concerns
- Integrating product recommendations with natural remedies
- Managing conversation flow for concern-based interactions

## Domain Model Components

### Aggregates

#### 1. ConcernConversation (Aggregate Root)
**Purpose**: Manages the complete lifecycle of a concern-based conversation
**Invariants**:
- Must have at least one user message to be valid
- Cannot have more than 100 messages per conversation
- Must maintain chronological order of messages
- Each concern detection must be linked to appropriate recommendations

**Entities**:
- `ConversationId` (Identity)
- `UserId` (optional)
- `Messages` (Collection of Message entities)
- `DetectedConcerns` (Collection of DetectedConcern entities)
- `ConversationState` (Value Object)
- `CreatedAt`, `LastUpdatedAt` (Timestamps)

**Business Methods**:
- `addUserMessage(content: string): MessageId`
- `addBotResponse(response: BotResponse): MessageId`
- `detectConcerns(message: string): List<DetectedConcern>`
- `generateResponse(concerns: List<DetectedConcern>): BotResponse`
- `isActive(): boolean`
- `endConversation(): void`

#### 2. ConcernKnowledgeBase (Aggregate Root)
**Purpose**: Manages the mapping between concerns, ingredients, and educational content
**Invariants**:
- Each concern must have at least one associated ingredient
- Ingredient mappings must be validated and approved
- Educational content must be present for each concern

**Entities**:
- `ConcernId` (Identity)
- `ConcernName` (Value Object)
- `AssociatedIngredients` (Collection of Ingredient entities)
- `EducationalContent` (Entity)
- `Keywords` (Collection of Keyword value objects)

**Business Methods**:
- `findConcernsByKeywords(keywords: List<string>): List<Concern>`
- `getIngredientsForConcern(concernId: ConcernId): List<Ingredient>`
- `getEducationalContent(concernId: ConcernId): EducationalContent`
- `addConcernMapping(concern: Concern, ingredients: List<Ingredient>): void`

### Entities

#### Message
**Purpose**: Represents individual messages in a conversation
**Attributes**:
- `MessageId` (Identity)
- `Content` (Value Object)
- `MessageType` (Value Object: USER, BOT)
- `Timestamp` (Value Object)
- `ProcessingStatus` (Value Object: PENDING, PROCESSED, FAILED)

#### DetectedConcern
**Purpose**: Represents a beauty concern identified from user input
**Attributes**:
- `DetectedConcernId` (Identity)
- `ConcernType` (Value Object)
- `ConfidenceScore` (Value Object: 0.0-1.0)
- `ExtractedKeywords` (Collection of Keyword value objects)
- `DetectedAt` (Timestamp)

#### Ingredient
**Purpose**: Represents beauty ingredients that address specific concerns
**Attributes**:
- `IngredientId` (Identity)
- `Name` (Value Object)
- `Benefits` (Collection of Benefit value objects)
- `ConcernTypes` (Collection of ConcernType value objects)
- `SafetyRating` (Value Object)

#### EducationalContent
**Purpose**: Contains educational information about beauty concerns
**Attributes**:
- `ContentId` (Identity)
- `Title` (Value Object)
- `Description` (Value Object)
- `Explanation` (Value Object)
- `Tips` (Collection of Tip value objects)
- `LastUpdated` (Timestamp)

### Value Objects

#### ConversationId
```python
@dataclass(frozen=True)
class ConversationId:
    value: str
    
    def __post_init__(self):
        if not self.value or len(self.value) < 8:
            raise ValueError("ConversationId must be at least 8 characters")
```

#### MessageContent
```python
@dataclass(frozen=True)
class MessageContent:
    text: str
    
    def __post_init__(self):
        if not self.text or len(self.text.strip()) == 0:
            raise ValueError("Message content cannot be empty")
        if len(self.text) > 1000:
            raise ValueError("Message content too long")
```

#### ConcernType
```python
@dataclass(frozen=True)
class ConcernType:
    name: str
    category: str  # SKIN, HAIR, GENERAL
    
    def __post_init__(self):
        valid_categories = ["SKIN", "HAIR", "GENERAL"]
        if self.category not in valid_categories:
            raise ValueError(f"Invalid category: {self.category}")
```

#### ConfidenceScore
```python
@dataclass(frozen=True)
class ConfidenceScore:
    value: float
    
    def __post_init__(self):
        if not 0.0 <= self.value <= 1.0:
            raise ValueError("Confidence score must be between 0.0 and 1.0")
```

#### ConversationState
```python
@dataclass(frozen=True)
class ConversationState:
    status: str  # ACTIVE, ENDED, PAUSED
    last_intent: str  # CONCERN, EXPLORATION, CHITCHAT
    
    def __post_init__(self):
        valid_statuses = ["ACTIVE", "ENDED", "PAUSED"]
        if self.status not in valid_statuses:
            raise ValueError(f"Invalid status: {self.status}")
```

### Domain Services

#### ConcernDetectionService
**Purpose**: Analyzes user messages to identify beauty concerns
**Methods**:
- `detectConcerns(message: MessageContent) -> List[DetectedConcern]`
- `extractKeywords(text: str) -> List[Keyword]`
- `calculateConfidence(keywords: List[Keyword], concern: ConcernType) -> ConfidenceScore`

#### ResponseGenerationService
**Purpose**: Creates comprehensive responses for detected concerns
**Methods**:
- `generateConcernResponse(concerns: List[DetectedConcern]) -> BotResponse`
- `formatEducationalContent(content: EducationalContent) -> str`
- `combineProductAndRemedyRecommendations(products: List[Product], remedies: List[Remedy]) -> str`

#### ConcernMappingService
**Purpose**: Maps detected concerns to ingredients and products
**Methods**:
- `mapConcernsToIngredients(concerns: List[DetectedConcern]) -> List[Ingredient]`
- `findRelevantProducts(ingredients: List[Ingredient]) -> List[ProductId]`
- `prioritizeRecommendations(products: List[Product], userProfile: UserProfile) -> List[Product]`

### Repositories

#### ConcernConversationRepository
**Purpose**: Manages persistence of concern-based conversations
**Methods**:
- `save(conversation: ConcernConversation) -> void`
- `findById(id: ConversationId) -> Optional[ConcernConversation]`
- `findActiveConversations() -> List[ConcernConversation]`
- `findByUserId(userId: UserId) -> List[ConcernConversation]`

#### ConcernKnowledgeRepository
**Purpose**: Manages concern-ingredient mappings and educational content
**Methods**:
- `findConcernsByKeywords(keywords: List[str]) -> List[Concern]`
- `findIngredientsByConcern(concernId: ConcernId) -> List[Ingredient]`
- `findEducationalContent(concernId: ConcernId) -> Optional[EducationalContent]`
- `loadFromCSV(csvData: CSVData) -> void`

### Domain Events

#### ConcernDetectedEvent
```python
@dataclass(frozen=True)
class ConcernDetectedEvent:
    conversation_id: ConversationId
    detected_concerns: List[DetectedConcern]
    user_message: MessageContent
    detected_at: datetime
    
    def __post_init__(self):
        if not self.detected_concerns:
            raise ValueError("Must have at least one detected concern")
```

#### ResponseGeneratedEvent
```python
@dataclass(frozen=True)
class ResponseGeneratedEvent:
    conversation_id: ConversationId
    response_content: MessageContent
    concerns_addressed: List[ConcernType]
    products_recommended: List[ProductId]
    generated_at: datetime
```

#### ConversationStartedEvent
```python
@dataclass(frozen=True)
class ConversationStartedEvent:
    conversation_id: ConversationId
    user_id: Optional[UserId]
    started_at: datetime
```

### Policies

#### ConcernPrioritizationPolicy
**Purpose**: Determines which concerns to address first when multiple are detected
**Rules**:
- Skin concerns take priority over hair concerns
- Higher confidence scores get priority
- Maximum 3 concerns addressed per response
- Severe concerns (acne, sensitivity) get immediate attention

#### ResponseLengthPolicy
**Purpose**: Ensures responses are comprehensive but not overwhelming
**Rules**:
- Educational content: 2-3 sentences maximum
- Product recommendations: Top 3 products only
- Natural remedies: 1-2 remedies maximum
- Total response length: Under 500 words

#### DataValidationPolicy
**Purpose**: Ensures data integrity for CSV imports
**Rules**:
- All concern names must be lowercase and standardized
- Ingredient names must be validated against approved list
- Product IDs must exist in product database
- Confidence thresholds must be calibrated regularly

### Application Services

#### ConcernChatApplicationService
**Purpose**: Orchestrates the concern-based chat workflow
**Methods**:
- `processConcernMessage(conversationId: ConversationId, message: str) -> ChatResponse`
- `startConcernConversation(userId: Optional[UserId]) -> ConversationId`
- `loadConcernData(csvFiles: Dict[str, CSVData]) -> void`

### Integration Points

#### External Dependencies
- **Product Catalog Service**: For retrieving product details and reviews
- **Natural Remedies Service**: For getting home remedy recommendations
- **User Profile Service**: For personalization data
- **Analytics Service**: For tracking conversation metrics

#### Data Sources (CSV Integration)
- **concerns.csv**: Concern types, keywords, categories
- **ingredients.csv**: Ingredient names, benefits, safety ratings
- **concern_ingredient_mapping.csv**: Mappings between concerns and ingredients
- **educational_content.csv**: Educational information for each concern
- **products.csv**: Product details, ratings, reviews
- **product_ingredients.csv**: Product-ingredient relationships

### Business Rules

1. **Concern Detection Rules**:
   - Minimum confidence score of 0.6 required for concern detection
   - Multiple concerns can be detected from a single message
   - Unknown concerns should trigger clarification questions

2. **Response Generation Rules**:
   - Always provide educational content before product recommendations
   - Include both commercial products and natural remedies
   - Personalize recommendations based on user profile when available

3. **Data Integrity Rules**:
   - All CSV data must be validated before loading
   - Concern-ingredient mappings must be bidirectional
   - Educational content must be reviewed and approved

4. **Conversation Flow Rules**:
   - Each concern detection must result in a comprehensive response
   - Follow-up questions should be encouraged
   - Conversation context must be maintained across messages

### Quality Attributes

- **Performance**: Concern detection within 200ms, response generation within 500ms
- **Accuracy**: Minimum 85% accuracy in concern detection
- **Maintainability**: Easy addition of new concerns and ingredients via CSV
- **Scalability**: Support for 1000+ concurrent conversations
- **Reliability**: Graceful handling of malformed input and missing data

## Implementation Notes

### CSV Data Structure Requirements
```
concerns.csv: concern_id, name, category, keywords
ingredients.csv: ingredient_id, name, benefits, safety_rating
concern_ingredient_mapping.csv: concern_id, ingredient_id, effectiveness_score
educational_content.csv: concern_id, title, description, explanation, tips
products.csv: product_id, name, price, rating, category, image_url
product_ingredients.csv: product_id, ingredient_id
reviews.csv: product_id, review_text, rating, reviewer_info
```

### Event Sourcing Considerations
- All domain events should be stored for audit trail
- Event replay capability for debugging and analytics
- Snapshot mechanism for conversation state recovery

### Testing Strategy
- Unit tests for all domain services and value objects
- Integration tests for CSV data loading
- End-to-end tests for complete conversation flows
- Property-based testing for concern detection accuracy
