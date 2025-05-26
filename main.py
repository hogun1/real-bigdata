import streamlit as st
st.title('나의 첫 Streamlit 앱')
st.write('안녕하세요!')
# 필요한 패키지를 자동으로 설치하도록 설정 (실행 환경에 pip가 있을 때만 동작)
import subprocess
import sys

def install_packages():
    """
    streamlit, pandas, plotly가 설치되어 있지 않으면 설치합니다.
    """
    packages = ["streamlit", "pandas", "plotly"]
    for pkg in packages:
        try:
            __import__(pkg)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

# 자동 설치 호출
install_packages()

# streamlit, pandas, plotly 임포트
import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="따릉이 대여 시각화",
    layout="wide"
)

# 제목
st.title("서울시 따릉이 대여 데이터 시각화")
st.markdown("구글 드라이브에서 데이터를 불러와 Plotly로 인터랙티브 차트를 그립니다.")

# 데이터 로드
@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    # 날짜 컬럼이 있다면 datetime으로 변환
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
    return df

DATA_URL = "https://drive.google.com/uc?export=download&id=1pwfON6doXyH5p7AOBJPfiofYlni0HVVY"

data = load_data(DATA_URL)

# 사이드바: 날짜 필터 (데이터에 date 컬럼이 있을 때)
if 'date' in data.columns:
    min_date = data['date'].min()
    max_date = data['date'].max()
    selected_range = st.sidebar.date_input(
        "기간 선택", [min_date, max_date], min_value=min_date, max_value=max_date
    )
    # 필터 적용
    if len(selected_range) == 2:
        start, end = selected_range
        mask = (data['date'] >= pd.to_datetime(start)) & (data['date'] <= pd.to_datetime(end))
        filtered = data.loc[mask]
    else:
        filtered = data.copy()
else:
    filtered = data.copy()

# 메인 차트: 가이드 예시
st.header("렌탈 건수 추이")
if 'date' in filtered.columns and 'count' in filtered.columns:
    fig = px.line(
        filtered,
        x='date',
        y='count',
        title='날짜별 대여 건수',
        labels={'date': '날짜', 'count': '대여 건수'}
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.warning("'date' 또는 'count' 컬럼이 데이터에 없습니다.")

# 추가 예: 지역별 대여 건수
st.header("지역별 대여 건수 분포")
if 'region' in filtered.columns and 'count' in filtered.columns:
    fig2 = px.bar(
        filtered.groupby('region', as_index=False)['count'].sum(),
        x='region',
        y='count',
        title='지역별 총 대여 건수',
        labels={'region': '지역', 'count': '총 대여 건수'}
    )
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("'region' 또는 'count' 컬럼이 데이터에 없습니다.")

# 실행 안내
st.markdown("---")
st.markdown(
    "### 로컬 실행 방법\n"
    "```bash\n"
    "git clone https://github.com/<your-username>/<your-repo>.git\n"
    "cd <your-repo>\n"
    "pip install streamlit pandas plotly\n"
    "streamlit run main.py\n"
    "```"
    "\n"
    "### Streamlit Cloud 배포 방법\n"
    "1. GitHub에 코드를 푸시합니다 (main.py 및 requirements.txt 생성).\n"
    "2. [Streamlit Cloud](https://share.streamlit.io/)에 로그인합니다.\n"
    "3. 앱 새로 만들기(New app) > GitHub 리포지토리 선택 > 브랜치(main) > 경로(main.py) 설정 후 배포합니다.\n"
    "4. 배포된 URL로 접속하면 대시보드가 자동으로 실행됩니다.\n"
)
