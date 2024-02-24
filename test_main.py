import warnings

warnings.filterwarnings(
    "ignore", category=DeprecationWarning
)  # importing first to ignore warnings from pandas

from classes import VanillaPythonAnalysis
from functions import *

import numpy as np
import pandas as pd


data_file = get_data_pd()
analysis = VanillaPythonAnalysis(file_path)


def test_mean_salary():
    assert np.isclose(
        analysis.get_average_salary(),
        float(data_file["salary_in_usd"].mean()),
        atol=1e-8,
    )


def test_salary_deviation():
    # using a higher atol as the value is large, making a 3USD difference in deviation acceptable considering the diffent methods used to calculate it
    assert np.isclose(
        analysis.get_salary_deviaton(), data_file["salary_in_usd"].std(), atol=3
    )


def test_years_deviation():
    dev, mean = analysis.get_years_deviaton()
    assert np.isclose(dev, data_file["work_year"].std(), atol=0.1)
    assert np.isclose(mean, data_file["work_year"].mean(), atol=0.1)


def test_job_frequency():
    frequency_pandas = data_file["job_category"].value_counts().to_dict()
    frequency_vanilla = dict(analysis.get_job_category_frequency())
    assert frequency_pandas == frequency_vanilla


def test_get_correlation():
    assert np.isclose(
        analysis.get_correlation_salary_years(),
        np.corrcoef(data_file["work_year"], data_file["salary_in_usd"])[0, 1],
        atol=1e-8,
    )
