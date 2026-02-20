/**
 * Shared UI components and API helpers
 * SPK Pemilihan Mata Pelajaran v2.0
 */

const API_BASE = "/api/v1";

// ─── API Helper ───────────────────────────────────────────────────────────────

async function apiFetch(endpoint, options = {}) {
  const res = await fetch(API_BASE + endpoint, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

// ─── Local Storage ────────────────────────────────────────────────────────────

const Store = {
  get: (key) => {
    try {
      return JSON.parse(localStorage.getItem(key));
    } catch {
      return null;
    }
  },
  set: (key, val) => localStorage.setItem(key, JSON.stringify(val)),
  remove: (key) => localStorage.removeItem(key),
};

// ─── Navbar Active Link ───────────────────────────────────────────────────────

function setActiveNavLink() {
  const path = window.location.pathname.split("/").pop() || "index.html";
  document.querySelectorAll(".navbar-links a").forEach((a) => {
    const href = a.getAttribute("href").split("/").pop();
    a.classList.toggle(
      "active",
      href === path || (path === "" && href === "index.html"),
    );
  });
}

// ─── Toast Notifications ──────────────────────────────────────────────────────

function showToast(message, type = "info", duration = 3500) {
  const container =
    document.getElementById("toast-container") || createToastContainer();
  const toast = document.createElement("div");
  toast.style.cssText = `
    padding: .75rem 1.25rem;
    border-radius: 10px;
    font-size: .875rem;
    font-weight: 500;
    box-shadow: 0 4px 16px rgba(0,0,0,.15);
    animation: slideToast .3s ease;
    max-width: 320px;
    display: flex; align-items: center; gap: .5rem;
  `;
  const colors = {
    success: { bg: "#d1fae5", color: "#065f46", icon: "✓" },
    error: { bg: "#fee2e2", color: "#991b1b", icon: "✕" },
    info: { bg: "#dbeafe", color: "#1e3a8a", icon: "ℹ" },
    warning: { bg: "#fef3c7", color: "#92400e", icon: "⚠" },
  };
  const c = colors[type] || colors.info;
  toast.style.background = c.bg;
  toast.style.color = c.color;
  toast.innerHTML = `<span style="font-size:1rem">${c.icon}</span> ${message}`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.animation = "fadeOut .3s ease forwards";
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

function createToastContainer() {
  const el = document.createElement("div");
  el.id = "toast-container";
  el.style.cssText =
    "position:fixed;bottom:1.5rem;right:1.5rem;z-index:9999;display:flex;flex-direction:column;gap:.5rem;";
  const style = document.createElement("style");
  style.textContent =
    "@keyframes slideToast{from{opacity:0;transform:translateX(20px)}to{opacity:1;transform:none}} @keyframes fadeOut{to{opacity:0;transform:translateX(20px)}}";
  document.head.appendChild(style);
  document.body.appendChild(el);
  return el;
}

// ─── RIASEC Colors/Labels (used by individual pages) ─────────────────────────
// Note: each page defines its own RIASEC_META array/object as needed

// ─── Format Helpers ───────────────────────────────────────────────────────────

function formatScore(val) {
  return (val * 100).toFixed(1);
}
function rankBadge(rank) {
  if (rank === 1) return `<span class="badge badge-amber">🏆 #1</span>`;
  if (rank <= 3) return `<span class="badge badge-green">#${rank}</span>`;
  return `<span class="badge badge-muted">#${rank}</span>`;
}

// ─── Init ─────────────────────────────────────────────────────────────────────

document.addEventListener("DOMContentLoaded", setActiveNavLink);
