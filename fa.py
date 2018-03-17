from tools import read_reg,infix2postfix

class Nfanode(object):
    def __init__(self):
        self.nextnode = set()
        self.end = False
    
class Nfa(object):

    def __init__(self):
        self.stat = 0
        self.nfa = dict()
       
    #the relation between nfa and nfanode need to rethink 
    def union(self,chr1,chr2,stat):
        for i in range(6):
            tmp = stat+i
            nfa_node[tmp] = Nfanode()
            nfa_node[tmp].nextnode['eps'] = list()
        nstat = stat + 1
        nfa_node[nstat].nextnode['eps'] = [nstat+1,nstat+3]
        #for everyedge represent bt chr1 create the node 
        #chr1 need to do something,from 'a-z'to ord(a)-ord(z)
       
        nfa_node[nstat+1].nextnode[chr1] = [nstat+2]
        nfa_node[nstat+1].nextnode[chr2] = [nstat+2]
       
        nfa_node[nstat+2].nextnode['eps'] = [nstat+5]
        nfa_node[nstat+4].nextnode['eps'] = [nstat+5]
        return 

def generate_nfa():
    flname = 'test.txt'
    regex = read_reg(flname)
    stat = 0
    unfa = Nfa()
    for (regtype,re) in regex.items():
        l = infix2postfix(re)
        symbolstack = list()
        if '.' not in l and '*' not in l:
            start  =  l.find('[')
            end = l.find(']')
            p = l.find('|')
            cnt = 1
            while p > 0 :
                 symbolstack += l[start+1:p-1]
                 start = p 
                 p = l.find('|',start+1)
                 cnt += 1
                 if p == -1:
                     symbolstack += l[p:end]
            
            if cnt != 0:
                #unfa.union()
                #todo


        
            symbolstack += l[p,q-1]

        print(re,infix2postfix(x))


if __name__ == '__main__':
    meow = Nfa()
         
        


    


        
