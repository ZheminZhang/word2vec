import json


def constructDescription(request):
    jsonbyte = request.body
    print('二进制格式ｊｓｏｎ字符串：', jsonbyte)
    jsonstr = jsonbyte.decode('utf8')  # 解码，二进制转为字符串
    print('ｊｓｏｎ字符串：', jsonstr)

    # 从ｊｓｏｎ字符串转换为ｊｓｏｎ对象，然后利用ｊｓｏｎ对象提供的ａｐｉ
    # 从ｊｓｏｎ字符串中取出我想要的内容(解析ｊｓｏｎ字符串)
    jsonobj = json.loads(jsonstr)  # 将字符串转为json对象
    # sentence = jsonobj.get('text')  # 就可以用api取值
    # print('sentence: ', sentence)
    sentence = ""
    sentenceArr = []

    for key in jsonobj:
        print(key + ": ")
        if jsonobj.get(key) == "" or jsonobj.get(key) == 0 or jsonobj.get(key) == "无" or jsonobj.get(key) == "否":
            print("null")
        else:
            print (jsonobj.get(key))
            if key == "temp1" or key == "temp2" or key == "temp3":
                sentenceArr.append("体温" + str(jsonobj.get(key)))
            elif key == "age":
                sentenceArr.append("年龄" + str(jsonobj.get(key)))
            elif key == "item3Value":
                sentenceArr.append("咽喉痛")
            elif key == "item4Value":
                sentenceArr.append("全身乏力酸疼")
            elif key == "item5Value":
                sentenceArr.append("打喷嚏及流涕")
            elif key == "item7Value":
                sentenceArr.append("舌苔偏厚")
            elif key == "zhouWei":
                sentenceArr.append(
                    "生活周边出现" + str(jsonobj.get(key)) + "名相似症状的人")
            elif key == "zhengZhuangDays":
                sentenceArr.append(
                    "上述症状已经持续" + str(jsonobj.get(key)) + "天")
            elif key == "city":
                sentenceArr.append(
                    "在过去两周内去过" + str(jsonobj.get(key)))
            elif key == "party":
                sentenceArr.append(
                    "过去5天内在" + str(jsonobj.get(key)) + "参加过聚会")
            elif key == "nowCity":
                sentenceArr.append(
                    "现在在" + str(jsonobj.get(key)))
            elif key == "item8Value":
                sentenceArr.append(
                    "与已知的新型冠状病毒感染者接触过")
            elif key == "item9Value":
                sentenceArr.append(
                    "与已知的武汉人员有过接触")
            elif key != "timeStamp":
                sentenceArr.append(str(jsonobj.get(key)))

    sentence = ",".join(sentenceArr)
    return sentence
