import re

import pandas as pd

from utilities import get_first

dim_df = pd.read_csv("candidateEvalData/dim_df_correct.csv")


def parse_dimensions(row):
    dim_re = '([\d\.\sx,×]+\s*cm(?![\s\)\(]*Image)|[\d\s]+by[\d\s]+in)'
    raw_dimension = get_first(re.findall(dim_re, row))
    raw_dimensions = re.findall(r'[\d\.,]+', raw_dimension)[:3]

    dimensions = []
    for dimension in raw_dimensions:
        dimension = float(dimension.replace(',', '.'))
        if 'in' in raw_dimension:
            dimension = dimension * 2.54
        dimensions.append(dimension)

    for _ in range(3 - len(dimensions)):
        dimensions.append(None)
    return pd.Series(dimensions)


dim_df[
    ['processed_height', 'processed_width', 'processed_depth']
] = dim_df['rawDim'].apply(lambda row: parse_dimensions(row))
