# -*- coding:utf-8 -*-
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
from tornado.httpserver import HTTPServer

from trainword2vec import train_word2vec
from word2vec_test import Word2Vec_Test
import sys
import json
import utils
import requests
import time
from concurrent.futures import ThreadPoolExecutor
import tornado
from tornado.concurrent import run_on_executor


class IndexHandler(RequestHandler):
    executor = ThreadPoolExecutor(20)
    output_model_name = "models/65d/models/word2vec_128d_model_zonghe"
    word2vec = Word2Vec_Test(output_model_name)

    def get(self):
        self.write("index")

    @tornado.gen.coroutine
    def post(self, *args, **kwargs):
        startTime = time.time()
        sentence = utils.constructDescription(self.request)
        print("constructDescription time: " + str(time.time() - startTime))
        sim = yield self.word2vec.cmp_description(sentence)
        print("sentence: " + sentence)
        endTime = time.time()
        print("total time cost: " + str(endTime - startTime))
        self.finish({"description": sentence, "similarity": sim,
                     "procTime": str(endTime - startTime)})


class AddressHandler(RequestHandler):
    def get(self):
        self.write("address get")

    def post(self):
        print("address post")
        jsonbyte = self.request.body
        print('二进制格式ｊｓｏｎ字符串：', jsonbyte)
        jsonstr = jsonbyte.decode('utf8')  # 解码，二进制转为字符串
        print('ｊｓｏｎ字符串：', jsonstr)
        jsonobj = json.loads(jsonstr)  # 将字符串转为json对象

        longitude = jsonobj.get("longitude")
        latitude = jsonobj.get("latitude")

        location = str(latitude) + "," + str(longitude)

        r = requests.get(url='http://api.map.baidu.com/reverse_geocoding/v3/',
                         params={'location': location, 'ak': 'exLGOnGUylFGD7MpuKtUZRL7G4s07I6e', 'output': 'json'})

        result = r.json()
        print("result:")
        print(result)
        city = result['result']['addressComponent']['city']
        print(city)

        self.finish(result)


class TestHandler(RequestHandler):
    executor = ThreadPoolExecutor(20)

    def initialize(self, i, startTime):
        self.i = i
        # print("i: " + str(i))
        self.startTime = startTime
        # print("startTime: " + str(startTime))

    @run_on_executor
    def waitTime(self):
        time.sleep(2)

    def get(self):
        self.write("index")

    @tornado.gen.coroutine
    def post(self):
        # print("startTime: " + str(self.startTime))
        if time.time() - self.startTime > 1:
            self.i = self.i + 1
        # time.sleep(2)
        yield self.waitTime()
        print("time cost: " + str(time.time() - self.startTime))
        self.finish({"i": self.i, "startTime": self.startTime})


if __name__ == '__main__':
    executor = ThreadPoolExecutor(2)

    startTime = time.time()
    i = 0
    app = Application([(r'/', IndexHandler), ('/address/',
                                              AddressHandler), ('/test/', TestHandler, {'i': i, "startTime": startTime})])
    http_server = HTTPServer(app)
    # 最原始的方式
    http_server.bind(8888)
    http_server.start(0)

    # 启动Ioloop轮循监听
    IOLoop.current().start()
    print("listening 8888")
