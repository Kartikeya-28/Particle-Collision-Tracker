class Linked_list():   # created linked list 
    pass
    class Node():
        def __init__(self,i,collision_time,m): # the node has 3 element : i , time of collision (from t = 0) , and m which is the index same as the index in a list , which I will use in heap_index (a list) .  
            self._collision_time = collision_time
            self._m = m
            self._i = i
            self._prev = None
            self._next = None

    def __init__(self):    # maintained head and last for the linked list . Created a list which can store address of the elements , so wherever they are present in a heap ,they can be accessed from their addresses stored in the list.
        self._head = None
        self._last = None
        self._l = []

    def is_Empty(self):
        if self._head == None :
            return True 
        else :
            return False

    def push(self,i,y,m):
        ptr = self.Node(i,y,m)
        self._l.append(ptr)
        if self._head == None:
            self._head = ptr
            self._last = ptr
        else :
            self._last._next = ptr
            ptr._prev = self._last
            self._last = ptr
            

    def pop(self):
        if Linked_list.is_Empty(self) == False :
            popped = self._last
            new_last = self._last._prev
            if self._head != self._last :
                new_last._next = None
                self._last = new_last
            else :
                self._head = None
                self._last = None
        
            return popped._collision_time

# heap_index is another list which stores the address of the elements in the same order as that of the heap i.e the 0th index of heap_index refers to the minimum(or root) element of the heap and so on .
def swap(heap_index,x1,x2):   # swap the addresses and update the m of their nodes to their new value.
    u_initial = heap_index[x1]
    x2_val = heap_index[x2]
    heap_index[x1] = x2_val 
    heap_index[x2] = u_initial
    heap_index[x2]._m = x2
    heap_index[x1]._m = x1
    m = x2  

def Heap_up(i,Address_list,heap,heap_index):  # Performs heap up operation.
    m = Address_list[i]._m
    u = heap_index[m]
    while ((u._collision_time < heap_index[(m-1)//2]._collision_time) or (u._collision_time == heap_index[(m-1)//2]._collision_time and u._i < heap_index[(m-1)//2]._i)):
        a = m
        b = (m-1)//2
        swap(heap_index,a,b) 
        m = b
        u = heap_index[b]
        if m < 1:
            break

def Heap_Down(i,Address_list,heap,heap_index):  # Performs heap down operation .
    m = Address_list[i]._m
    u = heap_index[m]
    child_1 = 2*m+1
    child_2 = 2*m+2

    if child_1 <= len(heap_index)-1 :
        if child_1 == len(heap_index)-1:   # if the last parent has only one child then take its another child(right child)  = left child .
            child_2 = child_1

        while ((u._collision_time > heap_index[child_1]._collision_time) or (u._collision_time > heap_index[child_2]._collision_time) or (u._collision_time == heap_index[child_1]._collision_time and u._i > heap_index[child_1]._i) or (u._collision_time == heap_index[child_2]._collision_time and u._i > heap_index[child_2]._i)) :   # condition impose on equality or loop termination
            min = heap_index[child_1]
            if heap_index[child_1]._collision_time > heap_index[child_2]._collision_time :
                min = heap_index[child_2]
            elif heap_index[child_1]._collision_time == heap_index[child_2]._collision_time :
                if heap_index[child_1]._i > heap_index[child_2]._i:
                    min = heap_index[child_2]

            a = min._m
            b = m
            
            swap(heap_index,a,b)
            m = a  
            u = heap_index[a]
            child_1 = 2*m+1
            child_2 = 2*m+2

            if 2*m + 1 > len(heap_index)-1 : # if we reached at mth index which does not have any child then break.
                break
            elif 2*m+1 == len(heap_index)-1:
                child_2 = child_1

def Build_Heap(Address_list,linked_list,heap_index):  # Builds the heap .
    for u in range (0,len(heap_index)) :
        i = heap_index[len(heap_index)-1-u]._i
        
        Heap_Down(i,Address_list,linked_list,heap_index)

def enqueue(i,time,heap_index,Address_list,heap):   # enqueue a new element in the heap.
    heap.push(i,time,len(heap_index))
    enqueued_element = Address_list[-1]
    heap_index.append(enqueued_element)
    Address_list[i] = enqueued_element
    Address_list.pop(-1)
    Heap_up(i,Address_list,heap,heap_index)

def extract_min(heap,Address_list,heap_index):  # extracting the root from heap and updating the address list as -1 which indicates that it is not present in the heap.
    if len(heap_index) > 0: 
        i_of_min = heap_index[0]._i
        time_min = heap_index[0]._collision_time
        swap(heap_index,0,len(heap_index)-1)
        heap.pop()
        heap_index.pop(-1)
        Address_list[i_of_min] = -1
        if len(heap_index) > 0:
            Heap_Down(heap_index[0]._i,Address_list,heap,heap_index)
        return time_min

def collision_time(i,p1,p2,vel_list):  
    v1 = vel_list[i]
    v2 = vel_list[i+1]
    time = -1
    if v1 > v2 :
        time = (p2-p1)/(v1-v2)
    return time

def vel_update(i,M,v):
    m1 = M[i]
    m2 = M[i+1]
    v1 = v[i]
    v2 = v[i+1]

    v[i] = ((m1-m2)/(m1+m2))*v1 + ((2*m2)/(m1+m2))*v2    
    v[i+1] = ((2*m1)/(m1+m2))*v1 - ((m1-m2)/(m1+m2))*v2   

# Because I am only updating the position of collision for the colliding objects , if I need to update the other positions I will update by initial position + velocity*(total time elapsed - the time at which this object(whose position is being updated) had the collision)
def position_update(i,Address_list,x,v,time_btw_collision,num_collision):
    collision = num_collision[i]
    x[i] += v[i]*(time_btw_collision[-1] - time_btw_collision[collision])


def listCollisions(M,x,v,m,T):
    heap = Linked_list()
    heap_index = []
    num_collision = [] # It stores the Collision_number at which the ith object had a collision for ease of update of position . 
    index = 0
    for i in range (0,len(M)-1):
        time  = collision_time(i,x[i],x[i+1],v)
        num_collision.append(0) # 0 appended n-1 times
        if time != -1:
            heap.push(i,time,index)
            heap_index.append(heap._l[i])
            index += 1
        else:
            heap._l.append(-1)  # If no possibility of collision append -1 in the address list which shows that this element is not present in the heap .
    num_collision.append(0)   # 0 appended at the nth time . All objects have 0 collision in the beginning hence appended 0.
    collisions_list = []  # The final list which needs to be returned .

    Build_Heap(heap._l,heap,heap_index)
    
    collisions = 0  
    time_elapsed = 0
    t_check = 0
    if len(heap_index) != 0 :
        t_check = heap_index[0]._collision_time 
    time_between_collision = [0]
    
    while (collisions < m) and (t_check <= T ) :
        if len(heap_index) != 0 :
            i = heap_index[0]._i
            time_elapsed = heap_index[0]._collision_time #time_elapsed
            time_between_collision.append(time_elapsed)
            position_update(i,heap._l,x,v,time_between_collision,num_collision) 
            position_update(i+1,heap._l,x,v,time_between_collision,num_collision) 
            
            extract_min(heap,heap._l,heap_index)
    
            vel_update(i,M,v)
        
            position_of_collision = x[i]
            if i != 0 :
                n_1 = num_collision[i-1]
                p1 = x[i-1]+v[i-1]*(time_elapsed-time_between_collision[n_1]) # posiiton of the i-1 th object
                
                t1 = collision_time(i-1,p1,x[i],v)
                
                if t1 >= 0 :
                    t1 += time_elapsed #(total time from t = 0)
                    
                    if heap._l[i-1] == -1:  # if element not in heap enqueue otherwise just update the collision time for i-1 and correspondingly heap up or heap down .
                        enqueue(i-1,t1,heap_index,heap._l,heap)
                    else :                   
                        heap._l[i-1]._collision_time = t1
                       
                        if heap._l[i-1]._m >= 1 : 
                            if (heap_index[(heap._l[i-1]._m-1)//2]._collision_time <= t1):
                                Heap_Down(i-1,heap._l,heap,heap_index)
                            elif (heap_index[(heap._l[i-1]._m-1)//2]._collision_time >= t1):
                                Heap_up(i-1,heap._l,heap,heap_index)
                        else:
                            Heap_Down(i-1,heap._l,heap,heap_index)
                        
            
            if i != len(M) -2:
                n_2 = num_collision[i+2]
                p2 = x[i+2]+v[i+2]*(time_elapsed - time_between_collision[n_2]) # position of the i+2 th object

                t2 = collision_time(i+1,x[i+1],p2,v)   
                
                if t2 >= 0 :
                    t2 += time_elapsed #(total time from t = 0)
                    
                    if heap._l[i+1] == -1:
                        enqueue(i+1,t2,heap_index,heap._l,heap)
                    else :
                        heap._l[i+1]._collision_time = t2
                        if (heap._l[i+1]._m >= 1) :
                            if (heap_index[(heap._l[i+1]._m-1)//2]._collision_time <= t2):  
                                Heap_Down(i+1,heap._l,heap,heap_index)
                            elif (heap_index[(heap._l[i+1]._m-1)//2]._collision_time >= t2):
                                Heap_up(i+1,heap._l,heap,heap_index)
                        else :
                            Heap_Down(i+1,heap._l,heap,heap_index)
            
            collisions_list.append((time_elapsed,i,position_of_collision))  # appending the (t,i,x) tuple in the final answer list .
            if len(heap_index) != 0 :
                t_check = heap_index[0]._collision_time
            else :
                break

            
            collisions += 1
            num_collision[i] = collisions   # changing the collision number for i to the collision th number at which this collision happened . 
            num_collision[i+1] = collisions # changing the collision number for i+1 to the collision th number at which this collision happened .
        else :
            break
    return collisions_list



        
        

    
