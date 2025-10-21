// Main JavaScript file for IKR Plantations Project

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('IKR Plantations Project loaded successfully');

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Form validation
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Basic validation - can be extended
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });

            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
    });

    // Image lazy loading
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                observer.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));

    // Search functionality
    const searchInput = document.querySelector('#search-input');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            const listings = document.querySelectorAll('.listing-card');

            listings.forEach(listing => {
                const title = listing.querySelector('h3').textContent.toLowerCase();
                const description = listing.querySelector('p').textContent.toLowerCase();

                if (title.includes(query) || description.includes(query)) {
                    listing.style.display = 'block';
                } else {
                    listing.style.display = 'none';
                }
            });
        });
    }

    // Modal functionality
    const modals = document.querySelectorAll('.modal');
    const modalTriggers = document.querySelectorAll('[data-toggle="modal"]');

    modalTriggers.forEach(trigger => {
        trigger.addEventListener('click', function() {
            const modalId = this.getAttribute('data-target');
            const modal = document.querySelector(modalId);
            if (modal) {
                modal.style.display = 'block';
            }
        });
    });

    // Close modals
    modals.forEach(modal => {
        const closeBtn = modal.querySelector('.close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                modal.style.display = 'none';
            });
        }

        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                modal.style.display = 'none';
            }
        });
    });
});
