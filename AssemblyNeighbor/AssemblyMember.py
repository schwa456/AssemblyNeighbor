class AssemblyMember:
    def __init__(self, name, party):
        self.name = name
        self.party = party
        self.vote = []

    def vote_to_agenda(self, agenda, vote):
        self.vote.append(vote)
        if vote == '찬성':
            agenda.agree_members.append(self)
        elif vote == '반대':
            agenda.disagree_members.append(self)
        elif vote == '기권':
            agenda.giveup_members.append(self)

class Agenda:
    def __init__(self, name, number, url):
        self.name = name
        self.number = number
        self.url = url
        self.agree_members = []
        self.disagree_members = []
        self.giveup_members = []

    def get_agree_members(self):
        return self.agree_members

    def get_disagree_members(self):
        return self.disagree_members

    def get_giveup_members(self):
        return self.giveup_members

class Party:
    def __init__(self, name):
        self.name = name
        self.members = []

    def add_member(self, member):
        self.members.append(member)

