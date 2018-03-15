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
        for line in reader:
            line = line[:line.find('#')]    # 删除注释
            line = parse_convert(line).strip()
            if line == '"""' or line == "'''":
                comment = not comment
            if comment:
                continue
            if line.startswith('#') or line.find("::=") <= 0:
                continue
            yield tuple(line.split(" ::= "))
    


if __name__ == '__main__':
   for n in read_reg():
       print(n)