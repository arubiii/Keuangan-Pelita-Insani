import re
from pathlib import Path

src = Path("sekolah1.py")
dst = Path("sekolah1_noemoji.py")

text = src.read_text(encoding="utf-8")

# hapus hampir semua emoji / ikon unicode
emoji_pattern = re.compile(
    "[" 
    "\U0001F300-\U0001F5FF"
    "\U0001F600-\U0001F64F"
    "\U0001F680-\U0001F6FF"
    "\U0001F700-\U0001F77F"
    "\U0001F780-\U0001F7FF"
    "\U0001F800-\U0001F8FF"
    "\U0001F900-\U0001F9FF"
    "\U0001FA00-\U0001FAFF"
    "\u2600-\u26FF"
    "\u2700-\u27BF"
    "]+", flags=re.UNICODE
)
cleaned = emoji_pattern.sub("", text)

dst.write_text(cleaned, encoding="utf-8")
print("✅ File bersih disimpan sebagai:", dst)
