import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
from graph_page import GraphPage

app = dash.Dash(__name__)
graph_num = -1
graph_list = [GraphPage("Settings Page"), GraphPage("Graph 1")]
tab_list = [dcc.Tab(label="Settings", value="tab_0"),
            dcc.Tab(label="Graph 1", value="tab_1")]
drop_list = [dcc.Dropdown(id="x_drop"),
             dcc.Dropdown(id="y_drop", multi=True)]

def add_graph(name = None):
    cur_num = len(graph_list)
    name = f"Graph {cur_num}" if name is None else name
    graph_list.append(GraphPage(name))
    tab_list.append(dcc.Tab(label=name, value=f"tab_{cur_num}"))


app.layout = html.Div([
    dcc.Tabs(id="graph-tabs", value="tab_0"),
    html.Button("Add Graph", id="button"),
    html.Div(id='tab-display'),
    html.Div(id='tmp')
],id='app-container')


@app.callback(Output('tmp', 'children'),
            [Input('x_drop', 'value'),
            Input('y_drop', 'value')])
def update_cur_graph(x_val, y_vals):
    cur_graph = graph_list[graph_num]
    cur_graph.create_graph(x_val, y_vals)


@app.callback(Output('graph-tabs', 'children'),
            [Input('button', 'n_clicks')])
def update_tabs(n_clicks):
    if n_clicks is not None:
        add_graph()
    return tab_list


@app.callback(Output('tab-display', 'children'),
            [Input('graph-tabs', 'value')])
def render_content(tab):
    global graph_num
    graph_num = int(tab[4])
    if graph_num == 0:
        return get_settings()
    else:
        sel_graph = graph_list[graph_num]
        return get_graph_page(sel_graph)


def get_settings():
    assets_list = []
    assets_list.append(html.H3("Settings Page"))
    assets_list.append(dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ))
    assets_list.append(html.Div(id='output-data-upload'))
    return assets_list
    


def get_graph_page(graph):
    options = []
    for var in graph.var_list:
        options.append({'label': var, 'value': var})
    drop_list[0].options, drop_list[0].value = options, graph.x
    drop_list[1].options, drop_list[1].value = options, graph.y
    display_list = [] + drop_list
    display_list.append(dcc.Graph(figure=graph.graph.display()))
    return display_list    


app.run_server(debug=True)