import random
from itertools import combinations,permutations
from binarytree import tree, Node

## to anaylze every cases, we use permutations of X to represent the order of
## these 6 value, the more previous, the more lower
## x2,x4,x1,x3,x5,x6 means x2<x4<x1<x3<x5<x6
X = ["x1","x2","x3","x4","x5","x6"]

state_list = [("",""),("x1","x2"),("x2","x1"),("x3","x4"),("x4","x3"),("x5","x6"),("x6","x5")]
## the search branch that player 1 moves on a, since we use the binarytree lib
## we build 3 subtrees for this branch depending on player 2's move
## s for swap. so three trees are ab,ac,as.
## Since the binarytree node's value must be number, so here we use a
## state_list for our node's value.
root_ab = Node(0)
root_ab.left = Node(1)
root_ab.right = Node(0)
root_ab.right.left = Node(2)
root_ab.right.right = Node(5)
# print(root_ab)
root_ac = Node(0)
root_ac.left = Node(3)
root_ac.right = Node(0)
root_ac.right.left = Node(4)
root_ac.right.right = Node(6)
# print(root_ac)
root_as = Node(0)
root_as.left = Node(2)
root_as.right = Node(4)
# print(root_as)

## the search branch that player 1 moves on b
root_ba = Node(0)
root_ba.left = Node(2)
root_ba.right = Node(0)
root_ba.right.left = Node(1)
root_ba.right.right = Node(3)
# print(root_ba)
root_bc = Node(0)
root_bc.left = Node(5)
root_bc.right = Node(0)
root_bc.right.left = Node(4)
root_bc.right.right = Node(6)
# print(root_bc)
root_bs = Node(0)
root_bs.left = Node(1)
root_bs.right = Node(6)
# print(root_bs)

## the search branch that player 1 moves on c
root_ca = Node(0)
root_ca.left = Node(4)
root_ca.right = Node(0)
root_ca.right.left = Node(1)
root_ca.right.right = Node(3)
# print(root_ca)
root_cb = Node(0)
root_cb.left = Node(6)
root_cb.right = Node(0)
root_cb.right.left = Node(2)
root_cb.right.right = Node(5)
# print(root_cb)
root_cs = Node(0)
root_cs.left = Node(3)
root_cs.right = Node(5)
# print(root_cs)

## according to the current X order recalculate the 9 search tree.
def Recalculate1(root,state_list,dict,pos=0):
    if(dict[state_list[root.left.value][pos]] > dict[state_list[root.right.value][pos]]):
        root.value = root.left.value
    else:
        root.value = root.right.value

def Recalculate2(root,state_list,dict):
    Recalculate1(root.right,state_list,dict,1)
    Recalculate1(root,state_list,dict)

def Recalculate3(root1,root2,root3,state_list,dict,pos=1):
    root = root1
    if(dict[state_list[root2.value][pos]] > dict[state_list[root.value][pos]]):
        root = root2
    if(dict[state_list[root3.value][pos]] > dict[state_list[root.value][pos]]):
        root = root3
    return root

def Recalculate4(state_list,dict):
    Recalculate2(root_ab,state_list,dict)
    Recalculate2(root_ac,state_list,dict)
    Recalculate1(root_as,state_list,dict)
    root_a = Recalculate3(root_ab,root_ac,root_as,state_list,dict)
    Recalculate2(root_ba,state_list,dict)
    Recalculate2(root_bc,state_list,dict)
    Recalculate1(root_bs,state_list,dict)
    root_b = Recalculate3(root_ba,root_bc,root_bs,state_list,dict)
    Recalculate2(root_ca,state_list,dict)
    Recalculate2(root_cb,state_list,dict)
    Recalculate1(root_cs,state_list,dict)
    root_c = Recalculate3(root_ca,root_cb,root_cs,state_list,dict)
    root = Recalculate3(root_a,root_b,root_c,state_list,dict,0)
    # print(state_list[root.value])
    return state_list[root.value]

## if we know X order, we can find the max(min(state))
def find(state_list,dict):
    result = state_list[1]
    for state in state_list[1:]:
        if(min(dict[state[0]],dict[state[1]]) > min(dict[result[0]],dict[result[1]])):
            result = state
    # print(result)
    return result


for perm in permutations(X):
    dict = {}
    i = 1
    for item in perm:
        dict[item] = i
        i = i+1
    result1 = Recalculate4(state_list,dict)
    result2 = find(state_list,dict)
    for item in result1:
        if(item != result2[0] and item != result2[1]):
            print("------------------------------------------------------------")
            print(dict)
