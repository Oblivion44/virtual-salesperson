const Anthropic = require('@anthropic-ai/sdk');
const ConcernAnalysisAgent = require('./ConcernAnalysisAgent');
const RecommendationAgent = require('./RecommendationAgent');
const EducationalAgent = require('./EducationalAgent');
const RoutineAgent = require('./RoutineAgent');

class BeautyChatbot {
  constructor() {
    this.anthropic = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY,
    });

    // Initialize specialized agents (Strand pattern)
    this.concernAgent = new ConcernAnalysisAgent();
    this.recommendationAgent = new RecommendationAgent();
    this.educationalAgent = new EducationalAgent();
    this.routineAgent = new RoutineAgent();

    this.systemPrompt = `You are Bella, an AI virtual salesperson for a beauty e-commerce company. You specialize in Skin, Hair, and Makeup products with access to 24K products.

Your personality:
- Friendly, knowledgeable, and enthusiastic about beauty
- Natural conversationalist who builds rapport
- Expert in skincare, haircare, and makeup
- Focused on personalized recommendations
- Educational and helpful

Your capabilities:
- Analyze skin/hair concerns and recommend products
- Provide educational content and tutorials
- Create personalized beauty routines
- Handle budget constraints intelligently
- Link to Nykaa.com products with images

Conversation flow:
1. Warm greeting and category detection (Skin/Hair/Makeup)
2. Progressive profile building (age, concerns, preferences)
3. Concern analysis and product recommendations
4. Educational content delivery when requested
5. Routine curation and budget-aware suggestions

Always be natural, avoid rigid forms, and focus on building trust through expertise.`;
  }

  async processMessage(message, session) {
    try {
      // Determine intent and route to appropriate agent
      const intent = await this.analyzeIntent(message, session);
      
      switch (intent.type) {
        case 'greeting':
          return this.handleGreeting(message, session);
        
        case 'concern_analysis':
          return await this.concernAgent.analyze(message, session);
        
        case 'product_recommendation':
          return await this.recommendationAgent.recommend(message, session);
        
        case 'educational_request':
          return await this.educationalAgent.provide(message, session);
        
        case 'routine_building':
          return await this.routineAgent.build(message, session);
        
        case 'general_chat':
          return this.handleGeneralChat(message, session);
        
        default:
          return this.handleFallback(message, session);
      }
    } catch (error) {
      console.error('Error in processMessage:', error);
      return {
        message: "I'm sorry, I encountered an issue. Could you please rephrase your question?",
        type: 'error'
      };
    }
  }

  async analyzeIntent(message, session) {
    const prompt = `Analyze the user's message and determine their intent. Consider the conversation history and current step.

User message: "${message}"
Current step: ${session.currentStep}
Conversation history: ${JSON.stringify(session.conversationHistory.slice(-3))}

Possible intents:
- greeting: Initial hello, introduction
- concern_analysis: Describing skin/hair issues, problems
- product_recommendation: Asking for product suggestions
- educational_request: Wanting tutorials, how-to content
- routine_building: Creating skincare/haircare routines
- general_chat: General beauty questions, chitchat

Respond with JSON: {"type": "intent_name", "confidence": 0.9, "entities": {...}}`;

    const response = await this.anthropic.messages.create({
      model: "claude-3-5-sonnet-20241022",
      max_tokens: 200,
      messages: [{ role: "user", content: prompt }]
    });

    try {
      return JSON.parse(response.content[0].text);
    } catch {
      return { type: 'general_chat', confidence: 0.5, entities: {} };
    }
  }

  handleGreeting(message, session) {
    session.currentStep = 'category_detection';
    
    const greetings = [
      "Hi there! I'm Bella, your personal beauty consultant! ✨ I'm here to help you discover amazing products for your skin, hair, or makeup needs. What brings you here today?",
      "Hello beautiful! 💄 I'm Bella, and I'm excited to help you find the perfect beauty products! Are you looking for skincare, haircare, or makeup solutions?",
      "Hey there! Welcome to your personalized beauty journey! I'm Bella, and I specialize in helping you find products that work perfectly for YOU. What area would you like to focus on - skin, hair, or makeup?"
    ];

    return {
      message: greetings[Math.floor(Math.random() * greetings.length)],
      type: 'greeting',
      suggestions: ['Skincare help', 'Hair concerns', 'Makeup advice', 'Build a routine']
    };
  }

  async handleGeneralChat(message, session) {
    const prompt = `${this.systemPrompt}

User profile: ${JSON.stringify(session.profile)}
Conversation history: ${JSON.stringify(session.conversationHistory.slice(-5))}

User message: "${message}"

Respond as Bella, the beauty consultant. Be helpful, engaging, and try to guide the conversation toward beauty topics where you can provide value.`;

    const response = await this.anthropic.messages.create({
      model: "claude-3-5-sonnet-20241022",
      max_tokens: 300,
      messages: [{ role: "user", content: prompt }]
    });

    return {
      message: response.content[0].text,
      type: 'general_chat',
      suggestions: this.generateSuggestions(session)
    };
  }

  handleFallback(message, session) {
    const fallbacks = [
      "I want to make sure I give you the best advice! Could you tell me a bit more about what you're looking for?",
      "That's interesting! To help you better, could you share more details about your beauty concerns or goals?",
      "I'm here to help with all things beauty! What specific area would you like to focus on - skincare, haircare, or makeup?"
    ];

    return {
      message: fallbacks[Math.floor(Math.random() * fallbacks.length)],
      type: 'clarification',
      suggestions: ['Skincare advice', 'Hair problems', 'Makeup tips', 'Product recommendations']
    };
  }

  generateSuggestions(session) {
    const baseSuggestions = [
      'Recommend products for me',
      'Show me tutorials',
      'Build a routine',
      'What\'s trending?'
    ];

    // Customize based on session data
    if (session.profile.category) {
      if (session.profile.category === 'skin') {
        return ['Skincare routine', 'Product recommendations', 'Skin tutorials', 'Ingredient advice'];
      } else if (session.profile.category === 'hair') {
        return ['Hair routine', 'Hair products', 'Styling tutorials', 'Hair health tips'];
      } else if (session.profile.category === 'makeup') {
        return ['Makeup looks', 'Product suggestions', 'Makeup tutorials', 'Color matching'];
      }
    }

    return baseSuggestions;
  }
}

module.exports = BeautyChatbot;
