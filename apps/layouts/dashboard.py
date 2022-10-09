from dash import html
import dash_bootstrap_components as dbc


def generate_layout(active_tab=None, children=[]):
    """
    Generates a layout for a dashboard tab and sets the active tab.
    :param active_tab: active tab name
    :param children: dash Components or list of Dash Components
    :return: list of dash Components
    """
    tabs = [
        dbc.Tabs(
            [
                dbc.Tab(label="Apps", tab_id="apps", activeTabClassName="dashboard-active", tab_class_name="first"),
                dbc.Tab(label="Devices", tab_id="devices", activeTabClassName="dashboard-active"),
                dbc.Tab(label="Naplan", tab_id="naplan", activeTabClassName="dashboard-active"),
                dbc.Tab(label="Compare", tab_id="compare", activeTabClassName="dashboard-active",
                        tab_class_name="last"),
            ],
            active_tab=active_tab,
            id="tabs",
            class_name="nav-justified vertical-tabs"
        ),
        dbc.CardBody(html.Div(id="dashboard-content", children=children),
                     style={"paddingLeft": "0.75rem", "paddingRight": "0.75rem", "paddingTop": 0}),
    ]
    return tabs


layout = html.P("Choose a category from above to get started!")
