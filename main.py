# -*- coding:utf-8 -*-
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer

from trainword2vec import train_word2vec
from word2vec_test import Word2Vec_Test
import sys
import json
import utils


class IndexHandler(RequestHandler):
    output_model_name = "models/65d/models/word2vec_128d_model_zonghe"
    word2vec = Word2Vec_Test(output_model_name)

    def get(self):
        self.write(self.word2vec.http_test("你好", "他们"))

    def post(self, *args, **kwargs):
        sentence = utils.constructDescription(self.request)
        sim = self.word2vec.cmp_description(sentence)
        self.finish({"description": sentence, "similarity": sim})
        print("sentence: " + sentence)


if __name__ == '__main__':
    app = Application([(r'/', IndexHandler)])
    http_server = HTTPServer(app)
    # 最原始的方式
    http_server.bind(8888)
    http_server.start(1)

    # 启动Ioloop轮循监听
    IOLoop.current().start()
    print("listening 8888")
