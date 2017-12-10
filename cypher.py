from collections import defaultdict
from random import choice

pages = []
index = defaultdict(list)  # word -> [(page, i), (page, i) ...]

with open('sherlock-holmes.txt') as fp:
    # ~300 words per page, ~10 words per sentence
    page, lnum, wnum = [], 1, 1
    for line in fp:
        if not line.strip():
            continue
        for wnum, word in enumerate(line.lower().split(), wnum):
            page.append(word)
            index[word].append((len(pages) + 1, wnum))
        wnum += 1
        lnum += 1

        if lnum == 30:
            pages.append(page)
            page, lnum, wnum = [], 1, 1
    if page:
        pages.append(page)


def encode(sentence):
    dec = []
    for word in sentence.lower().split():
        dec += choice(index[word])
    return dec


def decode(cypher):
    cypher = [int(w) for w in cypher.split()]
    words = []
    for i in range(0, len(cypher), 2):
        page = cypher[i] - 1
        wnum = cypher[i+1] - 1
        words.append(pages[page][wnum])
    return ' '.join(words)



#print(' '.join(str(n) for n in encode('london at afternoon')))
print(decode('117 278 243 249 87 213'))

