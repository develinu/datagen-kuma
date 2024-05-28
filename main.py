import copy
from typing import List
from collections import defaultdict

from icecream import ic
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde


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
        self.statistics = defaultdict(dict)
        self._init_column_dtype_classification()
        self._run_statistics()

    def __iter__(self):
        for idx, item in self.df.iterrows():
            yield idx, item

    def _init_column_dtype_classification(self):
        self.column_types["numeric"] = df.select_dtypes(include=["number"]).columns.tolist()
        self.column_types["categorical"] = df.select_dtypes(include=["category"]).columns.tolist()
        self.column_types["datetime"] = df.select_dtypes(include=["datetime"]).columns.tolist()
        self.column_types["boolean"] = df.select_dtypes(include=["bool"]).columns.tolist()
        self.column_types["etc"] = df.select_dtypes(
            exclude=["number", "category", "datetime", "bool"]
        ).columns.tolist()
        self._convert_column_dtype_object_to_category()
        self._convert_column_dtype_object_to_datetime()

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

    def _convert_column_dtype_object_to_datetime(self):
        etc_columns = copy.deepcopy(self.column_types["etc"])
        numeric_columns = copy.deepcopy(self.column_types["numeric"])
        columns_map = {
            "etc": etc_columns,
            "numeric": numeric_columns
        }
        for column_category, columns in columns_map.items():
            for column in columns:
                try:
                    self.df[column] = pd.to_datetime(self.df[column], format="ISO8601")
                    self.column_types["datetime"].append(column)
                    self.column_types[column_category].remove(column)
                except TypeError:
                    continue
                except ValueError:
                    continue
                except Exception:
                    raise

    def _run_statistics(self):
        self._numeric_statistics()
        self._categorical_statistics()
        self._boolean_statistics()
        self._datetime_statistics()
        self._etc_statistics()

    def _numeric_statistics(self):
        """
        커널 밀도 추정(Kernel Density Estimation, KDE) 기법을 활용한 임의의 값을 생성합니다.
        커널 밀도 함수는 `scipy.stats`의 `gaussian_kde`를 사용합니다.
        :return:
        """

        for column in self.column_types["numeric"]:
            series = self.df[column].dropna()
            self.statistics[column].update({
                "min": series.min(),
                "max": series.max(),
                "kde": gaussian_kde(series.values),
                "dtype": series.dtype
            })

    def _generate_numeric_data(self, count: int) -> List[pd.Series]:
        result: List[pd.Series] = []

        for column in self.column_types["numeric"]:
            kde = self.statistics[column]["kde"]
            min_value = self.statistics[column]["min"]
            max_value = self.statistics[column]["max"]
            dtype = self.statistics[column]["dtype"]
            kde_data = kde.resample(count).flatten()
            generated_data = np.clip(kde_data, min_value, max_value).astype(dtype)
            result.append(pd.Series(generated_data, dtype=dtype, name=column))

        return result

    def _boolean_statistics(self):
        pass

    def _generate_boolean_data(self, count: int) -> List[pd.Series]:
        return []

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
            self.statistics[column].update({
                "value_counts": value_counts,
                "frequencies_rate": self.calculate_relative_frequencies_rate(value_counts)
            })

    def _generate_categorical_data(self, count: int) -> List[pd.Series]:
        result: List[pd.Series] = []

        for column in self.column_types["categorical"]:
            frequencies_rate = self.statistics[column]["frequencies_rate"]
            keys = list(frequencies_rate.keys())
            values = list(frequencies_rate.values())
            generated_data = np.random.choice(keys, size=count, p=values)
            result.append(pd.Series(generated_data, dtype="category", name=column))

        return result

    def _datetime_statistics(self):
        for column in self.column_types["datetime"]:
            self.statistics[column].update({
                "start_datetime": self.df[column].min(),
                "end_datetime": self.df[column].max()
            })

    def _generate_datetime_data(self, count: int) -> List[pd.Series]:
        result: List[pd.Series] = []

        for column in self.column_types["datetime"]:
            start_datetime = self.statistics[column]["start_datetime"]
            end_datetime = self.statistics[column]["end_datetime"]
            generated_data = pd.to_datetime(
                np.random.randint(start_datetime.value, end_datetime.value, size=count, dtype="int64"),
                unit='ns'
            )
            result.append(pd.Series(generated_data, dtype="datetime64[ns]", name=column))

        return result

    def _etc_statistics(self):
        """
        해당 컬럼 중 랜덤한 값을 샘플링하여 값을 생성합니다.
        :return:
        """
        pass

    def _generate_etc_data(self, count: int) -> List[pd.Series]:
        return []

    def generate(self, count: int) -> pd.DataFrame:
        generated_data = [
            *self._generate_categorical_data(count),
            *self._generate_numeric_data(count),
            *self._generate_datetime_data(count),
            *self._generate_boolean_data(count),
            *self._generate_etc_data(count),
        ]
        ic(generated_data)
        return pd.concat(generated_data, axis=1)


if __name__ == "__main__":
    df = pd.read_csv("./data/events.csv")
    series_len = len(df.timestamp)
    df["my_dt"] = pd.date_range("2020-01-01", "2024-05-28", periods=series_len)
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