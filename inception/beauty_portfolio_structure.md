# Beauty Portfolio Data Structure

## Overview
This document defines the complete data structure for collecting customer beauty profiles to enable personalized AI recommendations.

## Data Categories

### 1. Skin Profile
```json
{
  "skin_type": {
    "type": "enum",
    "options": ["Dry", "Oily", "Combination", "Balanced"],
    "required": true
  },
  "skin_concerns": {
    "type": "multi-select",
    "options": [
      "Acne",
      "Tanning", 
      "Dryness",
      "Fine lines",
      "Oiliness",
      "Wrinkles",
      "Dull skin",
      "Dark spots & pigmentation",
      "Pores",
      "Dark circles",
      "Blackheads & whiteheads"
    ],
    "required": true
  }
}
```

### 2. Hair Profile
```json
{
  "hair_type": {
    "type": "enum",
    "options": ["Straight", "Wavy", "Curly"],
    "required": true
  },
  "scalp_type": {
    "type": "enum", 
    "options": ["Dry", "Balanced", "Oily"],
    "required": true
  },
  "hair_concerns": {
    "type": "multi-select",
    "options": [
      "Colour Protection",
      "Damaged Hair",
      "Dandruff & Flakes",
      "Dry Hair",
      "Dull Hair", 
      "Frizzy Hair",
      "Hairfall & Thinning",
      "Oily Scalp",
      "Split Ends"
    ],
    "required": true
  }
}
```

### 3. Makeup Profile
```json
{
  "skin_tone": {
    "type": "enum",
    "options": ["Fair", "Light", "Medium", "Tan", "Deep", "Dark"],
    "required": false
  },
  "undertone": {
    "type": "enum",
    "options": ["Cool", "Warm", "Neutral"],
    "required": false
  }
}
```

### 4. Demographics
```json
{
  "age_group": {
    "type": "enum",
    "options": [
      "Teens (13-19)",
      "Young Adults (20-29)", 
      "Adults (30-39)",
      "Mature (40+)"
    ],
    "required": true
  }
}
```

### 5. Budget Preferences
```json
{
  "budget_constraints": {
    "type": "text",
    "question": "Do you have any budget constraints?",
    "required": false,
    "note": "Customer provides their own budget range or amount"
  }
}
```

## Data Collection Flow

### 1. Initial Greeting & Category Detection
- AI starts with general beauty greeting: "Hello! I'm your personal beauty consultant. I'm here to help you with all your beauty needs - whether it's skincare, haircare, or makeup. What's on your mind today?"
- Analyze user response to detect primary interest category
- Use natural language processing to identify keywords:
  - Skin category: "skin", "face", "acne", "dry", "oily", "wrinkles", "aging", "cleanser", "moisturizer"
  - Hair category: "hair", "scalp", "dandruff", "frizzy", "damaged", "shampoo", "conditioner"
  - Makeup category: "makeup", "foundation", "lipstick", "eyeshadow", "concealer", "color matching"
- Gracefully handle mixed interests or unclear responses

### 2. Progressive Profiling
- Start with essential fields (type, main concerns)
- Collect additional details as conversation progresses
- Allow customers to update profile information

### 3. Data Validation
- Ensure required fields are collected
- Validate enum selections
- Handle gracefully when information is missing
- Provide helpful prompts for unclear responses

## Usage in Recommendations

### Product Filtering Logic
```
1. Filter by category (canonical_l1: Skin/Hair/Makeup)
2. Filter by sub-category (canonical_l3) based on concerns
3. Match ingredients to skin/hair type
4. Consider age-appropriate products
5. Apply budget constraints if provided
6. Rank by relevance and reviews
```

### Personalization Factors
- **Skin Type + Concerns** → Ingredient matching
- **Hair Type + Scalp Type + Concerns** → Product formulation
- **Age Group** → Age-appropriate products and concerns
- **Budget** → Price filtering and alternatives
- **Makeup Profile** → Shade matching and undertone compatibility

## Data Storage Considerations
- Store as structured JSON for easy querying
- Maintain conversation history for context
- Allow profile updates during conversation
- Track preference changes over time

## Privacy & Security
- No personally identifiable information stored
- Profile data used only for recommendations
- Data not shared with external services
- Customer can clear profile data anytime
