document.addEventListener('DOMContentLoaded', () => {

    // Exit early if this is not the project detail page
    if (!document.body.classList.contains('project-detail-page')) {
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
    // IMAGE SLIDER LOGIC
    // =========================================================================
    const sliderContainer = document.getElementById('project-slider');
    
    // Only run the slider script if the slider element exists
    if (sliderContainer) {
        const slider = sliderContainer.querySelector('.slider-wrapper');
        const prevBtn = sliderContainer.querySelector('#prev-slide');
        const nextBtn = sliderContainer.querySelector('#next-slide');
        const slides = Array.from(sliderContainer.querySelectorAll('.slide'));
        
        let currentIndex = 0;
        const totalSlides = slides.length;

        function goToSlide(index) {
            // Clamp the index to be within bounds
            if (index < 0) {
                index = totalSlides - 1;
            } else if (index >= totalSlides) {
                index = 0;
            }
            
            currentIndex = index;
            
            // Move the slider wrapper
            slider.style.transform = `translateX(-${currentIndex * 100}%)`;
        }

        nextBtn.addEventListener('click', () => {
            goToSlide(currentIndex + 1);
        });

        prevBtn.addEventListener('click', () => {
            goToSlide(currentIndex - 1);
        });

        // Initialize slider position
        goToSlide(0);
    }
});