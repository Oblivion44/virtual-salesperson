const Anthropic = require('@anthropic-ai/sdk');

class ConcernAnalysisAgent {
  constructor() {
    this.anthropic = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY,
    });
  }

  async analyze(message, session) {
    try {
      // Extract concerns and profile information
      const analysis = await this.extractConcerns(message, session);
      
      // Update user profile with extracted information
      this.updateProfile(session, analysis);
      
      // Generate response with follow-up questions or recommendations
      return this.generateResponse(analysis, session);
    } catch (error) {
      console.error('Error in concern analysis:', error);
      return {
        message: "I'd love to help you with your concerns! Could you tell me a bit more about what you're experiencing?",
        type: 'clarification'
      };
    }
  }

  async extractConcerns(message, session) {
    const prompt = `Analyze this beauty-related message and extract key information:

Message: "${message}"
Current profile: ${JSON.stringify(session.profile)}

Extract and categorize:
1. Category (skin, hair, makeup)
2. Specific concerns (acne, dryness, frizz, etc.)
3. Age group (if mentioned)
4. Skin/hair type (if mentioned)
5. Current products used (if mentioned)
6. Budget mentions (if any)
7. Lifestyle factors (if mentioned)

Respond with JSON:
{
  "category": "skin|hair|makeup",
  "concerns": ["concern1", "concern2"],
  "ageGroup": "teens|young_adults|adults|mature",
  "skinType": "oily|dry|combination|sensitive|normal",
  "hairType": "straight|wavy|curly|coily",
  "currentProducts": ["product1", "product2"],
  "budget": "budget_info_or_null",
  "lifestyle": ["factor1", "factor2"],
  "confidence": 0.8
}`;

    const response = await this.anthropic.messages.create({
      model: "claude-3-5-sonnet-20241022",
      max_tokens: 400,
      messages: [{ role: "user", content: prompt }]
    });

    try {
      return JSON.parse(response.content[0].text);
    } catch {
      return { category: 'general', concerns: [], confidence: 0.3 };
    }
  }

  updateProfile(session, analysis) {
    // Merge analysis results into user profile
    if (analysis.category) session.profile.category = analysis.category;
    if (analysis.concerns?.length) {
      session.profile.concerns = [...(session.profile.concerns || []), ...analysis.concerns];
      // Remove duplicates
      session.profile.concerns = [...new Set(session.profile.concerns)];
    }
    if (analysis.ageGroup) session.profile.ageGroup = analysis.ageGroup;
    if (analysis.skinType) session.profile.skinType = analysis.skinType;
    if (analysis.hairType) session.profile.hairType = analysis.hairType;
    if (analysis.currentProducts?.length) {
      session.profile.currentProducts = [...(session.profile.currentProducts || []), ...analysis.currentProducts];
    }
    if (analysis.budget) session.profile.budget = analysis.budget;
    if (analysis.lifestyle?.length) {
      session.profile.lifestyle = [...(session.profile.lifestyle || []), ...analysis.lifestyle];
    }

    // Update conversation step
    if (analysis.confidence > 0.7) {
      session.currentStep = 'recommendation_ready';
    } else {
      session.currentStep = 'gathering_info';
    }
  }

  async generateResponse(analysis, session) {
    const prompt = `You are Bella, a beauty consultant. Based on the concern analysis, generate an empathetic and helpful response.

Analysis: ${JSON.stringify(analysis)}
User Profile: ${JSON.stringify(session.profile)}

Guidelines:
- Acknowledge their concerns with empathy
- Ask clarifying questions if needed (confidence < 0.7)
- Offer to provide recommendations if you have enough info
- Be encouraging and supportive
- Keep response conversational and friendly

Generate a response that moves the conversation forward naturally.`;

    const response = await this.anthropic.messages.create({
      model: "claude-3-5-sonnet-20241022",
      max_tokens: 300,
      messages: [{ role: "user", content: prompt }]
    });

    const suggestions = this.generateSuggestions(analysis, session);

    return {
      message: response.content[0].text,
      type: 'concern_analysis',
      data: {
        analysis,
        profileUpdated: true
      },
      suggestions
    };
  }

  generateSuggestions(analysis, session) {
    const suggestions = [];

    if (analysis.confidence > 0.7) {
      suggestions.push('Show me product recommendations');
      suggestions.push('I want to see tutorials');
      
      if (analysis.category === 'skin') {
        suggestions.push('Build a skincare routine');
        suggestions.push('Tell me about ingredients');
      } else if (analysis.category === 'hair') {
        suggestions.push('Create a hair routine');
        suggestions.push('Show styling tips');
      } else if (analysis.category === 'makeup') {
        suggestions.push('Suggest makeup looks');
        suggestions.push('Help with color matching');
      }
    } else {
      // Need more information
      if (!session.profile.ageGroup) {
        suggestions.push('I\'m a teenager');
        suggestions.push('I\'m in my 20s');
        suggestions.push('I\'m in my 30s');
        suggestions.push('I\'m 40+');
      }
      
      if (analysis.category === 'skin' && !session.profile.skinType) {
        suggestions.push('My skin is oily');
        suggestions.push('My skin is dry');
        suggestions.push('I have combination skin');
        suggestions.push('I have sensitive skin');
      }
    }

    return suggestions.slice(0, 4); // Limit to 4 suggestions
  }
}

module.exports = ConcernAnalysisAgent;
