const Anthropic = require('@anthropic-ai/sdk');

class RecommendationAgent {
  constructor() {
    this.anthropic = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY,
    });
  }

  async recommend(message, session) {
    try {
      // Generate product recommendations based on user profile and message
      const recommendations = await this.generateRecommendations(message, session);
      
      // Format response with product suggestions
      return this.formatRecommendationResponse(recommendations, session);
    } catch (error) {
      console.error('Error in recommendation agent:', error);
      return {
        message: "I'd love to recommend some products for you! Could you tell me more about your specific needs?",
        type: 'clarification'
      };
    }
  }

  async generateRecommendations(message, session) {
    const prompt = `Based on the user's profile and message, recommend specific beauty products.

User Profile: ${JSON.stringify(session.profile)}
User Message: "${message}"

Consider:
- User's concerns and skin/hair type
- Age group and lifestyle
- Budget constraints (if mentioned)
- Current products they use

Generate 3-5 specific product recommendations with:
- Product name and brand
- Why it's suitable for them
- Key benefits
- Price range
- Nykaa availability

Respond with JSON array of products.`;

    const response = await this.anthropic.messages.create({
      model: "claude-3-5-sonnet-20241022",
      max_tokens: 600,
      messages: [{ role: "user", content: prompt }]
    });

    try {
      return JSON.parse(response.content[0].text);
    } catch {
      return this.getFallbackRecommendations(session);
    }
  }

  formatRecommendationResponse(recommendations, session) {
    const responseMessage = this.generateRecommendationMessage(recommendations, session);
    
    return {
      message: responseMessage,
      type: 'product_recommendations',
      data: {
        products: recommendations,
        productIds: recommendations.map(p => p.id || p.name)
      },
      suggestions: [
        'Tell me more about these products',
        'Show me tutorials',
        'Build a routine with these',
        'Find similar products'
      ]
    };
  }

  generateRecommendationMessage(recommendations, session) {
    const userName = session.profile.name || 'there';
    const category = session.profile.category || 'beauty';
    
    const messages = [
      `Perfect! I've found some amazing ${category} products that would work wonderfully for you! ✨`,
      `Great news! Based on your needs, I have some fantastic ${category} recommendations! 💄`,
      `I'm excited to share these ${category} products that are perfect for your concerns! 🌟`
    ];

    const baseMessage = messages[Math.floor(Math.random() * messages.length)];
    
    if (recommendations.length > 0) {
      return `${baseMessage}\n\nI've selected ${recommendations.length} products that address your specific needs. Each one has been chosen based on your profile and will help you achieve your beauty goals. Click below to see the full details and shop on Nykaa!`;
    }

    return baseMessage;
  }

  getFallbackRecommendations(session) {
    // Provide generic recommendations based on category
    const category = session.profile.category || 'skin';
    
    const fallbackProducts = {
      skin: [
        {
          name: "Cetaphil Gentle Skin Cleanser",
          brand: "Cetaphil",
          price: "₹599",
          benefits: "Gentle cleansing for all skin types",
          reason: "Perfect for daily cleansing without irritation"
        },
        {
          name: "The Ordinary Hyaluronic Acid 2% + B5",
          brand: "The Ordinary",
          price: "₹849",
          benefits: "Intense hydration and plumping",
          reason: "Great for maintaining skin moisture"
        }
      ],
      hair: [
        {
          name: "L'Oréal Paris Total Repair 5 Shampoo",
          brand: "L'Oréal Paris",
          price: "₹399",
          benefits: "Repairs damaged hair",
          reason: "Suitable for most hair types and concerns"
        }
      ],
      makeup: [
        {
          name: "Maybelline Fit Me Foundation",
          brand: "Maybelline",
          price: "₹499",
          benefits: "Natural coverage for all skin tones",
          reason: "Popular choice for everyday wear"
        }
      ]
    };

    return fallbackProducts[category] || fallbackProducts.skin;
  }
}

module.exports = RecommendationAgent;
