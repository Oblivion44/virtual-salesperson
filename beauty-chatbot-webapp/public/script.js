// Beauty Chatbot Frontend JavaScript
class BeautyChatApp {
    constructor() {
        this.socket = io();
        this.isConnected = false;
        this.isTyping = false;
        
        this.initializeElements();
        this.setupEventListeners();
        this.setupSocketListeners();
    }

    initializeElements() {
        // Chat elements
        this.chatMessages = document.getElementById('chatMessages');
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.videoButton = document.getElementById('videoButton');
        
        // Status elements
        this.connectionStatus = document.getElementById('connectionStatus');
        this.statusText = document.getElementById('statusText');
        
        // Suggestion elements
        this.suggestionsContainer = document.getElementById('suggestionsContainer');
        
        // Panel elements
        this.productsPanel = document.getElementById('productsPanel');
        this.videoPanel = document.getElementById('videoPanel');
        this.productsGrid = document.getElementById('productsGrid');
        this.videoContent = document.getElementById('videoContent');
        this.tutorialVideo = document.getElementById('tutorialVideo');
        this.videoLoading = document.getElementById('videoLoading');
        
        // Loading overlay
        this.loadingOverlay = document.getElementById('loadingOverlay');
        this.loadingText = document.getElementById('loadingText');
    }

    setupEventListeners() {
        // Send message on button click
        this.sendButton.addEventListener('click', () => this.sendMessage());
        
        // Send message on Enter key
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Video generation button
        this.videoButton.addEventListener('click', () => this.requestVideoTutorial());

        // Suggestion chips
        this.suggestionsContainer.addEventListener('click', (e) => {
            if (e.target.classList.contains('suggestion-chip')) {
                const message = e.target.getAttribute('data-message');
                this.sendMessage(message);
            }
        });

        // Panel close buttons
        document.getElementById('closeProducts').addEventListener('click', () => {
            this.productsPanel.classList.remove('active');
        });

        document.getElementById('closeVideo').addEventListener('click', () => {
            this.videoPanel.classList.remove('active');
        });

        // Input focus management
        this.messageInput.addEventListener('focus', () => {
            this.scrollToBottom();
        });
    }

    setupSocketListeners() {
        // Connection status
        this.socket.on('connect', () => {
            this.isConnected = true;
            this.updateConnectionStatus('Connected', true);
            console.log('Connected to beauty chatbot server');
        });

        this.socket.on('disconnect', () => {
            this.isConnected = false;
            this.updateConnectionStatus('Disconnected', false);
            console.log('Disconnected from server');
        });

        // Chat responses
        this.socket.on('bot_response', (data) => {
            this.addBotMessage(data.message, data.type, data.data);
            this.updateSuggestions(data.suggestions || []);
            this.hideLoading();
        });

        // Product recommendations
        this.socket.on('product_recommendations', (data) => {
            this.showProductRecommendations(data.products);
        });

        // Video content
        this.socket.on('video_content', (data) => {
            this.showVideoContent(data);
        });

        this.socket.on('video_generation_started', (data) => {
            this.showVideoLoading(data.message);
        });

        this.socket.on('video_generated', (data) => {
            this.showGeneratedVideo(data);
        });

        this.socket.on('video_error', (data) => {
            this.showVideoError(data.message);
        });

        // Search results
        this.socket.on('search_results', (data) => {
            this.showSearchResults(data.products);
        });

        // Error handling
        this.socket.on('error', (data) => {
            this.addBotMessage(data.message, 'error');
            this.hideLoading();
        });
    }

    sendMessage(message = null) {
        const text = message || this.messageInput.value.trim();
        if (!text || !this.isConnected) return;

        // Add user message to chat
        this.addUserMessage(text);
        
        // Clear input
        this.messageInput.value = '';
        
        // Show loading
        this.showLoading('Thinking...');
        
        // Send to server
        this.socket.emit('chat_message', {
            message: text,
            messageType: 'text',
            timestamp: new Date().toISOString()
        });

        // Hide suggestions temporarily
        this.hideSuggestions();
    }

    requestVideoTutorial() {
        const lastMessage = this.getLastUserMessage();
        if (!lastMessage) {
            this.addBotMessage("Please tell me what you'd like to learn about first, then I can create a video tutorial for you!", 'info');
            return;
        }

        this.showVideoPanel();
        this.showVideoLoading('Creating your personalized tutorial...');

        this.socket.emit('generate_video', {
            prompt: lastMessage,
            style: 'tutorial',
            duration: 10
        });
    }

    addUserMessage(text) {
        const messageDiv = this.createMessageElement(text, 'user');
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    addBotMessage(text, type = 'text', data = {}) {
        const messageDiv = this.createMessageElement(text, 'bot', type, data);
        this.chatMessages.appendChild(messageDiv);
        this.scrollToBottom();
    }

    createMessageElement(text, sender, type = 'text', data = {}) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;

        const avatar = document.createElement('div');
        avatar.className = `avatar ${sender}-avatar`;
        avatar.innerHTML = '<i class="fas fa-user-circle"></i>';

        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';

        const bubble = document.createElement('div');
        bubble.className = `message-bubble ${sender}-message`;
        
        // Handle different message types
        if (type === 'product_recommendations') {
            bubble.innerHTML = `
                <p>${text}</p>
                <button class="view-products-btn" onclick="app.showProductsPanel()">
                    <i class="fas fa-shopping-bag"></i> View Recommendations
                </button>
            `;
        } else if (type === 'video_tutorial_request') {
            bubble.innerHTML = `
                <p>${text}</p>
                <button class="view-video-btn" onclick="app.showVideoPanel()">
                    <i class="fas fa-play-circle"></i> Watch Tutorial
                </button>
            `;
        } else {
            bubble.innerHTML = `<p>${text}</p>`;
        }

        const timeDiv = document.createElement('div');
        timeDiv.className = 'message-time';
        timeDiv.textContent = this.formatTime(new Date());

        contentDiv.appendChild(bubble);
        contentDiv.appendChild(timeDiv);

        if (sender === 'user') {
            messageDiv.appendChild(contentDiv);
            messageDiv.appendChild(avatar);
        } else {
            messageDiv.appendChild(avatar);
            messageDiv.appendChild(contentDiv);
        }

        return messageDiv;
    }

    updateSuggestions(suggestions) {
        if (!suggestions || suggestions.length === 0) {
            this.hideSuggestions();
            return;
        }

        this.suggestionsContainer.innerHTML = '';
        
        suggestions.forEach(suggestion => {
            const chip = document.createElement('div');
            chip.className = 'suggestion-chip';
            chip.setAttribute('data-message', suggestion);
            
            // Add appropriate icon based on suggestion content
            let icon = 'fas fa-comment';
            if (suggestion.toLowerCase().includes('skin')) icon = 'fas fa-leaf';
            else if (suggestion.toLowerCase().includes('hair')) icon = 'fas fa-cut';
            else if (suggestion.toLowerCase().includes('makeup')) icon = 'fas fa-palette';
            else if (suggestion.toLowerCase().includes('routine')) icon = 'fas fa-calendar-alt';
            else if (suggestion.toLowerCase().includes('tutorial')) icon = 'fas fa-play-circle';
            else if (suggestion.toLowerCase().includes('product')) icon = 'fas fa-shopping-bag';

            chip.innerHTML = `<i class="${icon}"></i> ${suggestion}`;
            this.suggestionsContainer.appendChild(chip);
        });

        this.showSuggestions();
    }

    showSuggestions() {
        this.suggestionsContainer.style.display = 'flex';
    }

    hideSuggestions() {
        this.suggestionsContainer.style.display = 'none';
    }

    showProductRecommendations(products) {
        this.productsGrid.innerHTML = '';
        
        products.forEach(product => {
            const productCard = this.createProductCard(product);
            this.productsGrid.appendChild(productCard);
        });

        this.showProductsPanel();
    }

    createProductCard(product) {
        const card = document.createElement('div');
        card.className = 'product-card';
        
        card.innerHTML = `
            <img src="${product.image || '/images/placeholder-product.jpg'}" 
                 alt="${product.name}" 
                 class="product-image"
                 onerror="this.src='/images/placeholder-product.jpg'">
            <div class="product-name">${product.name}</div>
            <div class="product-price">₹${product.price}</div>
            <div class="product-rating">
                <div class="stars">${this.generateStars(product.rating || 4.5)}</div>
                <span class="rating-text">(${product.reviews || 0} reviews)</span>
            </div>
            <a href="${product.nykaaUrl || '#'}" 
               target="_blank" 
               class="product-link">
                <i class="fas fa-external-link-alt"></i> View on Nykaa
            </a>
        `;

        return card;
    }

    generateStars(rating) {
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 !== 0;
        let starsHtml = '';

        for (let i = 0; i < fullStars; i++) {
            starsHtml += '<i class="fas fa-star"></i>';
        }

        if (hasHalfStar) {
            starsHtml += '<i class="fas fa-star-half-alt"></i>';
        }

        const emptyStars = 5 - Math.ceil(rating);
        for (let i = 0; i < emptyStars; i++) {
            starsHtml += '<i class="far fa-star"></i>';
        }

        return starsHtml;
    }

    showProductsPanel() {
        this.productsPanel.classList.add('active');
    }

    showVideoPanel() {
        this.videoPanel.classList.add('active');
    }

    showVideoContent(data) {
        if (data.success && data.localPath) {
            this.videoLoading.style.display = 'none';
            this.tutorialVideo.style.display = 'block';
            this.tutorialVideo.src = data.localPath;
        } else if (data.fallback) {
            this.showVideoFallback(data.fallback);
        }
    }

    showVideoLoading(message) {
        this.videoLoading.style.display = 'block';
        this.tutorialVideo.style.display = 'none';
        this.videoLoading.querySelector('p').textContent = message;
    }

    showGeneratedVideo(data) {
        if (data.success) {
            this.showVideoContent(data);
        } else {
            this.showVideoError(data.error || 'Failed to generate video');
        }
    }

    showVideoError(message) {
        this.videoLoading.innerHTML = `
            <div style="text-align: center; color: #dc3545;">
                <i class="fas fa-exclamation-triangle" style="font-size: 2rem; margin-bottom: 1rem;"></i>
                <p>${message}</p>
                <button onclick="app.requestVideoTutorial()" style="margin-top: 1rem; padding: 0.5rem 1rem; background: #667eea; color: white; border: none; border-radius: 8px; cursor: pointer;">
                    Try Again
                </button>
            </div>
        `;
    }

    showVideoFallback(fallback) {
        this.videoContent.innerHTML = `
            <div class="text-tutorial">
                <h3><i class="fas fa-book-open"></i> ${fallback.title}</h3>
                <div class="tutorial-steps">
                    ${fallback.steps.map((step, index) => `
                        <div class="tutorial-step">
                            <div class="step-number">${index + 1}</div>
                            <div class="step-content">${step}</div>
                        </div>
                    `).join('')}
                </div>
                <p class="fallback-message">
                    <i class="fas fa-info-circle"></i> ${fallback.message}
                </p>
            </div>
        `;
    }

    showLoading(message = 'Processing...') {
        this.loadingText.textContent = message;
        this.loadingOverlay.style.display = 'flex';
    }

    hideLoading() {
        this.loadingOverlay.style.display = 'none';
    }

    updateConnectionStatus(status, connected) {
        this.statusText.textContent = status;
        this.connectionStatus.className = `status-dot ${connected ? '' : 'disconnected'}`;
    }

    scrollToBottom() {
        setTimeout(() => {
            this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        }, 100);
    }

    formatTime(date) {
        return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    }

    getLastUserMessage() {
        const userMessages = this.chatMessages.querySelectorAll('.message.user .message-bubble p');
        if (userMessages.length > 0) {
            return userMessages[userMessages.length - 1].textContent;
        }
        return null;
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.app = new BeautyChatApp();
    console.log('Beauty Chatbot App initialized');
});

// Add some additional CSS for tutorial steps
const additionalStyles = `
<style>
.view-products-btn, .view-video-btn {
    background: linear-gradient(135deg, #667eea, #764ba2);
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 8px;
    cursor: pointer;
    margin-top: 0.5rem;
    font-size: 0.9rem;
    transition: all 0.2s ease;
}

.view-products-btn:hover, .view-video-btn:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(102, 126, 234, 0.3);
}

.text-tutorial {
    padding: 1rem;
    max-width: 100%;
}

.text-tutorial h3 {
    color: #495057;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.tutorial-steps {
    margin-bottom: 1.5rem;
}

.tutorial-step {
    display: flex;
    align-items: flex-start;
    margin-bottom: 1rem;
    padding: 0.75rem;
    background: #f8f9fa;
    border-radius: 8px;
}

.step-number {
    background: #667eea;
    color: white;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.8rem;
    font-weight: 600;
    margin-right: 0.75rem;
    flex-shrink: 0;
}

.step-content {
    flex: 1;
    font-size: 0.9rem;
    line-height: 1.4;
}

.fallback-message {
    background: #e3f2fd;
    color: #1976d2;
    padding: 0.75rem;
    border-radius: 8px;
    font-size: 0.85rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
</style>
`;

document.head.insertAdjacentHTML('beforeend', additionalStyles);
