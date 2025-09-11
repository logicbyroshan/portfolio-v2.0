document.addEventListener('DOMContentLoaded', () => {

    // Exit early if this is not the blogs page
    if (!document.body.classList.contains('blog-list-page')) {
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
    // CLICKABLE BLOG CARDS
    // =========================================================================
    document.querySelectorAll('.blog-card[data-url]').forEach(card => {
        card.addEventListener('click', (e) => {
            if (e.target.closest('a, button')) return;
            if (window.getSelection().toString()) return;
            window.location.href = card.dataset.url;
        });
    });

    // =========================================================================
    // Pagination Logic
    // =========================================================================
    const cardContainer = document.getElementById('blog-card-container');
    const pageNumbersContainer = document.getElementById('page-numbers');
    const prevPageBtn = document.getElementById('prev-page');
    const nextPageBtn = document.getElementById('next-page');

    if (cardContainer && pageNumbersContainer && prevPageBtn && nextPageBtn) {
        const cards = Array.from(cardContainer.children);
        const itemsPerPage = 6;
        const totalPages = Math.ceil(cards.length / itemsPerPage);
        let currentPage = 1;

        function displayPage(page) {
            currentPage = page;
            const startIndex = (page - 1) * itemsPerPage;
            const endIndex = startIndex + itemsPerPage;
            
            cards.forEach((card, index) => {
                card.style.display = (index >= startIndex && index < endIndex) ? 'flex' : 'none';
            });
            updatePaginationUI();
        }

        function updatePaginationUI() {
            pageNumbersContainer.innerHTML = '';
            for (let i = 1; i <= totalPages; i++) {
                const pageNumberBtn = document.createElement('button');
                pageNumberBtn.textContent = i;
                pageNumberBtn.classList.add('page-number');
                pageNumberBtn.setAttribute('aria-label', `Go to page ${i}`);
                if (i === currentPage) {
                    pageNumberBtn.classList.add('active');
                    pageNumberBtn.setAttribute('aria-current', 'page');
                }
                pageNumberBtn.addEventListener('click', () => displayPage(i));
                pageNumbersContainer.appendChild(pageNumberBtn);
            }
            prevPageBtn.disabled = currentPage === 1;
            nextPageBtn.disabled = currentPage === totalPages;
        }

        prevPageBtn.addEventListener('click', () => { if (currentPage > 1) displayPage(currentPage - 1); });
        nextPageBtn.addEventListener('click', () => { if (currentPage < totalPages) displayPage(currentPage + 1); });

        if (totalPages > 0) {
            displayPage(1);
        } else {
            document.querySelector('.pagination')?.style.setProperty('display', 'none');
        }
    }

    // =========================================================================
    // BLOG CARDS HOVER EFFECTS
    // =========================================================================
    const blogCards = document.querySelectorAll('.blog-card');
    
    blogCards.forEach(card => {
        // Add hover effects for better UX
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px)';
            this.style.transition = 'transform 0.3s ease';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
});