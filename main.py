import numpy as np
import pandas as pd
from pandas.core.arrays.numeric import (
    NumericArray,
    NumericDtype,
)


class DataGen:
    """
    pandas dataframe을 받아
    컬럼별 데이터 타입 및 통계 정보를 기준으로 적절한 데이터를 임의로 생성
    """

    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.column_types = {
            "numeric": [],
            "categorical": [],
            "datetime": [],
            "boolean": []
        }
        self._init_column_dtype_classification()

    def __iter__(self):
        for idx, item in self.df.iterrows():
            yield idx, item

    def _init_column_dtype_classification(self):
        self.column_types["numeric"] = df.select_dtypes(include=['number']).columns.tolist()
        self.column_types["categorical"] = df.select_dtypes(include=['category']).columns.tolist()
        self.column_types["datetime"] = df.select_dtypes(include=['datetime']).columns.tolist()
        self.column_types["boolean"] = df.select_dtypes(include=['bool']).columns.tolist()
        self.column_types["etc"] = df.select_dtypes(
            exclude=['number', 'category', 'datetime', 'bool']
        ).columns.tolist()

    def _run_statistics(self):
        statistics = {}

    def _numeric_statistics(self):
        """
        3-sigma 내의 값 중 분포를 고려한 임의의 값을 생성합니다.
        :return:
        """
        pass

    def _categorical_statistics(self):
        """
        해당 컬럼 중 랜덤한 값을 샘플링하여 값을 생성합니다.
        :return:
        """
        pass

    def _datetime_statistics(self):
        pass

    def _etc_statistics(self):
        """
        해당 컬럼 중 랜덤한 값을 샘플링하여 값을 생성합니다.
        :return:
        """
        pass


if __name__ == '__main__':
    df = pd.DataFrame(np.empty([4, 5]))
    df["etc"] = pd.Series(data=[[1,2,3,4,5]])
    print(df)
    dg = DataGen(df)
    # for idx, item in dg:
    #     print(idx, item)
    print(dg.column_types)
    print(dg.column_types.values())