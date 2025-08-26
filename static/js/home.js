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


    // 3. Clickable Cards (UPDATED)
    // This now targets any element with a 'data-url' attribute, making it reusable.
    const clickableElements = document.querySelectorAll('[data-url]');
    clickableElements.forEach(card => {
        const url = card.dataset.url;
        if (url && url !== '#') {
            card.addEventListener('click', () => {
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

    // 6. On-Scroll Animation Functionality
    const animatedElements = document.querySelectorAll('[data-animation]');
    
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

    animatedElements.forEach(el => {
        observer.observe(el);
    });

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