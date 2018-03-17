from tools import read_reg

class Nfanode(object):
    def __init__(self):
        self.nextnode = set()
    
class Nfa(object):
    stat = 0

    def __init__(self):
        self.stat = 0
        self.nfa = dict()
        self.end = False

    def union(self,chr1,chr2,stat,nfa):
        for i in range(6):
            tmp = stat+i
            nfa[tmp] = Nfanode()
            nfa[tmp].nextnode['eps'] = list()
        nstat = stat + 1
        nfa[nstat].nextnode['eps'] = [stat+1,stat+3]
        #for everyedge represent bt chr1 create the node 
        #chr1 need to do something,from 'a-z'to ord(a)-ord(z)
        for i in range(chr1):
            nfa[stat+1].nextnode[i] = [stat+2]
        
        for i in range(chr2):
            nfa[stat+1].nextnode[i] = [stat+2]
       
        nfa[stat+2].nextnode['eps'] = [stat+5]
        nfa[stat+4].nextnode['eps'] = [stat+5]
        


if __name__ == '__main__':
    meow = Nfa()
         
        


    


        
