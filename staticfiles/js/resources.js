// js/resources.js
document.addEventListener('DOMContentLoaded', () => {
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

    // Toolbar: Category Scroller Logic
    const scrollLeftBtn = document.getElementById('scroll-left');
    const scrollRightBtn = document.getElementById('scroll-right');
    const categoriesList = document.getElementById('categories-list');
    if (scrollLeftBtn && scrollRightBtn && categoriesList) {
        scrollLeftBtn.addEventListener('click', () => categoriesList.scrollBy({ left: -200, behavior: 'smooth' }));
        scrollRightBtn.addEventListener('click', () => categoriesList.scrollBy({ left: 200, behavior: 'smooth' }));
    }
});