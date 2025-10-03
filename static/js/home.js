// home.js

document.addEventListener('DOMContentLoaded', () => {

    // 1. Hero Section Typing Effect
    const skillTextElement = document.getElementById('skill-text');
    if (skillTextElement) {
        // MODIFIED: Load skills dynamically with a fallback
        let skillsToType = ["Web Developer", "AI Enthusiast", "Python Programmer", "Creative Coder"]; // Default skills if DB is empty
        
        try {
            const skillsDataElement = document.getElementById('skills-data');
            if (skillsDataElement) {
                const skillsFromDB = JSON.parse(skillsDataElement.textContent);
                // Use skills from DB only if the array is not empty
                if (skillsFromDB && skillsFromDB.length > 0) {
                    skillsToType = skillsFromDB;
                }
            }
        } catch (e) {
            console.error("Could not parse skills data from Django. Using default skills.", e);
        }
        // END OF MODIFICATION

        let skillIndex = 0;
        let charIndex = 0;
        let isDeleting = false;
        const typingSpeed = 150;
        const deletingSpeed = 100;
        const delayBetweenWords = 2000;

        function type() {
            const currentSkill = skillsToType[skillIndex];
            
            if (isDeleting) {
                skillTextElement.textContent = currentSkill.substring(0, charIndex - 1);
                charIndex--;
            } else {
                skillTextElement.textContent = currentSkill.substring(0, charIndex + 1);
                charIndex++;
            }

            if (!isDeleting && charIndex === currentSkill.length) {
                setTimeout(() => { isDeleting = true; type(); }, delayBetweenWords);
            } else if (isDeleting && charIndex === 0) {
                isDeleting = false;
                skillIndex = (skillIndex + 1) % skillsToType.length;
                setTimeout(type, 500);
            } else {
                setTimeout(type, isDeleting ? deletingSpeed : typingSpeed);
            }
        }
        setTimeout(type, 500);
    }

    // 2. FAQ Accordion Functionality
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

    // 2.1. FAQ Show More Functionality
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


    // 3. Clickable Cards (UPDATED)
    // This now targets any element with a 'data-url' attribute, making it reusable.
    const clickableElements = document.querySelectorAll('[data-url]');
    clickableElements.forEach(card => {
        const url = card.dataset.url;
        if (url && url !== '#') {
            card.addEventListener('click', (e) => {
                e.preventDefault();
                e.stopPropagation();
                window.open(url, '_blank');
            });
            card.style.cursor = 'pointer';
        }
    });

    // 4. Newsletter Form Submission Simulation
    const ctaForm = document.querySelector('.cta-form');
    if (ctaForm) {
        ctaForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const successMsg = document.querySelector('.cta-success-message');
            ctaForm.style.display = 'none';
            if(successMsg) successMsg.style.display = 'block';
        });
    }

    // Contact form is now handled by contact_form.js with toast notifications

    // Animation system is now handled by animations.js
    // No need for duplicate animation code here

    // 7. Particles.js Initialization
    if (document.getElementById('particles-js')) {
        particlesJS('particles-js', {
            "particles": {
                "number": {
                    "value": 60,
                    "density": {
                        "enable": true,
                        "value_area": 800
                    }
                },
                "color": {
                    "value": "#ffffff"
                },
                "shape": {
                    "type": "circle",
                },
                "opacity": {
                    "value": 0.5,
                    "random": true,
                    "anim": {
                        "enable": true,
                        "speed": 1,
                        "opacity_min": 0.1,
                        "sync": false
                    }
                },
                "size": {
                    "value": 2,
                    "random": true,
                    "anim": {
                        "enable": false
                    }
                },
                "line_linked": {
                    "enable": true,
                    "distance": 150,
                    "color": "#ffffff",
                    "opacity": 0.2,
                    "width": 1
                },
                "move": {
                    "enable": true,
                    "speed": 1,
                    "direction": "none",
                    "random": false,
                    "straight": false,
                    "out_mode": "out",
                    "bounce": false,
                }
            },
            "interactivity": {
                "detect_on": "canvas",
                "events": {
                    "onhover": {
                        "enable": false,
                    },
                    "onclick": {
                        "enable": false,
                    },
                    "resize": true
                }
            },
            "retina_detect": true
        });
    }

});