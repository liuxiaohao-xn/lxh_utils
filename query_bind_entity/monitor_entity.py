from typing import Text, List
import pandas as pd
import os
from itertools import product
"""
场景说明：
    在做问答系统时，会遇到如下问题
    
    介绍一下盈合机器人
    介绍一下盈峰集团
    介绍一下xxx公司
    ...

    上面这些问句语义都很相似且不能穷举，需要通过实体(如 盈合机器人)进一步确认问题，以达到我在问 介绍一下盈峰集团 时不会误命中  介绍一下盈合机器人。

    以上情况query在找到标准问句后，需要二次确认query中的实体和标准问句绑定的实体是否一样，进而确定为是否为同一个问题，而实际情况问题可绑定多个实体，
    一个实体又有多种泛化实体。如何将query中抽取出来的实体和绑定实体集进行快速比较参考一下代码解决。

entities格式： query\tentities1\tentities2...
entites格式：entity1\nentity2...
"""

def query_bind_entities(csv_file: Text):
    query_with_entities = []
    for i, _irow in pd.read_csv(csv_file, sep="\t", header=None).iterrows():
        _irow = list(_irow)
        _query, _all_entities = _irow[0], _irow[1:]
        _bind_entities = []
        for _entities in _all_entities:
            if str(_entities) == "nan":
                continue
            _entities = _entities.split("\n")
            _entities = [entity for entity in _entities if entity.strip()]
            _bind_entities.append(_entities)
        # 不同类型实体组合可能
        # 这里要手动录入实体列数，如这里总共有两列,增加0,1,2
        if len(_bind_entities) == 0:
            continue
        elif len(_bind_entities) == 1:
            query_with_entities.append(
                (i, _query, list(product(_bind_entities[0]))) 
            )
        elif len(_bind_entities) == 2:
            query_with_entities.append(
                (i, _query, list(product(_bind_entities[0], _bind_entities[1])))
            )
        else:
            raise Exception(f"_bind_entities is out of range")
    
    def _split_entity(query_with_entity):
        res = []
        res.append(query_with_entity[0])
        res.append(query_with_entity[1])
        _combine_entities = []
        for combine_entities in query_with_entity[2]:
            _tuple_entities = []
            for combine_entity in combine_entities:
                _tuple_entities.extend([entity for entity in combine_entity.split("&&") if entity.strip()])
            _combine_entities.append(tuple(_tuple_entities))
        res.append(_combine_entities)
        return res
    query_with_entities = map(
        _split_entity,
        query_with_entities
    )
    return query_with_entities
    

if __name__=="__main__":
    for item in query_bind_entities(
        r"./entities.csv"
    ):
        print(item)
   