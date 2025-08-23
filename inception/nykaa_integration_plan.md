# Nykaa.com Integration & Product Linking Plan

## Overview
This document defines the integration strategy for displaying product images from Nykaa.com and providing direct links to product listings for seamless customer experience.

## Integration Architecture

### 1. Nykaa URL Structure Analysis
```python
class NykaaURLGenerator:
    def __init__(self):
        self.base_url = "https://www.nykaa.com"
        self.image_base_url = "https://images-static.nykaa.com"
        
        # Common Nykaa URL patterns
        self.url_patterns = {
            'product_page': '{base_url}/{brand-slug}/{product-slug}/p/{product_id}',
            'product_image': '{image_base}/buynow_files/product_images/{product_id}_1.jpg',
            'brand_page': '{base_url}/brands/{brand-slug}/c/{category_id}',
            'category_page': '{base_url}/beauty/{category-slug}/c/{category_id}'
        }
    
    def generate_product_url(self, product):
        """Generate Nykaa product page URL"""
        brand_slug = self.create_url_slug(product.brand_name)
        product_slug = self.create_url_slug(product.product_name)
        
        # Primary URL format
        primary_url = f"{self.base_url}/{brand_slug}/{product_slug}/p/{product.product_id}"
        
        # Alternative formats for fallback
        alternative_urls = [
            f"{self.base_url}/product/{product.product_id}",
            f"{self.base_url}/p/{product.product_id}",
            f"{self.base_url}/beauty/{product_slug}/p/{product.product_id}"
        ]
        
        return {
            'primary': primary_url,
            'alternatives': alternative_urls
        }
    
    def generate_product_image_url(self, product):
        """Generate Nykaa product image URL"""
        # Multiple image URL patterns to try
        image_urls = [
            f"{self.image_base_url}/buynow_files/product_images/{product.product_id}_1.jpg",
            f"{self.image_base_url}/product_images/{product.product_id}/1.jpg",
            f"{self.base_url}/productimages/{product.product_id}/1.jpg",
            f"{self.image_base_url}/images/product/{product.product_id}_1_listing.jpg"
        ]
        
        return image_urls
    
    def create_url_slug(self, text):
        """Convert text to URL-friendly slug"""
        import re
        
        # Convert to lowercase and replace spaces/special chars with hyphens
        slug = re.sub(r'[^\w\s-]', '', text.lower())
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug.strip('-')
```

### 2. Image Handling System
```python
class NykaaImageHandler:
    def __init__(self):
        self.image_cache = {}
        self.fallback_images = {
            'skincare': '/static/images/skincare_placeholder.jpg',
            'haircare': '/static/images/haircare_placeholder.jpg',
            'makeup': '/static/images/makeup_placeholder.jpg'
        }
    
    def get_product_image(self, product):
        """Get product image with fallback handling"""
        
        # Check cache first
        cache_key = f"img_{product.product_id}"
        if cache_key in self.image_cache:
            return self.image_cache[cache_key]
        
        # Try multiple Nykaa image URLs
        nykaa_urls = NykaaURLGenerator().generate_product_image_url(product)
        
        for url in nykaa_urls:
            if self.verify_image_exists(url):
                self.image_cache[cache_key] = url
                return url
        
        # Fallback to category placeholder
        fallback = self.fallback_images.get(product.canonical_l1.lower(), 
                                          self.fallback_images['skincare'])
        return fallback
    
    def verify_image_exists(self, url):
        """Check if image URL is accessible"""
        try:
            import requests
            response = requests.head(url, timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def create_responsive_image_html(self, product):
        """Create responsive image HTML with multiple sources"""
        image_url = self.get_product_image(product)
        
        html = f"""
        <div class="product-image-container">
            <img src="{image_url}" 
                 alt="{product.product_name}" 
                 class="product-image"
                 loading="lazy"
                 onerror="this.src='{self.get_fallback_image(product)}'">
            <div class="image-overlay">
                <span class="brand-badge">{product.brand_name}</span>
            </div>
        </div>
        """
        
        return html
    
    def get_fallback_image(self, product):
        """Get appropriate fallback image"""
        return self.fallback_images.get(product.canonical_l1.lower(), 
                                      self.fallback_images['skincare'])
```

### 3. Product Link Generation
```python
class NykaaLinkGenerator:
    def __init__(self):
        self.url_generator = NykaaURLGenerator()
        self.tracking_params = {
            'utm_source': 'beauty_chatbot',
            'utm_medium': 'ai_recommendation',
            'utm_campaign': 'virtual_salesperson'
        }
    
    def create_product_link(self, product, link_context='recommendation'):
        """Create trackable Nykaa product link"""
        
        # Generate base URL
        urls = self.url_generator.generate_product_url(product)
        primary_url = urls['primary']
        
        # Add tracking parameters
        tracked_url = self.add_tracking_params(primary_url, product, link_context)
        
        return {
            'url': tracked_url,
            'display_text': f"View {product.product_name} on Nykaa",
            'fallback_urls': urls['alternatives']
        }
    
    def add_tracking_params(self, base_url, product, context):
        """Add UTM tracking parameters"""
        params = self.tracking_params.copy()
        params.update({
            'utm_content': f"{product.canonical_l1}_{product.canonical_l3}",
            'utm_term': context,
            'product_id': product.product_id
        })
        
        # Build query string
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        separator = '&' if '?' in base_url else '?'
        
        return f"{base_url}{separator}{query_string}"
    
    def create_buy_button_html(self, product, button_style='primary'):
        """Create styled buy button with Nykaa link"""
        link_data = self.create_product_link(product, 'buy_button')
        
        button_classes = {
            'primary': 'btn btn-primary nykaa-buy-btn',
            'secondary': 'btn btn-secondary nykaa-link-btn',
            'minimal': 'text-link nykaa-text-link'
        }
        
        css_class = button_classes.get(button_style, button_classes['primary'])
        
        html = f"""
        <a href="{link_data['url']}" 
           target="_blank" 
           rel="noopener noreferrer"
           class="{css_class}"
           data-product-id="{product.product_id}"
           onclick="trackNykaaClick('{product.product_id}', 'buy_button')">
            🛒 Buy on Nykaa - ₹{product.mrp}
        </a>
        """
        
        return html
```

### 4. Product Card Integration
```python
class NykaaProductCard:
    def __init__(self, image_handler, link_generator):
        self.image_handler = image_handler
        self.link_generator = link_generator
    
    def create_product_card(self, product, recommendation_data=None):
        """Create complete product card with Nykaa integration"""
        
        # Get image and link
        image_html = self.image_handler.create_responsive_image_html(product)
        buy_button = self.link_generator.create_buy_button_html(product)
        
        # Build product card
        card_html = f"""
        <div class="product-card" data-product-id="{product.product_id}">
            {image_html}
            
            <div class="product-info">
                <h3 class="product-name">{product.product_name}</h3>
                <p class="product-brand">{product.brand_name}</p>
                <div class="product-price">₹{product.mrp}</div>
                
                {self.render_product_highlights(product)}
                {self.render_recommendation_reason(recommendation_data)}
                {self.render_customer_reviews(product)}
            </div>
            
            <div class="product-actions">
                {buy_button}
                <button class="btn btn-outline learn-more-btn" 
                        onclick="showProductDetails('{product.product_id}')">
                    Learn More
                </button>
            </div>
        </div>
        """
        
        return card_html
    
    def render_product_highlights(self, product):
        """Render key product highlights"""
        highlights = []
        
        # Key ingredients
        if product.ingredients:
            key_ingredients = product.ingredients.split(',')[:3]
            highlights.append(f"Key ingredients: {', '.join(key_ingredients)}")
        
        # Addresses concerns
        if product.concerns:
            concerns = product.concerns.split(',')[:2]
            highlights.append(f"Addresses: {', '.join(concerns)}")
        
        html = '<div class="product-highlights">'
        for highlight in highlights:
            html += f'<span class="highlight-tag">✨ {highlight}</span>'
        html += '</div>'
        
        return html
    
    def create_product_carousel(self, products, title="Recommended Products"):
        """Create carousel of product cards"""
        
        carousel_html = f"""
        <div class="product-carousel">
            <h3 class="carousel-title">{title}</h3>
            <div class="carousel-container">
                <div class="carousel-track">
        """
        
        for product in products:
            card_html = self.create_product_card(product)
            carousel_html += f'<div class="carousel-item">{card_html}</div>'
        
        carousel_html += """
                </div>
                <button class="carousel-btn prev-btn" onclick="slideCarousel(-1)">‹</button>
                <button class="carousel-btn next-btn" onclick="slideCarousel(1)">›</button>
            </div>
        </div>
        """
        
        return carousel_html
```

### 5. Link Validation and Fallback System
```python
class NykaaLinkValidator:
    def __init__(self):
        self.validation_cache = {}
        self.cache_duration = 3600  # 1 hour
    
    def validate_product_link(self, product):
        """Validate that Nykaa link is accessible"""
        
        cache_key = f"link_{product.product_id}"
        
        # Check cache
        if cache_key in self.validation_cache:
            cached_data = self.validation_cache[cache_key]
            if time.time() - cached_data['timestamp'] < self.cache_duration:
                return cached_data['result']
        
        # Generate and test URLs
        url_generator = NykaaURLGenerator()
        urls = url_generator.generate_product_url(product)
        
        # Test primary URL
        if self.test_url_accessibility(urls['primary']):
            result = {'status': 'valid', 'url': urls['primary']}
        else:
            # Try alternatives
            for alt_url in urls['alternatives']:
                if self.test_url_accessibility(alt_url):
                    result = {'status': 'alternative', 'url': alt_url}
                    break
            else:
                result = {'status': 'invalid', 'url': None}
        
        # Cache result
        self.validation_cache[cache_key] = {
            'result': result,
            'timestamp': time.time()
        }
        
        return result
    
    def test_url_accessibility(self, url):
        """Test if URL is accessible"""
        try:
            import requests
            response = requests.head(url, timeout=10, allow_redirects=True)
            return response.status_code in [200, 301, 302]
        except:
            return False
    
    def handle_invalid_links(self, product):
        """Handle products with invalid Nykaa links"""
        
        # Create generic search link
        search_query = f"{product.brand_name} {product.product_name}".replace(' ', '+')
        search_url = f"https://www.nykaa.com/search/result/?q={search_query}"
        
        return {
            'status': 'search_fallback',
            'url': search_url,
            'message': f"Search for {product.product_name} on Nykaa"
        }
```

### 6. Analytics and Tracking
```python
class NykaaClickTracker:
    def __init__(self):
        self.click_data = []
    
    def track_nykaa_click(self, product_id, click_context, customer_profile):
        """Track clicks to Nykaa links"""
        
        click_event = {
            'timestamp': time.time(),
            'product_id': product_id,
            'context': click_context,  # 'recommendation', 'buy_button', 'learn_more'
            'customer_age_group': customer_profile.age_group,
            'customer_concerns': customer_profile.concerns,
            'session_id': customer_profile.session_id
        }
        
        self.click_data.append(click_event)
        
        # Send to analytics service
        self.send_to_analytics(click_event)
    
    def generate_click_analytics(self):
        """Generate analytics report on Nykaa clicks"""
        
        if not self.click_data:
            return {}
        
        analytics = {
            'total_clicks': len(self.click_data),
            'clicks_by_context': {},
            'clicks_by_age_group': {},
            'top_clicked_products': {},
            'conversion_funnel': self.calculate_conversion_funnel()
        }
        
        for click in self.click_data:
            # Context analysis
            context = click['context']
            analytics['clicks_by_context'][context] = analytics['clicks_by_context'].get(context, 0) + 1
            
            # Age group analysis
            age_group = click['customer_age_group']
            analytics['clicks_by_age_group'][age_group] = analytics['clicks_by_age_group'].get(age_group, 0) + 1
            
            # Product popularity
            product_id = click['product_id']
            analytics['top_clicked_products'][product_id] = analytics['top_clicked_products'].get(product_id, 0) + 1
        
        return analytics
```

### 7. Mobile Optimization
```python
class MobileNykaaIntegration:
    def __init__(self):
        self.mobile_patterns = {
            'app_deep_link': 'nykaa://product/{product_id}',
            'mobile_web': 'https://m.nykaa.com/product/{product_id}',
            'amp_page': 'https://www.nykaa.com/amp/product/{product_id}'
        }
    
    def create_mobile_optimized_link(self, product, user_agent):
        """Create mobile-optimized Nykaa links"""
        
        if self.is_mobile_app_available(user_agent):
            # Try app deep link first
            app_link = self.mobile_patterns['app_deep_link'].format(product_id=product.product_id)
            fallback_link = self.mobile_patterns['mobile_web'].format(product_id=product.product_id)
            
            return {
                'primary': app_link,
                'fallback': fallback_link,
                'type': 'app_deep_link'
            }
        else:
            # Mobile web version
            mobile_link = self.mobile_patterns['mobile_web'].format(product_id=product.product_id)
            return {
                'primary': mobile_link,
                'type': 'mobile_web'
            }
    
    def create_mobile_product_card(self, product):
        """Create mobile-optimized product card"""
        
        # Simplified layout for mobile
        mobile_card = f"""
        <div class="mobile-product-card">
            <div class="mobile-product-image">
                <img src="{self.get_mobile_optimized_image(product)}" 
                     alt="{product.product_name}">
            </div>
            <div class="mobile-product-info">
                <h4>{product.product_name}</h4>
                <p class="mobile-brand">{product.brand_name}</p>
                <div class="mobile-price">₹{product.mrp}</div>
                <a href="{self.create_mobile_optimized_link(product, '')['primary']}" 
                   class="mobile-buy-btn">
                   Buy Now
                </a>
            </div>
        </div>
        """
        
        return mobile_card
```

## Implementation Checklist

### Phase 1: Basic Integration
- [ ] Implement URL generation for Nykaa product pages
- [ ] Create image handling with fallback system
- [ ] Build basic product card with Nykaa links
- [ ] Add click tracking functionality

### Phase 2: Enhanced Features
- [ ] Implement link validation and fallback system
- [ ] Create responsive product carousels
- [ ] Add mobile optimization
- [ ] Implement analytics and reporting

### Phase 3: Advanced Integration
- [ ] Add A/B testing for different link formats
- [ ] Implement caching for better performance
- [ ] Create advanced tracking and attribution
- [ ] Add error handling and monitoring

## Success Metrics
- **Link Accuracy**: 95%+ working Nykaa links
- **Image Load Success**: 90%+ product images display correctly
- **Click-Through Rate**: 15%+ customers click Nykaa links
- **Mobile Performance**: <3 second load time on mobile devices
