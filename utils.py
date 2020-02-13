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


def getDescription(request):
    jsonbyte = request.body
    print('二进制格式ｊｓｏｎ字符串：', jsonbyte)
    jsonstr = jsonbyte.decode('utf8')  # 解码，二进制转为字符串
    print('ｊｓｏｎ字符串：', jsonstr)

    jsonobj = json.loads(jsonstr)  # 将字符串转为json对象
    description = jsonobj.get("text")
    if description == "":
        print("get description from question")
        description = jsonobj.get("zhengZhuang")
    return description


def estimateByQuestion(request):
    jsonbyte = request.body
    print('二进制格式ｊｓｏｎ字符串：', jsonbyte)
    jsonstr = jsonbyte.decode('utf8')  # 解码，二进制转为字符串
    print('ｊｓｏｎ字符串：', jsonstr)

    jsonobj = json.loads(jsonstr)  # 将字符串转为json对象

    tempRatio = 0.08
    ageRatio = 0.01
    keSouRatio = 0.05
    huXiRatio = 0.05
    changWeiRatio = 0.02
    yanHouRatio = 0.05
    faLiRatio = 0.05
    penTiRatio = 0.02
    sheTaiRatio = 0.01
    zhouWeiRatio = 0.07
    zhengZhuangDaysRatio = 0.03
    cityRatio = 0.1
    partyRatio = 0.05
    nowCityRatio = 0.1
    jieChuRatio = 0.2
    wuHanJieChuRatio = 0.05
    cities1 = "武汉、鄂州、孝感、随州、黄冈"
    cities2 = "黄石、仙桃、咸宁、荆门、宜昌、襄阳、荆州、十堰"
    cities3 = "天门、潜江、新余、平遥县、温州、重庆万州区、三亚、恩施、珠海、南昌、信阳、深圳、双鸭山、天津宝坻区、长沙、蚌埠、台州"
    cities4 = "九江、广州、岳阳、北海、鸡西、宁波、防城港、杭州、莆田、合肥、甘孜州、中山、抚州、亳州、铜陵、重庆市、驻马店、马鞍山、上饶、北京市、西双版纳傣族自治州、安庆、银川、萍乡、南阳、娄底、株洲、宜春、上海市、郑州、常德、威海、邵阳"

    scoreArr = []
    for key in jsonobj:
        print(key + ": ")
        value = jsonobj.get(key)
        if key == "temp1" or key == "temp2" or key == "temp3":
            if value == "":
                value = "0"
            if float(value) < 37.3:
                scoreArr.append(0 * tempRatio)
            elif float(value) < 39:
                scoreArr.append(70 * tempRatio)
            else:
                scoreArr.append(30 * tempRatio)
        if key == "age":
            if value == "":
                value = "0"
            if int(value) < 50:
                scoreArr.append(0 * ageRatio)
            else:
                scoreArr.append(100 * ageRatio)
        if key == "itemValue":
            if value == "A":
                scoreArr.append(50 * keSouRatio)
            elif value == "B":
                scoreArr.append(25 * keSouRatio)
            elif value == "C":
                scoreArr.append(25 * keSouRatio)
            elif value == "D":
                scoreArr.append(0 * keSouRatio)
        if key == "item1Value":
            if value == "A":
                scoreArr.append(50 * huXiRatio)
            elif value == "B":
                scoreArr.append(25 * huXiRatio)
            elif value == "C":
                scoreArr.append(25 * huXiRatio)
            elif value == "D":
                scoreArr.append(0 * huXiRatio)
        if key == "item2Value":
            if value == "A":
                scoreArr.append(40 * changWeiRatio)
            elif value == "B":
                scoreArr.append(60 * changWeiRatio)
            elif value == "C":
                scoreArr.append(0 * changWeiRatio)
        if key == "item3Value":
            if value == "A":
                scoreArr.append(100 * yanHouRatio)
            elif value == "B":
                scoreArr.append(0 * yanHouRatio)
        if key == "item4Value":
            if value == "A":
                scoreArr.append(100 * faLiRatio)
            elif value == "B":
                scoreArr.append(0 * faLiRatio)
        if key == "item5Value":
            if value == "A":
                scoreArr.append(100 * penTiRatio)
            elif value == "B":
                scoreArr.append(0 * penTiRatio)
        if key == "item7Value":
            if value == "A":
                scoreArr.append(100 * sheTaiRatio)
            elif value == "B":
                scoreArr.append(0 * sheTaiRatio)
        if key == "zhouWei":
            if value == "":
                value = "0"
            if int(value) == 0:
                scoreArr.append(0 * zhouWeiRatio)
            elif int(value) < 3:
                scoreArr.append(50 * zhouWeiRatio)
            elif int(value) < 5:
                scoreArr.append(70 * zhouWeiRatio)
            else:
                scoreArr.append(100 * zhouWeiRatio)
        if key == "zhengZhuangDays":
            if value == "":
                value = "0"
            if int(value) == 0:
                scoreArr.append(0 * zhengZhuangDaysRatio)
            elif int(value) < 3:
                scoreArr.append(60 * zhengZhuangDaysRatio)
            elif int(value) < 7:
                scoreArr.append(80 * zhengZhuangDaysRatio)
            else:
                scoreArr.append(100 * zhengZhuangDaysRatio)
        if key == "city":
            if value == "":
                scoreArr.append(10 * cityRatio)
            elif value in cities1:
                scoreArr.append(100 * cityRatio)
            elif value in cities2:
                scoreArr.append(75 * cityRatio)
            elif value in cities3:
                scoreArr.append(50 * cityRatio)
            elif value in cities4:
                scoreArr.append(25 * cityRatio)
            else:
                scoreArr.append(10 * cityRatio)
        if key == "party":
            if value == "":
                scoreArr.append(10 * cityRatio)
            elif value in cities1:
                scoreArr.append(100 * partyRatio)
            elif value in cities2:
                scoreArr.append(75 * partyRatio)
            elif value in cities3:
                scoreArr.append(50 * partyRatio)
            elif value in cities4:
                scoreArr.append(25 * partyRatio)
            else:
                scoreArr.append(10 * partyRatio)
        if key == "nowCity":
            print("nowCity: " + value)
            if value == "":
                scoreArr.append(10 * cityRatio)
            elif value in cities1:
                print("in cities1")
                scoreArr.append(100 * nowCityRatio)
            elif value in cities2:
                print("in cities2")
                scoreArr.append(75 * nowCityRatio)
            elif value in cities3:
                print("in cities3")
                scoreArr.append(50 * nowCityRatio)
            elif value in cities4:
                print("in cities4")
                scoreArr.append(25 * nowCityRatio)
            else:
                print("not above")
                scoreArr.append(10 * nowCityRatio)
        if key == "item8Value":
            if value == "A":
                scoreArr.append(100 * jieChuRatio)
            elif value == "B":
                scoreArr.append(0 * jieChuRatio)
        if key == "item9Value":
            if value == "A":
                scoreArr.append(100 * wuHanJieChuRatio)
            elif value == "B":
                scoreArr.append(0 * wuHanJieChuRatio)
    return sum(scoreArr)/100


def constructDescription1(request):
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
    tempArr = []
    description = ""
    items = {"A": "干咳（无痰）", "B": "咳嗽（有痰）", "C": "严重咳嗽", "D": "无"}
    items1 = {"A": "躺着出现气喘/呼吸困难", "B": "坐着出现气喘/呼吸困难",
              "C": "走动后出现呼吸困难", "D": "无"}
    items2 = {"A": "恶心呕吐", "B": "腹泻", "C": "无"}
    items6 = {"A": "体温正常", "B": "低烧（37.2-38℃）", "C": "高烧（大于38℃）"}

    for key in jsonobj:
        value = jsonobj.get(key)
        print(key + ": " + str(value))
        if key == "text" and value != "":
            # sentenceArr.append(value)
            sentence = value
        elif key == "temp1" or key == "temp2" or key == "temp3":
            if value != "":
                tempArr.append(str(value))
        elif key == "age":
            # sentenceArr.append("年龄" + str(jsonobj.get(key)))
            print("")
        elif key == "itemValue" and value != "D":
            sentenceArr.append(items.get(value))
        elif key == "item1Value" and value != "D":
            sentenceArr.append(items1.get(value))
        elif key == "item2Value" and value != "C":
            sentenceArr.append(items2.get(value))
        elif key == "item3Value" and value == "A":
            sentenceArr.append("出现咽喉痛")
        elif key == "item4Value" and value == "A":
            sentenceArr.append("出现全身乏力酸疼")
        elif key == "item5Value":
            sentenceArr.append("打喷嚏及流涕")
        elif key == "item6Value":
            sentenceArr.append(items6.get(value))
            # sentenceArr.append("舌苔偏厚")
        elif key == "item7Value":
            # sentenceArr.append("舌苔偏厚")
            print("")
        elif key == "zhouWei":
            # sentenceArr.append(
            #     "生活周边出现" + str(jsonobj.get(key)) + "名相似症状的人")
            print("")
        elif key == "zhengZhuangDays":
            # sentenceArr.append(
            #     "上述症状已经持续" + str(jsonobj.get(key)) + "天")
            print("")
        elif key == "city":
            # sentenceArr.append(
            #     "在过去两周内去过" + str(jsonobj.get(key)))
            print("")
        elif key == "party":
            # sentenceArr.append(
            #     "过去5天内在" + str(jsonobj.get(key)) + "参加过聚会")
            print("")
        elif key == "nowCity":
            # sentenceArr.append(
            #     "现在在" + str(jsonobj.get(key)))
            print("")
        elif key == "item8Value":
            # sentenceArr.append(
            #     "与已知的新型冠状病毒感染者接触过")
            print("")
        elif key == "item9Value":
            # sentenceArr.append(
            #     "与已知的武汉人员有过接触")
            print("")
        elif key != "timeStamp":
            # sentenceArr.append(str(jsonobj.get(key)))
            print("")
    tempDescrption = ""
    if len(tempArr) > 0:
        tempDescrption = "最近" + str(len(tempArr)) + \
            "次体温:" + ",".join(tempArr) + "。"
    sentenceDescrption = ""
    if len(sentenceArr) > 0:
        sentenceDescrption = ",".join(sentenceArr) + "。"
    description = sentence + " " + tempDescrption + sentenceDescrption
    return description


def estimateByQuestion1(request):
    jsonbyte = request.body
    print('二进制格式ｊｓｏｎ字符串：', jsonbyte)
    jsonstr = jsonbyte.decode('utf8')  # 解码，二进制转为字符串
    print('ｊｓｏｎ字符串：', jsonstr)

    jsonobj = json.loads(jsonstr)  # 将字符串转为json对象

    # tempRatio = 0.08
    ageRatio = 0.02
    # keSouRatio = 0.05
    # huXiRatio = 0.05
    # changWeiRatio = 0.02
    # yanHouRatio = 0.05
    # faLiRatio = 0.05
    # penTiRatio = 0.02
    sheTaiRatio = 0.03
    zhouWeiRatio = 0.15
    zhengZhuangDaysRatio = 0.05
    cityRatio = 0.15
    partyRatio = 0.10
    nowCityRatio = 0.15
    jieChuRatio = 0.2
    wuHanJieChuRatio = 0.15
    sumRatio = 0
    cities1 = "武汉、鄂州、孝感、随州、黄冈"
    cities2 = "黄石、仙桃、咸宁、荆门、宜昌、襄阳、荆州、十堰"
    cities3 = "天门、潜江、新余、平遥县、温州、重庆万州区、三亚、恩施、珠海、南昌、信阳、深圳、双鸭山、天津宝坻区、长沙、蚌埠、台州"
    cities4 = "九江、广州、岳阳、北海、鸡西、宁波、防城港、杭州、莆田、合肥、甘孜州、中山、抚州、亳州、铜陵、重庆市、驻马店、马鞍山、上饶、北京市、西双版纳傣族自治州、安庆、银川、萍乡、南阳、娄底、株洲、宜春、上海市、郑州、常德、威海、邵阳"

    scoreArr = []
    for key in jsonobj:
        print(key + ": ")
        value = jsonobj.get(key)
        # if key == "temp1" or key == "temp2" or key == "temp3":
        #     if value == "":
        #         value = "0"
        #     if float(value) < 37.3:
        #         scoreArr.append(0 * tempRatio)
        #     elif float(value) < 39:
        #         scoreArr.append(70 * tempRatio)
        #     else:
        #         scoreArr.append(30 * tempRatio)
        if key == "age":
            if value == "":
                # value = "0"
                print("age null")
            else:
                sumRatio += ageRatio
                if int(value) < 50:
                    scoreArr.append(0 * ageRatio)
                else:
                    scoreArr.append(100 * ageRatio)
        # if key == "itemValue":
        #     if value == "A":
        #         scoreArr.append(50 * keSouRatio)
        #     elif value == "B":
        #         scoreArr.append(25 * keSouRatio)
        #     elif value == "C":
        #         scoreArr.append(25 * keSouRatio)
        #     elif value == "D":
        #         scoreArr.append(0 * keSouRatio)
        # if key == "item1Value":
        #     if value == "A":
        #         scoreArr.append(50 * huXiRatio)
        #     elif value == "B":
        #         scoreArr.append(25 * huXiRatio)
        #     elif value == "C":
        #         scoreArr.append(25 * huXiRatio)
        #     elif value == "D":
        #         scoreArr.append(0 * huXiRatio)
        # if key == "item2Value":
        #     if value == "A":
        #         scoreArr.append(40 * changWeiRatio)
        #     elif value == "B":
        #         scoreArr.append(60 * changWeiRatio)
        #     elif value == "C":
        #         scoreArr.append(0 * changWeiRatio)
        # if key == "item3Value":
        #     if value == "A":
        #         scoreArr.append(100 * yanHouRatio)
        #     elif value == "B":
        #         scoreArr.append(0 * yanHouRatio)
        # if key == "item4Value":
        #     if value == "A":
        #         scoreArr.append(100 * faLiRatio)
        #     elif value == "B":
        #         scoreArr.append(0 * faLiRatio)
        # if key == "item5Value":
        #     if value == "A":
        #         scoreArr.append(100 * penTiRatio)
        #     elif value == "B":
        #         scoreArr.append(0 * penTiRatio)
        if key == "item7Value":
            if value == "A":
                scoreArr.append(100 * sheTaiRatio)
            elif value == "B":
                scoreArr.append(0 * sheTaiRatio)
        if key == "zhouWei":
            if value == "":
                # value = "0"
                print("zhouWei null")
            else:
                sumRatio += zhouWeiRatio
                if int(value) == 0:
                    scoreArr.append(0 * zhouWeiRatio)
                elif int(value) < 3:
                    scoreArr.append(50 * zhouWeiRatio)
                elif int(value) < 5:
                    scoreArr.append(70 * zhouWeiRatio)
                else:
                    scoreArr.append(100 * zhouWeiRatio)
        if key == "zhengZhuangDays":
            if value == "":
                # value = "0"
                print("zhengZhuangDays null")
            else:
                sumRatio += zhengZhuangDaysRatio
                if int(value) == 0:
                    scoreArr.append(0 * zhengZhuangDaysRatio)
                elif int(value) < 3:
                    scoreArr.append(60 * zhengZhuangDaysRatio)
                elif int(value) < 7:
                    scoreArr.append(80 * zhengZhuangDaysRatio)
                else:
                    scoreArr.append(100 * zhengZhuangDaysRatio)
        if key == "city":
            if value == "":
                # value = "0"
                print("city null")
            else:
                sumRatio += cityRatio
                if value in cities1:
                    scoreArr.append(100 * cityRatio)
                elif value in cities2:
                    scoreArr.append(75 * cityRatio)
                elif value in cities3:
                    scoreArr.append(50 * cityRatio)
                elif value in cities4:
                    scoreArr.append(25 * cityRatio)
                else:
                    scoreArr.append(10 * cityRatio)
        if key == "party":
            if value == "":
                # value = "0"
                print("party null")
            else:
                sumRatio += partyRatio
                if value in cities1:
                    scoreArr.append(100 * partyRatio)
                elif value in cities2:
                    scoreArr.append(75 * partyRatio)
                elif value in cities3:
                    scoreArr.append(50 * partyRatio)
                elif value in cities4:
                    scoreArr.append(25 * partyRatio)
                else:
                    scoreArr.append(10 * partyRatio)
        if key == "nowCity":
            print("nowCity: " + value)
            if value == "":
                # value = "0"
                print("nowCity null")
            else:
                sumRatio += nowCityRatio
                if value in cities1:
                    print("in cities1")
                    scoreArr.append(100 * nowCityRatio)
                elif value in cities2:
                    print("in cities2")
                    scoreArr.append(75 * nowCityRatio)
                elif value in cities3:
                    print("in cities3")
                    scoreArr.append(50 * nowCityRatio)
                elif value in cities4:
                    print("in cities4")
                    scoreArr.append(25 * nowCityRatio)
                else:
                    print("not above")
                    scoreArr.append(10 * nowCityRatio)
        if key == "item8Value":
            sumRatio += jieChuRatio
            if value == "A":
                scoreArr.append(100 * jieChuRatio)
            elif value == "B":
                scoreArr.append(0 * jieChuRatio)
        if key == "item9Value":
            sumRatio += wuHanJieChuRatio
            if value == "A":
                scoreArr.append(100 * wuHanJieChuRatio)
            elif value == "B":
                scoreArr.append(0 * wuHanJieChuRatio)
    return sum(scoreArr)/100/sumRatio
