import os

def get_all_data() -> dict:
    data = {}
    for f in os.listdir("./data"):
        log = []
        for d in open("./data/"+f, "r", encoding="utf8").read().split("\n")[:-1]:
            ts, dm, ul = d.split(";")
            log.append({"timestamp":ts, "domain":dm, "url":ul})
        data[f[:-4]] = log
    return data

def get_all_domain_visit(limit=20) -> tuple[list[str], list[int]]:
    data = get_all_data()
    count = {}
    for d in data.keys():
        for d in data[d]:
            if d["domain"] not in count.keys():
                count[d["domain"]] = 0
            count[d["domain"]] += 1
    dm = []
    vl = []
    for d in sorted(count.items(), key=lambda x:x[1])[:limit]:
        dm.append(d[0])
        vl.append(int(d[1]))

    return dm, vl

def get_all_domain_ip(limit=20) -> tuple[list[str], list[int]]:
    data = get_all_data()
    count = {}
    for d in data.keys():
        count[d] = len(data[d])

    dm = []
    vl = []
    for d in sorted(count.items(), key=lambda x:x[1])[:limit]:
        dm.append(d[0])
        vl.append(int(d[1]))

    return dm, vl
