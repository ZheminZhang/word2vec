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


class IndexHandler(RequestHandler):
    output_model_name = "models/65d/models/word2vec_128d_model_zonghe"
    word2vec = Word2Vec_Test(output_model_name)

    def get(self):
        self.write("index")

    def post(self, *args, **kwargs):
        startTime = time.time()
        sentence = utils.constructDescription(self.request)
        print("constructDescription time: " + str(time.time() - startTime))
        sim = self.word2vec.cmp_description(sentence)
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


if __name__ == '__main__':
    app = Application([(r'/', IndexHandler), ('/address/', AddressHandler)])
    http_server = HTTPServer(app)
    # 最原始的方式
    http_server.bind(8888)
    http_server.start(0)

    # 启动Ioloop轮循监听
    IOLoop.current().start()
    print("listening 8888")
