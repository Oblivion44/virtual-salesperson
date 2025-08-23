const axios = require('axios');
const fs = require('fs').promises;
const csv = require('csv-parser');
const natural = require('natural');
const sentiment = require('sentiment');

class ProductService {
  constructor() {
    this.products = [];
    this.reviews = [];
    this.sentimentAnalyzer = new sentiment();
    this.nykaaBaseUrl = process.env.NYKAA_API_BASE_URL || 'https://www.nykaa.com';
    this.affiliateId = process.env.NYKAA_AFFILIATE_ID;
    
    // Initialize product data
    this.loadProductData();
  }

  async loadProductData() {
    try {
      // In a real implementation, you would load from CSV files
      // For now, we'll use sample data
      this.products = this.getSampleProducts();
      this.reviews = this.getSampleReviews();
      
      console.log(`Loaded ${this.products.length} products and ${this.reviews.length} reviews`);
    } catch (error) {
      console.error('Error loading product data:', error);
      this.products = this.getSampleProducts();
    }
  }

  async searchProducts(query, filters = {}) {
    try {
      let filteredProducts = [...this.products];

      // Text search
      if (query) {
        const searchTerms = query.toLowerCase().split(' ');
        filteredProducts = filteredProducts.filter(product => {
          const searchText = `${product.name} ${product.brand} ${product.category} ${product.description}`.toLowerCase();
          return searchTerms.some(term => searchText.includes(term));
        });
      }

      // Apply filters
      if (filters.category) {
        filteredProducts = filteredProducts.filter(p => 
          p.category.toLowerCase() === filters.category.toLowerCase()
        );
      }

      if (filters.skinType) {
        filteredProducts = filteredProducts.filter(p => 
          p.suitableFor && p.suitableFor.includes(filters.skinType)
        );
      }

      if (filters.concerns && filters.concerns.length > 0) {
        filteredProducts = filteredProducts.filter(p => 
          p.concerns && filters.concerns.some(concern => 
            p.concerns.includes(concern)
          )
        );
      }

      if (filters.priceRange) {
        const [min, max] = filters.priceRange;
        filteredProducts = filteredProducts.filter(p => 
          p.price >= min && p.price <= max
        );
      }

      if (filters.ageGroup) {
        filteredProducts = filteredProducts.filter(p => 
          p.ageGroups && p.ageGroups.includes(filters.ageGroup)
        );
      }

      // Sort by relevance and rating
      filteredProducts.sort((a, b) => {
        // Prioritize higher ratings
        if (b.rating !== a.rating) {
          return b.rating - a.rating;
        }
        // Then by number of reviews
        return b.reviewCount - a.reviewCount;
      });

      // Limit results
      return filteredProducts.slice(0, 20);
    } catch (error) {
      console.error('Error searching products:', error);
      return [];
    }
  }

  async getProductDetails(productIds) {
    try {
      const products = productIds.map(id => {
        const product = this.products.find(p => p.id === id || p.name === id);
        if (product) {
          return {
            ...product,
            nykaaUrl: this.generateNykaaUrl(product),
            reviews: this.getProductReviews(product.id),
            sentiment: this.analyzeProductSentiment(product.id)
          };
        }
        return null;
      }).filter(Boolean);

      return products;
    } catch (error) {
      console.error('Error getting product details:', error);
      return [];
    }
  }

  getProductReviews(productId, limit = 5) {
    const productReviews = this.reviews.filter(r => r.productId === productId);
    
    // Filter for positive sentiment reviews
    const positiveReviews = productReviews.filter(review => {
      const analysis = this.sentimentAnalyzer.analyze(review.text);
      return analysis.score > 0;
    });

    return positiveReviews.slice(0, limit);
  }

  analyzeProductSentiment(productId) {
    const productReviews = this.reviews.filter(r => r.productId === productId);
    
    if (productReviews.length === 0) {
      return { score: 0, positive: 0, negative: 0, neutral: 0 };
    }

    let totalScore = 0;
    let positive = 0;
    let negative = 0;
    let neutral = 0;

    productReviews.forEach(review => {
      const analysis = this.sentimentAnalyzer.analyze(review.text);
      totalScore += analysis.score;
      
      if (analysis.score > 0) positive++;
      else if (analysis.score < 0) negative++;
      else neutral++;
    });

    return {
      score: totalScore / productReviews.length,
      positive: (positive / productReviews.length) * 100,
      negative: (negative / productReviews.length) * 100,
      neutral: (neutral / productReviews.length) * 100
    };
  }

  generateNykaaUrl(product) {
    // Generate Nykaa URL with affiliate tracking
    const baseUrl = `${this.nykaaBaseUrl}/product/${product.slug || product.name.toLowerCase().replace(/\s+/g, '-')}`;
    
    if (this.affiliateId) {
      return `${baseUrl}?affiliate=${this.affiliateId}`;
    }
    
    return baseUrl;
  }

  async getRecommendations(userProfile, limit = 5) {
    try {
      const filters = {
        category: userProfile.category,
        skinType: userProfile.skinType,
        concerns: userProfile.concerns,
        ageGroup: userProfile.ageGroup
      };

      // If budget is specified, add price filter
      if (userProfile.budget) {
        const budgetRange = this.parseBudget(userProfile.budget);
        if (budgetRange) {
          filters.priceRange = budgetRange;
        }
      }

      const recommendations = await this.searchProducts('', filters);
      return recommendations.slice(0, limit);
    } catch (error) {
      console.error('Error getting recommendations:', error);
      return this.getSampleProducts().slice(0, limit);
    }
  }

  parseBudget(budgetString) {
    // Parse budget strings like "under 1000", "500-1500", "around 800"
    const budgetLower = budgetString.toLowerCase();
    
    if (budgetLower.includes('under')) {
      const match = budgetLower.match(/under\s+(\d+)/);
      if (match) {
        return [0, parseInt(match[1])];
      }
    }
    
    if (budgetLower.includes('around') || budgetLower.includes('about')) {
      const match = budgetLower.match(/(?:around|about)\s+(\d+)/);
      if (match) {
        const amount = parseInt(match[1]);
        return [amount * 0.7, amount * 1.3]; // ±30%
      }
    }
    
    // Range format: "500-1500"
    const rangeMatch = budgetLower.match(/(\d+)\s*-\s*(\d+)/);
    if (rangeMatch) {
      return [parseInt(rangeMatch[1]), parseInt(rangeMatch[2])];
    }
    
    return null;
  }

  getSampleProducts() {
    return [
      {
        id: 'p1',
        name: 'Cetaphil Gentle Skin Cleanser',
        brand: 'Cetaphil',
        category: 'skincare',
        subcategory: 'cleanser',
        price: 599,
        rating: 4.5,
        reviewCount: 1250,
        image: '/images/cetaphil-cleanser.jpg',
        description: 'Gentle, non-irritating cleanser for all skin types',
        suitableFor: ['sensitive', 'dry', 'normal', 'combination'],
        concerns: ['sensitivity', 'dryness'],
        ageGroups: ['teens', 'young_adults', 'adults', 'mature'],
        slug: 'cetaphil-gentle-skin-cleanser'
      },
      {
        id: 'p2',
        name: 'The Ordinary Hyaluronic Acid 2% + B5',
        brand: 'The Ordinary',
        category: 'skincare',
        subcategory: 'serum',
        price: 849,
        rating: 4.7,
        reviewCount: 2100,
        image: '/images/ordinary-hyaluronic.jpg',
        description: 'Intense hydration serum with hyaluronic acid',
        suitableFor: ['dry', 'normal', 'combination', 'oily'],
        concerns: ['dryness', 'dehydration', 'fine_lines'],
        ageGroups: ['young_adults', 'adults', 'mature'],
        slug: 'the-ordinary-hyaluronic-acid-2-b5'
      },
      {
        id: 'p3',
        name: 'Maybelline Fit Me Foundation',
        brand: 'Maybelline',
        category: 'makeup',
        subcategory: 'foundation',
        price: 499,
        rating: 4.3,
        reviewCount: 890,
        image: '/images/maybelline-fitme.jpg',
        description: 'Natural coverage foundation for all skin tones',
        suitableFor: ['normal', 'combination', 'oily'],
        concerns: ['uneven_tone', 'coverage'],
        ageGroups: ['teens', 'young_adults', 'adults'],
        slug: 'maybelline-fit-me-foundation'
      },
      {
        id: 'p4',
        name: 'L\'Oréal Paris Total Repair 5 Shampoo',
        brand: 'L\'Oréal Paris',
        category: 'haircare',
        subcategory: 'shampoo',
        price: 399,
        rating: 4.4,
        reviewCount: 756,
        image: '/images/loreal-shampoo.jpg',
        description: 'Repairing shampoo for damaged hair',
        suitableFor: ['damaged', 'dry', 'normal'],
        concerns: ['damage', 'dryness', 'breakage'],
        ageGroups: ['teens', 'young_adults', 'adults', 'mature'],
        slug: 'loreal-paris-total-repair-5-shampoo'
      },
      {
        id: 'p5',
        name: 'Neutrogena Ultra Sheer Sunscreen SPF 50+',
        brand: 'Neutrogena',
        category: 'skincare',
        subcategory: 'sunscreen',
        price: 699,
        rating: 4.6,
        reviewCount: 1450,
        image: '/images/neutrogena-sunscreen.jpg',
        description: 'Broad spectrum sun protection with lightweight formula',
        suitableFor: ['all', 'sensitive', 'oily', 'combination'],
        concerns: ['sun_protection', 'aging_prevention'],
        ageGroups: ['teens', 'young_adults', 'adults', 'mature'],
        slug: 'neutrogena-ultra-sheer-sunscreen-spf-50'
      }
    ];
  }

  getSampleReviews() {
    return [
      {
        id: 'r1',
        productId: 'p1',
        rating: 5,
        text: 'Amazing cleanser! So gentle on my sensitive skin and removes makeup perfectly.',
        helpful: 45,
        verified: true
      },
      {
        id: 'r2',
        productId: 'p1',
        rating: 4,
        text: 'Good for daily use, doesn\'t dry out my skin like other cleansers.',
        helpful: 32,
        verified: true
      },
      {
        id: 'r3',
        productId: 'p2',
        rating: 5,
        text: 'This serum is a game changer! My skin feels so plump and hydrated.',
        helpful: 67,
        verified: true
      },
      {
        id: 'r4',
        productId: 'p3',
        rating: 4,
        text: 'Great coverage and matches my skin tone perfectly. Lasts all day.',
        helpful: 28,
        verified: true
      },
      {
        id: 'r5',
        productId: 'p4',
        rating: 4,
        text: 'Really helps with my damaged hair. Noticed less breakage after a month.',
        helpful: 41,
        verified: true
      }
    ];
  }
}

module.exports = ProductService;
