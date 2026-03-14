/* ═══════════════════════════════════════════════════════════════════════════
   ActivityLog — Global JS
═══════════════════════════════════════════════════════════════════════════ */

// ── Sidebar toggle (mobile) ──────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  const toggle  = document.getElementById("sidebarToggle");
  const sidebar = document.getElementById("sidebar");

  if (toggle && sidebar) {
    toggle.addEventListener("click", () => {
      sidebar.classList.toggle("open");
    });

    // Close on outside click
    document.addEventListener("click", (e) => {
      if (sidebar.classList.contains("open") &&
          !sidebar.contains(e.target) &&
          !toggle.contains(e.target)) {
        sidebar.classList.remove("open");
      }
    });
  }

  // ── Load endpoint into sidebar badge
  fetchEndpoint();
});

// ── Fetch & display current endpoint ────────────────────────────────────
async function fetchEndpoint() {
  try {
    const r = await fetch("/api/config");
    const d = await r.json();
    updateSidebarEndpoint(d.endpoint || "");
  } catch (_) { /* silent */ }
}

function updateSidebarEndpoint(url) {
  const el = document.getElementById("endpointHost");
  if (!el) return;
  try {
    const u = new URL(url);
    el.textContent = u.host;
  } catch (_) {
    el.textContent = url || "not set";
  }
}
