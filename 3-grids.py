import random
from itertools import combinations,permutations

positions = ['a','b','c']
players_number = 2

def State2():
    stateA = random.uniform(0,1.)
    return [stateA,1-stateA]

def State2Raw():
    stateA = random.uniform(0,1.)
    stateB = random.uniform(0,1.)
    return [stateA,stateB]

def State():
        # return ProbToInt(State2())
        return ProbToIntRaw(State2Raw())

def ProbToInt(list):
    new_list = [int(100*c) for c in list]
    new_list[-1] = new_list[-1] - sum(new_list) + 100
    return new_list

def ProbToIntRaw(list):
    new_list = [int(100*c) for c in list]
    return new_list

def GenStates(positions):
    states_space = {}
    for comb in combinations(positions,players_number):
        comb_state = State()
        tmp_comb={}
        for i in range(players_number):
            tmp_comb[comb[i]] = comb_state[i]
        for perm in permutations(comb):
                perm_name = ''.join(perm)
                perm_state = [tmp_comb[c] for c in perm]
                states_space[perm_name] = perm_state
    return states_space

def Project(player_id,position,states):
    project_states = {}
    for key, value in states.items():
        if key.find(position) == player_id-1:
            project_states[key] = value
    return project_states

def FindBestCurrent(player_id,states):#player_id 1,2,3
    best_state={}
    for key, value in states.items():
        best_state['comb']=key
        best_state['prob']=value
    for key, value in states.items():
        if value[player_id-1] > best_state['prob'][player_id-1]:
            best_state['comb']=key
            best_state['prob']=value
    return best_state

def Strategy(positions,state_space):
    tmp2={}
    for x in positions:
        # print("x\t{s}".format(s=x))
        tmp1={}
        for y in positions:
            if y == x:
                continue
            # print("y\t{s}".format(s=y))
            tmp = {}
            tmp[FindBestCurrent(2,Project(1,y,state_space))['comb']]=FindBestCurrent(2,Project(1,y,state_space))['prob']
            # print("Project(1,y,state_space)\t{s}".format(s=Project(1,y,state_space)))
            tmp[x+y]=state_space[x+y]
            # print("tmp\t{s}".format(s=tmp))
            tmp1[FindBestCurrent(1,tmp)['comb']]=FindBestCurrent(1,tmp)['prob']
            # print("tmp1\t{s}".format(s=tmp1))
        tmp1[FindBestCurrent(1,Project(2,x,state_space))['comb']]=FindBestCurrent(1,Project(2,x,state_space))['prob']
        # print("Project(2,x,state_space)\t{s}".format(s=Project(2,x,state_space)))
        tmp2[FindBestCurrent(2,tmp1)['comb']]=FindBestCurrent(2,tmp1)['prob']
        # print("tmp2\t{s}".format(s=tmp2))
    best = FindBestCurrent(1,tmp2)
    return best

for i in range(1000000):
    print("---------------------%d------------------------" %(i))
    state_space = {}
    state_space = GenStates(positions)
    # max_X max_Y(max_1(_,X),max_1((X,Y),max_2(Y,_)))
    best = Strategy(positions,state_space)
    # min_diff = min([abs(value[0]-value[1]) for key,value in state_space.items()])
    # print(min_diff)
    # if min_diff != abs(best['prob'][0]-best['prob'][1]):
    #     print(state_space)
    #     print(Strategy(positions,state_space))
    min_value = max([min(value) for key,value in state_space.items()])
    if min_value != min(best['prob']):
        print(state_space)
        print(Strategy(positions,state_space))
        break
