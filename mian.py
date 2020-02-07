# coding=UTF-8
from trainword2vec import train_word2vec
from word2vec_test import Word2Vec_Test
import sys


if __name__ == '__main__':
    if sys.argv[1] == 'train':
        # train
        input_dir = 'data/formated_data'     # 输入文件或文件夹，即训练语料文件或文件夹
        output_model_name = 'models/zhuanye_32d/word2vec_32d_model_zhuanye'     # 要保存的模型名
        output_model_format = 'models/zhuanye_32d/word2vec_zhuanye_format'      # 要保存的模型格式
        # size是向量维数, window是窗口大小, min_count是最小词频，iter是迭代次数，默认多线程
        train_word2vec(input_dir, output_model_name, output_model_format,
                       size=32, window=5, min_count=5, iter=10)

    if sys.argv[1] == 'test':
        # test
        # output_model_name = "models/64d/models/word2vec_128d_model"           # 保存的word2vec模型
        output_model_name = "models/65d/models/word2vec_128d_model_zonghe"
        # output_model_name = "models/65d/models/word2vec_zonghe_format"
        word2vec = Word2Vec_Test(output_model_name)

        # 批量测试
        source_file = 'data/test_data/左侧.txt'
        target_file = 'data/test_data/右侧.txt'
        result_file = 'data/test_data/result.txt'
        # word2vec.mulit_test(source_file, target_file, result_file)

        # 如果想进行单条测试，把下面两个"""符号去掉
        while(True):
            word2vec.single_test()
            print('====================')
