/* ==========================================================================
   Lincoln County Painters — Premium JavaScript
   ========================================================================== */
(function () {
  'use strict';

  var prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------- NAV SCROLL ---------- */
  var nav = document.getElementById('nav');
  if (nav && !nav.classList.contains('nav-solid')) {
    var ticking = false;
    window.addEventListener('scroll', function () {
      if (!ticking) {
        requestAnimationFrame(function () {
          nav.classList.toggle('scrolled', window.scrollY > 60);
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });
  }

  /* ---------- MOBILE MENU ---------- */
  var toggle = document.getElementById('navToggle');
  var mob = document.getElementById('mobileNav');
  var mobClose = document.getElementById('mobileClose');

  function openMenu() {
    if (mob) mob.classList.add('open');
    if (toggle) toggle.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
  }
  function closeMenu() {
    if (mob) mob.classList.remove('open');
    if (toggle) toggle.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }
  if (toggle) toggle.addEventListener('click', openMenu);
  if (mobClose) mobClose.addEventListener('click', closeMenu);
  if (mob) {
    mob.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', closeMenu);
    });
  }

  /* ---------- HERO VIDEO / POSTER ---------- */
  var video = document.getElementById('heroVideo');
  var poster = document.getElementById('heroPoster');
  if (video) {
    video.addEventListener('canplay', function () {
      if (poster) poster.style.display = 'none';
    });
    video.addEventListener('error', function () {
      if (video) video.style.display = 'none';
    });
  }

  /* ---------- HERO PARALLAX ---------- */
  if (!prefersReducedMotion) {
    var heroMedia = document.querySelector('.hero-media');
    var heroContent = document.querySelector('.hero-content');
    if (heroMedia && heroContent) {
      var heroTicking = false;
      window.addEventListener('scroll', function () {
        if (!heroTicking) {
          requestAnimationFrame(function () {
            var y = window.scrollY;
            if (y < window.innerHeight) {
              heroMedia.style.transform = 'translateY(' + (y * 0.3) + 'px)';
              heroContent.style.transform = 'translateY(' + (y * 0.15) + 'px)';
              heroContent.style.opacity = Math.max(0, 1 - y / (window.innerHeight * 0.7));
            }
            heroTicking = false;
          });
          heroTicking = true;
        }
      }, { passive: true });
    }
  }

  /* ---------- SCROLL REVEAL ---------- */
  var revealObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        revealObserver.unobserve(e.target);
      }
    });
  }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

  document.querySelectorAll('.reveal').forEach(function (el) {
    revealObserver.observe(el);
  });

  /* ---------- STAT COUNTER ---------- */
  var counterObserver = new IntersectionObserver(function (entries) {
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      var el = e.target;
      var target = parseInt(el.dataset.target, 10);
      var duration = 1800;
      var start = performance.now();
      function tick(now) {
        var progress = Math.min((now - start) / duration, 1);
        var ease = 1 - Math.pow(1 - progress, 4);
        el.textContent = Math.round(target * ease);
        if (progress < 1) requestAnimationFrame(tick);
      }
      requestAnimationFrame(tick);
      counterObserver.unobserve(el);
    });
  }, { threshold: 0.5 });

  document.querySelectorAll('.stat-number[data-target]').forEach(function (el) {
    counterObserver.observe(el);
  });

  /* ---------- 3D TILT ON SERVICE CARDS ---------- */
  if (!prefersReducedMotion && window.innerWidth > 768) {
    document.querySelectorAll('.service-card').forEach(function (card) {
      card.addEventListener('mousemove', function (e) {
        var rect = card.getBoundingClientRect();
        var x = e.clientX - rect.left;
        var y = e.clientY - rect.top;
        var centerX = rect.width / 2;
        var centerY = rect.height / 2;
        var rotateX = ((y - centerY) / centerY) * -4;
        var rotateY = ((x - centerX) / centerX) * 4;
        card.style.transform = 'translateY(-8px) perspective(800px) rotateX(' + rotateX + 'deg) rotateY(' + rotateY + 'deg)';
      });
      card.addEventListener('mouseleave', function () {
        card.style.transform = '';
      });
    });
  }

  /* ---------- FAQ ACCORDION ---------- */
  document.querySelectorAll('.faq-question').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var item = btn.closest('.faq-item');
      var wasOpen = item.classList.contains('open');
      document.querySelectorAll('.faq-item.open').forEach(function (openItem) {
        openItem.classList.remove('open');
      });
      if (!wasOpen) item.classList.add('open');
    });
  });

  /* ---------- FORM SUBMISSION (Formspree) ---------- */
  var forms = document.querySelectorAll('form[data-formspree]');
  forms.forEach(function (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var btn = form.querySelector('button[type="submit"]');
      var originalText = btn ? btn.textContent : '';
      if (btn) {
        btn.disabled = true;
        btn.textContent = 'Sending...';
      }

      var data = new FormData(form);
      fetch(form.action, {
        method: 'POST',
        body: data,
        headers: { 'Accept': 'application/json' }
      })
        .then(function (response) {
          if (response.ok) {
            var redirect = form.dataset.redirect;
            if (redirect) {
              window.location.href = redirect;
            } else {
              var thanks = form.parentElement.querySelector('.form-thanks');
              if (thanks) {
                form.style.display = 'none';
                thanks.style.display = 'block';
              } else {
                form.reset();
                if (btn) {
                  btn.textContent = 'Sent!';
                  setTimeout(function () {
                    btn.textContent = originalText;
                    btn.disabled = false;
                  }, 3000);
                }
              }
            }
          } else {
            throw new Error('Form submission failed');
          }
        })
        .catch(function () {
          if (btn) {
            btn.textContent = 'Error - Try Again';
            btn.disabled = false;
            setTimeout(function () {
              btn.textContent = originalText;
            }, 3000);
          }
        });
    });
  });

  /* ---------- SMOOTH SCROLL ---------- */
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var href = a.getAttribute('href');
      if (href === '#' || href.length < 2) return;
      var target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        var navHeight = nav ? nav.offsetHeight : 72;
        var top = target.getBoundingClientRect().top + window.pageYOffset - navHeight;
        window.scrollTo({ top: top, behavior: 'smooth' });
      }
    });
  });

})();
