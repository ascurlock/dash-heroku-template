import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

#import numpy as np
#import pandas as pd
import plotly.graph_objects as go
#import plotly.express as px 
#import plotly.graph_objects as go
#import plotly.figure_factory as ff

#import dash
from jupyter_dash import JupyterDash
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
#fig4.show()
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

app = JupyterDash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        html.H1("Exploring Gender Inequality Measured By The 2019 General Social Survey"),
        
        dcc.Markdown(children = markdown_text),
        
        html.H2("Comparing The Average Income, Job Prestige Score, Socioeconomic Status, and Years of Education by Sex"),
        
        dcc.Graph(figure=fig2),
        
        html.H2("Level of Agreement With The Statement:"),
        html.H2('"It is much better for everyone involved if the man is the achiever outside the home and the woman takes care of the home and family."'),
        
        dcc.Graph(figure=fig3),
        
        html.H2("Income vs. Job Prestige by Sex"),
        
        dcc.Graph(figure=fig4),
        
        html.Div([
            
            html.H3("Distribution of Income by Sex"),
            
            dcc.Graph(figure=fig5_1)
            
        ], style = {'width':'48%', 'float':'left'}),
        
        html.Div([
            
            html.H3("Distribution of Job Prestige by Sex"),
            
            dcc.Graph(figure=fig5_2)
            
        ], style = {'width':'48%', 'float':'right'}),
        
        html.H2("Income of Males and Females at Varying Levels of Job Prestige"),
        
        dcc.Graph(figure=fig6)
    
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
