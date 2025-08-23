# AI Virtual Salesperson Chatbot - User Stories

## Epic 1: Personalized Beauty Consultation & Product Recommendations

### User Story 1.1: Initial Greeting and Category Detection
**As a** customer  
**I want to** be greeted naturally by the AI and have it detect my interests from my responses  
**So that** I get a personalized experience without rigid category selection  

**Acceptance Criteria:**
- AI starts with general beauty greeting (not category-specific)
- System analyzes user responses to detect interest category (Skin/Hair/Makeup)
- AI asks follow-up questions based on detected category
- System gracefully handles mixed interests across categories
- Conversation flows naturally without forced category selection

### User Story 1.2: Beauty Portfolio Data Collection
**As a** customer  
**I want to** provide my beauty profile information (skin type, concerns, hair type, age group)  
**So that** the AI can give me personalized recommendations  

**Acceptance Criteria:**
- System collects skin type (Dry, Oily, Combination, Balanced)
- System collects skin concerns (Acne, Tanning, Dryness, Fine lines, Oiliness, Wrinkles, Dull skin, Dark spots & pigmentation, Pores, Dark circles, Blackheads & whiteheads)
- System collects hair type (Straight, Wavy, Curly)
- System collects scalp type (Dry, Balanced, Oily)
- System collects hair concerns (Colour Protection, Damaged Hair, Dandruff & Flakes, Dry Hair, Dull Hair, Frizzy Hair, Hairfall & Thinning, Oily Scalp, Split Ends)
- System collects makeup preferences (skin tone, undertone)
- System asks for age group: Teens (13-19), Young Adults (20-29), Adults (30-39), Mature (40+)
- System handles missing information gracefully

### User Story 1.3: Intelligent Concern Analysis
**As a** customer  
**I want to** describe my beauty concerns in natural language  
**So that** the AI understands my needs without rigid forms  

**Acceptance Criteria:**
- AI processes natural language input using AWS Bedrock LLM
- System maps concerns to appropriate product categories
- AI asks clarifying questions when needed
- System provides concern validation and confirmation

### User Story 1.4: Budget-Based Product Recommendations
**As a** customer  
**I want to** receive product recommendations within my budget  
**So that** I can make affordable purchases  

**Acceptance Criteria:**
- System asks "Do you have any budget constraints?" without suggesting ranges
- If customer provides budget, filter recommendations accordingly
- If no budget constraints mentioned, system shows top sellers
- Recommendations include products from 24K product catalogue
- Products filtered by skin/hair type and concerns using canonical_l3 sub-categories
- System shows product images from Nykaa.com
- Each recommendation includes hyperlink to Nykaa product page

### User Story 1.5: Comprehensive Product Presentation
**As a** customer  
**I want to** see detailed product information with compelling sales pitches  
**So that** I can make informed purchase decisions  

**Acceptance Criteria:**
- Display product images from Nykaa.com
- Show filtered positive reviews from input reviews CSV using NLP sentiment analysis
- Generate AI-powered sales pitch for each product
- Include ingredient information relevant to customer concerns
- Display brand name and product details from catalogue CSV
- Utilize canonical_l3 field for accurate sub-category classification
- Provide direct link to Nykaa product listing

## Epic 2: Educational Content Delivery

### User Story 2.1: Video Content Recommendations
**As a** customer  
**I want to** access educational videos about recommended products  
**So that** I can learn how to use them effectively  

**Acceptance Criteria:**
- System asks if customer wants to see educational content
- AI generates 10-second real human-like tutorial videos (no anime)
- Videos focus entirely on demonstration without intro/outro (full 10 seconds of content)
- Content shows direct product application and techniques
- Videos cover ingredient benefits through visual demonstration
- System provides home-made remedy videos when relevant
- Videos feature natural, realistic human demonstrations

### User Story 2.2: Educational Image Content
**As a** customer  
**I want to** see educational images and tutorials  
**So that** I can understand product benefits and usage  

**Acceptance Criteria:**
- AI generates educational images using AWS Bedrock
- Images show step-by-step application processes
- Content explains ingredient benefits visually
- Images demonstrate before/after scenarios
- System provides infographics about beauty concerns

## Epic 3: Personalized Beauty Routine Curation

### User Story 3.1: Custom Routine Creation
**As a** customer  
**I want to** get a personalized beauty routine (skincare/haircare/makeup)  
**So that** I can follow a structured regimen for my concerns  

**Acceptance Criteria:**
- System creates routines based on skin/hair type, concerns, age, and budget
- Routines are customizable based on customer preferences
- Each routine includes morning and evening steps
- System explains the purpose of each step
- Routines include product recommendations with images and reviews

### User Story 3.2: Routine Customization
**As a** customer  
**I want to** modify my recommended routine  
**So that** it fits my lifestyle and preferences  

**Acceptance Criteria:**
- Customer can add/remove steps from routine
- System suggests alternative products for each step
- Routine adjusts based on budget constraints
- System maintains routine effectiveness while accommodating changes
- Customer can save multiple routine variations

### User Story 3.3: Routine Product Integration
**As a** customer  
**I want to** see how each product fits into my routine  
**So that** I understand the complete regimen  

**Acceptance Criteria:**
- Each routine step shows recommended products with images
- System displays product reviews and ratings
- AI generates sales pitch for routine combinations
- System shows total routine cost within budget
- Products link directly to Nykaa listings

## Epic 4: AI Guardrails & Content Filtering

### User Story 4.1: Conversation Guardrails
**As a** customer  
**I want** the chatbot to stay focused on beauty topics  
**So that** I get relevant and helpful responses  

**Acceptance Criteria:**
- System detects off-topic questions
- AI redirects irrelevant queries to beauty-related topics
- System provides polite responses for non-beauty questions
- Chatbot maintains professional beauty consultant persona
- System handles inappropriate content gracefully

### User Story 4.2: Review Quality Filtering
**As a** customer  
**I want to** see only relevant and positive product reviews  
**So that** I can make confident purchase decisions  

**Acceptance Criteria:**
- NLP system filters reviews from input reviews CSV for positive sentiment
- System shows reviews relevant to customer's concerns
- AI summarizes review highlights from CSV data
- System excludes spam or irrelevant reviews using sentiment analysis
- Reviews are presented in digestible format
- System matches reviews to products using product_id from both CSVs

## Epic 5: Technical Infrastructure

### User Story 5.1: AWS Bedrock Integration
**As a** system administrator  
**I want** seamless LLM integration  
**So that** the chatbot provides intelligent responses  

**Acceptance Criteria:**
- System integrates with AWS Bedrock for LLM capabilities
- AI generates natural language responses
- System handles API rate limits and errors
- LLM responses are contextually relevant
- System maintains conversation history

### User Story 5.2: Google Colab Deployment
**As a** developer  
**I want** the system to run on Google Colab  
**So that** we can demonstrate the POC effectively  

**Acceptance Criteria:**
- Web-based interface runs in Google Colab environment
- System handles Colab resource limitations
- Interface is responsive and user-friendly
- System maintains session state during conversations
- Easy setup and execution process

### User Story 5.3: Product Catalogue Integration
**As a** system  
**I want** to access the 24K product database efficiently  
**So that** recommendations are accurate and comprehensive  

**Acceptance Criteria:**
- System integrates product catalogue CSV (product_name, product_id, brand_name, canonical_l1, canonical_l3, ingredients, concerns)
- System integrates reviews CSV and matches to products via product_id
- Fast product search and filtering capabilities using canonical_l3 sub-categories
- System handles large dataset efficiently (24K products + reviews)
- Product data is always current and accurate
- System maps concerns to relevant products using canonical_l3 classification
- Reviews are properly linked to products for accurate sentiment analysis

## Epic 6: User Experience & Interface

### User Story 6.1: Conversational Interface
**As a** customer  
**I want** to interact with the chatbot naturally  
**So that** the experience feels like talking to a beauty expert  

**Acceptance Criteria:**
- Natural language processing for customer inputs
- Conversational flow feels human-like
- System remembers conversation context
- Interface is intuitive and easy to use
- System provides clear next steps and options

### User Story 6.2: Visual Product Display
**As a** customer  
**I want** to see attractive product presentations  
**So that** I can visualize the recommendations  

**Acceptance Criteria:**
- High-quality product images from Nykaa.com
- Clean and organized product layout
- Images load quickly and display properly
- Product information is clearly presented
- Visual hierarchy guides attention to key information

## Definition of Done
- [ ] All acceptance criteria met
- [ ] AWS Bedrock LLM integration working
- [ ] Nykaa.com image integration functional
- [ ] NLP sentiment analysis implemented
- [ ] Google Colab deployment successful
- [ ] User testing completed
- [ ] Performance acceptable for POC
- [ ] Documentation updated

## Technical Constraints
- Deployment: Google Colab only (POC)
- LLM: AWS Bedrock required
- Image Source: Nykaa.com only
- Product Database: 24K products across Skin, Hair, Makeup
- Video Duration: 10 seconds maximum (real human-like, no anime)
- No external integrations required
- Web-based interface
- No performance requirements specified
- **Data Input**: Product catalogue CSV + Reviews CSV (linked by product_id)
- **Age Groups**: Teens (13-19), Young Adults (20-29), Adults (30-39), Mature (40+)
- **Budget Handling**: Ask "Do you have any budget constraints?" without predefined ranges
- **Sub-categories**: Use canonical_l3 field from product catalogue
