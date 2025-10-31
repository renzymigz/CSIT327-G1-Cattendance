document.addEventListener('DOMContentLoaded', function () {
    const items = Array.from(document.querySelectorAll('.fade-item'));

    const observerOptions = {
        root: null, // observe relative to the viewport
        rootMargin: '0px', // no margin offset
        threshold: 0.5 // trigger fade-in when 50% of the element is in view
    };

    const fadeInOnScroll = (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Add fade-in class when element is in view
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target); // Stop observing once it's in view
            }
        });
    };

    const observer = new IntersectionObserver(fadeInOnScroll, observerOptions);

    // Start observing each fade-item element
    items.forEach(function (el) {
        observer.observe(el);
    });
});
