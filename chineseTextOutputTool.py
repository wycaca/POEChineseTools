from ntpath import join
import sys
import os
import chardet

source_file = "stat_descriptions.txt"
source_path = os.path.join(os.getcwd(), source_file)
target_path = os.path.join(os.getcwd(), "提取后的文本.txt")
split_key_word = "description"
lang_key_word = "lang \""

def get_encoding(file):
    with open(file, 'rb') as f:
        tmp = chardet.detect(f.read(2))
        return tmp['encoding']

def get_chinese_text(target_chinese_type):
    
    if (target_chinese_type == "Simplified"):
        print("开始提取简体中文文本")
        target_chinese_type = "Simplified Chinese"
    elif (target_chinese_type == "Traditional"):
        print("开始提取简体中文文本")
        target_chinese_type = "Traditional Chinese"
    else:
        print("输入的中文类型错误, 只能是 Simplified 或者 Traditional !")
    
    # 拼接 检索目标 字符串
    lang_str = 'lang \"' + target_chinese_type + '\"'
    print("开始查找目标字符串: {}".format(lang_str))

    # 读取文件
    # 检测编码
    encoding_str = get_encoding(source_path)
    with open(source_path, 'r', encoding = encoding_str) as f:
        data_strs = f.read().splitlines()

    # 检查关键字 description
    key_word_count = data_strs.count(split_key_word)
    if (key_word_count == 0):
        print("文本内容不正确, 请检查")
        return
    else:
        print("发现 {} 条描述".format(key_word_count + 1))
    
    # 循环, 找出不是中文的描述, 记录行号
    delete_index_list = []
    for i, data_str in enumerate(data_strs):
        # 发现 lang
        if data_str.count(lang_key_word) > 0:
            # 如果不是本次需要的中文, 记录行号
            if data_str.find(target_chinese_type) == -1:
                delete_index_list.append(i)
                
        # 如果行号 - 1 在列表中
        if (i - 1) in delete_index_list:
            # 如果是数字, 说明是 对应的描述行数 数字
            if data_str.lstrip().isdecimal():
                des_line_num = int(data_str.lstrip())
            else:
                # 如果不是, 则继续循环
                continue
            # print("描述为: {}行".format(des_line_num))
            delete_index_list.append(i)
            for j in range(des_line_num, 0):
                delete_index_list.append(j + des_line_num - 1)
                # 删除 对应行数的文本
                del data_strs[j + des_line_num - 1]
            # 删除 对应的 lang
            del data_strs[i - 1]
            # 删除 本行 数字
            del data_strs[i]
    
    # 输出结果
    with open(target_path, 'w', encoding=encoding_str) as f:
        for data_str in data_strs:
            f.write(data_str + "\n")


if __name__ == "__main__":
    get_chinese_text("Simplified")
