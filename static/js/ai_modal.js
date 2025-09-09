// AI Modal Functionality

document.addEventListener('DOMContentLoaded', function() {
    const openModalBtn = document.getElementById('open-ai-modal');
    const closeModalBtn = document.getElementById('close-ai-modal');
    const modal = document.getElementById('ai-chat-modal');
    const modalOverlay = document.getElementById('ai-modal-overlay');

    // Open modal
    function openModal() {
        modal.classList.add('active');
        document.body.style.overflow = 'hidden'; // Prevent background scrolling
        
        // Hide hero stats cards to prevent overlap
        const heroStats = document.querySelectorAll('.hero-stat-card');
        heroStats.forEach(stat => stat.style.visibility = 'hidden');
        
        // Focus on textarea when modal opens
        setTimeout(() => {
            const textarea = modal.querySelector('textarea[name="question"]');
            if (textarea) {
                textarea.focus();
            }
        }, 300);
    }

    // Close modal
    function closeModal() {
        modal.classList.remove('active');
        document.body.style.overflow = ''; // Restore scrolling
        
        // Show hero stats cards again
        const heroStats = document.querySelectorAll('.hero-stat-card');
        heroStats.forEach(stat => stat.style.visibility = 'visible');
    }

    // Event listeners
    if (openModalBtn) {
        openModalBtn.addEventListener('click', openModal);
    }

    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', closeModal);
    }

    if (modalOverlay) {
        modalOverlay.addEventListener('click', closeModal);
    }

    // Close modal on Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modal.classList.contains('active')) {
            closeModal();
        }
    });

    // Character counter functionality
    const textarea = modal.querySelector('textarea[name="question"]');
    const charCounter = modal.querySelector('#char-counter');
    
    if (textarea && charCounter) {
        textarea.addEventListener('input', function() {
            const count = this.value.length;
            charCounter.textContent = count;
            
            // Auto-resize textarea
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        });
    }

    // File attachment functionality
    const attachBtn = modal.querySelector('#attach-file-btn');
    const fileInput = modal.querySelector('#ai-file-input');
    const fileDisplayContainer = modal.querySelector('#file-display-container');

    if (attachBtn && fileInput) {
        attachBtn.addEventListener('click', function() {
            fileInput.click();
        });

        fileInput.addEventListener('change', function() {
            displaySelectedFiles();
        });
    }

    function displaySelectedFiles() {
        if (!fileDisplayContainer) return;
        
        fileDisplayContainer.innerHTML = '';
        const files = fileInput.files;

        for (let i = 0; i < files.length; i++) {
            const file = files[i];
            const fileItem = document.createElement('div');
            fileItem.className = 'file-display-item';
            
            fileItem.innerHTML = `
                <i class="fas fa-file"></i>
                <span>${file.name}</span>
                <span class="remove-file" data-index="${i}">&times;</span>
            `;
            
            fileDisplayContainer.appendChild(fileItem);
        }

        // Add event listeners for file removal
        const removeButtons = fileDisplayContainer.querySelectorAll('.remove-file');
        removeButtons.forEach(button => {
            button.addEventListener('click', function() {
                const index = parseInt(this.dataset.index);
                removeFile(index);
            });
        });
    }

    function removeFile(index) {
        const dt = new DataTransfer();
        const files = fileInput.files;

        for (let i = 0; i < files.length; i++) {
            if (i !== index) {
                dt.items.add(files[i]);
            }
        }

        fileInput.files = dt.files;
        displaySelectedFiles();
    }

    // Form submission handling
    const aiForm = modal.querySelector('#ai-form');
    if (aiForm) {
        aiForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const submitBtn = this.querySelector('.submit-btn');
            const originalContent = submitBtn.innerHTML;
            
            // Show loading state
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            submitBtn.disabled = true;
            
            // Add user message to chat
            const question = textarea.value.trim();
            if (question) {
                addMessageToChat('user', question);
                textarea.value = '';
                charCounter.textContent = '0';
                textarea.style.height = 'auto';
            }
            
            // Add typing indicator
            addTypingIndicator();
            
            // Submit form data (you can modify this based on your backend implementation)
            const formData = new FormData(this);
            
            fetch(this.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                }
            })
            .then(response => response.json())
            .then(data => {
                removeTypingIndicator();
                
                if (data.success) {
                    addMessageToChat('ai', data.response);
                } else {
                    addMessageToChat('ai', 'Sorry, I encountered an error. Please try again.');
                }
            })
            .catch(error => {
                removeTypingIndicator();
                addMessageToChat('ai', 'Sorry, I encountered an error. Please try again.');
            })
            .finally(() => {
                // Restore button
                submitBtn.innerHTML = originalContent;
                submitBtn.disabled = false;
            });
        });
    }

    function addMessageToChat(type, message) {
        const messagesContainer = modal.querySelector('#ai-chat-messages');
        if (!messagesContainer) return;

        const messageDiv = document.createElement('div');
        messageDiv.className = `${type}-message`;
        
        if (type === 'user') {
            messageDiv.innerHTML = `
                <div class="message-bubble">${message}</div>
            `;
        } else {
            messageDiv.innerHTML = `
                <div class="ai-avatar">
                    <i class="fas fa-robot"></i>
                </div>
                <div class="message-bubble">${message}</div>
            `;
        }
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function addTypingIndicator() {
        const messagesContainer = modal.querySelector('#ai-chat-messages');
        if (!messagesContainer) return;

        const typingDiv = document.createElement('div');
        typingDiv.className = 'ai-message typing-indicator-message';
        typingDiv.innerHTML = `
            <div class="ai-avatar">
                <i class="fas fa-robot"></i>
            </div>
            <div class="typing-indicator">
                <div class="typing-dots">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;
        
        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    function removeTypingIndicator() {
        const typingIndicator = modal.querySelector('.typing-indicator-message');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
});
