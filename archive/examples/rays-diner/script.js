// Ray's Diner Website JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scrolling for navigation links
    const navLinks = document.querySelectorAll('.nav-menu a[href^="#"]');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const headerHeight = document.querySelector('.header').offsetHeight;
                const targetPosition = targetSection.offsetTop - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Header background change on scroll
    const header = document.querySelector('.header');
    
    window.addEventListener('scroll', function() {
        if (window.scrollY > 100) {
            header.style.background = 'rgba(139, 69, 19, 0.95)';
            header.style.backdropFilter = 'blur(10px)';
        } else {
            header.style.background = 'linear-gradient(135deg, #8B4513 0%, #A0522D 100%)';
            header.style.backdropFilter = 'none';
        }
    });

    // Menu item hover effects
    const menuItems = document.querySelectorAll('.menu-item');
    
    menuItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(10px) scale(1.02)';
        });
        
        item.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(5px) scale(1)';
        });
    });

    // Info card animation on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe info cards and menu categories
    const animatedElements = document.querySelectorAll('.info-card, .menu-category, .highlight');
    
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(el);
    });

    // Phone number formatting and click tracking
    const phoneLinks = document.querySelectorAll('a[href^="tel:"]');
    
    phoneLinks.forEach(link => {
        link.addEventListener('click', function() {
            // Track phone clicks for analytics (if needed)
            console.log('Phone number clicked:', this.href);
        });
    });

    // Featured menu item spotlight effect
    const featuredItems = document.querySelectorAll('.menu-item.featured');
    
    setInterval(() => {
        featuredItems.forEach(item => {
            item.style.boxShadow = '0 0 20px rgba(255, 215, 0, 0.3)';
            setTimeout(() => {
                item.style.boxShadow = '0 5px 15px rgba(0,0,0,0.1)';
            }, 1000);
        });
    }, 5000);

    // Hours indicator (show if open/closed)
    function updateHoursStatus() {
        const now = new Date();
        const day = now.getDay(); // 0 = Sunday, 1 = Monday, etc.
        const hour = now.getHours();
        
        // Ray's Diner: Tuesday(2) - Sunday(0), 8 AM - 3 PM, Closed Monday(1)
        const isOpen = (day !== 1) && (hour >= 8 && hour < 15);
        
        const hoursCards = document.querySelectorAll('.info-card');
        const hoursCard = Array.from(hoursCards).find(card => 
            card.querySelector('h3').textContent.includes('Hours')
        );
        
        if (hoursCard) {
            const statusIndicator = document.createElement('div');
            statusIndicator.style.cssText = `
                padding: 0.5rem;
                border-radius: 5px;
                margin-top: 1rem;
                text-align: center;
                font-weight: bold;
            `;
            
            if (isOpen) {
                statusIndicator.textContent = '🟢 OPEN NOW';
                statusIndicator.style.background = '#d4edda';
                statusIndicator.style.color = '#155724';
            } else {
                statusIndicator.textContent = '🔴 CLOSED';
                statusIndicator.style.background = '#f8d7da';
                statusIndicator.style.color = '#721c24';
            }
            
            // Remove existing status indicator if present
            const existingIndicator = hoursCard.querySelector('.status-indicator');
            if (existingIndicator) {
                existingIndicator.remove();
            }
            
            statusIndicator.className = 'status-indicator';
            hoursCard.appendChild(statusIndicator);
        }
    }
    
    // Update hours status immediately and every minute
    updateHoursStatus();
    setInterval(updateHoursStatus, 60000);

    // Mobile menu toggle (if needed for smaller screens)
    function createMobileMenu() {
        if (window.innerWidth <= 768) {
            const nav = document.querySelector('.nav');
            const navMenu = document.querySelector('.nav-menu');
            
            if (!document.querySelector('.mobile-menu-toggle')) {
                const toggleButton = document.createElement('button');
                toggleButton.className = 'mobile-menu-toggle';
                toggleButton.innerHTML = '☰';
                toggleButton.style.cssText = `
                    background: none;
                    border: none;
                    color: white;
                    font-size: 1.5rem;
                    cursor: pointer;
                    display: none;
                `;
                
                if (window.innerWidth <= 768) {
                    toggleButton.style.display = 'block';
                    navMenu.style.display = 'none';
                }
                
                toggleButton.addEventListener('click', () => {
                    const isVisible = navMenu.style.display !== 'none';
                    navMenu.style.display = isVisible ? 'none' : 'flex';
                    navMenu.style.flexDirection = 'column';
                    navMenu.style.position = 'absolute';
                    navMenu.style.top = '100%';
                    navMenu.style.left = '0';
                    navMenu.style.right = '0';
                    navMenu.style.background = '#8B4513';
                    navMenu.style.padding = '1rem';
                });
                
                nav.appendChild(toggleButton);
            }
        }
    }
    
    createMobileMenu();
    window.addEventListener('resize', createMobileMenu);
});

// Contact form handler (if contact form is added later)
function handleContactForm(event) {
    event.preventDefault();
    
    // Get form data
    const formData = new FormData(event.target);
    const name = formData.get('name');
    const email = formData.get('email');
    const message = formData.get('message');
    
    // Simple validation
    if (!name || !email || !message) {
        alert('Please fill in all fields.');
        return;
    }
    
    // Here you would typically send the data to a server
    console.log('Contact form submitted:', { name, email, message });
    alert('Thank you for your message! We\'ll get back to you soon.');
    
    // Reset form
    event.target.reset();
}

// Utility function to format phone numbers
function formatPhoneNumber(phoneNumber) {
    const cleaned = phoneNumber.replace(/\D/g, '');
    const match = cleaned.match(/^(\d{3})(\d{3})(\d{4})$/);
    
    if (match) {
        return '(' + match[1] + ') ' + match[2] + '-' + match[3];
    }
    
    return phoneNumber;
}

// Add some Easter eggs for fun
let clickCount = 0;
document.addEventListener('click', function(e) {
    if (e.target.textContent && e.target.textContent.includes('Ray\'s Diner')) {
        clickCount++;
        if (clickCount === 5) {
            alert('🍽️ Thanks for loving Ray\'s Diner! Come visit us for the real experience!');
            clickCount = 0;
        }
    }
});