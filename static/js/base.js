document.addEventListener('DOMContentLoaded', () => {

    // =========================================================================
    // LOGO ANIMATION FUNCTIONALITY
    // =========================================================================
    const logoContainer = document.querySelector('.nav-center-logo');
    
    if (logoContainer) {
        logoContainer.addEventListener('click', (e) => {
            e.preventDefault();
            
            // Add clicked class to trigger animation
            logoContainer.classList.add('clicked');
            
            // Remove the class after animation completes (800ms)
            setTimeout(() => {
                logoContainer.classList.remove('clicked');
            }, 800);
        });
        
        // Add hover effect to indicate interactivity
        logoContainer.style.cursor = 'pointer';
    }

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
    
    // Set theme on document with smooth transitions
    const setTheme = (theme) => {
        // Add transition class to theme toggle buttons for smooth icon rotation
        const toggleButtons = [themeToggle, mobileThemeToggle, mobileHeaderThemeToggle].filter(Boolean);
        toggleButtons.forEach(button => button?.classList.add('transitioning'));
        
        // Add dissolve transition to body
        document.body.style.transition = 'all 0.6s ease';
        
        // Set theme with a slight delay for smoother transition
        setTimeout(() => {
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
            
            // Re-initialize particles with new theme colors
            setTimeout(() => {
                initParticles();
            }, 100);
        }, 100);
        
        // Remove transition classes after animation
        setTimeout(() => {
            toggleButtons.forEach(button => button?.classList.remove('transitioning'));
        }, 400);
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
    // GLOBAL READING PROGRESS INDICATOR
    // =========================================================================
    function initReadingProgress() {
        // Only add reading progress if page has sufficient content
        const bodyHeight = document.body.scrollHeight;
        const viewportHeight = window.innerHeight;
        
        // Only show progress bar if page is longer than 1.5 viewports
        if (bodyHeight > viewportHeight * 1.5) {
            const progressBar = document.createElement('div');
            progressBar.className = 'reading-progress';
            progressBar.setAttribute('aria-label', 'Reading progress');
            progressBar.setAttribute('role', 'progressbar');
            
            document.body.appendChild(progressBar);
            
            // Show progress bar after a short delay
            setTimeout(() => {
                progressBar.classList.add('active');
            }, 500);
            
            // Update reading progress on scroll
            function updateProgress() {
                const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
                const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
                const scrolled = Math.min((winScroll / height) * 100, 100);
                
                progressBar.style.width = scrolled + '%';
                progressBar.setAttribute('aria-valuenow', Math.round(scrolled));
                progressBar.setAttribute('aria-valuemin', '0');
                progressBar.setAttribute('aria-valuemax', '100');
            }
            
            // Throttled scroll event for better performance
            let scrollTimeout;
            window.addEventListener('scroll', () => {
                if (scrollTimeout) {
                    cancelAnimationFrame(scrollTimeout);
                }
                scrollTimeout = requestAnimationFrame(updateProgress);
            }, { passive: true });
            
            // Update on resize
            window.addEventListener('resize', () => {
                const newBodyHeight = document.body.scrollHeight;
                const newViewportHeight = window.innerHeight;
                
                if (newBodyHeight <= newViewportHeight * 1.5) {
                    progressBar.style.display = 'none';
                } else {
                    progressBar.style.display = 'block';
                    updateProgress();
                }
            }, { passive: true });
            
            // Initial update
            updateProgress();
        }
    }

    // Initialize reading progress
    initReadingProgress();

    // =========================================================================
    // PARTICLES.JS INITIALIZATION (GLOBAL)
    // =========================================================================
    initParticles();
});