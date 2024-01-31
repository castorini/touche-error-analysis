#!/usr/bin/env python3
import pandas as pd

def construct_count_aggregate_dataset(df):
    df = construct_and_count_dataset(df)
    ret = {}
    for i in df:
        for model, agreements in i['agreements'].items():
            if model not in ret:
                ret[model] = {'Agreement': 0, 'Disagreement': 0}

            ret[model]['Agreement'] = ret[model]['Agreement'] + agreements['agreement']
            ret[model]['Disagreement'] = ret[model]['Disagreement'] + agreements['disagreement']

    ret_df = []

    for model in ret.keys():
        ret_df += [{'Model': model, 'Agreement': ret[model]['Agreement'], 'Disagreement': ret[model]['Disagreement']}]

    return ret_df

def construct_and_count_dataset(df):
    df = construct_dataset(df)
    for i in df:
        i['agreements'] = {}
        for model, scores in i['scores'].items():
            pairs_with_agreement, pairs_with_disagreement = count_pairs_with_agreement_and_disagreement_for_lnc2(scores)
            i['agreements'][model] = {"agreement": pairs_with_agreement, "disagreement": pairs_with_disagreement}
        del i['scores']

    return df


def construct_dataset(df):
    ret = {}
    for _, i in df.iterrows():
        if i['qid'] not in ret:
            ret[i['qid']] = {}
        doc_id, k = i['docid'].split('_____')
        k = int(k)
        if doc_id not in ret[i['qid']]:
            ret[i['qid']][doc_id] = {'scores': {}}
        
        for model, score in i['scores'].items():
            if doc_id not in ret[i['qid']]:
                ret[i['qid']][doc_id]['scores'] = {}

            if model not in ret[i['qid']][doc_id]['scores']:
                ret[i['qid']][doc_id]['scores'][model] = {}

            ret[i['qid']][doc_id]['scores'][model][k] = score

    df_ret = []
    for qid in ret.keys():
        for doc_id in ret[qid].keys():
            df_ret += [{'qid': qid, 'docid': doc_id, 'scores': ret[qid][doc_id]['scores']}]

    return df_ret


def count_pairs_with_agreement_and_disagreement_for_lnc2(scores):
    pairs_with_agreement, pairs_with_disagreement = 0, 0

    for k_short_document, score_short_document in scores.items():
        for k_long_document, score_long_document in scores.items():
            if k_short_document >= k_long_document:
                # precondition not met
                continue

            assert k_short_document < k_long_document

            if score_short_document > score_long_document:
                pairs_with_disagreement += 1
            else:
                pairs_with_agreement += 1

    return pairs_with_agreement, pairs_with_disagreement


if __name__ == '__main__':
    for i in ['sample-without-title-for-lnc2-scores', 'sample-with-title-for-lnc2-scores']:
        df = construct_count_aggregate_dataset(pd.read_json(i + '.jsonl', lines=True))
        df = pd.DataFrame(df)
        df['AgreementRatio'] = df['Agreement'] / (df['Agreement'] + df['Disagreement'])
        df.to_json(i + '-aggregated-lnc2-agreement.jsonl', lines=True, orient='records')

        
