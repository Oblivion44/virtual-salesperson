const Anthropic = require('@anthropic-ai/sdk');

class RoutineAgent {
  constructor() {
    this.anthropic = new Anthropic({
      apiKey: process.env.ANTHROPIC_API_KEY,
    });
  }

  async build(message, session) {
    try {
      // Analyze what type of routine is needed
      const routineType = await this.analyzeRoutineRequest(message, session);
      
      // Generate personalized routine
      const routine = await this.generateRoutine(routineType, session);
      
      // Format response
      return this.formatRoutineResponse(routine, session);
    } catch (error) {
      console.error('Error in routine agent:', error);
      return {
        message: "I'd love to create a personalized routine for you! Tell me about your current routine and what you'd like to improve.",
        type: 'clarification'
      };
    }
  }

  async analyzeRoutineRequest(message, session) {
    const prompt = `Analyze this message to understand what type of beauty routine the user wants.

Message: "${message}"
User Profile: ${JSON.stringify(session.profile)}

Determine:
- Routine type (morning, evening, weekly, full_regimen)
- Category (skincare, haircare, makeup)
- Complexity level (beginner, intermediate, advanced)
- Time constraints (quick, standard, comprehensive)
- Special focus areas

Respond with JSON: {
  "type": "routine_type",
  "category": "category",
  "complexity": "level",
  "timeframe": "duration",
  "focus": ["area1", "area2"]
}`;

    const response = await this.anthropic.messages.create({
      model: "claude-3-5-sonnet-20241022",
      max_tokens: 300,
      messages: [{ role: "user", content: prompt }]
    });

    try {
      return JSON.parse(response.content[0].text);
    } catch {
      return {
        type: 'full_regimen',
        category: session.profile.category || 'skincare',
        complexity: 'beginner',
        timeframe: 'standard',
        focus: session.profile.concerns || []
      };
    }
  }

  async generateRoutine(routineType, session) {
    const prompt = `Create a personalized beauty routine based on the user's profile and requirements.

User Profile: ${JSON.stringify(session.profile)}
Routine Requirements: ${JSON.stringify(routineType)}

Create a detailed routine that includes:
- Step-by-step instructions
- Product recommendations
- Timing and frequency
- Tips for success
- Budget-conscious alternatives if budget is mentioned

Make it practical, achievable, and tailored to their specific needs and lifestyle.

Format as JSON with structure:
{
  "title": "Routine Name",
  "description": "Brief description",
  "steps": [
    {
      "step": 1,
      "name": "Step Name",
      "description": "What to do",
      "products": ["product suggestions"],
      "timing": "when to do it",
      "tips": "helpful tips"
    }
  ],
  "frequency": "how often",
  "totalTime": "estimated time",
  "budgetTips": "cost-saving suggestions"
}`;

    const response = await this.anthropic.messages.create({
      model: "claude-3-5-sonnet-20241022",
      max_tokens: 800,
      messages: [{ role: "user", content: prompt }]
    });

    try {
      return JSON.parse(response.content[0].text);
    } catch {
      return this.getFallbackRoutine(routineType, session);
    }
  }

  formatRoutineResponse(routine, session) {
    const message = this.generateRoutineMessage(routine, session);
    
    return {
      message: message,
      type: 'routine_created',
      data: {
        routine: routine,
        customized: true
      },
      suggestions: [
        'Show me product recommendations',
        'Create a shopping list',
        'Modify this routine',
        'Show me tutorials for these steps'
      ]
    };
  }

  generateRoutineMessage(routine, session) {
    const userName = session.profile.name || 'there';
    
    let message = `🌟 Perfect! I've created a personalized "${routine.title}" just for you!\n\n`;
    message += `${routine.description}\n\n`;
    
    message += `📋 **Your Routine Steps:**\n`;
    routine.steps.forEach(step => {
      message += `\n**${step.step}. ${step.name}**\n`;
      message += `${step.description}\n`;
      if (step.products && step.products.length > 0) {
        message += `*Recommended products: ${step.products.join(', ')}*\n`;
      }
      if (step.timing) {
        message += `*Timing: ${step.timing}*\n`;
      }
    });

    message += `\n⏰ **Frequency:** ${routine.frequency}`;
    message += `\n🕐 **Total Time:** ${routine.totalTime}`;
    
    if (routine.budgetTips) {
      message += `\n\n💡 **Budget Tips:** ${routine.budgetTips}`;
    }

    message += `\n\nI can help you find specific products for each step or show you tutorial videos! What would you like to explore first?`;

    return message;
  }

  getFallbackRoutine(routineType, session) {
    const category = routineType.category || 'skincare';
    
    const fallbackRoutines = {
      skincare: {
        title: "Basic Skincare Routine",
        description: "A gentle, effective routine suitable for most skin types",
        steps: [
          {
            step: 1,
            name: "Cleanse",
            description: "Gently cleanse your face with a mild cleanser",
            products: ["Gentle facial cleanser"],
            timing: "Morning and evening",
            tips: "Use lukewarm water and pat dry"
          },
          {
            step: 2,
            name: "Moisturize",
            description: "Apply a suitable moisturizer for your skin type",
            products: ["Facial moisturizer"],
            timing: "After cleansing",
            tips: "Apply while skin is still slightly damp"
          },
          {
            step: 3,
            name: "Sun Protection",
            description: "Apply broad-spectrum SPF 30+ sunscreen",
            products: ["Sunscreen SPF 30+"],
            timing: "Morning only",
            tips: "Reapply every 2 hours if outdoors"
          }
        ],
        frequency: "Daily",
        totalTime: "5-10 minutes",
        budgetTips: "Start with drugstore brands - they can be just as effective!"
      },
      haircare: {
        title: "Basic Hair Care Routine",
        description: "A simple routine to keep your hair healthy and manageable",
        steps: [
          {
            step: 1,
            name: "Shampoo",
            description: "Cleanse your scalp and hair with appropriate shampoo",
            products: ["Shampoo for your hair type"],
            timing: "2-3 times per week",
            tips: "Focus on the scalp, not the ends"
          },
          {
            step: 2,
            name: "Condition",
            description: "Apply conditioner to mid-lengths and ends",
            products: ["Conditioner"],
            timing: "After every shampoo",
            tips: "Leave on for 2-3 minutes before rinsing"
          },
          {
            step: 3,
            name: "Protect",
            description: "Use heat protectant before styling",
            products: ["Heat protectant spray"],
            timing: "Before heat styling",
            tips: "Apply to damp hair for best protection"
          }
        ],
        frequency: "2-3 times per week",
        totalTime: "10-15 minutes",
        budgetTips: "Invest in a good conditioner - it makes the biggest difference!"
      }
    };

    return fallbackRoutines[category] || fallbackRoutines.skincare;
  }
}

module.exports = RoutineAgent;
