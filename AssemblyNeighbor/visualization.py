import pandas as pd
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import plotly.express as px
from AssemblyMember import *
from data_setup import *
from vote_info import *

def get_pca(df, n_components=2):
    pca = PCA(n_components=n_components)
    pca_result = pca.fit_transform(df)

    pca_df = pd.DataFrame(pca_result, index=df.index, columns=['PC1', 'PC2'])

    return pca_df

def get_tsne(df, n_components=2):
    tsne = TSNE(n_components=n_components, random_state=42)
    tsne_result = tsne.fit_transform(df)

    tsne_df = pd.DataFrame(tsne_result, index=df.index, columns=['Dim1', 'Dim2'])

    return tsne_df

def get_graph(df):
    fig = px.scatter(df, x='PC1', y='PC2', text=df.index)
    fig.update_traces(textposition='top center')
    fig.update_layout(title='PCA of Lawmakers Voting Embeddings',
                      xaxis_title='Principal Component 1',
                      yaxis_title='Principal Component 2')
    fig.show()

def __main__():
    df = get_data()
    vote_info = get_vote_info(df)
    vote_embedding = get_vote_embedding(vote_info)
    pca_df = get_pca(vote_embedding)
    tsne_df = get_tsne(vote_embedding)
    get_graph(pca_df)
    get_graph(tsne_df)


if __name__ == '__main__':
    __main__()