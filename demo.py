import nltk
# print(nltk.download('averaged_perceptron_tagger'))
import random
import numpy as np
from collections import Counter, OrderedDict
from nltk.tree import Tree
import os
from IPython.display import Image, display
from nltk.draw import TreeWidget
from nltk.draw.util import CanvasFrame
flatten = lambda l: [item for sublist in l for item in sublist]
random.seed(1024)

if __name__ == '__main__':
    def draw_nltk_tree(tree):
        cf = CanvasFrame()
        tc = TreeWidget(cf.canvas(), tree)
        tc['node_font'] = 'arial 15 bold'
        tc['leaf_font'] = 'arial 15'
        tc['node_color'] = '#005990'
        tc['leaf_color'] = '#3F8F57'
        tc['line_color'] = '#175252'
        cf.add_widget(tc, 50, 50)
        cf.print_to_file('tmp_tree_output.ps')
        cf.destroy()
        os.system('convert tmp_tree_output.ps tmp_tree_output.png')
        display(Image(filename='tmp_tree_output.png'))
        # os.system('rm tmp_tree_output.ps tmp_tree_output.png')


    class TransitionState(object):
        def __init__(self, tagged_sent):
            self.root = ('ROOT', '<root>', -1)
            self.stack = [self.root]
            self.buffer = [(s[0], s[1], i) for i, s in enumerate(tagged_sent)]
            self.address = [s[0] for s in tagged_sent] + [self.root[0]]
            self.arcs = []
            self.terminal = False

        def __str__(self):
            return 'stack : %s \nbuffer : %s' % (str([s[0] for s in self.stack]), str([b[0] for b in self.buffer]))

        def shift(self):
            if len(self.buffer) >= 1:
                self.stack.append(self.buffer.pop(0))
            else:
                print("Empty buffer")

        def left_arc(self, relation=None):
            if len(self.stack) >= 2:
                arc = {}
                s2 = self.stack[-2]
                s1 = self.stack[-1]
                arc['graph_id'] = len(self.arcs)
                arc['form'] = s1[0]
                arc['addr'] = s1[2]
                arc['head'] = s2[2]
                arc['pos'] = s1[1]
                if relation:
                    arc['relation'] = relation
                self.arcs.append(arc)
                self.stack.pop(-2)          #####

            elif self.stack == [self.root]:
                print("Element Lacking")

        def right_arc(self, relation=None):
            if len(self.stack) >= 2:
                arc = {}
                s2 = self.stack[-2]
                s1 = self.stack[-1]
                arc['graph_id'] = len(self.arcs)
                arc['form'] = s2[0]
                arc['addr'] = s2[2]
                arc['head'] = s1[2]
                arc['pos'] = s2[1]
                if relation:
                    arc['relation'] = relation
                self.arcs.append(arc)
                self.stack.pop(-1)

            elif self.stack == [self.root]:
                print("Element Lacking")

        def is_done(self):
            return len(self.buffer) == 0 and self.stack == [self.root]

        def to_tree_string(self):
            if self.is_done() == False:
                return None
            ingredient = []
            for arc in self.arcs:
                ingredient.append([arc['form'], self.address[arc['head']]])
            ingredient = ingredient[-1:] + ingredient[:-1]
            return self._make_tree(ingredient, 0)

        def _make_tree(self, ingredient, i, new=True):
            # '(ROOT (has He (control good) .))'
            if new:
                treestr = "("
                treestr += ingredient[i][0]
                treestr += " "
            else:
                treestr = ""
            ingredient[i][0] = "CHECK"
            parents, _ = list(zip(*ingredient))

            if ingredient[i][1] not in parents:
                treestr += ingredient[i][1]
                return treestr
            else:
                treestr += "("
                treestr += ingredient[i][1]
                treestr += " "
                for node_i, node in enumerate(parents):
                    if node == ingredient[i][1]:
                        treestr += self._make_tree(ingredient, node_i, False)
                        treestr += " "

                treestr = treestr.strip()
                treestr += ")"
            if new:
                treestr += ")"
            return treestr

    state = TransitionState(nltk.pos_tag("The brown fox jumped with joy over the fence".split()))

    state.shift()
    state.shift()
    state.shift()
    state.left_arc()
    state.left_arc()
    state.shift()
    state.left_arc()
    state.shift()
    state.shift()
    state.right_arc()
    state.right_arc()
    state.shift()
    state.shift()
    state.shift()
    state.left_arc()
    state.right_arc()
    state.right_arc()
    state.right_arc()
    state.is_done()

    state.to_tree_string()
    print(Tree.fromstring(state.to_tree_string()))

    draw_nltk_tree(Tree.fromstring(state.to_tree_string()))

