---
layout: single
title: "In the Field"
permalink: /field/
author_profile: true
---

<div class="field-tabs">
  <nav class="field-tabs__nav">
    <button class="field-tabs__btn active" data-tab="liberia">Field Research in Liberia</button>
    <button class="field-tabs__btn" data-tab="cambridge">Field Research in Cambridge University Hospitals</button>
  </nav>

  <div class="field-tabs__panel active" id="tab-liberia">
    <p>I visited Liberia in July 2025. This trip built on three years of collaboration between the Family Health Division of Liberia's Ministry of Health, the University of Liberia's College of Health Sciences, London Business School, and the University of Michigan's School of Nursing.</p>

    <p>We visited health facilities and maternity waiting homes (MWHs) in Bong, Nimba, and Grand Cape Mount counties. We met with County Health Team officers, midwives, nurses, and patients to understand firsthand the challenges of delivering perinatal care in these settings.</p>

    <div class="field-gallery-wrap">
      <div class="field-gallery-wrap__label">Field Photo Gallery &mdash; Liberia, July 2025</div>
      <div class="field-gallery" id="liberia-gallery">
        <div class="field-gallery__item" onclick="openLightbox('/images/Liberia/workshop.JPG')">
          <img src="/images/Liberia/workshop.JPG" alt="Workshop in Liberia" />
          <div class="field-gallery__caption">Technical training workshop in Monrovia with the Ministry of Health, County Health Teams, the University of Liberia, and CHAI.</div>
        </div>
        <div class="field-gallery__item" onclick="openLightbox('/images/Liberia/CHT.JPG')">
          <img src="/images/Liberia/CHT.JPG" alt="Meeting with County Health Team" />
          <div class="field-gallery__caption">Meeting with County Health Team officers during facility visits.</div>
        </div>
        <div class="field-gallery__item" onclick="openLightbox('/images/Liberia/CA_map.png')">
          <img src="/images/Liberia/CA_map.png" alt="Catchment area map" />
          <div class="field-gallery__caption">Catchment area of Fenutoli Clinic.</div>
        </div>
        <div class="field-gallery__item" onclick="openLightbox('/images/Liberia/MWH_1.png')">
          <img src="/images/Liberia/MWH_1.png" alt="Maternity waiting home" />
          <div class="field-gallery__caption">A maternity waiting home (MWH) where expectant mothers stay near a clinic ahead of delivery.</div>
        </div>
        <div class="field-gallery__item" onclick="openLightbox('/images/Liberia/room.png')">
          <img src="/images/Liberia/room.png" alt="Inside an MWH" />
          <div class="field-gallery__caption">Inside an MWH: sleeping quarters for mothers awaiting delivery.</div>
        </div>
      </div>
    </div>

    <p>Our team also led a two-day technical training workshop in Monrovia. The workshop brought together maternal health leaders from across Liberia, including representatives from the Ministry of Health, County Health Teams, the University of Liberia, and the Clinton Health Access Initiative (CHAI). Participants received hands-on training on two analytical tools we developed for individual and population level unassisted birth risk assessment. The sessions also opened rich discussions. Participants shared accounts of limited MWH capacity, difficulties in communicating risk to patients and families, and the need for better training for midwives. These conversations reinforced how much lies beyond the reach of models and data alone, and confirmed the importance of designing tools that practitioners can trust and use.</p>

    <h2>Two Implementation Tools</h2>

    <div class="field-accordion">

      <details class="field-accordion__item" open>
        <summary class="field-accordion__header">
          <i class="fas fa-chevron-right field-accordion__arrow"></i>
          Tool 1: Skilled Birth Assistance (SBA) Wheel
        </summary>
        <div class="field-accordion__body">
          <p>For the local clinic (individual) level, we have designed and manufactured a cardboard-based device to facilitate the calculation by nurses of the BBA risks facing individual patients, and discussion of potential interventions to mitigate them, during their antenatal consultations. This device also quantifies the reduction of BBA risk associated with potential MWH stays of different lengths, and may thus facilitate (i) the promotion of MWHs as a perinatal health intervention; and (ii) the implementation of the optimal egalitarian MWH assignment policy derived as part of our analysis.</p>
          {% include sba-wheel.html %}
        </div>
      </details>

      <details class="field-accordion__item">
        <summary class="field-accordion__header">
          <i class="fas fa-chevron-right field-accordion__arrow"></i>
          Tool 2: Artemis Unassisted Birth Risk Mapping System
        </summary>
        <div class="field-accordion__body">
          <p>For the national or regional (population) health administration level, we have coordinated the development of an open-access, web-based software to map and analyze birth rate, HF network and BBA risk in order to (i) identify communities facing the highest risks of BBAs and prioritize related health interventions accordingly; (ii) evaluate, generate and disseminate data-driven MWH assignment policies; and (iii) inform capacity management and facility location decisions in MWH facility networks.</p>
          <p><a href="https://artemis-inky.vercel.app/dashboard" target="_blank" rel="noopener">Launch Artemis &rarr;</a></p>
          <div style="display:flex;flex-direction:column;gap:1.5em;margin-top:1em;align-items:center;">
            <figure style="margin:0;width:80%;text-align:left;">
              <figcaption style="font-size:.88em;color:#444;margin-bottom:.4em;">Figure: Selected Artemis Output Map.</figcaption>
              <img src="/images/Artemis/output_map.png" alt="Selected Artemis Output Map" style="width:100%;border:1px solid #ddd;" />
            </figure>
            <figure style="margin:0;width:80%;text-align:left;">
              <figcaption style="font-size:.88em;color:#444;margin-bottom:.4em;">Figure: Selected Artemis Output Table.</figcaption>
              <img src="/images/Artemis/output_table.png" alt="Selected Artemis Output Table" style="width:100%;border:1px solid #ddd;" />
            </figure>
          </div>
        </div>
      </details>

    </div>

    <p>For more information, please visit our project website: <a href="https://birth-analytics.org" target="_blank" rel="noopener">birth-analytics.org</a></p>
  </div>

  <div class="field-tabs__panel" id="tab-cambridge">
    <h2>Scheduling Elective Caesarean Sections in the NHS (2026)</h2>
    <p>In collaboration with Cambridge University Hospitals and the University of Cambridge (Department of Obstetrics &amp; Gynaecology), we are working with NHS maternity teams to rethink how scarce operating-theatre capacity is allocated between early- and late-booking patients. Building on this partnership, we have developed an <strong>interactive planning tool</strong> that allows any maternity unit to calibrate a fair and efficient scheduling policy to its own data.</p>
    <p><em style="color: var(--global-link-color);">Tool link coming soon.</em></p>
  </div>
</div>

<div class="field-lightbox" id="field-lightbox" onclick="closeLightbox()" role="dialog" aria-modal="true" aria-label="Photo viewer">
  <button class="field-lightbox__close" onclick="event.stopPropagation(); closeLightbox();" aria-label="Close (Esc)">
    <span class="field-lightbox__close-x" aria-hidden="true">&times;</span>
    <span>Close</span>
  </button>
  <button class="field-lightbox__nav field-lightbox__nav--prev" onclick="event.stopPropagation(); lightboxPrev();" aria-label="Previous photo">&#10094;</button>
  <button class="field-lightbox__nav field-lightbox__nav--next" onclick="event.stopPropagation(); lightboxNext();" aria-label="Next photo">&#10095;</button>
  <div class="field-lightbox__stage" onclick="event.stopPropagation()">
    <img id="field-lightbox-img" class="field-lightbox__img" src="" alt="" />
    <div class="field-lightbox__meta">
      <div class="field-lightbox__counter" id="field-lightbox-counter"></div>
      <div id="field-lightbox-caption"></div>
    </div>
  </div>
</div>

<script>
function showTab(tab) {
  document.querySelectorAll('.field-tabs__btn').forEach(function(b) {
    b.classList.toggle('active', b.getAttribute('data-tab') === tab);
  });
  ['liberia', 'cambridge'].forEach(function(t) {
    var el = document.getElementById('tab-' + t);
    if (el) el.classList.toggle('active', t === tab);
  });
}

(function() {
  document.querySelectorAll('.field-tabs__btn').forEach(function(btn) {
    btn.addEventListener('click', function() {
      showTab(btn.getAttribute('data-tab'));
    });
  });
})();

function galleryScroll(id, dir) {
  var gallery = document.getElementById(id);
  if (gallery) gallery.scrollBy({ left: dir * 400, behavior: 'smooth' });
}


var lightboxPhotos = [];
var lightboxIndex = 0;

function buildLightboxPhotos() {
  lightboxPhotos = Array.prototype.map.call(
    document.querySelectorAll('#liberia-gallery .field-gallery__item'),
    function(item) {
      var img = item.querySelector('img');
      var cap = item.querySelector('.field-gallery__caption');
      return {
        src: img ? img.getAttribute('src') : '',
        alt: img ? img.getAttribute('alt') : '',
        caption: cap ? cap.innerHTML : ''
      };
    }
  );
}

function renderLightbox() {
  if (!lightboxPhotos.length) return;
  var photo = lightboxPhotos[lightboxIndex];
  var imgEl = document.getElementById('field-lightbox-img');
  imgEl.src = photo.src;
  imgEl.alt = photo.alt;
  document.getElementById('field-lightbox-caption').innerHTML = photo.caption;
  document.getElementById('field-lightbox-counter').textContent =
    'Photo ' + (lightboxIndex + 1) + ' of ' + lightboxPhotos.length;
}

function openLightbox(src) {
  if (!lightboxPhotos.length) buildLightboxPhotos();
  var found = lightboxPhotos.findIndex(function(p) { return p.src === src; });
  lightboxIndex = found >= 0 ? found : 0;
  renderLightbox();
  document.getElementById('field-lightbox').classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeLightbox() {
  document.getElementById('field-lightbox').classList.remove('open');
  document.body.style.overflow = '';
}

function lightboxPrev() {
  if (!lightboxPhotos.length) return;
  lightboxIndex = (lightboxIndex - 1 + lightboxPhotos.length) % lightboxPhotos.length;
  renderLightbox();
}

function lightboxNext() {
  if (!lightboxPhotos.length) return;
  lightboxIndex = (lightboxIndex + 1) % lightboxPhotos.length;
  renderLightbox();
}

document.addEventListener('keydown', function(e) {
  var open = document.getElementById('field-lightbox').classList.contains('open');
  if (!open) return;
  if (e.key === 'Escape') closeLightbox();
  else if (e.key === 'ArrowLeft') lightboxPrev();
  else if (e.key === 'ArrowRight') lightboxNext();
});

(function() {
  var lb = document.getElementById('field-lightbox');
  if (!lb) return;
  var touchStartX = null;
  lb.addEventListener('touchstart', function(e) {
    if (e.touches.length === 1) touchStartX = e.touches[0].clientX;
  }, { passive: true });
  lb.addEventListener('touchend', function(e) {
    if (touchStartX === null) return;
    var dx = e.changedTouches[0].clientX - touchStartX;
    if (Math.abs(dx) > 40) { dx < 0 ? lightboxNext() : lightboxPrev(); }
    touchStartX = null;
  });
})();
</script>
