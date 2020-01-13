import os
import dash
import dash_core_components as dcc 
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from random import sample, choice
from skimage import io
import pathlib


###########################################################################
######################        Project Data      ###########################
###########################################################################

pp = pd.read_csv('csv_panama_papers/panama_papers.nodes.entity.csv')

pp["incorporation_date"] = pd.to_datetime(pp["incorporation_date"])
pp['year'], pp['month'] = pp['incorporation_date'].dt.year, pp['incorporation_date'].dt.month

pp.drop(["name", "inactivation_date", "struck_off_date", "ibcRUC", "status", "company_type", "valid_until", "note", "closed_date"], axis=1, inplace=True)

indexes = pp[pp["year"] < 1980].index.to_list()

pp.drop(indexes, inplace=True)
pp.dropna(inplace=True)

pp_ts = pp.groupby(["year","jurisdiction"]).count()["node_id"].unstack()
pp_ts.reset_index(inplace=True)

havens = [
        {"label": "Samoa", "value": "SAM"},
        {"label": "Panama", "value": "PMA"},
        {"label": "Nevada", "value": "NEV"},
        {"label": "United Kingdom", "value": "UK"},
        {"label": "Singapore", "value": "SGP"},
        {"label": "Ras Al Khaimah", "value": "RAK"},
        {"label": "Isle Of Man", "value": "IOM"},
        {"label": "British Anguilla", "value": "ANG"},
        {"label": "Seychelles", "value": "SEY"},
        {"label": "Niue", "value": "NIUE"},
        {"label": "Uruguay", "value": "UY"},
        {"label": "British Virgin Islands", "value": "BVI"},
        {"label": "Hong Kong", "value": "HK"},
        {"label": "New Zealand", "value": "NZL"},
        {"label": "Bahamas", "value": "BAH"},
        {"label": "Cyprus", "value": "CYP"},
        {"label": "Malta", "value": "MLT"},
        {"label": "Belize", "value": "BLZ"},
        {"label": "Jersey", "value": "JSY"},
        {"label": "Wyoming", "value": "WYO"},
        {"label": "Costa Rica", "value": "CRI"}
        ]
havens_full_list = ['SAM', 'PMA', 'NEV', 'UK', 'SGP', 'RAK', 'IOM', 'ANG', 'SEY', 'NIUE', 'UY', 'BVI', 'HK', 'NZL', 'BAH', 'CYP', 'MLT', 'BLZ', 'JSY', 'WYO', 'CRI']
countries = [
        {"label": "Hong Kong", "value": "HKG"},
        {"label": "Taiwan", "value": "TWN"},
        {"label": "China", "value": "CHN"},
        {"label": "Switzerland", "value": "CHE"},
        {"label": "Singapore", "value": "SGP"},
        {"label": "Brazil", "value": "BRA"},
        {"label": "Panama", "value": "PAN"},
        {"label": "Samoa", "value": "WSM"},
        {"label": "Liechtenstein", "value": "LIE"},
        {"label": "Spain", "value": "ESP"},
        {"label": "Thailand", "value": "THA"},
        {"label": "Colombia", "value": "COL"},
        {"label": "Jersey", "value": "JEY"},
        {"label": "Andorra", "value": "AND"},
        {"label": "Seychelles", "value": "SYC"},
        {"label": "Ireland", "value": "IRL"},
        {"label": "Belgium", "value": "BEL"},
        {"label": "Israel", "value": "ISR"},
        {"label": "Gibraltar", "value": "GIB"},
        {"label": "Guernsey", "value": "GGY"},
        {"label": "United Arab Emirates", "value": "ARE"},
        {"label": "Cyprus", "value": "CYP"},
        {"label": "Venezuela", "value": "VEN"},
        {"label": "Isle of Man", "value": "IMN"},
        {"label": "Lebanon", "value": "LBN"},
        {"label": "Denmark", "value": "DNK"},
        {"label": "Uruguay", "value": "URY"},
        {"label": "Jordan", "value": "JOR"},
        {"label": "Bahamas", "value": "BHS"},
        {"label": "United Kingdom", "value": "GBR"},
        {"label": "nan", "value": "nan"},
        {"label": "Belize", "value": "BLZ"},
        {"label": "Luxembourg", "value": "LUX"},
        {"label": "Ecuador", "value": "ECU"},
        {"label": "Guatemala", "value": "GTM"},
        {"label": "Germany", "value": "DEU"},
        {"label": "Mauritius", "value": "MUS"},
        {"label": "Turkey", "value": "TUR"},
        {"label": "United States", "value": "USA"},
        {"label": "Monaco", "value": "MCO"},
        {"label": "Estonia", "value": "EST"},
        {"label": "Niue", "value": "NIU"},
        {"label": "Czech Republic", "value": "CZE"},
        {"label": "Netherlands", "value": "NLD"},
        {"label": "Hungary", "value": "HUN"},
        {"label": "Costa Rica", "value": "CRI"},
        {"label": "Portugal", "value": "PRT"},
        {"label": "Cayman Islands", "value": "CYM"},
        {"label": "South Africa", "value": "ZAF"},
        {"label": "Malta", "value": "MLT"},
        {"label": "New Zealand", "value": "NZL"},
        {"label": "Côte d'Ivoire", "value": "CIV"},
        {"label": "Dominican Republic", "value": "DOM"},
        {"label": "France", "value": "FRA"},
        {"label": "Italy", "value": "ITA"},
        {"label": "Canada", "value": "CAN"},
        {"label": "Russia", "value": "RUS"},
        {"label": "Greece", "value": "GRC"},
        {"label": "Saudi Arabia", "value": "SAU"},
        {"label": "Qatar", "value": "QAT"},
        {"label": "Mexico", "value": "MEX"},
        {"label": "Peru", "value": "PER"},
        {"label": "Bermuda", "value": "BMU"},
        {"label": "El Salvador", "value": "SLV"},
        {"label": "Australia", "value": "AUS"},
        {"label": "Saint Kitts and Nevis", "value": "KNA"},
        {"label": "Argentina", "value": "ARG"},
        {"label": "Japan", "value": "JPN"},
        {"label": "Austria", "value": "AUT"},
        {"label": "American Samoa", "value": "ASM"},
        {"label": "Paraguay", "value": "PRY"},
        {"label": "Chile", "value": "CHL"},
        {"label": "Egypt", "value": "EGY"},
        {"label": "Sweden", "value": "SWE"},
        {"label": "British Virgin Islands", "value": "VGB"},
        {"label": "Poland", "value": "POL"},
        {"label": "Slovenia", "value": "SVN"},
        {"label": "Philippines", "value": "PHL"},
        {"label": "Saint Lucia", "value": "LCA"},
        {"label": "Indonesia", "value": "IDN"},
        {"label": "Honduras", "value": "HND"},
        {"label": "South Korea", "value": "KOR"},
        {"label": "Kuwait", "value": "KWT"},
        {"label": "Haiti", "value": "HTI"},
        {"label": "Zimbabwe", "value": "ZWE"},
        {"label": "Sudan", "value": "SDN"},
        {"label": "Nicaragua", "value": "NIC"},
        {"label": "Turks and Caicos Islands", "value": "TCA"},
        {"label": "Latvia", "value": "LVA"},
        {"label": "Nigeria", "value": "NGA"},
        {"label": "Ukraine", "value": "UKR"},
        {"label": "Anguilla", "value": "AIA"},
        {"label": "Kenya", "value": "KEN"},
        {"label": "Romania", "value": "ROU"},
        {"label": "Saint Vincent and the Grenadines", "value": "VCT"},
        {"label": "Norway", "value": "NOR"},
        {"label": "Bolivia", "value": "BOL"},
        {"label": "Lithuania", "value": "LTU"},
        {"label": "Viet Nam", "value": "VNM"},
        {"label": "Aruba", "value": "ABW"},
        {"label": "Bulgaria", "value": "BGR"},
        {"label": "Malaysia", "value": "MYS"},
        {"label": "Finland", "value": "FIN"},
        {"label": "Iran", "value": "IRN"},
        {"label": "Lesotho", "value": "LSO"},
        {"label": "Mozambique", "value": "MOZ"},
        {"label": "Macao", "value": "MAC"},
        {"label": "Ghana", "value": "GHA"},
        {"label": "Georgia", "value": "GEO"},
        {"label": "Yemen", "value": "YEM"},
        {"label": "Antigua and Barbuda", "value": "ATG"},
        {"label": "Curaçao", "value": "CUW"},
        {"label": "India", "value": "IND"},
        {"label": "Macedonia", "value": "MKD"},
        {"label": "Morocco", "value": "MAR"},
        {"label": "Senegal", "value": "SEN"},
        {"label": "Dominica", "value": "DMA"},
        {"label": "Namibia", "value": "NAM"},
        {"label": "Botswana", "value": "BWA"},
        {"label": "Cuba", "value": "CUB"},
        {"label": "Liberia", "value": "LBR"},
        {"label": "Cook Islands", "value": "COK"},
        {"label": "Syria", "value": "SYR"},
        {"label": "Sint Maarten (Dutch part)", "value": "SXM"},
        {"label": "Belarus", "value": "BLR"},
        {"label": "Djibouti", "value": "DJI"},
        {"label": "Barbados", "value": "BRB"},
        {"label": "Tunisia", "value": "TUN"},
        {"label": "Bahrain", "value": "BHR"},
        {"label": "Croatia", "value": "HRV"},
        {"label": "Nauru", "value": "NRU"},
        {"label": "Azerbaijan", "value": "AZE"},
        {"label": "Pakistan", "value": "PAK"},
        {"label": "Libya", "value": "LBY"},
        {"label": "Uganda", "value": "UGA"},
        {"label": "Uzbekistan", "value": "UZB"},
        {"label": "Trinidad and Tobago", "value": "TTO"},
        {"label": "Iceland", "value": "ISL"},
        {"label": "Sri Lanka", "value": "LKA"},
        {"label": "U.S. Virgin Islands", "value": "VIR"},
        {"label": "Tanzania", "value": "TZA"},
        {"label": "Puerto Rico", "value": "PRI"},
        {"label": "Malawi", "value": "MWI"},
        {"label": "Chad", "value": "TCD"},
        {"label": "Guam", "value": "GUM"},
        {"label": "Oman", "value": "OMN"},
        {"label": "Jamaica", "value": "JAM"},
        {"label": "Mali", "value": "MLI"},
        {"label": "Montenegro", "value": "MNE"},
        {"label": "Kazakhstan", "value": "KAZ"},
        {"label": "Vanuatu", "value": "VUT"},
        {"label": "Moldova", "value": "MDA"},
        {"label": "Angola", "value": "AGO"},
        {"label": "Bangladesh", "value": "BGD"},
        {"label": "Central African Republic", "value": "CAF"},
        {"label": "Brunei", "value": "BRN"},
        {"label": "Albania", "value": "ALB"},
        {"label": "Cameroon", "value": "CMR"},
        {"label": "Zambia", "value": "ZMB"},
        {"label": "Slovakia", "value": "SVK"}
        ]
countries_full_list = ['HKG', 'TWN', 'CHN', 'CHE', 'SGP', 'BRA', 'PAN', 'WSM', 'LIE', 'ESP', 'THA', 'COL', 'JEY', 'AND', 'SYC', 'IRL', 'BEL', 'ISR', 'GIB', 'GGY', 'ARE', 'CYP', 'VEN', 'IMN', 'LBN', 'DNK', 'URY', 'JOR', 'BHS', 'GBR', 'BLZ', 'LUX', 'ECU', 'GTM', 'DEU', 'MUS', 'TUR', 'USA', 'MCO', 'EST', 'NIU', 'CZE', 'NLD', 'HUN', 'CRI', 'PRT', 'CYM', 'ZAF', 'MLT', 'NZL', 'CIV', 'DOM', 'FRA', 'ITA', 'CAN', 'RUS', 'GRC', 'SAU', 'QAT', 'MEX', 'PER', 'BMU', 'SLV', 'AUS', 'KNA', 'ARG', 'JPN', 'AUT', 'ASM', 'PRY', 'CHL', 'EGY', 'SWE', 'VGB', 'POL', 'SVN', 'PHL', 'LCA', 'IDN', 'HND', 'KOR', 'KWT', 'HTI', 'ZWE', 'SDN', 'NIC', 'TCA', 'LVA', 'NGA', 'UKR', 'AIA', 'KEN', 'ROU', 'VCT', 'NOR', 'BOL', 'LTU', 'VNM', 'ABW', 'BGR', 'MYS', 'FIN', 'IRN', 'LSO', 'MOZ', 'MAC', 'GHA', 'GEO', 'YEM', 'ATG', 'CUW', 'IND', 'MKD', 'MAR', 'SEN', 'DMA', 'NAM', 'BWA', 'CUB', 'LBR', 'COK', 'SYR', 'SXM', 'BLR', 'DJI', 'BRB', 'TUN', 'BHR', 'HRV', 'NRU', 'AZE', 'PAK', 'LBY', 'UGA', 'UZB', 'TTO', 'ISL', 'LKA', 'VIR', 'TZA', 'PRI', 'MWI', 'TCD', 'GUM', 'OMN', 'JAM', 'MLI', 'MNE', 'KAZ', 'VUT', 'MDA', 'AGO', 'BGD', 'CAF', 'BRN', 'ALB', 'CMR', 'ZMB', 'SVK']

defaultImg = io.imread("images/power_players.jpg")

img_map = {
    "AUS": "images/australia.png",
    "IRQ": "images/iraq.png",
    "MOR": "images/morocco.png",
    "YEM": "images/yemen.png",
    "TUR": "images/turkey.png",
    "GBR": "images/uk.png",
    "LBY": "images/liberia.png",
    "LTU": "images/lithuania.png",
    "NGA": "images/nigeria.png",
    "SAU": "images/saudi .png",
    "ANG": "images/angola.png",
    "KEN": "images/kenya.png",
    "VEN": "images/venezuela.png",
    "AUS": "images/austria.png",
    "JOR": "images/jordan.png",
    "RUS": "images/russia.png",
    "IND": "images/india.png",
    "CAN": "images/canada.png",
    "UKR": "images/ukraine.png",
    "ITA": "images/italy.png",
    "ARG": "images/argentina.png",
    "CIV": "images/coteivoire.png",
    "GHA": "images/ghana.png",
    "PRT": "images/portugal.png",
    "PAK": "images/pakistan.png",
    "GEO": "images/georgia.png",
    "CHN": "images/china.png",
    "AZE": "images/azerbaijan.png",
    "UGA": "images/uganda.png",
    "SDN": "images/sudan.png",
    "ISL": "images/iceland.png",
    "UAE": "images/uae.png",
    "MON": "images/mongolia.png",
    "IDN": "images/indonesia.png",
    "ECU": "images/ecuador.png",
    "FRA": "images/france.png",
    "KAZ": "images/kazakhstan.png",
    "SYR": "images/syria.png",
    "QAT": "images/qatar.png",
    "BHR": "images/bermuda.png",
    "EGY": "images/egypt.png",
    "MLT": "images/malta.png",
    "MEX": "images/mexico.png",
    "ZAM": "images/zambia.png",
    "BRA": "images/brazil.png",
    "SPA": "images/spain.png",
    "JAP": "images/japan.png",
    "USA": "images/us.png"
}

###########################################################################
####################        App Layout      ###############################
###########################################################################

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div(children=[

html.Div([
        html.H1(children="The Panama Papers")
], className='title'),
html.Div([
        html.P(children="A Visual Exploratory Framework for Tax Havens")
], className='subtitle'),

html.Br(),

html.Div([

    html.P([

    ], className='separator'),

    html.Div([

        html.Div([

                html.Div([


                            html.Div([

                                html.Div([

                                ], className="box"),

                                html.P([ "Explore the Panana Papers figures"

                                ],className="P"),

                            ]),



                    html.Div([
                        html.P([
                                "The Panama Papers expose the internal operations of one of the world’s leading firms in incorporation of offshore entities, Panama-headquartered Mossack Fonseca. The 2.6 terabyte trove of data at the core of this investigation contains nearly 40 years of records, and includes information about more than 210,000 companies in 21 offshore jurisdictions."
                     ],className='p'),

                    ]),

                    html.P(['select tax haven:'], className="label"),

                    html.Div([

                        dcc.Dropdown(
                        id="time-series-countries",
                        options=havens,
                        multi=True,
                        value=sample(havens_full_list, 10)
                        )

                    ],className='dropdown_1')

                ],className='top_left')

        ], className='column1_row1'),

        html.Div([

            html.Div([

                dcc.Graph(
                    id="time-series-incorporation"
                ),

                html.Div([
                        dcc.RangeSlider(
                                    id='year-slider',
                                    count=5,
                                    min=pp_ts['year'].min(),
                                    max=pp_ts['year'].max(),
                                    value=[pp_ts['year'].min(), pp_ts['year'].max()],
                                    marks={i: '{}'.format(i) for i in range(int(pp_ts['year'].min()), int(pp_ts['year'].max()))},step=1,
                                    allowCross= False
                                ),

                    ], className='slider'),

            ],className='topright')

        ],className='column2_row2')

    ],className='row'),

    html.P([

    ], className='separator'),

    html.Div([

                html.Div([

                    html.Div([

                        html.Div([

                        ], className="box"),

                        html.P(["On the hunt for tax evaders"

                                ], className="P"),

                    ]),

                    html.Div([
                        html.P([
                            "In the papers were revealed names of very powerful people and world leaders"
                        ], className='p'),

                    ]),

                    html.P(['select country:'],className="label"),

                    html.Div([
                            dcc.Dropdown(
                                    id="sankey-country",
                                    options=countries,
                                    value=choice(countries_full_list))
                        ],className="dropdown_2")




                ],className="column1_row2"),

                html.Div([

                    dcc.Graph(
                        id="sankey-flow"
                    ),


                    html.Div([
                            dcc.RangeSlider(
                                            id='sankey-slider',
                                            count=1,
                                            min=pp_ts['year'].min(),
                                            max=pp_ts['year'].max(),
                                            value=[pp_ts['year'].min(), pp_ts['year'].max()],
                                            marks={i: '{}'.format(i) for i in range(int(pp_ts['year'].min()), int(pp_ts['year'].max()))},        step=1
                                        )

                        ], className='slider'),

                ],className='column2_row2')



    ],className='row'),

    html.Br(),

    html.P([

                ], className='separator'),

    html.Div([

        html.Div([

            dcc.Graph(
                id="image"
            ),

        ],className='column1_row3'),

        html.Br(),

        html.Div([

            dcc.Graph(
                id="map"
            )
        ], className='column2_row3')

    ],className='row'),

    html.Br(),

html.P([

        ], className='separator'),

],className='container'),


html.Footer([
            "Made by Dave Montali M20190201 Matteo Fiorani M20190746 Umberto Tammaro M20190806"
        ], className="footer"),

])


###########################################################################
####################        Dash Components      ##########################
###########################################################################

@app.callback(
    Output("time-series-incorporation", "figure"),
    [Input("time-series-countries", "value"),
    Input('year-slider', "value")]
)
def time_series(selected_havens, selected_year):
    filt_df = pp_ts[pp_ts["year"] > selected_year[0]]
    filt_df = filt_df[filt_df["year"] <= selected_year[1]]
    traces = []
    for c in selected_havens:
        traces.append(dict(
            x=filt_df.year,
            y=filt_df[c],
            text=c,
            name=c
        ))
    
    return {
        "data": traces
    }

@app.callback(
    Output("sankey-flow", "figure"),
    [Input("sankey-country", "value"),
    Input("sankey-slider", "value")]
)
def sankey_flow(selected_country, selected_year):
    filt_df = pp[pp["country_codes"] == selected_country]
    filt_df = filt_df[filt_df["year"] > selected_year[0]]
    filt_df = filt_df[filt_df["year"] <= selected_year[1]]
    haven_list = list(filt_df["jurisdiction"].unique())
    fig = go.Figure(data=[go.Sankey(
    node = dict(
      pad = 15,
      thickness = 20,
      line = dict(color = "black", width = 0.5),
      label = [selected_country] + haven_list,
      color = "blue",
    ),
    link = dict(
      source = [0] * len(haven_list),
      target = [x for x in range(1, len(haven_list)+1)],
      value = [filt_df[filt_df["jurisdiction"] == x].count()[0] for x in haven_list]
    ))])

    fig.update_layout(title_text="Tax Haven Popularity by Country", font_size=10)

    return fig

@app.callback(
    Output("image", "figure"),
    [Input("sankey-country", "value")]
)
def return_images(selected_country):
    if selected_country in img_map:
        img = io.imread(img_map[selected_country])
        fig = px.imshow(img)
        fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
        return fig
    else:
        fig = px.imshow(defaultImg)
        fig.update_xaxes(showticklabels=False).update_yaxes(showticklabels=False)
        return fig

@app.callback(
    Output("map", "figure"),
    [Input("sankey-country", "value")]
)
def map(selected_country):
    filt_df = pp[pp["country_codes"] == selected_country]
    selected_country = filt_df["countries"].unique()[0]
    clist = [[selected_country, x] for x in filt_df["jurisdiction_description"]]
    polyline = [i for sl in clist for i in sl]
    
    fig = px.line_geo(filt_df, locations=polyline,
                    locationmode="country names",
                    projection="orthographic")

    return fig

##########################################################################
#####################        Exec App      ###############################
##########################################################################

if __name__ == '__main__':
    app.run_server(debug=True)