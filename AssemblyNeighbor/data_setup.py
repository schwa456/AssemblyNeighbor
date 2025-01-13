import pandas as pd
from AssemblyMember import *

def get_data():
    file_path = '../data/데이터_국회의원 본회의 표결정보.xlsx'
    df = pd.read_excel(file_path)
    return df

def get_members(df):
    members = []
    for _, row in df.iterrows():
        member = AssemblyMember(row['의원'], row['정당'])
        print(member.name)
        if member not in members:
            members.append(member)
    return members

def get_parties(df):
    parties = []
    for _, row in df.iterrows():
        party = Party(row['정당'])
        print(party.name)
        if party not in parties:
            parties.append(party)
    return parties

def get_agendas(df):
    agendas = []
    for _, row in df.iterrows():
        agenda = Agenda(row['의안명'], row['의안번호'], row['의안URL'])
        print(agenda.name)
        if agenda not in agendas:
            agendas.append(agenda)
    return agendas

def __main__():
    df = get_data()
    members = get_members(df)
    for i in range(len(members)):
        print(members[i].name, members[i].party)
    parties = get_parties(df)
    for i in range(len(parties)):
        print(parties[i].name)
    agendas = get_agendas(df)
    for i in range(len(agendas)):
        print(agendas[i].name)
if __name__ == '__main__':
    __main__()