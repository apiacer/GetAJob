(function () {
  const el = document.getElementById("verify-countdown");
  if (!el) return;

  let remaining = parseInt(el.dataset.remaining, 10);
  if (isNaN(remaining) || remaining < 0) {
    remaining = 0;
  }

  function format(seconds) {
    if (seconds <= 0) return "0s";
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    if (m > 0) return m + "m " + s + "s";
    return s + "s";
  }

  function tick() {
    if (remaining <= 0) {
      el.textContent = "expired";
      return;
    }
    el.textContent = format(remaining);
    remaining -= 1;
    setTimeout(tick, 1000);
  }

  tick();
})();
