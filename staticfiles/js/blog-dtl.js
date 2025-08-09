document.addEventListener('DOMContentLoaded', () => {

    // Exit early if this is not the blog detail page
    if (!document.body.classList.contains('blog-detail-page')) {
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
    // COMMENTS SECTION LOGIC
    // =========================================================================
    const commentList = document.getElementById('comment-list');
    
    if (commentList) {
        const loadMoreBtn = document.getElementById('load-more-comments');
        const allComments = Array.from(commentList.querySelectorAll('.comment-item'));
        const COMMENTS_PER_PAGE = 5;
        let commentsShown = 0;

        // --- Like Button Functionality ---
        commentList.addEventListener('click', (e) => {
            const likeBtn = e.target.closest('.like-btn');
            if (!likeBtn) return;
            
            const likeIcon = likeBtn.querySelector('i');
            const likeCountSpan = likeBtn.querySelector('.like-count');
            let likeCount = parseInt(likeCountSpan.textContent);

            if (likeBtn.classList.contains('active')) {
                likeBtn.classList.remove('active');
                likeIcon.classList.remove('fa-solid'); // Switch to regular heart
                likeIcon.classList.add('fa-regular');
                likeCount--;
            } else {
                likeBtn.classList.add('active');
                likeIcon.classList.remove('fa-regular');
                likeIcon.classList.add('fa-solid'); // Switch to solid heart
                likeCount++;
            }
            likeCountSpan.textContent = likeCount;
        });

        // --- Load More Comments Functionality ---
        function loadMoreComments() {
            const fragment = document.createDocumentFragment();
            const commentsToLoad = allComments.slice(commentsShown, commentsShown + COMMENTS_PER_PAGE);
            
            commentsToLoad.forEach(comment => {
                comment.classList.remove('hidden');
                // We don't need to append, just show them as they are already in the DOM
            });
            
            commentsShown += commentsToLoad.length;
            
            // Hide "Load More" button if all comments are shown
            if (commentsShown >= allComments.length) {
                loadMoreBtn.style.display = 'none';
            }
        }

        if (loadMoreBtn && allComments.length > 0) {
            loadMoreBtn.addEventListener('click', loadMoreComments);
            // Initial load
            loadMoreComments();
        } else if (loadMoreBtn) {
            // Hide button if there are no comments to begin with
            loadMoreBtn.style.display = 'none';
        }
    }
});