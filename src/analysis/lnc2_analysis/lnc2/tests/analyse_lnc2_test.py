from lnc2.analyse_lnc2 import construct_dataset, count_pairs_with_agreement_and_disagreement_for_lnc2, construct_and_count_dataset, construct_count_aggregate_dataset
import pandas as pd

perfect_df = pd.DataFrame([
    {"qid": "3", "docid": "doc-1_____1", "scores": {"Model1": 1.2, "Model2": 2.3, "Model3": 3.4}},
    {"qid": "4", "docid": "doc-1_____2", "scores": {"Model1": 0.2, "Model2": 0.3, "Model3": 0.4}},
    {"qid": "3", "docid": "doc-1_____3", "scores": {"Model1": 2.4, "Model2":4.6, "Model3": 6.8}},
])

non_perfect_df = pd.DataFrame([
    {"qid": "3", "docid": "doc-1_____1", "scores": {"Model1": 1.2, "Model2": 2.3, "Model3": 3.4}},
    {"qid": "3", "docid": "doc-1_____2", "scores": {"Model1": 0.2, "Model2": 0.3, "Model3": 0.4}},
    {"qid": "3", "docid": "doc-1_____3", "scores": {"Model1": 2.4, "Model2":4.6, "Model3": 6.8}},
])

def test_construct_dataset_on_perfect_df():
    df = perfect_df.copy()
    expected = [
        {"qid": "3", "docid": "doc-1", "scores": {"Model1": {1: 1.2, 3: 2.4}, "Model2": {1: 2.3, 3: 4.6}, "Model3": {1: 3.4, 3: 6.8}}},
        {"qid": "4", "docid": "doc-1", "scores": {"Model1": {2: 0.2}, "Model2": {2: 0.3}, "Model3": {2: 0.4}}},
    ]
    
    actual = construct_dataset(df)
    
    assert expected == actual

def test_counting_on_non_perfect_df():
    df = non_perfect_df.copy()
    expected = [
        {"qid": "3", "docid": "doc-1", "agreements": {"Model1": {"agreement": 2, "disagreement": 1}, "Model2": {"agreement": 2, "disagreement": 1}, "Model3": {"agreement": 2, "disagreement": 1}}},
    ]
    
    actual = construct_and_count_dataset(df)
    
    assert expected == actual


def test_counting_on_perfect_df():
    df = perfect_df.copy()
    expected = [
        {"qid": "3", "docid": "doc-1", "agreements": {"Model1": {"agreement": 1, "disagreement": 0}, "Model2": {"agreement": 1, "disagreement": 0}, "Model3": {"agreement": 1, "disagreement": 0}}},
        {"qid": "4", "docid": "doc-1", "agreements": {"Model1": {"agreement": 0, "disagreement": 0}, "Model2": {"agreement": 0, "disagreement": 0}, "Model3": {"agreement": 0, "disagreement": 0}}},
    ]
    
    actual = construct_and_count_dataset(df)
    
    assert expected == actual

def test_aggregating_on_perfect_df():
    df = perfect_df.copy()
    expected = [{'Model': 'Model1', 'Agreement': 1, 'Disagreement': 0},
                {'Model': 'Model2', 'Agreement': 1, 'Disagreement': 0},
                {'Model': 'Model3', 'Agreement': 1, 'Disagreement': 0},
               ]
    
    actual = construct_count_aggregate_dataset(df)
    
    assert expected == actual


def test_construct_dataset_on_non_perfect_df():
    df = non_perfect_df.copy()
    expected = [
        {"qid": "3", "docid": "doc-1", "scores": {"Model1": {1: 1.2, 2: 0.2, 3: 2.4}, "Model2": {1: 2.3, 2: 0.3, 3: 4.6}, "Model3": {1: 3.4, 2: 0.4, 3: 6.8}}}
    ]
    
    actual = construct_dataset(df)
    
    assert expected == actual

def test_counting_pairs_everything_agrees_01():
    expected_agreement, expected_disagreement = (1, 0)

    scores = {1: 1.2, 2: 1.2}

    actual = count_pairs_with_agreement_and_disagreement_for_lnc2(scores)
    
    assert expected_agreement == actual[0]
    assert expected_disagreement == actual[1]

def test_counting_pairs_everything_agrees_02():
    expected_agreement, expected_disagreement = (3, 0)

    scores = {1: 1.2, 3: 2.4, 4: 2.5}

    actual = count_pairs_with_agreement_and_disagreement_for_lnc2(scores)
    
    assert expected_agreement == actual[0]
    assert expected_disagreement == actual[1]

def test_counting_pairs_almost_everything_agrees_01():
    expected_agreement, expected_disagreement = (2, 1)

    scores = {1: 1.2, 3: 2.4, 4: 2.3}

    actual = count_pairs_with_agreement_and_disagreement_for_lnc2(scores)
    
    assert expected_agreement == actual[0]
    assert expected_disagreement == actual[1]
    
