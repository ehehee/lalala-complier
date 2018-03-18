from tools import read_reg,infix2postfix

class Nfanode(object):
    def __init__(self):
        self.nextnode = dict()
        self.end = False
    
class Nfa(object):

    def __init__(self):
        self.stat = 0
        self.nfa = dict()
       
    #the relation between nfa and nfanode need to rethink 
    def union(self,chr1,chr2,stat):
        nfa = dict()
        for i in range(6):
            tmp = stat+i
            nfa[tmp] = Nfanode()
            nfa[tmp].nextnode['eps'] = list()
        nstat = stat + 1
        nfa[nstat].nextnode['eps'] = [nstat+1,nstat+3]
        #for everyedge represent bt chr1 create the node 
        #chr1 need to do something,from 'a-z'to ord(a)-ord(z)
       
        nfa[nstat+1].nextnode[chr1] = [nstat+2]
        nfa[nstat+1].nextnode[chr2] = [nstat+2]
       
        nfa[nstat+2].nextnode['eps'] = [nstat+5]
        nfa[nstat+4].nextnode['eps'] = [nstat+5]
        return nfa 

def generate_nfa():
    flname = 'test.txt'
    regex = read_reg(flname)
    stat = 1
    unfa = Nfa()
    for (regtype,re) in regex.items():
        l = infix2postfix(re)
        symbolstack = list()
        if '.' not in l:
            start  =  l.find('[')
            end = l.find(']')
            p = l.find('|')
            cnt = 1
            while p > 0 :
                 symbolstack += l[start+1:p]
                 print(symbolstack)
                 start = p 
                 p = l.find('|',start+1)
                 cnt += 1
                 if p == -1:
                     symbolstack += l[p:end]
                     break
            symbolstack.remove('\\')
            if cnt != 0:
                unfa.union(symbolstack[cnt-1],symbolstack[cnt],stat)
                

                #todo


if __name__ == '__main__':
    meow = Nfa()
         
        


    


        
