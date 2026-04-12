(function () {
      /*
       * Hero + ambient previews: Squarespace HLS (or .mp4 / YouTube / Vimeo).
       * Instagram reels are linked in the grid; embeds look like IG’s widget, so we use
       * native video for the “playing” look. Per-reel MP4s would need to be hosted by you.
       */
      /* Must exist on the deployed site (commit assets/hero-bg.mp4) or use a full URL: https://…/file.mp4, .m3u8, YouTube, or Vimeo.
       * If you change this, update the matching <link rel="preload"> in <head> (and poster preload if the fallback image changes). */
      var HERO_VIDEO_URL = 'assets/hero-bg.mp4';
      var AMBIENT_VIDEO_URL = HERO_VIDEO_URL;
      var HERO_FALLBACK_IMAGE =
        'https://images.squarespace-cdn.com/content/v1/65390bdc8b505402583f3d5b/74725833-ff01-45a1-a950-fb6e02e1976c/IMG_6154.jpg';

      function extractYouTubeId(url) {
        var m = url.match(/(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/|youtube\.com\/shorts\/)([^&\s?/#]+)/);
        return m ? m[1] : null;
      }
      function extractVimeoId(url) {
        var m = url.match(/vimeo\.com\/(?:video\/)?(\d+)/);
        return m ? m[1] : null;
      }
      function isHlsUrl(url) {
        return /\.m3u8(\?|$)/i.test(url) || url.indexOf('playlist.m3u8') !== -1;
      }
      function applyHeroImageFallback(container) {
        if (!container || container.id !== 'heroBg') return;
        container.classList.add('hero-bg--image');
        if (HERO_FALLBACK_IMAGE) {
          container.style.backgroundImage = 'url("' + HERO_FALLBACK_IMAGE + '")';
        }
      }
      function attachStreamingVideo(url, container, opts) {
        opts = opts || {};
        var isHero = opts.hero === true;
        var videoClass = opts.videoClass || 'hero-video';
        var video = document.createElement('video');
        video.className = videoClass;
        video.setAttribute('playsinline', '');
        video.setAttribute('webkit-playsinline', '');
        video.muted = true;
        video.loop = true;
        video.autoplay = true;
        video.playsInline = true;
        video.setAttribute('aria-hidden', 'true');
        if (opts.title) video.title = opts.title;
        if (isHero) {
          video.preload = 'auto';
          video.setAttribute('preload', 'auto');
          video.setAttribute('fetchpriority', 'high');
          if (HERO_FALLBACK_IMAGE) {
            video.poster = HERO_FALLBACK_IMAGE;
          }
        } else {
          video.preload = 'metadata';
          video.setAttribute('preload', 'metadata');
        }
        container.appendChild(video);

        function tryPlay() {
          var p = video.play();
          if (p && typeof p.catch === 'function') p.catch(function () {});
        }

        video.addEventListener(
          'error',
          function onVideoError() {
            video.removeEventListener('error', onVideoError);
            if (video.parentNode === container) container.removeChild(video);
            applyHeroImageFallback(container);
          },
          false
        );

        if (isHlsUrl(url)) {
          if (video.canPlayType('application/vnd.apple.mpegurl')) {
            video.src = url;
            video.addEventListener(
              'canplay',
              function onCp() {
                video.removeEventListener('canplay', onCp);
                tryPlay();
              },
              { once: true }
            );
            video.load();
            tryPlay();
            return;
          }
          if (typeof Hls !== 'undefined' && Hls.isSupported()) {
            var hlsConfig = {
              enableWorker: true,
              lowLatencyMode: false,
              maxBufferLength: 24,
              maxMaxBufferLength: 60
            };
            if (isHero) {
              hlsConfig.startLevel = 0;
              hlsConfig.capLevelToPlayerSize = true;
            }
            var hls = new Hls(hlsConfig);
            hls.loadSource(url);
            hls.attachMedia(video);
            hls.on(Hls.Events.MANIFEST_PARSED, function () {
              tryPlay();
            });
            hls.on(Hls.Events.ERROR, function (_, data) {
              if (data.fatal) {
                hls.destroy();
                if (video.parentNode === container) container.removeChild(video);
                applyHeroImageFallback(container);
              }
            });
            return;
          }
          if (video.parentNode === container) container.removeChild(video);
          applyHeroImageFallback(container);
          return;
        }
        var source = document.createElement('source');
        source.src = url;
        source.type = 'video/mp4';
        video.appendChild(source);
        video.load();
        video.addEventListener(
          'canplay',
          function onHeroCanPlay() {
            video.removeEventListener('canplay', onHeroCanPlay);
            tryPlay();
          },
          { once: true }
        );
        tryPlay();
      }
      function initHeroVideo() {
        var url = (typeof HERO_VIDEO_URL === 'string' && HERO_VIDEO_URL.trim()) || '';
        var container = document.getElementById('heroBg');
        if (!url || !container) return;
        if (container.classList.contains('hero-bg--image')) {
          container.classList.remove('hero-bg--image');
          container.style.backgroundImage = '';
        }

        if (/youtube\.com|youtu\.be/i.test(url)) {
          var yid = extractYouTubeId(url);
          if (!yid) return;
          var iframe = document.createElement('iframe');
          iframe.className = 'hero-video';
          iframe.title = 'Levels hero background';
          iframe.setAttribute('loading', 'eager');
          iframe.setAttribute('fetchpriority', 'high');
          iframe.src = 'https://www.youtube.com/embed/' + yid +
            '?autoplay=1&mute=1&loop=1&playlist=' + encodeURIComponent(yid) +
            '&controls=0&modestbranding=1&playsinline=1&rel=0&showinfo=0';
          iframe.setAttribute('allow', 'autoplay; encrypted-media; picture-in-picture; fullscreen');
          iframe.setAttribute('allowfullscreen', '');
          container.appendChild(iframe);
          return;
        }
        if (/vimeo\.com/i.test(url)) {
          var vid = extractVimeoId(url);
          if (!vid) return;
          var vframe = document.createElement('iframe');
          vframe.className = 'hero-video';
          vframe.title = 'Levels hero background';
          vframe.setAttribute('loading', 'eager');
          vframe.setAttribute('fetchpriority', 'high');
          vframe.src = 'https://player.vimeo.com/video/' + vid +
            '?autoplay=1&muted=1&loop=1&background=1&autopause=0';
          vframe.setAttribute('allow', 'autoplay; fullscreen; picture-in-picture');
          container.appendChild(vframe);
          return;
        }
        attachStreamingVideo(url, container, { hero: true });
      }

      function initAmbientVideos() {
        var url = (typeof AMBIENT_VIDEO_URL === 'string' && AMBIENT_VIDEO_URL.trim()) || '';
        if (!url) return;
        if (/youtube\.com|youtu\.be|vimeo\.com/i.test(url)) return;
        document.querySelectorAll('[data-ambient-video]').forEach(function (el) {
          attachStreamingVideo(url, el, { videoClass: 'ambient-video__el', title: 'Levels video preview' });
        });
      }

      function initHeroServices() {
        var wrap = document.querySelector('[data-hero-services]');
        if (!wrap) return;
        var grid = wrap.querySelector('.hero-services__grid');
        var dotsWrap = wrap.querySelector('[data-hero-dots]');
        if (!grid) return;
        var cards = grid.querySelectorAll('.hero-service-card');
        if (!cards.length) return;
        var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        var idx = 0;
        var timer = null;

        function setHighlight(i) {
          idx = (i + cards.length) % cards.length;
          cards.forEach(function (c, j) {
            c.classList.toggle('is-highlight', j === idx);
          });
          if (dotsWrap) {
            var dots = dotsWrap.querySelectorAll('.hero-services__dot');
            dots.forEach(function (d, j) {
              d.setAttribute('aria-current', j === idx ? 'true' : 'false');
            });
          }
        }

        function scrollCardIntoView(i) {
          if (window.innerWidth > 699) return;
          var card = cards[i];
          if (!card) return;
          var left = card.offsetLeft - grid.offsetLeft;
          try {
            grid.scrollTo({ left: left, behavior: reduced ? 'auto' : 'smooth' });
          } catch (e) {
            grid.scrollLeft = left;
          }
        }

        function isMobile() {
          return window.innerWidth <= 699;
        }

        if (dotsWrap && isMobile()) {
          for (var di = 0; di < cards.length; di++) {
            (function (n) {
              var b = document.createElement('button');
              b.type = 'button';
              b.className = 'hero-services__dot';
              b.setAttribute('aria-label', 'Go to service ' + (n + 1));
              b.addEventListener('click', function () {
                setHighlight(n);
                scrollCardIntoView(n);
              });
              dotsWrap.appendChild(b);
            })(di);
          }
        }

        setHighlight(0);

        if (!reduced) {
          timer = window.setInterval(function () {
            var next = (idx + 1) % cards.length;
            setHighlight(next);
            if (isMobile()) scrollCardIntoView(next);
          }, isMobile() ? 6200 : 4800);
        }

        if (isMobile()) {
          grid.addEventListener(
            'scroll',
            function () {
              var vp = grid.scrollLeft + grid.clientWidth * 0.5;
              var best = 0;
              var bestDist = Infinity;
              for (var si = 0; si < cards.length; si++) {
                var c = cards[si];
                var mid = c.offsetLeft + c.clientWidth * 0.5;
                var d = Math.abs(mid - vp);
                if (d < bestDist) {
                  bestDist = d;
                  best = si;
                }
              }
              setHighlight(best);
            },
            { passive: true }
          );
        }
      }

      initHeroVideo();
      initAmbientVideos();
      initHeroServices();

      (function initReelsCarousel() {
        var track = document.getElementById('reelsTrack');
        var wrap = document.getElementById('reelsCarousel');
        if (!track || !wrap) return;
        track.innerHTML += track.innerHTML;
        wrap.addEventListener('mouseenter', function () { track.classList.add('is-paused'); });
        wrap.addEventListener('mouseleave', function () { track.classList.remove('is-paused'); });
        wrap.addEventListener('touchstart', function () { track.classList.add('is-paused'); }, { passive: true });
        wrap.addEventListener('touchend', function () {
          window.setTimeout(function () { track.classList.remove('is-paused'); }, 2400);
        }, { passive: true });
      })();

      (function initBookingForm() {
        var form = document.getElementById('bookingForm');
        if (!form) return;
        form.addEventListener('submit', function (e) {
          e.preventDefault();
          var fd = new FormData(form);
          var name = (fd.get('name') || '').toString().trim();
          var email = (fd.get('email') || '').toString().trim();
          if (!name || !email) {
            window.alert('Please enter your name and email.');
            return;
          }
          var lines = [];
          lines.push('BOOKING REQUEST — Levels');
          lines.push('');
          lines.push('Name: ' + name);
          lines.push('Email: ' + email);
          lines.push('Phone: ' + (fd.get('phone') || '').toString().trim());
          lines.push('Event date: ' + (fd.get('event_date') || '').toString().trim());
          lines.push('Venue / city: ' + (fd.get('venue') || '').toString().trim());
          lines.push('');
          lines.push('Services:');
          if (fd.get('svc_videobooth')) lines.push('  · 360 Videobooth');
          if (fd.get('svc_pancake')) lines.push('  · Pancake cart');
          if (fd.get('svc_chocolate')) lines.push('  · Chocolate fountain');
          if (fd.get('svc_selfie')) lines.push('  · Selfie booth');
          lines.push('');
          lines.push('Message:');
          lines.push((fd.get('message') || '').toString().trim());
          var body = lines.join('\n');
          var subject = 'Booking request — ' + ((fd.get('event_date') || '').toString().trim() || 'Levels event');
          window.location.href = 'mailto:levels_360@outlook.com?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(body);
        });
      })();

      const loader = document.getElementById('loader');
      function hideLoader() {
        if (!loader || loader.classList.contains('hidden')) return;
        loader.classList.add('hidden');
        loader.setAttribute('aria-busy', 'false');
      }
      /* DOMContentLoaded + load: some previews never fire `load` if a resource hangs */
      document.addEventListener('DOMContentLoaded', function () {
        setTimeout(hideLoader, 380);
      });
      window.addEventListener('load', function () {
        setTimeout(hideLoader, 120);
      });
      window.setTimeout(hideLoader, 6000);

      const header = document.getElementById('siteHeader');
      if (header) {
        window.addEventListener('scroll', function () {
          header.classList.toggle('is-scrolled', window.scrollY > 24);
        });
      }

      const toggle = document.getElementById('navToggle');
      const mobile = document.getElementById('navMobile');
      if (toggle && mobile) {
        toggle.addEventListener('click', function () {
          const open = toggle.getAttribute('aria-expanded') === 'true';
          toggle.setAttribute('aria-expanded', !open);
          mobile.classList.toggle('is-open', !open);
        });
        mobile.querySelectorAll('a').forEach(function (link) {
          link.addEventListener('click', function () {
            toggle.setAttribute('aria-expanded', 'false');
            mobile.classList.remove('is-open');
          });
        });
      }

      document.querySelectorAll('.nav-desktop a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
          const id = this.getAttribute('href');
          if (id.length > 1) {
            e.preventDefault();
            const el = document.querySelector(id);
            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        });
      });
      mobile.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
          const id = this.getAttribute('href');
          if (id.length > 1) {
            e.preventDefault();
            const el = document.querySelector(id);
            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        });
      });
      document.querySelectorAll('.hero-actions a[href^="#"]').forEach(function (anchor) {
        anchor.addEventListener('click', function (e) {
          const id = this.getAttribute('href');
          if (id.length > 1) {
            e.preventDefault();
            const el = document.querySelector(id);
            if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        });
      });

      document.querySelectorAll('.card-grid, .testimonial-grid, .premium-grid, .gallery-masonry, .process-steps, .page-hub, .hero-services__grid').forEach(function (grid) {
        var items = [];
        for (var ci = 0; ci < grid.children.length; ci++) {
          var ch = grid.children[ci];
          if (ch.classList && ch.classList.contains('fade-in')) items.push(ch);
        }
        items.forEach(function (el, i) {
          el.style.setProperty('--enter-delay', (i * 0.07) + 's');
        });
      });

      var io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) entry.target.classList.add('visible');
        });
      }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
      document.querySelectorAll('.fade-in').forEach(function (el) { io.observe(el); });

      var sections = document.querySelectorAll('main section[id]');
      var navLinks = document.querySelectorAll('.nav-desktop a[href^="#"]');
      function setActive() {
        var y = window.scrollY + 120;
        var current = 'home';
        sections.forEach(function (s) {
          if (s.offsetTop <= y) current = s.getAttribute('id');
        });
        navLinks.forEach(function (l) {
          l.classList.toggle('active', l.getAttribute('href') === '#' + current);
        });
      }
      window.addEventListener('scroll', setActive);
      setActive();

      var navDropdown = document.getElementById('navDropdown');
      var navDropdownBtn = document.getElementById('navDropdownBtn');
      var navDropdownPanel = document.getElementById('navDropdownPanel');
      if (navDropdown && navDropdownBtn && navDropdownPanel) {
        navDropdownBtn.addEventListener('click', function (e) {
          e.stopPropagation();
          var open = navDropdown.classList.toggle('is-open');
          navDropdownBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
        });
        navDropdownPanel.querySelectorAll('a').forEach(function (a) {
          a.addEventListener('click', function () {
            navDropdown.classList.remove('is-open');
            navDropdownBtn.setAttribute('aria-expanded', 'false');
          });
        });
        document.addEventListener('click', function () {
          navDropdown.classList.remove('is-open');
          navDropdownBtn.setAttribute('aria-expanded', 'false');
        });
        navDropdown.addEventListener('click', function (e) {
          e.stopPropagation();
        });
      }
    })();
