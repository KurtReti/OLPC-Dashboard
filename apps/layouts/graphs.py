import plotly.express as px
from dash import html, dcc
from apps.layouts.export import create_export_components
from apps.plotly_templates import get_colours, get_template

MODEBAR_CONFIG = {
    'displayModeBar': "hover",
    'displaylogo': False,
    'modeBarButtonsToAdd': [{'name': 'export_data',
                             'icon': {'width': 857.1,
                                      'height': 1000,
                                      'path': 'm214-7h429v214h-429v-214z m500 0h72v500q0 8-6 21t-11 20l-157 156q-5 6-19 12t-22 5v-232q0-22-15-38t-38-16h-322q-22 0-37 16t-16 38v232h-72v-714h72v232q0 22 16 38t37 16h465q22 0 38-16t15-38v-232z m-214 518v178q0 8-5 13t-13 5h-107q-7 0-13-5t-5-13v-178q0-8 5-13t13-5h107q7 0 13 5t5 13z m357-18v-518q0-22-15-38t-38-16h-750q-23 0-38 16t-16 38v750q0 22 16 38t38 16h517q23 0 50-12t42-26l156-157q16-15 27-42t11-49z',
                                      'transform': 'matrix(1 0 0 -1 0 850)'
                                      },
                             'title': 'Export Chart Data',
                             'click': """new Function("gd", "")"""
                             }
                            ]
}


class Graphs:
    """
    Static class to handle creating plotly graphs
    """

    @staticmethod
    def no_data():
        return html.B("no data to display")

    @staticmethod
    def build_graph(method, colourblind_mode=False, dark_mode=False, text_size=0, text_font="Inter",
                    export_button=None, export_filename="export", export_dataframe=None, update_layout={}, **kwargs):
        if method == "scatter_mapbox":
            kwargs["color_continuous_scale"] = get_colours(colourblind_mode, dark_mode)
        else:
            kwargs["color_discrete_sequence"] = get_colours(colourblind_mode, dark_mode)

        fig = getattr(px, method)(**kwargs)

        fig.update_layout(
            template=get_template(colourblind_mode, dark_mode, text_size, text_font),
            coloraxis_showscale=True,
            **update_layout
        )
        graph = dcc.Graph(figure=fig)
        if export_button is True:
            if not export_dataframe:
                export_dataframe = kwargs["data_frame"]
            export_button, store, download = create_export_components(export_dataframe, export_filename)
            graph.config = MODEBAR_CONFIG
            graph = html.Div([graph, export_button, store, download])
        return graph

    @staticmethod
    def scatter_mapbox(colourblind_mode=False, dark_mode=False, text_size=0, text_font="Inter", export_button=None,
                       export_filename="export", export_dataframe=None,
                       update_layout={}, **kwargs):
        return Graphs.build_graph("scatter_mapbox", colourblind_mode=colourblind_mode, dark_mode=dark_mode,
                                  text_size=text_size, text_font=text_font, export_button=export_button,
                                  export_filename=export_filename, export_dataframe=export_dataframe,
                                  update_layout=update_layout, mapbox_style="dark" if dark_mode else "light", **kwargs)

    @staticmethod
    def bar(colourblind_mode=False, dark_mode=False, text_size=0, text_font="Inter", export_button=None,
            export_filename="export", export_dataframe=None,
            update_layout={}, **kwargs):
        return Graphs.build_graph("bar", colourblind_mode=colourblind_mode, dark_mode=dark_mode,
                                  text_size=text_size, text_font=text_font, export_button=export_button,
                                  export_filename=export_filename, export_dataframe=export_dataframe,
                                  update_layout=update_layout, **kwargs)

    @staticmethod
    def pie(colourblind_mode=False, dark_mode=False, text_size=0, text_font="Inter", export_button=None,
            export_filename="export", export_dataframe=None,
            update_layout={}, **kwargs):
        return Graphs.build_graph("pie", colourblind_mode=colourblind_mode, dark_mode=dark_mode,
                                  text_size=text_size, text_font=text_font, export_button=export_button,
                                  export_filename=export_filename, export_dataframe=export_dataframe,
                                  update_layout=update_layout, **kwargs)

    @staticmethod
    def histogram(colourblind_mode=False, dark_mode=False, text_size=0, text_font="Inter", export_button=None,
                  export_filename="export", export_dataframe=None,
                  update_layout={}, **kwargs):
        return Graphs.build_graph("histogram", colourblind_mode=colourblind_mode, dark_mode=dark_mode,
                                  text_size=text_size, text_font=text_font, export_button=export_button,
                                  export_filename=export_filename, export_dataframe=export_dataframe,
                                  update_layout=update_layout, **kwargs)
