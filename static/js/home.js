// home.js
document.addEventListener('DOMContentLoaded', () => {

    // Typing effect removed - now using static text


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