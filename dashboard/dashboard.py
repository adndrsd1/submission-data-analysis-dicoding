import streamlit as st
import pandas as pd
import plotly.express as px

st.title("Dashboard Submission Dicoding: Analisis Dataset Bike Sharing")

st.markdown(
    """
    - Nama: Adinda Rizki Sya'bana Diva
    - Email: adindarizki15@gmail.com
    - ID Dicoding: adndrsd
    """
)

all_df = pd.read_csv('all_data_dashboard.csv')
all_df.reset_index(inplace=True)

question_1, question_2, question_3 = st.tabs(["Visualisasi 1", "Visualisasi 2", "Visualisasi 3"])

with question_1:
    st.header("Perbandingan Jumlah Pengguna dalam Musim Tertentu")
    cs  = all_df.groupby(['season']).sum().reset_index()
    fig_bar_season = px.bar(cs, x='season', y=['casual', 'registered'], barmode='group', title='Seasonal Bike Rental Count', 
                        height=400, width=650, color_discrete_sequence=['#4169E1', '#EF553B'], text_auto=True)
    st.plotly_chart(fig_bar_season, use_container_width=True, theme='streamlit')

with question_2:
    st.header("Pengaruh Kondisi Lingkungan terhadap Frekuensi Jumlah Pelanggan")
    ce = all_df.groupby('weathersit').max()[['cnt']].reset_index()
    fig_bar_env = px.bar(ce, x='weathersit', y='cnt', title='Environmental Bike Rental Count', 
                    height=450, width=700, color_discrete_sequence=['#4169E1'], barmode='group', text_auto=True)
    st.plotly_chart(fig_bar_env, use_container_width=True, theme='streamlit')

with question_3:
    st.header("Grafik Jumlah Pengguna dalam Waktu Tertentu")
    page_select = st.selectbox("Pilih waktu : ", ["Daily", "Holiday", "Weekday", "Workingday"])

    cus_time = all_df[['dteday', 'holiday', 'weekday', 'workingday', 'casual', 'registered', 'cnt']]

    if page_select == "Daily":

        cus_time['dteday'] = pd.to_datetime(cus_time['dteday'])

        min_date = cus_time['dteday'].min()
        max_date = cus_time['dteday'].max()

        st.sidebar.header("Pilih Tanggal")
        try:
            with st.sidebar:
                start_date, end_date = st.date_input(
                    label='Rentang Tanggal', min_value=min_date, max_value=max_date,
                    value=(min_date, max_date)
                )
        except:
            st.sidebar.error("Rentang tanggal tidak valid")
            st.stop()

        filtered_df = cus_time[(cus_time['dteday'] >= str (start_date)) & (cus_time['dteday'] <= str (end_date))]
        
        ct = filtered_df[['casual', 'registered', 'cnt']].groupby(filtered_df['dteday']).sum()
        fig_line_daily = px.line(ct, x=ct.index, y=['casual', 'registered'], title='Daily Bike Rental Count', 
                             height=450, width=700, color_discrete_sequence=['#4169E1', '#EF553B'], markers=True)
        st.plotly_chart(fig_line_daily, use_container_width=True, theme='streamlit')

    elif page_select == "Holiday":
        time_holiday = cus_time[['casual', 'registered', 'cnt']].groupby(cus_time['holiday']).sum()
        fig_bar_holiday = px.bar(time_holiday, x=time_holiday.index, y=['casual', 'registered'], title='Holiday Bike Rental Count', 
                            height=450, width=700, barmode='group', color_discrete_sequence=['#4169E1', '#EF553B'], text_auto=True)
        st.plotly_chart(fig_bar_holiday, use_container_width=True, theme='streamlit')

    elif page_select == "Weekday":
        time_weekday = cus_time[['casual', 'registered', 'cnt']].groupby(cus_time['weekday']).sum()
        fig_bar_weekday = px.bar(time_weekday, x=time_weekday.index, y=['casual', 'registered'], title='Weekday Bike Rental Count', 
                            height=450, width=700, barmode='group', color_discrete_sequence=['#4169E1', '#EF553B'], text_auto=True)
        st.plotly_chart(fig_bar_weekday, use_container_width=True, theme='streamlit')

    elif page_select == "Workingday":
        time_workingday = cus_time[['casual', 'registered', 'cnt']].groupby(cus_time['workingday']).sum()
        fig_bar_workingday = px.bar(time_workingday, x=time_workingday.index, y=['casual', 'registered'], title='Workingday Bike Rental Count',
                            height=450, width=700, barmode='group', color_discrete_sequence=['#4169E1', '#EF553B'], text_auto=True)
        st.plotly_chart(fig_bar_workingday, use_container_width=True, theme='streamlit')
