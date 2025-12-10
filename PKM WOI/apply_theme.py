# apply_theme.py
# Usage: put this file in same folder as sekolah1.py and run `python apply_theme.py`
import re
from pathlib import Path

SRC = Path("sekolah1.py")
DST = Path("sekolah1_mod.py")

if not SRC.exists():
    print("Error: sekolah1.py not found in current directory.")
    raise SystemExit(1)

text = SRC.read_text(encoding="utf-8")

# ---------------------------
# 1) Remove / normalize emojis
# Use a regex that targets most emoji ranges (works for common cases)
# ---------------------------
emoji_pattern = re.compile(
    "[" 
    "\U0001F300-\U0001F5FF"  # symbols & pictographs
    "\U0001F600-\U0001F64F"  # emoticons
    "\U0001F680-\U0001F6FF"  # transport & map
    "\U0001F700-\U0001F77F"  # alchemical
    "\U0001F780-\U0001F7FF"
    "\U0001F800-\U0001F8FF"
    "\U0001F900-\U0001F9FF"
    "\U0001FA00-\U0001FA6F"
    "\U0001FA70-\U0001FAFF"
    "\u2600-\u26FF"          # Misc symbols
    "\u2700-\u27BF"          # Dingbats
    "]+", flags=re.UNICODE
)

text_no_emoji = emoji_pattern.sub("", text)

# Also remove stray heavy symbols like arrows and checkmarks in ascii ranges
# Replace some common unicode bullets/arrows that may remain:
text_no_emoji = re.sub(r"[⬆⬇➡✅❌🔍🔐🔑💾🚪🖨️🎫🎓📄📚📊💰💳💸👨‍🏫👥👤👨‍👩‍👧‍👦🧾🎨🏦🏫🔔]", "", text_no_emoji)

# ---------------------------
# 2) Prepare CSS block to inject (modern flat / light theme)
# We'll insert it after the import block (after the last import statement).
# If imports contain "streamlit as st" we'll inject right after the first occurrence.
# ---------------------------
css_block = r"""
# === START: INJECTED THEME (AUTOMATICALLY ADDED) ===
import streamlit as st as __st_theme_injected  # marker import to avoid duplicate injection

st.markdown(\"\"\"
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'Poppins', sans-serif; background-color: #f9fafb !important; color: #1e293b !important; }
[data-testid="stAppViewContainer"] { background-color: #f9fafb !important; }
[data-testid="stSidebar"] { background-color: #ffffff !important; border-right: 1px solid #e2e8f0; box-shadow: 2px 0 6px rgba(0,0,0,0.04); }
h1,h2,h3,h4 { color: #1d4ed8 !important; font-weight:600; }
div[data-testid="stVerticalBlock"] { background:#ffffff; border-radius:12px; box-shadow:0 2px 8px rgba(0,0,0,0.05); padding:1rem 1.3rem; margin-bottom:10px; }
[data-testid="stMetric"]{ background:#fff !important; padding:1.2rem !important; border-radius:12px !important; box-shadow:0 2px 8px rgba(0,0,0,0.05) !important; border:1px solid #e2e8f0 !important; }
[data-testid="stMetricLabel"]{ color:#475569 !important; }
[data-testid="stMetricValue"]{ color:#0f172a !important; font-weight:600 !important; }
button[kind="primary"], .stButton>button { background-color:#0078d4 !important; color:#fff !important; border-radius:8px !important; border:none !important; font-weight:500 !important; }
div[data-baseweb="tab-list"]{ background-color:#e0f2fe; border-radius:10px; padding:6px; }
div[data-baseweb="tab"]{ color:#0369a1 !important; font-weight:500; border-radius:8px; padding:0.5rem 1rem !important; }
div[data-baseweb="tab"][aria-selected="true"]{ background-color:#0369a1 !important; color:#fff !important; }
input, select, textarea { border-radius:6px !important; border:1px solid #cbd5e1 !important; }
.stDataFrame { border-radius:10px !important; overflow:hidden !important; box-shadow:0 2px 6px rgba(0,0,0,0.05); }
</style>
\"\"\", unsafe_allow_html=True)
# === END: INJECTED THEME ===
"""

# We'll try to insert the CSS block only once.
# Find insertion point: after the last import statement (i.e., last line that starts with "import" or "from ... import ...")
lines = text_no_emoji.splitlines()
insert_at = 0
for i, line in enumerate(lines):
    stripped = line.strip()
    if stripped.startswith("import ") or stripped.startswith("from "):
        insert_at = i + 1

# Prevent double injection: if marker already exists, skip insertion
already_injected = any("INJECTED THEME" in ln for ln in lines)
if already_injected:
    new_text = text_no_emoji
    print("Note: theme already injected previously — re-using cleaned text.")
else:
    # Reconstruct text with CSS inserted
    before = "\n".join(lines[:insert_at])
    after = "\n".join(lines[insert_at:])
    new_text = before + "\n\n" + css_block + "\n\n" + after
    print(f"Injected theme CSS after line {insert_at} (after imports).")

# ---------------------------
# 3) Minor textual cleanups:
# - Remove consecutive empty lines
# - Ensure "st.title" and other titles no longer contain multiple spaces from emoji removal
# ---------------------------
# collapse >2 blank lines to 2
new_text = re.sub(r"\n{3,}", "\n\n", new_text)

# remove trailing spaces on each line
new_text = "\n".join([ln.rstrip() for ln in new_text.splitlines()])

# backup original
bak = SRC.with_suffix(".py.bak")
bak.write_text(text, encoding="utf-8")
print(f"Backup saved to {bak}")

# write output
DST.write_text(new_text, encoding="utf-8")
print(f"Modified file written to {DST}")

# Show a short preview of changed lines where emojis were likely removed.
preview_lines = DST.read_text(encoding="utf-8").splitlines()
for idx, ln in enumerate(preview_lines[:200]):
    if ("st.title" in ln) or ("st.subheader" in ln) or ("st.markdown" in ln) or ("st.radio" in ln) or ("st.button" in ln):
        print(f"[{idx+1:04d}] {ln}")
