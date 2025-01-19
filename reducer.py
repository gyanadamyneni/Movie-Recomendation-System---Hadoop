import sys
from collections import defaultdict

def pearson_corr(u, o):
    c = set(u) & set(o)
    if not c: return 0
    um, om = sum(u.values())/len(u), sum(o.values())/len(o)
    n = sum((u[m] - um) * (o[m] - om) for m in c)
    du = sum((r - um) ** 2 for r in u.values())
    do = sum((r - om) ** 2 for r in o.values())
    return n / (du ** 0.5 * do ** 0.5) if du != 0 and do != 0 else 0

def recommend(u, d):
    t = sorted(d[u], key=d[u].get, reverse=True)[:5]
    s = defaultdict(float)
    for m in t:
        for o, r in d.items():
            if o != u and m in r: s[o] += r[m]
    p = {o: pearson_corr(d[u], d[o]) for o in s}
    pc = {o: p[o] for o in p if p[o] > 0}
    rec = set()
    for o, _ in sorted(pc.items(), key=lambda x: x[1], reverse=True)[:5]:
        for m in d[o]:
            if m not in d[u]: rec.add(m)
    return list(rec)[:5]

def reducer():
    d = defaultdict(dict)
    for line in sys.stdin:
        u, r = line.strip().split("\t")
        r = r.strip("{}").split(", ") if r else []
        for i in r:
            m, v = i.split(": ")
            d[u][m] = float(v)
    for u in d:
        rec = recommend(u, d)
        print(f"{u}\t{rec}")

if __name__ == "__main__":
    reducer()
