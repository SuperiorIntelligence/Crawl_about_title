const form = document.getElementById("search-form");
const input = document.getElementById("q");
const status = document.getElementById("status");
const btn = document.getElementById("btn-search");

form?.addEventListener("submit", async (event) => {
  event.preventDefault();
  const query = (input?.value || "").trim();
  if (!query) return;

  btn.disabled = true;
  status.textContent = "در حال جستجو در فروشگاه‌ها… ممکن است کمی طول بکشد.";

  try {
    const res = await fetch("/api/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query, use_cache: true }),
    });
    if (!res.ok) {
      const text = await res.text();
      throw new Error(text || "HTTP " + res.status);
    }
    status.textContent = "تمام شد — در حال نمایش نتایج…";
    const url = new URL(window.location.href);
    url.searchParams.set("q", query);
    window.location.href = url.pathname + "?" + url.searchParams.toString();
  } catch (err) {
    status.textContent = "خطا: " + err.message;
    btn.disabled = false;
  }
});
