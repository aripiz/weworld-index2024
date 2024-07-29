# layout_methodology.py

from index import data, metadata
from dash import dcc, html
import dash_bootstrap_components as dbc

from configuration import NOTES_FILE

# Options
subindexes_list = [data.columns[4]]
features_list = data.columns[4:23].to_list()
years_list = data['year'].unique()
components_list = [f"Indicator {num}: {metadata.loc[num]['name']}" for num in metadata.loc[1:30].index]
indicators_list = [f"{num}: {metadata.loc[num]['name']}" for num in metadata.loc[1:30].index]

# Methodology tabs
tab_indicators = html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Label("Indicator"),
            dcc.Dropdown(
                id='indicator',
                options=indicators_list,
                value=indicators_list[0],
                style={"width": "100%"}),
        ]),
    ], className='mt-2'),
    dbc.Row([
        dbc.Col(
            dbc.Table([
                html.Tbody([
                    html.Tr([html.Th("Indicator", style={'font-weight': 'bold', 'text-transform': 'uppercase'}), html.Td(id="indicator_num")]),
                    html.Tr([html.Th("Name", style={'font-weight': 'bold', 'text-transform': 'uppercase'}), html.Td(id="indicator_name")]),
                    html.Tr([html.Th("Sub-index", style={'font-weight': 'bold', 'text-transform': 'uppercase'}), html.Td(id="indicator_sub")]),
                    html.Tr([html.Th("Dimension", style={'font-weight': 'bold', 'text-transform': 'uppercase'}), html.Td(id="indicator_dim")]),
                    html.Tr([html.Th("Definition", style={'font-weight': 'bold', 'text-transform': 'uppercase'}), html.Td(id="indicator_des")]),
                    html.Tr([html.Th("Unit", style={'font-weight': 'bold', 'text-transform': 'uppercase'}), html.Td(id="indicator_unit")]),
                    html.Tr([html.Th("Last update", style={'font-weight': 'bold', 'text-transform': 'uppercase'}), html.Td(id="indicator_update")]),
                    html.Tr([html.Th("Source", style={'font-weight': 'bold', 'text-transform': 'uppercase'}), html.Td(html.A(id="indicator_source", target="_blank", rel="noopener noreferrer"))])
                ])
            ], bordered=True, hover=True, responsive=True, striped=True, size='sm')
        )
    ], className='mt-2')
])

tab_construction = html.Div([
    dbc.Row(
        dbc.Col([
            dcc.Markdown(
                """
                CFA Index ranks 157 countries from 2015 to 2023 combining 30 different indicators. The Index - together with the 3 Sub-indexes _Context_, _Children_ and _Women_ - aims at inquiring the implementation of human rights for children and women at the country, regional area and world level.
                """),
                html.Div(["For a detailed description of the method adopted refer to the ", html.A("Techincal Notes", href=NOTES_FILE),'.']),
            ]),
    className='mt-4', justify='evenly' ),
    dbc.Row([
        dbc.Col([
            dcc.Markdown("### Index structure"),
            dcc.Markdown(
                """
            The need to evaluate the performance of territories separately in relation to the three sub-indices arises from a specific assumption: intervening to ensure inclusion in general, without considering the specific gender and generational needs and risks, adopting an intersectional approach, does not allow for the full realization of the rights and empowerment of women, children, and adolescents.

            Real inclusion for these categories, in fact, can only be achieved through the creation, implementation, and monitoring of appropriate policies that must be multidimensional to account for the intersection between the rights of women and minors, and targeted to address their specific needs. Therefore, it is necessary to look even more closely at their conditions.

            It is therefore necessary to proceed on two parallel and complementary fronts: on the one hand, it is essential to work on the contexts in which women, children, and adolescents live to make them as favorable as possible for their full development; on the other hand, it cannot be assumed that favorable contexts alone are sufficient to meet the needs and demands of women, children, and adolescents, for which adequate policies and targeted interventions are necessary.
                """

            ),
        ], lg=6, xs =12),
        dbc.Col(
            dbc.CardGroup([
                dbc.Card([
                    dbc.CardImg(
                        src="assets/icona-contesto.png",
                        top=True,
                        style={"width": "100px",  # Riduce la larghezza dell'immagine
                                "height": "100px",  # Riduce l'altezza dell'immagine
                                "object-fit": "cover"  # Mantiene le proporzioni e adatta l'immagine all'area specificata
                        }
                    ),
                    dbc.CardBody([
                        html.H4("Context", className="card-title"),
                        html.Div([html.P(dim) for dim in metadata.loc[[1,3,5,7,9],'dimension']],
                        className="card-text",), 
                        ])
                ]),
                dbc.Card([
                    dbc.CardImg(
                        src="assets/icona-bambini.png",
                        top=True,
                        style={"width": "100px",  # Riduce la larghezza dell'immagine
                                "height": "100px",  # Riduce l'altezza dell'immagine
                                "object-fit": "cover"  # Mantiene le proporzioni e adatta l'immagine all'area specificata
                        }
                    ),
                    dbc.CardBody([
                        html.H4("Children", className="card-title"),
                        html.Div([ html.P(dim) for dim in metadata.loc[[11,13,15,17,19],'dimension']],
                        className="card-text",)
                        ])
                ]),
                dbc.Card([
                    dbc.CardImg(
                        src="assets/icona-donne.png",
                        top=True,
                        style={"width": "100px",  # Riduce la larghezza dell'immagine
                                "height": "100px",  # Riduce l'altezza dell'immagine
                                "object-fit": "cover"  # Mantiene le proporzioni e adatta l'immagine all'area specificata
                        }
                    ),
                    dbc.CardBody([
                        html.H4("Women", className="card-title"),
                        html.Div([ html.P(dim) for dim in metadata.loc[[21,23,25,27,29],'dimension']],
                        className="card-text",)
                    ])
                ])
            ]),
        align='center', lg= 6, xs =12)
    ], className='mt-4', justify="around"),
    dbc.Row([
        dbc.Col([
            dcc.Markdown("### Aggregation process"),
            dcc.Markdown("""
                CFA Index for each territory consists of a **0-100 score** developed by aggregating the normalised data of its 30 Indicators in **three different steps**.

                First, the scores of each of each **Dimension** is calculated by taking the arithmetic mean of the scores of the two constituent **Component** (normalised indicators). Next, to avoid full compensability between Dimensions, the score of the **Sub-indexes** is determined by the geometric mean of the Dimensions that are part of it. Finally, the geometric mean is also used to calculate the overall **Index** from the 3 Sub-indexes.

                This kind of aggregation is **non-compensatory**: a poor performance in one aspect judged to be crucial for inclusion cannot be fully or partly compensated for by a high score in others.
                """)
        ], lg=6, xs =12),
        dbc.Col(
            dbc.CardGroup([
                dbc.Card(
                    dbc.CardBody([
                        html.H4("Dimensions", className="card-title"),
                        dcc.Markdown("The **arithmetic mean** of the **2 Components** (indicators) of each dimension gives its score.", className="card-text")
                        ])
                ),
                dbc.Card(
                    dbc.CardBody([
                        html.H4("Sub-indexes", className="card-title"),
                         dcc.Markdown("The **geometric mean** of the **5 Dimensions** of each Sub-index gives its score.", className="card-text")
                        ])
                ),
                dbc.Card(
                    dbc.CardBody([
                        html.H4("Index", className="card-title"),
                        dcc.Markdown("The **geometric mean** of **3 Sub-indexes** gives the Index score.", className="card-text")
                    ])
                )
            ]),
        align='center', lg= 6, xs =12)
    ], className='mt-4', justify="around")
])


