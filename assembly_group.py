import pandas as pd
from sklearn.manifold import TSNE
from sklearn.decomposition import PCA
import plotly.express as px
import dash
from dash import dcc, html, Input, Output
import dash_daq as daq

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

class Visualizer:
    def __init__(self, embedding, metadata):
        self.embedding = embedding
        self.metadata = metadata

    def plot(self, title='Visualization of Lawmakers Voting Embeddings'):
        df = pd.DataFrame(self.embedding, columns=['Dim1', 'Dim2'])
        df['name'] = self.metadata.index
        df['party'] = self.metadata['정당'].values

        color_discrete_map = {
            '더불어민주당' : '#000dff',
            '국민의힘' : '#E61E2B',
            '정의당' : '#ffed00',
            '진보당': '#d6001C',
            '개혁신당': '#ff4d00',
            '조국혁신당': '#06275e',
            '사회민주당': '#f58400',
            '기본소득당': '#00D2C3',
            '무소속': 'grey',
        }

        fig = px.scatter(df, x='Dim1', y='Dim2', color='party', text='name',
                         title=title, labels={'party': 'Political Party'},
                         color_discrete_map=color_discrete_map)
        fig.update_layout(
            dragmode='zoom',
            hovermode='closest',
            showlegend=True,
            legend_title='Political Party',
            updatemenus=[
                {
                    "buttons": [
                        {"label": "Show Names", "method": "update", "args": [{"text": [df['name']]}]},
                        {"label": "Hide Names", "method": "update", "args": [{"text": [None]}]}
                    ],
                    "direction": "down",
                    "showactive": True
                }
            ]
        )
        fig.show()

if __name__ == '__main__':
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
    color_discrete_map = {
        '더불어민주당': '#000dff',
        '국민의힘': '#E61E2B',
        '정의당': '#ffed00',
        '진보당': '#d6001C',
        '개혁신당': '#ff4d00',
        '조국혁신당': '#06275e',
        '사회민주당': '#f58400',
        '기본소득당': '#008B7E',
        '무소속': 'grey',
    }

    app = dash.Dash(__name__)

    # Dash Layout Setting
    app.layout = html.Div([
        html.H1("Visualization of Lawmakers Voting Embeddings"),
        html.Label("Search for a lawmaker:"),
        dcc.Input(
            id='search-input',
            type='text',
            placeholder='Enter Lawmaker Name',
            debounce=True
        ),
        dcc.Graph(id='scatter-plot'),
        daq.BooleanSwitch(
            id='toggle-text',
            on=True,
            label='Show Text',
            labelPosition='top'
        )
    ])

    @app.callback(
        Output('scatter-plot', 'figure'),
        [Input('toggle-text', 'on'),
         Input('search-input', 'value')]
    )
    def update_scatter(show_text, search_name):
        df['opacity'] = 1.0

        if search_name:  # 검색어가 입력된 경우
            # 입력값 전처리
            search_name = search_name.strip().lower()  # 공백 제거 및 소문자 변환

            # 매칭 디버깅 로그
            print(f"Search Name (processed): {search_name}")

            # 이름과 비교하여 투명도 설정
            def match_name(row_name):
                row_name_processed = row_name.strip().lower()
                is_match = search_name == row_name_processed
                print(f"Matching: {row_name_processed} == {search_name} -> {is_match}")
                return 1.0 if is_match else 0.2

            df['opacity'] = df['name'].apply(match_name)
            for _, row in df.iterrows():
                print(f"name : {row['name']}, opacity : {row['opacity']}")
        fig = px.scatter(
            df,
            x='Dim1',
            y='Dim2',
            text='name' if show_text else None,
            hover_name='name',
            color='party',
            opacity=df['opacity'],
            color_discrete_map=color_discrete_map,
            title="Visualization of Lawmakers Voting Embeddings"
        )

        for i, trace in enumerate(fig.data):
            party_data = df[df['party'] == trace.name]
            fig.data[i].marker.opacity = party_data['opacity'].tolist()

        for trace in fig.data:
            if trace.name in ['국민의힘', '개혁신당']:  # 테두리를 추가할 정당
                trace.marker.line = {
                    'color': 'black',  # 테두리 색상
                    'width': 2  # 테두리 두께
                }

        fig.update_traces(
            mode='markers+text' if show_text else 'markers',
            textposition='top center' if show_text else None,
        )
        fig.update_layout(
            xaxis_title="Dim1",
            yaxis_title="Dim2",
            legend_title="Political Party",
            hovermode='closest'
        )
        return fig

    app.run_server(debug=True)
