import re, sys

if len(sys.argv) < 2:
	print("the version was not detected")
	exit(1)
version = sys.argv[1]
print(f"the version recognized is: {version}")
with open("buildVars.py", 'r+', encoding='utf-8') as f:
	text = f.read()
	text = re.sub('"addon_version" *:.*,', f'"addon_version" : "{version}",', text)
	f.seek(0)
	f.write(text)
	f.truncate()
