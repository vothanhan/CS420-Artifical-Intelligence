import matplotlib.pyplot as plt
import networkx as nx
import Queue
import timeit
import re
import os,subprocess
import collections

def initiateGraph(node1,node2,w):
    #declare starting nodes, ending nodes and weight arrays
    
    
    #declare graph
    G = nx.Graph()   # or DiGraph, MultiGraph, MultiDiGraph, etc
    
    #add nodes, edges to the graph
    for i in range(len(node1)):
            G.add_edge(node1[i], node2[i], weight = w[i], color = "black")
    return (G,node1,node2,w)

def UCS(start,end,graph):
    Open=Queue.PriorityQueue()  #Initiate priority queue
    Closed=[]       #Initiate closed set
    Path={} #Initiate path
    Path[start]=[start] #The path from start is start city
    Cost={} #Initiate cost
    Cost[start]=0   #Cost from start to start is 0
    Open.push(start,0)  #Push start to open  
    while not Open.isEmpty():
        state=Open.pop()    #Pop the top of the queue
        Closed.append(state)    #Add the state to closed
        if state==end:      #If state is end state, stop the process and return the path
            return Path[state]
        Successors=graph.neighbors(state)   #Get all successor of the state
        for succ in Successors:     
            check=checkPrioQueue(Open.heap,succ)    #Check if state is in heap
            if check==-1 and succ not in Closed:    #If state is not in open and closed set, push it to open
                pushToFrontier(succ,graph,Open,Cost,Path,state)
            elif check!=-1 and Cost[succ]>int(graph[state][succ]['weight'])+Cost[state]:    #If state is in open but the cost is lower, push it to frontier
                pushToFrontier(succ,graph,Open,Cost,Path,state)
                if succ in Closed:  #If state is in closed, remove it from closed
                    Closed.remove(succ)
def GreedyBFS(start,end,graph,heuristic):
    Open=Queue.PriorityQueue()  #Greedy BFS is similar to UCS but instead of pushing the total cost, we push the heuristic of the state
    Closed=[]
    Path={}
    Path[start]=[start]
    Open.push(start,heuristic[start])
    while not Open.isEmpty():
        state=Open.pop()
        Closed.append(state)
        if state==end:
            return Path[state]
        Successors=graph.neighbors(state)
        for succ in Successors:
            check=checkPrioQueue(Open.heap,succ)
            if check==-1 and succ not in Closed:    #Same city have same heuristic, no need to have another case when city is already in open
                pushGreedy(succ,Open,Path,heuristic,state)

def Astar(start,end,graph,heuristic):
    Open=Queue.PriorityQueue()  #A* is similar to UCS but instead of pushing the total cost, we push the sum of heuristic of the successor and the cost of reaching that state
    Closed=[]
    Path={}
    Path[start]=[start]
    Cost={}
    Cost[start]=0
    Open.push(start,0)
    while not Open.isEmpty():
        state=Open.pop()
        Closed.append(state)
        if state==end:
            return Path[state]
        Successors=graph.neighbors(state)
        for succ in Successors:
            check=checkPrioQueue(Open.heap,succ)
            if check==-1 and succ not in Closed:
                pushAstar(succ,graph,Open,Cost,Path,heuristic,state)
            elif check!=-1 and Cost[succ]>Cost[state]+int(graph[state][succ]['weight']):
                pushAstar(succ,graph,Open,Cost,Path,heuristic,state)
                if succ in Closed:
                    Closed.remove(succ)
def GetHeuristic(h_path,heuristic):
    fh=open(h_path,"rb")
    lines=fh.readlines()
    for line in lines:
        words=line.split("\t")
        heuristic[words[0]]=int(words[1])

def pushGreedy(succ,frontier,path,heuristic,state): #The push function of Greedy, only push the heuristic of the successor
    frontier.push(succ,heuristic[succ])
    path[succ]=[]
    for node in path[state]:
        path[succ].append(node)
    path[succ].append(succ)
def pushAstar(succ,graph,frontier,pathCost,path,heuristic,state):   #The push function of A*, push the sum of total cost to current state and heuristic of successor
    frontier.push(succ,int(graph[state][succ]['weight']) + pathCost[state]+heuristic[succ])
    pathCost[succ] = int(graph[state][succ]['weight']) + pathCost[state]
    path[succ]=[]
    for node in path[state]:
        path[succ].append(node)
    path[succ].append(succ)
def pushToFrontier(succ,graph,frontier,pathCost,path,state):    #The push function of UCS, push the total cost to reach the successor
    frontier.push(succ,int(graph[state][succ]['weight']) + pathCost[state])
    pathCost[succ] = int(graph[state][succ]['weight']) + pathCost[state]
    path[succ]=[]
    for node in path[state]:
        path[succ].append(node)
    path[succ].append(succ)

def checkPrioQueue(frontier, i):    #Check if i is in the heap
    t = -1
    for k in frontier:
        t +=1
        if i in k:
            return t
    return -1
   


# start_node_and_goal_node is taken from the user's input; path is the result
# from the sortest path searching algorithm
def draw(start,goal, path,G,node1,node2,weight):
    for i in range(len(path)-1):
        G[path[i]][path[i+1]]['color'] = 'red'

    #resize the canvas
    plt.figure(num=None, figsize=(25, 25), dpi=800)
    
    #draw nodes and edges
    pos = nx.spring_layout(G) # using default position and layout
    
    nx.draw(G
            , pos
            , edges = G.edges()
            ,edge_color = [G[u][v]['color'] for u,v in G.edges()]
            , weight = [G[u][v]['weight'] for u,v in G.edges()]
            , width = "5")
    
    #draw edge label
    nx.draw_networkx_edge_labels(G, pos, edge_label = weight, font_size = 1)
    #node label
    label = {}  # dictionary
    for i in range(len(node1)):
        name = node1[i]
        label[name] = name
        name = node2[i]
        label[name] = name
        
    #customize and draw node label
    nx.draw_networkx_labels(G,pos,label,font_size = 14, font_weight = "heavy")
    
    #customize and draw node
    nx.draw_networkx_nodes(G, pos, nodelist = node1 + node2, node_color = 'w', node_shape = 's')
    
    #customize start node and goal node
    nx.draw_networkx_nodes(G, pos, nodelist = [start,goal], node_color = 'r', node_shape = 's' )
    
    
    #save img
    plt.savefig("Test.pdf", bbox_inches = "tight")

def execute(distance, heuristic,start,end,algo):
    node1=[]
    node2=[]
    weight=[]
    for c in distance.keys():   #Initiate city1,city2, and distance list
        c1,c2=c
        node1.append(str(c1))
        node2.append(str(c2))
        weight.append(int(distance[c]))
    path="" #Initiate path
    graph,node1,node2,weight=initiateGraph(node1,node2,weight)  #Initiate the graph
    allnode=graph.nodes()
    ok=0
    algorithm_name=""
    start_time=timeit.default_timer()   #Start the timer to calculate finding time
    if(algo==2):    #Start the algorithm depending on the selected algorithm
        path=UCS(start,end, graph)     
        algorithm_name="Uniform Cost Search"
    elif(algo==3):
        path=GreedyBFS(start,end,graph,heuristic)
        algorithm_name="Greedy Best First Search"
    elif(algo==1):
        path=Astar(start,end,graph,heuristic)
        algorithm_name="A*"
    else:
        print "Invalid algorithm"
        return
    elapsed = timeit.default_timer()-start_time #Get finding time
    start_time=timeit.default_timer()   #Start the timer to calculate drawing time
    if(path==None):
        return None,None,None
    draw(start,end,path,graph,node1,node2,weight) #comment out this to disable drawing, drawing take a lot of time
    elapsed2 = timeit.default_timer()-start_time    #Get drawing time
    os.system("start Test.pdf") #comment out this to disable open the map after complete
    return path,elapsed,elapsed2    #Return result