import copy
from typing import List

from icecream import ic
import numpy as np
import pandas as pd
from pandas.core.arrays.numeric import (
    NumericArray,
    NumericDtype,
)


class DataGen:
    """
    pandas DataFrame을 받아 컬럼별 데이터 타입 및 통계 정보를 생성합니다.
    생성된 통계 데이터를 기반으로 적절한 데이터를 임의로 생성합니다.
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.column_types = {
            "numeric": [],
            "categorical": [],
            "datetime": [],
            "boolean": []
        }
        self.statistics = {}
        self._init_column_dtype_classification()
        self._convert_column_dtype_object_to_category()
        self._categorical_statistics()

    def __iter__(self):
        for idx, item in self.df.iterrows():
            yield idx, item

    def _preprocessing(self):
        pass

    def _init_column_dtype_classification(self):
        self.column_types["numeric"] = df.select_dtypes(include=["number"]).columns.tolist()
        self.column_types["categorical"] = df.select_dtypes(include=["category"]).columns.tolist()
        self.column_types["datetime"] = df.select_dtypes(include=["datetime"]).columns.tolist()
        self.column_types["boolean"] = df.select_dtypes(include=["bool"]).columns.tolist()
        self.column_types["etc"] = df.select_dtypes(
            exclude=["number", "category", "datetime", "bool"]
        ).columns.tolist()

    def _convert_column_dtype_object_to_category(self):
        etc_columns = copy.deepcopy(self.column_types["etc"])
        for column in etc_columns:
            try:
                self.df[column] = self.df[column].astype("category")
                self.column_types["categorical"].append(column)
                self.column_types["etc"].remove(column)
            except TypeError:
                continue
            except Exception:
                raise

    def _run_statistics(self):
        statistics = {}

    def _numeric_statistics(self):
        """
        3-sigma 내의 값 중 분포를 고려한 임의의 값을 생성합니다.
        :return:
        """
        pass

    @staticmethod
    def calculate_relative_frequencies_rate(value_counts: dict):
        total_counts = sum(value_counts.values())
        relative_frequencies = {key: value / total_counts for key, value in value_counts.items()}
        return relative_frequencies

    @staticmethod
    def calculate_value_counts(series: pd.Series) -> dict:
        return series.value_counts().to_dict()

    def _categorical_statistics(self):
        for column in self.column_types["categorical"]:
            value_counts = self.calculate_value_counts(self.df[column])
            self.statistics[column] = {
                "categorical": {
                    "value_counts": value_counts,
                    "frequencies_rate": self.calculate_relative_frequencies_rate(value_counts)
                }
            }

    def _generate_categorical_data(self, count: int) -> List[pd.Series]:
        result: List[pd.Series] = []

        for column in self.column_types["categorical"]:
            frequencies_rate = self.statistics[column]["categorical"]["frequencies_rate"]
            keys = list(frequencies_rate.keys())
            values = list(frequencies_rate.values())
            generated_data = np.random.choice(keys, size=count, p=values)
            result.append(pd.Series(generated_data, dtype="category", name=column))

        return result


    def _datetime_statistics(self):
        pass

    def _etc_statistics(self):
        """
        해당 컬럼 중 랜덤한 값을 샘플링하여 값을 생성합니다.
        :return:
        """
        pass

    def generate(self, count: int) -> pd.DataFrame:
        data = self._generate_categorical_data(count)
        return pd.concat(data, axis=1)


if __name__ == "__main__":
    df = pd.DataFrame(np.empty([4, 5]))
    df["etc"] = pd.Series(data=[[1,2,3,4,5]])
    df["item"] = pd.Series(data=["a", "b", "c", "a", "a"])
    df["person"] = pd.Series(data=["inu", "joe", "stew", "stew", "inu", "joe", "joe", "inu", "inu", "inu"])
    print(df)
    print(df.info())
    dg = DataGen(df)
    # for idx, item in dg:
    #     print(idx, item)
    print(dg.column_types)
    print(dg.column_types.values())
    print(dg.statistics)
    gen_df = dg.generate(count=100)
    print(gen_df)
    print(gen_df.info())