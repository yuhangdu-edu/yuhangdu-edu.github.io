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
  var N = 22;

  // Table 1 – Nulliparous [row = time interval, col = scenario]
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

  // Table 2 – Multiparous
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

  // ── COLOUR SCHEME (matching physical device) ──────────────────────────
  // Layer 2: uniform light-blue cells with red numbers – no traffic-light coding
  var THEME = {
    nulliparous: {
      cellBg: '#c2dff0',      // light blue data cells
      cellSel: '#a6cde6',     // slightly darker for selected sector
      ringText: '#1a5f8c',    // blue outer-ring labels
      wedge:  '#c2dff0',      // layer-1 wedge (same as cells)
      arrow:  '#0d3d6b',      // dark blue arrow
      border: '#8ab4ce',      // border lines
      centerFg: '#1a5f8c'
    },
    multiparous: {
      cellBg: '#d4c4eb',
      cellSel: '#bcacda',
      ringText: '#5c2d91',
      wedge:  '#d4c4eb',
      arrow:  '#3a1a6e',
      border: '#a68fc4',
      centerFg: '#5c2d91'
    }
  };
  var CELL_RED = '#cc0000'; // all numbers are red

  // ── GEOMETRY (600 × 600) ──────────────────────────────────────────────
  var W = 600;
  var CX = 300, CY = 300;
  // Layer 2 (lower wheel): outer ring R_CTR..R_OUT
  // Layer 1 (upper wheel/wedge): covers R_CTR..R_LABEL (data rings only)
  // Outer label ring (R_LABEL..R_OUT) is always visible – layer 2 is larger than layer 1
  var R_OUT   = 292;   // outer edge of label ring
  var R_LABEL = 256;   // inner edge of label ring = outer edge of data rings
  var RING_W  = 34;    // each of the 6 data rings (6 × 34 = 204 = R_LABEL − R_CTR)
  var R_CTR   = 52;    // centre knob radius
  var ASTEP   = (2 * Math.PI) / N;
  var A0      = -Math.PI / 2;

  // Layer-1 wedge spans 8 sectors; the ARROW is at the LEFT edge (needleAngle)
  // so the wedge extends ~8 sectors CLOCKWISE from the arrow direction.
  var WEDGE_SECTORS = 8;
  var WEDGE_SPAN    = ASTEP * WEDGE_SECTORS;

  function secAngles(i) {
    var a0 = A0 + i * ASTEP;
    return { a0: a0, a1: a0 + ASTEP, mid: a0 + ASTEP / 2 };
  }
  // Draw an annular sector on an arbitrary 2d context
  function arcSector(c, ri, ro, a0, a1) {
    c.beginPath();
    c.arc(CX, CY, ro, a0, a1);
    c.arc(CX, CY, ri, a1, a0, true);
    c.closePath();
  }

  // ── STATE ─────────────────────────────────────────────────────────────
  var parity   = 'nulliparous';
  var selected = 0;
  var needleAngle = secAngles(0).mid;
  var isDragging  = false;

  canvas.width  = W;
  canvas.height = W;

  // ── MAIN DRAW ─────────────────────────────────────────────────────────
  function drawWheel() {
    var data  = parity === 'nulliparous' ? NULI : MULTI;
    var theme = THEME[parity];
    ctx.clearRect(0, 0, W, W);

    // ── LAYER 2: lower data disc (always drawn in full) ───────────────

    // background disc
    ctx.beginPath();
    ctx.arc(CX, CY, R_OUT, 0, 2 * Math.PI);
    ctx.fillStyle = '#e8f4fb';
    ctx.fill();

    // 22 × 6 colour-coded data cells – uniform light blue, no traffic-light
    for (var i = 0; i < N; i++) {
      var ang = secAngles(i);
      for (var j = 0; j < 6; j++) {
        arcSector(ctx, R_LABEL - (j + 1) * RING_W, R_LABEL - j * RING_W,
                  ang.a0, ang.a1);
        ctx.fillStyle = (i === selected) ? theme.cellSel : theme.cellBg;
        ctx.fill();
      }
    }

    // red numbers in each data cell
    for (var i = 0; i < N; i++) {
      var ang = secAngles(i);
      for (var j = 0; j < 6; j++) {
        var ro   = R_LABEL - j * RING_W;
        var rMid = ro - RING_W / 2;
        var px   = CX + rMid * Math.cos(ang.mid);
        var py   = CY + rMid * Math.sin(ang.mid);
        ctx.save();
        ctx.translate(px, py);
        ctx.rotate(ang.mid + Math.PI / 2);
        ctx.fillStyle = CELL_RED;
        ctx.font = 'bold ' + (j < 3 ? '12' : '11') + 'px sans-serif';
        ctx.textAlign    = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(Math.round(data[i][j] * 100), 0, 0);
        ctx.restore();
      }
    }

    // white cell borders (concentric rings)
    for (var k = 0; k <= 6; k++) {
      ctx.beginPath();
      ctx.arc(CX, CY, R_LABEL - k * RING_W, 0, 2 * Math.PI);
      ctx.strokeStyle = 'rgba(255,255,255,0.85)';
      ctx.lineWidth   = 1.5;
      ctx.stroke();
    }
    // white radial spokes
    for (var i = 0; i < N; i++) {
      var a = A0 + i * ASTEP;
      ctx.beginPath();
      ctx.moveTo(CX + R_CTR  * Math.cos(a), CY + R_CTR  * Math.sin(a));
      ctx.lineTo(CX + R_OUT  * Math.cos(a), CY + R_OUT  * Math.sin(a));
      ctx.strokeStyle = 'rgba(255,255,255,0.85)';
      ctx.lineWidth   = 1.5;
      ctx.stroke();
    }

    // outer label ring – white background; tint the selected sector
    for (var i = 0; i < N; i++) {
      var ang = secAngles(i);
      arcSector(ctx, R_LABEL, R_OUT, ang.a0, ang.a1);
      ctx.fillStyle = (i === selected) ? '#ddeef7' : '#ffffff';
      ctx.fill();
    }
    // outer ring border
    ctx.beginPath(); ctx.arc(CX, CY, R_OUT,   0, 2 * Math.PI);
    ctx.strokeStyle = theme.border; ctx.lineWidth = 2; ctx.stroke();
    ctx.beginPath(); ctx.arc(CX, CY, R_LABEL, 0, 2 * Math.PI);
    ctx.strokeStyle = 'rgba(255,255,255,0.85)'; ctx.lineWidth = 1.5; ctx.stroke();

    // time labels in outer ring
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

    // ── LAYER 1: rotating wedge with 6 window holes ───────────────────
    drawWedge(theme);

    // arrow indicator (in the outer label ring, at the needle angle)
    drawArrow(theme);

    // centre knob
    ctx.beginPath(); ctx.arc(CX, CY, R_CTR, 0, 2 * Math.PI);
    ctx.fillStyle   = '#fff'; ctx.fill();
    ctx.strokeStyle = theme.centerFg; ctx.lineWidth = 3; ctx.stroke();
    ctx.fillStyle    = theme.centerFg;
    ctx.font         = 'bold 10px sans-serif';
    ctx.textAlign    = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('P(SBA)', CX, CY - 8);
    ctx.font = '9px sans-serif';
    ctx.fillText(parity === 'nulliparous' ? 'Nulliparous' : 'Multiparous', CX, CY + 8);
  }

  // ── LAYER 1: wedge ────────────────────────────────────────────────────
  // The wedge starts at (needleAngle − ASTEP/2) and extends WEDGE_SPAN clockwise.
  // The 6 window holes are cut at the needle angle (left edge of wedge),
  // one per concentric data ring, matching the selected sector's cells.
  function drawWedge(theme) {
    var off = document.createElement('canvas');
    off.width = W; off.height = W;
    var oc = off.getContext('2d');

    // Wedge boundaries
    var wL = needleAngle - ASTEP / 2;           // left edge (where arrow is)
    var wR = wL + WEDGE_SPAN;                    // right edge

    // Solid wedge (data-ring area only; outer label ring stays exposed)
    arcSector(oc, R_CTR, R_LABEL, wL, wR);
    oc.fillStyle = theme.wedge;
    oc.fill();

    // Punch 6 transparent window holes at the needle angle
    oc.globalCompositeOperation = 'destination-out';
    var hA = ASTEP * 0.46;                       // half-angle of each window
    for (var j = 0; j < 6; j++) {
      var ro = R_LABEL - j * RING_W - 2;
      var ri = Math.max(R_LABEL - (j + 1) * RING_W + 2, R_CTR + 3);
      arcSector(oc, ri, ro, needleAngle - hA, needleAngle + hA);
      oc.fill();
    }

    // Blit onto main canvas
    ctx.drawImage(off, 0, 0);

    // Draw wedge outline and internal ring dividers on main canvas
    arcSector(ctx, R_CTR, R_LABEL, wL, wR);
    ctx.strokeStyle = theme.border; ctx.lineWidth = 1.5; ctx.stroke();

    for (var k = 1; k < 6; k++) {
      var r = R_LABEL - k * RING_W;
      ctx.beginPath();
      ctx.arc(CX, CY, r, wL, wR);
      ctx.strokeStyle = 'rgba(255,255,255,0.7)'; ctx.lineWidth = 1; ctx.stroke();
    }
  }

  // Arrow sits in the outer label ring pointing outward – marks the selected sector
  function drawArrow(theme) {
    var angle = needleAngle;
    var tipR  = R_OUT - 3;
    var baseR = R_LABEL + 4;
    var hW    = ASTEP * 0.38;
    ctx.beginPath();
    ctx.moveTo(CX + tipR  * Math.cos(angle),       CY + tipR  * Math.sin(angle));
    ctx.lineTo(CX + baseR * Math.cos(angle - hW),  CY + baseR * Math.sin(angle - hW));
    ctx.lineTo(CX + baseR * Math.cos(angle + hW),  CY + baseR * Math.sin(angle + hW));
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
    var idx = angleToSector(a);
    needleAngle = secAngles(idx).mid;
    selected    = idx;
    drawWheel();
  }

  canvas.addEventListener('mousedown', function (e) {
    var p = canvasXY(e);
    var d = dist(p.x, p.y);
    if (d > R_OUT) return;
    if (d > R_LABEL) {
      snapNeedle(ptAngle(p.x, p.y));  // click on outer ring → snap
    } else {
      isDragging = true;
      canvas.style.cursor = 'grabbing';
    }
  });
  document.addEventListener('mousemove', function (e) {
    if (!isDragging) return;
    var p = canvasXY(e);
    needleAngle = ptAngle(p.x, p.y);
    var idx = angleToSector(needleAngle);
    if (idx !== selected) { selected = idx; }
    drawWheel();
  });
  document.addEventListener('mouseup', function () {
    if (!isDragging) return;
    isDragging = false;
    canvas.style.cursor = 'grab';
    snapNeedle(needleAngle);
  });
  canvas.addEventListener('touchstart', function (e) {
    e.preventDefault();
    var p = canvasXY(e);
    if (dist(p.x, p.y) <= R_OUT) { isDragging = true; }
  }, { passive: false });
  canvas.addEventListener('touchmove', function (e) {
    e.preventDefault();
    if (!isDragging) return;
    var p = canvasXY(e);
    needleAngle = ptAngle(p.x, p.y);
    var idx = angleToSector(needleAngle);
    if (idx !== selected) { selected = idx; }
    drawWheel();
  }, { passive: false });
  canvas.addEventListener('touchend', function () {
    if (!isDragging) return;
    isDragging = false;
    snapNeedle(needleAngle);
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
