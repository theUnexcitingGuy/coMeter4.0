#!/usr/bin/env python
# coding: utf-8

# # LEARNING DASH

# # Adding css style to the whole code

# In[ ]:


from dash.dependencies import Input, Output, State
from pytrends.request import TrendReq
import dash_table
import pandas as pd
from pytrends.request import TrendReq
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
import bs4
import requests
import wikipedia
from udemy import *
import json
import dash_bootstrap_components as dbc
import dash_table_experiments as dt

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# In[ ]:


#creating the button for plotting single trend data
app.layout = html.Div(children=[
#first row 
    html.Div([
        html.H1("coMeter 4.0")
    ], className = "row"),
        
    html.Div([
        html.Div([
            html.Div(children='''
                Plot trends:
            '''),
            dcc.Input(id='input0', value='', type='text', placeholder = 'input text here'),
            html.Button(id = "submit_button0", n_clicks = 0, children = "Submit")
        ], className = "six columns"),
        html.Div([
             html.Div(children='''
                Compare trends:
            '''),
            dcc.Input(id='input', value='', type='text', placeholder = 'input text here'),
            dcc.Input(id='input1', value='', type='text', placeholder = 'compare with...'),
            html.Button(id = "submit_button", n_clicks = 0, children = "Submit")
        ], className = "six columns")
    ], className = "row"),
    
#second row with graphs
    
    html.Div([
        html.Div([
            html.Div(id='output-graph0')
        ], className = "six columns"),
        html.Div([
            html.Div(id='output-graph')
        ], className = "six columns")
    ], className = "row"),
    
#third row with regional data graph
    html.Div([
        html.Br(),
         html.Div(children='''
            Get regional data:
        '''),
        dcc.Input(id='input2', value='', type='text', placeholder = 'input text here'),
        html.Button(id = "submit_button1", n_clicks = 0, children = "Submit")
    ], className = "row"),
    
    html.Div([
        html.Div(id='output-graph1')
    ], className = "row"),
    
    
#fourth row
    html.Div([
        html.H2('Discovering concepts')
    ], className = "row"),
    
    html.Div([
        html.Div([
            html.Div(children='''
                Type below the major topic for which you want to extract the related concepts:
            '''),
            dcc.Input(id='inputX', value='', type='text', placeholder = 'input text here'),
            html.Button(id = "submit_buttonX", n_clicks = 0, children = "Submit"),

            html.Div(children='''
                Which of the following topics best fits your research query?:
            '''),
        ], className = "six columns"),
        
        html.Div([
            html.Div(children='''
                Type here the suggestion you chose to extract the related topics:
            '''),
            dcc.Input(id='inputY', value='', type='text', placeholder = 'input text here'),
            html.Button(id = "submit_buttonY", n_clicks = 0, children = "Submit"),
        ], className = "six columns")
    ], className = "row"),
    
    html.Div([
        html.Div([
            html.Div(id='output-tableX')  
        ], className = "six columns"),
        html.Div([
            html.Div(id='output-tableY')
        ], className = "six columns")
    ], className = "row"),
    
    
    
#fifth row
    html.Div([
        html.Div([
            html.H2('Connect skills to job profiles!'),
            html.Div(children='''
                Which skill do you want to link to profiles?
            '''),
            dcc.Input(id='input3', value='', type='text', placeholder = 'input skill here'),
            html.Button(id = "submit_button3", n_clicks = 0, children = "Submit"),
        ], className = "six columns"),
        html.Div([
            html.H2('Connect skills to MOOCs!'),
            html.Div(children='''
                Type below the skill you want to learn:
            '''),
            dcc.Input(id='inputW', value='', type='text', placeholder = 'input skill here'),
            html.Button(id = "submit_buttonW", n_clicks = 0, children = "Submit")
        ], className = "six columns")
    ], className = "row"),

#sisth row
    html.Div([
        html.Div([
            html.Div(id='output-table')
        ], className = "six columns"),
        html.Div([
            html.Div(id='output-tableW')
        ], className = "six columns")
    ], className = "row")
    
])   

#callback for plotting single trends
@app.callback(
    Output(component_id='output-graph0', component_property='children'),
    [Input(component_id='submit_button0', component_property='n_clicks')],
    [State('input0', 'value')]
    )

def graph(n_clicks, input_data):  #n_clicks means that once i click on the submit button, then the function starts
    pytrend = TrendReq()
    pytrend.build_payload(kw_list=[input_data], timeframe='all',  geo='US')
    # Interest Over Time
    interest_over_time_df = pytrend.interest_over_time()
    interest_over_time_df.index.name = 'date'
    Data = interest_over_time_df.reset_index()
    Data['date'] = Data['date'].astype(str)
    Data['year'] = Data['date'].str.split('-').str[0]
    Data['year'] = Data['year'].astype(int)
    Data_sum = Data.groupby('year').sum()
    Data_sum.index.name = 'year'
    Data_final = Data_sum.reset_index()
    return dcc.Graph(
        id = 'test0',
        figure = {
            'data' : [
                {'x' : Data_final['year'], 'y': Data_final[input_data],'type' : 'line', 'name': input_data}
            ],
            'layout' : {
                'title' : input_data
            }
        }
    )


#callback for comparing trends
@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='submit_button', component_property='n_clicks')],
    [State('input1', 'value'),State(component_id='input', component_property='value')]
    )

def graph(n_clicks, input_data, input_data1):  
    pytrend = TrendReq()
    pytrend.build_payload(kw_list=[input_data, input_data1], timeframe='all',  geo='US')
    # Interest Over Time
    interest_over_time_df = pytrend.interest_over_time()
    interest_over_time_df.index.name = 'date'
    Data = interest_over_time_df.reset_index()
    Data['date'] = Data['date'].astype(str)
    Data['year'] = Data['date'].str.split('-').str[0]
    Data['year'] = Data['year'].astype(int)
    Data_sum = Data.groupby('year').sum()
    Data_sum.index.name = 'year'
    Data_final = Data_sum.reset_index()
    return dcc.Graph(
        id = 'test', #ho messo l'id uguale a quello sopra
        figure = {
            'data' : [
                {'x' : Data_final['year'], 'y': Data_final[input_data] ,'type' : 'line', 'name': input_data},
                {'x' : Data_final['year'], 'y': Data_final[input_data1] ,'type' : 'line', 'name': input_data1}
            ],
            'layout' : {
                'title' : input_data1 +' ' + input_data
            }
        }
    )

#callback for region data
@app.callback(
    Output(component_id='output-graph1', component_property='children'),
    [Input(component_id='submit_button1', component_property='n_clicks')],
    [State('input2', 'value')]
    )

def region_single_query(n_clicks, query):
    pytrend = TrendReq()
    pytrend.build_payload(kw_list=[query], geo = 'US', timeframe = "now 1-H")
    Region_data = pytrend.interest_by_region(resolution='COUNTRY', inc_low_vol=True, inc_geo_code=False)
    Region_data.index.name = 'geoName'
    Reg_data = Region_data.reset_index()
    return dcc.Graph(
        id = 'region', #ho messo l'id uguale a quello sopra
        figure = {
            'data' : [
                {'x' : Reg_data['geoName'], 'y': Reg_data[query] ,'type' : 'bar', 'name': query}
            ],
            'layout' : {
                'title' : query
            }
        }
    )

#callback for extracting job profiles from skills
@app.callback(
    Output(component_id='output-table', component_property='children'),
    [Input(component_id='submit_button3', component_property='n_clicks')],
    [State('input3', 'value')]
    )

def skills_to_profiles(n_clicks, skill):
    new_list = []
    lista = []
    ref_skill = []
    base_url = "https://www.monster.com/jobs/search/?q="
    url = base_url + skill
    page = requests.get(url).text
    soup = bs4.BeautifulSoup(page, "lxml")
    card_header = soup.find_all('header', class_ = "card-header")
    for card in card_header:
        try:
            a = card.find('a')
            #print(a.text)
            lista.append(a.text)
        except:
            print("error")

    for el in lista:
        stringa = el.replace("\r\n", "")
        new_list.append(stringa)
        ref_skill.append(skill)

    job_extraction = pd.DataFrame({'skill' : ref_skill, 'job' : new_list})
    
    #data cleansing
    job_extraction['job'] = job_extraction['job'].str.split('-').str[0] #remove of the part that is on the right of "-"
    job_extraction['job'] = job_extraction['job'].str.split('(').str[0] #remove everything that is in the () parenthesis
    job_extraction['job'] = job_extraction['job'].str.split('0').str[0] #remove numerical characters
    job_extraction['job'] = job_extraction['job'].str.split('1').str[0]
    job_extraction['job'] = job_extraction['job'].str.split('2').str[0]
    job_extraction['job'] = job_extraction['job'].str.split('3').str[0]
    job_extraction['job'] = job_extraction['job'].str.split('4').str[0]
    job_extraction['job'] = job_extraction['job'].str.split('5').str[0]
    job_extraction['job'] = job_extraction['job'].str.split('6').str[0]
    job_extraction['job'] = job_extraction['job'].str.split('7').str[0]
    job_extraction['job'] = job_extraction['job'].str.split('8').str[0]
    job_extraction['job'] = job_extraction['job'].str.split('9').str[0]
    job_extraction['job'] = job_extraction['job'].str.split('–').str[0]
    job_extraction['job'] = job_extraction['job'].str.split(',').str[0]
    job_extraction.drop_duplicates(subset ="job", keep = 'first', inplace = True) 
    filter1 = job_extraction[~job_extraction.job.str.contains("Sr")]
    filter2 = filter1[~filter1.job.str.contains("Senior")]
    
    return dash_table.DataTable(
                    id = 'Table',
                    columns = [{"name" : i, "id": i} for i in filter2.columns],
                    data = filter2.to_dict("rows"),
                    fixed_rows={ 'headers': True, 'data': 0 },
                    style_cell={'width': '150px',  'maxHeight': '200px'},
                    editable=True,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    row_selectable="multi",
                    row_deletable=True,
                    page_action="native",
                    )

#callback for extracting suggestions 
@app.callback(
    Output(component_id='output-tableX', component_property='children'),
    [Input(component_id='submit_buttonX', component_property='n_clicks')],
    [State('inputX', 'value')]
    )
def extract_suggestions(n_clicks, input_topic):
    suggestions = wikipedia.search(input_topic, results=10, suggestion=False)
    sugg_table = pd.DataFrame(suggestions) 
    sugg_table.rename(columns={0 : 'possible topics'}, inplace=True)
    return dash_table.DataTable(
                    id = 'Table',
                    columns = [{"name" : i, "id": i} for i in sugg_table.columns],
                    data = sugg_table.to_dict("rows"),
                    )

#callback for extracting related topics 
@app.callback(
    Output(component_id='output-tableY', component_property='children'),
    [Input(component_id='submit_buttonY', component_property='n_clicks')],
    [State('inputY', 'value')]
    )

def extract_related_topics(n_clicks, input_sugg):
    topic_column = []
    suggestion_element = []
    topics = wikipedia.WikipediaPage(title=input_sugg).links
    for el in topics:
        topic_column.append(el)
        suggestion_element.append(input_sugg)
    data_topics = pd.DataFrame({'topic' : suggestion_element, 'related topics': topic_column})
    return dash_table.DataTable(
                    id = 'Table1',
                    columns = [{"name" : i, "id": i} for i in data_topics.columns],
                    data = data_topics.to_dict("rows"),
                    fixed_rows={ 'headers': True, 'data': 0 },
                    style_cell={'width': '150px', 'maxHeight': '200px'},
                    editable=True,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    row_selectable="multi",
                    row_deletable=True,
                    page_action="native",
                    )

#callback for the buttons to display MOOC table
@app.callback(
    Output(component_id='output-tableW', component_property='children'),
    [Input(component_id='submit_buttonW', component_property='n_clicks')],
    [State('inputW', 'value')]
    )

def MOOC_matching(n_clicks, stringa_input):
    Client = PyUdemy(clientID = 'Jp0HqVHUQeUmaJEfN56bTfkhEtIn0X1gmV3nrjBa', clientSecret = '84h4xRdAu86vEfyk4u1m8sDTtHNAxn3kZ76U39hPCX9XstpmlPFZBVHgIkkLc1JJc6QLyLAZIuVLLz3vqZgG7Lsm0R4LJZPFeqllHMiEt1bcufGElJFozipQv2wwcT3G')
    skill_list = stringa_input.split(",")
    title_course = []
    difficulty_of_course = []
    stringa = ["beginner", "intermediate", "expert"]
    ref_skill = []

    for index2, skill in enumerate(skill_list):
        for level in stringa:
            for i in range(1,3):
                try:
                    object_det_courses = Client.get_courseslist(search = skill, language = "en", page=i, instructional_level = level)
                    d = json.loads(object_det_courses)
                    for index, ris in enumerate(d['results']):
                        title_course.append(ris['title'])
                        difficulty_of_course.append(level)
                        ref_skill.append(skill)
                except:
                    print("404 error")

    courses = pd.DataFrame({'course title' : title_course, 'difficulty' : difficulty_of_course, 'Skill' : ref_skill})
    
    #creating a table in which there is the number of skills out of the total given in input that the course teaches
    dummies = pd.get_dummies(courses['course title']) #tabella one hot encoding
    dummies['skill'] = courses['Skill']
    
    frequency = pd.value_counts(courses['course title'])
    freq_table = pd.DataFrame(frequency)
    freq_table.columns = ['n']
    freq_table.index.name = 'courses'   #con questo codice sto trasformando row_names in una colonna della tabella
    freq_table.reset_index(inplace=True)
    #adding to the frequency table a column in which we show which skills are taught out of the total given in input
    colonna_skill = []
    for titolo in freq_table['courses']:
        skilldelcorso = []
        for ind, corso in enumerate(dummies[titolo]):
            if corso == 1:
                skilldelcorso.append(dummies['skill'][ind])

        colonna_skill.append(skilldelcorso)

    colonna_skill2 = []
    for titolo in freq_table['courses']:
        stringa = ""
        for ind, corso in enumerate(dummies[titolo]):
            if corso == 1:
                stringa+=(dummies['skill'][ind])
                stringa+=";"

        colonna_skill2.append(stringa)

    freq_table['skills'] = colonna_skill2

    #adding a new column in which we show the missing skills which are not taught in the course
    colonna_skill_mancanti = []
    for skill in freq_table['skills']:
        listatemporana = skill.split(";")
        differenza = set(skill_list) - set(listatemporana)
        s = ';'
        skill_mancanti = s.join(differenza)
        colonna_skill_mancanti.append(skill_mancanti)

    freq_table['missing skills'] = colonna_skill_mancanti
    freq_table.rename(columns={'courses': 'course title'}, inplace=True)

    #now i want to add the column of the difficulty of that course so that the output is complete
    difficulty_column = courses[['course title','difficulty']]
    MOOCs = pd.merge(freq_table, difficulty_column, on='course title', how='left')
    return dash_table.DataTable(
                    id = 'MOOC',
                    columns = [{"name" : i, "id": i} for i in MOOCs.columns],
                    data = MOOCs.to_dict("rows"),
                    fixed_rows={ 'headers': True, 'data': 0 },
                    style_cell={'width': '150px', 'maxHeight': '200px'},
                    editable=True,
                    filter_action="native",
                    sort_action="native",
                    sort_mode="multi",
                    row_selectable="multi",
                    row_deletable=True,
                    page_action="native",
                    )


# In[ ]:


if __name__ == '__main__':
    app.run_server()

