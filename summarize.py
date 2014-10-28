#!/usr/bin/env python
'''Ultra simple summarizer'''

# Algorithm:
# 1. For each word, caluclate it's frequency in the document
# 2. For each sentence in the document
#       score(sentence) = sum([freq(word) for word in sentence])
# 3. Print X top sentences such that their size < MAX_SUMMARY_SIZE
# See http://en.wikipedia.org/wiki/Sentence_extraction for more

__author__ = 'Miki Tebeka <miki.tebeka@gmail.com>'

from collections import defaultdict
import re

MAX_SUMMARY_SIZE = 300


def tokenize(text):
    '''Very simple white space tokenizer, in real life we'll be much more
    fancy.
    '''
    return text.split()


def split_to_sentences(text):
    '''Very simple spliting to sentences by [.!?] and paragraphs.
    In real life we'll be much more fancy.
    '''
    sentences = []
    start = 0

    # We use finditer and not split since we want to keep the end
    for match in re.finditer('(\s*[.!?]\s*)|(\n{2,})', text):
        sentences.append(text[start:match.end()].strip())
        start = match.end()

    if start < len(text):
        sentences.append(text[start:].strip())

    return sentences


def token_frequency(text):
    '''Return frequency (count) for each token in the text'''
    frequencies = defaultdict(int)
    for token in tokenize(text):
        frequencies[token] += 1

    return frequencies


def sentence_score(sentence, frequencies):
    return sum((frequencies[token] for token in tokenize(sentence)))


def create_summary(sentences, max_length):
    summary = []
    size = 0
    for sentence in sentences:
        summary.append(sentence)
        size += len(sentence)
        if size >= max_length:
            break

    summary = summary[:max_length]
    return '\n'.join(summary)


def summarize(text, max_summary_size=MAX_SUMMARY_SIZE):
    frequencies = token_frequency(text)
    sentences = split_to_sentences(text)
    sentences.sort(key=lambda s: sentence_score(s, frequencies), reverse=1)
    summary = create_summary(sentences, max_summary_size)

    return summary


def _test(size=MAX_SUMMARY_SIZE):
    text = '''
    Turkey has recalled its ambassador to Sweden after the Swedish Parliament
    voted to describe Turkey's killings of Armenians in World War I as
    "genocide."

    The Swedish vote came despite the Swedish government's opposition to the
    resolution, as several parliament members crossed party lines in the vote,
    which passed the resolution by a vote of 131-130, with 88 parliament
    members absent. The Swedish government called the vote a "mistake," but
    added that it will not influence their position on the matter. The Turkish
    government released a statement saying, "our people and our government
    reject this decision based upon major errors and without foundation," and
    Prime Minister Tayyip Erdogan immediately cancelled a planned visit to
    Sweden. Despite the reaction, Turkey said that the moves did "not
    correspond to the close friendship of our two nations," and they were only
    recalling their ambassador for consultations.

    The resolution is particularly sensitive given that Sweden has long been a
    strong supporter of Turkey and their bid to join the European Union, and
    Turkey has been for years maintaining that their actions in World War I
    against Armenians did not amount to genocide. Despite Turkey's claims,
    Armenians have been heavily campaigning for the killings to be recognized
    as genocide, and many countries worldwide have done so.

    Swedish Foreign Minister Carl Bildt said that the vote would likely have a
    significant effect on the fate of negotiations between Turkey and Armenia,
    which have been attempting to resume normal diplomatic relations since last
    year. The Turkish ambassador that was recalled said that the vote would
    have "drastic effects" on the negotiations, and it would have an impact for
    some time.

    The Swedish vote came not long after a similar vote by a US Congressional
    panel, which also approved a resolution with similar terminology, leading
    to the removal of Turkey's ambassador. In that case, the US government has
    been trying to prevent the resolution from going further, in an attempt to
    limit the consequences of the vote.'''

    print(summarize(text, size))


def main(argv=None):
    import sys
    from argparse import ArgumentParser

    argv = argv or sys.argv

    parser = ArgumentParser(description='Summarize text')
    parser.add_argument('file', nargs='?',
        help='file to summarize (stdin will be used otherwise)')
    parser.add_argument('-s', '--size', help='Size of summary',
                        default=MAX_SUMMARY_SIZE, type=int)
    parser.add_argument('--test', help='test', action='store_true',
                        default=False)
    args = parser.parse_args(argv[1:])

    if args.test:
        _test(args.size)
        raise SystemExit

    if args.file:
        if args.file == '-':
            fo = sys.stdin
        else:
            try:
                fo = open(args.file)
            except IOError as err:
                raise SystemExit('error: cannot open {}: {}'.format(
                    args.file, err))
    else:
        fo = sys.stdin

    text = fo.read()
    print(summarize(text, args.size))


if __name__ == '__main__':
    main()
