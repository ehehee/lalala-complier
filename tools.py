def read_reg(filename = 'reg.txt'):
        """
    :param filename: 文件名
    :return: 返回一个每次迭代得到一行分割之后的二元组的生成器
    """
    with open(filename) as reader:
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

    for index,line in enumerate(open(filename)):
        print(line)


if __name__ == '__main__':
    read_reg()