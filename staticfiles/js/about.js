// js/about.js
document.addEventListener('DOMContentLoaded', () => {
    // Animation system is now handled by animations.js
    // No need for duplicate animation code here

    // FAQ Accordion Functionality
    const faqCards = document.querySelectorAll('.faq-card');
    faqCards.forEach(card => {
        card.addEventListener('click', () => {
            const isActive = card.classList.contains('active');
            if (!isActive) {
                card.classList.add('active');
            } else {
                card.classList.remove('active');
            }
        });
    });

    // FAQ Show More Functionality
    const faqShowMoreBtn = document.getElementById('faq-show-more-btn');
    const faqContainer = document.getElementById('faq-container');
    const hiddenFaqs = document.querySelectorAll('.faq-hidden');
    
    if (faqShowMoreBtn && hiddenFaqs.length > 0) {
        let isShowing = false;
        
        faqShowMoreBtn.addEventListener('click', () => {
            isShowing = !isShowing;
            
            if (isShowing) {
                // Show hidden FAQs
                faqContainer.classList.add('faq-showing');
                faqShowMoreBtn.classList.add('showing');
                faqShowMoreBtn.innerHTML = '<i class="fas fa-chevron-up"></i> Show Less FAQs';
                
                // Re-initialize accordion for new FAQs
                const newFaqCards = document.querySelectorAll('.faq-hidden');
                newFaqCards.forEach(card => {
                    card.addEventListener('click', () => {
                        const isActive = card.classList.contains('active');
                        if (!isActive) {
                            card.classList.add('active');
                        } else {
                            card.classList.remove('active');
                        }
                    });
                });
            } else {
                // Hide FAQs
                faqContainer.classList.remove('faq-showing');
                faqShowMoreBtn.classList.remove('showing');
                faqShowMoreBtn.innerHTML = '<i class="fas fa-chevron-down"></i> Show More FAQs';
                
                // Close any open hidden FAQs
                hiddenFaqs.forEach(faq => {
                    faq.classList.remove('active');
                });
            }
        });
    }
});