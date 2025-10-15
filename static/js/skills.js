// js/skills.js
document.addEventListener('DOMContentLoaded', () => {

    // Exit early if this is not the skills list page
    if (!document.body.classList.contains('skills-list-page')) {
        return;
    }

    // Animation system is now handled by animations.js
    // No need for duplicate animation code here

    // =========================================================================
    // TOOLBAR LOGIC (SORT & FILTER)
    // =========================================================================
    const sortButton = document.getElementById('sort-button');
    const sortItems = document.getElementById('sort-items');
    if (sortButton && sortItems) {
        sortButton.addEventListener('click', (e) => {
            e.stopPropagation();
            sortItems.classList.toggle('show');
        });
        window.addEventListener('click', () => {
            if (sortItems.classList.contains('show')) {
                sortItems.classList.remove('show');
            }
        });
    }

    const scrollLeftBtn = document.getElementById('scroll-left');
    const scrollRightBtn = document.getElementById('scroll-right');
    const categoriesList = document.getElementById('categories-list');
    if (scrollLeftBtn && scrollRightBtn && categoriesList) {
        scrollLeftBtn.addEventListener('click', () => categoriesList.scrollBy({ left: -200, behavior: 'smooth' }));
        scrollRightBtn.addEventListener('click', () => categoriesList.scrollBy({ left: 200, behavior: 'smooth' }));
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
            
            const url = this.getAttribute('data-url');
            if (url) {
                // Add a small delay for visual feedback
                setTimeout(() => {
                    window.location.href = url;
                }, 100);
            }
        });
        
        // Removed hover effects for simplified interaction
    });
});