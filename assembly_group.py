import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html, Input, Output, State
import dash_daq as daq
import webbrowser
import os

if __name__ == '__main__':
    app = dash.Dash(__name__)

    df = pd.read_csv('./data/final_data.csv')

    color_discrete_map = {
        '더불어민주당': '#000dff',
        '국민의힘': '#E61E2B',
        '정의당': '#ffed00',
        '진보당': '#d6001C',
        '개혁신당': '#ff4d00',
        '조국혁신당': '#06275e',
        '사회민주당': '#f58400',
        '기본소득당': '#03fceb',
        '무소속': 'grey',
    }

    # Dash Layout Setting
    app.layout = html.Div([
        html.H1("제22대 국회 본회의 안건 투표에 따른 국회의원 유사도", style={'textAlign': 'center'}),
        html.Label("국회의원 이름 검색:", style={'margin': '10px 0'}),
        dcc.Input(
            id='search-input',
            type='text',
            placeholder='이름을 입력하세요',
            debounce=True,
            style={
                'width' : '100%',
                'maxWidth': '600px',
                'padding': '10px',
                'margin-bottom' : '20px',
                'boxSizing':'border-box',
            }
        ),
        dcc.Graph(id='scatter-plot',
                  style={
                      'width': '100%',
                      'height': '100%',
                      'maxWidth': '600px',
                      'margin': '0 auto',
                  }),
        daq.BooleanSwitch(
            id='toggle-text',
            on=True,
            label='이름 보이기',
            labelPosition='top',
            style={'margin': '20px 0', 'textAlign': 'center'},
        ),
        dcc.Location(id='url', refresh=True),  # 리디렉션을 위한 Location 컴포넌트
        html.Div(id='link', style={'margin-top': '20px'})  # 동적 링크 표시
    ])

    # Plotly 그래프 업데이트 콜백
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
            title="제22대 국회 본회의 안건 투표에 따른 국회의원 유사도"
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
            autosize=True,
            margin=dict(l=10, r=10, t=30, b=10),
            height=400,
            hoverlabel=dict(
                font_size=12,
                bgcolor='white',
            ),
            xaxis_title="X축",
            yaxis_title="Y축",
            legend_title="정당",
            hovermode='closest'
        )
        return fig

    # Viewport 메타 태그 추가
    app.index_string = '''
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Mobile Optimized Scatter Plot</title>
            {%metas%}
            {%css%}
        </head>
        <body>
            <div id="dash-app">
                {%app_entry%}
            </div>
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
    '''

    """
    @app.callback(
        Output('link', 'children'),
        [Input('scatter-plot', 'clickData')]
    )
    def display_link(clickData):
        if clickData:
            # 클릭한 포인트의 텍스트 (국회의원 이름)
            lawmaker_name = clickData['points'][0]['text']
            # URL 생성
            url = f"https://assembly101.kr/{lawmaker_name}"
            # HTML 링크 반환
            return html.A(f"Go to {lawmaker_name}'s page", href=url, target='_blank')
        return "Click on a point to view details."
    """

    port = int(os.environ.get('PORT', 10000))
    app.run_server(host='0.0.0.0', port=port, debug=True)
