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
    <p>The goal is to develop evidence-based knowledge and tools leveraging modern analytical methods for improving the effectiveness of perinatal health delivery systems.</p>
    <p>I visited Liberia in July, 2025.</p>
    <p>Implementation Tools: I and our team have developed two related tools to facilitate the implementation of this research by practitioners at both individual and population health levels. During the fieldwork, our team led a two-day workshop.</p>

    <div class="field-gallery-wrap">
      <div class="field-gallery" id="liberia-gallery">
        <div class="field-gallery__item" onclick="openLightbox('/images/Liberia/workshop.JPG')">
          <img src="/images/Liberia/workshop.JPG" alt="Workshop in Liberia" />
          <div class="field-gallery__caption"></div>
        </div>
        <div class="field-gallery__item" onclick="openLightbox('/images/Liberia/CHT.JPG')">
          <img src="/images/Liberia/CHT.JPG" alt="CHT Liberia" />
          <div class="field-gallery__caption"></div>
        </div>
        <div class="field-gallery__item" onclick="openLightbox('/images/Liberia/CA_map.png')">
          <img src="/images/Liberia/CA_map.png" alt="CA Map" />
          <div class="field-gallery__caption"></div>
        </div>
        <div class="field-gallery__item" onclick="openLightbox('/images/Liberia/MWH_1.png')">
          <img src="/images/Liberia/MWH_1.png" alt="MWH" />
          <div class="field-gallery__caption"></div>
        </div>
        <div class="field-gallery__item" onclick="openLightbox('/images/Liberia/room.png')">
          <img src="/images/Liberia/room.png" alt="Room" />
          <div class="field-gallery__caption"></div>
        </div>
      </div>
      <div class="field-gallery-controls">
        <button class="field-gallery-arrow" onclick="galleryScroll('liberia-gallery', -1)">&#9664;</button>
        <div class="field-gallery-track" id="liberia-track" onclick="galleryTrackClick(event, 'liberia-gallery')">
          <div class="field-gallery-thumb" id="liberia-thumb"></div>
        </div>
        <button class="field-gallery-arrow" onclick="galleryScroll('liberia-gallery', 1)">&#9654;</button>
      </div>
    </div>

    <p><strong>Two Implementation Tools</strong></p>

    <div class="field-accordion">

      <div class="field-accordion__item">
        <div class="field-accordion__header" onclick="toggleAccordion(this)">
          <span class="field-accordion__arrow open">&#9658;</span>
          <span>Tool 1: Skilled Birth Assistance (SBA) Wheel</span>
        </div>
        <div class="field-accordion__body open">
          <p>For the local clinic (individual) level, we have designed and manufactured a cardboard-based device to facilitate the calculation by nurses of the BBA risks facing individual patients, and discussion of potential interventions to mitigate them, during their antenatal consultations. This device also quantifies the reduction of BBA risk associated with potential MWH stays of different lengths, and may thus facilitate (i) the promotion of MWHs as a perinatal health intervention; and (ii) the implementation of the optimal egalitarian MWH assignment policy derived as part of our analysis.</p>
        </div>
      </div>

      <div class="field-accordion__item">
        <div class="field-accordion__header" onclick="toggleAccordion(this)">
          <span class="field-accordion__arrow">&#9658;</span>
          <span>Tool 2: Artemis Unassisted Birth Risk Mapping System</span>
        </div>
        <div class="field-accordion__body">
          <p>For the national or regional (population) health administration level, we have coordinated the development of an open-access, web-based software to map and analyze birth rate, HF network and BBA risk in order to (i) identify communities facing the highest risks of BBAs and prioritize related health interventions accordingly; (ii) evaluate, generate and disseminate data-driven MWH assignment policies; and (iii) inform capacity management and facility location decisions in MWH facility networks.</p>
        </div>
      </div>

    </div>
  </div>

  <div class="field-tabs__panel" id="tab-cambridge">
    Coming soon.
  </div>
</div>

<div class="field-lightbox" id="field-lightbox" onclick="closeLightbox()">
  <button class="field-lightbox__close" onclick="closeLightbox()">&times;</button>
  <img id="field-lightbox-img" src="" alt="" onclick="event.stopPropagation()" />
</div>

<script>
(function () {
  var buttons = document.querySelectorAll('.field-tabs__btn');
  var panels  = document.querySelectorAll('.field-tabs__panel');
  buttons.forEach(function (btn) {
    btn.addEventListener('click', function () {
      buttons.forEach(function (b) { b.classList.remove('active'); });
      panels.forEach(function (p) { p.classList.remove('active'); });
      btn.classList.add('active');
      document.getElementById('tab-' + btn.dataset.tab).classList.add('active');
    });
  });

  // Init gallery scrollbar thumbs
  ['liberia'].forEach(function(id) {
    var gallery = document.getElementById(id + '-gallery');
    if (gallery) {
      gallery.addEventListener('scroll', function() { updateThumb(id); });
      updateThumb(id);
    }
  });
})();

function updateThumb(id) {
  var gallery = document.getElementById(id + '-gallery');
  var thumb   = document.getElementById(id + '-thumb');
  if (!gallery || !thumb) return;
  var ratio    = gallery.clientWidth / gallery.scrollWidth;
  var leftFrac = gallery.scrollLeft / (gallery.scrollWidth - gallery.clientWidth);
  var track    = thumb.parentElement;
  thumb.style.width = (ratio * track.clientWidth) + 'px';
  thumb.style.left  = (leftFrac * (track.clientWidth - thumb.offsetWidth)) + 'px';
}

function galleryScroll(id, dir) {
  var gallery = document.getElementById(id);
  if (gallery) gallery.scrollBy({ left: dir * 280, behavior: 'smooth' });
}

function galleryTrackClick(e, id) {
  var gallery = document.getElementById(id);
  var track   = e.currentTarget;
  var frac    = e.offsetX / track.clientWidth;
  gallery.scrollLeft = frac * (gallery.scrollWidth - gallery.clientWidth);
}

function toggleAccordion(header) {
  var arrow = header.querySelector('.field-accordion__arrow');
  var body  = header.nextElementSibling;
  arrow.classList.toggle('open');
  body.classList.toggle('open');
}

function openLightbox(src) {
  document.getElementById('field-lightbox-img').src = src;
  document.getElementById('field-lightbox').classList.add('open');
}

function closeLightbox() {
  document.getElementById('field-lightbox').classList.remove('open');
}

document.addEventListener('keydown', function(e) {
  if (e.key === 'Escape') closeLightbox();
});
</script>
