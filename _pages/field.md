---
layout: single
title: "In the Field"
permalink: /field/
author_profile: true
---

<style>.page__title { display: none; }</style>

<div class="field-tabs">
  <div class="field-tabs__sticky">
    <h1 class="field-tabs__title">In the Field</h1>
    <nav class="field-tabs__nav">
      <button class="field-tabs__btn active" data-tab="liberia">Field Research in Liberia</button>
      <button class="field-tabs__btn" data-tab="cambridge">Field Research in Cambridge University Hospitals</button>
    </nav>
  </div>

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
    </div>

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
  </div>

  <div class="field-tabs__panel" id="tab-cambridge"><p>Coming soon.</p></div>
</div>

<div class="field-lightbox" id="field-lightbox" onclick="closeLightbox()">
  <button class="field-lightbox__close" onclick="closeLightbox()">&times;</button>
  <img id="field-lightbox-img" src="" alt="" onclick="event.stopPropagation()" />
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
