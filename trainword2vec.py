# coding=UTF-8
"""
这个小程序目的是用word2vec来训练词向量，可以配置“input_dir”来设置训练用的语料（注意要分词！）。
"""

import logging
import multiprocessing
import time
import os.path
import sys
from gensim.models import Word2Vec
from gensim.models.word2vec import PathLineSentences


def train_word2vec(input_path, in_output_model_name, in_output_model_format,
                   size=128, window=10, min_count=5, iter=10):
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    start_time = time.time()
    model = Word2Vec(PathLineSentences(input_path),
                     size=size, window=window, min_count=min_count, workers=multiprocessing.cpu_count(), iter=iter)
    model.save(in_output_model_name)
    model.wv.save_word2vec_format(in_output_model_format, binary=False)
    end_time = time.time()
    logger.info("Time consume %s" % str(end_time - start_time))
