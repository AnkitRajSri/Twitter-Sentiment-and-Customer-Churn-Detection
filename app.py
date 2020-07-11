import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html

import flask
import pandas as pd
import time
import os

import plotly.graph_objects as go
import plotly.express as px
server = flask.Flask('app')
server.secret_key = os.environ.get('secret_key', 'secret')


wd = os.getcwd()


overall_platform_data = pd.read_csv(os.path.join(wd, 'overall_platforms_data.csv'))
netflix_df = pd.read_csv(os.path.join(wd, 'netflix_df.csv'))
primevideo_df = pd.read_csv(os.path.join(wd, 'primevideo_df.csv'))
hulu_df = pd.read_csv(os.path.join(wd, 'hulu_df.csv'))
disneyplus_df = pd.read_csv(os.path.join(wd, 'disneyplus_df.csv'))
tweets_per_day_df = pd.read_csv(os.path.join(wd, 'tweets_per_day.csv'))
overall_performance_data = pd.read_csv(os.path.join(wd, 'overall_performance_data.csv'))
churn_likeliness_data = pd.read_csv(os.path.join(wd, 'churn_likeliness_data.csv'))



colors = {
    'background': 'rgba(0,0,0,0)',
    'text': '#7FDBFF'
}
marker_colors = ('#00A8E1', '#E50914', '#66AA33', '#113CCF')

overall_platform_data['positive_tweet_count'] = ''
overall_platform_data['positive_tweet_percentage'] = ''
overall_platform_data['negative_tweet_count'] = ''
overall_platform_data['negative_tweet_percentage'] = ''

# Iterated over a for loop to calculate the positive and negative tweet counts and percentages
for platform in (primevideo_df, netflix_df, hulu_df, disneyplus_df):
    platform_name = platform.loc[0, 'streaming_platform']
    
    negative_tweet_count = len(platform.loc[platform['sentiment'] == 'Negative'])
    negative_tweet_percentage = negative_tweet_count/overall_platform_data.loc[overall_platform_data['streaming_platform'] == platform_name, 'tweet_count']

    overall_platform_data.loc[overall_platform_data['streaming_platform'] == platform_name, 'negative_tweet_count'] = negative_tweet_count
    overall_platform_data.loc[overall_platform_data['streaming_platform'] == platform_name, 'negative_tweet_percentage'] = negative_tweet_percentage
    
    positive_tweet_count = len(platform.loc[platform['sentiment'] == 'Positive'])
    positive_tweet_percentage = positive_tweet_count/overall_platform_data.loc[overall_platform_data['streaming_platform'] == platform_name, 'tweet_count']
    
    overall_platform_data.loc[overall_platform_data['streaming_platform'] == platform_name, 'positive_tweet_count'] = positive_tweet_count
    overall_platform_data.loc[overall_platform_data['streaming_platform'] == platform_name, 'positive_tweet_percentage'] = positive_tweet_percentage



app = dash.Dash('app', server=server, external_stylesheets=[dbc.themes.CYBORG, os.path.join(wd, 'style.css')])

app.scripts.config.serve_locally = False
dcc._js_dist[0]['external_url'] = 'https://cdn.plot.ly/plotly-basic-latest.min.js'

app.layout = html.Div([
    html.H1("ANALYSIS OF TWITTER DATA", style={'textAlign': 'center', 'color': colors['text']}),
    html.Div(
        className='row',
        children=[ 
            dcc.Markdown("This dashboard shows the change in sentiment of web streaming services over time and the features that help us identify the churners which help us predict the likelihood of churn. We choose to focus on the top 4 web streaming services (Amazon Prime Video, Hulu, Disney Plus, & Netflix). This is particularly due to current Covid-19 times causing increasing usage and engagement of these services."),
        ],style={}
    ),
    html.Br(),
    html.Div(
        [dcc.Graph(
        id='graph1',
        figure=go.Figure(
            data = [
            go.Bar(
                name = 'Tweets',
                 x = overall_platform_data['streaming_platform'],
                 y = overall_platform_data['tweet_count'],
                 marker_color = marker_colors),
            go.Bar(name = 'Retweets',
                x = overall_platform_data['streaming_platform'],
                y = overall_platform_data['retweet_count'],
                marker_color = marker_colors)],
            layout= {
            'title': 'Tweets vs. ReTweets per Platform',
            'xaxis_title' : 'Web Streaming Platforms', 
            'yaxis_title' : 'Tweet Count', 
            'showlegend': False,
            'plot_bgcolor': colors['background'],
            'paper_bgcolor': colors['background'],
            'font': {
                    'color': colors['text']
                }
            }
            )
        ),
        dcc.Graph(
            id='graph4',
            figure=go.Figure(
                data = [go.Bar(
                    name = 'Positive', 
                    x = overall_platform_data['streaming_platform'], 
                    y = overall_platform_data['positive_tweet_percentage'],
                    marker_color = marker_colors),
                go.Bar(
                    name = 'Negative', 
                    x = overall_platform_data['streaming_platform'], 
                    y = overall_platform_data['negative_tweet_percentage'],
                    marker_color = marker_colors)],
            layout= {
                'barmode' : 'group', 
                'xaxis_title' : 'Web Streaming Platforms', 
                'yaxis_title' : 'Percentage', 
                'title': 'Positive vs. Negetive Tweets',
                'showlegend': False,
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }           
            }
            )
        )],
        style={'columnCount': 2}
    ),
    html.Div(
        className='row',
        children=[ 
            dcc.Markdown("We can see that Netflix is the leading platform in terms of tweets followed by Hulu and Disney Plus a close second and third with PrimeVideo lagging the group. In terms of sentiment DisneyPlus seems to have the highest percentage of positive and lowest percent of negative tweets, with Prime, Hulu, and Netflix in that order."),
        ],style={}
    ),
    html.Br(),
    dcc.Dropdown(
        id='my-dropdown1',
        options=[
            {'label': 'All', 'value': 'all'},
            {'label': 'Netflix', 'value': 'netflix'},
            {'label': 'Prime Video', 'value': 'primevideo'},
            {'label': 'Hulu', 'value': 'hulu'},
            {'label': 'Disney Plus', 'value': 'disneyplus'}
        ],
        value='all'
        ),
    html.Div(
        [dcc.Graph(
            id='graph2'
        ),    
        dcc.Graph(
            id='graph3'
        )],
        style={'columnCount': 2}
    ), 
    html.Div(
        className='row',
        children=[ 
            dcc.Markdown("Interestingly we see a big spike in Disney for the first week that may be useful further study which brought its overall performance much higher. This means that although Netflix is currently holding the largest presence – this may be threatened by DisneyPlus surge were it to be a repeat threat as it did have the highest tweet count in a day for the period we studied. Thus, time is a critical factor and to properly understand the trend and anomalies and how we deal with them for machine learning purposes will be crucial for our analysis. The streaming companies can see from the tweet count and sentiment polarity distribution over time to observe if any recently added content causes any change in customer sentiment and thus, they can identify what kind of content is well received."),
        ],style={}
    ),
    html.Br(),   

    html.Div(
        [
        html.Div(
        className='row',
        children=[ 
            dcc.Markdown("Select a value to see the churn likeliness rate"),
        ],style={'textAlign': 'center'}
        ),
        dcc.Dropdown(
        id='my-dropdown2',
        options=[
            {'label': 'Netflix', 'value': 'Netflix'},
            {'label': 'Prime Video', 'value': 'PrimeVideo'},
            {'label': 'Hulu', 'value': 'Hulu'},
            {'label': 'Disney Plus', 'value': 'DisneyPlus'}
        ],
        value='Netflix'
        ),
        dcc.Graph(
            id='graph6'

        ),
        dcc.Graph(
            id='graph5',
            figure=go.Figure(
            data = [
                go.Bar(
                    name = 'MorePreferred',
                    x = overall_performance_data['StreamingPlatform'],
                    y = overall_performance_data['MorePreferredPercentage'],
                    marker_color = marker_colors),
                go.Bar(name = 'LessPreferred',
                    x = overall_performance_data['StreamingPlatform'],
                    y = overall_performance_data['LessPreferredPercentage'],
                    marker_color = marker_colors)],
            layout = {
                'barmode' : 'group', 
                'xaxis_title' : 'Web Streaming Platforms', 
                'yaxis_title' : 'Percentage', 
                'title' : 'More Preferred vs Less Preferred % of the Streaming Platforms',
                'showlegend': False,
                'plot_bgcolor': colors['background'],
                'paper_bgcolor': colors['background'],
                'font': {
                    'color': colors['text']
                }            
            }
        )
        )],
        style={'columnCount': 2}
    ),    
    html.Div(
        className='row',
        children=[ 
            dcc.Markdown("The findings can help the streaming companies to get an idea where they stand in the current market compared to the other streaming services according to the customer tweets. For example, it is visible from the more preferred vs less preferred graph that despite having 69 million US subscribers, out of all the tweets mentioned, Netflix is the less preferred service more than 80% of the time."),
        ],style={}
    )], className="container")


@app.callback(Output('graph2', 'figure'),
              [Input('my-dropdown1', 'value')])
def update_graph(selected_dropdown_value):
    if selected_dropdown_value == "all":
        dff = tweets_per_day_df
    else:
        dff = tweets_per_day_df[tweets_per_day_df['platform'] == selected_dropdown_value]
    fig =  px.line(
        dff,
        x = 'date',
        y = 'tweet_count',
        color = 'platform',
        title = 'Tweet Count per day for the Web Streaming Platforms',        
        )
    fig.layout = {
        'title' : 'Tweet Count per day for the Web Streaming Platforms',
        'showlegend': False,
        'plot_bgcolor': colors['background'],
        'paper_bgcolor': colors['background'],
        'font': {
                'color': colors['text']
            }
        }
    return fig


@app.callback(Output('graph3', 'figure'),
              [Input('my-dropdown1', 'value')])
def update_graph(selected_dropdown_value):
    if selected_dropdown_value == "all":
        dff = tweets_per_day_df
    else:
        dff = tweets_per_day_df[tweets_per_day_df['platform'] == selected_dropdown_value]
    fig = px.line(
        dff,
        x = 'date',
        y = 'sentiment_polarity',
        color = 'platform',
        title = 'Average Sentiment per day for the Web Streaming Platforms'
        )
    fig.layout = {
        'title' : 'Average Sentiment per day for the Web Streaming Platforms',
        'showlegend': False,
        'plot_bgcolor': colors['background'],
        'paper_bgcolor': colors['background'],
        'font': {
            'color': colors['text']
        }
    }
    return fig

@app.callback(Output('graph6', 'figure'),
              [Input('my-dropdown2', 'value')])
def update_graph(selected_dropdown_value):
    
    count = 'Count' + selected_dropdown_value
    churn = 'ChurnLikeliness'+ selected_dropdown_value
    fig_pie = px.pie(churn_likeliness_data, values=count, names=churn)
    fig_pie.layout = {
        'title' : 'Likely to Churn Rate',
        #'showlegend': False,
        'plot_bgcolor': colors['background'],
        'paper_bgcolor': colors['background'],
        'font': {
                'color': colors['text']
            }
        }
    return fig_pie

if __name__ == '__main__':
    app.run_server()