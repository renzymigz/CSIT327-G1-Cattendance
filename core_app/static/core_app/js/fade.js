document.addEventListener('DOMContentLoaded', function () {
    const items = Array.from(document.querySelectorAll('.fade-item'));

    const observerOptions = {
        root: null, // 
        rootMargin: '0px',
        threshold: 0.3, 
    };

    const fadeInOnScroll = (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const visibleItems = items.filter(el => el.getBoundingClientRect().top < window.innerHeight);
                
                visibleItems.forEach((el, i) => {
                    el.style.animationDelay = `${i * 0.15}s`; // stagger delay
                    el.classList.add('fade-in');
                    observer.unobserve(el);
                });
            }
        });
    };

    const observer = new IntersectionObserver(fadeInOnScroll, observerOptions);

    items.forEach(el => observer.observe(el));
});