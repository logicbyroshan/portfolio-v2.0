// animations.js - Unified Animation System for Portfolio
// This file provides a consistent animation system across all pages

class AnimationController {
    constructor() {
        this.observers = new Map();
        this.initialized = false;
        this.init();
    }

    init() {
        if (this.initialized) return;
        
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setupAnimations());
        } else {
            this.setupAnimations();
        }
        
        this.initialized = true;
    }

    setupAnimations() {
        // Find all elements with animation attributes
        const animatedElements = document.querySelectorAll('[data-animation]');
        
        if (animatedElements.length === 0) return;

        // Create intersection observer with improved settings
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.triggerAnimation(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.05, // Lower threshold for better triggering
            rootMargin: '50px 0px -50px 0px' // Start animation before element is fully visible
        });

        // Observe all animated elements
        animatedElements.forEach(element => {
            observer.observe(element);
        });

        // Store observer for cleanup if needed
        this.observers.set('main', observer);
    }

    triggerAnimation(element) {
        const delay = parseInt(element.dataset.animationDelay) || 0;
        
        // Apply animation with delay
        setTimeout(() => {
            element.classList.add('is-visible');
            
            // Dispatch custom event for additional handling
            element.dispatchEvent(new CustomEvent('animationTriggered', {
                bubbles: true,
                detail: { element, animationType: element.dataset.animation }
            }));
        }, delay);
    }

    // Method to manually trigger animations (useful for dynamic content)
    triggerAnimationForElement(element) {
        if (element && element.hasAttribute('data-animation')) {
            this.triggerAnimation(element);
        }
    }

    // Method to reset animations (useful for SPAs or dynamic content)
    resetAnimations(container = document) {
        const animatedElements = container.querySelectorAll('[data-animation].is-visible');
        animatedElements.forEach(element => {
            element.classList.remove('is-visible');
        });
    }

    // Cleanup method
    destroy() {
        this.observers.forEach(observer => observer.disconnect());
        this.observers.clear();
        this.initialized = false;
    }
}

// Create global animation controller instance
window.AnimationController = new AnimationController();

// Expose methods for external use
window.triggerAnimation = (element) => window.AnimationController.triggerAnimationForElement(element);
window.resetAnimations = (container) => window.AnimationController.resetAnimations(container);

// Handle page visibility changes to restart animations if needed
document.addEventListener('visibilitychange', () => {
    if (!document.hidden) {
        // Restart animations when page becomes visible again
        setTimeout(() => {
            window.AnimationController.setupAnimations();
        }, 100);
    }
});

// Handle window resize to recalculate intersection observer
let resizeTimeout;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
        // Recreate observers after resize
        window.AnimationController.destroy();
        window.AnimationController = new AnimationController();
    }, 250);
});