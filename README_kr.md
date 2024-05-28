# DataGen
DataGen은 테스트용 데이터 생성을 위한 라이브러리입니다.   
판다스의 데이터프레임을 기반으로 동일한 스키마의 유사 데이터를 생성합니다.

# 동작 방식
DataGen은 데이터프레임을 입력 받아 임의의 테스트 데이터를 생성합니다.   
내부적으로 데이터 생성을 위한 데이터 유형별 통계 지표를 생성합니다.   
통계 지표를 활용하여 해당 데이터 유형에 적합한 유사 데이터를 생성합니다.

## 데이터 분류 및 생성
- Numeric   : 숫자형 데이터. 커널 밀도 추정(Kernel Density Estimation, KDE) 기법을 활용한 임의의 값을 생성합니다.
              커널 밀도 함수는 `scipy.stats`의 `gaussian_kde`를 사용합니다.
- Category  : 범주형 데이터. 각 값의 출현 빈도를 측정하여 빈도의 비율대로 값을 생성합니다.
- Datetime  : ISO-8601 표준을 따르는 날짜형 데이터. Pandas Timestamp로 변환되어 해당 날짜 사이의 임의의 값을 생성합니다. 
- Boolean   : 참/거짓 데이터. 각 값의 출현 빈도를 측정하여 빈도의 비율대로 값을 생성합니다.
- ETC       : 위에서 언급되지 않은 모든 데이터. 값을 랜덤으로 복원추출하여 데이터를 생성합니다.

# 사용법
df라는 판다스 데이터프레임이 있다고 가정합니다.
100,000 row의 데이터를 생성합니다.
생성된 객체는 Iteration을 통해 각 row에 접근할 수 있습니다.
```python
from datagen import DataGen

datagen = DataGen(df=df, count=100_000)
for idx, row in datagen:
    print(idx, row)
```

데이터프레임을 가져오기 위해서는 다음과 같이 수행합니다.
```python
generated_df = datagen.dataframe
```

