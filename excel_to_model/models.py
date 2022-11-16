from typing import List


class Field(object):
    def __init__(self, name: str, verbose_name: str, max_length: int = 128):
        self.name = name
        self.verbose_name = verbose_name
        self.max_length = max_length

    def __str__(self):
        return f'<Field>{self.name}:{self.verbose_name}'

    def __repr__(self):
        return self.__str__()


class Model(object):
    def __init__(self, name: str, verbose_name: str, id_field: Field, fields: List[Field]):
        """

        :param name: 模型名称
        :param verbose_name: 中文名
        """
        self.name = name
        self.verbose_name = verbose_name
        self.id_field = id_field
        self.fields: List[Field] = fields

    @property
    def snake_name(self):
        import re
        pattern = re.compile(r'(?<!^)(?=[A-Z])')
        name = pattern.sub('_', self.name).lower()
        return name

    def __str__(self):
        return f'<Model>{self.name}:{self.verbose_name}'

    def __repr__(self):
        return self.__str__()
