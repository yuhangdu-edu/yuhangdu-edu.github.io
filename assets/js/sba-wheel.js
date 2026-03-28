(function () {
  var canvas = document.getElementById('sbaCanvas');
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  if (!ctx) return;

  // ── GEOMETRY ──────────────────────────────────────────────────────────
  var W = 2400, CX = 1200, CY = 1200, R_OUT = 1168;
  var N = 22, ASTEP = (2 * Math.PI) / N, A0 = -Math.PI / 2;

  // Angle of the arrow in the natural (unrotated) Layer 1 PNG.
  // Empirically measured: centroid of blue arrow pixels in layer1_nuli.png
  // relative to disc centre = -2.552613 rad (-146.3 deg)
  var DEFAULT_ANGLE = -2.552613;

  // ── STATE ─────────────────────────────────────────────────────────────
  var parity = 'nulliparous', selected = 18, isDragging = false;
  var cache = {};

  canvas.width = W;
  canvas.height = W;
  ctx.imageSmoothingEnabled = true;
  ctx.imageSmoothingQuality = 'high';

  // ── IMAGE LOADER ──────────────────────────────────────────────────────
  function loadImages(par, cb) {
    if (cache[par]) { cb(cache[par]); return; }
    var base = '/assets/images/sba-wheel/';
    var sfx  = par === 'nulliparous' ? 'nuli' : 'multi';
    var l2 = new Image(), l1 = new Image(), n = 0;
    function done() {
      if (++n === 2) { cache[par] = { l2: l2, l1: l1 }; cb(cache[par]); }
    }
    l2.onload = done; l1.onload = done;
    l2.onerror = l1.onerror = function() { console.error('SBA wheel image failed to load'); };
    l2.src = base + 'layer2_' + sfx + '.png';
    l1.src = base + 'layer1_' + sfx + '.png';
  }

  // ── DRAW ──────────────────────────────────────────────────────────────
  function drawWheel(imgs) {
    ctx.clearRect(0, 0, W, W);

    // Layer 2: static data disc
    ctx.drawImage(imgs.l2, 0, 0, W, W);

    // Layer 1: rotating wedge overlay
    // Rotate so the arrow (at DEFAULT_ANGLE in image space) aligns with
    // the left edge of the selected sector.
    var rotation = (A0 + selected * ASTEP + ASTEP / 2) - DEFAULT_ANGLE;
    ctx.save();
    ctx.translate(CX, CY);
    ctx.rotate(rotation);
    ctx.drawImage(imgs.l1, -W / 2, -W / 2, W, W);
    ctx.restore();
  }

  function render() { loadImages(parity, drawWheel); }

  // ── INTERACTION ────────────────────────────────────────────────────────
  function angleToSector(a) {
    var norm = ((a - A0) % (2 * Math.PI) + 2 * Math.PI) % (2 * Math.PI);
    return Math.max(0, Math.min(N - 1, Math.floor(norm / ASTEP)));
  }
  function distC(x, y) { return Math.sqrt((x - CX) * (x - CX) + (y - CY) * (y - CY)); }
  function ptAngle(x, y) { return Math.atan2(y - CY, x - CX); }
  function canvasXY(e) {
    var rect = canvas.getBoundingClientRect(), src = e.touches ? e.touches[0] : e;
    return { x: (src.clientX - rect.left) * (W / rect.width),
             y: (src.clientY - rect.top)  * (W / rect.height) };
  }

  function setFromAngle(a) {
    selected = angleToSector(a);
    render();
  }

  canvas.addEventListener('mousedown', function (e) {
    var p = canvasXY(e);
    if (distC(p.x, p.y) > R_OUT) return;
    isDragging = true;
    canvas.style.cursor = 'grabbing';
    setFromAngle(ptAngle(p.x, p.y));
  });
  document.addEventListener('mousemove', function (e) {
    if (!isDragging) return;
    var p = canvasXY(e);
    setFromAngle(ptAngle(p.x, p.y));
  });
  document.addEventListener('mouseup', function () {
    if (!isDragging) return;
    isDragging = false;
    canvas.style.cursor = 'grab';
  });
  canvas.addEventListener('touchstart', function (e) {
    e.preventDefault();
    var p = canvasXY(e);
    if (distC(p.x, p.y) <= R_OUT) { isDragging = true; setFromAngle(ptAngle(p.x, p.y)); }
  }, { passive: false });
  canvas.addEventListener('touchmove', function (e) {
    e.preventDefault();
    if (!isDragging) return;
    var p = canvasXY(e);
    setFromAngle(ptAngle(p.x, p.y));
  }, { passive: false });
  canvas.addEventListener('touchend', function () { isDragging = false; });

  // ── PARITY SWITCH ──────────────────────────────────────────────────────
  var switchBtn = document.getElementById('sbaSwitchBtn');
  if (switchBtn) {
    switchBtn.addEventListener('click', function () {
      parity = parity === 'nulliparous' ? 'multiparous' : 'nulliparous';
      var nameEl = document.getElementById('sbaParityName');
      if (nameEl) nameEl.textContent = parity === 'nulliparous' ? 'Nulliparous' : 'Multiparous';
      this.textContent = parity === 'nulliparous' ? 'Switch to Multiparous' : 'Switch to Nulliparous';
      render();
    });
  }

  // ── INIT ───────────────────────────────────────────────────────────────
  canvas.style.cursor = 'grab';
  render();
})();
