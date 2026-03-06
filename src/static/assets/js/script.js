// Script.js - Krypta Code Site
// Interatividades e animações da página

document.addEventListener('DOMContentLoaded', function () {
    // Inicializar observador de scroll para animações
    initScrollAnimations();

    // Adicionar event listeners aos botões
    initButtons();

    // Smooth scroll para links de navegação
    initSmoothScroll();
});

/**
 * Inicializar animações ao scroll
 */
function initScrollAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-slide-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    });

    // Observar cards e elementos
    const cards = document.querySelectorAll('.solution-card, .step-card, .about-icon-box');
    cards.forEach(card => {
        observer.observe(card);
    });
}

/**
 * Inicializar event listeners dos botões
 */
function initButtons() {
    const buttons = document.querySelectorAll('.btn-primary, .cta-button');

    buttons.forEach(button => {
        button.addEventListener('click', function (e) {
            // Adicionar efeito de clique
            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            this.appendChild(ripple);

            // Remover ripple após animação
            setTimeout(() => {
                ripple.remove();
            }, 600);

            // Aqui você pode adicionar lógica de redirecionamento ou modal
            console.log('Botão clicado:', this.textContent);

            // Exemplo: abrir modal ou redirecionar
            // window.location.href = '/contato';
        });
    });
}

/**
 * Smooth scroll para links internos
 */
function initSmoothScroll() {
    const links = document.querySelectorAll('a[href^="#"]');

    links.forEach(link => {
        link.addEventListener('click', function (e) {
            const href = this.getAttribute('href');

            // Ignorar links vazios
            if (href === '#') return;

            e.preventDefault();

            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Adicionar classe ao navbar ao fazer scroll
 */
window.addEventListener('scroll', function () {
    const nav = document.querySelector('nav');
    if (window.scrollY > 50) {
        nav.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.1)';
    } else {
        nav.style.boxShadow = 'none';
    }
});

/**
 * Função para abrir modal de contato (exemplo)
 */
function openContactModal() {
    console.log('Abrindo modal de contato...');
    // Implementar lógica de modal aqui
}

/**
 * Função para enviar formulário de contato (exemplo)
 */
function submitContactForm(formData) {
    console.log('Enviando formulário:', formData);
    // Implementar lógica de envio aqui
}

/**
 * Adicionar animação de hover aos cards
 */
function addCardHoverAnimation() {
    const cards = document.querySelectorAll('.solution-card, .step-card, .about-icon-box');

    cards.forEach(card => {
        card.addEventListener('mouseenter', function () {
            this.style.transform = 'translateY(-8px)';
        });

        card.addEventListener('mouseleave', function () {
            this.style.transform = 'translateY(0)';
        });
    });
}

/**
 * Função para rastrear eventos (analytics)
 */
function trackEvent(category, action, label) {
    if (typeof gtag !== 'undefined') {
        gtag('event', action, {
            'event_category': category,
            'event_label': label
        });
    }
}

/**
 * Inicializar quando o DOM estiver pronto
 */
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', addCardHoverAnimation);
} else {
    addCardHoverAnimation();
}

// Exportar funções para uso global
window.kryptaCode = {
    openContactModal,
    submitContactForm,
    trackEvent
};
