// swipe.js — prevent swipe from breaking mobile scroll
(function() {
  let startX = 0;
  let endX = 0;
  let isDragging = false;
  let dragStartTime = 0;
  const minSwipeDistance = 50;
  const maxDragTime = 300;

  function getNavigationUrls() {
    const navLinks = document.querySelectorAll('.nav-links .nav-link, .mobile-nav a');
    const urls = [];
    navLinks.forEach(link => {
      let href = link.getAttribute('href');
      if (href && href !== '#' && !href.includes('logout') && !href.includes('login') && !href.includes('register')) {
        if (!urls.includes(href)) urls.push(href);
      }
    });
    if (urls.length === 0) return ['/', '/notes/', '/syllabus/', '/books/', '/pyq/', '/doubts/'];
    return urls;
  }

  function getCurrentPageIndex(urls) {
    const currentPath = window.location.pathname;
    let idx = urls.findIndex(u => currentPath === u || currentPath === u + '/');
    if (idx === -1) {
      idx = urls.findIndex(u => currentPath.includes(u.replace(/\//g, '')));
    }
    return idx !== -1 ? idx : 0;
  }

  function navigateBySwipe(diffX) {
    if (Math.abs(diffX) < minSwipeDistance) return false;
    const urls = getNavigationUrls();
    if (urls.length === 0) return false;

    const currentIdx = getCurrentPageIndex(urls);
    let newIdx = currentIdx;

    // diffX > 0 means swipe left -> next
    if (diffX > 0) newIdx = Math.min(urls.length - 1, currentIdx + 1);
    else if (diffX < 0) newIdx = Math.max(0, currentIdx - 1);

    if (newIdx !== currentIdx && urls[newIdx]) {
      window.location.href = urls[newIdx];
      return true;
    }
    return false;
  }

  function shouldIgnoreTouch(target) {
    if (!target) return false;
    // allow scroll; do not start swipe on interactive elements
    return target.closest('a, button, .btn, input, select, textarea, label, [role="button"], .auth-card, .auth-form');
  }

  // TOUCH: keep it passive and never prevent default (so vertical scroll works)
  document.addEventListener('touchstart', (e) => {
    const t = e.target;
    if (shouldIgnoreTouch(t)) {
      isDragging = false;
      return;
    }
    startX = e.changedTouches[0].screenX;
    isDragging = true;
    dragStartTime = Date.now();
  }, { passive: true });

  document.addEventListener('touchend', (e) => {
    if (!isDragging) return;
    endX = e.changedTouches[0].screenX;
    const diff = startX - endX;
    const dragDuration = Date.now() - dragStartTime;
    if (dragDuration <= maxDragTime) navigateBySwipe(diff);
    isDragging = false;
  }, { passive: true });

  // MOUSE: desktop swipe support but do not block scroll
  let mouseStartX = 0;
  let mouseDragging = false;

  document.addEventListener('mousedown', (e) => {
    if (e.button !== 0) return;
    if (e.target && e.target.closest && e.target.closest('a, button, .btn, input, select, textarea, [role="button"]')) {
      mouseDragging = false;
      return;
    }
    mouseStartX = e.screenX;
    mouseDragging = true;
    dragStartTime = Date.now();
  });

  document.addEventListener('mouseup', (e) => {
    if (!mouseDragging) return;
    const mouseEndX = e.screenX;
    const diff = mouseStartX - mouseEndX;
    const dragDuration = Date.now() - dragStartTime;
    if (dragDuration <= maxDragTime) navigateBySwipe(diff);
    mouseDragging = false;
  });
})();
