from ntpath import join
import sys
import os

split_key_word = "description"
lang_key_word = "lang \""
type_chinese_simple = "Simplified"
type_chinese_traditional = "Traditional"
english_lang_key_word = "lang \"English\""
current_path = os.getcwd()

def get_current_path(output_dir):
    return os.path.abspath(os.path.join(current_path, output_dir))


def readFile(source_path):
    # 读取文件
    with open(source_path, 'r', encoding = 'utf-16-le') as f:
        data_strs = f.read().splitlines()
    # for i in range(len(data_strs) - 1, -1, -1):
    #     data_str = data_strs[i]
    #     if data_str == "":
    #         data_strs.remove(data_str)
    return data_strs


def getLangIndexList(data_strs, target_chinese_type):
    # 循环, 找出不是中文的描述, 记录行号
    lang_index_list = []
    for i, data_str in enumerate(data_strs):
        # 发现 lang
        if data_str.count(lang_key_word) > 0:
            # 判断是否为2种中文模式
            if (target_chinese_type == "ALL"):
                # 如果不是本次需要的中文, 记录行号
                if data_str.find(type_chinese_simple) == -1 and data_str.find(type_chinese_traditional) == -1:
                    lang_index_list.append(i)
                    data_strs[i] = ""
            else:
                if data_str.find(target_chinese_type) == -1:
                    lang_index_list.append(i)
                    data_strs[i] = ""
    return lang_index_list


def getChineseText(target_chinese_type, source_file):
    source_path = os.path.join(os.getcwd(), source_file)
    if (target_chinese_type == "S"):
        print("开始 简体中文文本 提取 {}".format(source_file))
        target_chinese_type = type_chinese_simple
        target_path = get_current_path("简体中文文本")
    elif (target_chinese_type == "T"):
        print("开始 繁体中文文本 提取 {}".format(source_file))
        target_chinese_type = type_chinese_traditional
        target_path = get_current_path("繁体中文文本")
    elif (target_chinese_type == "ALL"):
        print("开始 2种中文文本 提取 {}".format(source_file))
        target_path = get_current_path("2种中文文本")
    else:
        print("输入的中文类型错误, 只能是 Simplified, Traditional 或者 ALL!")

    # 检测文件夹, 不存在则创建
    if not os.path.exists(target_path):
        os.makedirs(target_path)
    # 拼接输出文件名
    target_path = os.path.join(target_path, source_file)
    
    # 读取文件
    data_strs = readFile(source_path)

    # 记录非中文描述行号
    lang_index_list = getLangIndexList(data_strs, target_chinese_type)
    
    # 循环 待删索引列表, 目前是每种语言的头一行
    for i in lang_index_list:
        setEmptyText(i, data_strs)
    
    # 输出结果
    with open(target_path, 'w', encoding='utf-16-le') as f:
        for i, data_str in enumerate(data_strs):
            if data_str != "":
                f.write(data_str + "\n")
    print("处理完成, 输出至{}".format(target_path))

# todo
def addEnLang(source_file):
    print("添加英文标识, 开始处理: {}".format(source_file))
    # 得到所有描述行号
    # 倒序循环, 添加英文描述标识


def setEmptyText(i, data_strs):
    # 下一行, 一般是数字, 对应的描述行数 数字
    data_str = data_strs[i + 1].replace('\n', '').replace('\t', '').lstrip()
    # 如果没找到, 往下找一行, 直到找到数字
    while data_str.isdecimal():
        des_line_num = int(data_str)
        # print("描述为: {}行".format(des_line_num))
        data_strs[i + 1] = ""
        for j in range(des_line_num + 1):
            data_strs[j + i + 1] = ""
        break
    else:
        i = i + 1
        print("未找到描述行数 {}, 尝试+1, 取下一行数据".format(i))
        setEmptyText(i, data_strs)


if __name__ == "__main__":
    argv_len = len(sys.argv)
    # 设置默认值
    chinese_type = "T"
    add_lang = 0
    if argv_len >= 2:
        chinese_type = sys.argv[1]
    if argv_len >=3:
        add_lang = sys.argv[2]

    for file in os.listdir(os.getcwd()):
        if file.endswith(".txt"):
            new_file = getChineseText(chinese_type, file)
            if add_lang == 1:
                addEnLang(new_file)
    print("全部 处理完成")
