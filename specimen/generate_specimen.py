import base64
import os
import subprocess

repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
font_dir = os.path.join(repo_root, "dist", "ttf")
output_png = os.path.join(repo_root, "specimen", "specimen.png")

with open(os.path.join(font_dir, "DuboriAsomiyaSerif-Regular.ttf"), "rb") as f:
    reg_b64 = base64.b64encode(f.read()).decode("ascii")
with open(os.path.join(font_dir, "DuboriAsomiyaSerif-Bold.ttf"), "rb") as f:
    bold_b64 = base64.b64encode(f.read()).decode("ascii")
with open(os.path.join(font_dir, "DuboriAsomiyaSerif-Medium.ttf"), "rb") as f:
    med_b64 = base64.b64encode(f.read()).decode("ascii")
with open(os.path.join(font_dir, "DuboriAsomiyaSerif-SemiBold.ttf"), "rb") as f:
    semi_b64 = base64.b64encode(f.read()).decode("ascii")

html_content = f"""<!DOCTYPE html>
<html lang="as">
<head>
<meta charset="utf-8">
<style>
  @font-face {{
    font-family: 'Dubori Asomiya Serif';
    src: url('data:font/ttf;base64,{reg_b64}') format('truetype');
    font-weight: 400;
    font-style: normal;
  }}
  @font-face {{
    font-family: 'Dubori Asomiya Serif';
    src: url('data:font/ttf;base64,{med_b64}') format('truetype');
    font-weight: 500;
    font-style: normal;
  }}
  @font-face {{
    font-family: 'Dubori Asomiya Serif';
    src: url('data:font/ttf;base64,{semi_b64}') format('truetype');
    font-weight: 600;
    font-style: normal;
  }}
  @font-face {{
    font-family: 'Dubori Asomiya Serif';
    src: url('data:font/ttf;base64,{bold_b64}') format('truetype');
    font-weight: 700;
    font-style: normal;
  }}

  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    -webkit-font-smoothing: antialiased;
    text-rendering: optimizeLegibility;
  }}

  body {{
    width: 1200px;
    height: 675px;
    background: #042f2e;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Dubori Asomiya Serif', serif;
    font-feature-settings: "kern" 1, "liga" 1, "locl" 1;
    overflow: hidden;
  }}

  .card {{
    width: 1120px;
    height: 605px;
    background: #021a19;
    border: 2px solid #2dd4bf;
    border-radius: 24px;
    padding: 34px 44px;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.6);
  }}

  .top-row {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
  }}

  .badge {{
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 5px 14px;
    background: #0d9488;
    color: #ffffff;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.08em;
    border-radius: 9999px;
    text-transform: uppercase;
  }}

  .badge-secondary {{
    display: inline-flex;
    align-items: center;
    padding: 4px 12px;
    background: rgba(45, 212, 191, 0.12);
    border: 1px solid #14b8a6;
    color: #5eead4;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 12px;
    font-weight: 600;
    border-radius: 9999px;
  }}

  .title-group {{
    margin-bottom: 14px;
  }}

  .title {{
    font-size: 40px;
    font-weight: 700;
    color: #f0fdfa;
    line-height: 1.15;
    letter-spacing: -0.01em;
  }}

  .title .as-title {{
    color: #5eead4;
    font-weight: 700;
    margin-left: 6px;
  }}

  .subtitle {{
    font-size: 17px;
    font-weight: 400;
    color: #94a3b8;
    margin-top: 4px;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }}

  .divider {{
    height: 1px;
    background: #134e4a;
    margin: 12px 0 16px 0;
  }}

  .hero-proverb-box {{
    background: rgba(19, 78, 74, 0.25);
    border: 1px solid #0f766e;
    border-radius: 14px;
    padding: 14px 20px;
    margin-bottom: 14px;
  }}

  .section-label {{
    font-size: 13px;
    font-weight: 600;
    color: #2dd4bf;
    letter-spacing: 0.04em;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    text-transform: uppercase;
    margin-bottom: 4px;
  }}

  .proverb {{
    font-size: 34px;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.25;
    letter-spacing: 0.01em;
  }}

  .proverb-meaning {{
    font-size: 13px;
    color: #94a3b8;
    margin-top: 3px;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-style: italic;
  }}

  .ligatures-row {{
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 14px;
  }}

  .lig-label {{
    font-size: 13px;
    color: #cbd5e1;
    font-weight: 500;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    white-space: nowrap;
  }}

  .lig-chips {{
    display: flex;
    gap: 6px;
    flex-wrap: wrap;
  }}

  .chip {{
    background: #0f172a;
    border: 1px solid #134e4a;
    color: #5eead4;
    padding: 2px 10px;
    border-radius: 6px;
    font-size: 18px;
    font-weight: 600;
  }}

  .chip-highlight {{
    background: #134e4a;
    border: 1px solid #2dd4bf;
    color: #ffffff;
    padding: 2px 10px;
    border-radius: 6px;
    font-size: 18px;
    font-weight: 700;
  }}

  .alphabet-section {{
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid #134e4a;
    border-radius: 12px;
    padding: 12px 18px;
  }}

  .alphabet {{
    font-size: 19px;
    color: #e2e8f0;
    line-height: 1.5;
    letter-spacing: 0.08em;
    word-spacing: 0.2em;
  }}

  .footer {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding-top: 12px;
    border-top: 1px solid #134e4a;
    font-size: 14px;
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  }}

  .styles-list {{
    color: #5eead4;
    font-weight: 600;
    font-size: 13px;
    letter-spacing: 0.02em;
  }}

  .credits {{
    font-size: 13px;
    color: #94a3b8;
  }}
</style>
</head>
<body>
  <div class="card">
    <div>
      <div class="top-row">
        <span class="badge">Google Fonts Submission</span>
        <span class="badge-secondary">Authentic Assamese Orthography</span>
      </div>

      <div class="title-group">
        <h1 class="title">Dubori Asomiya Serif <span class="as-title">(দুবৰি অসমীয়া চেৰিফ)</span></h1>
        <p class="subtitle">Open-Access SIL OFL 1.1 Editorial Typeface Family for Assamese Literature &amp; Publishing</p>
      </div>

      <div class="divider"></div>

      <div class="hero-proverb-box">
        <div class="section-label">দৃষ্টান্ত বাক্য (Specimen Proverb):</div>
        <div class="proverb">জ্ঞানতকৈ সংসাৰত উত্তম একো নাই।</div>
        <div class="proverb-meaning">In this mortal world, there is nothing more sublime than knowledge.</div>
      </div>

      <div class="ligatures-row">
        <span class="lig-label">Authentic Orthography &amp; Conjuncts:</span>
        <div class="lig-chips">
          <span class="chip-highlight" title="Pure Assamese Ra">ৰ (Ra)</span>
          <span class="chip-highlight" title="Pure Assamese Va">ৱ (Va)</span>
          <span class="chip">ক্ষ</span>
          <span class="chip">জ্ঞ</span>
          <span class="chip">হ্ম</span>
          <span class="chip">হ্ণ</span>
          <span class="chip">হ্ন</span>
          <span class="chip">ত্ব</span>
          <span class="chip">দ্ধ</span>
          <span class="chip">ন্ত</span>
          <span class="chip">ন্দ</span>
          <span class="chip">ষ্ট</span>
          <span class="chip">ব্ব</span>
          <span class="chip">শ্ব</span>
        </div>
      </div>

      <div class="alphabet-section">
        <p class="alphabet">অ আ ই ঈ উ ঊ ঋ এ ঐ ও ঔ &nbsp; ক খ গ ঘ ঙ চ ছ জ ঝ ঞ ট ঠ ড ঢ ণ</p>
        <p class="alphabet">ত থ দ ধ ন প ফ ব ভ ম য ৰ ল ৱ শ ষ স হ ক্ষ ড় ঢ় য় ৎ ং ঃ ঁ</p>
      </div>
    </div>

    <div class="footer">
      <div class="styles-list">
        10 Styles: Regular (400) | Medium (500) | SemiBold (600) | Bold (700) | Black (900) | Condensed | Variable
      </div>
      <div class="credits">
        Designed by Dubori &amp; Naruttam Boruah | github.com/narnonymous/dubori-asomiya-serif
      </div>
    </div>
  </div>
</body>
</html>
"""

temp_html = "/tmp/specimen_pro.html"
with open(temp_html, "w", encoding="utf-8") as f:
    f.write(html_content)

chrome_bin = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
cmd = [
    chrome_bin,
    "--headless",
    "--disable-gpu",
    f"--screenshot={output_png}",
    "--window-size=1200,675",
    "--force-device-scale-factor=2",
    "--default-background-color=00000000",
    f"file://{temp_html}"
]
subprocess.run(cmd, check=True)
print("Saved specimen poster to:", output_png)
