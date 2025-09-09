document.addEventListener('DOMContentLoaded', () => {

    // Exit early if this is not the project detail page
    if (!document.body.classList.contains('project-detail-page')) {
        return;
    }

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
    // IMAGE SLIDER LOGIC
    // =========================================================================
    const sliderContainer = document.getElementById('project-slider');
    
    // Only run the slider script if the slider element exists
    if (sliderContainer) {
        const slider = sliderContainer.querySelector('.slider-wrapper');
        const prevBtn = sliderContainer.querySelector('#prev-slide');
        const nextBtn = sliderContainer.querySelector('#next-slide');
        const slides = Array.from(sliderContainer.querySelectorAll('.slide'));
        
        let currentIndex = 0;
        const totalSlides = slides.length;

        function goToSlide(index) {
            // Clamp the index to be within bounds
            if (index < 0) {
                index = totalSlides - 1;
            } else if (index >= totalSlides) {
                index = 0;
            }
            
            currentIndex = index;
            
            // Move the slider wrapper - ensure exactly 100% per slide
            const translateX = -(currentIndex * 100);
            slider.style.transform = `translateX(${translateX}%)`;
            
            // Update slide indicators if they exist
            updateSlideIndicators();
            
            // Update image counter
            updateImageCounter();
        }

        function updateImageCounter() {
            const currentSlideElement = document.getElementById('current-slide');
            if (currentSlideElement) {
                currentSlideElement.textContent = currentIndex + 1;
            }
        }

        function updateSlideIndicators() {
            const indicators = sliderContainer.querySelectorAll('.slide-indicator');
            indicators.forEach((indicator, index) => {
                indicator.classList.toggle('active', index === currentIndex);
            });
        }

        function createSlideIndicators() {
            if (totalSlides <= 1) return;
            
            const indicatorsContainer = document.createElement('div');
            indicatorsContainer.className = 'slide-indicators';
            
            for (let i = 0; i < totalSlides; i++) {
                const indicator = document.createElement('button');
                indicator.className = 'slide-indicator';
                indicator.setAttribute('aria-label', `Go to slide ${i + 1}`);
                if (i === 0) indicator.classList.add('active');
                
                indicator.addEventListener('click', () => goToSlide(i));
                indicatorsContainer.appendChild(indicator);
            }
            
            sliderContainer.appendChild(indicatorsContainer);
        }

        // Event listeners for navigation buttons
        if (nextBtn) {
            nextBtn.addEventListener('click', () => {
                goToSlide(currentIndex + 1);
            });
        }

        if (prevBtn) {
            prevBtn.addEventListener('click', () => {
                goToSlide(currentIndex - 1);
            });
        }

        // Keyboard navigation
        sliderContainer.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') {
                e.preventDefault();
                goToSlide(currentIndex - 1);
            } else if (e.key === 'ArrowRight') {
                e.preventDefault();
                goToSlide(currentIndex + 1);
            }
        });

        // Touch/swipe support for mobile
        let startX = 0;
        let endX = 0;

        sliderContainer.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
        });

        sliderContainer.addEventListener('touchend', (e) => {
            endX = e.changedTouches[0].clientX;
            handleSwipe();
        });

        function handleSwipe() {
            const minSwipeDistance = 50;
            const swipeDistance = startX - endX;

            if (Math.abs(swipeDistance) > minSwipeDistance) {
                if (swipeDistance > 0) {
                    goToSlide(currentIndex + 1); // Swipe left, go to next
                } else {
                    goToSlide(currentIndex - 1); // Swipe right, go to previous
                }
            }
        }

        // Auto-play functionality (optional, can be enabled)
        let autoPlayInterval;
        const autoPlayDelay = 5000; // 5 seconds

        function startAutoPlay() {
            if (totalSlides <= 1) return;
            autoPlayInterval = setInterval(() => {
                goToSlide(currentIndex + 1);
            }, autoPlayDelay);
        }

        function stopAutoPlay() {
            if (autoPlayInterval) {
                clearInterval(autoPlayInterval);
                autoPlayInterval = null;
            }
        }

        // Pause auto-play on hover/focus
        sliderContainer.addEventListener('mouseenter', stopAutoPlay);
        sliderContainer.addEventListener('mouseleave', startAutoPlay);
        sliderContainer.addEventListener('focusin', stopAutoPlay);
        sliderContainer.addEventListener('focusout', startAutoPlay);

        // Initialize slider
        createSlideIndicators();
        goToSlide(0);
        
        // Uncomment the next line if you want auto-play enabled
        // startAutoPlay();
    }

    // =========================================================================
    // COMMENT FUNCTIONALITY
    // =========================================================================
    const commentForm = document.getElementById('comment-form');
    
    if (commentForm) {
        // Comment form will submit normally to the server
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
        let commentsLoaded = 5; // Initial 5 comments are already loaded
        
        // Get the project slug from the URL
        const pathParts = window.location.pathname.split('/');
        const projectSlug = pathParts[pathParts.length - 2]; // Assuming URL structure: /projects/slug/

        // --- Like Button Functionality ---
        commentList.addEventListener('click', (e) => {
            const likeBtn = e.target.closest('.like-btn');
            if (!likeBtn) return;
            
            const likeIcon = likeBtn.querySelector('i');
            const likeCountSpan = likeBtn.querySelector('.like-count');
            let likeCount = parseInt(likeCountSpan.textContent);

            // Toggle active state and update UI
            if (likeBtn.classList.toggle('active')) {
                likeIcon.classList.replace('fa-regular', 'fa-solid');
                likeCount++;
            } else {
                likeIcon.classList.replace('fa-solid', 'fa-regular');
                likeCount--;
            }
            likeCountSpan.textContent = likeCount;

            // Note: In a real app, you would send an AJAX request here to update the like count on the server.
        });

        // --- Load More Comments Functionality ---
        function loadMoreComments() {
            if (!loadMoreBtn) return;
            
            // Show loading state
            const originalText = loadMoreBtn.textContent;
            loadMoreBtn.textContent = 'Loading...';
            loadMoreBtn.disabled = true;
            
            // Make AJAX request to load more comments
            fetch(`/projects/${projectSlug}/load-more-comments/?offset=${commentsLoaded}`)
                .then(response => response.json())
                .then(data => {
                    if (data.comments && data.comments.length > 0) {
                        // Add new comments to the list
                        data.comments.forEach(comment => {
                            const commentHTML = createCommentHTML(comment);
                            commentList.insertAdjacentHTML('beforeend', commentHTML);
                        });
                        
                        commentsLoaded += data.comments.length;
                        
                        // Hide load more button if no more comments
                        if (!data.has_more) {
                            loadMoreBtn.style.display = 'none';
                        }
                    }
                    
                    // Reset button state
                    loadMoreBtn.textContent = originalText;
                    loadMoreBtn.disabled = false;
                })
                .catch(error => {
                    console.error('Error loading comments:', error);
                    loadMoreBtn.textContent = originalText;
                    loadMoreBtn.disabled = false;
                });
        }
        
        // Create HTML for a comment
        function createCommentHTML(comment) {
            return `
                <div class="comment-item">
                    <div class="comment-header">
                        <img src="/static/images/author-avatar.png" alt="Author Avatar" class="comment-avatar">
                        <div class="comment-meta">
                            <h4 class="comment-author">${comment.author_name}</h4>
                            <span class="comment-date">${comment.created_at}</span>
                        </div>
                    </div>
                    <div class="comment-body">
                        <p>${comment.body}</p>
                    </div>
                    <div class="comment-actions">
                        <button class="like-btn" data-comment-id="${comment.id}">
                            <i class="fa-regular fa-heart"></i>
                            <span class="like-count">${comment.likes}</span>
                        </button>
                    </div>
                </div>
            `;
        }

        if (loadMoreBtn) {
            loadMoreBtn.addEventListener('click', loadMoreComments);
        }
    }
});