from pathlib import Path
p = Path('interview_bot/interview_bot.py')
text = p.read_text(encoding='utf-8')
lines = text.splitlines()
for i,l in enumerate(lines,1):
    if '"""' in l or "'''" in l:
        print(i, l)
