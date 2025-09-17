document.addEventListener('DOMContentLoaded', () => {

    // Exit early if this is not the blog detail page
    if (!document.body.classList.contains('blog-detail-page')) {
        return;
    }

    // Helper function to get CSRF token for AJAX POST requests
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    // Set avatar colors from data attributes
    function setAvatarColors() {
        const avatars = document.querySelectorAll('.comment-avatar[data-avatar-color]');
        avatars.forEach(avatar => {
            const color = avatar.getAttribute('data-avatar-color');
            if (color) {
                avatar.style.backgroundColor = color;
            }
        });
    }
    
    // Initialize avatar colors on page load
    setAvatarColors();


    // =========================================================================
    // ON-SCROLL ANIMATION
    // =========================================================================
    const animatedElements = document.querySelectorAll('[data-animation]');
    if (animatedElements.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const delay = parseInt(entry.target.dataset.animationDelay) || 0;
                    setTimeout(() => {
                        entry.target.classList.add('is-visible');
                    }, delay);
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.1
        });
        animatedElements.forEach(el => observer.observe(el));
    }

    // =========================================================================
    // COMMENT FORM LOGIC (SIMPLIFIED)
    // =========================================================================
    const commentForm = document.getElementById('comment-form');
    
    if (commentForm) {
        // Comment form will submit normally to the server
        // No subscribe modal interception needed
        commentForm.addEventListener('submit', (e) => {
            // Just let the form submit normally
            // The server will handle the comment creation
        });
    }

    // =========================================================================
    // DYNAMIC COMMENTS SECTION LOGIC (LIKE & LOAD MORE)
    // =========================================================================
    const commentList = document.getElementById('comment-list');
    
    if (commentList) {
        const loadMoreBtn = document.getElementById('load-more-comments');
        const allComments = Array.from(commentList.querySelectorAll('.comment-item'));
        const COMMENTS_PER_PAGE = 5;
        let commentsShown = 0;

        // --- Like Button Functionality ---
        commentList.addEventListener('click', async (e) => {
            const likeBtn = e.target.closest('.like-btn');
            if (!likeBtn) return;
            
            // Prevent multiple clicks
            if (likeBtn.disabled) return;
            likeBtn.disabled = true;
            
            const commentId = likeBtn.dataset.commentId;
            if (!commentId) {
                likeBtn.disabled = false;
                return;
            }
            
            const likeIcon = likeBtn.querySelector('i');
            const likeCountSpan = likeBtn.querySelector('.like-count');
            
            try {
                // Get CSRF token
                const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value || 
                                 document.querySelector('meta[name="csrf-token"]')?.content;
                
                const response = await fetch(`/blog/comment/${commentId}/like/`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrfToken,
                    },
                });
                
                if (response.status === 401 || response.status === 403) {
                    // User not authenticated - redirect to login
                    window.location.href = `/auth/login/?next=${window.location.pathname}%23comments`;
                    return;
                }
                
                const data = await response.json();
                
                if (data.success) {
                    // Update UI based on server response
                    if (data.liked) {
                        likeBtn.classList.add('active');
                        likeIcon.classList.replace('fa-regular', 'fa-solid');
                    } else {
                        likeBtn.classList.remove('active');
                        likeIcon.classList.replace('fa-solid', 'fa-regular');
                    }
                    likeCountSpan.textContent = data.total_likes;
                } else {
                    console.error('Error toggling like:', data.error);
                }
                
            } catch (error) {
                console.error('Network error:', error);
            } finally {
                likeBtn.disabled = false;
            }
        });

        // --- Load More Comments Functionality ---
        function loadMoreComments() {
            const commentsToLoad = allComments.slice(commentsShown, commentsShown + COMMENTS_PER_PAGE);
            
            commentsToLoad.forEach(comment => {
                comment.classList.remove('hidden'); // This makes the comment visible
            });
            
            commentsShown += commentsToLoad.length;
            
            // Hide "Load More" button if all comments are now visible
            if (loadMoreBtn && commentsShown >= allComments.length) {
                loadMoreBtn.style.display = 'none';
            }
        }

        if (loadMoreBtn) {
            loadMoreBtn.addEventListener('click', loadMoreComments);
        }
        
        // Initial load of the first page of comments
        loadMoreComments();
    }

    // =========================================================================
    // ENHANCED SOCIAL SHARING
    // =========================================================================
    function initializeSocialSharing() {
        const shareButtons = document.querySelectorAll('.share-btn');
        const shareData = document.querySelector('.share-data');
        const feedbackElement = document.getElementById('share-feedback');
        
        if (!shareData) return;
        
        // Extract sharing data from hidden elements
        const blogData = {
            title: shareData.querySelector('[data-title]').getAttribute('data-title'),
            summary: shareData.querySelector('[data-summary]').getAttribute('data-summary'),
            url: shareData.querySelector('[data-url]').getAttribute('data-url'),
            image: shareData.querySelector('[data-image]').getAttribute('data-image'),
            author: shareData.querySelector('[data-author]').getAttribute('data-author'),
            date: shareData.querySelector('[data-date]').getAttribute('data-date'),
            categories: shareData.querySelector('[data-categories]').getAttribute('data-categories')
        };

        // Show feedback message
        function showFeedback(message, type = 'success') {
            const feedbackMessage = feedbackElement.querySelector('.feedback-message');
            feedbackMessage.textContent = message;
            feedbackElement.className = `share-feedback ${type}`;
            feedbackElement.style.display = 'block';
            
            setTimeout(() => {
                feedbackElement.style.display = 'none';
            }, 3000);
        }

        // Generate platform-specific share URLs and content
        function getShareUrl(platform) {
            const encodedTitle = encodeURIComponent(blogData.title);
            const encodedSummary = encodeURIComponent(blogData.summary);
            const encodedUrl = encodeURIComponent(blogData.url);
            const encodedImage = encodeURIComponent(blogData.image);
            
            const shareText = `${blogData.title} - A great read by ${blogData.author}`;
            const encodedShareText = encodeURIComponent(shareText);
            
            const hashTags = blogData.categories.split(', ').map(cat => 
                cat.replace(/\s+/g, '').toLowerCase()
            ).join(',');

            switch (platform) {
                case 'twitter':
                    return `https://twitter.com/intent/tweet?text=${encodedShareText}&url=${encodedUrl}&hashtags=${hashTags}`;
                
                case 'linkedin':
                    return `https://www.linkedin.com/sharing/share-offsite/?url=${encodedUrl}&title=${encodedTitle}&summary=${encodedSummary}`;
                
                case 'facebook':
                    return `https://www.facebook.com/sharer/sharer.php?u=${encodedUrl}&quote=${encodedShareText}`;
                
                case 'whatsapp':
                    const whatsappText = `${blogData.title}\n\n${blogData.summary}\n\nRead more: ${blogData.url}`;
                    return `https://wa.me/?text=${encodeURIComponent(whatsappText)}`;
                
                case 'reddit':
                    return `https://reddit.com/submit?url=${encodedUrl}&title=${encodedTitle}`;
                
                case 'telegram':
                    const telegramText = `${blogData.title}\n\n${blogData.summary}\n\n${blogData.url}`;
                    return `https://t.me/share/url?url=${encodedUrl}&text=${encodeURIComponent(telegramText)}`;
                
                case 'email':
                    const emailSubject = `Check out: ${blogData.title}`;
                    const emailBody = `Hi there!\n\nI thought you might be interested in this article:\n\n"${blogData.title}"\nBy ${blogData.author} • ${blogData.date}\n\n${blogData.summary}\n\nRead the full article: ${blogData.url}\n\nBest regards!`;
                    return `mailto:?subject=${encodeURIComponent(emailSubject)}&body=${encodeURIComponent(emailBody)}`;
                
                default:
                    return blogData.url;
            }
        }

        // Handle share button clicks
        shareButtons.forEach(button => {
            button.addEventListener('click', async (e) => {
                e.preventDefault();
                const platform = button.getAttribute('data-platform');
                
                if (platform === 'copy') {
                    // Copy link to clipboard
                    try {
                        await navigator.clipboard.writeText(blogData.url);
                        showFeedback('Link copied to clipboard!', 'success');
                    } catch (err) {
                        // Fallback for older browsers
                        const textArea = document.createElement('textarea');
                        textArea.value = blogData.url;
                        document.body.appendChild(textArea);
                        textArea.select();
                        document.execCommand('copy');
                        document.body.removeChild(textArea);
                        showFeedback('Link copied to clipboard!', 'success');
                    }
                } else {
                    // Open share URL in new window
                    const shareUrl = getShareUrl(platform);
                    const windowFeatures = 'width=600,height=400,scrollbars=yes,resizable=yes';
                    
                    try {
                        window.open(shareUrl, '_blank', windowFeatures);
                        showFeedback(`Opened ${platform.charAt(0).toUpperCase() + platform.slice(1)} share dialog`, 'success');
                    } catch (err) {
                        showFeedback('Could not open share dialog', 'error');
                    }
                }
            });
        });
    }

    // Initialize social sharing
    initializeSocialSharing();
});