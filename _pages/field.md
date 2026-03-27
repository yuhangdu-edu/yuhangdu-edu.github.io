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

    <div class="field-gallery">
      <div class="field-gallery__item" onclick="openLightbox('/images/Liberia/workshop.JPG')">
        <img src="/images/Liberia/workshop.JPG" alt="Workshop in Liberia" />
      </div>
      <div class="field-gallery__item" onclick="openLightbox('/images/Liberia/CHT.JPG')">
        <img src="/images/Liberia/CHT.JPG" alt="CHT Liberia" />
      </div>
    </div>

    <p><strong>Two Implementation Tools</strong></p>
    <p>For the local clinic (individual) level, we have designed and manufactured a cardboard-based device to facilitate the calculation by nurses of the BBA risks facing individual patients, and discussion of potential interventions to mitigate them, during their antenatal consultations. This device also quantifies the reduction of BBA risk associated with potential MWH stays of different lengths, and may thus facilitate (i) the promotion of MWHs as a perinatal health intervention; and (ii) the implementation of the optimal egalitarian MWH assignment policy derived as part of our analysis.</p>
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
})();

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
