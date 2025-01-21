import pandas as pd
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA

class VotingData:
    def __init__(self, file_path):
        self.data_df = pd.read_excel(file_path)
        self.vote_data = self.data_df[['의안번호', '의원', '정당', '표결결과']]
        self.vote_mapping = {
            '찬성' : 1,
            '반대' : -1,
            '기권' : 0,
            None : -2
        }
        self.process_data()

    def process_data(self):
        self.vote_data.loc[:, '표결결과'] = self.vote_data['표결결과'].map(self.vote_mapping).fillna(-2)
        self.pivot_table = self.vote_data.pivot_table(index='의안번호', columns='의원', values='표결결과', fill_value=-2)
        self.party_info = self.vote_data[['의원', '정당']].drop_duplicates().set_index('의원')

    def get_pivot_table(self):
        return self.pivot_table

    def get_party_info(self):
        return self.party_info

class DimensionReducer:
    def __init__(self, method='tsne', n_components=2, random_state=42, learning_rate=100, perplexity=20):
        self.method = method
        self.n_components = n_components
        self.random_state = random_state
        self.learning_rate = learning_rate
        self.perplexity = perplexity

    def fit_transform(self, data):
        if self.method == 'tsne':
            reducer = TSNE(n_components=self.n_components, random_state=self.random_state, learning_rate=self.learning_rate, perplexity=self.perplexity)
        elif self.method == 'pca':
            reducer = PCA(n_components=self.n_components, random_state=self.random_state)
        else:
            raise ValueError
        return reducer.fit_transform(data)

def __main__():
    file_path = 'data/데이터_국회의원 본회의 표결정보.xlsx'
    voting_data = VotingData(file_path)

    # Dimension Reduction
    reducer = DimensionReducer()
    pivot_table = voting_data.get_pivot_table().T
    embedding = reducer.fit_transform(pivot_table)

    # Data Preparation
    party_info = voting_data.get_party_info()
    df = pd.DataFrame(embedding, columns=['Dim1', 'Dim2'])
    df['name'] = party_info.index
    df['party'] = party_info['정당'].values

    df.to_csv('./data/final_data.csv')

if __name__ == '__main__':
    __main__()