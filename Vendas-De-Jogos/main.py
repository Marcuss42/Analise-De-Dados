import streamlit as st
import pandas as pd
import plotly.express as px

DATASET_NAME = "vgsales.csv"
min_year = None
max_year = None


def transform_data(df):
    global min_year, max_year

    df['Year'] = df['Year'].apply(lambda x: int(x) if str(x).count('.') else 0)
    df = df[df['Year'] > 0]
    min_year = df['Year'].min()
    max_year = df['Year'].max()

    return df

def sales_by_platform_bar_chart(df, region, title):
    df_platform = df[df[region].notna()].groupby([region,'Platform'])\
        .size()\
        .reset_index(name='count')\
        .sort_values(by='count', ascending=False)\
        .reset_index(drop=True)\
        .groupby('Platform')[region].sum().reset_index()

    df_platform = df_platform[df_platform[region] > 0]
    df_platform = df_platform.sort_values(by=region, ascending=False)

    fig = px.bar(
        data_frame=df_platform,
        x='Platform',
        y=region,
        color='Platform',
        labels={region: 'Total', 'Platform': 'Plataforma'},
    )

    fig.update_layout(
        title=dict(text=title, x=0.5, xanchor="center"),
        annotations=[
            dict(
                text="Plataformas com vendas acima de 0",
                x=0, y=1.05,
                xref="paper", yref="paper",
                showarrow=False,
                font=dict(size=12, color="gray")
            )
        ]
    )

    fig.update_yaxes(ticksuffix="M")

    return fig

def sales_by_platform_pie_chart(df, region, title):
    df_platform = df[df[region].notna()].groupby([region,'Platform'])\
        .size()\
        .reset_index(name='count')\
        .sort_values(by='count', ascending=False)\
        .reset_index(drop=True)\
        .groupby('Platform')[region].sum().reset_index()

    df_platform['percentual'] = df_platform[region] / df_platform[region].sum() * 100
    df_outros = df_platform[df_platform['percentual'] < 1]
    soma_outros = df_outros[region].sum()

    df_platform = df_platform[df_platform['percentual'] >= 1]
    df_platform.loc[len(df_platform)] = ['OTHERS', soma_outros, soma_outros / df_platform[region].sum()]

    fig = px.pie(
        data_frame=df_platform,
        values=region,
        names='Platform',
        title=title,
        labels={region: 'Total'}
    )

    fig.update_layout(
        margin=dict(t=50, b=50, l=50, r=50),
        title=dict(text=title, x=0.5, xanchor="center"),
        annotations=[
            dict(
                text="OTHERS: Plataformas com vendas abaixo de 1%",
                x=0, y=-.1,
                xref="paper", yref="paper",
                showarrow=False,
                font=dict(size=12, color="gray")
            )
        ]
    )

    return fig

def game_sales_by_platform_bar_chart(df, platform, region, title, ascending=False, length=10):
    if platform == 'All':
        df_games = df[df[region] > 0]
    else:
        df_games = df[(df[region] > 0) & (df['Platform'] == platform)]

    df_games = df_games.groupby(['Name', 'Platform'])[region].sum().reset_index().sort_values(by=region, ascending=ascending).head(length)

    fig = px.bar(
        data_frame=df_games,
        y='Name',
        x=region,
        color='Name',
        labels={region: 'Total', 'Name': ''},
        hover_data=['Platform'] if platform == 'All' else None,
    )
    fig.update_traces(hovertemplate="Total=%{x}<br>Platform=%{customdata[0]}<extra></extra>")

    fig.update_layout(
        title=dict(text=title, x=0.5, xanchor="center"),
        showlegend=False
    )

    fig.update_xaxes(ticksuffix="M")
    return fig

def genre_sales_by_platform_bar_chart(df, platform, region, title, ascending=False, length=10):
    if platform == 'All':
        df_genres = df[df[region] > 0]
    else:
        df_genres = df[(df[region] > 0) & (df['Platform'] == platform)]

    df_genres = df_genres.groupby(['Genre', 'Platform'])[region].sum().reset_index().sort_values(by=region, ascending=ascending).head(length)
    if platform == 'All':
        df_genres = df_genres.groupby('Genre')[region].sum().reset_index().sort_values(by=region, ascending=ascending).head(length)

    fig = px.bar(
        data_frame=df_genres,
        y='Genre',
        x=region,
        color='Genre',
        labels={region: 'Total', 'Genre': ''},
    )

    fig.update_traces(hovertemplate="Total=%{x}<extra></extra>")

    fig.update_layout(
        title=dict(text=title, x=0.5, xanchor="center"),
        showlegend=False
    )

    fig.update_xaxes(ticksuffix="M")

    return fig

def na_tab(df, sales_by_platform_pie_title, sales_by_platform_bar_title, game_sales_by_platform_bar_title, genre_sales_by_platform_bar_title, selectbox_label):
    col1, col2 = st.columns([3, 3])
    
    with col1:
        fig_sales_by_platform = sales_by_platform_pie_chart(df, 'NA_Sales', sales_by_platform_pie_title)
        st.plotly_chart(fig_sales_by_platform)

        platform = st.selectbox(selectbox_label, options=['All'] + df['Platform'].unique().tolist(), key='na_select1')
        st.plotly_chart(game_sales_by_platform_bar_chart(df, platform, 'NA_Sales', game_sales_by_platform_bar_title))

    with col2:
        fig_sales_by_platform_bar = sales_by_platform_bar_chart(df, 'NA_Sales', sales_by_platform_bar_title)
        st.plotly_chart(fig_sales_by_platform_bar)

        platform = st.selectbox(selectbox_label, options=['All'] + df['Platform'].unique().tolist(), key='na_select2')
        st.plotly_chart(genre_sales_by_platform_bar_chart(df, platform, 'NA_Sales', genre_sales_by_platform_bar_title))

def eu_tab(df, sales_by_platform_pie_title, sales_by_platform_bar_title, game_sales_by_platform_bar_title, genre_sales_by_platform_bar_title, selectbox_label):
    col1, col2 = st.columns([3, 3])
    with col1:
        fig_sales_by_platform = sales_by_platform_pie_chart(df, 'EU_Sales', sales_by_platform_pie_title)
        st.plotly_chart(fig_sales_by_platform)

        platform = st.selectbox(selectbox_label, options=['All'] + df['Platform'].unique().tolist(), key='eu_select1')
        st.plotly_chart(game_sales_by_platform_bar_chart(df, platform, 'EU_Sales', game_sales_by_platform_bar_title))

    with col2:
        fig_sales_by_platform_bar = sales_by_platform_bar_chart(df, 'EU_Sales', sales_by_platform_bar_title)
        st.plotly_chart(fig_sales_by_platform_bar)

        platform = st.selectbox(selectbox_label, options=['All'] + df['Platform'].unique().tolist(), key='eu_select2')
        st.plotly_chart(genre_sales_by_platform_bar_chart(df, platform, 'EU_Sales', genre_sales_by_platform_bar_title))

def jp_tab(df, sales_by_platform_pie_title, sales_by_platform_bar_title, game_sales_by_platform_bar_title, genre_sales_by_platform_bar_title, selectbox_label):
    col1, col2 = st.columns([3, 3])
    with col1:
        fig_sales_by_platform = sales_by_platform_pie_chart(df, 'JP_Sales', sales_by_platform_pie_title)
        st.plotly_chart(fig_sales_by_platform)

        platform = st.selectbox(selectbox_label, options=['All'] + df['Platform'].unique().tolist(), key='jp_select1')
        st.plotly_chart(game_sales_by_platform_bar_chart(df, platform, 'JP_Sales', game_sales_by_platform_bar_title))

    with col2:
        fig_sales_by_platform_bar = sales_by_platform_bar_chart(df, 'JP_Sales', sales_by_platform_bar_title)
        st.plotly_chart(fig_sales_by_platform_bar)

        platform = st.selectbox(selectbox_label, options=['All'] + df['Platform'].unique().tolist(), key='jp_select2')
        st.plotly_chart(genre_sales_by_platform_bar_chart(df, platform, 'JP_Sales', genre_sales_by_platform_bar_title))

def other_tab(df, sales_by_platform_pie_title, sales_by_platform_bar_title, game_sales_by_platform_bar_title, genre_sales_by_platform_bar_title, selectbox_label):
    col1, col2 = st.columns([3, 3])
    with col1:
        fig_sales_by_platform = sales_by_platform_pie_chart(df, 'Other_Sales', sales_by_platform_pie_title)
        st.plotly_chart(fig_sales_by_platform)

        platform = st.selectbox(selectbox_label, options=['All'] + df['Platform'].unique().tolist(), key='other_select1')
        st.plotly_chart(game_sales_by_platform_bar_chart(df, platform, 'Other_Sales', game_sales_by_platform_bar_title))

    with col2:
        fig_sales_by_platform_bar = sales_by_platform_bar_chart(df, 'Other_Sales', sales_by_platform_bar_title)
        st.plotly_chart(fig_sales_by_platform_bar)

        platform = st.selectbox(selectbox_label, options=['All'] + df['Platform'].unique().tolist(), key='other_select2')
        st.plotly_chart(genre_sales_by_platform_bar_chart(df, platform, 'Other_Sales', genre_sales_by_platform_bar_title))

def global_tab(df, sales_by_platform_pie_title, sales_by_platform_bar_title, game_sales_by_platform_bar_title, genre_sales_by_platform_bar_title, selectbox_label):
    col1, col2 = st.columns([3, 3])
    with col1:
        fig_sales_by_platform = sales_by_platform_pie_chart(df, 'Global_Sales', sales_by_platform_pie_title)
        st.plotly_chart(fig_sales_by_platform)

        platform = st.selectbox(selectbox_label, options=['All'] + df['Platform'].unique().tolist(), key='global_select1')
        st.plotly_chart(game_sales_by_platform_bar_chart(df, platform, 'Global_Sales', game_sales_by_platform_bar_title))

    with col2:
        fig_sales_by_platform_bar = sales_by_platform_bar_chart(df, 'Global_Sales', sales_by_platform_bar_title)
        st.plotly_chart(fig_sales_by_platform_bar)

        platform = st.selectbox(selectbox_label, options=['All'] + df['Platform'].unique().tolist(), key='global_select2')
        st.plotly_chart(genre_sales_by_platform_bar_chart(df, platform, 'Global_Sales', genre_sales_by_platform_bar_title))


def main():
    st.set_page_config(layout="wide")

    st.warning("Alguns jogos foram removidos pois não possuem ano de lançamento definido.", icon="⚠️")
    st.title("Venda de Jogos")

    df = transform_data(pd.read_csv(DATASET_NAME))

    intervalo = st.sidebar.slider(
        "Selecione o intervalo de anos",
        min_value=(min_year := df['Year'].min()),
        max_value=(max_year := df['Year'].max()),
        value=(min_year, max_year),
        step=1
    )

    df_filtrado = df[(df['Year'] >= intervalo[0]) & (df['Year'] <= intervalo[1])]

    tab_titles = ["North America", "Europe", "Japan", "Other", "Global"]
    tab_funcs = [na_tab, eu_tab, jp_tab, other_tab, global_tab]
    tabs = st.tabs(tab_titles)

    sales_by_platform_pie_title = 'Percentual de vendas'
    sales_by_platform_bar_title = 'Vendas em Milhões'
    game_sales_by_platform_bar_title = 'Jogos mais vendidos'
    genre_sales_by_platform_bar_title = 'Gêneros mais vendidos'
    selectbox_label = 'Selecione a Plataforma'

    for i in range(len(tabs)):
        with tabs[i]: 
            st.subheader(f"Vendas por Plataforma - {tab_titles[i]}")
            tab_funcs[i](
                df_filtrado, sales_by_platform_pie_title=sales_by_platform_pie_title, sales_by_platform_bar_title=sales_by_platform_bar_title, 
                game_sales_by_platform_bar_title=game_sales_by_platform_bar_title, genre_sales_by_platform_bar_title=genre_sales_by_platform_bar_title,
                selectbox_label=selectbox_label
        )

    st.text("Novas análises em breve...")

if __name__ == "__main__":
    main()
