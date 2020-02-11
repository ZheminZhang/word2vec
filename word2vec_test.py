# coding=UTF-8
from gensim.models import Word2Vec
import numpy as np
from gensim import matutils
import jieba
import codecs
from tornado.concurrent import run_on_executor
from concurrent.futures import ThreadPoolExecutor
import utils


class Word2Vec_Test(object):
    executor = ThreadPoolExecutor(20)

    def __init__(self, model_path):
        self.model_path = model_path
        self.embedding_size = 64
        self.model_load = Word2Vec.load(self.model_path)

        # self.stop_words = {'我': 1, '你': 1, '啊': 1}
        self.stop_words = list()

    def word2vec(self, word):
        if word != '':
            try:
                return list(self.model_load[word])
            except ValueError as e:
                return list(np.ones(self.embedding_size))
        return list(np.zeros(self.embedding_size))

    # stop_word default True
    def sentence2tokens(self, sentence, stop_word=True, cut_all=False):
        in_tokens = list()
        break_flag = False
        if sentence != '':
            in_words = list(jieba.cut(sentence.strip(), cut_all=cut_all))
            for in_word in in_words:
                if stop_word:
                    for in_character in list(in_word):
                        if in_character in self.stop_words:
                            break_flag = True
                            continue
                    if break_flag:
                        break_flag = False
                        continue
                try:
                    if list(self.model_load[in_word]):
                        in_tokens.append(in_word)
                except KeyError as e:
                    continue
        # print("in_tokens:", in_tokens)
        return in_tokens

    def sentence2vec(self, in_sentence, input_type='sequence'):
        in_sentence_embed = []
        if input_type == 'token':
            if in_sentence:
                for in_word in in_sentence:
                    in_word_embed = self.word2vec(in_word)
                    in_sentence_embed.append(in_word_embed)
            return in_sentence_embed
        if input_type == 'sequence':
            if in_sentence:
                in_sentence = self.sentence2tokens(in_sentence)
                for in_word in in_sentence:
                    in_word_embed = self.word2vec(in_word)
                    in_sentence_embed.append(in_word_embed)
            print("embedding:", matutils.unitvec(
                np.array(in_sentence_embed).mean(axis=0)))
            return in_sentence_embed
        else:
            print("Please input right input_type: 'sequence' or 'token' ")

    def similarity(self, sentence1, sentence2, input_type='sequence'):
        if input_type == 'sequence' or input_type == 'token':
            if sentence1 and sentence2:
                return np.dot(matutils.unitvec(np.array(self.sentence2vec(sentence1, input_type=input_type)).mean(axis=0)),
                              matutils.unitvec(np.array(self.sentence2vec(sentence2, input_type=input_type)).mean(axis=0)))
            return 0.0
        if input_type == 'vector':
            if sentence1 and sentence2:
                return np.dot(matutils.unitvec(np.array(sentence1).mean(axis=0)),
                              matutils.unitvec(np.array(sentence2).mean(axis=0)))
            return 0
        else:
            print(
                "Please choose the right input_type: 'sequence' or 'token' or 'vector'. ")

    def http_test(self, sentence1, sentence2):
        a = "此次新型冠状病毒感染的肺炎病例感染后常表现为发热、乏力、干咳，鼻塞、流涕等上呼吸道症状少见。约半数患者在 1 周后会出现呼吸困难，严重者可快速进展为急性呼吸窘迫综合征、脓毒症休克、难以纠正的代谢性酸中毒和凝血功能障碍。部分患者起病症状轻微，可无发热，少数患者病情危重，甚至死亡。老人出现发热、咳嗽、咽痛、胸闷、呼吸困难、乏力、恶心呕吐、腹泻、结膜炎、肌肉酸痛等可疑症状。其中多数感染者表现为，间断发热或持续发热、中低热较多（37.3~38℃）、咳嗽、肌肉酸痛、乏力、呼吸困难、干咳、气喘、胸闷、畏寒、气短（活动后明显）、呼吸不畅、心率加快、精神差、食欲差；少部分感染者表现为头痛、腹泻、流涕、打喷嚏、喉咙疼痛、恶心呕吐、头晕、咯血，可能出现腹泻、恶心等消化道症状"
        b = "发热（体温37-38°C）、咳嗽及胸部不适症状，在临床症状出现后4天，咳嗽和肺部不适症状加重，但发热症状缓解。"
        c = "体温37.2℃，血压134/87mm Hg，脉搏每分钟110次，呼吸频率每分钟16次，自然呼吸时血氧饱和度96%。肺部有听诊音，X光胸片显示未见异常。持续干咳和2天恶心呕吐史，没有呼吸短促或胸痛。生命体征在正常范围内。在住院的第2天至第5天，除了伴有间歇性心动过速的高烧之外，这名患者的生命体征基本维持稳定。"
        sim = self.similarity(sentence1, sentence2)
        simArr = []
        simArr.append(self.similarity(a, b))
        simArr.append(self.similarity(a, c))
        simArr.append(self.similarity(b, c))
        print("similarity: ", str(sim))
        # return str(sim)
        return str(max(simArr))

    def http_cmp(self, sentence):
        a = "此次新型冠状病毒感染的肺炎病例感染后常表现为发热、乏力、干咳，鼻塞、流涕等上呼吸道症状少见。约半数患者在 1 周后会出现呼吸困难，严重者可快速进展为急性呼吸窘迫综合征、脓毒症休克、难以纠正的代谢性酸中毒和凝血功能障碍。部分患者起病症状轻微，可无发热，少数患者病情危重，甚至死亡。老人出现发热、咳嗽、咽痛、胸闷、呼吸困难、乏力、恶心呕吐、腹泻、结膜炎、肌肉酸痛等可疑症状。其中多数感染者表现为，间断发热或持续发热、中低热较多（37.3~38℃）、咳嗽、肌肉酸痛、乏力、呼吸困难、干咳、气喘、胸闷、畏寒、气短（活动后明显）、呼吸不畅、心率加快、精神差、食欲差；少部分感染者表现为头痛、腹泻、流涕、打喷嚏、喉咙疼痛、恶心呕吐、头晕、咯血，可能出现腹泻、恶心等消化道症状"
        b = "发热（体温37-38°C）、咳嗽及胸部不适症状，在临床症状出现后4天，咳嗽和肺部不适症状加重，但发热症状缓解。"
        c = "体温37.2℃，血压134/87mm Hg，脉搏每分钟110次，呼吸频率每分钟16次，自然呼吸时血氧饱和度96%。肺部有听诊音，X光胸片显示未见异常。持续干咳和2天恶心呕吐史，没有呼吸短促或胸痛。生命体征在正常范围内。在住院的第2天至第5天，除了伴有间歇性心动过速的高烧之外，这名患者的生命体征基本维持稳定。"
        simArr = []
        simArr.append(self.similarity(sentence, a))
        simArr.append(self.similarity(sentence, b))
        simArr.append(self.similarity(sentence, c))
        # return str(sim)
        return str(max(simArr))

    @run_on_executor
    def cmp_description(self, sentence, description_data):
        simArr = []
        # description_file = 'data/test_data/description.txt'
        # with codecs.open(description_file, 'r', 'utf-8') as description:
        #     description_data = description.readlines()
        #     for description_line in description_data:
        #         simArr.append(self.similarity(sentence, description_line))

        for description_line in description_data:
            simArr.append(self.similarity(sentence, description_line))
        print("simArr length: " + str(len(simArr)))
        return str(max(simArr))

    @run_on_executor
    def sickEstimate(self, request, description_data):
        descriptionRatio = 0.25
        questionRatio = 0.3
        simArr = []
        description = utils.getDescription(request)
        for description_line in description_data:
            simArr.append(self.similarity(description, description_line))
        print("simArr length: " + str(len(simArr)))
        descriptionEstimate = max(simArr) * descriptionRatio
        print("descriptionEstimate: " + str(descriptionEstimate))
        questionEstimate = utils.estimateByQuestion(request) * questionRatio
        print("questionEstimate: " + str(questionEstimate))
        overallEstimate = (descriptionEstimate + questionEstimate) / \
            (descriptionRatio + questionRatio)
        if (overallEstimate > 1):
            return "1"
        else:
            return str(overallEstimate)

    def single_test(self):
        sentence1 = input('input A:')
        sentence2 = input('input B:')
        print('similarity of "{}" and "{}":'.format(
            sentence1, sentence2), self.similarity(sentence1, sentence2))

    def mulit_test(self, test_source, test_target, result_file):
        with codecs.open(test_source, 'r', 'utf-8') as source, codecs.open(test_target, 'r', 'utf-8') as target, codecs.open(result_file, 'w', 'utf-8') as result:
            data_s = source.readlines()
            data_t = target.readlines()
            counter_s = len(data_s)
            counter_t = len(data_t)
            for line_s in data_s:
                for line_t in data_t:
                    # print('sentence 1: {}\tsentence 2:{}\tsimilarity:{}'.format(line_s, line_t, self.similarity(line_s, line_t)))
                    result.write(line_s.strip() + '\t' + line_t.strip() +
                                 '\t' + str(self.similarity(line_s, line_t)) + '\n')
        print('计算完毕，源端共计{}句，目标端{}句。'.format(counter_s, counter_t))
