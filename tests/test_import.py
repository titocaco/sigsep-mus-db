import pytest
import dsdtools
import dsdtools.evaluate as ev
import numpy as np


@pytest.fixture(params=['data/DSD100subset'])
def dsd(request):
    return dsdtools.DB(root_dir=request.param, evaluation=True)


def test_mat_import(dsd):
    # run the baseline evaluation
    dsd.evaluate(
        estimates_dirs='tests/data/'
    )
    # load the mat file
    mat_data = ev.Data(dsd.evaluator.data.columns)
    mat_data.import_mat('tests/data/results.mat')
    # compare the methods
    # make sure they have the same columns
    assert set(mat_data.df.columns) == set(dsd.evaluator.data.df.columns)
    # estimate_dir will be different; remove it from both
    del mat_data.df['estimate_dir']
    del dsd.evaluator.data.df['estimate_dir']
    # reorder the columns so they are the same
    mat_data.df = mat_data.df[dsd.evaluator.data.df.columns]
    # test the numerical fields
    mat_sub = mat_data.df.select_dtypes(include=['float64'])
    dsd_sub = dsd.evaluator.data.df.select_dtypes(include=['float64'])
    assert np.all(np.isclose(mat_sub, dsd_sub))
    # test the non-number fields
    mat_sub = mat_data.df.select_dtypes(exclude=['float64'])
    dsd_sub = dsd.evaluator.data.df.select_dtypes(exclude=['float64'])
    assert mat_sub.equals(dsd_sub)


def test_json_import(dsd):
    # run the baseline evaluation
    dsd.evaluate(
        estimates_dirs='tests/data/'
    )
    # load the json file
    json_data = ev.Data(dsd.evaluator.data.columns)
    json_data.import_json('tests/data/evaluation.json')
    # compare the methods
    # make sure they have the same columns
    assert set(json_data.df.columns) == set(dsd.evaluator.data.df.columns)
    # estimate_dir will be different; remove it from both
    del json_data.df['estimate_dir']
    del dsd.evaluator.data.df['estimate_dir']
    # reorder the columns so they are the same
    json_data.df = json_data.df[dsd.evaluator.data.df.columns]
    # test the numerical fields
    json_sub = json_data.df.select_dtypes(include=['float64'])
    dsd_sub = dsd.evaluator.data.df.select_dtypes(include=['float64'])
    assert np.all(np.isclose(json_sub, dsd_sub))
    # test the non-number fields
    json_sub = json_data.df.select_dtypes(exclude=['float64'])
    dsd_sub = dsd.evaluator.data.df.select_dtypes(exclude=['float64'])
    assert json_sub.equals(dsd_sub)