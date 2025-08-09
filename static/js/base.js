document.addEventListener('DOMContentLoaded', () => {

    // =========================================================================
    // MOBILE NAVIGATION TOGGLE
    // =========================================================================
    const mobileNavToggle = document.getElementById('mobile-nav-toggle');
    const siteHeader = document.querySelector('.site-header');

    if (mobileNavToggle && siteHeader) {
        mobileNavToggle.addEventListener('click', () => {
            siteHeader.classList.toggle('mobile-menu-active');
        });
    }

    // =========================================================================
    // RESUME MODAL LOGIC
    // =========================================================================
    const resumeModal = document.getElementById('resume-modal');
    const openResumeBtn = document.getElementById('resume-nav-btn');
    const closeResumeBtn = document.getElementById('close-resume-modal');

    if (resumeModal && openResumeBtn && closeResumeBtn) {
        const openModal = () => {
            resumeModal.classList.add('active');
            document.body.style.overflow = 'hidden';
        };

        const closeModal = () => {
            resumeModal.classList.remove('active');
            document.body.style.overflow = 'auto';
        };

        openResumeBtn.addEventListener('click', (e) => {
            e.preventDefault();
            openModal();
        });

        closeResumeBtn.addEventListener('click', closeModal);

        // Close modal when clicking on the background overlay
        resumeModal.addEventListener('click', (e) => {
            if (e.target === resumeModal) {
                closeModal();
            }
        });
    }

    // =========================================================================
    // PARTICLES.JS INITIALIZATION (GLOBAL)
    // =========================================================================
    if (document.getElementById('particles-js')) {
        particlesJS('particles-js', {
            "particles": { "number": { "value": 60, "density": { "enable": true, "value_area": 800 } }, "color": { "value": "#ffffff" }, "shape": { "type": "circle", }, "opacity": { "value": 0.5, "random": true, "anim": { "enable": true, "speed": 1, "opacity_min": 0.1, "sync": false } }, "size": { "value": 2, "random": true, "anim": { "enable": false } }, "line_linked": { "enable": true, "distance": 150, "color": "#ffffff", "opacity": 0.2, "width": 1 }, "move": { "enable": true, "speed": 1, "direction": "none", "random": false, "straight": false, "out_mode": "out", "bounce": false, } }, "interactivity": { "detect_on": "canvas", "events": { "onhover": { "enable": false, }, "onclick": { "enable": false, }, "resize": true } }, "retina_detect": true
        });
    }
});