const axios = require('axios');
const fs = require('fs').promises;
const path = require('path');
const { v4: uuidv4 } = require('uuid');

class VideoGenerator {
  constructor() {
    this.apiKey = process.env.NOVELAI_API_KEY;
    this.baseUrl = process.env.NOVELAI_REEL_ENDPOINT || 'https://api.novelai.net/ai/generate-video';
    this.videoStoragePath = process.env.VIDEO_STORAGE_PATH || './public/videos';
    
    // Ensure video storage directory exists
    this.ensureStorageDirectory();
  }

  async ensureStorageDirectory() {
    try {
      await fs.mkdir(this.videoStoragePath, { recursive: true });
    } catch (error) {
      console.error('Error creating video storage directory:', error);
    }
  }

  async generateVideo(options) {
    const {
      prompt,
      style = 'tutorial',
      duration = 10,
      userId,
      aspectRatio = '16:9',
      quality = 'high'
    } = options;

    try {
      // Generate unique video ID
      const videoId = uuidv4();
      const filename = `${videoId}.mp4`;
      const filePath = path.join(this.videoStoragePath, filename);

      // Prepare NovelAI Reel request
      const requestData = {
        prompt: this.enhancePrompt(prompt, style),
        duration: Math.min(duration, 30), // Cap at 30 seconds
        aspect_ratio: aspectRatio,
        quality: quality,
        style: this.getStylePreset(style),
        seed: Math.floor(Math.random() * 1000000)
      };

      console.log(`Generating video for user ${userId}: ${prompt}`);

      // Make request to NovelAI Reel API
      const response = await axios.post(this.baseUrl, requestData, {
        headers: {
          'Authorization': `Bearer ${this.apiKey}`,
          'Content-Type': 'application/json'
        },
        timeout: 120000 // 2 minute timeout
      });

      // Handle the response based on NovelAI's API structure
      let videoUrl;
      if (response.data.video_url) {
        // Direct URL provided
        videoUrl = response.data.video_url;
      } else if (response.data.task_id) {
        // Async generation - poll for completion
        videoUrl = await this.pollForCompletion(response.data.task_id);
      } else {
        throw new Error('Unexpected API response format');
      }

      // Download and save video locally
      const localPath = await this.downloadVideo(videoUrl, filePath);

      return {
        success: true,
        videoId,
        localPath: `/videos/${filename}`,
        originalPrompt: prompt,
        enhancedPrompt: requestData.prompt,
        duration: duration,
        style: style,
        metadata: {
          generatedAt: new Date().toISOString(),
          userId: userId,
          fileSize: await this.getFileSize(localPath)
        }
      };

    } catch (error) {
      console.error('Video generation error:', error);
      
      // Return fallback response
      return {
        success: false,
        error: error.message,
        fallback: this.getFallbackContent(prompt, style)
      };
    }
  }

  async generateTutorial(topic) {
    const tutorialPrompts = {
      'skincare_routine': 'A person demonstrating a gentle skincare routine, applying cleanser, toner, and moisturizer with proper techniques, clean aesthetic, natural lighting',
      'makeup_application': 'Professional makeup application tutorial showing foundation, concealer, and basic eye makeup techniques, clean beauty setup',
      'hair_styling': 'Hair styling tutorial showing how to create loose waves using a curling iron, professional salon setting',
      'ingredient_education': 'Close-up shots of skincare ingredients like hyaluronic acid serum, vitamin C, and retinol with text overlays explaining benefits'
    };

    const prompt = tutorialPrompts[topic] || `Beauty tutorial about ${topic}, professional, educational, clean aesthetic`;

    return await this.generateVideo({
      prompt,
      style: 'tutorial',
      duration: 10
    });
  }

  enhancePrompt(originalPrompt, style) {
    const styleEnhancements = {
      tutorial: 'professional beauty tutorial, clean aesthetic, good lighting, educational, step-by-step demonstration',
      product_demo: 'product demonstration, before and after, clean background, professional photography',
      routine: 'beauty routine demonstration, natural movements, clean setup, lifestyle aesthetic',
      ingredient_focus: 'close-up product shots, ingredient focus, clean aesthetic, professional photography'
    };

    const baseEnhancement = styleEnhancements[style] || styleEnhancements.tutorial;
    
    return `${originalPrompt}, ${baseEnhancement}, high quality, 4K, professional lighting, beauty content, no intro or outro, direct to content`;
  }

  getStylePreset(style) {
    const presets = {
      tutorial: 'educational',
      product_demo: 'commercial',
      routine: 'lifestyle',
      ingredient_focus: 'macro'
    };

    return presets[style] || 'educational';
  }

  async pollForCompletion(taskId, maxAttempts = 30) {
    for (let attempt = 0; attempt < maxAttempts; attempt++) {
      try {
        const response = await axios.get(`${this.baseUrl}/status/${taskId}`, {
          headers: {
            'Authorization': `Bearer ${this.apiKey}`
          }
        });

        if (response.data.status === 'completed') {
          return response.data.video_url;
        } else if (response.data.status === 'failed') {
          throw new Error('Video generation failed');
        }

        // Wait 4 seconds before next poll
        await new Promise(resolve => setTimeout(resolve, 4000));
      } catch (error) {
        if (attempt === maxAttempts - 1) {
          throw error;
        }
      }
    }

    throw new Error('Video generation timeout');
  }

  async downloadVideo(videoUrl, localPath) {
    const response = await axios({
      method: 'GET',
      url: videoUrl,
      responseType: 'stream'
    });

    const writer = require('fs').createWriteStream(localPath);
    response.data.pipe(writer);

    return new Promise((resolve, reject) => {
      writer.on('finish', () => resolve(localPath));
      writer.on('error', reject);
    });
  }

  async getFileSize(filePath) {
    try {
      const stats = await fs.stat(filePath);
      return stats.size;
    } catch {
      return 0;
    }
  }

  getFallbackContent(prompt, style) {
    // Return text-based tutorial content when video generation fails
    const fallbackContent = {
      type: 'text_tutorial',
      title: `Tutorial: ${prompt}`,
      steps: this.generateTextSteps(prompt, style),
      message: 'Video generation is temporarily unavailable. Here\'s a detailed text tutorial instead!'
    };

    return fallbackContent;
  }

  generateTextSteps(prompt, style) {
    // Generate basic text steps based on the prompt
    const commonSteps = {
      skincare: [
        'Start with clean hands and a clean face',
        'Apply products from thinnest to thickest consistency',
        'Use gentle upward motions when applying',
        'Allow each product to absorb before applying the next',
        'Don\'t forget your neck and décolletage'
      ],
      makeup: [
        'Start with a clean, moisturized face',
        'Apply primer and let it set',
        'Use the right tools for each product',
        'Build coverage gradually',
        'Set with powder or setting spray'
      ],
      haircare: [
        'Start with clean, towel-dried hair',
        'Apply products evenly from mid-length to ends',
        'Use heat protectant before styling',
        'Work in sections for best results',
        'Finish with a light hold product'
      ]
    };

    // Determine category from prompt
    const category = prompt.toLowerCase().includes('skin') ? 'skincare' :
                    prompt.toLowerCase().includes('makeup') ? 'makeup' :
                    prompt.toLowerCase().includes('hair') ? 'haircare' : 'skincare';

    return commonSteps[category] || commonSteps.skincare;
  }
}

module.exports = VideoGenerator;
