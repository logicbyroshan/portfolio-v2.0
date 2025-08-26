// Contact Form JavaScript with Toast Notifications
document.addEventListener('DOMContentLoaded', () => {
    const contactForm = document.getElementById('contact-form');
    
    if (contactForm) {
        const submitBtn = document.getElementById('contact-submit-btn');
        const nameInput = document.getElementById('name');
        const emailInput = document.getElementById('email');
        const subjectInput = document.getElementById('subject');
        const messageInput = document.getElementById('contact-message');

        // Enhanced Form Submission with Toast Notifications
        contactForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // Basic validation
            if (!validateForm()) {
                return;
            }

            // Set loading state
            setContactFormState('loading');
            
            try {
                const formData = new FormData(contactForm);
                const response = await fetch(contactForm.action, {
                    method: 'POST',
                    body: formData,
                    headers: { 
                        'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                });

                const data = await response.json();
                
                if (data.status === 'success') {
                    setContactFormState('success');
                    showToast(data.message || 'Message sent successfully!', 'success');
                    
                    // Reset form after success
                    setTimeout(() => {
                        contactForm.reset();
                        setContactFormState('default');
                    }, 2000);
                } else {
                    setContactFormState('error');
                    showToast(data.message || 'Failed to send message', 'error');
                    setTimeout(() => setContactFormState('default'), 3000);
                }
            } catch (error) {
                console.error('Contact form submission error:', error);
                setContactFormState('error');
                showToast('Network error. Please try again.', 'error');
                setTimeout(() => setContactFormState('default'), 3000);
            }
        });

        // Form validation
        function validateForm() {
            const name = nameInput.value.trim();
            const email = emailInput.value.trim();
            const message = messageInput.value.trim();

            if (!name) {
                showToast('Please enter your name', 'error');
                nameInput.focus();
                return false;
            }

            if (!email) {
                showToast('Please enter your email', 'error');
                emailInput.focus();
                return false;
            }

            if (!isValidEmail(email)) {
                showToast('Please enter a valid email address', 'error');
                emailInput.focus();
                return false;
            }

            if (!message) {
                showToast('Please enter your message', 'error');
                messageInput.focus();
                return false;
            }

            return true;
        }

        // Email validation
        function isValidEmail(email) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(email);
        }

        // Contact form state management
        function setContactFormState(state) {
            submitBtn.classList.remove('loading', 'success', 'error');
            submitBtn.disabled = false;
            
            switch (state) {
                case 'loading':
                    submitBtn.classList.add('loading');
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Sending...';
                    break;
                case 'success':
                    submitBtn.classList.add('success');
                    submitBtn.innerHTML = '<i class="fa-solid fa-check"></i> Sent!';
                    break;
                case 'error':
                    submitBtn.classList.add('error');
                    submitBtn.innerHTML = '<i class="fa-solid fa-exclamation"></i> Failed';
                    break;
                default:
                    submitBtn.innerHTML = 'Send Message';
            }
        }

        // Add input validation styling
        [nameInput, emailInput, subjectInput, messageInput].forEach(input => {
            input.addEventListener('blur', () => {
                if (input.required && !input.value.trim()) {
                    input.classList.add('error');
                } else if (input.type === 'email' && input.value.trim() && !isValidEmail(input.value.trim())) {
                    input.classList.add('error');
                } else {
                    input.classList.remove('error');
                }
            });

            input.addEventListener('input', () => {
                input.classList.remove('error');
            });
        });
    }

    // Reusable Toast Notification System
    function showToast(message, type = 'info') {
        // Calculate position for multiple toasts
        const existingToasts = document.querySelectorAll('.contact-toast');
        let bottomOffset = 20;
        
        existingToasts.forEach(toast => {
            const rect = toast.getBoundingClientRect();
            bottomOffset += rect.height + 10;
        });

        // Create toast
        const toast = document.createElement('div');
        toast.className = `contact-toast contact-toast-${type}`;
        toast.style.bottom = `${bottomOffset}px`;
        toast.innerHTML = `
            <div class="contact-toast-content">
                <i class="fa-solid ${getToastIcon(type)}"></i>
                <span>${message}</span>
                <button class="contact-toast-close">&times;</button>
            </div>
        `;

        // Add to body
        document.body.appendChild(toast);

        // Add styles if not already present
        if (!document.querySelector('#contact-toast-styles')) {
            addContactToastStyles();
        }

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.style.animation = 'slideOutDown 0.3s ease-in';
                setTimeout(() => {
                    toast.remove();
                    // Reposition remaining toasts
                    repositionToasts();
                }, 300);
            }
        }, 5000);

        // Manual close
        toast.querySelector('.contact-toast-close').addEventListener('click', () => {
            toast.style.animation = 'slideOutDown 0.3s ease-in';
            setTimeout(() => {
                toast.remove();
                // Reposition remaining toasts
                repositionToasts();
            }, 300);
        });
    }

    // Reposition remaining toasts when one is removed
    function repositionToasts() {
        const toasts = document.querySelectorAll('.contact-toast');
        let bottomOffset = 20;
        
        toasts.forEach(toast => {
            toast.style.bottom = `${bottomOffset}px`;
            const rect = toast.getBoundingClientRect();
            bottomOffset += rect.height + 10;
        });
    }

    function getToastIcon(type) {
        const icons = {
            'success': 'fa-check-circle',
            'error': 'fa-exclamation-circle',
            'warning': 'fa-exclamation-triangle',
            'info': 'fa-info-circle'
        };
        return icons[type] || icons.info;
    }

    function addContactToastStyles() {
        const style = document.createElement('style');
        style.id = 'contact-toast-styles';
        style.textContent = `
            .contact-toast {
                position: fixed;
                right: 20px;
                z-index: 10000;
                animation: slideInUp 0.3s ease-out;
                max-width: 400px;
                transition: bottom 0.3s ease;
            }
            .contact-toast-content {
                display: flex;
                align-items: center;
                gap: 12px;
                padding: 12px 16px;
                border-radius: 8px;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
                backdrop-filter: blur(10px);
                font-size: 14px;
                font-weight: 500;
            }
            .contact-toast-success .contact-toast-content {
                background: linear-gradient(135deg, rgba(46, 213, 115, 0.9) 0%, rgba(38, 201, 104, 0.9) 100%);
                color: white;
                border: 1px solid rgba(46, 213, 115, 0.3);
            }
            .contact-toast-error .contact-toast-content {
                background: linear-gradient(135deg, rgba(255, 71, 87, 0.9) 0%, rgba(255, 56, 56, 0.9) 100%);
                color: white;
                border: 1px solid rgba(255, 71, 87, 0.3);
            }
            .contact-toast-warning .contact-toast-content {
                background: linear-gradient(135deg, rgba(255, 177, 66, 0.9) 0%, rgba(255, 159, 28, 0.9) 100%);
                color: white;
                border: 1px solid rgba(255, 177, 66, 0.3);
            }
            .contact-toast-info .contact-toast-content {
                background: linear-gradient(135deg, rgba(0, 169, 255, 0.9) 0%, rgba(0, 135, 204, 0.9) 100%);
                color: white;
                border: 1px solid rgba(0, 169, 255, 0.3);
            }
            .contact-toast-close {
                background: none;
                border: none;
                color: inherit;
                font-size: 18px;
                font-weight: bold;
                cursor: pointer;
                opacity: 0.8;
                transition: opacity 0.2s;
                margin-left: auto;
                padding: 0;
                width: 20px;
                height: 20px;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .contact-toast-close:hover {
                opacity: 1;
            }
            
            /* Form state styles */
            .outline-btn.loading {
                background: var(--accent-color, #00A9FF);
                color: white;
                pointer-events: none;
                opacity: 0.8;
            }
            .outline-btn.success {
                background: #2ed573;
                border-color: #2ed573;
                color: white;
            }
            .outline-btn.error {
                background: #ff4757;
                border-color: #ff4757;
                color: white;
            }
            
            /* Input error states */
            .form-group input.error,
            .form-group textarea.error {
                border-color: #ff4757;
                box-shadow: 0 0 0 2px rgba(255, 71, 87, 0.2);
            }
            
            @keyframes slideInUp {
                from { transform: translateY(100%); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
            @keyframes slideOutDown {
                from { transform: translateY(0); opacity: 1; }
                to { transform: translateY(100%); opacity: 0; }
            }
        `;
        document.head.appendChild(style);
    }
});
