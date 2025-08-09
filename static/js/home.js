// home.js

document.addEventListener('DOMContentLoaded', () => {

    // 1. Hero Section Typing Effect
    const skillTextElement = document.getElementById('skill-text');
    if (skillTextElement) {
        const skillsToType = ["Web Developer", "AI Enthusiast", "Python Programmer", "Creative Coder"];
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
            faqCards.forEach(otherCard => {
                otherCard.classList.remove('active');
            });
            if (!isActive) {
                card.classList.add('active');
            }
        });
    });

    // 3. Video Resume Modal Functionality
    const videoResumeBtn = document.getElementById('video-resume-btn');
    const videoModal = document.getElementById('video-modal');
    
    if (videoResumeBtn && videoModal) {
        const closeModalBtn = document.getElementById('close-modal-btn');
        const videoIframe = document.getElementById('resume-video-iframe');
        const originalVideoSrc = videoIframe ? videoIframe.src : "";

        const openModal = () => {
            videoModal.style.display = 'flex';
            setTimeout(() => videoModal.classList.add('active'), 10);
            document.body.style.overflow = 'hidden';
        };

        const closeModal = () => {
            videoModal.classList.remove('active');
            setTimeout(() => {
                videoModal.style.display = 'none';
                document.body.style.overflow = 'auto';
                if(videoIframe) {
                    videoIframe.src = originalVideoSrc;
                }
            }, 300);
        };

        videoResumeBtn.addEventListener('click', (e) => {
            e.preventDefault();
            openModal();
        });

        if(closeModalBtn) closeModalBtn.addEventListener('click', closeModal);

        videoModal.addEventListener('click', (e) => {
            if (e.target === videoModal) {
                closeModal();
            }
        });
    }

    // 4. Clickable Cards (UPDATED)
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

    // 5. Newsletter Form Submission Simulation
    const ctaForm = document.querySelector('.cta-form');
    if (ctaForm) {
        ctaForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const successMsg = document.querySelector('.cta-success-message');
            ctaForm.style.display = 'none';
            if(successMsg) successMsg.style.display = 'block';
        });
    }

    // 6. Contact Form Submission Simulation
    const contactForm = document.querySelector('.right-contact-form form');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();
            alert("Thank you for your message! I'll get back to you soon.");
            contactForm.reset();
        });
    }

    // 7. On-Scroll Animation Functionality
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

    // 8. Particles.js Initialization
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