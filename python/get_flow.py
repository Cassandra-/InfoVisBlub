import json
from test import build_database
from collections import Counter, defaultdict

from_to = []

DATA = build_database()
for student in DATA._data:
        to_dict = dict(student._to)
        from_dict = dict(student._from)
        if 'gemeente' in to_dict and 'gemeente' in from_dict:
            from_to.append([from_dict['gemeente'], to_dict['gemeente']])

from_to = filter(lambda x: x[0] != x[1], from_to)
from_to = map(tuple, from_to)
hist = Counter(from_to)

out = defaultdict(lambda: {})
for key, count in hist.items():
    frm = key[0]
    to = key[1]

    out[frm][to] = count

with open('flow.json', 'w') as f:
    json.dump(out, f, encoding='latin1', indent=1)
