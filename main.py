
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash_table import DataTable, FormatTemplate
import plotly.express as px
import pandas as pd
import numpy as np
import dash_bootstrap_components as dbc
import datetime

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP],suppress_callback_exceptions = True)

app.title = 'Keating Research - Denver Early Vote Tracker'
summary_2017 = pd.read_csv('counts_2017.csv')
summary_2019 = pd.read_csv('counts_2019.csv')
summary_2021 = pd.read_csv('counts_2021.csv')
df = summary_2021.append([summary_2019,summary_2017])
df.voted_date = pd.to_datetime(df.voted_date)
df = df.replace(np.nan, '', regex=True)
df['days_out'] = df['days_out'].str.extract('(\d+)').astype(int,errors='ignore')
df['voted'] = np.where(df['voted_date'].isnull(), 0, 1)
df['days_out_num'] = df['days_out'].astype(np.float)


min_days_out = df[(df['Year'] == 2021)]

df['comp'] = np.where(df['days_out_num'] == min_days_out['days_out_num'].min(),1,
             np.where(df['days_out_num'] > min_days_out['days_out_num'].min(),0,
             np.where(df['days_out_num'] == 0,3,2)))

df['Party_gender'] = np.where((df['party_code'] == 1) & (df['gender_code'] == 1),"Dem Women",
                     np.where((df['party_code'] == 1) & (df['gender_code'] == 2),"Dem Men",
                     np.where((df['party_code'] == 2) & (df['gender_code'] == 1),"Una Women",
                     np.where((df['party_code'] == 2) & (df['gender_code'] == 2),"Una Men",
                     np.where((df['party_code'] == 3) & (df['gender_code'] == 1),"Rep Women",
                     np.where((df['party_code'] == 3) & (df['gender_code'] == 2),"Rep Men",
                     np.where((df['party_code'] == 4) | (df['gender_code'] == 3),"Other","Other")))))))

df['Party_age'] = np.where((df['party_code'] == 1) & (df['Age2'] == 1),"Dem 18-49",
                     np.where((df['party_code'] == 1) & (df['Age2'] == 2),"Dem 50+",
                     np.where((df['party_code'] == 2) & (df['Age2'] == 1),"Una 18-49",
                     np.where((df['party_code'] == 2) & (df['Age2'] == 2),"Una 50+",
                     np.where((df['party_code'] == 3) & (df['Age2'] == 1),"Rep 18-49",
                     np.where((df['party_code'] == 3) & (df['Age2'] == 2),"Rep 50+",
                     np.where((df['party_code'] == 4) | (df['Age2'] == 3),"Other","Other")))))))

df['gendergrouptext'] = np.where(df['gender_code'] == 1,'Male',
                      np.where(df['gender_code'] == 2,"Female","Unknown"))

df['agegroup_text'] = np.where(df['Age4'] == 1,'18-34',
                      np.where(df['Age4'] == 2,"35-49",
                      np.where(df['Age4'] == 3,"50-64",
                      np.where(df['Age4'] == 4,"65+",0))))

df['partygroup_text'] = np.where(df['party_code'] == 1,'Dem',
                      np.where(df['party_code'] == 2,"Una",
                      np.where(df['party_code'] == 3,"Rep",
                      np.where(df['party_code'] == 4,"Oth",0))))

df['Citywide'] = "All regions"

SBD_unique = df.SBD.unique()
SBD_unique.sort()
CC_unique = df.Council.unique()
CC_unique.sort()
NH_unique = df.Neighborhood.unique()
NH_unique.sort()
all_voters = ["All regions"]

df.rename(columns={
 'party_code':'Party',
    }, inplace = True)

all_options = {
    'Citywide': all_voters,
    'SBD': tuple(SBD_unique),
    'Council': tuple(CC_unique),
    "Neighborhood": tuple(NH_unique)
}

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": "60px",
    "left": 0,
    "bottom": 0,
    "width": '22.5%',
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa"}

color_map = {"Dem": "#2b83ba",
                     "Una": "#008656",
                     "Rep": "#d9534f",
                     "Oth": "#CA7C1B",

                     "18-34": "#80c3ab",
                     "35-49": "#4daa89",
                     "50-64": "#008656",
                     "65+": "#006b45",

                     "Male": "#008656",
                     "Female": "#4E2A83",
                     "Unknown":"#EB9A76",
                     "Dem Women": "#226995",
                     "Dem Men": "#6ba8cf",
                     "Una Women": "#006b45",
                     "Una Men": "#66b69a",
                     "Rep Women": "#c34b47",
                     "Rep Men": "#e48784",
                     "Other": "#daa35f",

                     "Dem 18-49": "#0570b0",
                     "Dem 50+": "#74a9cf",
                     "Una 18-49": "#006d2c",
                     "Una 50+": "#66c2a4",
                     "Rep 18-49": "#ef6548",
                     "Rep 50+": "#b30000",

                     }


SORT = [
        "Dem",
        "Una",
        "Rep",
        "Oth",
        "18-34",
        "35-49",
        "50-64",
        "65+",
        "Male",
        "Female",
        "Unknown",
        "Dem Women",
        "Dem Men",
        "Una Women",
        "Una Men",
        "Rep Women",
        "Rep Men",
        "Other",
        "Dem 18-49",
        "Dem 50+",
        "Una 18-49",
        "Una 50+",
        "Rep 18-49",
        "Rep 50+",
        "Other"]
CONTENT_STYLE = {
    "margin-left": "auto",
    "margin-right": "10px",
    "margin-top": "45px",
    "padding": "2rem 1rem",
    "width": '77.5%',
}

CHART_STYLE = {
    'padding-right': '10px',
    "width": '100%'
}

SPLIT_CHART_STYLE = {
    'padding-right': '10px',
    "width": '35%'
}
navbar = dbc.NavbarSimple(
    brand="Keating Research - Denver Early Vote Tracker - Testing",
    brand_href="#",
    fluid=True,
    color="#4E2A85",
    dark=True,
    className="navbar-fixed-top",
    fixed='top'
)


sidebar = html.Div([
        html.H5("Compare this year's ballot returns to:"),
        html.Br(style={"line-height": "50%"}),
        dcc.Dropdown(id='comp_drop',clearable=False,
                         options=[
                             {'label': ' This point in previous cycles', 'value': 1},
                             {'label': ' Final turnout in previous cycles', 'value': 3}],
                         value=3,
                           ),
        html.Br(style={"line-height": "200%"}),
        html.H5("Use the filters below to drill down to specific geographies:"),
        html.Br(style={"line-height": "50%"}),
        dcc.Dropdown(id='geo_type',
                     options=[{'label': k, 'value': k} for k in all_options.keys()],
                     value='Citywide', clearable=False,
                     placeholder="Select age group"),
        html.Br(style={"line-height": "50%"}),
        dcc.Dropdown(id='geo_filter', value='All voters', clearable=False),
        html.Br(style={"line-height": "200%"}),
        html.H5("Select a group to split demographic charts:"),
        html.Br(style={"line-height": "50%"}),
        dcc.Dropdown(id='demo_drop', value='partygroup_text', clearable=False,
                 options=[
                     {'label': 'Party', 'value': 'partygroup_text'},
                     {'label': 'Age', 'value': 'agegroup_text'},
                     {'label': 'Gender', 'value': "gendergrouptext"},
                     {'label': 'Party X Gender', 'value': "Party_gender"},
                     {'label': 'Party X Age', 'value': "Party_age"},
                     {'label': 'School board district', 'value': "SBD"}
                 ], placeholder="Select age group"),
    html.Br(style={"line-height": "150%"}),

    # dbc.ListGroup(
    #         [
    #             dbc.ListGroupItem(
    #                 [
    #                     html.Div(
    #                         [
    #                             html.H5(id="total_turnout_count", className="mb-1"),
    #                         ],
    #                         className="d-flex w-100 justify-content-between",
    #                     ),
    #                     html.P("Total Ballots returned"),
    #                 ]
    #             ),
    #             dbc.ListGroupItem(
    #                 [
    #                     html.Div(
    #                         [
    #                             html.H5(id="turnout_rate", className="mb-1"),
    #                         ],
    #                         className="d-flex w-100 justify-content-between",
    #                     ),
    #                     html.P("Turnout rate"),
    #                 ]
    #             ),
    #             dbc.ListGroupItem(
    #                 [
    #                     html.Div(
    #                         [
    #                             html.H5(id="net_change", className="mb-1"),
    #                         ],
    #                         className="d-flex w-100 justify-content-between",
    #                     ),
    #                     html.P("Total Increase in Ballots Returned Since Yesterday"),
    #                 ]
    #             ),
    #             dbc.ListGroupItem(
    #                 [
    #                     html.Div(
    #                         [
    #                             html.H3(id="perc_change", className="mb-1"),
    #                         ],
    #                         className="d-flex w-100 justify-content-between",
    #                     ),
    #                     html.P("Perent Increase of Ballots Since Last Update"),
    #                 ]
    #             ),
    #         ]
    #     )
    ],
    style=SIDEBAR_STYLE
)
summary = html.Div([
    dbc.Row([
        dbc.Col(children=[
            html.H4("Overall Turnout", className="subtitle padded",
                    style={"text-indent": "5px", "background-color": "#e6f2f6", "display": "block",
                           'padding': '12px', "margin-left": "3%", "margin-right": "5%",
                           "border-radius": "4px", "border-left": "20px solid #007FA3", "color": "#CA7C1B"}),
            dcc.Graph(id="overall_turnout", style=CHART_STYLE),])]),
    dbc.Row([
        dbc.Col(children=[
            html.H4("Turnout Among Selected Demographic Groups", className="subtitle padded",
                    style={"text-indent": "5px", "background-color": "#e6f2f6", "display": "block",
                           'padding': '12px', "margin-left": "3%", "margin-right": "5%",
                           "border-radius": "4px", "border-left": "20px solid #007FA3", "color": "#CA7C1B"}),
            html.H5("Distribution of Ballots Returned by Group", className="subtitle padded",
                    style={"text-indent": "8px", "display": "block",
                           'padding': '12px', "margin-left": "5%", "margin-right": "5%"}),
            dcc.Graph(id="party_distribution", style=CHART_STYLE)]), ]),
    html.Br(style={"line-height": "150%"}),
    html.Hr(),
    html.Br(style={"line-height": "150%"}),    dbc.Row([
        dbc.Col(children=[
            html.H5("Rate of Ballots Returned within Group", className="subtitle padded",
                    style={"text-indent": "8px", "display": "block",
                           'padding': '12px', "margin-left": "5%", "margin-right": "5%"}),
            dcc.Graph(id="party_turnout_rates", style=CHART_STYLE)])]),
    html.Br(style={"line-height": "150%"}),
    html.Hr(),
    html.Br(style={"line-height": "150%"}),
    dbc.Row([
        dbc.Col(children=[
            html.H5("Running Total of Returns within Group by Day", className="subtitle padded",
                    style={"text-indent": "8px", "display": "block",
                           'padding': '12px', "margin-left": "5%", "margin-right": "5%"}),
            dcc.Graph(id="cumulative_turnout",style=CHART_STYLE)])]),
    html.Br(style={"line-height": "150%"}),
    html.Hr(),
    html.Br(style={"line-height": "150%"}),
    dbc.Row([
        dbc.Col(children=[
            html.H5("Daily Total of Returns within Group by Day", className="subtitle padded",
                    style={"text-indent": "8px", "display": "block",
                           'padding': '12px', "margin-left": "5%", "margin-right": "5%"}),
            dcc.Graph(id="daily_returns", style=CHART_STYLE)])]),
    html.Br(style={"line-height": "150%"}),
    html.Hr(),
    html.Br(style={"line-height": "150%"}),
    dbc.Row([
        dbc.Col(children=[
            html.H5("Distribution of Returns within Group by Day", className="subtitle padded",
                    style={"text-indent": "8px", "display": "block",
                           'padding': '12px', "margin-left": "5%", "margin-right": "5%"}),
            dcc.Graph(id="party_voted_share", style=CHART_STYLE)])])
], style=CONTENT_STYLE)



gender = html.Div([], style=CONTENT_STYLE)

tables = html.Div([], style=CONTENT_STYLE)


app.layout = html.Div([
                summary,
                navbar,
                html.Div(id='page-content'),
                sidebar
])


@app.callback(
    Output('geo_filter', 'options'),
    Input('geo_type', 'value'))
def set_cities_options(selected_type):
    return [{'label': i, 'value': i} for i in all_options[selected_type]]


@app.callback(
    Output('geo_filter', 'value'),
    Input('geo_filter', 'options'))
def set_cities_value(available_options):
    return available_options[0]['value']


@app.callback(
    Output('display-selected-values', 'children'),
    Input('geo_type', 'value'),
    Input('geo_filter', 'value'))
def set_display_children(selected_type, selected_filter):
    return selected_type, selected_filter


@app.callback(
    [Output("overall_turnout", "figure"),
     Output("cumulative_turnout", "figure"),
     Output("daily_returns", "figure"),
     Output("party_distribution", "figure"),
     Output("party_turnout_rates", "figure"),
     Output("party_voted_share", "figure")],
    [Input("comp_drop", "value"),
     Input("demo_drop", "value"),
     Input("geo_type", "value"),
     Input("geo_filter", "value")])
def update_graph(selected_comp, selected_demo, selected_type, selected_filter):
    if ((selected_comp > 0) |  (selected_demo != 0) |(len(selected_type) > 0) |(selected_filter != 0)):
        if selected_comp == 0:
            selected_comp = selected_comp
        if selected_demo == 0:
            selected_demo = selected_demo
        if len(selected_type) == 0:
            selected_type = selected_type
        if selected_filter == 0:
            selected_filter = selected_filter

        filtered_df = df[(df[selected_type] == selected_filter)]
        base_reg = filtered_df
        filtered_df = filtered_df[(filtered_df["comp"] <= selected_comp)]
        filtered_df = filtered_df.sort_values(by=['Year','days_out_num'])

        cumul_df = filtered_df[filtered_df["voted"] == 1]
        cumul_df = cumul_df.groupby(['Year', 'days_out_num'])['VOTER_ID'].sum()
        cumul_df = pd.DataFrame(cumul_df)
        cumul_df = cumul_df.sort_values(by=['Year', 'days_out_num'], ascending=False).reset_index()
        cumul_df['running_total_year'] = cumul_df.groupby(['Year'])['VOTER_ID'].cumsum()

        display_df = filtered_df.groupby(['voted_date','days_out','Year',selected_demo])['VOTER_ID'].sum()
        display_df = pd.DataFrame(display_df)
        display_df = display_df.reset_index()
        display_df['days_out'] = display_df['days_out'].astype(int)
        display_df = display_df.sort_values(by=['days_out','Year',selected_demo])
        display_df['cumal'] = display_df.groupby('Year')['VOTER_ID'].cumsum()
        # display_df = display_df.sort_values(by=['Year', 'days_out', selected_demo]).reset_index()

        #Overall Turnout

        overall_turnout = px.line(cumul_df,x="days_out_num", y="running_total_year",color='Year',
                                  custom_data=['Year', 'days_out_num', 'running_total_year','VOTER_ID'],
                                  color_discrete_map={
                                                      2017: "#80bfd1",
                                                      2019: "#ecac90",
                                                      2021: "#4E2A83"})
        overall_turnout.update_traces(
            hovertemplate="<br>".join([
                "Election Year: %{customdata[0]}",
                "Days Until Election Day: %{customdata[1]}",
                "Total Ballots Returned: %{customdata[2]}",
                "New Ballots Added: %{customdata[3]}",
            ])
        )
        overall_turnout.update_annotations(font_size=16,font_family="Arial")
        overall_turnout.update_layout(plot_bgcolor="#f8fbfc",margin_t= 20, margin_r= 40,margin_b= 20,yaxis_range=[0, (cumul_df['running_total_year'].max()*1.2)],xaxis_range=[14, 0])
        overall_turnout.update_yaxes(title='Total Ballot Returns')
        overall_turnout.update_xaxes(title='Days Until Election Day',showline=True, linewidth=1, linecolor='#7F7F7F')
        overall_turnout.update_traces(line=dict(width=8))

        # Cumulative turnout time series X year
        display_df = filtered_df[filtered_df["voted"] == 1]
        display_df = display_df.groupby(['Year', 'days_out_num', selected_demo])['VOTER_ID'].sum()
        display_df = pd.DataFrame(display_df)
        display_df = display_df.sort_values(by=['Year', 'days_out_num', selected_demo], ascending=False).reset_index()
        display_df['cumal'] = display_df.groupby(['Year', selected_demo])['VOTER_ID'].cumsum()

        display_df = display_df.sort_values(by=['Year','days_out_num'],ascending=False).reset_index() #sort of facets
        display_df = display_df[(display_df[selected_demo] != "Other")]

        cumulative_turnout = px.line(display_df,x="days_out_num", y="cumal",color=selected_demo,
                                     facet_col='Year',color_discrete_map=color_map,
                                     )
        cumulative_turnout.update_layout(yaxis_range=[0, (display_df['cumal'].max()*1.2)])
        cumulative_turnout.update_layout(xaxis_range=[15, 0],plot_bgcolor= "#fcfcfc")
        cumulative_turnout.update_xaxes(linecolor="#77757a")
        cumulative_turnout.update_yaxes(gridcolor = "#f6f5f9",showgrid=True, gridwidth=1)
        cumulative_turnout.update_traces(texttemplate='%{text:.2s}', textposition='top left')
        cumulative_turnout.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        cumulative_turnout.update_traces(line=dict(width=2))
        cumulative_turnout.update_xaxes(showline=True, linewidth=1, linecolor='#7F7F7F',categoryarray= SORT)
        cumulative_turnout.update_layout(hovermode="x")
        cumulative_turnout.update_traces(hovertemplate='%{y:,}')
        cumulative_turnout.update_layout(plot_bgcolor="#f8fbfc",margin_t= 20, margin_r= 40,margin_b= 20,legend_title_text='')
        cumulative_turnout.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        cumulative_turnout.update_annotations(font_size=16,font_family="Arial")
        cumulative_turnout.update_yaxes(title='')
        cumulative_turnout.update_layout(yaxis1=dict(title="Total Ballot Returns"))
        cumulative_turnout.update_xaxes(title='')
        cumulative_turnout.update_layout(xaxis1=dict(title="Days Until Election Day"))

        # daily turnout time series X year


        display_df = filtered_df[filtered_df["voted"] == 1]
        display_df = display_df.groupby(['Year', 'days_out_num', selected_demo])['VOTER_ID'].sum()
        display_df = pd.DataFrame(display_df)
        display_df = display_df.sort_values(by=['Year', 'days_out_num', selected_demo], ascending=False).reset_index()

        display_df = display_df.sort_values(by=['Year','days_out_num'],ascending=False).reset_index() #sort of facets
        display_df = display_df[(display_df[selected_demo] != "Other")]
        daily_returns = px.line(display_df, x="days_out_num", y="VOTER_ID", color=selected_demo,facet_col='Year',color_discrete_map=color_map)

        daily_returns.update_layout(plot_bgcolor="#f8fbfc", margin_t=30,
                                   margin_r=40,
                                   margin_b=10)
        daily_returns.update_layout(yaxis_range=[0, (display_df['VOTER_ID'].max()*1.2)])
        daily_returns.update_layout(xaxis_range=[15, 0],plot_bgcolor= "#fcfcfc")
        daily_returns.update_xaxes(categoryarray= SORT,linecolor="#77757a")
        daily_returns.update_yaxes(title="Daily Returned",gridcolor = "#edeaf3",showgrid=True, gridwidth=1)
        daily_returns.update_traces(texttemplate='%{text:.2s}', textposition='top left')
        daily_returns.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
        daily_returns.update_traces(line=dict(width=2))
        daily_returns.update_layout(hovermode="x",plot_bgcolor="#f8fbfc",margin_t= 20, margin_r= 40,margin_b= 20,legend_title_text='')
        daily_returns.update_traces(hovertemplate='%{y:,}')
        daily_returns.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        daily_returns.update_annotations(font_size=16,font_family="Arial")
        daily_returns.update_yaxes(title='')
        daily_returns.update_layout(yaxis1=dict(title="Number of Ballots Returned by Day"))
        daily_returns.update_xaxes(title='',showline=True, linewidth=1, linecolor='#7F7F7F')
        daily_returns.update_layout(xaxis1=dict(title="Days Until Election Day"))

        ## Distribution Bar Chart
        voted_df = filtered_df[filtered_df["voted"] == 1]
        voted_display_df = voted_df.groupby(['Year', selected_demo])['VOTER_ID'].sum()
        voted_display_df = pd.DataFrame(voted_display_df)
        voted_display_df = voted_display_df.reset_index()
        voted_display_df['cumal'] = voted_display_df.groupby(['Year', selected_demo])['VOTER_ID'].cumsum()
        voted_display_df['percent'] = voted_display_df.cumal / voted_display_df.groupby('Year').cumal.transform('sum')
        voted_display_df = voted_display_df.sort_values(by=['Year',selected_demo])
        voted_display_df = voted_display_df.sort_values(by='Year',ascending=False).reset_index() #sort of facets

        voted_display_df['label'] = voted_display_df['percent'].astype(float).map('{:.1%}'.format)
        voted_display_df = voted_display_df[(voted_display_df[selected_demo] != "Other")]
        distribution = px.bar(voted_display_df, x=selected_demo, y="percent", text='label',facet_col="Year",
                              facet_col_spacing=0.01,color_discrete_map=color_map,color=selected_demo,
                              custom_data=['cumal'])
        distribution.update_traces(
            hovertemplate="<br>".join([
                "Ballots Returned: %{customdata[0]}",
            ])
        )
        distribution.update_traces(textposition='outside')
        distribution.update_yaxes(title="Distribution", gridcolor = "#edeaf3",showgrid=True, gridwidth=1)
        # distribution.update_layout(hovermode="x",showlegend=True)
        # distribution.update_traces(hovertemplate='%{y:,}')
        distribution.update_layout(yaxis_range=[0, 1],plot_bgcolor="#f8fbfc",margin_t= 30, margin_r= 40,
                                         margin_b= 10,yaxis_tickformat = '.0%',yaxis1=dict(title="Turnout Rate"))
        distribution.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        distribution.update_xaxes(showline=True, linewidth=1, linecolor='#7F7F7F',categoryarray= SORT)
        distribution.update_annotations(font_size=16,font_family="Arial")
        distribution.update_yaxes(title='')
        distribution.update_layout(yaxis1=dict(title="Distribution"),legend_title_text='')
        distribution.update_xaxes(title='')


        # turnout rate
        voted_df = filtered_df[filtered_df["voted"] == 1]
        voted_display_df = voted_df.groupby(['Year', selected_demo])['VOTER_ID'].sum()
        voted_display_df = pd.DataFrame(voted_display_df)
        voted_display_df = voted_display_df.reset_index()
        totalreg_df = base_reg.groupby(['Year', selected_demo])['VOTER_ID'].sum()
        totalreg_df = pd.DataFrame(totalreg_df)
        totalreg_df = totalreg_df.reset_index()
        merged = pd.merge(voted_display_df, totalreg_df, how ='left',left_on = ['Year', selected_demo], right_on = ['Year', selected_demo])
        merged['percent'] = merged.VOTER_ID_x / merged.VOTER_ID_y
        merged = merged.sort_values(by=[selected_demo])
        merged = merged.sort_values(by='Year',ascending=False).reset_index()
        merged['label'] = merged['percent'].astype(float).map('{:.1%}'.format)
        merged = merged[(merged[selected_demo] != "Other")]

        turnout_rates = px.bar(merged, x=selected_demo, y="percent",facet_col="Year",
                               text='label',color_discrete_map=color_map,color=selected_demo,
                              custom_data=['label'])
        turnout_rates.update_traces(
            hovertemplate="<br>".join([
                "Ballots Returned: %{customdata[0]}",
            ])
        )
        turnout_rates.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        turnout_rates.update_annotations(font_size=16,font_family="Arial")
        turnout_rates.update_layout(yaxis_range=[0, 1],plot_bgcolor = "#f8fbfc", margin_t = 20, margin_r = 40, margin_b = 20,yaxis_tickformat = '.0%')
        turnout_rates.update_yaxes(title='',gridcolor = "#edeaf3",showgrid=True, gridwidth=1)
        turnout_rates.update_layout(yaxis1=dict(title="Turnout Rate"),legend_title_text='')
        turnout_rates.update_xaxes(title='',showline=True, linewidth=1, linecolor='#7F7F7F',categoryarray= SORT)
        turnout_rates.update_traces(textposition='outside')



        # Share of votes by day by group
        voted_share_df = filtered_df[filtered_df["voted"] == 1]
        voted_share_df = voted_share_df.groupby(['Year', 'days_out_num', selected_demo])['VOTER_ID'].sum()
        voted_share_df = pd.DataFrame(voted_share_df)
        voted_share_df = voted_share_df.sort_values(by=['Year', 'days_out_num', selected_demo], ascending=False).reset_index()
        voted_share_df['cumal_demo'] = voted_share_df.groupby(['Year', selected_demo])['VOTER_ID'].cumsum()

        voted_share_df_yearday = df[df["voted"] == 1]
        voted_share_df_yearday = voted_share_df_yearday.groupby(['Year', 'days_out_num'])['VOTER_ID'].sum()
        voted_share_df_yearday = pd.DataFrame(voted_share_df_yearday)
        voted_share_df_yearday = voted_share_df_yearday.sort_values(by=['Year', 'days_out_num'],
                                                                    ascending=False).reset_index()

        voted_share_df_yearday['cumal_day'] = voted_share_df_yearday.groupby('Year')['VOTER_ID'].cumsum()
        voted_share_df_yearday = voted_share_df_yearday.drop(columns=['VOTER_ID'])
        voted_share_df = pd.merge(voted_share_df, voted_share_df_yearday, how='left', left_on=['Year', 'days_out_num'],
                                  right_on=['Year', 'days_out_num'])

        voted_share_df['percent'] = voted_share_df.cumal_demo / voted_share_df.cumal_day
        voted_share_df = voted_share_df.sort_values(by=['Year', 'days_out_num', selected_demo]).reset_index()

        voted_share_df['label'] = voted_share_df['percent'].astype(float).map('{:.1%}'.format)
        voted_share_df = voted_share_df.sort_values(by=['Year','days_out_num'],ascending=False) #sort of facets
        voted_share_df = voted_share_df[(voted_share_df[selected_demo] != "Other")]
        voted_share = px.line(voted_share_df, x="days_out_num", y="percent", facet_col="Year",
                              color=selected_demo,color_discrete_map=color_map,
                              custom_data=['label'])
        voted_share.update_traces(
            hovertemplate="<br>".join([
                "Share: %{customdata[0]}",
            ])
        )
        voted_share.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        voted_share.update_annotations(font_size=16,font_family="Arial")
        voted_share.update_layout(plot_bgcolor = "#f8fbfc", margin_t = 20, margin_r = 40, margin_b = 20,yaxis_tickformat = '.0%',xaxis_range=[15, 0])
        voted_share.update_yaxes(title='',gridcolor = "#edeaf3",showgrid=True, gridwidth=1)
        voted_share.update_layout(yaxis1=dict(title="Distribution of Returns"),yaxis_range=[0, 1],legend_title_text='')
        voted_share.update_xaxes(title='',showline=True, linewidth=1, linecolor='#7F7F7F',categoryarray= SORT)
        voted_share.update_layout(xaxis1=dict(title="Days Until Election Day"))

        return overall_turnout, cumulative_turnout, daily_returns,distribution,turnout_rates,voted_share
#
if __name__ == '__main__':
    app.run_server(debug=True)
