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


def gen_cands(word, *args):
    for func in args:
        for cand in func(word):
            yield (cand)


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


def valid(cand, word):
    lcand, lword = cand.lower(), word.lower()
    return (
        False
        if (lcand == lword)
        or (lcand == lword + "s")
        or (lword == lcand + "s")
        or (lword[-1] == "e" and lcand[-2:] == "ed")
        or ((lword, lcand) in filtered_swaps)
        or (lcand not in words)
        else True
    )


def formatted(cand, i, spell):
    return " ".join(ins(spell.split(" "), i, [cand.capitalize()], 1))


def gen_misspells(spells):
    for index, word, spell in spell_words(spells):
        for cand in gen_cands(word, addeds, removeds, replaceds, swappeds):
            if valid(cand, word):
                yield f'  "{formatted(cand, index, spell)}",\n'


def write_js_arr(name, items, file):
    file.write(f"const {name} = [\n")
    for item in items:
        file.write(item)
    file.write("]")


output_file = "misspells.js"
temp_file = "tmp_" + output_file

if __name__ == "__main__":
    with open(temp_file, "w") as f:
        write_js_arr("misspells", (ms for ms in gen_misspells(spells)), f)

    os.replace(temp_file, output_file)
