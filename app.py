import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

#import numpy as np
#import pandas as pd
#import plotly.graph_objects as go
#import plotly.express as px 
#import plotly.graph_objects as go
#import plotly.figure_factory as ff

#import dash
#from jupyter_dash import JupyterDash
#import dash_core_components as dcc
#import dash_html_components as html
#from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#
#%%capture
gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

#
mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')

#
markdown_text = "The general social survery or GSS has been gathering data on varying aspects of American society since 1972 and in considered the best source for sociological and attitudinal trend data in the United States according to the GSS's offical website. The GSS contains questions covering demographic, behavioral, attitudinal, and some special interest topics. The results that will be focused on involve gender equality and the pay gap. According to website payscale gap in pay between men an women varies by profession however, there is still a notable difference between the median income of men compared to the median income of women."
about_the_response_variables1 = """
satjob: responses to "On the whole, how satisfied are you with the work you do?"\n
relationship: agree or disagree with: "A working mother can establish just as warm and secure a relationship with her children as a mother who does not work."\n
male_breadwinner: agree or disagree with: "It is much better for everyone involved if the man is the achiever outside the home and the woman takes care of the home and family."
"""

about_the_response_variables2 = """
men_bettersuited: agree or disagree with: "Most men are better suited emotionally for politics than are most women."\n
child_suffer: agree or disagree with: "A preschool child is likely to suffer if his or her mother works."\n
men_overwork: agree or disagree with: "Family life often suffers because men concentrate too much on their work."
"""

about_the_group_variables = """
sex: male or female\n
education: years of formal education\n
region: region of the country where the respondent lives
"""

source = "https://www.payscale.com/data/gender-pay-gap"
source2 = "http://www.gss.norc.org/About-The-GSS"

#
plot1_df = gss_clean[['sex','income','job_prestige','socioeconomic_index','education']].groupby('sex').mean()
plot1_df = round(plot1_df, 2)
plot1_df = plot1_df.reset_index().rename({'sex':'Sex','income':'Income','job_prestige':'Job Prestige Rating','socioeconomic_index':'Socioeconomic Index','education':'Years of Education'}, axis=1)

fig2 = ff.create_table(plot1_df)
#fig2.show()
#
gss_clean['male_breadwinner'] = gss_clean['male_breadwinner'].astype('category')
gss_clean['male_breadwinner'] = gss_clean['male_breadwinner'].cat.reorder_categories(['strongly disagree', 
                                                            'disagree', 
                                                            'agree', 
                                                            'strongly agree'])
                                                            #.cat.reorder_categories(['strongly agree', 
                                                            #'agree', 
                                                            #'disagree', 
                                                            #'strongly disagree'])

bread_bars = gss_clean[['sex','male_breadwinner']].groupby(['sex','male_breadwinner']).size()
bread_bars = bread_bars.reset_index()
bread_bars = bread_bars.rename({0:'count'}, axis=1)
bread_bars
fig3 = px.bar(bread_bars, x='male_breadwinner', y='count', color='sex',
            labels={'count':'Number of People', 'male_breadwinner':'Level of Agreement'},
            color_discrete_map = {'male':'blue', 'female':'red'},
            barmode = 'group')
fig3.update_layout(showlegend=True)
fig3.update(layout=dict(title=dict(x=0.5)))
#fig3.show()

#
gss_scatter = gss_clean[['sex','job_prestige','income','education','socioeconomic_index']]


fig4 = px.scatter(gss_scatter, x='job_prestige', y='income', 
                 color = 'sex',
                 trendline='ols',
                 labels={'job_prestige':'Job Prestige Rating', 
                        'income':'Income'},
                 color_discrete_map = {'male':'blue', 'female':'red'},
                 hover_data=['education', 'socioeconomic_index'])
fig4 = fig4.update_layout(title='Income Vs. Job Prestige by Sex')
#
fig5_1 = px.box(gss_clean, x='sex', y = 'income', color = 'sex',
                   labels={'income':'Income', 'sex':''})
fig5_1.update_layout(showlegend=False)
#fig5_1.show()

fig5_2 = px.box(gss_clean, x='sex', y = 'job_prestige', color = 'sex',
                   labels={'job_prestige':'Job Prestige Rating', 'sex':''})
fig5_2.update_layout(showlegend=False)
#fig5_2.show()

#
gss_clean['job_prestige_cat'] = pd.cut(gss_clean.job_prestige, bins=[15,26,37,48,59,70,81],
       labels=['16-26','27-37','38-48','49-59','60-70','71-81'])

gss_clean['job_prestige_cat'] = gss_clean['job_prestige_cat'].astype('category')
gss_clean['job_prestige_cat'] = gss_clean['job_prestige_cat'].cat.reorder_categories(['16-26','27-37','38-48','49-59','60-70','71-81'])

df6 = gss_clean[['income','sex','job_prestige_cat']].dropna().sort_values(by='job_prestige_cat')

fig6 = px.box(df6, x='sex', y='income', facet_col='job_prestige_cat', color = 'sex',
                 facet_col_wrap=2,
                 color_discrete_map = {'male':'blue', 'female':'red'},
                 labels={'income':'Income','sex':''},
                 height=800)
fig6 = fig6.update_layout(showlegend=False)
fig6 = fig6.for_each_annotation(lambda a: a.update(text=a.text.replace("job_prestige_cat=", "Job Prestige ")))
#fig6.show()

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.layout = dbc.Container(
    [
        dcc.Store(id="store"),
        html.H1("Exploring Gender Inequality Measured By The 2019 General Social Survey"),
        dcc.Markdown(children = markdown_text),
        html.Hr(),
        dbc.Button(
            "Regenerate graphs",
            color="primary",
            block=True,
            id="button",
            className="mb-3",
        ),
        dbc.Tabs(
            [
                dbc.Tab(label="Barplots", tab_id="bar"),
                dbc.Tab(label="Scatterplot", tab_id="scatter"),
                dbc.Tab(label="Boxplots", tab_id="box")
            ],
            id="tabs",
            active_tab="bar",
        ),
        html.Div(id="tab-content", className="p-4"),
    ]
)


@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"), Input("store", "data")],
)
def render_tab_content(active_tab, data):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_tab and data is not None:
        if active_tab == "bar":
            return dbc.Row(
                [
                    html.Div(
                [
                    html.H2("Level of Agreement to Various Statements by Sex, Region, or Education"),

                    html.Div([

                        html.H3("Response To:"),

                        dcc.Dropdown(id='categories',
                                     options=[{'label': i, 'value': i} for i in cat_columns]),

                        html.H3("Group By:"),

                        dcc.Dropdown(id='groupby',
                                     options=[{'label': j, 'value': j} for j in grp_columns]),

                     ], style={'width': '25%', 'float': 'left'}),

                    html.Div([

                        dcc.Graph(id="graph")

                    ], style={'width': '70%', 'float': 'right'}),
                    html.Div([
            
                    html.H3("Response Variables"),
            
                    dcc.Markdown(children = about_the_response_variables1)
            
                    ],style = {'width':'48%', 'float':'left'}),
        
                html.Div([
                    
                    html.H3(". "),
            
                    dcc.Markdown(children = about_the_response_variables2)
            
                    ],style = {'width':'48%', 'float':'right'}),
                
                html.Div([
                    
                    #html.H3("Group By Variables"),
            
                    dcc.Markdown(children = about_the_group_variables)
            
                    ],style = {'width':'48%', 'float':'right'})
                ]
            )
                ])

        elif active_tab == "scatter":
            return dbc.Row(
                [
                html.Div([
            
                    html.H3("Income Vs. Job Prestige by Sex"),
            
                    dcc.Graph(figure=fig4)
            
                    ], style = {'width':'48%', 'float':'left'})
                ]
            )
        
        elif active_tab == "box":
            return dbc.Row(
                [
                html.Div([
            
                    html.H3("Income by Sex"),
            
                    dcc.Graph(figure=fig5_1)
            
                    ], style = {'width':'48%', 'float':'left'}),
        
                html.Div([
            
                    html.H3("Job Prestige by Sex"),
            
                    dcc.Graph(figure=fig5_2)
            
                    ], style = {'width':'48%', 'float':'right'}),
                    
                html.H2("Income of Males and Females at Varying Levels of Job Prestige"),
        
                dcc.Graph(figure=fig6)
                ]
            )
    return "No tab selected"


@app.callback(Output("store", "data"), [Input("button", "n_clicks")])
def generate_graphs(n):
    """
    This callback generates three simple graphs from random data.
    """
    if not n:
        # generate empty graphs when app loads
        return {k: go.Figure(data=[]) for k in ["bars", "scatter", "box"]}

    # simulate expensive graph generation process
    time.sleep(2)

    # generate 100 multivariate normal samples
    data = np.random.multivariate_normal([0, 0], [[1, 0.5], [0.5, 1]], 100)

    scatter = go.Figure(
        data=[go.Scatter(x=data[:, 0], y=data[:, 1], mode="markers")]
    )
    hist_1 = go.Figure(data=[go.Histogram(x=data[:, 0])])
    hist_2 = go.Figure(data=[go.Histogram(x=data[:, 1])])

    # save figures in a dictionary for sending to the dcc.Store
    return {"scatter": scatter, "hist_1": hist_1, "hist_2": hist_2}


if __name__ == '__main__':
    app.run_server(debug=True)
