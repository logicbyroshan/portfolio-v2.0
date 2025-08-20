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
    // SUBSCRIBE MODAL & COMMENT FORM LOGIC
    // =========================================================================
    const commentForm = document.getElementById('comment-form');
    const subscribeModal = document.getElementById('subscribe-modal');
    const closeModalBtn = document.getElementById('close-subscribe-modal');
    const subscribeForm = document.getElementById('subscribe-form-modal');
    const modalMessage = document.getElementById('modal-message');

    if (subscribeModal && closeModalBtn && subscribeForm) {
        // --- Modal Controls ---
        const openSubscribeModal = () => subscribeModal.classList.add('active');
        const closeSubscribeModal = () => subscribeModal.classList.remove('active');

        closeModalBtn.addEventListener('click', closeSubscribeModal);
        subscribeModal.addEventListener('click', (e) => {
            if (e.target === subscribeModal) closeSubscribeModal();
        });

        // --- Comment Form Interception ---
        if (commentForm) {
            commentForm.addEventListener('submit', (e) => {
                // Check for a subscriber cookie
                if (document.cookie.indexOf('is_subscriber=true') === -1) {
                    e.preventDefault(); // Stop normal form submission
                    openSubscribeModal(); // Show the subscribe modal instead
                }
                // If cookie exists, let the form submit normally to the server
            });
        }

        // --- AJAX Subscription Form in Modal ---
        subscribeForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const emailInput = document.getElementById('modal-email-input');
            const email = emailInput.value;

            // Simple frontend validation
            if (!email || !email.includes('@') || !email.includes('.')) {
                modalMessage.className = 'modal-message error';
                modalMessage.textContent = 'Please enter a valid email address.';
                return;
            }

            fetch("/subscribe/", { // The URL for our NewsletterSubscribeView
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrftoken, // Use the CSRF token we retrieved
                },
                body: `email=${encodeURIComponent(email)}`
            })
            .then(response => response.json())
            .then(data => {
                modalMessage.textContent = data.message;
                if (data.success) {
                    modalMessage.className = 'modal-message success';
                    // Set a cookie (valid for 1 year) so they don't have to subscribe again
                    document.cookie = "is_subscriber=true;max-age=31536000;path=/";
                    
                    // After a short delay, close the modal and prepare the main form
                    setTimeout(() => {
                        closeSubscribeModal();
                        const mainEmailInput = commentForm.querySelector('input[name="email"]');
                        if (mainEmailInput) mainEmailInput.value = email; // Autofill email
                    }, 2000);
                } else {
                    modalMessage.className = 'modal-message error';
                }
            })
            .catch(error => {
                modalMessage.className = 'modal-message error';
                modalMessage.textContent = 'An error occurred. Please try again.';
                console.error('Subscription error:', error);
            });
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
});