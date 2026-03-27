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

Coming soon.

  </div>

  <div class="field-tabs__panel" id="tab-cambridge">

Coming soon.

  </div>
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
</script>
