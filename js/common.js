/* ═══ Wczytywanie wspólnych partiali (nav + footer) ═══ */

async function loadPartials() {
  try {
    const navRes = await fetch('/partials/nav.html');
    const navHTML = await navRes.text();
    const navPlaceholder = document.getElementById('nav-placeholder');
    if (navPlaceholder) navPlaceholder.innerHTML = navHTML;

    const footerRes = await fetch('/partials/footer.html');
    const footerHTML = await footerRes.text();
    const footerPlaceholder = document.getElementById('footer-placeholder');
    if (footerPlaceholder) footerPlaceholder.innerHTML = footerHTML;

    initMenu();
  } catch (err) {
    console.error('Nie udało się wczytać nav/footer:', err);
  }
}

/* ═══ Obsługa menu mobilnego (uruchamiana po wstrzyknięciu nav.html) ═══ */
function initMenu() {
  const hamburger = document.getElementById('hbg');
  const mobileMenu = document.getElementById('mobileMenu');
  const submenu = document.getElementById('tematySubmenu');
  const arrow = document.getElementById('tematyArrow');

  if (!hamburger || !mobileMenu) return;

  window.toggleMenu = function () {
    hamburger.classList.toggle('open');
    mobileMenu.classList.toggle('open');
    document.body.style.overflow = mobileMenu.classList.contains('open') ? 'hidden' : '';
  };

  window.closeMenu = function () {
    hamburger.classList.remove('open');
    mobileMenu.classList.remove('open');
    if (submenu) submenu.classList.remove('open');
    if (arrow) arrow.classList.remove('rotated');
    document.body.style.overflow = '';
  };

  window.toggleSubmenu = function () {
    if (submenu) submenu.classList.toggle('open');
    if (arrow) arrow.classList.toggle('rotated');
  };
}

document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape' && typeof window.closeMenu === 'function') {
    window.closeMenu();
  }
});

document.addEventListener('DOMContentLoaded', loadPartials);
