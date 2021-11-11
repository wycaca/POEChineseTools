from ntpath import join
import sys
import os
import chardet

def get_encoding(file):
    with open(file, 'rb') as f:
        tmp = chardet.detect(f.read(2))
        return tmp['encoding']

if __name__ == "__main__":
    msg_arr = []
    # print("当前路径: {}".format(os.getcwd()))
    for file in os.listdir(os.getcwd()):
        if file.endswith(".txt"):
            path = os.path.join(os.getcwd(), file)
            encoding_str = get_encoding(path)
            for index, line_str in enumerate(open(path, 'r', encoding=encoding_str)):
                time = line_str.count("\"")
                if time % 2 != 0:
                    msg = "文件路径: {}, 第 {} 行, 文本为: {}".format(path, index + 1, line_str)
                    msg_arr.append(msg)
                    print(msg)

    log_path = os.path.join(os.getcwd(), "result.log")
    with open(log_path, 'w') as f:
        for msg in msg_arr:
            f.write(msg)
                    