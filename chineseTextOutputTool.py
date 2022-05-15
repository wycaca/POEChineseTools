from ntpath import join
# import sys
import os
# import chardet

source_file = "stat_descriptions.txt"
source_path = os.path.join(os.getcwd(), source_file)
split_key_word = "description"
lang_key_word = "lang \""
type_chinese_simple = "Simplified Chinese"
type_chinese_traditional = "Traditional Chinese"

# def get_encoding(file):
#     with open(file, 'rb') as f:
#         tmp = chardet.detect(f.read(2))
#         return tmp['encoding']

def get_chinese_text(target_chinese_type):
    if (target_chinese_type == "S"):
        print("开始提取简体中文文本")
        target_chinese_type = type_chinese_simple
        target_path = os.path.join(os.getcwd(), "简体中文文本.txt")
    elif (target_chinese_type == "T"):
        print("开始提取繁体中文文本")
        target_chinese_type = type_chinese_traditional
        target_path = os.path.join(os.getcwd(), "繁体中文文本.txt")
    elif (target_chinese_type == "ALL"):
        print("开始提取2种中文文本")
        target_path = os.path.join(os.getcwd(), "2种中文文本.txt")
    else:
        print("输入的中文类型错误, 只能是 Simplified, Traditional 或者 ALL!")
    
    # 拼接 检索目标 字符串
    # lang_str = lang_key_word + target_chinese_type + '\"'
    # print("开始查找目标字符串: {}".format(lang_str))

    # 读取文件
    # 检测编码
    # encoding_str = get_encoding(source_path)
    # encoding_str = 'utf-8'
    with open(source_path, 'r', encoding = 'utf-16-le') as f:
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
    lang_index_list = []
    for i, data_str in enumerate(data_strs):
        # 发现 lang
        if data_str.count(lang_key_word) > 0:
            # 判断是否为2种中文模式
            if (target_chinese_type == "ALL"):
                # 如果不是本次需要的中文, 记录行号
                if data_str.find(type_chinese_simple) == -1 and data_str.find(type_chinese_traditional) == -1:
                    lang_index_list.append(i)
            else:
                if data_str.find(target_chinese_type) == -1:
                    lang_index_list.append(i)
    
    # 循环 待删索引列表, 目前是每种语言的头一行
    for i in lang_index_list:
        # 下一行, 一般是数字, 对应的描述行数 数字
        data_str = data_strs[i + 1].lstrip()
        if data_str.lstrip().isdecimal():
            des_line_num = int(data_str.lstrip())
            # print("描述为: {}行".format(des_line_num))
            delete_index_list.append(i + 1)
            for j in range(des_line_num + 1):
                delete_index_list.append(j + i + 1)
    
    # 将lang 行号添加至 总列表中, 去重
    delete_index_list = list(set(delete_index_list + lang_index_list))
    # print("删除的索引列表 {}".format(delete_index_list))
    # 输出结果
    with open(target_path, 'w', encoding='utf-8') as f:
        for i, data_str in enumerate(data_strs):
            if i not in delete_index_list:
                f.write(data_str + "\n")


if __name__ == "__main__":
    get_chinese_text("T")
