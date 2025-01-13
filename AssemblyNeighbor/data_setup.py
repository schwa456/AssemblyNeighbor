import pandas as pd
from AssemblyMember import *

def get_data():
    file_path = '../data/데이터_국회의원 본회의 표결정보.xlsx'
    df = pd.read_excel(file_path)
    return df

def get_members_df(df):
    members = {}
    for _, row in df.iterrows():
        members[row['의원']] = row['정당']

    members_df = pd.DataFrame.from_dict(members, orient='index', columns=['party'])

    members_df.reset_index(inplace=True)
    members_df.rename(columns={'index' : 'name'}, inplace=True)

    return members_df

def get_agendas_df(df):
    agendas = {}
    for _, row in df.iterrows():
        agendas[row['의안명']] = [row['의안번호'], row['의안URL']]

    agendas_df = pd.DataFrame.from_dict(agendas, orient='index', columns=['agenda_id', 'agenda_url'])
    agendas_df.reset_index(inplace=True)
    agendas_df.rename(columns={'index' : 'agenda_name'}, inplace=True)

    return agendas_df

def __main__():
    df = get_data()
    members_df = get_members_df(df)
    print(members_df)
    members_df.to_csv('../data/members.csv')

    agendas_df = get_agendas_df(df)
    print(agendas_df)
    agendas_df.to_csv('../data/agendas.csv')

if __name__ == '__main__':
    __main__()