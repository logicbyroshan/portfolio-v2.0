document.addEventListener('DOMContentLoaded', () => {

    // Exit early if this is not the skill detail page
    if (!document.body.classList.contains('skill-detail-page')) {
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
        animatedElements.forEach(el => observer.observe(el));
    }

    // =========================================================================
    // ACCORDION LOGIC
    // =========================================================================
    const accordionContainer = document.getElementById('tech-accordion');

    if (accordionContainer) {
        const accordionItems = accordionContainer.querySelectorAll('.accordion-item');

        accordionItems.forEach(item => {
            const header = item.querySelector('.accordion-header');
            
            header.addEventListener('click', () => {
                // Check if the clicked item is already active
                const wasActive = item.classList.contains('active');

                // First, close all other accordion items
                accordionItems.forEach(otherItem => {
                    otherItem.classList.remove('active');
                });

                // If the clicked item was not active, open it
                if (!wasActive) {
                    item.classList.add('active');
                }
                // If it was already active, the loop above has already closed it.
            });
        });
    }

});