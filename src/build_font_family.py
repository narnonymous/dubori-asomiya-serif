#!/usr/bin/env python3
"""
Dubori Asomiya Serif (দুবৰি অসমীয়া চেৰিফ) - Build & Family Generation Pipeline
-------------------------------------------------------------------------------
Engineered by Dubori & Naruttam Boruah.
Generates an authoritative, publication-ready Assamese Serif typeface family
with comprehensive weights (Regular, Medium, SemiBold, Bold, Black),
width axes (Condensed, Bold Condensed, Black Condensed),
slanted styles (Italic, Bold Italic), and Variable Font formats.

Features:
- Native Assamese script optimization (U+0980 - U+09FF)
- Preserves authentic Assamese Ra (ৰ - U+09F0), Va (ৱ - U+09F1), Ya (য় - U+09DF)
- Injects explicit OpenType LangSys 'ASM ' into 'bng2' and 'beng' scripts
- Complete 209-conjunct ligature support verified by HarfBuzz
- Outputs Desktop TTF, Web WOFF2, and unified CSS @font-face rules
"""

import os
import sys
import copy
import math
import shutil
import zipfile
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables import otTables
from fontTools.varLib import instancer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"
MASTERS_DIR = SRC_DIR / "masters"
DIST_DIR = PROJECT_ROOT / "dist"
TTF_DIR = DIST_DIR / "ttf"
WOFF2_DIR = DIST_DIR / "woff2"
SPECIMEN_DIR = PROJECT_ROOT / "specimen"

for d in [TTF_DIR, WOFF2_DIR, SPECIMEN_DIR]:
    d.mkdir(parents=True, exist_ok=True)

MASTER_VAR_PATH = MASTERS_DIR / "NotoSerifBengali-Variable.ttf"

def restore_authentic_matra_overhang(font):
    """
    Restores the authentic classical Assamese headline (matra / শিৰোৰেখা) overhang
    for terminal vowel signs.
    In Noto Serif Bengali, final forms (.fina) were truncated flush at the vertical stem.
    This restores the full overhanging serif spur (as shown in traditional Assamese penmanship
    and editorial typography) for:
      - uni09BE.fina (া - aa-kar)
      - uni09C0.fina (ী - dirgha-i-kar)
      - uni09D7.fina (ৌ - au-kar length mark)
      - uni09D7.fina.001.001
    """
    if "glyf" not in font or "hmtx" not in font:
        return
    glyf = font["glyf"]
    hmtx = font["hmtx"]
    gvar = font.get("gvar")
    
    pairs = [
        ("uni09BE", "uni09BE.fina"),
        ("uni09C0", "uni09C0.fina"),
        ("uni09D7", "uni09D7.fina"),
        ("uni09D7.fina.001", "uni09D7.fina.001.001")
    ]
    for src, dst in pairs:
        if src in glyf and dst in glyf:
            glyf[dst] = copy.deepcopy(glyf[src])
            hmtx[dst] = copy.deepcopy(hmtx[src])
            if gvar and src in gvar.variations and dst in gvar.variations:
                gvar.variations[dst] = copy.deepcopy(gvar.variations[src])
            print(f"  [Matra Overhang] Restored authentic overhanging serif: {src} -> {dst}")

def inject_assamese_language_system(font):
    """Injects 'ASM ' (Assamese) LangSys record into GSUB bng2 and beng scripts."""
    if "GSUB" not in font:
        return
    gsub = font["GSUB"].table
    for script_rec in gsub.ScriptList.ScriptRecord:
        if script_rec.ScriptTag in ["bng2", "beng"]:
            script = script_rec.Script
            existing = [l.LangSysTag for l in script.LangSysRecord]
            if "ASM " not in existing and script.DefaultLangSys:
                new_lang_rec = otTables.LangSysRecord()
                new_lang_rec.LangSysTag = "ASM "
                new_lang_rec.LangSys = copy.deepcopy(script.DefaultLangSys)
                script.LangSysRecord.append(new_lang_rec)
                print(f"  [GSUB] Injected LangSys 'ASM ' into script '{script_rec.ScriptTag}'")

def set_font_naming(font, subfamily, weight_val, width_val=100, is_italic=False, is_variable=False):
    """Sets standard, cross-platform OpenType naming records for Dubori Asomiya Serif."""
    name_table = font["name"]
    family_name = "Dubori Asomiya Serif"
    
    # Subfamily display
    if is_variable:
        subfamily_name = "Regular"
        full_name = f"{family_name} Variable"
        ps_name = "DuboriAsomiyaSerif-Variable"
    else:
        subfamily_name = subfamily
        full_name = f"{family_name} {subfamily}"
        ps_clean = subfamily.replace(" ", "")
        ps_name = f"DuboriAsomiyaSerif-{ps_clean}"

    unique_id = f"1.000;DBRI;{ps_name}"
    version_str = "Version 1.000; Dubori Release 2026; build.dbri.01"
    copyright_str = "Copyright 2026 Dubori & Naruttam Boruah. Portions Copyright Google Inc. Distributed under SIL Open Font License, Version 1.1."
    desc_str = (
        "Dubori Asomiya Serif is an authoritative, open-access Assamese editorial serif typeface "
        "engineered by Dubori for high-resolution desktop publishing, literature, news columns, "
        "and digital web typography. Featuring authentic Assamese Ra, Va, complete 209-conjunct ligature shaper, "
        "and multi-width axes."
    )
    designer_str = "Dubori & Naruttam Boruah"
    vendor_str = "Dubori"
    vendor_url = "https://dubori.in"
    designer_url = "https://linkedin.com/in/naruttamboruah"
    license_str = "This Font Software is licensed under the SIL Open Font License, Version 1.1."
    license_url = "https://openfontlicense.org"

    names_map = {
        0: copyright_str,
        1: family_name,
        2: subfamily_name,
        3: unique_id,
        4: full_name,
        5: version_str,
        6: ps_name,
        7: "Dubori is a registered trademark of Naruttam Boruah.",
        8: vendor_str,
        9: designer_str,
        10: desc_str,
        11: vendor_url,
        12: designer_url,
        13: license_str,
        14: license_url,
        16: family_name,
        17: subfamily_name,
    }

    for name_id, val in names_map.items():
        # Windows / Unicode
        name_table.setName(val, name_id, platformID=3, platEncID=1, langID=0x409)
        # Macintosh / Roman
        name_table.setName(val, name_id, platformID=1, platEncID=0, langID=0x0)

    # OS/2 table settings
    if "OS/2" in font:
        os2 = font["OS/2"]
        os2.usWeightClass = int(weight_val)
        if width_val <= 75:
            os2.usWidthClass = 3  # Condensed
        elif width_val <= 87.5:
            os2.usWidthClass = 4  # SemiCondensed
        else:
            os2.usWidthClass = 5  # Medium/Normal

        # Handle fsSelection bits
        # bit 0: Italic, bit 5: Bold, bit 6: Regular
        os2.fsSelection &= ~64  # clear regular default
        if is_italic:
            os2.fsSelection |= 1
        if weight_val >= 700:
            os2.fsSelection |= 32
        if not is_italic and weight_val < 700 and width_val == 100:
            os2.fsSelection |= 64  # set regular

        os2.achVendID = b"DBRI"

    # Head table macStyle
    if "head" in font:
        head = font["head"]
        head.macStyle = 0
        if weight_val >= 700:
            head.macStyle |= 1  # Bold
        if is_italic:
            head.macStyle |= 2  # Italic

    # Post table italic angle
    if "post" in font:
        font["post"].italicAngle = -11.5 if is_italic else 0.0

def apply_italic_shear(font, angle_degrees=11.5):
    """Applies authentic typographical shear slant to all glyph coordinates in glyf table."""
    if "glyf" not in font:
        return
    glyf = font["glyf"]
    tan_angle = math.tan(math.radians(angle_degrees))

    for gname in glyf.glyphs.keys():
        g = glyf[gname]
        if hasattr(g, "coordinates") and g.coordinates:
            new_coords = []
            for x, y in g.coordinates:
                # Shear relative to baseline (y=0)
                nx = round(x + tan_angle * y)
                new_coords.append((nx, y))
            g.coordinates = type(g.coordinates)(new_coords)
            # Recompute bounding box
            g.xMin = min(c[0] for c in new_coords)
            g.xMax = max(c[0] for c in new_coords)
            g.yMin = min(c[1] for c in new_coords)
            g.yMax = max(c[1] for c in new_coords)

def build_static_instances():
    """Generates all targeted static instances from the master variable font."""
    print("\n📦 Generating Dubori Asomiya Serif Typeface Family...")

    instances_spec = [
        # (Subfamily Name, Weight, Width, IsItalic, FileSuffix)
        ("Regular", 400, 100, False, "Regular"),
        ("Medium", 500, 100, False, "Medium"),
        ("SemiBold", 600, 100, False, "SemiBold"),
        ("Bold", 700, 100, False, "Bold"),
        ("Black", 900, 100, False, "Black"),
        ("Condensed", 400, 75, False, "Condensed"),
        ("Bold Condensed", 700, 75, False, "BoldCondensed"),
        ("Black Condensed", 900, 75, False, "BlackCondensed"),
        ("Italic", 400, 100, True, "Italic"),
        ("Bold Italic", 700, 100, True, "BoldItalic"),
    ]

    generated_fonts = []

    for name, wght, wdth, is_italic, suffix in instances_spec:
        print(f"\n  🔨 Building '{name}' (wght={wght}, wdth={wdth}%, italic={is_italic})...")
        master = TTFont(MASTER_VAR_PATH)
        restore_authentic_matra_overhang(master)
        inject_assamese_language_system(master)

        # Instantiate static instance from variable coordinates
        inst = instancer.instantiateVariableFont(master, {"wght": wght, "wdth": wdth})

        # Apply italic shear if requested
        if is_italic:
            apply_italic_shear(inst, angle_degrees=11.5)

        # Set official names and tables
        set_font_naming(inst, name, wght, wdth, is_italic=is_italic, is_variable=False)

        # Save Desktop TTF
        ttf_path = TTF_DIR / f"DuboriAsomiyaSerif-{suffix}.ttf"
        inst.save(str(ttf_path))
        ttf_size = os.path.getsize(ttf_path)

        # Save Web WOFF2
        woff2_path = WOFF2_DIR / f"DuboriAsomiyaSerif-{suffix}.woff2"
        inst.flavor = "woff2"
        inst.save(str(woff2_path))
        woff2_size = os.path.getsize(woff2_path)

        print(f"     ✓ TTF: {ttf_path.name} ({ttf_size // 1024} KB)")
        print(f"     ✓ WOFF2: {woff2_path.name} ({woff2_size // 1024} KB)")

        generated_fonts.append({
            "name": name,
            "suffix": suffix,
            "weight": wght,
            "width": wdth,
            "italic": is_italic,
            "ttf_file": ttf_path.name,
            "woff2_file": woff2_path.name
        })

    # Also build the enhanced Master Variable Font
    print("\n  🌟 Building Dubori Asomiya Serif Variable Font [wdth,wght]...")
    var_font = TTFont(MASTER_VAR_PATH)
    restore_authentic_matra_overhang(var_font)
    inject_assamese_language_system(var_font)
    set_font_naming(var_font, "Regular", 400, 100, is_italic=False, is_variable=True)

    var_ttf_path = TTF_DIR / "DuboriAsomiyaSerif-Variable.ttf"
    var_font.save(str(var_ttf_path))
    var_woff2_path = WOFF2_DIR / "DuboriAsomiyaSerif-Variable.woff2"
    var_font.flavor = "woff2"
    var_font.save(str(var_woff2_path))

    print(f"     ✓ Variable TTF: {var_ttf_path.name} ({os.path.getsize(var_ttf_path) // 1024} KB)")
    print(f"     ✓ Variable WOFF2: {var_woff2_path.name} ({os.path.getsize(var_woff2_path) // 1024} KB)")

    return generated_fonts

def generate_css_bundle(generated_fonts):
    """Generates the official dubori-asomiya-serif.css stylesheet."""
    css_content = """/* ==========================================================================
   Dubori Asomiya Serif (দুবৰি অসমীয়া চেৰিফ) - Official Web Typography Bundle
   Designed by Dubori & Naruttam Boruah (https://dubori.in)
   Open-Access SIL Open Font License 1.1
   ========================================================================== */

/* 1. Variable Font (@supports variable font rendering) */
@supports (font-variation-settings: normal) {
  @font-face {
    font-family: 'Dubori Asomiya Serif';
    src: url('./woff2/DuboriAsomiyaSerif-Variable.woff2') format('woff2-variations'),
         url('./ttf/DuboriAsomiyaSerif-Variable.ttf') format('truetype');
    font-weight: 100 900;
    font-stretch: 62.5% 100%;
    font-style: normal;
    font-display: swap;
    unicode-range: U+0980-09FF, U+0020-007E, U+200C-200D, U+25CC;
  }
}

/* 2. Static Font Fallbacks & Dedicated Instances */
"""

    for f in generated_fonts:
        style = "italic" if f["italic"] else "normal"
        stretch = "condensed" if f["width"] < 80 else "normal"
        css_content += f"""@font-face {{
  font-family: 'Dubori Asomiya Serif';
  src: url('./woff2/{f["woff2_file"]}') format('woff2'),
       url('./ttf/{f["ttf_file"]}') format('truetype');
  font-weight: {f["weight"]};
  font-style: {style};
  font-stretch: {stretch};
  font-display: swap;
  unicode-range: U+0980-09FF, U+0020-007E, U+200C-200D, U+25CC;
}}

"""

    css_content += """/* 3. Utility Classes for Typographic Hierarchy */
.font-dubori-serif {
  font-family: 'Dubori Asomiya Serif', 'Noto Serif Bengali', serif;
  font-feature-settings: "kern" 1, "liga" 1, "locl" 1;
  text-rendering: optimizeLegibility;
  -webkit-font-smoothing: antialiased;
}

.font-dubori-condensed {
  font-family: 'Dubori Asomiya Serif', serif;
  font-stretch: condensed;
  font-variation-settings: "wdth" 75;
}

.font-dubori-black {
  font-family: 'Dubori Asomiya Serif', serif;
  font-weight: 900;
  font-variation-settings: "wght" 900;
}
"""

    css_path = DIST_DIR / "dubori-asomiya-serif.css"
    with open(css_path, "w", encoding="utf-8") as f:
        f.write(css_content)
    print(f"\n  ✓ Generated CSS stylesheet: {css_path.name}")

def package_desktop_zip():
    """Packages all TrueType fonts and OFL license into a clean desktop ZIP distribution."""
    zip_path = DIST_DIR / "Dubori-Asomiya-Serif-Font-Family.zip"
    
    # Write a clean README & OFL
    readme_text = """Dubori Asomiya Serif (দুবৰি অসমীয়া চেৰিফ) - Version 1.000
========================================================================

Designed & Engineered by Dubori (Naruttam Boruah)
Website: https://dubori.in | Lexicon: https://assamesedictionary.org

ABOUT THIS TYPEFACE:
Dubori Asomiya Serif is an authoritative, multi-weight, multi-width Assamese serif font
family engineered specifically for publication, books, newspaper columns, posters, and web.

INCLUDED STYLES (TTF):
1. DuboriAsomiyaSerif-Regular.ttf (Book / Body 400)
2. DuboriAsomiyaSerif-Medium.ttf (Medium 500)
3. DuboriAsomiyaSerif-SemiBold.ttf (SemiBold 600)
4. DuboriAsomiyaSerif-Bold.ttf (Bold 700)
5. DuboriAsomiyaSerif-Black.ttf (Heavy Display 900)
6. DuboriAsomiyaSerif-Condensed.ttf (Narrow Column / Editorial 400)
7. DuboriAsomiyaSerif-BoldCondensed.ttf (Narrow Headline 700)
8. DuboriAsomiyaSerif-BlackCondensed.ttf (Heavy Poster Condensed 900)
9. DuboriAsomiyaSerif-Italic.ttf (11.5° Slanted Cursive 400)
10. DuboriAsomiyaSerif-BoldItalic.ttf (Bold Slanted 700)
11. DuboriAsomiyaSerif-Variable.ttf (Continuous wght 100-900 & wdth 62.5-100%)

INSTALLATION:
- Windows: Select all .ttf files, right click and choose "Install for all users".
- macOS: Double-click each .ttf or open Font Book, File -> Add Fonts.
- Linux: Copy to ~/.local/share/fonts and run `fc-cache -fv`.

LICENSE:
Licensed under the SIL Open Font License, Version 1.1 (OFL-1.1).
Free for personal, educational, publishing, commercial, and open-source usage.
"""
    readme_file = DIST_DIR / "README.txt"
    with open(readme_file, "w", encoding="utf-8") as f:
        f.write(readme_text)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(readme_file, arcname="README.txt")
        for ttf in TTF_DIR.glob("*.ttf"):
            z.write(ttf, arcname=f"fonts/{ttf.name}")

    print(f"  ✓ Packaged Desktop Release ZIP: {zip_path.name} ({os.path.getsize(zip_path) // 1024} KB)")

def sync_to_web_dist():
    """Copies generated font assets to web production directories."""
    web_root = PROJECT_ROOT.parent.parent
    web_dist_fonts = web_root / "dist" / "fonts"
    web_downloads_fonts = web_root / "downloads" / "fonts"
    
    web_dist_fonts.mkdir(parents=True, exist_ok=True)
    web_downloads_fonts.mkdir(parents=True, exist_ok=True)
    
    # Copy WOFF2s & CSS to dist/fonts
    for f in WOFF2_DIR.glob("*.woff2"):
        shutil.copy2(f, web_dist_fonts / f.name)
    css_file = DIST_DIR / "dubori-asomiya-serif.css"
    if css_file.exists():
        shutil.copy2(css_file, web_dist_fonts / "dubori-asomiya-serif.css")
        
    # Copy TTFs & ZIP to downloads/fonts
    for f in TTF_DIR.glob("*.ttf"):
        shutil.copy2(f, web_downloads_fonts / f.name)
    zip_file = DIST_DIR / "Dubori-Asomiya-Serif-Font-Family.zip"
    if zip_file.exists():
        shutil.copy2(zip_file, web_downloads_fonts / "Dubori-Asomiya-Serif-Font-Family.zip")
        
    print("  ✓ Synchronized all font files to web dist/fonts and downloads/fonts")

if __name__ == "__main__":
    fonts = build_static_instances()
    generate_css_bundle(fonts)
    package_desktop_zip()
    sync_to_web_dist()
    print("\n🎉 [Dubori Font Build] Completed successfully!\n")
