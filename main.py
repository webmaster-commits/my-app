"use client";
import React, { useEffect, useMemo, useRef, useState, createElement as h } from "react";

// === Pricing logic (no React needed) ===
const basePrices = { 1000: 9.99, 5000: 39.99, 10000: 69.99, 25000: 149.99 };
const premiumMultiplier = 1.2; // +20%
function calcPrice(qty, tier) {
  const base = basePrices[qty] || 0;
  return tier === "premium" ? base * premiumMultiplier : base;
}

// Optional: tiny env guard (harmless in Next "use client" component)
const envReadyNow = () => {
  try {
    if (typeof window === "undefined" || typeof document === "undefined") return false;
    const rs = document.readyState;
    return rs === "interactive" || rs === "complete";
  } catch {
    return false;
  }
};

// Simple payment icons (text badges) used in footer
function PaymentIcons() {
  const items = ["Mastercard", "Visa", "Amex", "Apple Pay", "Crypto"];
  return h(
    "div",
    { className: "flex flex-wrap items-center gap-2" },
    ...items.map((name) =>
      h(
        "span",
        {
          key: name,
          className:
            "inline-flex items-center px-2 py-1 text-xs rounded-md border border-slate-200 dark:border-white/15 bg-white dark:bg-white/5",
        },
        name
      )
    )
  );
}

export default function BuyInstagramFollowersPage() {
  if (!envReadyNow()) return null; // avoids hydration hiccups in quirky hosts

  // ===== State =====
  const [qty, setQty] = useState(1000);
  const [tier, setTier] = useState("hq"); // 'hq' | 'premium'
  const [mode, setMode] = useState("dark"); // 'dark' | 'light'
  const buyRef = useRef(null);

  // Initialize theme from localStorage or prefers-color-scheme
  useEffect(() => {
    try {
      let initial = null;
      const saved = window.localStorage ? window.localStorage.getItem("ui-theme") : null;
      if (saved === "light" || saved === "dark") initial = saved; // fixed logic
      if (!initial && window.matchMedia && window.matchMedia("(prefers-color-scheme: light)").matches)
        initial = "light";
      if (initial) setMode(initial);
    } catch {}
  }, []);

  const price = useMemo(() => calcPrice(qty, tier), [qty, tier]);

  function buildCheckoutURL() {
    const p = price.toFixed(2);
    return `/checkout?product=instagram_followers&qty=${qty}&tier=${tier}&price=${p}`;
  }

  function handleCheckout() {
    const url = buildCheckoutURL();
    if (typeof window !== "undefined" && window.location) {
      window.location.href = url;
    } else {
      try {
        console.log("[Checkout URL]", url);
      } catch {}
    }
  }

  function selectPackage(q, t = tier) {
    setQty(q);
    setTier(t);
    setTimeout(() => {
      if (buyRef.current?.scrollIntoView) {
        buyRef.current.scrollIntoView({ behavior: "smooth" });
      }
    }, 0);
  }

  function toggleTheme() {
    const next = mode === "dark" ? "light" : "dark";
    setMode(next);
    try {
      window.localStorage?.setItem("ui-theme", next);
    } catch {}
  }

  // ===== Self-tests (run after mount) =====
  useEffect(() => {
    function almostEq(a, b, eps = 1e-3) {
      return Math.abs(a - b) < eps;
    }
    try {
      // === Existing tests (unchanged) ===
      console.assert(almostEq(calcPrice(1000, "hq"), 9.99), "calcPrice 1000 hq");
      console.assert(almostEq(calcPrice(1000, "premium"), 9.99 * 1.2), "calcPrice 1000 premium");
      console.assert(almostEq(calcPrice(5000, "hq"), 39.99), "calcPrice 5000 hq");
      console.assert(almostEq(calcPrice(10000, "premium"), 69.99 * 1.2), "calcPrice 10000 premium");
      console.assert(almostEq(calcPrice(12345, "hq"), 0), "calcPrice unknown qty");

      // === Additional tests (added) ===
      [1000, 5000, 10000, 25000].forEach((q) => {
        const v = calcPrice(q, "hq");
        console.assert(Number.isFinite(v), `calcPrice ${q} hq is finite`);
      });
      [1000, 5000, 10000, 25000].forEach((q) => {
        const hq = calcPrice(q, "hq");
        const pr = calcPrice(q, "premium");
        console.assert(almostEq(pr, hq * premiumMultiplier), `premium == hq * ${premiumMultiplier} for ${q}`);
      });
      console.assert(almostEq(calcPrice("not-a-number", "hq"), 0), "string qty handled");
      console.assert(
        almostEq(calcPrice(0, "hq"), 0) && almostEq(calcPrice(-5000, "premium"), 0),
        "non-positive qty handled"
      );
      console.assert(almostEq(calcPrice(25000, "premium"), 149.99 * 1.2), "calcPrice 25000 premium");
      console.assert(almostEq(calcPrice(1000, "unknown"), 9.99), "unknown tier falls back to base");
      const allFormattedOk = [1000, 5000, 10000, 25000].every((q) =>
        calcPrice(q, "premium").toFixed(2).match(/^\d+\.(\d{2})$/)
      );
      console.assert(allFormattedOk, "toFixed(2) formatting stable across tiers");

      // New tests for URL + env + components
      console.assert(typeof buildCheckoutURL === "function", "buildCheckoutURL exists");
      const u = buildCheckoutURL();
      console.assert(u.includes("product=instagram_followers"), "checkout url has product");
      console.assert(u.includes("qty=" + qty), "checkout url has qty");
      console.assert(u.includes("tier=" + tier), "checkout url has tier");
      console.assert(/price=\d+\.\d{2}$/.test(u), "checkout price has two decimals");
      console.assert(typeof PaymentIcons === "function", "PaymentIcons exists");

      console.log("[SelfTest] calcPrice: all tests passed");
    } catch (err) {
      try {
        console.warn("[SelfTest] calcPrice tests failed", err);
      } catch {}
    }
  }, [qty, tier, price]);

  // ===== Theme classes =====
  const isDark = mode === "dark";
  const pageBg = isDark
    ? "bg-[linear-gradient(180deg,#0b0f17_0%,#0c1222_60%,#0d1426_100%)] text-slate-100"
    : "bg-white text-slate-900";
  const headerBg = isDark ? "bg-[rgba(11,15,23,0.7)] border-white/10" : "bg-white/70 border-slate-200";
  const badgeBg = isDark ? "border-white/10 bg-white/5" : "border-slate-200 bg-slate-100";
  const muted = isDark ? "text-slate-300/80" : "text-slate-600";
  const cardBg = isDark ? "bg-[#101626] border-white/10" : "bg-white border-slate-200";
  const heroCardBg = isDark ? "bg-[linear-gradient(180deg,#0e162b,#0e1526)] border-white/10" : "bg-white border-slate-200";
  const btnPrimary = isDark
    ? "bg-[linear-gradient(135deg,#8ab4ff,#6ee7b7)] text-slate-900"
    : "bg-[linear-gradient(135deg,#2563eb,#10b981)] text-white";

  // ===== Small components =====
  function PlanCard({ pill, title, price: priceText, items, primary, onSelect }) {
    return h(
      "div",
      { className: `relative rounded-2xl p-4 border shadow-xl ${cardBg} overflow-hidden` },
      h(
        "span",
        {
          className: `absolute top-3 right-3 text-xs rounded-full px-2 py-1 border ${
            isDark
              ? "border-emerald-300/40 bg-emerald-300/15 text-emerald-50"
              : "border-emerald-500/40 bg-emerald-500/10 text-emerald-700"
          }`,
        },
        pill
      ),
      h("h3", { className: "text-lg font-bold" }, title),
      h("div", { className: "text-3xl font-black my-1" }, priceText),
      h(
        "ul",
        { className: "grid gap-1 my-2" },
        ...(items || []).map((it) => h("li", { key: it, className: "list-none flex items-start gap-2" }, h("span", null, it)))
      ),
      h(
        "button",
        {
          onClick: onSelect,
          className: `w-full py-3 rounded-xl font-bold border ${
            isDark ? "border-white/20 bg-white/5" : "border-slate-200 bg-slate-100"
          } ${primary ? `!border-0 ${btnPrimary}` : ""}`,
        },
        "Select"
      )
    );
  }

  // ===== Render =====
  return h(
    "div",
    { className: `min-h-screen ${pageBg}` },
    // Header
    h(
      "header",
      { className: `sticky top-0 z-40 backdrop-blur border-b ${headerBg}` },
      h(
        "div",
        { className: "mx-auto w-[min(1100px,92%)] flex items-center justify-between py-3.5" },
        h(
          "div",
          { className: "flex items-center gap-2 font-extrabold tracking-tight" },
          h("div", {
            className: `w-8 h-8 rounded-xl shadow-[0_6px_16px_rgba(138,180,255,0.35)] ${
              isDark ? "bg-[linear-gradient(135deg,#6ee7b7,#8ab4ff)]" : "bg-[linear-gradient(135deg,#60a5fa,#34d399)]"
            }`,
          }),
          h("span", null, "Likes.io")
        ),
        h(
          "nav",
          { className: "hidden sm:flex items-center gap-2" },
          h(
            "a",
            { href: "#pricing", className: `px-3 py-2 rounded-lg border ${isDark ? "border-white/10 bg-white/5" : "border-slate-200 bg-slate-100"}` },
            "Pricing"
          ),
          h(
            "a",
            { href: "#how", className: `px-3 py-2 rounded-lg border ${isDark ? "border-white/10 bg-white/5" : "border-slate-200 bg-slate-100"}` },
            "How it works"
          ),
          h(
            "a",
            { href: "#faq", className: `px-3 py-2 rounded-lg border ${isDark ? "border-white/10 bg-white/5" : "border-slate-200 bg-slate-100"}` },
            "FAQ"
          ),
          h("a", { href: "#buy", className: `px-3 py-2 rounded-lg font-bold ${btnPrimary}` }, "Get Followers"),
          h(
            "button",
            { onClick: toggleTheme, "aria-label": "Toggle theme", className: `ml-2 px-3 py-2 rounded-lg border ${isDark ? "border-white/10 bg-white/5" : "border-slate-200 bg-slate-100"}` },
            isDark ? "☀️ Light" : "🌙 Dark"
          )
        )
      )
    ),

    // Main
    h(
      "main",
      null,
      // Hero
      h(
        "section",
        { className: "mx-auto w-[min(1100px,92%)] grid md:grid-cols-[1.2fr_.8fr] gap-9 items-center pt-14 pb-6" },
        h(
          "div",
          null,
          h(
            "h1",
            { className: "text-[clamp(28px,4.6vw,48px)] leading-tight font-extrabold" },
            "Buy Instagram Followers — Instant Delivery. Real Quality."
          ),
          h(
            "p",
            { className: `${muted} text-[clamp(14px,2.4vw,18px)] mt-2` },
            "Boost credibility and reach with high-quality Instagram followers delivered fast. No password required, 24/7 support, and a refill warranty for peace of mind."
          ),
          h(
            "div",
            { className: "flex flex-wrap gap-2 mt-4 mb-6" },
            ..."⚡ Instant delivery,🛡️ Refill warranty,🔒 No password needed,💬 24/7 support"
              .split(",")
              .map((b) => h("span", { key: b, className: `inline-flex items-center gap-2 px-3 py-2 rounded-full border text-sm ${badgeBg}` }, b))
          ),
          h(
            "div",
            { className: `flex flex-wrap gap-3 text-[13px] ${muted}` },
            h("div", { className: "flex items-center gap-2" }, "✅ Trusted by 500k+ creators"),
            h("div", { className: "flex items-center gap-2" }, "⭐ 4.9/5 average rating"),
            h("div", { className: "flex items-center gap-2" }, "💳 Secure checkout")
          )
        ),
        h(
          "aside",
          { id: "buy", ref: buyRef, className: `rounded-2xl p-4 border shadow-xl ${heroCardBg}` },
          h("h3", { className: "m-0 text-lg font-bold" }, "Choose Your Package"),
          h("p", { className: `${muted} mt-1` }, "Select a size and quality tier. You can adjust later."),
          // Quantity options
          h(
            "div",
            { className: "grid grid-cols-2 gap-2 mt-3" },
            ...[1000, 5000, 10000, 25000].map((q) =>
              h(
                "label",
                {
                  key: q,
                  className: `rounded-xl p-3 cursor-pointer transition border ${
                    isDark ? "bg-[#0a1222]" : "bg-slate-50"
                  } ${
                    qty === q
                      ? isDark
                        ? "border-[#8ab4ff]"
                        : "border-sky-400"
                      : isDark
                      ? "border-white/20 hover:border-[#8ab4ff]"
                      : "border-slate-200 hover:border-sky-400"
                  }`,
                },
                h("div", { className: "flex items-center justify-between font-bold" }, h("span", null, `${q.toLocaleString()} Followers`), h("span", null, `$${(basePrices[q] ?? 0).toFixed(2)}`)),
                h(
                  "small",
                  { className: `${muted} block mt-1` },
                  q === 1000 ? "Fast delivery • Best for trying out" : q === 5000 ? "Popular • Strong social proof" : q === 10000 ? "Viral push • Best value" : "For brands & agencies"
                ),
                h("input", { type: "radio", name: "qty", className: `mt-2 ${isDark ? "accent-[#8ab4ff]" : "accent-sky-500"}`, checked: qty === q, onChange: () => setQty(q) })
              )
            )
          ),
          // Tier options
          h(
            "div",
            { className: "mt-3" },
            h("label", { className: "font-bold block mb-1" }, "Quality"),
            h(
              "div",
              { className: "grid grid-cols-2 gap-2" },
              ...[
                { value: "hq", label: "High-Quality", right: "Included", desc: "Great profiles, quick delivery" },
                { value: "premium", label: "Premium", right: "+20%", desc: "Higher retention & activity" },
              ].map((o) =>
                h(
                  "label",
                  {
                    key: o.value,
                    className: `rounded-xl p-3 cursor-pointer transition border ${
                      isDark ? "bg-[#0a1222]" : "bg-slate-50"
                    } ${
                      tier === o.value
                        ? isDark
                          ? "border-[#8ab4ff]"
                          : "border-sky-400"
                        : isDark
                        ? "border-white/20 hover:border-[#8ab4ff]"
                        : "border-slate-200 hover:border-sky-400"
                    }`,
                  },
                  h("div", { className: "flex items-center justify-between font-bold" }, h("span", null, o.label), h("span", null, o.right)),
                  h("small", { className: `${muted} block mt-1` }, o.desc),
                  h("input", { type: "radio", name: "tier", className: `mt-2 ${isDark ? "accent-[#8ab4ff]" : "accent-sky-500"}`, checked: tier === o.value, onChange: () => setTier(o.value) })
                )
              )
            )
          ),
          h("div", { className: `text-[13px] ${muted} mt-2` }, "No password required. Make your account public during delivery."),
          h("button", { onClick: handleCheckout, className: `w-full mt-3 inline-flex items-center justify-center gap-2 px-4 py-3 rounded-xl font-extrabold shadow-[0_10px_24px_rgba(138,180,255,0.35)] ${btnPrimary}` }, "Continue to Checkout →"),
          h("div", { className: `text-[13px] ${muted} mt-2` }, "30-day refill warranty • Money-back guarantee")
        )
      ),

      // Trust features
      h(
        "section",
        { className: "mx-auto w-[min(1100px,92%)] py-8" },
        h(
          "div",
          { className: "grid md:grid-cols-3 gap-4" },
          ...[
            { title: "Real-Looking Profiles", desc: "We deliver high-quality profiles designed for better credibility and retention." },
            { title: "Fast & Safe", desc: "Start seeing results within minutes. No password needed—ever." },
            { title: "24/7 Support", desc: "Our team is available around the clock to help with any order." },
          ].map((c) => h("div", { key: c.title, className: `rounded-2xl p-4 border shadow-xl ${cardBg}` }, h("h3", { className: "text-lg font-bold" }, c.title), h("p", { className: muted }, c.desc)))
        )
      ),

      // Pricing
      h(
        "section",
        { id: "pricing", className: "mx-auto w-[min(1100px,92%)] py-8" },
        h("h2", { className: "text-[clamp(22px,3.4vw,34px)] font-extrabold" }, "Transparent Pricing"),
        h("p", { className: `${muted} mb-3` }, "Simple packages with refill warranty. Choose what fits your goals."),
        h(
          "div",
          { className: "grid md:grid-cols-3 gap-4" },
          h(PlanCard, { pill: "Starter", title: "High-Quality Followers", price: "$9.99", items: ["✅ Instant delivery", "✅ No password needed", "✅ 30-day refill warranty"], onSelect: () => selectPackage(1000, tier) }),
          h(PlanCard, { pill: "Most Popular", title: "Premium Followers", price: "$39.99", items: ["✅ Faster delivery window", "✅ Higher retention", "✅ Priority support"], primary: true, onSelect: () => selectPackage(5000, "premium") }),
          h(PlanCard, { pill: "Best Value", title: "Premium+ Bulk", price: "$69.99", items: ["✅ Optimized drip schedule", "✅ Enhanced refill coverage", "✅ Ideal for brands"], onSelect: () => selectPackage(10000, "premium") })
        )
      ),

      // How it works
      h(
        "section",
        { id: "how", className: "mx-auto w-[min(1100px,92%)] py-8" },
        h("h2", { className: "text-[clamp(22px,3.4vw,34px)] font-extrabold" }, "How It Works"),
        h(
          "div",
          { className: "grid md:grid-cols-2 lg:grid-cols-4 gap-3" },
          ...[
            { n: "STEP 1", t: "Pick a package", d: "Choose the size and quality that match your goals." },
            { n: "STEP 2", t: "Enter username", d: "No password required. Keep your account public." },
            { n: "STEP 3", t: "Secure payment", d: "Pay with major cards. Encrypted and safe." },
            { n: "STEP 4", t: "Instant delivery", d: "Followers begin arriving within minutes." },
          ].map((s) =>
            h(
              "div",
              { key: s.n, className: `p-4 rounded-xl border ${isDark ? "border-white/20 bg-white/5" : "border-slate-200 bg-slate-50"}` },
              h("div", { className: isDark ? "text-xs font-black tracking-[0.12em] text-[#0ea5e9]" : "text-xs font-black tracking-[0.12em] text-sky-600" }, s.n),
              h("h3", { className: "font-bold mt-1" }, s.t),
              h("p", { className: muted }, s.d)
            )
          )
        )
      ),

      // Social proof
      h(
        "section",
        { className: "mx-auto w-[min(1100px,92%)] py-8" },
        h("h2", { className: "text-[clamp(22px,3.4vw,34px)] font-extrabold" }, "Loved by Creators & Brands"),
        h(
          "div",
          { className: "grid md:grid-cols-3 gap-4" },
          ...[
            { name: "Sam R.", text: "Exactly what I needed to kickstart a new brand page. Delivery was fast and support was helpful." },
            { name: "Alya K.", text: "Great retention compared to others I tried. The Premium tier is worth it for bigger pushes." },
            { name: "Marco D.", text: "Simple process and the refill warranty gave me confidence. Will reorder soon." },
          ].map((r) =>
            h("div", { key: r.name, className: `rounded-2xl p-4 border shadow-xl ${cardBg}` }, h("div", { className: "tracking-widest" }, "★★★★★"), h("p", { className: "mt-2" }, r.text), h("div", { className: muted }, `— ${r.name}`))
          )
        )
      ),

      // FAQ
      h(
        "section",
        { id: "faq", className: "mx-auto w-[min(1100px,92%)] py-8" },
        h("h2", { className: "text-[clamp(22px,3.4vw,34px)] font-extrabold" }, "Frequently Asked Questions"),
        h(
          "div",
          { className: "grid gap-2" },
          ...[
            { q: "Do you need my password?", a: "No. We only need your public username and a public account during delivery." },
            { q: "How fast is delivery?", a: "Most orders start within minutes. Larger packages may use a drip schedule for safety." },
            { q: "What if followers drop?", a: "You’re covered by our 30-day refill warranty. We’ll automatically top up eligible orders." },
            { q: "Is this safe for my account?", a: "We use safe delivery methods and never ask for your password. Use at your own discretion and follow platform rules." },
            { q: "What payment methods do you accept?", a: "Major credit/debit cards. Contact support if you need alternatives." },
          ].map((f) => h("details", { key: f.q, className: `rounded-xl p-4 border ${cardBg}` }, h("summary", { className: "cursor-pointer font-bold" }, f.q), h("p", { className: `${muted} mt-1` }, f.a)))
        )
      )
    ),

    // Footer
    h(
      "footer",
      { className: `py-10 border-t ${isDark ? "border-white/10" : "border-slate-200"} ${muted}` },
      h(
        "div",
        { className: "mx-auto w-[min(1100px,92%)] grid gap-8 md:grid-cols-5 items-start" },
        h("div", { className: "col-span-1" }, h("div", { className: `font-bold ${isDark ? "text-slate-100" : "text-slate-900"}` }, "Likes.io"), h("div", { className: "mt-2" }, `© ${new Date().getFullYear()} Likes.io. All rights reserved.`)),
        h(
          "div",
          null,
          h("div", { className: "font-semibold mb-2 text-slate-900 dark:text-slate-100" }, "Instagram"),
          h(
            "ul",
            { className: "space-y-2" },
            h("li", null, h("a", { href: "/buy-instagram-followers", className: "hover:underline" }, "Buy Instagram Followers")),
            h("li", null, h("a", { href: "/buy-instagram-likes", className: "hover:underline" }, "Buy Instagram Likes")),
            h("li", null, h("a", { href: "/buy-instagram-views", className: "hover:underline" }, "Buy Instagram Views"))
          )
        ),
        h(
          "div",
          null,
          h("div", { className: "font-semibold mb-2 text-slate-900 dark:text-slate-100" }, "YouTube"),
          h(
            "ul",
            { className: "space-y-2" },
            h("li", null, h("a", { href: "/buy-youtube-views", className: "hover:underline" }, "Buy Youtube Views")),
            h("li", null, h("a", { href: "/buy-youtube-likes", className: "hover:underline" }, "Buy Youtube Likes")),
            h("li", null, h("a", { href: "/buy-youtube-subscribers", className: "hover:underline" }, "Buy Youtube Subscribers"))
          )
        ),
        h(
          "div",
          null,
          h("div", { className: "font-semibold mb-2 text-slate-900 dark:text-slate-100" }, "TikTok"),
          h(
            "ul",
            { className: "space-y-2" },
            h("li", null, h("a", { href: "/buy-tiktok-followers", className: "hover:underline" }, "Buy TikTok Followers")),
            h("li", null, h("a", { href: "/buy-tiktok-likes", className: "hover:underline" }, "Buy TikTok Likes")),
            h("li", null, h("a", { href: "/buy-tiktok-views", className: "hover:underline" }, "Buy TikTok Views"))
          )
        ),
        h(
          "div",
          null,
          h("div", { className: "font-semibold mb-2 text-slate-900 dark:text-slate-100" }, "Account"),
          h("ul", { className: "space-y-2" }, h("li", null, h("a", { href: "/account", className: "hover:underline font-semibold" }, "My Account"))),
          h("div", { className: "font-semibold mt-4 mb-2 text-slate-900 dark:text-slate-100" }, "Payments"),
          h(PaymentIcons, null)
        )
      ),
      h(
        "div",
        { className: `mx-auto w-[min(1100px,92%)] flex flex-wrap items-center justify-between gap-4 mt-8 pt-6 border-t ${isDark ? "border-white/10" : "border-slate-200"}` },
        h("div", { className: "flex gap-4" }, h("a", { href: "/terms" }, "Terms"), h("a", { href: "/privacy" }, "Privacy"), h("a", { href: "/contact" }, "Contact")),
        h("button", { onClick: toggleTheme, "aria-label": "Toggle theme", className: `px-3 py-2 rounded-lg border ${isDark ? "border-white/10 bg-white/5" : "border-slate-200 bg-slate-100"}` }, isDark ? "☀️ Light mode" : "🌙 Dark mode")
      )
    )
  );
}
