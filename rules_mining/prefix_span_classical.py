from collections import defaultdict

db =  [['attr_1(1->2)', 'attr_1(2->3)', 'attr_1(3->4)'],
           #['attr_1:1', 'attr_1:2', 'attr_1:2', 'attr_1:3', 'attr_1:3', 'attr_1:3', 'attr_1:3', 'attr_1:3', 'target'],
]

minsup = 1

results = []

def mine_rec(patt, mdb):
    def localOccurs(mdb):
        occurs = defaultdict(list)

        for (i, stoppos) in mdb:
            seq = db[i]
            for j in range(stoppos, len(seq)):
                l = occurs[seq[j]]
                if len(l) == 0 or l[-1][0] != i:
                    l.append((i, j + 1))
        return occurs

    for (c, newmdb) in localOccurs(mdb).items():
        newsup = len(newmdb)

        if newsup >= minsup:
            newpatt = patt + [c]

            results.append((newpatt, [i for (i, stoppos) in newmdb]))
            mine_rec(newpatt, newmdb)

mine_rec([], [(i, 0) for i in range(len(db))])

for r in results:
    print(r)