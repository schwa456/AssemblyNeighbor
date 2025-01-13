class AssemblyMember:
    def __init__(self, name, party):
        self.name = name
        self.party = party
        self.vote = []

class Agenda:
    def __init__(self, name, id, url):
        self.name = name
        self.id = id
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

