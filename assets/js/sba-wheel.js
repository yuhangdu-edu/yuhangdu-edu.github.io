(function () {
  var canvas = document.getElementById('sbaCanvas');
  if (!canvas) return;
  var ctx = canvas.getContext('2d');
  if (!ctx) return;

  // ── DATA ──────────────────────────────────────────────────────────────
  var LABELS = [
    '0\u20131h','1\u20132h','2\u20133h','3\u20133.5h','3.5\u20134h',
    '4\u20134.5h','4.5\u20135h','5\u20135.5h','5.5\u20136h','6\u20136.5h',
    '6.5\u20137h','7\u20137.5h','7.5\u20138h','8\u20138.5h','8.5\u20139h',
    '9\u20139.5h','9.5\u201310h','10\u201310.5h','10.5\u201311h',
    '11\u201311.5h','11.5\u201312h','12+h'
  ];
  var WIN_LABELS = ['No MWH Stay', '0 Wks', '1 Wk', '2 Wks', '3 Wks', '4 Wks'];
  var N = 22;

  var NULI = [
    [.96,.98,.99,.99,.99,.99],[.92,.96,.98,.99,.99,.99],[.86,.92,.96,.99,.99,.99],
    [.82,.91,.95,.98,.99,.99],[.78,.89,.95,.97,.99,.99],[.74,.87,.94,.97,.98,.99],
    [.70,.85,.93,.97,.98,.99],[.66,.82,.92,.96,.98,.99],[.62,.80,.91,.96,.98,.99],
    [.58,.78,.90,.95,.98,.99],[.54,.76,.89,.95,.98,.99],[.50,.74,.88,.95,.97,.99],
    [.46,.72,.87,.94,.97,.99],[.42,.70,.86,.94,.97,.99],[.39,.69,.85,.94,.97,.99],
    [.36,.67,.85,.93,.97,.99],[.33,.66,.84,.93,.97,.99],[.30,.64,.83,.93,.97,.99],
    [.28,.63,.83,.92,.96,.99],[.26,.62,.82,.92,.96,.99],[.24,.61,.82,.92,.96,.99],
    [.22,.60,.81,.92,.96,.99]
  ];
  var MULTI = [
    [.93,.96,.98,.99,.99,.99],[.82,.91,.95,.98,.99,.99],[.69,.84,.92,.96,.98,.99],
    [.62,.80,.91,.96,.98,.99],[.56,.77,.89,.95,.98,.99],[.50,.74,.88,.95,.97,.99],
    [.44,.71,.87,.94,.97,.99],[.39,.69,.85,.94,.97,.99],[.35,.66,.84,.93,.97,.99],
    [.30,.64,.83,.93,.97,.99],[.26,.62,.82,.92,.96,.99],[.23,.60,.81,.92,.96,.99],
    [.19,.59,.81,.92,.96,.99],[.16,.57,.80,.91,.96,.99],[.14,.56,.79,.91,.96,.99],
    [.12,.55,.79,.91,.96,.99],[.10,.54,.78,.91,.96,.99],[.08,.53,.78,.90,.96,.99],
    [.06,.52,.78,.90,.95,.99],[.05,.51,.77,.90,.95,.99],[.04,.51,.77,.90,.95,.99],
    [.03,.51,.77,.90,.95,.99]
  ];

  // ── COLOURS ───────────────────────────────────────────────────────────
  // Layer 2: light blue/purple uniform cells, red numbers (matching physical device)
  // Layer 1: distinctly darker blue/purple wedge (matching physical device)
  var THEME = {
    nulliparous: {
      cellBg:   '#bdd9ec',   // light blue data cells (layer 2)
      cellSel:  '#a3c8e0',   // selected sector slightly darker
      ringText: '#1b5e8c',   // outer ring label text
      wedge:    '#5a96c5',   // medium blue wedge (layer 1) – clearly darker than cells
      wedgeBorder: '#3a76a5',
      arrow:    '#0d3d6b',
      centerFg: '#1b5e8c'
    },
    multiparous: {
      cellBg:   '#cfc5e8',
      cellSel:  '#baaeda',
      ringText: '#4b2d8c',
      wedge:    '#7b5ea7',
      wedgeBorder: '#5b3e87',
      arrow:    '#3a1a6e',
      centerFg: '#4b2d8c'
    }
  };
  var CELL_RED = '#cc0000';

  // ── GEOMETRY (600 × 600) ──────────────────────────────────────────────
  var W      = 600;
  var CX     = 300, CY = 300;
  var R_OUT  = 292;   // outer edge of label ring
  var R_LABEL= 256;   // inner edge of label ring / outer edge of data rings
  var RING_W = 34;    // 6 data rings × 34 = 204 px = R_LABEL − R_CTR
  var R_CTR  = 52;    // centre knob
  var ASTEP  = (2 * Math.PI) / N;
  var A0     = -Math.PI / 2;
  // Wedge: left edge at needle − half sector, spans 8 sectors clockwise
  var WEDGE_SPAN = ASTEP * 8;

  function secAngles(i) {
    var a0 = A0 + i * ASTEP;
    return { a0: a0, a1: a0 + ASTEP, mid: a0 + ASTEP / 2 };
  }
  function arcSector(c, ri, ro, a0, a1) {
    c.beginPath();
    c.arc(CX, CY, ro, a0, a1);
    c.arc(CX, CY, ri, a1, a0, true);
    c.closePath();
  }

  // ── STATE ─────────────────────────────────────────────────────────────
  var parity      = 'nulliparous';
  var selected    = 0;
  var needleAngle = secAngles(0).mid;
  var isDragging  = false;

  canvas.width  = W;
  canvas.height = W;

  // ── MAIN DRAW ─────────────────────────────────────────────────────────
  function drawWheel() {
    var data  = parity === 'nulliparous' ? NULI : MULTI;
    var theme = THEME[parity];
    ctx.clearRect(0, 0, W, W);

    // ── LAYER 2: fixed lower data disc ───────────────────────────────

    // Background
    ctx.beginPath();
    ctx.arc(CX, CY, R_OUT, 0, 2 * Math.PI);
    ctx.fillStyle = '#e4f1f9';
    ctx.fill();

    // 22 × 6 light-blue cells (uniform, no traffic-light coding)
    for (var i = 0; i < N; i++) {
      var ang = secAngles(i);
      for (var j = 0; j < 6; j++) {
        arcSector(ctx,
          R_LABEL - (j + 1) * RING_W,
          R_LABEL - j * RING_W,
          ang.a0, ang.a1);
        ctx.fillStyle = (i === selected) ? theme.cellSel : theme.cellBg;
        ctx.fill();
      }
    }

    // Red numbers in every cell
    for (var i = 0; i < N; i++) {
      var ang  = secAngles(i);
      for (var j = 0; j < 6; j++) {
        var rMid = R_LABEL - j * RING_W - RING_W / 2;
        ctx.save();
        ctx.translate(CX + rMid * Math.cos(ang.mid),
                      CY + rMid * Math.sin(ang.mid));
        ctx.rotate(ang.mid + Math.PI / 2);
        ctx.fillStyle    = CELL_RED;
        ctx.font         = 'bold ' + (j < 3 ? '12' : '11') + 'px sans-serif';
        ctx.textAlign    = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(Math.round(data[i][j] * 100), 0, 0);
        ctx.restore();
      }
    }

    // White grid lines
    for (var k = 0; k <= 6; k++) {
      ctx.beginPath();
      ctx.arc(CX, CY, R_LABEL - k * RING_W, 0, 2 * Math.PI);
      ctx.strokeStyle = 'rgba(255,255,255,0.9)'; ctx.lineWidth = 1.5; ctx.stroke();
    }
    for (var i = 0; i < N; i++) {
      var a = A0 + i * ASTEP;
      ctx.beginPath();
      ctx.moveTo(CX + R_CTR  * Math.cos(a), CY + R_CTR  * Math.sin(a));
      ctx.lineTo(CX + R_OUT  * Math.cos(a), CY + R_OUT  * Math.sin(a));
      ctx.strokeStyle = 'rgba(255,255,255,0.9)'; ctx.lineWidth = 1.5; ctx.stroke();
    }

    // Outer label ring – white, tint selected sector
    for (var i = 0; i < N; i++) {
      var ang = secAngles(i);
      arcSector(ctx, R_LABEL, R_OUT, ang.a0, ang.a1);
      ctx.fillStyle = (i === selected) ? '#d4eaf7' : '#ffffff';
      ctx.fill();
    }
    ctx.beginPath(); ctx.arc(CX, CY, R_OUT,   0, 2 * Math.PI);
    ctx.strokeStyle = theme.ringText; ctx.lineWidth = 1.5; ctx.stroke();
    ctx.beginPath(); ctx.arc(CX, CY, R_LABEL, 0, 2 * Math.PI);
    ctx.strokeStyle = 'rgba(255,255,255,0.8)'; ctx.lineWidth = 1; ctx.stroke();

    // Time labels
    for (var i = 0; i < N; i++) {
      var ang  = secAngles(i);
      var rMid = (R_LABEL + R_OUT) / 2;
      ctx.save();
      ctx.translate(CX + rMid * Math.cos(ang.mid),
                    CY + rMid * Math.sin(ang.mid));
      ctx.rotate(ang.mid + Math.PI / 2);
      ctx.fillStyle    = theme.ringText;
      ctx.font         = (i === selected ? 'bold 9.5px' : '8.5px') + ' sans-serif';
      ctx.textAlign    = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(LABELS[i], 0, 0);
      ctx.restore();
    }

    // ── LAYER 1: rotating wedge ───────────────────────────────────────
    drawWedge(theme, data);

    // Arrow in outer ring (marks selected sector)
    drawArrow(theme);

    // Centre knob
    ctx.beginPath(); ctx.arc(CX, CY, R_CTR, 0, 2 * Math.PI);
    ctx.fillStyle = '#fff'; ctx.fill();
    ctx.strokeStyle = theme.centerFg; ctx.lineWidth = 3; ctx.stroke();
    ctx.fillStyle    = theme.centerFg;
    ctx.font         = 'bold 10px sans-serif';
    ctx.textAlign    = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText('P(SBA)', CX, CY - 8);
    ctx.font = '9px sans-serif';
    ctx.fillText(parity === 'nulliparous' ? 'Nulliparous' : 'Multiparous', CX, CY + 8);
  }

  // ── LAYER 1 wedge ─────────────────────────────────────────────────────
  function drawWedge(theme, data) {
    // 1. Build wedge on offscreen canvas, punch window holes
    var off = document.createElement('canvas');
    off.width = W; off.height = W;
    var oc = off.getContext('2d');

    var wL = needleAngle - ASTEP / 2;
    var wR = wL + WEDGE_SPAN;

    arcSector(oc, R_CTR, R_LABEL, wL, wR);
    oc.fillStyle = theme.wedge;
    oc.fill();

    oc.globalCompositeOperation = 'destination-out';
    var hA = ASTEP * 0.45;
    for (var j = 0; j < 6; j++) {
      var ro = R_LABEL - j * RING_W - 2;
      var ri = Math.max(R_LABEL - (j + 1) * RING_W + 2, R_CTR + 3);
      arcSector(oc, ri, ro, needleAngle - hA, needleAngle + hA);
      oc.fill();
    }

    ctx.drawImage(off, 0, 0);

    // 2. Wedge outline and internal ring dividers
    arcSector(ctx, R_CTR, R_LABEL, wL, wR);
    ctx.strokeStyle = theme.wedgeBorder; ctx.lineWidth = 1.5; ctx.stroke();
    for (var k = 1; k < 6; k++) {
      ctx.beginPath();
      ctx.arc(CX, CY, R_LABEL - k * RING_W, wL, wR);
      ctx.strokeStyle = 'rgba(255,255,255,0.5)'; ctx.lineWidth = 0.75; ctx.stroke();
    }

    // 3. White value box in each window + "%" label + scenario label
    for (var j = 0; j < 6; j++) {
      var rMid = R_LABEL - j * RING_W - RING_W / 2;
      var pct  = Math.round(data[selected][j] * 100);

      // ── White box at needle angle ──
      var bx = CX + rMid * Math.cos(needleAngle);
      var by = CY + rMid * Math.sin(needleAngle);
      var bW = RING_W * 0.72, bH = RING_W * 0.62;

      ctx.save();
      ctx.translate(bx, by);
      ctx.rotate(needleAngle + Math.PI / 2);
      ctx.fillStyle = '#ffffff';
      ctx.strokeStyle = 'rgba(0,0,0,0.2)';
      ctx.lineWidth = 0.5;
      ctx.beginPath();
      if (ctx.roundRect) {
        ctx.roundRect(-bW / 2, -bH / 2, bW, bH, 2);
      } else {
        ctx.rect(-bW / 2, -bH / 2, bW, bH);
      }
      ctx.fill(); ctx.stroke();
      ctx.fillStyle    = CELL_RED;
      ctx.font         = 'bold ' + Math.round(RING_W * 0.38) + 'px sans-serif';
      ctx.textAlign    = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(pct, 0, 0);
      ctx.restore();

      // ── "%" just clockwise of the box ──
      var pctA = needleAngle + hA + 0.04;
      ctx.save();
      ctx.translate(CX + rMid * Math.cos(pctA), CY + rMid * Math.sin(pctA));
      ctx.rotate(pctA + Math.PI / 2);
      ctx.fillStyle    = CELL_RED;
      ctx.font         = Math.round(RING_W * 0.28) + 'px sans-serif';
      ctx.textAlign    = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText('%', 0, 0);
      ctx.restore();

      // ── Scenario label inside wedge (diagonal cascade) ──
      // Each label steps 1 sector further clockwise as we go to inner rings,
      // recreating the diagonal arrangement of the physical device
      var lblA = needleAngle + ASTEP * (1.5 + j * 0.9);
      ctx.save();
      ctx.translate(CX + rMid * Math.cos(lblA), CY + rMid * Math.sin(lblA));
      ctx.rotate(lblA + Math.PI / 2);
      ctx.fillStyle    = 'rgba(255,255,255,0.92)';
      ctx.font         = 'bold ' + Math.round(RING_W * 0.29) + 'px sans-serif';
      ctx.textAlign    = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(WIN_LABELS[j], 0, 0);
      ctx.restore();
    }
  }

  // Arrow in outer label ring pointing toward selected sector
  function drawArrow(theme) {
    var angle = needleAngle;
    var tipR  = R_OUT - 3;
    var baseR = R_LABEL + 4;
    var hW    = ASTEP * 0.38;
    ctx.beginPath();
    ctx.moveTo(CX + tipR  * Math.cos(angle),      CY + tipR  * Math.sin(angle));
    ctx.lineTo(CX + baseR * Math.cos(angle - hW), CY + baseR * Math.sin(angle - hW));
    ctx.lineTo(CX + baseR * Math.cos(angle + hW), CY + baseR * Math.sin(angle + hW));
    ctx.closePath();
    ctx.fillStyle   = theme.arrow; ctx.fill();
    ctx.strokeStyle = '#fff'; ctx.lineWidth = 1.5; ctx.stroke();
  }

  // ── INTERACTION ────────────────────────────────────────────────────────
  function angleToSector(a) {
    var norm = ((a - A0) % (2 * Math.PI) + 2 * Math.PI) % (2 * Math.PI);
    return Math.max(0, Math.min(N - 1, Math.floor(norm / ASTEP)));
  }
  function dist(x, y) {
    return Math.sqrt((x - CX) * (x - CX) + (y - CY) * (y - CY));
  }
  function ptAngle(x, y) { return Math.atan2(y - CY, x - CX); }
  function canvasXY(e) {
    var rect = canvas.getBoundingClientRect();
    var src  = e.touches ? e.touches[0] : e;
    return {
      x: (src.clientX - rect.left) * (W / rect.width),
      y: (src.clientY - rect.top)  * (W / rect.height)
    };
  }
  function snapNeedle(a) {
    var idx     = angleToSector(a);
    needleAngle = secAngles(idx).mid;
    selected    = idx;
    drawWheel();
  }

  canvas.addEventListener('mousedown', function (e) {
    var p = canvasXY(e), d = dist(p.x, p.y);
    if (d > R_OUT) return;
    if (d > R_LABEL) { snapNeedle(ptAngle(p.x, p.y)); }
    else { isDragging = true; canvas.style.cursor = 'grabbing'; }
  });
  document.addEventListener('mousemove', function (e) {
    if (!isDragging) return;
    var p = canvasXY(e);
    needleAngle = ptAngle(p.x, p.y);
    var idx = angleToSector(needleAngle);
    if (idx !== selected) selected = idx;
    drawWheel();
  });
  document.addEventListener('mouseup', function () {
    if (!isDragging) return;
    isDragging = false; canvas.style.cursor = 'grab';
    snapNeedle(needleAngle);
  });
  canvas.addEventListener('touchstart', function (e) {
    e.preventDefault();
    if (dist(canvasXY(e).x, canvasXY(e).y) <= R_OUT) isDragging = true;
  }, { passive: false });
  canvas.addEventListener('touchmove', function (e) {
    e.preventDefault();
    if (!isDragging) return;
    var p = canvasXY(e);
    needleAngle = ptAngle(p.x, p.y);
    var idx = angleToSector(needleAngle);
    if (idx !== selected) selected = idx;
    drawWheel();
  }, { passive: false });
  canvas.addEventListener('touchend', function () {
    if (!isDragging) return;
    isDragging = false; snapNeedle(needleAngle);
  });

  // ── PARITY SWITCH ──────────────────────────────────────────────────────
  var switchBtn = document.getElementById('sbaSwitchBtn');
  if (switchBtn) {
    switchBtn.addEventListener('click', function () {
      parity = parity === 'nulliparous' ? 'multiparous' : 'nulliparous';
      var nameEl = document.getElementById('sbaParityName');
      if (nameEl) nameEl.textContent = parity === 'nulliparous' ? 'Nulliparous' : 'Multiparous';
      this.textContent = parity === 'nulliparous' ? 'Switch to Multiparous' : 'Switch to Nulliparous';
      drawWheel();
    });
  }

  // ── INIT ───────────────────────────────────────────────────────────────
  canvas.style.cursor = 'grab';
  drawWheel();
})();
