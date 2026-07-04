/* SmartCredit AI - Lightweight Canvas Chart Library (no external dependencies) */

const SmartChart = (function () {
  function getCSSVar(name) {
    return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
  }

  function setupCanvas(canvas) {
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();
    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    const ctx = canvas.getContext('2d');
    ctx.scale(dpr, dpr);
    return { ctx, width: rect.width, height: rect.height };
  }

  function donut(canvas, segments, opts = {}) {
    const { ctx, width, height } = setupCanvas(canvas);
    const cx = width / 2, cy = height / 2;
    const radius = Math.min(width, height) / 2 - 6;
    const thickness = opts.thickness || radius * 0.34;
    const total = segments.reduce((s, d) => s + d.value, 0) || 1;
    let start = -Math.PI / 2;

    ctx.clearRect(0, 0, width, height);
    segments.forEach((seg) => {
      const angle = (seg.value / total) * Math.PI * 2;
      ctx.beginPath();
      ctx.arc(cx, cy, radius - thickness / 2, start, start + angle);
      ctx.lineWidth = thickness;
      ctx.strokeStyle = seg.color;
      ctx.lineCap = 'butt';
      ctx.stroke();
      start += angle;
    });

    if (opts.centerText) {
      ctx.fillStyle = getCSSVar('--text-primary');
      ctx.font = '700 26px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      ctx.fillText(opts.centerText, cx, cy - 6);
      if (opts.centerSubtext) {
        ctx.fillStyle = getCSSVar('--text-muted');
        ctx.font = '500 12px Inter, sans-serif';
        ctx.fillText(opts.centerSubtext, cx, cy + 16);
      }
    }
  }

  function gauge(canvas, value, opts = {}) {
    const { ctx, width, height } = setupCanvas(canvas);
    const cx = width / 2, cy = height * 0.86;
    const radius = Math.min(width / 2, height) - 18;
    const startAngle = Math.PI;
    const endAngle = 0;

    ctx.clearRect(0, 0, width, height);

    // Track
    ctx.beginPath();
    ctx.arc(cx, cy, radius, startAngle, endAngle, true);
    ctx.lineWidth = 18;
    ctx.strokeStyle = getCSSVar('--border');
    ctx.lineCap = 'round';
    ctx.stroke();

    // Value arc
    const valueAngle = startAngle - (Math.min(value, 100) / 100) * Math.PI;
    const grad = ctx.createLinearGradient(0, 0, width, 0);
    grad.addColorStop(0, opts.colorFrom || '#4f46e5');
    grad.addColorStop(1, opts.colorTo || '#06b6d4');
    ctx.beginPath();
    ctx.arc(cx, cy, radius, startAngle, valueAngle, true);
    ctx.lineWidth = 18;
    ctx.strokeStyle = grad;
    ctx.lineCap = 'round';
    ctx.stroke();

    ctx.fillStyle = getCSSVar('--text-primary');
    ctx.font = '800 32px Inter, sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText(Math.round(value) + '%', cx, cy - 18);
    if (opts.label) {
      ctx.fillStyle = getCSSVar('--text-muted');
      ctx.font = '600 12px Inter, sans-serif';
      ctx.fillText(opts.label, cx, cy + 4);
    }
  }

  function bars(canvas, data, opts = {}) {
    const { ctx, width, height } = setupCanvas(canvas);
    ctx.clearRect(0, 0, width, height);
    const padding = { top: 16, right: 10, bottom: 28, left: 10 };
    const chartW = width - padding.left - padding.right;
    const chartH = height - padding.top - padding.bottom;
    const max = Math.max(...data.map((d) => d.value), 1) * 1.15;
    const barWidth = chartW / data.length * 0.5;
    const gap = chartW / data.length;

    data.forEach((d, i) => {
      const barH = (d.value / max) * chartH;
      const x = padding.left + i * gap + (gap - barWidth) / 2;
      const y = padding.top + (chartH - barH);
      const grad = ctx.createLinearGradient(0, y, 0, y + barH);
      grad.addColorStop(0, d.color || '#7c3aed');
      grad.addColorStop(1, d.colorEnd || '#4f46e5');
      ctx.fillStyle = grad;
      const radius = 6;
      ctx.beginPath();
      ctx.moveTo(x, y + barH);
      ctx.lineTo(x, y + radius);
      ctx.arcTo(x, y, x + radius, y, radius);
      ctx.lineTo(x + barWidth - radius, y);
      ctx.arcTo(x + barWidth, y, x + barWidth, y + radius, radius);
      ctx.lineTo(x + barWidth, y + barH);
      ctx.closePath();
      ctx.fill();

      ctx.fillStyle = getCSSVar('--text-muted');
      ctx.font = '600 11px Inter, sans-serif';
      ctx.textAlign = 'center';
      ctx.fillText(d.label, x + barWidth / 2, height - 8);
    });
  }

  function line(canvas, points, opts = {}) {
    const { ctx, width, height } = setupCanvas(canvas);
    ctx.clearRect(0, 0, width, height);
    const padding = { top: 14, right: 14, bottom: 24, left: 14 };
    const chartW = width - padding.left - padding.right;
    const chartH = height - padding.top - padding.bottom;
    const max = Math.max(...points.map((p) => p.value), 1) * 1.2;
    const min = 0;
    const stepX = points.length > 1 ? chartW / (points.length - 1) : 0;

    const coords = points.map((p, i) => ({
      x: padding.left + i * stepX,
      y: padding.top + chartH - ((p.value - min) / (max - min || 1)) * chartH,
    }));

    // Area fill
    if (coords.length) {
      const grad = ctx.createLinearGradient(0, padding.top, 0, padding.top + chartH);
      grad.addColorStop(0, 'rgba(79,70,229,0.28)');
      grad.addColorStop(1, 'rgba(79,70,229,0)');
      ctx.beginPath();
      ctx.moveTo(coords[0].x, padding.top + chartH);
      coords.forEach((c) => ctx.lineTo(c.x, c.y));
      ctx.lineTo(coords[coords.length - 1].x, padding.top + chartH);
      ctx.closePath();
      ctx.fillStyle = grad;
      ctx.fill();
    }

    // Line
    ctx.beginPath();
    coords.forEach((c, i) => (i === 0 ? ctx.moveTo(c.x, c.y) : ctx.lineTo(c.x, c.y)));
    ctx.strokeStyle = opts.lineColor || '#4f46e5';
    ctx.lineWidth = 2.5;
    ctx.lineJoin = 'round';
    ctx.stroke();

    // Points
    coords.forEach((c) => {
      ctx.beginPath();
      ctx.arc(c.x, c.y, 3.5, 0, Math.PI * 2);
      ctx.fillStyle = getCSSVar('--surface-solid');
      ctx.fill();
      ctx.lineWidth = 2;
      ctx.strokeStyle = opts.lineColor || '#4f46e5';
      ctx.stroke();
    });
  }

  function hbar(canvas, data, opts = {}) {
    const { ctx, width, height } = setupCanvas(canvas);
    ctx.clearRect(0, 0, width, height);
    const rowH = height / data.length;
    const max = Math.max(...data.map((d) => d.value), 0.0001);
    const labelW = opts.labelWidth || 130;

    data.forEach((d, i) => {
      const y = i * rowH + rowH * 0.22;
      const barH = rowH * 0.56;
      const barMaxW = width - labelW - 50;
      const barW = (d.value / max) * barMaxW;

      ctx.fillStyle = getCSSVar('--text-secondary');
      ctx.font = '600 12px Inter, sans-serif';
      ctx.textAlign = 'left';
      ctx.textBaseline = 'middle';
      ctx.fillText(d.label, 0, y + barH / 2, labelW - 10);

      ctx.beginPath();
      const grad = ctx.createLinearGradient(labelW, 0, labelW + barW, 0);
      grad.addColorStop(0, d.color || '#4f46e5');
      grad.addColorStop(1, d.colorEnd || '#06b6d4');
      ctx.fillStyle = grad;
      const r = 5;
      ctx.moveTo(labelW, y);
      ctx.lineTo(labelW + Math.max(barW - r, 0), y);
      ctx.arcTo(labelW + barW, y, labelW + barW, y + r, r);
      ctx.lineTo(labelW + barW, y + barH - r);
      ctx.arcTo(labelW + barW, y + barH, labelW + Math.max(barW - r, 0), y + barH, r);
      ctx.lineTo(labelW, y + barH);
      ctx.closePath();
      ctx.fill();

      ctx.fillStyle = getCSSVar('--text-primary');
      ctx.font = '700 12px Inter, sans-serif';
      ctx.textAlign = 'left';
      ctx.fillText((d.value * 100).toFixed(1) + '%', labelW + barW + 8, y + barH / 2);
    });
  }

  return { donut, gauge, bars, line, hbar };
})();
