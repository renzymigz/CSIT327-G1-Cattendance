document.addEventListener('DOMContentLoaded', function () {
  const toggleBtn = document.getElementById('sidebarToggle');
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebarOverlay');
  const mainContent = document.getElementById('mainContent');

  // Labels inside links and header that should be hidden when sidebar is collapsed on desktop
  const labelEls = sidebar ? sidebar.querySelectorAll('.sidebar-label') : [];

  if (!toggleBtn || !sidebar) return;

  const isMobileOpen = () => !sidebar.classList.contains('-translate-x-full');
  const isDesktop = () => window.innerWidth >= 768;

  function openSidebar() {
    sidebar.classList.remove('-translate-x-full');
    sidebar.classList.add('translate-x-0');
    if (overlay) overlay.classList.remove('hidden');
    toggleBtn.setAttribute('aria-expanded', 'true');
    // move focus into the sidebar for accessibility
    const focusable = sidebar.querySelector('a, button, input, [tabindex]:not([tabindex="-1"])');
    if (focusable) focusable.focus();
  }

  function closeSidebar() {
    sidebar.classList.add('-translate-x-full');
    sidebar.classList.remove('translate-x-0');
    if (overlay) overlay.classList.add('hidden');
    toggleBtn.setAttribute('aria-expanded', 'false');
    toggleBtn.focus();
  }

  function toggleSidebar() {
    if (isMobileOpen()) closeSidebar(); else openSidebar();
  }

  function toggleDesktopCollapse() {
    // toggle collapsed state
    const collapsed = sidebar.classList.toggle('collapsed');

    if (!mainContent) return;

    if (collapsed) {
      // shrink sidebar to icons-only
      sidebar.classList.remove('w-72');
      sidebar.classList.add('w-24');
      // adjust main content margin for md and up
      mainContent.classList.remove('md:ml-72');
      mainContent.classList.add('md:ml-24');
      // hide labels
      labelEls.forEach(el => el.classList.add('hidden'));
      toggleBtn.setAttribute('aria-expanded', 'true');
    } else {
      // expand sidebar
      sidebar.classList.remove('w-24');
      sidebar.classList.add('w-72');
      mainContent.classList.remove('md:ml-24');
      mainContent.classList.add('md:ml-72');
      // show labels
      labelEls.forEach(el => el.classList.remove('hidden'));
      toggleBtn.setAttribute('aria-expanded', 'false');
    }
  }

  toggleBtn.addEventListener('click', function (e) {
    e.preventDefault();
    if (isDesktop()) {
      toggleDesktopCollapse();
    } else {
      toggleSidebar();
    }
  });

  if (overlay) {
    overlay.addEventListener('click', function () {
      closeSidebar();
    });
  }

  // Close on Escape
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && isMobileOpen()) {
      closeSidebar();
    }
  });
});
