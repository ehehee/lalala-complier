def parse_convert(s):
    """
    :param s: 字符串
    :return: 转换转义符之后的字符串
    """
    s = s.replace(r"\n", "\n")
    s = s.replace(r"\r", "\r")
    s = s.replace(r"\t", "\t")
    return s

def read_reg(filename = 'reg.txt'):
    """
    :param filename: 文件名
    :return: 返回一个每次迭代得到一行分割之后的二元组的生成器
   """
    with open(filename,'r') as reader:
        comment = False
        reg_type = {}
        for line in reader:
            line = line[:line.find('#')]    # 删除注释
            line = parse_convert(line).strip()
            if line == '"""' or line == "'''":
                comment = not comment
            if comment:
                continue
            if line.startswith('#') or line.find("::=") <= 0:
                continue
            l = list(line.split(" ::= "))
            reg_type[l[0]] = l[1]
    return reg_type
            
    
  
def infix2postfix(s):
    s1 = s
    opstack = []
    chrstack = []
    p = s1.find('[')
    if p == -1 : return s1
    while p<len(s):
        q = s1.find(']',p)
        chrstack += s1[p:q+1]
        if q == -1 or q+1 == len(s): break
        
        if s1[q+1] != '*' :
            opstack +=['.']
        if s1[q+1] == '*':
            opstack +=['*']
        p = q+1
        
    return ("".join(chrstack) + "".join(list(reversed(opstack))))
    
if __name__ == '__main__':
    tmp = read_reg()
    for (d,x) in tmp.items():
       print(d,infix2postfix(x))
         
        


    


        
