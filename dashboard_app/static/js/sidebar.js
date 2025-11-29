document.addEventListener('DOMContentLoaded', function () {
  const toggleBtn = document.getElementById('sidebarToggle');
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('sidebarOverlay');
  const mainContent = document.getElementById('mainContent');

  // Labels inside links and header that should be hidden when sidebar is collapsed on desktop
   const labelEls = sidebar ? sidebar.querySelectorAll('.sidebar-label') : [];
   const logoText = sidebar ? sidebar.querySelector('.leading-tight') : null;
   const navLinks = sidebar ? sidebar.querySelectorAll('nav a, nav button') : [];

  if (!toggleBtn || !sidebar) return;

  const isMobileOpen = () => !sidebar.classList.contains('-translate-x-full');
  const isDesktop = () => window.innerWidth >= 768;

  // Restore sidebar state from localStorage
  const savedCollapsed = localStorage.getItem('sidebarCollapsed') === 'true';
  if (savedCollapsed && isDesktop()) {
    // Apply collapsed state
    sidebar.classList.add('collapsed');
    sidebar.classList.remove('md:w-72');
    sidebar.classList.add('md:w-20');
    mainContent.classList.remove('md:ml-72');
    mainContent.classList.add('md:ml-20');
    labelEls.forEach(el => el.classList.add('hidden'));
    if (logoText) logoText.classList.add('hidden');
    navLinks.forEach(link => {
      link.classList.add('justify-center');
      link.classList.add('hover:bg-blue-50');
      link.classList.remove('hover:bg-gray-100');
    });
  }

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

    // Save state to localStorage
    localStorage.setItem('sidebarCollapsed', collapsed);

    if (!mainContent) return;

    if (collapsed) {
      // shrink sidebar to icons-only
      sidebar.classList.remove('md:w-72');
      sidebar.classList.add('md:w-20');
      // adjust main content margin for md and up
      mainContent.classList.remove('md:ml-72');
      mainContent.classList.add('md:ml-20');
      // hide labels and logo text
      labelEls.forEach(el => el.classList.add('hidden'));
      if (logoText) logoText.classList.add('hidden');
      // center nav link icons and adjust hover effects
      navLinks.forEach(link => {
        link.classList.add('justify-center');
        link.classList.add('hover:bg-blue-50');
        link.classList.remove('hover:bg-gray-100');
      });
      toggleBtn.setAttribute('aria-expanded', 'true');
    } else {
      // expand sidebar
      sidebar.classList.remove('md:w-20');
      sidebar.classList.add('md:w-72');
      mainContent.classList.remove('md:ml-20');
      mainContent.classList.add('md:ml-72');
      // show labels and logo text
      labelEls.forEach(el => el.classList.remove('hidden'));
      if (logoText) logoText.classList.remove('hidden');
      // left-align nav link content and restore hover effects
      navLinks.forEach(link => {
        link.classList.remove('justify-center');
        link.classList.remove('hover:bg-blue-50');
        link.classList.add('hover:bg-gray-100');
      });
      toggleBtn.setAttribute('aria-expanded', 'false');
    }
  }

  function handleToggle(e) {
    e.preventDefault();
    if (isDesktop()) {
      toggleDesktopCollapse();
    } else {
      toggleSidebar();
    }
  }

  toggleBtn.addEventListener('click', handleToggle);

  // Expose globally for inline onclick
  window.toggleSidebarGlobal = handleToggle;

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
