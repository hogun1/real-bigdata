import streamlit as st
st.title('나의 첫 Streamlit 앱')
st.write('안녕하세요!')
import streamlit as st
import pandas as pd
import plotly.express as px

# 반드시 Streamlit의 첫 번째 명령어로 실행되어야 합니다.
st.set_page_config(
    page_title="따릉이 대여 시각화",
    layout="wide"
)

# 제목
st.title("서울시 따릉이 대여 데이터 시각화")
st.markdown("구글 드라이브에서 데이터를 불러와 Plotly로 인터랙티브 차트를 그립니다.")

# 데이터 로드 함수 (캐시 사용)
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    return df

DATA_URL = "https://drive.google.com/uc?export=download&id=1pwfON6doXyH5p7AOBJPfiofYlni0HVVY"

data = load_data(DATA_URL)

# 사이드바: 날짜 필터
if 'date' in data.columns:
    start_date, end_date = st.sidebar.date_input(
        "기간 선택", [data['date'].min(), data['date'].max()]
    )
    if start_date and end_date:
        mask = (data['date'] >= pd.to_datetime(start_date)) & (data['date'] <= pd.to_datetime(end_date))
        data = data.loc[mask]

# 렌탈 건수 추이
st.header("렌탈 건수 추이")
if 'date' in data.columns and 'count' in data.columns:
    fig = px.line(
        data, x='date', y='count',
        title='날짜별 대여 건수',
        labels={'date': '날짜', 'count': '대여 건수'}
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("'date' 또는 'count' 컬럼이 없습니다.")

# 지역별 대여 건수 분포
st.header("지역별 대여 건수 분포")
if 'region' in data.columns and 'count' in data.columns:
    region_df = data.groupby('region', as_index=False)['count'].sum()
    fig2 = px.bar(
        region_df, x='region', y='count',
        title='지역별 총 대여 건수',
        labels={'region': '지역', 'count': '총 대여 건수'}
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("'region' 또는 'count' 컬럼이 없습니다.")

# 실행 안내
st.markdown("---")
st.markdown(
    "로컬에서 실행하려면:\n"
    "```
"
    "pip install streamlit pandas plotly\n"
    "streamlit run main.py\n"
    "```")
