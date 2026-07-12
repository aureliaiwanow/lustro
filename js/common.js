/* ═══ Obsługa menu mobilnego ═══ */
/* Nav i footer są teraz wklejone bezpośrednio w HTML (przez Jekyll include),
   więc nie ma już fetch()'a ani czekania na wstrzyknięcie — ta funkcja
   uruchamia się od razu. */

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

document.addEventListener('DOMContentLoaded', initMenu);
