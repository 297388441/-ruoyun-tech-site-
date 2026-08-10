// 移动端菜单开合
(function () {
  const toggle = document.getElementById('navToggle');
  const menu = document.getElementById('navMenu');
  if (!toggle || !menu) return;

  function closeMenu() {
    menu.classList.remove('open');
    toggle.setAttribute('aria-expanded', 'false');
  }

  toggle.addEventListener('click', function () {
    const isOpen = menu.classList.toggle('open');
    toggle.setAttribute('aria-expanded', String(isOpen));
  });

  // 点击菜单项后自动收起
  menu.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', closeMenu);
  });

  // 视口放大到桌面尺寸时重置菜单状态
  window.addEventListener('resize', function () {
    if (window.innerWidth > 720) closeMenu();
  });
})();

// 页脚年份
(function () {
  const el = document.getElementById('year');
  if (el) el.textContent = new Date().getFullYear();
})();

// 关于我数字滚动（轻量，进入视口才跑）
(function () {
  const nums = document.querySelectorAll('.stat__num[data-target]');
  if (!nums.length) return;
  const run = function (node) {
    const target = parseInt(node.getAttribute('data-target'), 10);
    let cur = 0;
    const step = Math.max(1, Math.ceil(target / 30));
    const tick = function () {
      cur += step;
      if (cur >= target) { node.textContent = target; return; }
      node.textContent = cur;
      requestAnimationFrame(tick);
    };
    tick();
  };
  if (!('IntersectionObserver' in window)) {
    nums.forEach(run);
    return;
  }
  const io = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) { run(e.target); io.unobserve(e.target); }
    });
  }, { threshold: 0.5 });
  nums.forEach(function (n) { io.observe(n); });
})();
