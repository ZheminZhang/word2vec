# coding=UTF-8
import jieba
import os


def token(source_path, target_path, stop_words_file):
    file_list = os.listdir(source_path)
    stop_words = [word.strip() for word in open(
        stop_words_file, 'r', encoding='utf-8').readlines()]
    # print(stop_words)
    for single_file in file_list:
        with open(os.path.join(source_path, single_file), 'r', encoding='utf-8') as source, \
                open(os.path.join(target_path, 'token_' + single_file), 'w', encoding='utf-8') as target:
            for line in source:
                new_line = list()
                for item in list(jieba.cut(line.strip())):
                    if item not in stop_words:
                        new_line.append(item)
                # new_line = ' '.join(list(jieba.cut(line.strip(), cut_all=False)))
                target.write(' '.join(new_line) + '\n')


if __name__ == '__main__':
    jieba.load_userdict("jieba/mydict.txt")                     # 加载自定义词典
    stop_words_file = 'jieba/stop_words.txt'                    # 加载停用词表
    source_dir = 'data/row_data'                                # 原始数据
    target_dir = 'data/formated_data'                           # 分词后的数据

    token(source_dir, target_dir, stop_words_file)
