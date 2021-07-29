from queue import PriorityQueue

class State(object):
    
    def __init__(self, value, parent, start=0, goal=0):
        self.children = []   #list of all membering possibilities
        self.parent = parent #current parent
        self.value = value   # current value
        self.dist = 0        #current distance
        
        #checks if parent is plucked
        if parent:
            self.start = parent.start  #start state
            self.goal = parent.goal    #goal state
            self.path = parent.path[:] #copies parent path
            self.path.append(value)    #store all values in our path
            
        else:
            self.path = [value] #sets the path with a list of objects with the current value
            self.start = start  #start state
            self.goal = goal    #goal state
            
    def GetDistance(self):
        pass
    def CreateChildren(self):
        pass
    
class State_String(State):
    
    def __init__(self, value, parent, start=0, goal=0 ):
        super(State_String, self).__init__(value, parent, start, goal) 
        self.dist = self.GetDistance() #overrides distance variable
        
    def GetDistance(self):
        #check if it's reached the goal
        if self.value == self.goal:
            return 0
        dist = 0
        
        for i in range(len(self.goal)):
            letter = self.goal[i] #current letter
            dist += abs(i - self.value.index(letter)) #finds the index of the letter in the current value 
            
        return dist
    
    #generate the children
    def CreateChildren(self):
        #if no children, then generate a child
        if not self.children:
            for i in range(len(self.goal)-1): #loop through all the possible combinations
                val = self.value
                #switches the second and first letter
                val = val[:i] + val[i+1] + val[i] + val[i+2:]
                #creates a child with theh value of the child and self parent info
                child = State_String(val, self)
                self.children.append(child)
                
#solver
class A_Star_Solver:
    
    def __init__(self, start, goal):
        self.path = [] #stores final solution
        self.visitedQueue = [] #keeps track of the children visited
        self.priorityQueue = PriorityQueue()
        self.start = start
        self.goal = goal
        
    def Solve(self):
        startState = State_String(self.start,0,self.start,self.goal)
        count = 0
        
        #used to add children
        self.priorityQueue.put((0,count,startState))
        
        #work horse
        while(not self.path and self.priorityQueue.qsize()):
            closesetChild = self.priorityQueue.get()[2] #getting topmost value from the priority queue
            closesetChild.CreateChildren()
            self.visitedQueue.append(closesetChild.value) #keep track all the children that we are visited
            for child in closesetChild.children:
                if child.value not in self.visitedQueue:
                    count += 1
                    if not child.dist:
                        self.path = child.path
                        break
                    self.priorityQueue.put((child.dist,count,child))
                    
        if not self.path:
            print("Goal of  is not possible!" + self.goal)
        
        return self.path
        
if __name__ == '__main__':
    start = "hema"
    goal = "mahe"
    print("Started...")
    a = A_Star_Solver(start, goal)
    a.Solve()
    
    for i in range(len(a.path)):
        print("{0}){1}".format(i, a.path[i]))