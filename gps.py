#-*- coding:utf8

#-*- coding:utf8
import json

import xlrd

from Pinyin2Chinese_master.pinyincut import *
from Pinyin2Hanzi import DefaultDagParams
from Pinyin2Hanzi import dag
# cuter = PinyinCut()
#将字符串列表转为汉子
# def pinyin_2_hanzi(pinyinList):
#     dagParams = DefaultDagParams()
#     result = dag(dagParams, pinyinList, path_num=1, log=True)#10代表侯选值个数
#     re=""
#     for item in result:
#         socre = item.score
#         res = item.path # 转换结果
#         re=res[0]
#         break
#     return re
#将字符串转为汉子
# def pintohanzi(sent):
#     a=cuter.cut(sent.lower())
#     b=pinyin_2_hanzi(a)
#     return b

import re
def IsContainNum(str):
    bool(re.search(r'\d', str))

#字符串包含中文字符或者英文字符串，则返回true，否则false
def IsPunctions(str):
    flag=False
    for line in str:
        if line in string.punctuation or line in punctuation:
            flag= True
            break
    return flag
#字符串包含英文字符串，则返回true，否则false
def IsPunction(str):
    flag=False
    lens = len(str)
    for i in range(lens):
        if str[i]  in string.punctuation:
            flag=True
    return flag
#包含英文字符则返回true，否则false
def containenglish(str0):
    return bool(re.search('[a-z]', str0))


from langconv import *
import sys
# 转换繁体到简体
def cht_to_chs(line):
    line = Converter('zh-hans').convert(line)
    line.encode('utf-8')
    return line

# 转换简体到繁体
def chs_to_cht(line):
    line = Converter('zh-hant').convert(line)
    line.encode('utf-8')
    return line




#繁体转为简体

#判断字符串中含有英文大写字符的格式
def static_alphrase_num(str):
    num=0
    lens=len(str)
    for i in range(lens):
        if (str[i]>='A') and (str[i]<='Z'):
            num+=1
    return num
#检测语言的种类97种，en为英语，zh为中文
#语种类型包括：af, am, an, ar, as, az, be, bg, bn, br, bs, ca, cs, cy, da, de, dz, el, en, eo, es, et, eu, fa, fi, fo, fr, ga, gl, gu, he, hi, hr, ht, hu, hy, id, is, it, ja, jv, ka, kk, km, kn, ko, ku, ky, la, lb, lo, lt, lv, mg, mk, ml, mn, mr, ms, mt, nb, ne, nl, nn, no, oc, or, pa, pl, ps, pt, qu, ro, ru, rw, se, si, sk, sl, sq, sr, sv, sw, ta, te, th, tl, tr, ug, uk, ur, vi, vo, wa, xh, zh, zu
#返回语言的类型
import langid
def detect_lang(str):
    result=langid.classify(str)
    return result[0]
def is_all_chinese(str):
    return all(map(lambda c: '\u4e00' <= c <= '\u9fa5', str))
def is_all_english(str):
    return all(map(lambda c: 'A' <= c <= 'Z' or 'a' <= c <= 'z', str))
#print(is_all_english('Baden-Wurttemberg'))
# def liuniu_tuniu_Address(file):
#     wb=xlrd.open_workbook(file)
#     tuniu=wb.sheet_by_name("途牛周边地址1").col_values(0)
#
#     citys=wb.sheet_by_name("中国城市").col_values(0)
#     province=wb.sheet_by_name("中国省份").col_values(0)
#     countrys=wb.sheet_by_name("外国国家").col_values(0)
#     forgin_city=wb.sheet_by_name("外国城市").col_values(0)
#
#     return tuniu,citys,province,countrys,forgin_city
# def name_to_address(data,address):
#     result=""
#     if data in address:
#         result=data
#     else:
#         flag=False
#         for ad in address:
#             name=ad
#             if name[-3:]=="自治县":
#                 name=name[:-3]
#             if len(name)>2 and (name[-1:]=="县"or name[-1:]=="市" or name[-1:]=="区"):
#                 name=name[:-1]
#             if data.find(name)==0:
#                 flag = True
#                 result=ad
#                 break
#     return result
import langid

# def tuniu_duiying(name,address):
#     result=""
#     if name in address:
#         result=name
#     else:
#         result = name_to_address(name, tuniu)
#     return result
#获取字
def national_list(file):
    china_dic={}
    foreign_dic={}
    wb = xlrd.open_workbook(file)
    sheet1 = wb.sheet_by_name('中国')
    nrows=sheet1.nrows

    province_capital=""
    #获取城市的地区
    for i in range(1,nrows):
        data=sheet1.row_values(i)
        #country=data[0]
        province = data[1].replace(" ","").replace("\xa0","")
        capital = data[2].replace(" ","").replace("\xa0","")
        city = data[3].replace(" ","").replace("\xa0","")
        county = data[4].replace(" ","").replace("\xa0","")

        if province not in china_dic:
            china_dic[province]={}
        if capital:
            province_capital=capital
        if 'capital' not in china_dic[province]:
            china_dic[province]['capital']=province_capital
        if city not in china_dic[province]:
            china_dic[province][city]=[]
        if county:
            china_dic[province][city].append(county)


    sheet2 = wb.sheet_by_name('国外城市 ')
    nrows = sheet2.nrows
    for i in range(nrows):
        data=sheet2.row_values(i)
        globals=data[0].replace(" ","").replace("\xa0","")
        country = data[1].replace(" ","").replace("\xa0","")
        city = data[2].replace(" ","").replace("\xa0","")
        # if globals not in foreign_dic:
        #     foreign_dic[globals]={}
        if country not in foreign_dic:
            foreign_dic[country]=[]
        foreign_dic[country].append(city)
    sheet2 = wb.sheet_by_name('中国省份')
    provinceList=sheet2.col_values(0)


    #获取中英文对照数据
    pinyin_zhongwen={}
    sheet2 = wb.sheet_by_name('中文版英文对照版')
    nrows = sheet2.nrows
    for i in range(nrows):
        data = sheet2.row_values(i)
        pinyin_zhongwen[data[0].replace(" ","")]=data[1].replace(" ","")
    return china_dic,foreign_dic,provinceList,pinyin_zhongwen
#从县中找到对应的城市内容。type=1，仅从县中找到县的数据，从县中找到县或者市的数据。
'''city,city_dic的key数据
city_gps,gps数据
sublocity,县的数据
city_dic,市的数据
province,市的对应省
type，type==2，则数据县的相关数据，否则type==1，输出市、县的相关数据
'''
def search_sublocity_data(city,city_gps,sublocity,sublocity_data,city_dic,province,type):
    #print("县级",city,city_gps,sublocity,sublocity_data,city_dic,province,type)
    sublocity_temp,city_sublocaty,province_sublocaty="","",""
    city_temp,province_city="",""
    if sublocity and sublocity in city_dic:
        sublocity_temp = sublocity
        province_sublocaty = province
        city_sublocaty = city
        #print(sublocity,sublocity_temp)
    if not sublocity_temp and sublocity_data and sublocity in city_dic:
        sublocity_temp = sublocity
        province_sublocaty = province
        city_sublocaty = city
    for data in city_dic:
        if type=="2" and not city_gps and (data.find(city_gps) == 0 or city_gps.find(data) == 0):
            city_temp = city
            province_city = province
            continue
        if not sublocity_temp and  sublocity and (data.find(sublocity) == 0 or sublocity.find(data) == 0):
            sublocity_temp = data
            province_sublocaty = province
            city_sublocaty = city
            continue
        if city_temp and sublocity_temp:
            break
    if type=='1':
        return sublocity_temp, city_sublocaty, province_sublocaty
    else:
        return city_temp,sublocity_temp,province_city,city_sublocaty,province_sublocaty
'''city,
city_data,去掉省、市、县 的结果，若为空，则说明没有进行处理
sublocity,
sublocity_data,去掉省、市、县 的结果，若为空，则说明没有进行处理
province_dic,
province
'''
def search_city_data(city,city_data,sublocity,sublocity_data,province_dic,province):
    # if city_temp:
    #     sublocity_temp,city_sublocaty,province_sublocaty=search_sublocity_data(city_temp, city,sublocity, province_dic[city_temp], province,'1')
    #
    # if not city_temp:
    #     for key2, value2 in province_dic.items():
    #         if key2 != "capital":
    #             if not sublocity_temp and sublocity and (key2.find(sublocity) == 0 or sublocity.find(key2) == 0):
    #                 sublocity_temp = key2
    #                 province_sublocaty = province
    #                 city_sublocaty = province
    #                 break
    #             if not sublocity_temp and sublocity:
    #                 city_temp,sublocity_temp,province_city,city_sublocaty,province_sublocaty = search_sublocity_data(key2, city,sublocity,
    #                                                                                        value2,
    #                                                                                        province,'2')
        #print('对应的县2', sublocity_temp, city_sublocaty, province_sublocaty)
    #print("city_data,start",city,city_data,sublocity,sublocity_data,province_dic,province)
    city_temp, sublocity_temp, province_city, city_sublocaty, province_sublocaty="","","","",""
    if city in province_dic:
        #print("kkk_city")
        province_city = province
        city_temp = city
        sublocity_temp, city_sublocaty, province_sublocaty = search_sublocity_data(city_temp, city, sublocity,
                                                                                   sublocity_data, province_dic[city_temp], province,
                                                                                   '1')
        #print(province_city,city_temp,sublocity_temp, city_sublocaty, province_sublocaty)
    elif city_data and city_data in province_dic:
        #print('city_data')
        province_city = province
        city_temp = city_data
        sublocity_temp, city_sublocaty, province_sublocaty = search_sublocity_data(city_data, city, sublocity,
                                                                                   sublocity_data,
                                                                                   province_dic[city_temp], province,
                                                                                   '1')
    else:
        for key1, value1 in province_dic.items():
            # 查询县
            if key1!="capital":
                # 字符匹配市
                #print(city_data,city,key1)
                #print(key1)
                if (city_data and (key1.find(city_data) == 0 or city_data.find(key1) == 0)) or (
                        key1.find(city) == 0 or city.find(key1) == 0):
                    province_city = province
                    city_temp = key1

                    break
                if city in value1:
                    province_city = province
                    city_temp = key1
                    break
                if city_data and city_data in value1:
                    province_city = province
                    city_temp = key1
                    break


            # 字符串匹配县
        #print('city_temps',city_temp)
        if not city_temp:
            if city_data:
                city_temp,sublocity_temp,province_city,city_sublocaty,province_sublocaty=search_sublocity_data(key1, city_data, sublocity, sublocity_data, value1, province, '2')
            else:
                city_temp,sublocity_temp,province_city,city_sublocaty,province_sublocaty=search_sublocity_data(key1, city, sublocity, sublocity_data, value1, province,
                                      '2')

        else:
            if city_data:
                sublocity_temp,city_sublocaty,province_sublocaty=search_sublocity_data(key1, city_data, sublocity, sublocity_data, value1, province,
                                      '1')
            else:
                sublocity_temp,city_sublocaty,province_sublocaty=search_sublocity_data(key1, city, sublocity, sublocity_data, value1, province,
                                 '1')
    #print(city_temp, sublocity_temp, province_city, city_sublocaty, province_sublocaty)
    return city_temp,sublocity_temp,province_city,city_sublocaty,province_sublocaty


from zhon.hanzi import punctuation
import string
def search_china(country,province,city,sublocity,china_area):
    province_data,city_data,sublocity_data="","",""
    if country.find("台湾")!=-1:
        if province.find("台湾")==-1:
            sublocity=city
            city=province
            province=country
        country="中国"
    #print(country,province,city,sublocity,china_area)
    #将省，市，县，地区，进行简化
    if len(province)>2 and province[-1:]=="省" or province[-1:]=="市" or province[-1:]=="县":
        province_data=province[:-1]
    if len(city)>2 and city[-1:]=="省" or city[-1:]=="市" or city[-1:]=="县" :
        city_data=city[:-1]
    if len(city)>3 and city[-2:] == "地区":
        city_data = city[:-2]
    if len(sublocity)>2 and sublocity[-1:]=="省" or sublocity[-1:]=="市" or sublocity[-1:]=="县":
        sublocity_data=sublocity[:-1]
    if len(sublocity)>3 and sublocity[-2:] == "地区":
        sublocity_data = sublocity[:-2]
    #print(country,province,city,sublocity)
    result=""
    province_temp, city_temp, sublocity_temp = "", "", ""
    province_city, city_sublocaty, province_sublocaty="", "", ""
    if province==city and province:
        #查找省、市部分数据
        if province in china_area :
            province_temp=province
            province_city=province
            ##如果县有数据，则查找县下的数据
            if not sublocity:
                city_temp = china_area[province]['capital']
                return city_temp
            else:
                city_temp,sublocity_temp,province_city,city_sublocaty,province_sublocaty=search_city_data(sublocity, sublocity_data, sublocity, sublocity_data, china_area[province_temp], province_temp)
        if province_data and province_data in china_area :
            province_temp = province_data
            province_city = province_data
            ##如果县有数据，则查找县下的数据
            if not sublocity:
                city_temp = china_area[province_data]['capital']
                return city_temp
            else:
                city_temp, sublocity_temp, province_city, city_sublocaty, province_sublocaty = search_city_data(
                    sublocity, sublocity_data, sublocity, sublocity_data, china_area[province_temp], province_temp)

        for key, value in china_area.items():
            if (province_data and (province_data.find(key) == 0 or key.find(province_data)==0))or (province.find(key) == 0 or key.find(province)==0):
                province_temp = key
                province_city = key
                if not sublocity:
                ##如果县有数据，则查找县下的数据
                    city_temp=value['capital']
                    return city_temp
                else:
                    #print("a",country,province,city,sublocity,province_temp)
                    city_temp, sublocity_temp, province_city, city_sublocaty, province_sublocaty = search_city_data(
                        sublocity, sublocity_data, sublocity, sublocity_data, china_area[province_temp], province_temp)
                break
                #print("province_temp,city_temp, sublocity_temp, province_city, city_sublocaty, province_sublocaty",province_temp,city_temp, sublocity_temp, province_city, city_sublocaty, province_sublocaty)
            else:
                for key1,value1 in value.items():
                    if (province_data and (province_data.find(key1) == 0 or key1.find(province_data)==0))or (province.find(key1) == 0 or key1.find(province)==0):
                        province_temp = key
                        province_city = key
                        #print(province_temp)
                        ##如果县有数据，则查找县下的数据
                        if not sublocity:
                            city_temp = china_area[province_temp]['capital']
                            return city_temp
                        else:
                            city_temp, sublocity_temp, province_city, city_sublocaty, province_sublocaty = search_city_data(
                                sublocity, sublocity_data, sublocity, sublocity_data, china_area[province_temp],
                                province_temp)


                        break
    else:#查询省，市，县 是否可以查到，若可以查到，则判断是否有逻辑关系
        #查询省

        if province:
            if province in china_area:
                province_temp = province
            elif province_data and province_data in china_area :
                province_temp = province_data
            else:
                for key1,value1 in china_area.items():
                    if (province_data and (key1.find(province_data)==0 or province_data.find(key1)==0))or(key1.find(province)==0 or province.find(key1)==0):
                        province_temp=key1
                        break
                    if (province in value1) :
                        province_temp = key1
                        province_city = key1
                        city_temp =province
                        break
                    if province_data and province_data in value1:
                        province_temp=key1
                        province_city = key1
                        city_temp=province_data
                        break
        #print("province",province_temp)
        if city:
            #print(province_temp)
            if province_temp:
                #如果直接根据key可以查到则查找，否则从县级数据查找
                #print("ttt")
                city_temp,sublocity_temp,province_city,city_sublocaty,province_sublocaty=search_city_data\
                    (city,city_data,sublocity,sublocity_data,china_area[province_temp],province_temp)
                #print("province_",province_temp,city_temp,sublocity_temp,province_city,city_sublocaty,province_sublocaty)
            if not city_temp:#从每个城市中遍历
                #print("kkkk")
                for key, value in china_area.items():
                    city_temp,sublocity_temp,province_city,city_sublocaty,province_sublocaty=search_city_data(city, city_data, sublocity, sublocity_data, value,
                                     key)
                    if city_temp or sublocity_temp:
                        break
                #print('a',city_temp,sublocity,sublocity_temp,province_city,city_sublocaty,province_sublocaty)
                # for key2,value2 in value1.items():
                #     if key2!="capital":
                #         if key2.find(city)==0 or city.find(key2)==0:
                #             city_temp = key2
                #             province_city=key1
                #         if sublocity and (key2.find(sublocity)==0 or sublocity.find(key2)==0):
                #             sublocity_temp = key2
                #             province_sublocaty=key1
                #             city_sublocaty=key1
                #         if not city_temp or not sublocity_temp:
                #             for data in value2:
                #                 if not city_temp and(data.find(city)==0 or city.find(data)==0) :
                #                     city_temp = data
                #                     province_city=key1
                #
                #                 if not sublocity_temp and (data.find(sublocity)==0 or sublocity.find(data)==0):
                #                     sublocity_temp = data
                #                     province_sublocaty = key1
                #                     city_sublocaty = key2
        #print(province_city,province_sublocaty,city_sublocaty,"end")
        #print(province_temp,city_temp,sublocity_temp)
    #print("各个护具",province_city,province_temp,city_sublocaty,city_temp,province_sublocaty,province_temp)
    if country .find("台湾")!=-1 or province .find("台湾")!=-1:
        if (not province_temp) and (not city_temp) and (not sublocity_temp):
            result="台北市"
        elif province_city!="台湾省" and province_sublocaty!="台湾省":
            result = "台北市"
    if not result:
        if province_temp and city_temp and sublocity_temp and province_city!=province_temp and city_sublocaty!=city_temp and province_sublocaty!=province_temp:
            return city_temp
        if province_temp and city_temp and province_city==province_temp:
            #print('tt')
            return city_temp
        elif city_temp and sublocity_temp and city_sublocaty==city_temp:
            return city_temp
        elif province_temp and sublocity_temp and province_sublocaty==province_temp:
            return china_area[province_temp]['capital']
        if province_temp and (not city_temp) and (not sublocity_temp):
            return china_area[province_temp]['capital']
        if (not province_temp) and  city_temp and (not sublocity_temp):
            return city_temp
        if (not province_temp) and (not city_temp) and  sublocity_temp:
            return city_sublocaty
    return result

def search_foreign(country,province,city,sublocity,foreign_dic):
    result=""
    if country:
        if country in foreign_dic:
            result = country
        else:
            for key1,value1 in foreign_dic.items():
                if country in value1:
                    result = key1
    else:
        for key1,value1 in foreign_dic.items():
                if province :
                    if province in  value1 :
                        result=province
                if not province or (not result):
                    if city in value1:
                        result = key1
    return result
def read_file(file,output1,output2):
    wb=xlrd.open_workbook(file)
    sheet=wb.sheet_by_name('city_data')
    nrows=sheet.nrows
    output=open(output1,"w",encoding='utf8')
    for i in range(nrows):
        data=sheet.row_values(i)
        country=data[0]
        province=data[1]
        city = data[2]
        sublocity = data[3]
        result=gps2aritcle_address(country, province, city, sublocity,china_area,foreign_area,pinyin_zhongwen)
        #print("result",data,result)
        output.writelines("\t".join(data)+"\t"+result+"\n")
    output.close()

def read_json_file(file, output1, output2):
    f=open(file,"r",encoding='utf8')
    load_dict=json.load(f)
    #去重结果
    load_dict=list(set(load_dict))
    #print(type(load_dict),len(load_dict))
    output=open(output1,'w',encoding='utf8')
    time1=datetime.now()
    for line in load_dict:
        times=datetime.now()
        result =stringGpsTostandarddata(line,china_area,foreign_area,pinyin_zhongwen,provinceList)
        ends=datetime.now()-times

        if ends.microseconds>=1500:
            print('>2000',line,ends,ends.seconds,result)

        output.writelines(line+ "\t" + result + "\n")
    print("all,time",datetime.now()-time1)
    output.close()

def stringGpsTostandarddata(gps,china_area,foreign_area,pinyin_zhongwen,provinceList):
    result=""
    if gps and gps.find('_')==-1:

        data=re.split(r'([省市县区])',gps)
        data.append("")
        data = ["".join(i) for i in zip(data[0::2], data[1::2])]
        gps="_".join(data)
        if gps.find("_")==-1:
            gps=gps+"_"
    if gps and gps.find('_')!=-1:
        data=gps.split("_")
        country,province,city,sublocity="","","",""

        if  (not is_all_chinese(data[0])) and (not  is_all_english(data[0])):
            data[0]=""
        if len(data[0])<=1:
            data[0] = ""

        if (not  is_all_chinese(data[1])) and (not  is_all_english(data[1])):
            data[1]=""
        if len(data[1]) <= 1:
            data[1] = ""
        if len(data)>=3 and ( not is_all_chinese(data[2])) and (not is_all_english(data[2])):
            data[2]=""
        if len(data)>=3 and len(data[2])<=1:
            data[2] = ""
        if len(data)>=4 and (not is_all_chinese(data[3])) and  (not is_all_english(data[3])):
            data[3]=""
        if  len(data)>=4 and len(data[3]) <= 1:
            data[3] = ""
        if data[0][-1:]=="省" or data[0][-1:]=="市" or data[0][-1:]=="自治区" or data[0][-1:]=="自治洲" or data[0] in provinceList :
            province = data[0]
            city=data[1]
            if len(data)>=3 and (not IsContainNum(data[2])) and (not IsPunctions(data[2])) and (static_alphrase_num(data[2])<=1):
                sublocity = data[2]
        else:
            country = data[0]
            province = data[1]
            if len(data)>=3 and (not IsContainNum(data[2])) and (not IsPunctions(data[2])) and (static_alphrase_num(data[2])<=1):
                city = data[2]
            if len(data) >= 4 and (not IsContainNum(data[3])) and (not IsPunctions(data[3])) and (static_alphrase_num(data[3])<=1) :
                sublocity = data[3]

        if country or province or city or sublocity:
            #print('str',country, province, city, sublocity)
            result = gps2aritcle_address(country, province, city, sublocity,china_area,foreign_area,pinyin_zhongwen)
    return result
def gpsToStandarddata(country,province,city,sublocity,china_area,foreign_area):
    result=""

    if (country.find("香港")!=-1 or province.find("香港")!=-1 or city.find("香港")!=-1 or sublocity.find("香港")!=-1):
        result="香港特别行政区"
    elif country.find("澳门")!=-1 or province.find("澳门")!=-1 or city.find("澳门")!=-1 or sublocity.find("澳门")!=-1:
        result = "澳门特别行政区"
    elif country.find("台湾")!=-1 or province.find("台湾")!=-1 or city.find("台湾")!=-1 :
        #查找中国地区词典
        result=search_china(country, province, city, sublocity, china_area)
        #print("台湾",result)
        if not result:
            result="台北市"
    elif country.find("中国")!=-1 or country.find("中华人民共和國")!=-1 or country.find("中华人民共和国")!=-1:
        result=search_china(country, province, city, sublocity, china_area)
    elif not country:  # 国家列为空，查询所有的国内外数据
        result = search_china(country, province, city, sublocity, china_area)
        if not result:
            result = search_foreign(country, province, city, sublocity, foreign_area)
    else:#查找国外地区词典
        result = search_foreign(country, province, city, sublocity, foreign_area)
    return result







def gps2aritcle_address(china,province,city,sublocity,china_area,foreign_area,pinyin_zhongwen):
    result=""
    #print('判断标点符号开始',datetime.now())
    if china and IsPunctions(china) or " "  in china or IsContainNum(china) or (static_alphrase_num(china)>=2):
        china=""
        return result
    if IsPunctions(province) or " "  in province or IsContainNum(province) or (static_alphrase_num(province)>=2):
        province=""
    if IsPunctions(city) or " "  in city or IsContainNum(city) or (static_alphrase_num(city)>=2):
        city=""
    if IsPunctions(sublocity) or " "  in sublocity or IsContainNum(sublocity) or (static_alphrase_num(sublocity)>=2):
        sublocity=""
    if china and china[-1:]==" ":
        china=china[:-1]
    if province and province[-1:]==" ":
        province=province[:-1]
    if city and city[-1:]==" ":
        city=city[:-1]
    if sublocity and sublocity[-1:]==" ":
        sublocity=sublocity[:-1]
    if not china and (not province) and (not city) and (not sublocity):
        return result
    # print('判断语言判断开始',datetime.now())
    # #包含标点符号，含有空格，有》=2个大写字母，包含数字的内容，不处理
    # china_pinyin, province_pinyin, city_pinyin, sublocity_pinyin="","","",""
    # langage1=detect_lang(china)
    # print(china,langage1)
    # if china!="老挝" and  china!="蒙古":
    #     if langage1=="en":
    #         china_pinyin=pintohanzi(china)
    #     elif langage1=="zh":
    #         china_pinyin = china
    # else:
    #     china_pinyin = china
    # if province.find("内蒙古")!=-1:
    #     province_pinyin = province
    # else:
    #     langage2 = detect_lang(province)
    #     if langage2=="en":
    #         province_pinyin=pintohanzi(province)
    #     elif langage2=="zh":
    #         province_pinyin = province
    # langage3 = detect_lang(city)
    # if langage3=="en":
    #     city_pinyin=pintohanzi(city)
    # elif langage3=="zh":
    #     city_pinyin = city
    # print('city',city, langage3, city_pinyin)
    # langage4 = detect_lang(sublocity)
    # if langage4=="en":
    #     sublocity_pinyin=pintohanzi(sublocity)
    # elif langage4=="zh":
    #     sublocity_pinyin = sublocity
    # print('判断拼音转换开始',datetime.now())
    #print("拼音转换，",china_pinyin , province_pinyin , city_pinyin , sublocity_pinyin)
    if containenglish(china):
        if china in pinyin_zhongwen:
            china=pinyin_zhongwen[china.lower()]
        else:
            china=""
    if containenglish(province):
        if province in pinyin_zhongwen:
            province = pinyin_zhongwen[province.lower()]
        else:
            province = ""
    if containenglish(city):
        if city in pinyin_zhongwen:
            city = pinyin_zhongwen[city.lower()]
        else:
            city = ""
    if containenglish(sublocity):
        if sublocity in pinyin_zhongwen:
            sublocity = pinyin_zhongwen[sublocity.lower()]
        else:
            sublocity = ""
    if china or province or city or sublocity:
        #将中文的信息进行对应
        country=cht_to_chs(china)
        if len(country)<=1 or containenglish(country):
            country=""
        provin=cht_to_chs(province)
        if len(provin)<=1 or containenglish(provin):
            provin=""
        citys=cht_to_chs(city)
        if len(citys)<=1 or containenglish(citys):
            citys=""
        locity=cht_to_chs(sublocity)
        if len(locity)<=1 or containenglish(locity):
            locity=""
        #print(datetime.now())
        #print('convert***',country, provin, citys, locity)
        if (china and country)or (not china and (country or  provin or  citys or locity)) :
            result=gpsToStandarddata(country, provin, citys, locity,china_area,foreign_area)
    return result

import pinyin
def hanzitopinyin(key,dic):
    data = pinyin.get(key, format='strip',delimiter="")
    dic[data] = key
    if len(key) > 2 and (key[-1:] == "省" or key[-1:] == "市" or key[-1:] == "县"):
        pinyin_data = pinyin.get(key[:-1], format='strip',delimiter="")
        dic[pinyin_data] = key
    if len(key) > 3 and key[-2:] == "地区":
        pinyin_data = pinyin.get(key[:-2],format='strip', delimiter="")
        dic[pinyin_data] = key
    if len(key) > 4 and (key[-3:] == "自治州" or key[-3:] == "自治区" or key[-3:] == "自治县"):
        pinyin_data = pinyin.get(key[:-3], format='strip',delimiter="")
        dic[pinyin_data] = key
    if len(key) > 6 and key[-5:] == "特别行政区":
        pinyin_data = pinyin.get(key[:-5], format='strip',delimiter="")
        dic[pinyin_data] = key
    return dic
# dic={}
# a=[]
# for key,value in china_area.items():
#     dic=hanzitopinyin(key, dic)
#     print(dic)
#     if key.find("自治")!=-1 and key not in a:
#         a.append(key)
#     for key1,value1 in value.items():
#         if key1!="capital":
#             dic=hanzitopinyin(key1, dic)
#             if key1.find("自治") != -1 and key1 not in a:
#                 a.append(key1)
#             for data in value1:
#                 dic = hanzitopinyin(data, dic)
#                 if data.find("自治") != -1 and data not in a:
#                     a.append(data)
#
# f=open("X:\尚文清\旅游\yingwenTozhongwen.txt","w",encoding='utf8')
# for key,value in dic.items():
#     f.writelines(key+"\t"+value+"\n")
# f.close()
# print()








#print('result',search_china('中国', '广西', '来宾市', '来宾市', china_area))

china_area,foreign_area,provinceList,pinyin_zhongwen=national_list('X:\尚文清\旅游\\2019_全球省市县.xlsx')
from  datetime import datetime
output2=""
#read_file("X:\尚文清\旅游\gpsTotuniu_city.xlsx","X:\尚文清\旅游\gpsToArticle.txt",output2)
file="X:\尚文清\旅游\generalloc4400000.json"
output2=""
#根据文本进行处理
#print(datetime.now())
read_json_file(file, "X:\尚文清\旅游\gpsToArticle.txt", output2)

times=datetime.now()

# 根据字符串进行处理
result=stringGpsTostandarddata('台湾_太平區_太平區_永樂街92号',china_area,foreign_area,pinyin_zhongwen,provinceList)
end=datetime.now()-times
print('result',result,end)
