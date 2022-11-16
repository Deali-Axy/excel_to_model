import os
import re
from typing import List, Optional

from pypinyin import pinyin, lazy_pinyin, Style
from jinja2 import Environment, PackageLoader, FileSystemLoader
from excel_to_model.models import Model, Field


class ExcelToModel(object):
    def __init__(self, filepath, header_index=0):
        self.filepath = filepath
        self.header_index = header_index
        self.columns = []
        self.fields: List[Field] = []

        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.template_path = os.path.join(self.base_dir, 'templates')
        self.jinja2_env = Environment(loader=FileSystemLoader(self.template_path))

        self.load_file()

    @staticmethod
    def to_pinyin(text: str) -> str:
        pattern = r'~`!#$%^&*()_+-=|\';"＂:/.,?><~·！@#￥%……&*（）——+-=“：’；、。，？》{《}】【\n\]\[ '
        text = re.sub(r"[%s]+" % pattern, "", text)
        return '_'.join(lazy_pinyin(text, style=Style.NORMAL))

    def load_file(self):
        import pandas as pd
        xlsx = pd.ExcelFile(self.filepath)
        df = pd.read_excel(xlsx, 0, header=self.header_index)
        df.fillna('', inplace=True)
        self.columns = list(df.columns)
        for col in self.columns:
            field = Field(self.to_pinyin(col), col)
            self.fields.append(field)
            for index, row in df.iterrows():
                item_len = len(str(row[col]))
                if item_len > field.max_length:
                    field.max_length = item_len + 32

            print(field.verbose_name, field.name, field.max_length)

    def find_field_by_verbose_name(self, verbose_name) -> Optional[Field]:
        for field in self.fields:
            if field.verbose_name == verbose_name:
                return field

        return None

    def generate_file(self, model_name: str, verbose_name: str, id_field_verbose_name: str, output_filepath: str):
        template = self.jinja2_env.get_template('output.jinja2')
        context = {
            'model': Model(
                model_name, verbose_name,
                self.find_field_by_verbose_name(id_field_verbose_name),
                self.fields
            ),
            'excel_filepath': self.filepath,
            'excel_header': self.header_index,
        }
        with open(output_filepath, 'w+', encoding='utf-8') as f:
            render_result = template.render(context)
            f.write(render_result)


if __name__ == '__main__':
    tool = ExcelToModel('file.xlsx')
    tool.generate_file('CitizenFertility', '房价与居民生育率', '证件号码', 'output/citizen_fertility.py')
