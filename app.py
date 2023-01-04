import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(layout = 'wide',page_title = 'Startup Analysis beta by DIVYOM')
df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'],errors = 'coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year
sorted(set(df['inverstors'].str.split(',').sum()))

def overall_analysis():
    st.title('Overall Analysis')
    # total invested amount
    total = round(df['amount'].sum())
    # maximum amount infused in a startup
    max_funding = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
    # average funding by any startup
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    # total funded startup
    num_startup = df['startup'].nunique
    col6 , col7 , col8, col9 = st.columns(4)
    with col6:
        st.metric('Total', str(total) + ' rs')
    with col7:
        st.metric('Maximum funding taken by any startup', str(max_funding) + ' rs')
    with col8:
        st.metric('Average funding taken by any startup', str(round(avg_funding)) + ' rs')
    with col9:
        st.metric('Total number of startups', '2533' )

    st.header('Month on Month')
    selected_option = st.selectbox('Select Type',['Total','Count'])

    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    fig9, ax9 = plt.subplots()
    ax9.plot(temp_df['x_axis'], temp_df['amount'])

    st.pyplot(fig9)

def load_inverstor_details(inverstor):
    st.title(inverstor)
    # load the recent 5 investments of the inverstor
    last5_df = df[df['inverstors'].str.contains(inverstor)].head()[['date','startup','vertical','city','round','amount']]
    st.subheader('Most Recent Inverstments')
    st.dataframe(last5_df)
    col1 , col2 = st.columns(2)
    with col1:
        # biggest investments
        st.subheader('Top 5 biggest Investments')
        big_series = df[df['inverstors'].str.contains(inverstor)].groupby('startup')['amount'].sum().sort_values(ascending=False).head()
        st.dataframe(big_series)
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)

        st.pyplot(fig)
    with col2:
        vertical_series = df[df['inverstors'].str.contains(inverstor)].groupby('startup')['amount'].sum()

        st.subheader('Sectors invested in')
        fig1 , ax1 = plt.subplots()
        ax1.pie(vertical_series,labels = vertical_series.index,autopct = '%0.01f%%')

        st.pyplot(fig1)

    df['year'] = df['date'].dt.year
    year_series = df[df['inverstors'].str.contains(inverstor)].groupby('city')['amount'].sum()
    st.subheader('Year on year investment')
    fig5, ax5 = plt.subplots()
    ax5.plot(year_series.index, year_series.values)

    st.pyplot(fig5)


    col3 , col4 = st.columns(2)
    with col3:
        # equity details
        round_series = df[df['inverstors'].str.contains(inverstor)].groupby('round')['amount'].sum()
        st.subheader('Equity details')
        fig2, ax2 = plt.subplots()
        ax2.pie(round_series, labels=round_series.index, autopct='%0.01f%%')
        st.pyplot(fig2)
    with col4:
        city_series = df[df['inverstors'].str.contains(inverstor)].groupby('city')['amount'].sum()
        st.subheader('City wise investments')
        fig3, ax3 = plt.subplots()
        ax3.pie(city_series, labels=city_series.index, autopct='%0.01f%%')
        st.pyplot(fig3)

st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','Investors'])

if option == 'Overall Analysis':
        overall_analysis()

else:
    selected_inverstor = st.sidebar.selectbox('Investors',sorted(df['inverstors'].unique().tolist()))
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_inverstor_details(selected_inverstor)


    st.title('Investor Analysis')



