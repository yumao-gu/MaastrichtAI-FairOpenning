from itertools import combinations,permutations
import random

positions = ['a','b','c','d']
players = ['A','B','C']
low_prob = 0.
players_number = 3
test_num = 10
rule = 2

def State3():
    stateA = random.uniform(low_prob,1.)
    stateB = random.uniform(low_prob,1-stateA)
    return [stateA,stateB,1-stateA-stateB]

def State4():
    stateA = random.uniform(low_prob,1.)
    stateB = random.uniform(low_prob,1-stateA)
    stateC = random.uniform(low_prob,1-stateA-stateB)
    return [stateA,stateB,stateC,1-stateA-stateB-stateC]

def State(players_number):
    if players_number == 3:
        return ProbToInt(State3())
    elif players_number == 4:
        return ProbToInt(State4())
    else:
        print("State Do not support this players_number")

def ProbToInt(list):
    new_list = [int(100*c) for c in list]
    new_list[-1] = new_list[-1] - sum(new_list) + 100
    return new_list

def GenStates(positions,players_number):
    states_space = {}
    for comb in combinations(positions,players_number):
        comb_state = State(players_number)
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

def ReProject(id1,id2,state):
    string = state['comb']
    temp = string[id2]
    trailer = string[id2+1:] if id2 + 1 < len(string) else ''
    string = string[0:id2] + string[id1] + trailer
    string = string[0:id1] + temp + string[id1+1:]
    state['comb'] = string
    state['prob'][id1],state['prob'][id2] = state['prob'][id2],state['prob'][id1]

def ReOrder(id,state):
    list1 = state["prob"][id:]
    list2 = list(state["comb"][id:])
    list1, list2 = (list(t) for t in zip(*sorted(zip(list1, list2))))
    state["prob"][id:] = list1
    state["comb"] = state["comb"][:id]+"".join(list2)

def FindBest(rule,player_id,states):
    assert player_id <= players_number
    if player_id == players_number:
        return FindBestCurrent(player_id,states)
    elif rule == 0:
        return FindBestCurrent(player_id,states)
    elif rule == 1:
        return FindBestToNext(player_id,states)
    elif rule == 2:
        return FindBestToEnd(player_id,states)
    else:
        print("Do not support the rule")

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

def FindBestToNext(player_id,states):#player_id 1,2,3
    assert player_id < players_number
    best_state={}
    for key, value in states.items():
        best_state['comb']=key
        best_state['prob']=value
    for key, value in states.items():
        # print(best_state)
        if min(value[player_id-1],value[player_id]) \
        >= min(best_state['prob'][player_id-1],best_state['prob'][player_id]):
            best_state['comb']=key
            best_state['prob']=value
            # print(best_state)
            if value[player_id-1] >= value[player_id]:
                # print("ReProject")
                ReProject(player_id-1,player_id,best_state)
                # print(best_state)
    assert best_state['prob'][player_id-1]<=best_state['prob'][player_id]
    return best_state

def FindBestToEnd(player_id,states):#player_id 1,2,3
    best_state={}
    for key, value in states.items():
        best_state['comb']=key
        best_state['prob']=value
    for key, value in states.items():
        if min(value[player_id-1:]) >= min(best_state['prob'][player_id-1:]):
            best_state['comb']=key
            best_state['prob']=value
            ReOrder(player_id-1,best_state)
    return best_state

def FindFair_d(states):
    fair_state={}
    for key, value in states.items():
        fair_state['comb']=key
        fair_state['prob']=value
    for key, value in states.items():
        if min(value) > min(fair_state['prob']):
            fair_state['comb']=key
            fair_state['prob']=value
    return fair_state

def FindFair_D(states):
    fair_state={}
    for key, value in states.items():
        fair_state['comb']=key
        fair_state['prob']=value
    for key, value in states.items():
        if max(value) < max(fair_state['prob']):
            fair_state['comb']=key
            fair_state['prob']=value
    return fair_state

def FindFair_D_bar(states,players_number):
    fair_state={}
    for key, value in states.items():
        fair_state['comb']=key
        fair_state['prob']=value
    best_D_bar = 0.
    for prob in fair_state['prob']:
        best_D_bar += abs(prob - 1./players_number)
    for key, value in states.items():
        D_bar = 0.
        for prob in value:
            D_bar += abs(prob - 100./players_number)
        if D_bar < best_D_bar:
            best_D_bar = D_bar
            fair_state['comb']=key
            fair_state['prob']=value
    return fair_state

def Strategy3(states_space):
    bestAs = {}
    for positionA in positions:
        projectA = Project(1,positionA,states_space)
        bestBs = {}
        for positionB in positions:
            if positionA is not positionB:
                projectB = Project(2,positionB,projectA)
                bestCs = {}
                for positionC in positions:
                    if positionA is not positionC and positionB is not positionC :
                        projectC = Project(3,positionC,projectB)
                        tmpC=FindBest(rule,3,projectC)
                        print("tmpC\t{s}".format(s=tmpC))
                        bestCs[tmpC['comb']] = tmpC['prob']
                print("bestCs\t{s}".format(s=bestCs))
                bestC = FindBest(rule,3,bestCs)
                print("bestC\t{s}".format(s=bestC))
                bestBs[bestC['comb']] = bestC['prob']
        print("bestBs\t{s}".format(s=bestBs))
        bestB = FindBest(rule,2,bestBs)
        print("bestB\t{s}".format(s=bestB))
        bestAs[bestB['comb']] = bestB['prob']
    print("bestAs\t{s}".format(s=bestAs))
    return FindBest(rule,1,bestAs)

def Strategy4(states_space):
    bestAs = {}
    for positionA in positions:
        projectA = Project(1,positionA,states_space)
        bestBs = {}
        for positionB in positions:
            if positionA is not positionB:
                projectB = Project(2,positionB,projectA)
                bestCs = {}
                for positionC in positions:
                    if positionA is not positionC and positionB is not positionC :
                        projectC = Project(3,positionC,projectB)
                        bestDs = {}
                        for positionD in positions:
                            if positionA is not positionD and positionB is not positionD and  positionC is not positionD:
                                projectD = Project(4,positionD,projectC)
                                tmpD=FindBest(rule,4,projectD)
                                bestDs[tmpD['comb']] = tmpD['prob']
                        bestD = FindBest(rule,4,bestDs)
                        bestCs[bestD['comb']] = bestD['prob']
                bestC = FindBest(rule,3,bestCs)
                bestBs[bestC['comb']] = bestC['prob']
        bestB = FindBest(rule,2,bestBs)
        bestAs[bestB['comb']] = bestB['prob']
    return FindBest(rule,1,bestAs)

def Strategy(states_space,players_number):
    if players_number == 3:
        return Strategy3(states_space)
    elif players_number == 4:
        return Strategy4(states_space)
    else:
        print("Strategy Do not support this players_number")

if __name__ == "__main__":
    for i in range(test_num):
        print("---------------------%d------------------------" %(i))
        states_space = GenStates(positions,players_number)
        print(states_space)
        fair_d = FindFair_d(states_space)
        fair_D = FindFair_D(states_space)
        fair_D_bar = FindFair_D_bar(states_space,players_number)
        print("Fair_d:  \t{key}\t{value}".format(key=fair_d['comb'],value=fair_d['prob']))
        print("Fair_D:  \t{key}\t{value}".format(key=fair_D['comb'],value=fair_D['prob']))
        print("Fair_D_bar:  \t{key}\t{value}".format(key=fair_D_bar['comb'],value=fair_D_bar['prob']))
        solution = Strategy(states_space,players_number)
        print("Solution:  \t{key}\t{value}".format(key=solution['comb'],value=solution['prob']))
