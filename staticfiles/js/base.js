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
    const openResumeBtn = document.getElementById('open-resume-modal');
    const closeResumeBtn = document.getElementById('close-resume-modal');
    const mobileResumeBtn = document.getElementById('mobile-open-resume-modal');

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
    const openVideoBtn = document.getElementById('open-video-modal');
    const closeVideoBtn = document.getElementById('close-video-modal');
    const videoIframe = document.getElementById('resume-video-iframe');
    const mobileVideoResumeBtn = document.getElementById('mobile-open-video-modal');

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
    // THEME TOGGLE FUNCTIONALITY
    // =========================================================================
    const themeToggle = document.getElementById('theme-toggle');
    const mobileThemeToggle = document.getElementById('mobile-theme-toggle');
    const mobileHeaderThemeToggle = document.getElementById('mobile-header-theme-toggle');
    const themeIcon = document.getElementById('theme-icon');
    const mobileThemeIcon = document.getElementById('mobile-theme-icon');
    const mobileHeaderThemeIcon = document.getElementById('mobile-header-theme-icon');

    // Get current theme from localStorage or default to dark
    const getCurrentTheme = () => localStorage.getItem('theme') || 'dark';
    
    // Set theme on document
    const setTheme = (theme) => {
        if (theme === 'light') {
            document.documentElement.setAttribute('data-theme', 'light');
            if (themeIcon) themeIcon.className = 'fas fa-moon';
            if (mobileThemeIcon) mobileThemeIcon.className = 'fas fa-moon';
            if (mobileHeaderThemeIcon) mobileHeaderThemeIcon.className = 'fas fa-moon';
        } else {
            document.documentElement.removeAttribute('data-theme');
            if (themeIcon) themeIcon.className = 'fas fa-sun';
            if (mobileThemeIcon) mobileThemeIcon.className = 'fas fa-sun';
            if (mobileHeaderThemeIcon) mobileHeaderThemeIcon.className = 'fas fa-sun';
        }
        localStorage.setItem('theme', theme);
    };

    // Initialize particles function
    const initParticles = () => {
        if (document.getElementById('particles-js')) {
            const isDarkTheme = getCurrentTheme() === 'dark';
            const particleColor = isDarkTheme ? "#ffffff" : "#475569";
            const particleOpacity = isDarkTheme ? 0.5 : 0.3;
            const lineOpacity = isDarkTheme ? 0.2 : 0.15;

            particlesJS('particles-js', {
                "particles": { 
                    "number": { "value": 60, "density": { "enable": true, "value_area": 800 } }, 
                    "color": { "value": particleColor }, 
                    "shape": { "type": "circle", }, 
                    "opacity": { "value": particleOpacity, "random": true, "anim": { "enable": true, "speed": 1, "opacity_min": 0.1, "sync": false } }, 
                    "size": { "value": 2, "random": true, "anim": { "enable": false } }, 
                    "line_linked": { "enable": true, "distance": 150, "color": particleColor, "opacity": lineOpacity, "width": 1 }, 
                    "move": { "enable": true, "speed": 1, "direction": "none", "random": false, "straight": false, "out_mode": "out", "bounce": false, } 
                }, 
                "interactivity": { "detect_on": "canvas", "events": { "onhover": { "enable": false, }, "onclick": { "enable": false, }, "resize": true } }, 
                "retina_detect": true
            });
        }
    };

    // Initialize theme on page load
    const currentTheme = getCurrentTheme();
    setTheme(currentTheme);

    // Theme toggle functionality
    const toggleTheme = () => {
        const currentTheme = getCurrentTheme();
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        setTheme(newTheme);
        // Reinitialize particles with new theme
        setTimeout(initParticles, 100);
    };

    // Add event listeners
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }

    if (mobileThemeToggle) {
        mobileThemeToggle.addEventListener('click', () => {
            toggleTheme();
            // Close mobile menu if open
            siteHeader.classList.remove('mobile-menu-active');
        });
    }

    if (mobileHeaderThemeToggle) {
        mobileHeaderThemeToggle.addEventListener('click', toggleTheme);
    }


    // =========================================================================
    // PARTICLES.JS INITIALIZATION (GLOBAL)
    // =========================================================================
    initParticles();
});