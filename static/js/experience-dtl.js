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

});