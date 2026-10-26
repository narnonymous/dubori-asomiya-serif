# দুবৰি অসমীয়া চেৰিফ (Dubori Asomiya Serif)

[![License: OFL-1.1](https://img.shields.io/badge/License-OFL%201.1-emerald.svg)](https://openfontlicense.org)
[![Styles](https://img.shields.io/badge/Styles-11%20Total%20%2B%20Variable-teal.svg)](#11-styles-matrix)
[![Conjuncts](https://img.shields.io/badge/Conjuncts-209%20Verified%20Ligatures-blue.svg)](https://assamesedictionary.org/conjuncts)
[![Interactive Specimen](https://img.shields.io/badge/Live%20Specimen-Workbench-teal.svg)](https://assamesedictionary.org/specimen)

**Dubori Asomiya Serif** is an authoritative, 11-style open-access Assamese editorial serif typeface family designed and engineered by **Dubori** ([Naruttam Boruah](https://github.com/narnonymous)). 

Tailored specifically for high-resolution desktop publishing, classical Vaishnavite literature, newspaper editorial columns, and digital web typography.

---

## Key Highlights

- **11 Curated Styles**: Continuous weight interpolation from Hairline to heavy Black (900), paired with dedicated 75% Narrow Condensed styles for editorial news columns, 11.5° cursive slants, and a continuous Variable Font (`[wght, wdth]`).
- **Authentic Assamese Script Optimization**: Injects native OpenType `LangSys: ASM ` into both `bng2` (Indic 2) and `beng` (Indic 1) GSUB tables, strictly preserving authentic Assamese **ৰ** (`U+09F0`), **ৱ** (`U+09F1`), and **য়** (`U+09DF`).
- **Authentic Headline (শিৰোৰেখা) Overhang**: Accurately preserves the classical headline overhang spur on terminal vowel marks (**া** - `U+09BE`, **ী** - `U+09C0`, **ৌ** - `U+09D7`), matching natural Assamese penmanship and traditional printing presses.
- **Complete 209-Conjunct Shaper**: Verified across 209 compound characters (দ্বি-ব্যঞ্জন, ত্ৰি-ব্যঞ্জন, চতুৰ্ব্যঞ্জন, ৰেফ, কূট যুক্তাক্ষৰ) with the HarfBuzz shaping engine.
- **Open-Access**: Released under the [SIL Open Font License 1.1](OFL.txt). Free for personal, commercial, publishing, educational, and open-source usage.

---

## 11 Styles Matrix

| Style Name | Weight | Width | PostScript Name | Best Use Case |
| :--- | :---: | :---: | :--- | :--- |
| **Regular** | 400 | 100% | `DuboriAsomiyaSerif-Regular` | Book text, body paragraphs, prose |
| **Medium** | 500 | 100% | `DuboriAsomiyaSerif-Medium` | Journalistic reading, academic papers |
| **SemiBold** | 600 | 100% | `DuboriAsomiyaSerif-SemiBold` | Subheadings, emphasis, callouts |
| **Bold** | 700 | 100% | `DuboriAsomiyaSerif-Bold` | Chapter titles, section headings |
| **Black** | 900 | 100% | `DuboriAsomiyaSerif-Black` | Heavy display, book covers, posters |
| **Condensed** | 400 | 75% | `DuboriAsomiyaSerif-Condensed` | Tight newspaper columns, dense tables |
| **Bold Condensed** | 700 | 75% | `DuboriAsomiyaSerif-BoldCondensed` | Newspaper headlines, banners |
| **Black Condensed** | 900 | 75% | `DuboriAsomiyaSerif-BlackCondensed` | Ultra-compact heavy display |
| **Italic** | 400 | 100% | `DuboriAsomiyaSerif-Italic` | 11.5° cursive quotations, poetry |
| **Bold Italic** | 700 | 100% | `DuboriAsomiyaSerif-BoldItalic` | Slanted headings, pull quotes |
| **Variable Font** | 100–900 | 75–100% | `DuboriAsomiyaSerif-Variable` | Fluid responsive web & animation |

---

## Web Font Integration

Embed Dubori Asomiya Serif in your website using the self-hosted stylesheet:

```html
<!-- 1. Include the stylesheet in your HTML <head> -->
<link rel="stylesheet" href="https://assamesedictionary.org/dist/fonts/dubori-asomiya-serif.css">
```

```css
/* 2. Apply font-family in CSS */
.assamese-text {
  font-family: 'Dubori Asomiya Serif', 'Noto Serif Bengali', serif;
  font-feature-settings: "kern" 1, "liga" 1, "locl" 1;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
}
```

---

## Desktop Installation

1. Download the complete [Dubori-Asomiya-Serif-Font-Family.zip](https://assamesedictionary.org/downloads/fonts/Dubori-Asomiya-Serif-Font-Family.zip).
2. Extract the archive.
3. Install:
   * **macOS**: Double-click each `.ttf` file and click **Install Font** in Font Book.
   * **Windows**: Select all `.ttf` files, right-click, and select **Install for all users**.
   * **Linux**: Copy files to `~/.local/share/fonts/` and run `fc-cache -fv`.

---

## Interactive Playground

Test real-time weights, widths, leading, alignment, presets, and all 209 conjuncts on the live test bench:
👉 **[assamesedictionary.org/specimen](https://assamesedictionary.org/specimen)**

---

## License

This Font Software is licensed under the [SIL Open Font License, Version 1.1](OFL.txt).
Designed & engineered by **Dubori** ([Naruttam Boruah](https://dubori.in)).
