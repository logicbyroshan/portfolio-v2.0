document.addEventListener('DOMContentLoaded', () => {

    // Exit early if this is not the experience detail page
    if (!document.body.classList.contains('experience-detail-page')) {
        return;
    }

    // =========================================================================
    // ON-SCROLL ANIMATION LOGIC
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

        animatedElements.forEach(element => {
            observer.observe(element);
        });
    }

    // =========================================================================
    // CLICKABLE CARDS NAVIGATION
    // =========================================================================
    const clickableCards = document.querySelectorAll('.clickable-card');
    
    clickableCards.forEach(card => {
        // Add cursor pointer style for better UX
        card.style.cursor = 'pointer';
        
        card.addEventListener('click', function(e) {
            // Check if click was on a link or button to prevent navigation conflict
            if (e.target.tagName === 'A' || e.target.tagName === 'BUTTON' || e.target.closest('a') || e.target.closest('button')) {
                return; // Let the link/button handle the click
            }
            
            const url = this.getAttribute('data-href') || this.getAttribute('data-url');
            if (url) {
                // Add a small delay for visual feedback
                this.style.transform = 'scale(0.98)';
                setTimeout(() => {
                    window.location.href = url;
                }, 100);
            }
        });
        
        // Add hover effects
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.transition = 'transform 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

});