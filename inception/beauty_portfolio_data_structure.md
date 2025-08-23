# Beauty Portfolio Data Structure

## Customer Profile Schema

### 1. Skin Profile
```json
{
  "skin_profile": {
    "skin_type": {
      "type": "enum",
      "values": ["Dry", "Oily", "Combination", "Balanced"],
      "required": true
    },
    "skin_concerns": {
      "type": "array",
      "values": [
        "Acne", "Tanning", "Dryness", "Fine lines", "Oiliness", 
        "Wrinkles", "Dull skin", "Dark spot and pigmentation", 
        "Pores", "Dark circles", "Blackheads and whiteheads"
      ],
      "required": true,
      "multiple_selection": true
    },
    "age_group": {
      "type": "enum",
      "values": ["Teen (13-19)", "Young Adult (20-29)", "Adult (30-39)", "Mature (40+)"],
      "required": true
    },
    "date_of_birth": {
      "type": "date",
      "required": false,
      "note": "If not provided, use age_group"
    }
  }
}
```

### 2. Hair Profile
```json
{
  "hair_profile": {
    "hair_type": {
      "type": "enum",
      "values": ["Straight", "Wavy", "Curly"],
      "required": true
    },
    "scalp_type": {
      "type": "enum", 
      "values": ["Dry", "Balanced", "Oily"],
      "required": true
    },
    "hair_concerns": {
      "type": "array",
      "values": [
        "Colour Protection", "Damaged Hair", "Dandruff & Flakes",
        "Dry Hair", "Dull Hair", "Frizzy Hair", 
        "Hairfall & Thinning", "Oily Scalp", "Split Ends"
      ],
      "required": true,
      "multiple_selection": true
    }
  }
}
```

### 3. Makeup Profile
```json
{
  "makeup_profile": {
    "skin_tone": {
      "type": "string",
      "required": true,
      "note": "Customer-defined description"
    },
    "undertone": {
      "type": "string", 
      "required": true,
      "note": "Customer-defined description"
    }
  }
}
```

### 4. Budget & Preferences
```json
{
  "preferences": {
    "budget": {
      "type": "number",
      "required": false,
      "currency": "INR",
      "note": "If not provided, show top sellers"
    },
    "preferred_brands": {
      "type": "array",
      "required": false
    },
    "ingredient_allergies": {
      "type": "array", 
      "required": false
    },
    "routine_complexity": {
      "type": "enum",
      "values": ["Simple", "Moderate", "Advanced"],
      "default": "Moderate"
    }
  }
}
```

## Complete Customer Profile Example
```json
{
  "customer_id": "CUST_12345",
  "profile_created": "2024-01-15T10:30:00Z",
  "last_updated": "2024-01-20T14:22:00Z",
  "skin_profile": {
    "skin_type": "Combination",
    "skin_concerns": ["Acne", "Dark spot and pigmentation", "Pores"],
    "age_group": "Young Adult (20-29)"
  },
  "hair_profile": {
    "hair_type": "Wavy",
    "scalp_type": "Oily", 
    "hair_concerns": ["Frizzy Hair", "Oily Scalp", "Dull Hair"]
  },
  "makeup_profile": {
    "skin_tone": "Medium with warm undertones",
    "undertone": "Warm golden"
  },
  "preferences": {
    "budget": 2500,
    "preferred_brands": ["Nykaa", "Lakme", "Maybelline"],
    "ingredient_allergies": ["Sulfates", "Parabens"],
    "routine_complexity": "Moderate"
  }
}
```
