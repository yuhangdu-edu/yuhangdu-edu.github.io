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
  var SCENARIOS = [
    'No MWH stay',
    'Move to MWH on EDD',
    'Move 1 wk before EDD',
    'Move 2 wks before EDD',
    'Move 3 wks before EDD',
    'Move 4 wks before EDD'
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

  // ── COLORS ────────────────────────────────────────────────────────────
  var THEME = {
    nulliparous: { ring: '#2f7f93', center: '#2f7f93', needle: '#1a5060' },
    multiparous:  { ring: '#7b5ea7', center: '#7b5ea7', needle: '#4e3870' }
  };

  function cellBg(v) {
    if (v >= .95) return '#5a9a5a';
    if (v >= .90) return '#a8d8a8';
    return '#f4a0a0';
  }
  function cellFg(v) {
    if (v >= .95) return '#fff';
    if (v >= .90) return '#1a5c1a';
    return '#7a0000';
  }
  function lighten(hex, amt) {
    var r = parseInt(hex.slice(1,3),16);
    var g = parseInt(hex.slice(3,5),16);
    var b = parseInt(hex.slice(5,7),16);
    return 'rgb('+Math.round(r+(255-r)*amt)+','+Math.round(g+(255-g)*amt)+','+Math.round(b+(255-b)*amt)+')';
  }

  // ── GEOMETRY ──────────────────────────────────────────────────────────
  var CX = 240, CY = 240;
  var R_OUT = 234, R_LABEL = 205, RING_W = 27, R_CTR = 43;
  var ASTEP = (2 * Math.PI) / N;
  var A0 = -Math.PI / 2;

  function secAngles(i) {
    var a0 = A0 + i * ASTEP;
    return { a0: a0, a1: a0 + ASTEP, mid: a0 + ASTEP / 2 };
  }

  // ── STATE ─────────────────────────────────────────────────────────────
  var parity = 'nulliparous';
  var selected = 0;
  var needleAngle = secAngles(0).mid;
  var isDragging = false;

  // ── CANVAS SETUP ──────────────────────────────────────────────────────
  canvas.width = 480;
  canvas.height = 480;

  // ── DRAWING ───────────────────────────────────────────────────────────
  function annulus(ri, ro, a0, a1) {
    ctx.beginPath();
    ctx.arc(CX, CY, ro, a0, a1);
    ctx.arc(CX, CY, ri, a1, a0, true);
    ctx.closePath();
  }

  function drawWheel() {
    var data  = parity === 'nulliparous' ? NULI : MULTI;
    var theme = THEME[parity];
    ctx.clearRect(0, 0, 480, 480);

    // background disc
    ctx.beginPath();
    ctx.arc(CX, CY, R_OUT, 0, 2*Math.PI);
    ctx.fillStyle = '#f5f5f5';
    ctx.fill();

    // sectors
    for (var i = 0; i < N; i++) {
      var ang   = secAngles(i);
      var isSel = (i === selected);

      // label ring
      annulus(R_LABEL, R_OUT, ang.a0, ang.a1);
      ctx.fillStyle = isSel ? lighten(theme.ring, .35) : theme.ring;
      ctx.fill();

      // 6 data rings
      for (var j = 0; j < 6; j++) {
        var ro = R_LABEL - j * RING_W;
        var ri = ro - RING_W;
        var v  = data[i][j];
        annulus(ri, ro, ang.a0, ang.a1);
        ctx.fillStyle = isSel ? lighten(cellBg(v), .25) : cellBg(v);
        ctx.fill();
      }
    }

    // concentric borders
    for (var k = 0; k <= 6; k++) {
      ctx.beginPath();
      ctx.arc(CX, CY, R_LABEL - k*RING_W, 0, 2*Math.PI);
      ctx.strokeStyle = 'rgba(0,0,0,.2)';
      ctx.lineWidth = .5;
      ctx.stroke();
    }
    ctx.beginPath(); ctx.arc(CX,CY,R_OUT,0,2*Math.PI);
    ctx.strokeStyle='rgba(0,0,0,.3)'; ctx.lineWidth=1; ctx.stroke();
    ctx.beginPath(); ctx.arc(CX,CY,R_LABEL,0,2*Math.PI);
    ctx.strokeStyle='rgba(0,0,0,.3)'; ctx.lineWidth=1; ctx.stroke();

    // radial spokes
    for (var i = 0; i < N; i++) {
      var a = A0 + i * ASTEP;
      ctx.beginPath();
      ctx.moveTo(CX + R_CTR*Math.cos(a), CY + R_CTR*Math.sin(a));
      ctx.lineTo(CX + R_OUT*Math.cos(a),  CY + R_OUT*Math.sin(a));
      ctx.strokeStyle = 'rgba(0,0,0,.2)'; ctx.lineWidth = .5; ctx.stroke();
    }

    // numbers in data cells
    for (var i = 0; i < N; i++) {
      var ang = secAngles(i);
      for (var j = 0; j < 6; j++) {
        var ro   = R_LABEL - j * RING_W;
        var rMid = ro - RING_W / 2;
        var v    = data[i][j];
        var px   = CX + rMid * Math.cos(ang.mid);
        var py   = CY + rMid * Math.sin(ang.mid);
        ctx.save();
        ctx.translate(px, py);
        ctx.rotate(ang.mid + Math.PI / 2);
        ctx.fillStyle = cellFg(v);
        ctx.font = 'bold ' + (j < 3 ? '9' : '8') + 'px sans-serif';
        ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.fillText(Math.round(v * 100), 0, 0);
        ctx.restore();
      }
    }

    // time labels in label ring
    for (var i = 0; i < N; i++) {
      var ang  = secAngles(i);
      var rMid = (R_LABEL + R_OUT) / 2;
      var px   = CX + rMid * Math.cos(ang.mid);
      var py   = CY + rMid * Math.sin(ang.mid);
      ctx.save();
      ctx.translate(px, py);
      ctx.rotate(ang.mid + Math.PI / 2);
      ctx.fillStyle = '#fff';
      ctx.font = 'bold 7.5px sans-serif';
      ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
      ctx.fillText(LABELS[i], 0, 0);
      ctx.restore();
    }

    // selected sector highlight
    if (selected !== null) {
      var ang = secAngles(selected);
      annulus(R_CTR, R_OUT, ang.a0, ang.a1);
      ctx.strokeStyle = theme.ring; ctx.lineWidth = 3.5; ctx.stroke();
    }

    // needle
    drawNeedle(theme);

    // centre knob
    ctx.beginPath(); ctx.arc(CX, CY, R_CTR, 0, 2*Math.PI);
    ctx.fillStyle = theme.center; ctx.fill();
    ctx.strokeStyle = '#fff'; ctx.lineWidth = 2; ctx.stroke();
    ctx.fillStyle = '#fff'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.font = 'bold 8px sans-serif'; ctx.fillText('P(SBA)', CX, CY - 7);
    ctx.font = '7.5px sans-serif';
    ctx.fillText(parity === 'nulliparous' ? 'Nulliparous' : 'Multiparous', CX, CY + 5);
  }

  function drawNeedle(theme) {
    var angle = needleAngle;
    var tipR  = R_LABEL - 4;
    var baseR = R_CTR + 8;
    var halfW = ASTEP * 0.28;
    ctx.beginPath();
    ctx.moveTo(CX + tipR  * Math.cos(angle),        CY + tipR  * Math.sin(angle));
    ctx.lineTo(CX + baseR * Math.cos(angle - halfW), CY + baseR * Math.sin(angle - halfW));
    ctx.lineTo(CX + baseR * Math.cos(angle + halfW), CY + baseR * Math.sin(angle + halfW));
    ctx.closePath();
    ctx.fillStyle   = 'rgba(255,255,255,0.92)'; ctx.fill();
    ctx.strokeStyle = theme.needle; ctx.lineWidth = 1.5; ctx.stroke();
    ctx.beginPath();
    ctx.arc(CX + tipR * Math.cos(angle), CY + tipR * Math.sin(angle), 4, 0, 2*Math.PI);
    ctx.fillStyle = theme.needle; ctx.fill();
  }

  // ── INTERACTION ────────────────────────────────────────────────────────
  function angleToSector(a) {
    var norm = ((a - A0) % (2*Math.PI) + 2*Math.PI) % (2*Math.PI);
    return Math.max(0, Math.min(N-1, Math.floor(norm / ASTEP)));
  }
  function distFromCenter(x, y) {
    var dx = x - CX, dy = y - CY;
    return Math.sqrt(dx*dx + dy*dy);
  }
  function ptAngle(x, y) { return Math.atan2(y - CY, x - CX); }
  function canvasXY(e) {
    var rect = canvas.getBoundingClientRect();
    var src  = e.touches ? e.touches[0] : e;
    return {
      x: (src.clientX - rect.left) * (480 / rect.width),
      y: (src.clientY - rect.top)  * (480 / rect.height)
    };
  }
  function snapNeedle(a) {
    var idx = angleToSector(a);
    needleAngle = secAngles(idx).mid;
    selected = idx;
    drawWheel();
    updateReadout();
  }

  canvas.addEventListener('mousedown', function(e) {
    var p = canvasXY(e);
    var d = distFromCenter(p.x, p.y);
    if (d > R_OUT) return;
    if (d > R_LABEL) {
      snapNeedle(ptAngle(p.x, p.y));
    } else {
      isDragging = true;
      canvas.style.cursor = 'grabbing';
    }
  });
  document.addEventListener('mousemove', function(e) {
    if (!isDragging) return;
    var p = canvasXY(e);
    needleAngle = ptAngle(p.x, p.y);
    var idx = angleToSector(needleAngle);
    if (idx !== selected) { selected = idx; updateReadout(); }
    drawWheel();
  });
  document.addEventListener('mouseup', function() {
    if (!isDragging) return;
    isDragging = false;
    canvas.style.cursor = 'grab';
    snapNeedle(needleAngle);
  });
  canvas.addEventListener('touchstart', function(e) {
    e.preventDefault();
    var p = canvasXY(e);
    if (distFromCenter(p.x, p.y) <= R_OUT) { isDragging = true; }
  }, { passive: false });
  canvas.addEventListener('touchmove', function(e) {
    e.preventDefault();
    if (!isDragging) return;
    var p = canvasXY(e);
    needleAngle = ptAngle(p.x, p.y);
    var idx = angleToSector(needleAngle);
    if (idx !== selected) { selected = idx; updateReadout(); }
    drawWheel();
  }, { passive: false });
  canvas.addEventListener('touchend', function() {
    if (!isDragging) return;
    isDragging = false;
    snapNeedle(needleAngle);
  });

  // ── READOUT ────────────────────────────────────────────────────────────
  function updateReadout() {
    var el = document.getElementById('sbaReadout');
    if (!el) return;
    var data = parity === 'nulliparous' ? NULI : MULTI;
    var row  = data[selected];
    var html = '<div class="sba-readout-title">Time to SBA: ' + LABELS[selected] + '</div>';
    for (var j = 0; j < 6; j++) {
      var v   = row[j];
      var pct = Math.round(v * 100);
      var cls = v >= .95 ? 'sba-dgreen' : (v >= .90 ? 'sba-lgreen' : 'sba-salmon');
      html += '<div class="sba-row"><span class="sba-scenario">' + SCENARIOS[j] +
              '</span><span class="sba-pct ' + cls + '">' + pct + '%</span></div>';
    }
    el.innerHTML = html;
  }

  // ── PARITY SWITCH ──────────────────────────────────────────────────────
  var switchBtn = document.getElementById('sbaSwitchBtn');
  if (switchBtn) {
    switchBtn.addEventListener('click', function() {
      parity = parity === 'nulliparous' ? 'multiparous' : 'nulliparous';
      var nameEl = document.getElementById('sbaParityName');
      if (nameEl) nameEl.textContent = parity === 'nulliparous' ? 'Nulliparous' : 'Multiparous';
      this.textContent = parity === 'nulliparous' ? 'Switch to Multiparous' : 'Switch to Nulliparous';
      drawWheel();
      updateReadout();
    });
  }

  // ── INIT ───────────────────────────────────────────────────────────────
  canvas.style.cursor = 'grab';
  drawWheel();
  updateReadout();
})();
