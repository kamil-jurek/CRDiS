from collections import defaultdict


def freq_seq_enum(sequences, min_support):
    freq_seqs = set()
    _freq_seq(sequences, tuple(), 0, min_support, freq_seqs)
    return freq_seqs


def _freq_seq(sdb, prefix, prefix_support, min_support, freq_seqs):
    print("------------------------------")
    if prefix:
        print("freq_seq", (prefix, prefix_support))
        freq_seqs.add((prefix, prefix_support))

    locally_frequents = _local_freq_items(sdb, prefix, min_support)
    print("local_freq", locally_frequents)
    if not locally_frequents:
        return

    for (item, support) in locally_frequents:
        new_prefix = prefix + (item,)
        print("new_prefix", new_prefix)
        new_sdb = _project(sdb, new_prefix)
        print("new_sdb", new_sdb)

        _freq_seq(new_sdb, new_prefix, support, min_support, freq_seqs)

def contains(small, big):
    for i in range(len(big)-len(small)+1):
        for j in range(len(small)):
            if big[i+j] != small[j]:
                break
        else:
            return i, i+len(small)
    return False

def _local_freq_items(sdb, prefix, min_support):
    items = defaultdict(int)
    freq_items = []
    for entry in sdb:
        visited = set()
        #print("element", entry[0])
        #items[entry[0]] += 1
        for element in entry:
            if element not in visited:
              #if element not in visited and contains(prefix+tuple(element), entry):
                print("element", element)
                items[element] += 1
                visited.add(element)
    # Sorted is optional. Just useful for debugging for now.
    print("items", items)
    for item in items:
        support = items[item]
        if support >= min_support:
            freq_items.append((item, support))
    return freq_items


def _project(sdb, prefix):
    new_sdb = []
    if not prefix:
        return sdb
    current_prefix_item = prefix[-1]
    for entry in sdb:
        j = 0
        projection = None
        for item in entry:
            if item == current_prefix_item:
                projection = entry[j + 1:]
                break
            j += 1
        if projection:
            new_sdb.append(projection)
    return new_sdb


seqs = ( 'caabc', 'abcb', 'cabc', 'abbca')
freq_seqs = freq_seq_enum(seqs, 2)
print(sorted(freq_seqs))