# User Profile Unit

## Overview
This bounded context manages user profiles, preferences, and personalization data. It provides user-specific information to other units for personalized recommendations and experiences.

## Bounded Context Scope
- User profile creation and management
- Personal preference storage and retrieval
- Profile-based personalization logic
- User data validation and privacy
- Profile persistence during sessions

## User Stories Included

### US-001: User Profile Creation
**As a** beauty enthusiast  
**I want to** create a personal profile with my age, budget, skin type, sun exposure, location, and profession  
**So that** I can receive personalized beauty recommendations tailored to my specific needs  

**Acceptance Criteria:**
- [ ] User can input age (13-80 years)
- [ ] User can select budget range ($0-25, $25-50, $50-100, $100+)
- [ ] User can choose skin type (Normal, Dry, Oily, Combination, Sensitive)
- [ ] User can specify daily sun exposure (Minimal, Moderate, High, Very High)
- [ ] User can enter location (city/country)
- [ ] User can select profession (Student, Office Worker, Healthcare, Outdoor Work, Creative, Other)
- [ ] Profile data is saved and persists during the session
- [ ] User receives confirmation when profile is saved

### US-002: Profile-Based Personalization
**As a** user with a saved profile  
**I want to** receive recommendations that consider my personal characteristics  
**So that** the suggested products are relevant to my lifestyle and needs  

**Acceptance Criteria:**
- [ ] Product recommendations are filtered by budget range
- [ ] Recommendations consider skin type compatibility
- [ ] Sun exposure level influences SPF and protection product suggestions
- [ ] Location affects product availability and climate-appropriate recommendations
- [ ] Profession influences makeup and skincare routine suggestions (e.g., office-friendly)

## Domain Concepts

### Core Entities
- **UserProfile**: Complete user profile with all personal information and preferences
- **User**: Basic user identity and session information

### Value Objects
- **UserId**: Unique identifier for users
- **Age**: User age with validation (13-80 years)
- **BudgetRange**: Enumerated budget categories with price ranges
- **SkinType**: Enumerated skin type classifications
- **SunExposure**: Daily sun exposure levels with time ranges
- **Location**: Geographic location information
- **Profession**: Professional category affecting lifestyle needs
- **ProfileCompleteness**: Percentage of profile fields completed

### Aggregates
- **UserProfileAggregate**: Root aggregate managing user profile data and validation

### Domain Services
- **ProfileValidationService**: Validates profile data and completeness
- **PersonalizationService**: Provides personalization logic based on profile
- **ProfileRecommendationService**: Suggests profile improvements for better recommendations

### Repositories
- **UserProfileRepository**: Manages profile data persistence and retrieval
- **UserRepository**: Basic user identity management

### Domain Events
- **ProfileCreated**: When a new user profile is created
- **ProfileUpdated**: When profile information is modified
- **ProfileCompleted**: When all required profile fields are filled
- **PersonalizationRequested**: When personalized data is requested

## External Dependencies
- **Product Recommendation Unit**: Receives personalization requests
- **Conversation Management Unit**: Provides user context for conversations
- **Shopping Cart Unit**: Provides user information for cart operations

## Interface Contracts

### Inbound
- `createProfile(profileData: ProfileData): UserProfile`
- `updateProfile(userId: UserId, updates: ProfileUpdates): UserProfile`
- `getProfile(userId: UserId): UserProfile`
- `validateProfile(profileData: ProfileData): ValidationResult`
- `getPersonalizationCriteria(userId: UserId): PersonalizationCriteria`

### Outbound
- `notifyProfileUpdate(userId: UserId, profile: UserProfile): void`

## Business Rules
1. **Age Validation**: Age must be between 13 and 80 years
2. **Budget Consistency**: Budget range must align with realistic beauty spending
3. **Skin Type Uniqueness**: User can only have one primary skin type
4. **Location Format**: Location must be in "City, Country" or "Country" format
5. **Profile Completeness**: Minimum 60% completion required for personalization
6. **Data Privacy**: Personal data must not be shared outside the system
7. **Session Persistence**: Profile data must persist throughout user session
8. **Default Values**: System must provide sensible defaults for optional fields

## Personalization Logic

### Budget-Based Filtering
- **$0-25**: Focus on drugstore and affordable options
- **$25-50**: Include mid-range and some premium options
- **$50-100**: Include premium and luxury options
- **$100+**: No budget restrictions, include all price ranges

### Skin Type Considerations
- **Normal**: Balanced product recommendations
- **Dry**: Emphasize hydrating and moisturizing products
- **Oily**: Focus on oil-control and mattifying products
- **Combination**: Recommend targeted products for different face areas
- **Sensitive**: Prioritize gentle, fragrance-free, hypoallergenic products

### Sun Exposure Impact
- **Minimal (0-2h)**: Basic SPF recommendations
- **Moderate (2-4h)**: SPF 30+ recommendations
- **High (4-6h)**: SPF 50+ and protective products
- **Very High (6h+)**: Maximum protection and after-sun care

### Profession-Based Recommendations
- **Student**: Budget-friendly, low-maintenance routines
- **Office Worker**: Professional, long-lasting makeup; office-appropriate
- **Healthcare**: Gentle, hygienic products; mask-friendly makeup
- **Outdoor Work**: High SPF, sweat-resistant, protective products
- **Creative**: Trendy, expressive products; bold colors and styles
- **Other**: Balanced recommendations based on other profile factors

### Location Considerations
- **Climate**: Humid vs. dry climate product recommendations
- **Availability**: Regional product availability and shipping
- **Cultural**: Culturally appropriate beauty standards and preferences

## Data Validation Rules

### Required Fields
- Age (must be provided)
- Skin type (must be selected)
- Budget range (must be selected)

### Optional Fields
- Sun exposure (defaults to "Moderate")
- Location (defaults to "Not specified")
- Profession (defaults to "Other")

### Validation Constraints
- Age: Integer between 13 and 80
- Budget: Must be one of predefined ranges
- Skin Type: Must be one of predefined types
- Sun Exposure: Must be one of predefined levels
- Location: String, max 100 characters
- Profession: Must be one of predefined categories

## Quality Attributes
- **Privacy**: User data must be handled securely and not logged
- **Performance**: Profile retrieval must complete within 100ms
- **Usability**: Profile creation must be intuitive and quick
- **Reliability**: Profile data must persist reliably throughout sessions
