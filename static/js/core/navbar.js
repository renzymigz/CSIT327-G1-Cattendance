/**
    JS FOR THE RESPONSIVE STUFF (thx jeepeetee </3)
 */


// JavaScript for changing navbar background on scroll
document.addEventListener('DOMContentLoaded', function() {
    console.log("JS loaded");
    const navbar = document.getElementById('navbar');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 0) {
            navbar.classList.remove('bg-transparent');
            navbar.classList.add('bg-white');
        } else {
            navbar.classList.remove('bg-white');
            navbar.classList.add('bg-transparent');
        }
    });
    
    // Mobile menu functionality
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const menuIcon = document.getElementById('menu-icon');
    
    if (mobileMenuBtn && mobileMenu) {
        // Toggle mobile menu on button click
        mobileMenuBtn.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
            mobileMenu.classList.toggle('show');
            
            // Toggle hamburger/close icon
            if (mobileMenu.classList.contains('hidden')) {
                menuIcon.className = 'fas fa-bars text-xl';
            } else {
                menuIcon.className = 'fas fa-times text-xl';
            }
        });
        
        // Close mobile menu when clicking on navigation links
        const mobileLinks = document.querySelectorAll('.mobile-link');
        mobileLinks.forEach(link => {
            link.addEventListener('click', function() {
                mobileMenu.classList.add('hidden');
                mobileMenu.classList.remove('show');
                menuIcon.className = 'fas fa-bars text-xl';
            });
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!mobileMenuBtn.contains(e.target) && !mobileMenu.contains(e.target)) {
                mobileMenu.classList.add('hidden');
                mobileMenu.classList.remove('show');
                menuIcon.className = 'fas fa-bars text-xl';
            }
        });
    }
    
    // Smooth scrolling functionality for anchor links
    const smoothScrollLinks = document.querySelectorAll('.smooth-scroll');
    
    smoothScrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                // Calculate offset to account for fixed navbar height
                const navbarHeight = document.querySelector('nav').offsetHeight;
                const targetPosition = targetSection.offsetTop - navbarHeight - 20; // 20px extra padding
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
});

