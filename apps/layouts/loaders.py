from dash import html

# replicate dash loaders since they don't show on page load and need workaround to have them displayed

cube_loader = html.Div(html.Div([html.Div(className="dash-cube-side dash-cube-side--front"),
                                 html.Div(className="dash-cube-side dash-cube-side--back"),
                                 html.Div(className="dash-cube-side dash-cube-side--right"),
                                 html.Div(className="dash-cube-side dash-cube-side--left"),
                                 html.Div(className="dash-cube-side dash-cube-side--top"),
                                 html.Div(className="dash-cube-side dash-cube-side--bottom")], className="dash-cube"),
                       className="dash-spinner dash-cube-container")

default_loader = html.Div(
    [html.Div(className="dash-default-spinner-rect1"), html.Div(className="dash-default-spinner-rect2"),
     html.Div(className="dash-default-spinner-rect3"), html.Div(className="dash-default-spinner-rect4"),
     html.Div(className="dash-default-spinner-rect5")], className="dash-spinner dash-default-spinner")
