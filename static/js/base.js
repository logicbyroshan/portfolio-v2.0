document.addEventListener('DOMContentLoaded', () => {

    // =========================================================================
    // MOBILE NAVIGATION TOGGLE
    // =========================================================================
    const mobileNavToggle = document.getElementById('mobile-nav-toggle');
    const siteHeader = document.querySelector('.site-header');

    if (mobileNavToggle && siteHeader) {
        mobileNavToggle.addEventListener('click', () => {
            console.log('Mobile toggle clicked'); // Debug log
            siteHeader.classList.toggle('mobile-menu-active');
            console.log('Header classes:', siteHeader.className); // Debug log
        });
    } else {
        console.log('Mobile nav elements not found:', { mobileNavToggle, siteHeader }); // Debug log
    }

    // =========================================================================
    // RESUME MODAL LOGIC
    // =========================================================================
    const resumeModal = document.getElementById('resume-modal');
    const openResumeBtn = document.getElementById('resume-nav-btn');
    const closeResumeBtn = document.getElementById('close-resume-modal');
    const mobileResumeBtn = document.getElementById('mobile-resume-btn');

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

        if (mobileResumeBtn) {
            mobileResumeBtn.addEventListener('click', (e) => {
                e.preventDefault();
                openModal();
                siteHeader.classList.remove('mobile-menu-active'); // Close mobile menu
            });
        }

        closeResumeBtn.addEventListener('click', closeModal);

        // Close modal when clicking on the background overlay
        resumeModal.addEventListener('click', (e) => {
            if (e.target === resumeModal) {
                closeModal();
            }
        });
    }

    // =========================================================================
    // VIDEO RESUME MODAL LOGIC
    // =========================================================================
    const videoModal = document.getElementById('video-modal');
    const openVideoBtn = document.getElementById('video-resume-nav-btn');
    const closeVideoBtn = document.getElementById('close-video-modal');
    const videoIframe = document.getElementById('resume-video-iframe');
    const mobileVideoResumeBtn = document.getElementById('mobile-video-resume-btn');

    if (videoModal && openVideoBtn && closeVideoBtn) {
        const originalVideoSrc = videoIframe ? videoIframe.src : null;

        const openVideoModal = () => {
            videoModal.classList.add('active');
            document.body.style.overflow = 'hidden';
        };

        const closeVideoModal = () => {
            videoModal.classList.remove('active');
            document.body.style.overflow = 'auto';
            // Reset the iframe src to stop the video from playing in the background
            if (videoIframe && originalVideoSrc) {
                videoIframe.src = originalVideoSrc;
            }
        };

        openVideoBtn.addEventListener('click', (e) => {
            e.preventDefault();
            openVideoModal();
        });

        if (mobileVideoResumeBtn) {
            mobileVideoResumeBtn.addEventListener('click', (e) => {
                e.preventDefault();
                openVideoModal();
                siteHeader.classList.remove('mobile-menu-active'); // Close mobile menu
            });
        }

        closeVideoBtn.addEventListener('click', closeVideoModal);

        videoModal.addEventListener('click', (e) => {
            if (e.target === videoModal) {
                closeVideoModal();
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