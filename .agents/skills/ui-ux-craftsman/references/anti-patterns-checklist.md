# UI/UX Anti-Patterns & Visual Pitfalls Checklist

This guide identifies the most common visual mistakes that degrade user experience and gives direct solutions for each.

---

## 🚫 Common Design Pitfalls & Modern Fixes

| # | Anti-Pattern (What went wrong) | Symptom / User Feeling | The Solution |
|:---:|---|---|---|
| **1** | **Harsh High-Contrast Borders** | "Caged UI", eye fatigue, visual clutter | Replace `1px solid #475569` with `rgba(255, 255, 255, 0.08)` or use subtle background luminance steps (`--bg-surface`). |
| **2** | **Saturated Colored Left-Bars on Chips** | Visual noise, glaring stripes in lists | Use clean, neutral chips (`#0f172a`) with subtle 1px border. Represent status via minimal pill badges instead of full border strips. |
| **3** | **Pure Black/White High-Contrast** | "Halo effect", retinal glare in dark mode | Soften `#ffffff` to `#f8fafc` or `#f1f5f9`. Soften `#000000` to deep slate `#0f172a` or `#1e293b`. |
| **4** | **Arbitrary Margin Guessing** | Disconnected items, chaotic alignment | Enforce geometric 4/8px spacing tokens (`4px`, `8px`, `12px`, `16px`, `24px`). |
| **5** | **Huge Untracked Headings** | Loose, sloppy typography | Apply negative tracking (`letter-spacing: -0.02em` to `-0.04em`) to headings $\ge 1.2\text{rem}$. |
| **6** | **Tiny Unpadded Click Targets** | Mis-clicks, frustration | Ensure clickable containers meet $\ge 32\times 32\text{px}$ hitbox via padding, even if the icon is $16\text{px}$. |
| **7** | **Cluttered All-at-Once Data** | Cognitive overload | Use progressive disclosure: partition leaf data from category branches, use clean paragraph dividers. |
| **8** | **Rigid Fixed-Pixel Widths** | Content clipping, broken multi-column wrappers | Use `grid-template-columns: repeat(auto-fill, minmax(220px, 1fr))` and fluid flex wrapping. |
| **9** | **Missing Micro-Transitions** | Jerky, cheap feel | Add `transition: all 0.15s cubic-bezier(0.4, 0, 0.2, 1)` with subtle translateY(-1px) and border hover. |
| **10** | **Non-Tabular Numeric Misalignment** | Wobbly tables, hard to compare metrics | Apply `font-variant-numeric: tabular-nums` or `font-family: var(--font-mono)` to numbers and align right. |
