import random

graph = {
    'a':['b','c'],
    'b':['d'],
    'c':['e'],
    'd':[],
    'e':['b'],
    'f':['d']
}

linkable = {
    1:[2,3],
    2:[4,5],
    3:[6],
    4:[],
    5:[7,8],
    6:[9],
    7:[],
    8:[],
    9:[],
}

def print_graph(graph, node, depth = 0):
    # print(node,end='')
    # if graph[node]:
    #     print("->",end='')
    # for dest in graph[node]:
    #     print_graph(dest)
    # if not graph[node]:
    #     print()
    print("\t" * depth,node,"at depth",depth)
    for dest in graph[node]:
        print_graph(graph, dest, depth + 1)

N = 5

def get_random_children(n):
    return sorted(random.sample(range(n + 1, N), N-n-1))

print_graph(graph, 'a')
print('\n')
print_graph(linkable, 1)
print('\n')

rand = {}
for i in range(1,N):
     rand[i] = get_random_children(i)
print_graph(rand, 1)
