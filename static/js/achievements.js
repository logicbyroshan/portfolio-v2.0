// js/achievements.js
document.addEventListener('DOMContentLoaded', () => {

    // Exit early if this is not the achievements list page
    if (!document.body.classList.contains('achievements-list-page')) {
        return;
    }

    // Animation system is now handled by animations.js
    // No need for duplicate animation code here

    // Toolbar: Sort Dropdown Logic
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

    // Toolbar: Category Scroller Logic
    const scrollLeftBtn = document.getElementById('scroll-left');
    const scrollRightBtn = document.getElementById('scroll-right');
    const categoriesList = document.getElementById('categories-list');
    if (scrollLeftBtn && scrollRightBtn && categoriesList) {
        scrollLeftBtn.addEventListener('click', () => categoriesList.scrollBy({ left: -200, behavior: 'smooth' }));
        scrollRightBtn.addEventListener('click', () => categoriesList.scrollBy({ left: 200, behavior: 'smooth' }));
    }

    // Masonry Layout for Achievement Cards
    function initMasonryLayout() {
        const grid = document.querySelector('.achievements-grid');
        const cards = document.querySelectorAll('.achievement-card');
        
        if (!grid || cards.length === 0) return;

        // Reset any existing grid positioning
        cards.forEach(card => {
            card.style.gridRowEnd = '';
        });

        // Calculate row span for each card based on its height
        function setCardPosition(card) {
            const cardHeight = card.getBoundingClientRect().height;
            const rowHeight = parseInt(window.getComputedStyle(grid).getPropertyValue('grid-auto-rows'));
            const rowGap = parseInt(window.getComputedStyle(grid).getPropertyValue('gap'));
            
            const rowSpan = Math.ceil((cardHeight + rowGap) / (rowHeight + rowGap));
            card.style.gridRowEnd = `span ${rowSpan}`;
        }

        // Apply masonry layout
        function applyMasonryLayout() {
            cards.forEach(card => {
                // Wait for images to load before calculating height
                const images = card.querySelectorAll('img');
                if (images.length > 0) {
                    let loadedImages = 0;
                    images.forEach(img => {
                        if (img.complete) {
                            loadedImages++;
                        } else {
                            img.addEventListener('load', () => {
                                loadedImages++;
                                if (loadedImages === images.length) {
                                    setCardPosition(card);
                                }
                            });
                        }
                    });
                    if (loadedImages === images.length) {
                        setCardPosition(card);
                    }
                } else {
                    setCardPosition(card);
                }
            });
        }

        // Initial layout
        setTimeout(applyMasonryLayout, 100);

        // Re-apply on window resize
        let resizeTimeout;
        window.addEventListener('resize', () => {
            clearTimeout(resizeTimeout);
            resizeTimeout = setTimeout(applyMasonryLayout, 250);
        });
    }

    // Initialize masonry layout
    initMasonryLayout();
});