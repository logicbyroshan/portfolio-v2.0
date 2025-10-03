document.addEventListener('DOMContentLoaded', () => {

    // Exit early if this is not the skill detail page
    if (!document.body.classList.contains('skill-detail-page')) {
        return;
    }

    // Animation system is now handled by animations.js
    // No need for duplicate animation code here

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