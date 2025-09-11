// Newsletter Form JavaScript with Toast Notifications
document.addEventListener('DOMContentLoaded', () => {
    const newsletterForm = document.getElementById('newsletter-form');
    
    if (newsletterForm) {
        const emailInput = document.getElementById('newsletter-email');
        const submitBtn = document.getElementById('newsletter-submit-btn');

        // Enhanced Form Submission with Toast Notifications
        newsletterForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            // Basic validation
            if (!validateNewsletterForm()) {
                return;
            }

            // Set loading state
            setNewsletterFormState('loading');
            
            try {
                const formData = new FormData(newsletterForm);
                const response = await fetch(newsletterForm.action, {
                    method: 'POST',
                    body: formData,
                    headers: { 
                        'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                });

                const data = await response.json();
                
                if (data.status === 'success') {
                    setNewsletterFormState('success');
                    showNewsletterToast(data.message || 'Successfully subscribed!', 'success');
                    
                    // Reset form after success
                    setTimeout(() => {
                        newsletterForm.reset();
                        setNewsletterFormState('default');
                    }, 2000);
                } else if (data.status === 'info') {
                    setNewsletterFormState('info');
                    showNewsletterToast(data.message || 'Already subscribed!', 'info');
                    setTimeout(() => setNewsletterFormState('default'), 3000);
                } else {
                    setNewsletterFormState('error');
                    showNewsletterToast(data.message || 'Subscription failed', 'error');
                    setTimeout(() => setNewsletterFormState('default'), 3000);
                }
            } catch (error) {
                console.error('Newsletter subscription error:', error);
                setNewsletterFormState('error');
                showNewsletterToast('Network error. Please try again.', 'error');
                setTimeout(() => setNewsletterFormState('default'), 3000);
            }
        });

        // Form validation
        function validateNewsletterForm() {
            const email = emailInput.value.trim();

            if (!email) {
                showNewsletterToast('Please enter your email address', 'error');
                emailInput.focus();
                return false;
            }

            if (!isValidEmail(email)) {
                showNewsletterToast('Please enter a valid email address', 'error');
                emailInput.focus();
                return false;
            }

            return true;
        }

        // Email validation
        function isValidEmail(email) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            return emailRegex.test(email);
        }

        // Newsletter form state management
        function setNewsletterFormState(state) {
            submitBtn.classList.remove('loading', 'success', 'error', 'info');
            submitBtn.disabled = false;
            
            switch (state) {
                case 'loading':
                    submitBtn.classList.add('loading');
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Subscribing...';
                    break;
                case 'success':
                    submitBtn.classList.add('success');
                    submitBtn.innerHTML = '<i class="fa-solid fa-check"></i> Subscribed!';
                    break;
                case 'info':
                    submitBtn.classList.add('info');
                    submitBtn.innerHTML = '<i class="fa-solid fa-info-circle"></i> Already subscribed';
                    break;
                case 'error':
                    submitBtn.classList.add('error');
                    submitBtn.innerHTML = '<i class="fa-solid fa-exclamation"></i> Failed';
                    break;
                default:
                    submitBtn.innerHTML = 'Subscribe';
            }
        }

        // Add input validation styling
        emailInput.addEventListener('blur', () => {
            if (emailInput.value.trim() && !isValidEmail(emailInput.value.trim())) {
                emailInput.classList.add('error');
            } else {
                emailInput.classList.remove('error');
            }
        });

        emailInput.addEventListener('input', () => {
            emailInput.classList.remove('error');
        });
    }

    // Newsletter Toast Notification System
    function showNewsletterToast(message, type = 'info') {
        // Calculate position for multiple toasts
        const existingToasts = document.querySelectorAll('.newsletter-toast');
        let bottomOffset = 20;
        
        existingToasts.forEach(toast => {
            const rect = toast.getBoundingClientRect();
            bottomOffset += rect.height + 10;
        });

        // Create toast
        const toast = document.createElement('div');
        toast.className = `newsletter-toast newsletter-toast-${type}`;
        toast.style.bottom = `${bottomOffset}px`;
        toast.innerHTML = `
            <div class="newsletter-toast-content">
                <i class="fa-solid ${getNewsletterToastIcon(type)}"></i>
                <span>${message}</span>
                <button class="newsletter-toast-close">&times;</button>
            </div>
        `;

        // Add to body
        document.body.appendChild(toast);

        // Add styles if not already present
        if (!document.querySelector('#newsletter-toast-styles')) {
            addNewsletterToastStyles();
        }

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (toast.parentNode) {
                toast.style.animation = 'slideOutDown 0.3s ease-in';
                setTimeout(() => {
                    toast.remove();
                    // Reposition remaining toasts
                    repositionNewsletterToasts();
                }, 300);
            }
        }, 5000);

        // Manual close
        toast.querySelector('.newsletter-toast-close').addEventListener('click', () => {
            toast.style.animation = 'slideOutDown 0.3s ease-in';
            setTimeout(() => {
                toast.remove();
                // Reposition remaining toasts
                repositionNewsletterToasts();
            }, 300);
        });
    }

    // Reposition remaining toasts when one is removed
    function repositionNewsletterToasts() {
        const toasts = document.querySelectorAll('.newsletter-toast');
        let bottomOffset = 20;
        
        toasts.forEach(toast => {
            toast.style.bottom = `${bottomOffset}px`;
            const rect = toast.getBoundingClientRect();
            bottomOffset += rect.height + 10;
        });
    }

    function getNewsletterToastIcon(type) {
        const icons = {
            'success': 'fa-check-circle',
            'error': 'fa-exclamation-circle',
            'warning': 'fa-exclamation-triangle',
            'info': 'fa-info-circle'
        };
        return icons[type] || icons.info;
    }

    function addNewsletterToastStyles() {
        const style = document.createElement('style');
        style.id = 'newsletter-toast-styles';
        style.textContent = `
            .newsletter-toast {
                position: fixed;
                right: 20px;
                z-index: 10001;
                animation: slideInUp 0.3s ease-out;
                max-width: 400px;
                transition: bottom 0.3s ease;
            }
            .newsletter-toast-content {
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
            .newsletter-toast-success .newsletter-toast-content {
                background: linear-gradient(135deg, rgba(46, 213, 115, 0.9) 0%, rgba(38, 201, 104, 0.9) 100%);
                color: white;
                border: 1px solid rgba(46, 213, 115, 0.3);
            }
            .newsletter-toast-error .newsletter-toast-content {
                background: linear-gradient(135deg, rgba(255, 71, 87, 0.9) 0%, rgba(255, 56, 56, 0.9) 100%);
                color: white;
                border: 1px solid rgba(255, 71, 87, 0.3);
            }
            .newsletter-toast-warning .newsletter-toast-content {
                background: linear-gradient(135deg, rgba(255, 177, 66, 0.9) 0%, rgba(255, 159, 28, 0.9) 100%);
                color: white;
                border: 1px solid rgba(255, 177, 66, 0.3);
            }
            .newsletter-toast-info .newsletter-toast-content {
                background: linear-gradient(135deg, rgba(0, 169, 255, 0.9) 0%, rgba(0, 135, 204, 0.9) 100%);
                color: white;
                border: 1px solid rgba(0, 169, 255, 0.3);
            }
            .newsletter-toast-close {
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
            .newsletter-toast-close:hover {
                opacity: 1;
            }
            
            /* Form state styles */
            .cta-form .filled-btn.loading {
                background: var(--accent-color, #00A9FF);
                opacity: 0.8;
                pointer-events: none;
            }
            .cta-form .filled-btn.success {
                background: #2ed573;
                border-color: #2ed573;
            }
            .cta-form .filled-btn.info {
                background: #3742fa;
                border-color: #3742fa;
            }
            .cta-form .filled-btn.error {
                background: #ff4757;
                border-color: #ff4757;
            }
            
            /* Input error states */
            .cta-form input.error {
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
