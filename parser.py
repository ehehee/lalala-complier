from queue import Queue
from collections import defaultdict
from prettytable import PrettyTable

def parse_convert(s):
    """
    :param s: 字符串
    :return: 转换转义符之后的字符串
    """
    s = s.replace(r"\n", "\n")
    s = s.replace(r"\r", "\r")
    s = s.replace(r"\t", "\t")
    return s
    
class ItemCluster(object):
    def __init__(self):
        self.items = set()
        self.nextitem = defaultdict(tuple)

    def add_item(self,i_head, i_left, i_right, i_tail, num):
        self.items.add((i_head, i_left, i_right, i_tail, num))
    
class Parser(object):
    def __init__(self, filename='parse.txt'):
        self.filename = filename
        self.prs = defaultdict(list)
        self.termset = set()
        self.ntermset = set()
        self._itemcluster = dict()
        self._items = set()
        self._table = defaultdict(dict)
        self.first = defaultdict(set)
        self.cnt = 0

    def next_cnt(self):
        self.cnt+=1
        return self.cnt

    def read_parse(self):
        self.cnt = 0
        with open(self.filename) as reader:
            r = reader.readlines()
            for line in r:
                if(line[0] == '#'):
                    continue
                key,value  = line.split(" ::= ")
                key = key[1:-1]
                self.ntermset.add(key)
                value = value.strip().split('|')
                x = [(self.next_cnt(),[V[1:-1] for V in v.split()]) for v in value]
                for _,i in x:
                    for j in i:
                        self.termset.add(j)
                self.prs[key].extend(x)
            self.termset = self.termset.difference(self.ntermset)

    def closure(self,itemset): #itemset为itemcluster
        que = Queue()
        for item in itemset.items:
            que.put(item)
        while not que.empty():
            it = que.get()
            if len(it[2]) >0 and it[2][0] in self.ntermset:
                l = list()
                if len(it[2])>1:
                    l = list(it[2][1:-1])+list(it[2][-1])
                    l = self.get_first(l)
                if len(l)==0:
                    l = list(it[3])
                for _, val in self.prs[it[2][0]]:
                    newit = (tuple(it[2][0]),(),tuple(val),it[3],self.prs[it[2][0]][0][0])
                    if newit not in itemset.items:
                        #print(val)
                        #print(self.prs[it[2][0]][0])
                        for lla in self.prs[it[2][0]]:
                            if lla[1] == val:
                                itemset.add_item(tuple(it[2][0]),(),tuple(val),frozenset(l),lla[0])
                        que.put(newit)
        return itemset
   
    def build_first(self): #构建文法的first集
        num = 0
        while True:
            for t in self.ntermset:
                for i in self.prs[t]:
                    #print(i[1][0])
                    if i[1][0] in self.termset:
                        if i[1][0] == 'eps' and len(i[1])>1:
                            self.first[t].add(self.first[i[1][1]])
                        else:
                            self.first[t] |= {i[1][0]}
                    else: 
                        self.first[t] |= self.first[i[1][0]]
            t_num = 0
            for t in self.ntermset:
                t_num += len(self.first[t])
            if t_num == num:
                return
            num = t_num

    def get_first(self,l = None): #获取list l的first集
        ret = set()
        for i in l:
            if i in self.termset:
                ret.add(i)
                break
            ret |= self.first[i]
            if 'eps' not in self.first[i]:
                break
        if 'eps' in ret:
            ret.remove('eps')
        return ret
    
    def xurtx_go(self,itemclstr,psymbol):
        newitemclstr = ItemCluster()
        for i in itemclstr.items:
            if len(i[2]) == 0:
                continue
            if i[2][0] == psymbol:
                if len(i[2])>1:
                    t1 = tuple(list(i[1])+list(i[2][0]))
                    t2 = tuple(list(i[2][1:-1])+list(i[2][-1]))
                    newitemclstr.add_item(i[0],t1,t2,i[3],i[4])
                else:
                    t3 = tuple(list(i[1])+list(i[2][0]))
                    newitemclstr.add_item(i[0],t3,(),i[3],i[4])
        return self.closure(newitemclstr)

def init_parser(parsername):
    parsername.read_parse()
    parsername.build_first()
    parsername.termset|= {'#'}

def init_itemcluster(itemname,parsername):
    itemname.add_item("S'",(),('S'),frozenset('#'),1)
    parsername.closure(itemname)
    parsername._itemcluster[tuple(itemname.items)] = 0
    parsername._items.add(tuple(itemname.items))

def create_itemcluster(itemname,parsername):
    que = Queue()
    que.put(itemname)
    nowstat = -1
    num = 0
    while not que.empty():
        nowstat += 1
        q = que.get()
        goset = set()
        for it in q.items:
            if(len(it[2])>0):
                goset |= set(it[2][0])
        print(q.items)
        for g in goset :
            num += 1
            tmp = parsername.xurtx_go(q,g)
            tu = tuple(tmp.items)
            if tu in parsername._items:
                q.nextitem[g] = tmp
                num-=1
                continue
            else:
                parsername._items.add(tu)
                parsername._itemcluster[tu] = num
                q.nextitem[g] = tmp
                que.put(tmp)
           # print(g,num,tu,"llllll")
    print("项目集：")
    for i,j in parser_la._itemcluster.items():
        print(j)
        for item in i:
            print(item[0],"->",item[1],'.',item[2],item[3])

def create_table(itemname,parsername):
    for i,j in parsername._itemcluster.items():
        for n in parsername.termset|parsername.ntermset:
            if n !="S'":
                parsername._table[j][n]= None
        for item in i:
            if item[2] == ():
                for x in item[3]:
                    parsername._table[j][x] = 'r'+str(item[4])
                    #print(j,x,'r'+str(item[4]))
    que = Queue()
    que.put(itemname)
    while not que.empty():
        q = que.get()
        for i,j in q.nextitem.items():
            num = parsername._itemcluster[tuple(q.items)]
            parsername._table[num][i]=parsername._itemcluster[tuple(j.items)]
            que.put(j)
    
    
    m = list(parsername.termset)+list(parsername.ntermset)
    x =list()
    for i in m:
        if i == "S'":
            continue
        x += i
    x = ["rownum"]+x
    t = PrettyTable(x)
    print(t)
    for row_num,val in parsername._table.items():
        l = list()
        for i in x:
            for j in val:
                if j[0] == i:
                    l.append(parsername._table[row_num][i])
        l = [row_num]+l
        t.add_row(l)
    print(t)

def lr1analysis(s,parsername):
    t = PrettyTable(['statlist','lsynbolist','rsynbolist','nextstat'])
    statlist = [0]
    lsynbolist = []
    rsynbolist = list(s)
    nextstat = parsername._table[statlist[-1]][rsynbolist[0]]
    t.add_row([statlist,lsynbolist,rsynbolist,nextstat])
    while lsynbolist != ['S']:
        tmp = nextstat
        if tmp == None:
            print("分析失败！")
            break
        if len(str(tmp))==1: #移进
            statlist.append(tmp)
            lsynbolist.append(rsynbolist[0])
            rsynbolist = rsynbolist[1:]
            nextstat = parsername._table[statlist[-1]][rsynbolist[0]]
        if len(str(tmp))==2:
            flag = 0
            for index,value in parsername.prs.items():
                if flag == 1:
                    break
                for item in value:
                    if str(item[0]) == tmp[1]:
                        l = len(item[1])
                        statlist = statlist[0:-l]
                        newtmp = parsername._table[statlist[-1]][index]
                        statlist.append(newtmp)
                        if type(lsynbolist[0:-l]) == 'Nonetype':
                            lsynbolist = list(index)
                        else:
                            lsynbolist = lsynbolist[0:-l]+list(index)
                        print(statlist[-1])
                        nextstat = parsername._table[statlist[-1]][rsynbolist[0]]
                        flag = 1
                        break
        print(statlist,lsynbolist,rsynbolist,nextstat)
        t.add_row([statlist,lsynbolist,rsynbolist,nextstat])
    print(t)
   

if __name__ == '__main__':
    parser_la = Parser('parse2.txt')
    init_parser(parser_la)
    item_la = ItemCluster()
    init_itemcluster(item_la,parser_la)
    create_itemcluster(item_la,parser_la)
    create_table(item_la,parser_la)
    print(parser_la.prs)
    lr1analysis('a#',parser_la)



        
      
            



             
