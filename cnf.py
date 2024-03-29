from sys import stdin, stderr
from json import loads, dumps
import copy


def cnf(tree):
    n = len(tree)
    # eliminate unary branching by merging nodes
    if n == 2:
        if not isinstance(tree[1], str):
            nodes = copy.deepcopy(tree[1][1:])
            tree[0] = tree[0] + "+" + tree[1][0]
            del tree[1]
            for i in nodes:
                tree.append(i)
            cnf(tree)
    # eliminate n-ary branching subtrees by inserting additional nodes
    elif n > 3:
        nodes = copy.deepcopy(tree[2:])
        del tree[3:]
        tree[2] = [tree[0] + "|" + tree[1][0]]
        for i in nodes:
            tree[2].append(i)
        cnf(tree)
    else:
        cnf(tree[1])
        cnf(tree[2])


def is_cnf(tree):
    n = len(tree)
    if n == 2:
        return isinstance(tree[1], str)
    elif n == 3:
        return is_cnf(tree[1]) and is_cnf(tree[2])
    else:
        return False


def words(tree):
    if isinstance(tree, str):
        return [tree]
    else:
        ws = []
        for t in tree[1:]:
            ws = ws + words(t)
        return ws


if __name__ == "__main__":

    for line in stdin:
        tree = loads(line)
        sentence = words(tree)
        input = str(dumps(tree))
        cnf(tree)
        if is_cnf(tree) and words(tree) == sentence:
            print(dumps(tree))
        else:
            print("Something went wrong!", file=stderr)
            print("Sentence: " + " ".join(sentence), file=stderr)
            print("Input: " + input, file=stderr)
            print("Output: " + str(dumps(tree)), file=stderr)
            exit()
