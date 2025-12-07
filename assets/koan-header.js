document.addEventListener('DOMContentLoaded', () => {
  const header = document.querySelector('.koan-header');
  const menuOverlay = document.querySelector('.koan-menu-overlay');
  const hamburgerBtn = document.querySelector('.js-hamburger-toggle');
  const menuItems = document.querySelectorAll('.koan-menu-item');
  const transparentOnTop = header.dataset.transparent === 'true';
  const menuLinks = menuOverlay.querySelectorAll('a, button'); // Focusable elements

  let lastScrollTop = 0;
  let isMenuOpen = false;

  // Initialize Header State
  updateHeaderState();

  // Scroll Behavior
  window.addEventListener('scroll', () => {
    if (isMenuOpen) return; // Don't hide header if menu is open

    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    // Threshold for solid transition
    const threshold = 50;

    // 1. Transparent vs Solid Logic
    if (scrollTop > threshold) {
      header.classList.remove('koan-header--transparent');
      header.classList.add('koan-header--solid');
    } else {
      if (transparentOnTop) {
        header.classList.add('koan-header--transparent');
        header.classList.remove('koan-header--solid');
      } else {
        header.classList.remove('koan-header--transparent');
        header.classList.add('koan-header--solid');
      }
    }

    // 2. Hide/Show Logic
    // Only trigger hide if scrolled past threshold to avoid flickering at top
    if (scrollTop > threshold && scrollTop > lastScrollTop) {
      // Scroll Down
      header.classList.add('koan-header--hidden');
      header.classList.remove('koan-header--visible');
    } else {
      // Scroll Up
      header.classList.remove('koan-header--hidden');
      header.classList.add('koan-header--visible');
    }

    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
  }, { passive: true });

  function updateHeaderState() {
     if (window.scrollY > 50) {
        header.classList.remove('koan-header--transparent');
        header.classList.add('koan-header--solid');
     } else if (transparentOnTop) {
        header.classList.add('koan-header--transparent');
     } else {
        header.classList.add('koan-header--solid');
     }
  }

  function toggleMenu() {
    isMenuOpen = !isMenuOpen;
    menuOverlay.classList.toggle('is-active', isMenuOpen);
    menuOverlay.setAttribute('aria-hidden', !isMenuOpen);
    hamburgerBtn.setAttribute('aria-expanded', isMenuOpen);

    // Toggle Hamburger Icon State (X shape) if desired - using CSS class
    hamburgerBtn.classList.toggle('is-active', isMenuOpen);

    // Lock Body Scroll
    document.body.style.overflow = isMenuOpen ? 'hidden' : '';

    if (isMenuOpen) {
      // Ensure header is visible and solid when menu is open
      header.classList.remove('koan-header--hidden', 'koan-header--transparent');
      header.classList.add('koan-header--visible', 'koan-header--solid');

      // Staggered Animation
      menuItems.forEach((item, index) => {
        setTimeout(() => {
          item.classList.add('is-visible');
        }, index * 100); // 100ms delay per item
      });

      // Trap focus
      if (menuLinks.length > 0) {
        // Wait for animation to start effectively
        setTimeout(() => {
            menuLinks[0].focus();
        }, 100);
      }
    } else {
      // Reset Animation
      menuItems.forEach(item => {
        item.classList.remove('is-visible');
      });
      // Re-evaluate header state
      updateHeaderState();
      hamburgerBtn.focus();
    }
  }

  // Mobile Menu Toggle
  hamburgerBtn.addEventListener('click', toggleMenu);

  // Close on Esc
  document.addEventListener('keydown', (e) => {
    if (isMenuOpen && e.key === 'Escape') {
      toggleMenu();
    }
  });

  // Basic Focus Trap inside Menu
  menuOverlay.addEventListener('keydown', (e) => {
    if (!isMenuOpen) return;

    const firstElement = menuLinks[0];
    const lastElement = menuLinks[menuLinks.length - 1];

    if (e.key === 'Tab') {
        if (e.shiftKey) { // Shift + Tab
            if (document.activeElement === firstElement) {
                e.preventDefault();
                lastElement.focus();
            }
        } else { // Tab
            if (document.activeElement === lastElement) {
                e.preventDefault();
                firstElement.focus();
            }
        }
    }
  });
});
