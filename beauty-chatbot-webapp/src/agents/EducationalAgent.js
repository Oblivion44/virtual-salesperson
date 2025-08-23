const Anthropic = require('@anthropic-ai/sdk');

class EducationalAgent {
  constructor() {
    this.anthropic = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY,
    });
  }

  async provide(message, session) {
    try {
      // Determine what type of educational content is needed
      const contentType = await this.analyzeEducationalRequest(message, session);
      
      // Generate appropriate educational response
      return await this.generateEducationalContent(contentType, message, session);
    } catch (error) {
      console.error('Error in educational agent:', error);
      return {
        message: "I'd love to teach you about beauty! What specific topic would you like to learn about?",
        type: 'clarification'
      };
    }
  }

  async analyzeEducationalRequest(message, session) {
    const prompt = `Analyze this message to determine what type of educational beauty content the user wants.

Message: "${message}"
User Profile: ${JSON.stringify(session.profile)}

Types of educational content:
- tutorial: Step-by-step how-to guides
- ingredient_education: Information about skincare/makeup ingredients
- technique_tips: Application techniques and tips
- routine_explanation: How to build and follow routines
- product_knowledge: Understanding different product types
- skin_science: Scientific explanations about skin/hair

Respond with JSON: {"type": "content_type", "topic": "specific_topic", "format": "video|text|both"}`;

    const response = await this.anthropic.messages.create({
      model: "claude-3-5-sonnet-20241022",
      max_tokens: 200,
      messages: [{ role: "user", content: prompt }]
    });

    try {
      return JSON.parse(response.content[0].text);
    } catch {
      return { type: 'tutorial', topic: 'general_beauty', format: 'text' };
    }
  }

  async generateEducationalContent(contentType, message, session) {
    const prompt = `You are Bella, a beauty education expert. Create educational content based on the request.

Content Type: ${contentType.type}
Topic: ${contentType.topic}
User Message: "${message}"
User Profile: ${JSON.stringify(session.profile)}

Create engaging, informative content that:
- Is appropriate for their age group and experience level
- Addresses their specific concerns
- Includes practical tips they can use
- Is encouraging and supportive

If video content is requested, also provide a detailed description for video generation.`;

    const response = await this.anthropic.messages.create({
      model: "claude-3-5-sonnet-20241022",
      max_tokens: 500,
      messages: [{ role: "user", content: prompt }]
    });

    const content = response.content[0].text;

    // Determine if video should be offered
    const shouldOfferVideo = contentType.format === 'video' || contentType.format === 'both' || 
                           contentType.type === 'tutorial';

    const responseData = {
      message: content,
      type: shouldOfferVideo ? 'video_tutorial_request' : 'educational_content',
      data: {
        contentType: contentType.type,
        topic: contentType.topic,
        videoPrompt: shouldOfferVideo ? this.generateVideoPrompt(contentType, session) : null
      },
      suggestions: this.generateEducationalSuggestions(contentType, session)
    };

    return responseData;
  }

  generateVideoPrompt(contentType, session) {
    const category = session.profile.category || 'skincare';
    const ageGroup = session.profile.ageGroup || 'young_adults';
    
    const prompts = {
      tutorial: {
        skincare: `Professional skincare tutorial for ${ageGroup}, demonstrating proper cleansing, toning, and moisturizing techniques, clean aesthetic, natural lighting`,
        hair: `Hair care tutorial showing proper washing, conditioning, and styling techniques for ${ageGroup}, professional salon setting`,
        makeup: `Makeup application tutorial for ${ageGroup}, showing foundation, concealer, and basic eye makeup, clean beauty setup`
      },
      ingredient_education: `Close-up shots of skincare ingredients with text overlays explaining benefits, professional product photography, educational style`,
      technique_tips: `Beauty technique demonstration showing proper application methods, professional lighting, step-by-step visual guide`
    };

    return prompts[contentType.type]?.[category] || prompts[contentType.type] || prompts.tutorial.skincare;
  }

  generateEducationalSuggestions(contentType, session) {
    const baseSuggestions = [
      'Show me a video tutorial',
      'Tell me about ingredients',
      'Give me more tips',
      'Explain the science behind it'
    ];

    const category = session.profile.category;
    
    if (category === 'skin') {
      return [
        'Show me skincare routine video',
        'Explain skincare ingredients',
        'Application techniques',
        'Skin science basics'
      ];
    } else if (category === 'hair') {
      return [
        'Hair styling tutorial',
        'Hair care ingredients',
        'Styling techniques',
        'Hair health tips'
      ];
    } else if (category === 'makeup') {
      return [
        'Makeup tutorial video',
        'Color theory basics',
        'Application techniques',
        'Product knowledge'
      ];
    }

    return baseSuggestions;
  }
}

module.exports = EducationalAgent;
