import re

s = "hrehdfhg123231&"
p = re.compile(r'[a-z\u0590-\u05fe1-9]+$')

print(bool(p.match(s)))