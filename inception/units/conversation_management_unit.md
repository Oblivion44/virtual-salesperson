# Conversation Management Unit

## Overview
This bounded context is responsible for all conversational interactions between users and the beauty chatbot. It handles intent detection, conversation flow, and response generation while maintaining conversation context and history.

## Bounded Context Scope
- Natural language processing and intent classification
- Conversation flow management and context tracking
- Response generation and formatting
- Chat interface and user interaction handling
- Session management for conversations

## User Stories Included

### US-003: Concern-Based Conversation Handling
**As a** user with specific beauty concerns  
**I want to** describe my problems in natural language  
**So that** the chatbot can understand and provide targeted solutions  

**Acceptance Criteria:**
- [ ] System detects concern keywords (acne, dryness, oily, aging, dark spots, sensitive, dull, hair loss, dandruff, frizzy hair)
- [ ] System provides educational explanation about the detected concern
- [ ] System maps concerns to appropriate ingredients and products
- [ ] Response includes both product recommendations and natural remedies
- [ ] System handles multiple concerns in a single message

### US-004: Exploration-Based Conversation Handling
**As a** user exploring beauty products  
**I want to** ask for general recommendations without specific concerns  
**So that** I can discover new products and categories  

**Acceptance Criteria:**
- [ ] System detects exploration keywords (recommend, suggest, looking for, new product, etc.)
- [ ] System identifies product categories from user input (skincare, haircare, makeup)
- [ ] System displays top 4 products with reviews for identified categories
- [ ] System provides encouraging and helpful exploration messages

### US-005: Chit-Chat and Engagement
**As a** user having casual conversation  
**I want to** engage in friendly dialogue with the chatbot  
**So that** I feel comfortable and the interaction feels natural  

**Acceptance Criteria:**
- [ ] System recognizes non-beauty related messages
- [ ] System responds with friendly, engaging messages
- [ ] System gently steers conversation back to beauty topics
- [ ] System maintains conversational context and personality

### US-013: Interactive Chat Interface
**As a** user interacting with the chatbot  
**I want to** have a smooth, intuitive chat experience  
**So that** I can easily communicate my needs and receive help  

**Acceptance Criteria:**
- [ ] Chat interface is visually appealing and easy to use
- [ ] User can type messages and send with button or Enter key
- [ ] Chat history is maintained during the session
- [ ] User can clear chat history when needed
- [ ] Interface is responsive and works well in Google Colab
- [ ] Messages are clearly distinguished between user and bot

### US-015: Session Management and Analytics
**As a** system administrator  
**I want to** track user interactions and system performance  
**So that** I can understand usage patterns and improve the system  

**Acceptance Criteria:**
- [ ] System tracks conversation history during session
- [ ] System maintains cart state throughout session
- [ ] System can export conversation data
- [ ] System provides basic analytics (conversations, cart items, etc.)
- [ ] Session data is properly managed and cleaned up

## Domain Concepts

### Core Entities
- **Conversation**: Represents a complete chat session with a user
- **Message**: Individual messages within a conversation (user or bot)
- **Intent**: Classified user intention (concern, exploration, chitchat)
- **ConversationContext**: Maintains state and context throughout the conversation

### Value Objects
- **MessageType**: Enumeration of message types (UserMessage, BotMessage)
- **IntentType**: Enumeration of intent classifications (Concern, Exploration, ChitChat)
- **ConversationId**: Unique identifier for conversations
- **Timestamp**: When messages were sent/received

### Domain Services
- **IntentDetectionService**: Classifies user messages into intents
- **ResponseGenerationService**: Creates appropriate responses based on intent
- **ConversationFlowService**: Manages conversation state and transitions
- **NaturalLanguageProcessor**: Handles text processing and keyword extraction

### Repositories
- **ConversationRepository**: Stores and retrieves conversation data
- **MessageRepository**: Manages message persistence and history

### Domain Events
- **ConversationStarted**: When a new conversation begins
- **MessageReceived**: When user sends a message
- **IntentDetected**: When system classifies user intent
- **ResponseGenerated**: When bot generates a response
- **ConversationEnded**: When conversation session ends

## External Dependencies
- **Product Recommendation Unit**: For retrieving product suggestions
- **Natural Remedies Unit**: For getting remedy recommendations
- **User Profile Unit**: For accessing user preferences and personalization
- **Data Management Unit**: For concern keywords and mappings

## Interface Contracts

### Inbound
- `processUserMessage(message: string, conversationId: ConversationId): Response`
- `startConversation(userId?: UserId): ConversationId`
- `endConversation(conversationId: ConversationId): void`
- `getConversationHistory(conversationId: ConversationId): Message[]`

### Outbound
- `requestProductRecommendations(concern: string, userProfile: UserProfile): Product[]`
- `requestNaturalRemedies(concern: string): Remedy[]`
- `getUserProfile(userId: UserId): UserProfile`

## Business Rules
1. Every user message must be classified into exactly one intent type
2. Concern-based messages must trigger both product and remedy recommendations
3. Exploration messages must identify at least one product category
4. Chit-chat responses must attempt to redirect to beauty topics
5. Conversation context must be maintained throughout the session
6. All messages must be timestamped and stored for the session duration

## Quality Attributes
- **Performance**: Intent detection must complete within 500ms
- **Usability**: Interface must be intuitive and responsive
- **Maintainability**: Intent classification rules must be easily configurable
- **Reliability**: System must handle malformed or unexpected input gracefully
