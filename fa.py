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
        nfa[stat+1].nextnode['eps'] = [nfa[stat+2],nfa[stat+4]]

if __name__ == '__main__':
    meow = Nfa()
    
         
        


    


        