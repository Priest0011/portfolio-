// ===== PARTICLE NETWORK =====
const canvas = document.getElementById('particles-canvas');
const ctx = canvas.getContext('2d');
let particles = [];
let animationId;

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

class Particle {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.vx = (Math.random() - 0.5) * 0.5;
        this.vy = (Math.random() - 0.5) * 0.5;
        this.size = Math.random() * 2 + 1;
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;

        if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
        if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
    }

    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(255, 51, 102, 0.5)';
        ctx.fill();
    }
}

function initParticles() {
    particles = [];
    const count = Math.min(Math.floor(window.innerWidth / 10), 100);
    for (let i = 0; i < count; i++) {
        particles.push(new Particle());
    }
}
initParticles();

function animateParticles() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    particles.forEach((p, i) => {
        p.update();
        p.draw();

        for (let j = i + 1; j < particles.length; j++) {
            const dx = particles[j].x - p.x;
            const dy = particles[j].y - p.y;
            const dist = Math.sqrt(dx * dx + dy * dy);

            if (dist < 150) {
                ctx.beginPath();
                ctx.moveTo(p.x, p.y);
                ctx.lineTo(particles[j].x, particles[j].y);
                ctx.strokeStyle = `rgba(255, 51, 102, ${0.2 * (1 - dist / 150)})`;
                ctx.lineWidth = 0.5;
                ctx.stroke();
            }
        }
    });

    animationId = requestAnimationFrame(animateParticles);
}
animateParticles();

// ===== CUSTOM CURSOR =====
const cursor = document.querySelector('.cursor');
const cursorTrail = document.querySelector('.cursor-trail');
let mouseX = 0, mouseY = 0;
let trailX = 0, trailY = 0;

document.addEventListener('mousemove', (e) => {
    mouseX = e.clientX;
    mouseY = e.clientY;
    cursor.style.left = mouseX - 6 + 'px';
    cursor.style.top = mouseY - 6 + 'px';
});

function animateCursor() {
    trailX += (mouseX - trailX) * 0.15;
    trailY += (mouseY - trailY) * 0.15;
    cursorTrail.style.left = trailX - 20 + 'px';
    cursorTrail.style.top = trailY - 20 + 'px';
    requestAnimationFrame(animateCursor);
}
animateCursor();

document.querySelectorAll('a, button, .portfolio-item, .service-card, .blog-card, input, textarea').forEach(el => {
    el.addEventListener('mouseenter', () => cursor.classList.add('hover'));
    el.addEventListener('mouseleave', () => cursor.classList.remove('hover'));
});

// ===== SCROLL PROGRESS =====
const scrollProgress = document.querySelector('.scroll-progress');
window.addEventListener('scroll', () => {
    const scrollTop = window.scrollY;
    const docHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = (scrollTop / docHeight) * 100;
    scrollProgress.style.width = progress + '%';
});

// ===== NAVBAR SCROLL =====
const navbar = document.getElementById('navbar');
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// ===== MOBILE MENU =====
const hamburger = document.getElementById('hamburger');
const navLinks = document.getElementById('navLinks');
hamburger.addEventListener('click', () => {
    navLinks.classList.toggle('active');
});

document.querySelectorAll('.nav-links a').forEach(link => {
    link.addEventListener('click', () => {
        navLinks.classList.remove('active');
    });
});

// =====================================================
// PART A — REPLACE your whole "TEXT SCRAMBLE EFFECT" block
// (from `class TextScramble` down to the closing } of `if (scrambleEl)`)
// =====================================================

// ===== TEXT SCRAMBLE EFFECT =====
class TextScramble {
    constructor(el) {
        this.el = el;
        // No < or > here: they were being injected as raw HTML and could break the markup
        this.chars = '!-_\\/[]{}=+*^?#_';
        this.update = this.update.bind(this);
        this.current = el.textContent;
    }

    setText(newText) {
        const oldText = this.current;
        const length = Math.max(oldText.length, newText.length);
        const promise = new Promise((resolve) => (this.resolve = resolve));
        this.queue = [];
        for (let i = 0; i < length; i++) {
            const from = oldText[i] || '';
            const to = newText[i] || '';
            const start = Math.floor(Math.random() * 25);
            const end = start + Math.floor(Math.random() * 25);
            this.queue.push({ from, to, start, end });
        }
        this.current = newText;
        cancelAnimationFrame(this.frameRequest);
        this.frame = 0;
        this.update();
        return promise;
    }

    update() {
        let output = '';
        let complete = 0;
        for (let i = 0, n = this.queue.length; i < n; i++) {
            let { from, to, start, end, char } = this.queue[i];
            if (this.frame >= end) {
                complete++;
                output += to;
            } else if (this.frame >= start) {
                if (!char || Math.random() < 0.28) {
                    char = this.randomChar();
                    this.queue[i].char = char;
                }
                output += `<span class="scramble-char">${char}</span>`;
            } else {
                output += from;
            }
        }
        this.el.innerHTML = output;
        if (complete === this.queue.length) {
            this.resolve();
        } else {
            this.frameRequest = requestAnimationFrame(this.update);
            this.frame++;
        }
    }

    randomChar() {
        return this.chars[Math.floor(Math.random() * this.chars.length)];
    }
}

const scrambleEl = document.getElementById('scramble-text');
if (scrambleEl) {
    const phrases = ['Developer', 'Designer', 'Problem Solver', 'Django Expert', 'Creator'];
    scrambleEl.setAttribute('aria-label', 'Developer, Designer, Problem Solver, Django Expert, Creator');
    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    if (!reduceMotion) {
        const fx = new TextScramble(scrambleEl);
        let counter = 1; // "Developer" is already on screen, so start with the next one
        const nextPhrase = () => {
            // Pause while the tab is hidden so it doesn't pile up animations
            if (document.hidden) return setTimeout(nextPhrase, 1000);
            fx.setText(phrases[counter]).then(() => setTimeout(nextPhrase, 2500));
            counter = (counter + 1) % phrases.length;
        };
        setTimeout(nextPhrase, 2500);
    }
}


// =====================================================
// PART B — ADD THIS ANYWHERE BELOW "PORTFOLIO FILTER"
// (e.g. right before "3D TILT EFFECT"). Keep the filter code as it is.
// =====================================================

// ===== PROJECT DETAILS MODAL =====
const projectModal = document.getElementById('projectModal');
if (projectModal) {
    const mImage = document.getElementById('modalImage');
    const mMedia = document.getElementById('modalMedia');
    const mCategory = document.getElementById('modalCategory');
    const mTitle = document.getElementById('modalTitle');
    const mDesc = document.getElementById('modalDesc');
    const mTech = document.getElementById('modalTech');
    const mTechWrap = document.getElementById('modalTechWrap');
    const mLink = document.getElementById('modalLink');
    let lastFocused = null;

    function openProject(card) {
        lastFocused = document.activeElement;
        const { title, image, url, tech, category } = card.dataset;

        mTitle.textContent = title;
        mCategory.textContent = category;
        mDesc.innerHTML = card.querySelector('.project-extra').innerHTML;

        if (image) {
            mImage.src = image;
            mImage.alt = title;
            mMedia.hidden = false;
        } else {
            mMedia.hidden = true;
        }

        mTech.innerHTML = '';
        const techs = (tech || '').split(',').map(t => t.trim()).filter(Boolean);
        techs.forEach(t => {
            const li = document.createElement('li');
            li.textContent = t;
            mTech.appendChild(li);
        });
        mTechWrap.hidden = techs.length === 0;

        // The live link only appears here, after the details
        if (url) {
            mLink.href = url;
            mLink.style.display = '';
        } else {
            mLink.style.display = 'none';
        }

        projectModal.classList.add('open');
        projectModal.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';
        projectModal.querySelector('.modal-close').focus();
    }

    function closeProject() {
        projectModal.classList.remove('open');
        projectModal.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
        if (lastFocused) lastFocused.focus();
    }

    document.querySelectorAll('.project-card').forEach(card => {
        card.addEventListener('click', () => openProject(card));
        card.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                openProject(card);
            }
        });
    });

    projectModal.querySelectorAll('[data-close]').forEach(el => {
        el.addEventListener('click', closeProject);
    });

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && projectModal.classList.contains('open')) closeProject();
    });
}

// ===== SCROLL REVEAL =====
const revealElements = document.querySelectorAll('.reveal');
const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('active');
        }
    });
}, { threshold: 0.1 });

revealElements.forEach(el => revealObserver.observe(el));

// ===== COUNTER ANIMATION =====
const statNumbers = document.querySelectorAll('.stat-number');
const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const target = parseInt(entry.target.dataset.target);
            let current = 0;
            const increment = target / 50;
            const timer = setInterval(() => {
                current += increment;
                if (current >= target) {
                    entry.target.textContent = target + (target === 99 ? '%' : '+');
                    clearInterval(timer);
                } else {
                    entry.target.textContent = Math.floor(current) + (target === 99 ? '%' : '+');
                }
            }, 30);
            counterObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

statNumbers.forEach(el => counterObserver.observe(el));

// ===== PORTFOLIO FILTER =====
const filterBtns = document.querySelectorAll('.filter-btn');
const portfolioItems = document.querySelectorAll('.portfolio-item');

filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const filter = btn.dataset.filter;

        portfolioItems.forEach(item => {
            if (filter === 'all' || item.dataset.category === filter) {
                item.classList.remove('hidden');
                setTimeout(() => item.classList.add('visible'), 50);
            } else {
                item.classList.remove('visible');
                setTimeout(() => item.classList.add('hidden'), 500);
            }
        });
    });
});

// ===== 3D TILT EFFECT =====
document.querySelectorAll('[data-tilt]').forEach(card => {
    card.addEventListener('mousemove', (e) => {
        const rect = card.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        const centerX = rect.width / 2;
        const centerY = rect.height / 2;
        const rotateX = (y - centerY) / 20;
        const rotateY = (centerX - x) / 20;
        card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-8px)`;
        card.style.setProperty('--mouse-x', `${(x / rect.width) * 100}%`);
        card.style.setProperty('--mouse-y', `${(y / rect.height) * 100}%`);
    });

    card.addEventListener('mouseleave', () => {
        card.style.transform = 'perspective(1000px) rotateX(0) rotateY(0) translateY(0)';
    });
});

// ===== MAGNETIC BUTTONS =====
document.querySelectorAll('.btn').forEach(btn => {
    btn.addEventListener('mousemove', (e) => {
        const rect = btn.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        btn.style.transform = `translate(${x * 0.3}px, ${y * 0.3}px)`;
    });

    btn.addEventListener('mouseleave', () => {
        btn.style.transform = 'translate(0, 0)';
    });
});

// ===== FORM SUBMIT =====
const contactForm = document.getElementById('contactForm');
if (contactForm) {
    contactForm.addEventListener('submit', (e) => {
        // Let Django handle the actual submission
        // This just adds visual feedback
        const btn = e.target.querySelector('button[type="submit"]');
        if (btn) {
            const originalText = btn.innerHTML;
            btn.innerHTML = 'Sending...';
            btn.disabled = true;

            // Re-enable after a moment (Django will handle the actual redirect)
            setTimeout(() => {
                btn.innerHTML = originalText;
                btn.disabled = false;
            }, 3000);
        }
    });
}

// ===== SMOOTH SCROLL =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });
});

// ===== MESSAGE AUTO-DISMISS =====
const messageContainer = document.querySelector('.message-container');
if (messageContainer) {
    setTimeout(() => {
        messageContainer.style.transition = 'opacity 0.5s, transform 0.5s';
        messageContainer.style.opacity = '0';
        messageContainer.style.transform = 'translateX(100px)';
        setTimeout(() => messageContainer.remove(), 500);
    }, 5000);
}