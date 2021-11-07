from itertools import pairwise as pairs
from string import ascii_lowercase as abc
import os

from allspells import spells
from allwords import words
from filteredswaps import filtered_swaps


def spell_words(spells):
    for spell in spells:
        for i, word in enumerate(spell.split(" ")):
            yield i, word, spell


def ins(iter, pos, add="", rem=0):
    return iter[:pos] + add + iter[pos + rem :]


def addeds(w):
    return (ins(w, i, a) for a in abc for i in range(len(w) + 1))


def removeds(w):
    return (ins(w, i, rem=1) for i, l in enumerate(w) if l.isalpha())


def replaceds(w):
    return (ins(w, i, a, 1) for i, l in enumerate(w) if l.isalpha() for a in abc.replace(l, ""))


def swappeds(w):
    return (
        ins(w, i, y + x, 2) for i, (x, y) in enumerate(pairs(w)) if x.isalpha() and y.isalpha()
    )


def gen_cands(word, *args):
    for func in args:
        for cand in func(word):
            yield (cand)


def valid(cand, word):
    return (
        False
        if (cand == word)
        or (cand == word + "s")
        or (word == cand + "s")
        or (word[-1] == "e" and cand[-2:] == "ed")
        or ((word, cand) in filtered_swaps)
        or (cand not in words)
        else True
    )


def formatted(cand, i, spell):
    return " ".join(ins(spell.split(" "), i, [cand.capitalize()], 1))


output_file = "misspells.js"
temp_file = "tmp_" + output_file

if __name__ == "__main__":
    with open(temp_file, "w") as f:
        f.write("const misspells = [\n")
        for index, word, spell in spell_words(spells):
            for cand in gen_cands(word, addeds, removeds, replaceds, swappeds):
                if valid(cand.lower(), word.lower()):
                    f.write('  "' + formatted(cand, index, spell) + '",\n')
        f.write("]")
        os.replace(temp_file, output_file)
