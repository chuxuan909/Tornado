#!/usr/bin/env python
# -*- coding:utf-8 -*-

num_dict={'fish':[0,0,0],
          'doll':[0,0,0],
          'chess':{'classic':[0,0,0],
                   'classic_no_shuffle':[0,0,0],
                   'slander':[0,0,0],
                   'double_slander':[0,0,0]
                  },
          'turntable':[0,0,0],
          'total':[0,]
          }

reflect_dict={
    '1':'fish',
    '2':'doll',
    '3':'chess',
    '4':'turntable',
}


reflect_zh_dict={
    'fish':'捕鱼',
    'doll':'娃娃机',
    'chess':'斗地主',
    'turntable':'幸运闯关',
    'classic':'经典洗牌',
    'slander':'经典癞子',
    'classic_no_shuffle':'经典不洗牌',
    'double_slander':'天地癞子',
    'total':'总计'
}

def game_sort(input_dicts,game_kind,game_types=None):
    '''按照中高低的分类营收统计'''
    global  num_dict
    num_dict['total'][0]+=input_dicts.get('revenue')
    if game_types:
        if input_dicts.get('level') == '新手场':
            num_dict[game_kind][game_types][0]+=input_dicts.get('revenue')
        elif input_dicts.get('level') == '中级场':
            num_dict[game_kind][game_types][1]+=input_dicts.get('revenue')
        else:
            num_dict[game_kind][game_types][2]+=input_dicts.get('revenue')
    else:
        if input_dicts.get('level') == '初级场':
            num_dict[game_kind][0]+=input_dicts.get('revenue')
        elif input_dicts.get('level') == '中级场':
            num_dict[game_kind][1]+=input_dicts.get('revenue')
        else:
            # print('高级场',input_dicts.get('gameId'),input_dicts)
            num_dict[game_kind][2]+=input_dicts.get('revenue')

def game_detailed(input_dicts):
    '''更详细的分类'''
    if input_dicts.get('type') == '经典洗牌':
        game_sort(input_dicts,'chess','classic')
    elif input_dicts.get('type') == '经典不洗牌':
        game_sort(input_dicts,'chess','classic_no_shuffle')
    elif input_dicts.get('type') == '经典癞子':
        game_sort(input_dicts,'chess','slander')
    elif input_dicts.get('type') == '天地癞子':
        game_sort(input_dicts,'chess','double_slander')


# def game_doll(doll_dicts):
#     global num_dict
#     if doll_dicts.get('type') == '普通':
#         pass
#     if doll_dicts.get('type') == 'VIP':
#         pass

def openr_games(all_dicts):
    '''游戏营收记录分类统计'''
    global reflect_dict
    for i in all_dicts:
        # print('数据处理中的mongo dict字典为',i)
        if i.get('gameId') == '3':
            game_detailed(i)
        else:
            game_sort(i,reflect_dict[i.get('gameId')])
    # print('统计后的字典：',num_dict)
    return num_dict

def record_output(num_dicts):
    '''输出统计好的营收记录'''
    global reflect_zh_dict
    for key in num_dicts:
        if key == 'chess':
            print('\n')
            print('================================================')
            print('%s\t\t新手场\t\t中级场\t\t高级场' % reflect_zh_dict[key])
            for index_key in num_dicts[key]:
                print('\n')
                print('%s\t' % reflect_zh_dict[index_key],end='')
                for i in num_dicts[key][index_key]:
                    print('%s\t\t\t' % i,end='')

        else:
            print('\n')
            print('================================================')
            print('%s\t\t低级场\t\t中级场\t\t高级场' % reflect_zh_dict[key])
            print('\t',end='')
            for index in num_dict[key]:
                print('\t\t%s\t' % index,end='')

def num_dict_initialize():
    '''初始化字典'''
    global num_dict
    num_dict=num_dict={'fish':[0,0,0],
          'doll':[0,0,0],
          'chess':{'classic':[0,0,0],
                   'classic_no_shuffle': [0, 0, 0],
                   'slander':[0,0,0],
                   'double_slander':[0,0,0]
                  },
          'turntable':[0,0,0],
          'total':[0,]
          }

if __name__ == '__main__':
    # 测试数据统计是否正常
    import pymongo
    mongo_client = pymongo.MongoClient("mongodb://xxx.xxx.xxx.xxx:27017/")
    m_db = mongo_client['GHall']
    m_col = m_db['userPut']
    all_dicts = m_col.find({'date': '2019-10-31'}, {'_id': 0})
    record_output(openr_games(all_dicts))


