# -*- coding: utf-8 -*-
# @Author:  SmokedInk
# @Title:   collections
# @Time:    2019-12-26 14:14:05
# @Desc:    collections

from enum import Enum
from config.exceptions import EnumError


class BaseEnum(Enum):

    @classmethod
    def check(cls, value):
        values = [obj.value[0] for obj in list(cls.__members__.values())]
        if value not in values:
            raise EnumError("{enum}:{value}: 不存在".format(
                value=value,
                enum = cls.__name__
            ))

    @classmethod
    def get_value_dict(cls):
        value_dict = {}
        for obj in list(cls.__members__.values()):
            value_dict.update({obj.value[0]:obj.value[1]})
        return value_dict
