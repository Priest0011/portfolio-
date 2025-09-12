
// Mobile Navigation Toggle
const hamburger = document.querySelector('.hamburger');
const navLinks = document.querySelector('.nav-links');

hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('active');
    hamburger.innerHTML = navLinks.classList.contains('active') ? 
        '<i class="fas fa-times"></i>' : '<i class="fas fa-bars"></i>';
});

// Close mobile menu when clicking a link
document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('active');
        hamburger.innerHTML = '<i class="fas fa-bars"></i>';
    });
});


window.addEventListener('scroll', () => {
    const header = document.querySelector('header');
    if (window.scrollY > 100) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            window.scrollTo({
                top: target.offsetTop - 80,
                behavior: 'smooth'
            });
        }
    });
});

// Portfolio filtering
const filterBtns = document.querySelectorAll('.filter-btn');
const portfolioItems = document.querySelectorAll('.portfolio-item');

filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        // Remove active class from all buttons
        filterBtns.forEach(b => b.classList.remove('active'));
        // Add active class to clicked button
        btn.classList.add('active');
        
        const filter = btn.getAttribute('data-filter');
        
        portfolioItems.forEach(item => {
            if (filter === 'all' || item.getAttribute('data-category') === filter) {
                item.style.display = 'block';
            } else {
                item.style.display = 'none';
            }
        });
    });
});



// Auto-typing effect
const typed = new Typed('.typed-text', {
    strings: ['Web Developer',  'Creative Coder','Full Stack Developer','DataBase Administrator','Backend Specialist', ],
    typeSpeed: 50,
    backSpeed: 50,
    loop: true,
    showCursor: true,
    cursorChar: '|',
    smartBackspace: true
});

// Scroll animations
const animateOnScroll = () => {
    const elements = document.querySelectorAll('.service-card, .portfolio-item, .blog-card, .about-image, .about-text');
    
    elements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150;
        
        if (elementTop < window.innerHeight - elementVisible) {
            element.style.opacity = "1";
            element.style.transform = "translateY(0)";
        }
    });
};

// Set initial state for animated elements
document.querySelectorAll('.service-card, .portfolio-item, .blog-card, .about-image, .about-text').forEach(el => {
    el.style.opacity = "0";
    el.style.transform = "translateY(30px)";
    el.style.transition = "opacity 0.6s ease, transform 0.6s ease";
});

// Listen for scroll events
window.addEventListener('scroll', animateOnScroll);

// Trigger once on load
window.addEventListener('load', animateOnScroll);




const music = document.getElementById('bg-music');
let started = false;

function playMusic() {
    if (!started) {
    music.play()
        .then(() => {
        console.log("Music playing");
        localStorage.setItem('musicStarted', 'true');  // Save state
        })
        .catch(err => {
        console.warn("Play failed:", err);
        });
    started = true;
    }
}

// Check if music started before
if (localStorage.getItem('musicStarted') === 'true') {
    // Try autoplay without interaction (might work on some browsers)
    playMusic();
} else {
    // Trigger on interaction
    window.addEventListener("click", playMusic);
    window.addEventListener("scroll", playMusic);
    window.addEventListener("keydown", playMusic);
}
