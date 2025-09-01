// js/skills.js
document.addEventListener('DOMContentLoaded', () => {

    // Exit early if this is not the skills list page
    if (!document.body.classList.contains('skills-list-page')) {
        return;
    }

    // On-Scroll Animation
    const animatedElements = document.querySelectorAll('[data-animation]');
    if (animatedElements.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const delay = parseInt(entry.target.dataset.animationDelay) || 0;
                    setTimeout(() => entry.target.classList.add('is-visible'), delay);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });
        animatedElements.forEach(el => observer.observe(el));
    }

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
        
        const categoryBadges = document.querySelectorAll('.category-badge');
        categoryBadges.forEach(badge => {
            badge.addEventListener('click', (e) => {
                e.preventDefault();
                document.querySelector('.category-badge.active')?.classList.remove('active');
                badge.classList.add('active');
            });
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
            
            const url = this.getAttribute('data-url');
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