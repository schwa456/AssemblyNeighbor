import pandas as pd
from AssemblyMember import *
from data_setup import *

def get_vote_info(df):
    vote_info = df.pivot(index='의원', columns='의안번호', values='표결결과')
    vote_info.fillna('불참', inplace=True)
    return vote_info

def get_vote_embedding(vote_info):
    vote_mapping = {
        '찬성' : 1,
        '기권' : 0,
        '반대' : -1,
        '불참' : -2
    }

    vote_embedding = vote_info.replace(vote_mapping)
    return vote_embedding


def __main__():
    df = get_data()
    vote_info = get_vote_info(df)
    vote_embedding = get_vote_embedding(vote_info)
    print(vote_embedding)
    vote_embedding.to_csv('../data/vote_embedding.csv')


if __name__ == '__main__':
    __main__()