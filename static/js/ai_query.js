// AI Query Form JavaScript
document.addEventListener('DOMContentLoaded', () => {
    const aiForm = document.getElementById('ai-form');
    
    if (aiForm) {
        const questionTextarea = aiForm.querySelector('textarea[name="question"]');
        const attachFileBtn = document.getElementById('attach-file-btn');
        const aiFileInput = document.getElementById('ai-file-input');
        const fileDisplayContainer = document.getElementById('file-display-container');
        const submitBtn = aiForm.querySelector('button[type="submit"]');

        // Enhanced Textarea Auto-Resize with smooth animation
        function autoResizeTextarea() {
            questionTextarea.style.height = 'auto';
            const newHeight = Math.min(questionTextarea.scrollHeight, 120); // Max height 120px
            questionTextarea.style.height = `${newHeight}px`;
        }

        questionTextarea.addEventListener('input', autoResizeTextarea);
        questionTextarea.addEventListener('focus', () => {
            aiForm.classList.add('focused');
        });
        questionTextarea.addEventListener('blur', () => {
            aiForm.classList.remove('focused');
        });

        // File Attachment Logic with better UX
        attachFileBtn.addEventListener('click', () => {
            aiFileInput.click();
        });

        aiFileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                // Check file size (max 10MB)
                if (file.size > 10 * 1024 * 1024) {
                    showNotification('File size must be less than 10MB', 'error');
                    aiFileInput.value = '';
                    return;
                }

                // Display file with animation
                fileDisplayContainer.innerHTML = `
                    <div class="file-display-item" style="animation: slideInUp 0.3s ease-out;">
                        <i class="fa-solid fa-file"></i>
                        <span>${file.name}</span>
                        <span class="clear-file-btn" title="Remove file">&times;</span>
                    </div>
                `;
                
                // Add file type icon
                const fileIcon = fileDisplayContainer.querySelector('.fa-file');
                const fileExtension = file.name.split('.').pop().toLowerCase();
                updateFileIcon(fileIcon, fileExtension);
            } else {
                fileDisplayContainer.innerHTML = '';
            }
        });

        // Update file icon based on file type
        function updateFileIcon(iconElement, extension) {
            const iconMap = {
                'pdf': 'fa-file-pdf',
                'doc': 'fa-file-word',
                'docx': 'fa-file-word',
                'txt': 'fa-file-text',
                'jpg': 'fa-file-image',
                'jpeg': 'fa-file-image',
                'png': 'fa-file-image',
                'gif': 'fa-file-image',
                'mp4': 'fa-file-video',
                'avi': 'fa-file-video',
                'zip': 'fa-file-archive',
                'rar': 'fa-file-archive'
            };
            
            const iconClass = iconMap[extension] || 'fa-file';
            iconElement.className = `fa-solid ${iconClass}`;
        }

        // Clear Attached File Logic with animation
        fileDisplayContainer.addEventListener('click', (e) => {
            if (e.target.classList.contains('clear-file-btn')) {
                const fileItem = e.target.closest('.file-display-item');
                fileItem.style.animation = 'slideOutUp 0.3s ease-in';
                setTimeout(() => {
                    aiFileInput.value = '';
                    fileDisplayContainer.innerHTML = '';
                }, 300);
            }
        });

        // Enhanced Form Submission with better UX
        aiForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const question = questionTextarea.value.trim();
            if (!question) {
                showNotification('Please enter a question', 'error');
                questionTextarea.focus();
                return;
            }

            // Set loading state
            setFormState('loading');
            
            try {
                const formData = new FormData(aiForm);
                const response = await fetch(aiForm.action, {
                    method: 'POST',
                    body: formData,
                    headers: { 
                        'X-CSRFToken': formData.get('csrfmiddlewaretoken'),
                        'X-Requested-With': 'XMLHttpRequest'
                    },
                });

                const data = await response.json();
                
                if (data.status === 'success') {
                    setFormState('success');
                    showNotification(data.message || 'Query submitted successfully!', 'success');
                    
                    // Reset form with animation
                    setTimeout(() => {
                        aiForm.reset();
                        fileDisplayContainer.innerHTML = '';
                        autoResizeTextarea();
                        setFormState('default');
                    }, 1500);
                } else {
                    setFormState('error');
                    showNotification(data.message || 'Submission failed', 'error');
                    setTimeout(() => setFormState('default'), 2000);
                }
            } catch (error) {
                console.error('Submission error:', error);
                setFormState('error');
                showNotification('Network error. Please try again.', 'error');
                setTimeout(() => setFormState('default'), 2000);
            }
        });

        // Form state management
        function setFormState(state) {
            aiForm.classList.remove('loading', 'success', 'error');
            submitBtn.disabled = false;
            
            switch (state) {
                case 'loading':
                    aiForm.classList.add('loading');
                    submitBtn.disabled = true;
                    submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i>';
                    break;
                case 'success':
                    aiForm.classList.add('success');
                    submitBtn.innerHTML = '<i class="fa-solid fa-check"></i>';
                    break;
                case 'error':
                    aiForm.classList.add('error');
                    submitBtn.innerHTML = '<i class="fa-solid fa-exclamation"></i>';
                    break;
                default:
                    submitBtn.innerHTML = '<i class="fa-solid fa-arrow-up"></i>';
            }
        }

        // Notification system
        function showNotification(message, type = 'info') {
            // Remove existing notification
            const existingNotification = document.querySelector('.ai-notification');
            if (existingNotification) {
                existingNotification.remove();
            }

            // Create notification
            const notification = document.createElement('div');
            notification.className = `ai-notification ai-notification-${type}`;
            notification.innerHTML = `
                <div class="ai-notification-content">
                    <i class="fa-solid ${getNotificationIcon(type)}"></i>
                    <span>${message}</span>
                    <button class="ai-notification-close">&times;</button>
                </div>
            `;

            // Add to body
            document.body.appendChild(notification);

            // Add styles if not already present
            if (!document.querySelector('#ai-notification-styles')) {
                addNotificationStyles();
            }

            // Auto-remove after 5 seconds
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.style.animation = 'slideOutDown 0.3s ease-in';
                    setTimeout(() => notification.remove(), 300);
                }
            }, 5000);

            // Manual close
            notification.querySelector('.ai-notification-close').addEventListener('click', () => {
                notification.style.animation = 'slideOutDown 0.3s ease-in';
                setTimeout(() => notification.remove(), 300);
            });
        }

        function getNotificationIcon(type) {
            const icons = {
                'success': 'fa-check-circle',
                'error': 'fa-exclamation-circle',
                'warning': 'fa-exclamation-triangle',
                'info': 'fa-info-circle'
            };
            return icons[type] || icons.info;
        }

        function addNotificationStyles() {
            const style = document.createElement('style');
            style.id = 'ai-notification-styles';
            style.textContent = `
                .ai-notification {
                    position: fixed;
                    bottom: 20px;
                    right: 20px;
                    z-index: 9998;
                    animation: slideInUp 0.3s ease-out;
                    max-width: 400px;
                }
                .ai-notification-content {
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
                .ai-notification-success .ai-notification-content {
                    background: linear-gradient(135deg, rgba(46, 213, 115, 0.9) 0%, rgba(38, 201, 104, 0.9) 100%);
                    color: white;
                }
                .ai-notification-error .ai-notification-content {
                    background: linear-gradient(135deg, rgba(255, 71, 87, 0.9) 0%, rgba(255, 56, 56, 0.9) 100%);
                    color: white;
                }
                .ai-notification-warning .ai-notification-content {
                    background: linear-gradient(135deg, rgba(255, 177, 66, 0.9) 0%, rgba(255, 159, 28, 0.9) 100%);
                    color: white;
                }
                .ai-notification-info .ai-notification-content {
                    background: linear-gradient(135deg, rgba(0, 169, 255, 0.9) 0%, rgba(0, 135, 204, 0.9) 100%);
                    color: white;
                }
                .ai-notification-close {
                    background: none;
                    border: none;
                    color: inherit;
                    font-size: 18px;
                    font-weight: bold;
                    cursor: pointer;
                    opacity: 0.8;
                    transition: opacity 0.2s;
                    margin-left: auto;
                }
                .ai-notification-close:hover {
                    opacity: 1;
                }
                @keyframes slideInRight {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
                @keyframes slideOutUp {
                    from { transform: translateY(0); opacity: 1; }
                    to { transform: translateY(-100%); opacity: 0; }
                }
                @keyframes slideOutDown {
                    from { transform: translateY(0); opacity: 1; }
                    to { transform: translateY(100%); opacity: 0; }
                }
                @keyframes slideInUp {
                    from { transform: translateY(100%); opacity: 0; }
                    to { transform: translateY(0); opacity: 1; }
                }
            `;
            document.head.appendChild(style);
        }

        // Keyboard shortcuts
        questionTextarea.addEventListener('keydown', (e) => {
            // Submit with Ctrl/Cmd + Enter
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                e.preventDefault();
                aiForm.dispatchEvent(new Event('submit'));
            }
        });

        // Initialize
        autoResizeTextarea();
    }
});
