# Design Tokens & Color Palettes Cheat Sheet

This reference contains ready-to-use color formulas, typography scales, and spacing maps tailored for high-performance dark and light web applications.

---

## 1. 12-Step Functional Color Scale (Dark Mode Focus)

| Step | Role | Dark Slate Hex / RGBA | Light Slate Hex | Usage |
|:---:|---|---|---|---|
| **1** | App Background | `#0f172a` (Slate 900) | `#f8fafc` | Main body/window canvas |
| **2** | Subtle Surface | `#1e293b` (Slate 800) | `#f1f5f9` | Sidebars, table footers, toolbars |
| **3** | Card / Panel Surface | `#162032` / `#1e293b` | `#ffffff` | Floating cards, row containers |
| **4** | Component Hover | `#273549` | `#e2e8f0` | Hover state for buttons/rows |
| **5** | Component Active | `#334566` | `#cbd5e1` | Pressed / active state |
| **6** | Subtle Border | `rgba(255, 255, 255, 0.08)` | `rgba(0, 0, 0, 0.08)` | Cards, row dividers, containers |
| **7** | Interactive Border | `rgba(255, 255, 255, 0.16)` | `rgba(0, 0, 0, 0.18)` | Inputs, button resting borders |
| **8** | Focus / Hover Border | `rgba(56, 189, 248, 0.4)` | `rgba(2, 132, 199, 0.5)` | Hover borders, subtle focus rings |
| **9** | Solid Accent (Primary) | `#38bdf8` (Sky 400) | `#0284c7` (Sky 600) | Main action CTA, active tabs |
| **10** | Accent Hover | `#0284c7` (Sky 600) | `#0369a1` (Sky 700) | CTA hover state |
| **11** | Secondary / Muted Text | `#94a3b8` / `#64748b` | `#64748b` / `#94a3b8` | Metadata, paths, helper hints |
| **12** | Primary High-Contrast Text | `#f8fafc` (Slate 50) | `#0f172a` (Slate 900) | Titles, headers, card names |

---

## 2. Typography Hierarchy & Optical Tracking Scale

| Element | Size | Weight | Tracking (`letter-spacing`) | Line-Height | Text Color |
|---|---|---|---|---|---|
| **Page Title (H1)** | `1.5rem - 1.75rem` | `700` | `-0.03em` | `1.2` | `#f8fafc` |
| **Section Header (H2)** | `1.15rem - 1.25rem` | `600` | `-0.02em` | `1.3` | `#f8fafc` |
| **Card / Row Title (H3)** | `0.88rem - 0.95rem` | `600` | `-0.01em` | `1.35` | `#f8fafc` |
| **Body / Default Text** | `0.82rem - 0.875rem` | `400 / 500` | `0` | `1.5` | `#e2e8f0` |
| **Sub-Group / Tier Label** | `0.70rem - 0.75rem` | `600` | `+0.04em` (Uppercase) | `1.2` | `#94a3b8` |
| **Badge / Pill Tag** | `0.65rem - 0.70rem` | `600` | `+0.02em` | `1.2` | Accent Color |
| **Monospace Data / Code** | `0.75rem - 0.80rem` | `500` | `0` | `1.4` | `#38bdf8` |

---

## 3. Status Accent Palettes (Subtle, Non-Blinding Tones)

```css
/* Success / Leaves / Positive */
--badge-success-bg: rgba(16, 185, 129, 0.08);
--badge-success-text: #34d399;
--badge-success-border: rgba(16, 185, 129, 0.2);

/* Info / Branches / Categories */
--badge-info-bg: rgba(56, 189, 248, 0.08);
--badge-info-text: #7dd3fc;
--badge-info-border: rgba(56, 189, 248, 0.2);

/* Warning / Duplicates / Cross-Level Matches */
--badge-warning-bg: rgba(245, 158, 11, 0.08);
--badge-warning-text: #fbbf24;
--badge-warning-border: rgba(245, 158, 11, 0.22);

/* Danger / Errors / Destructive */
--badge-danger-bg: rgba(244, 63, 94, 0.08);
--badge-danger-text: #fb7185;
--badge-danger-border: rgba(244, 63, 94, 0.22);
```
