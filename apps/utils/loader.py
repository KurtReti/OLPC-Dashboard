from dash import dcc


class MyLoading(dcc.Loading):
    def __init__(self, *args, **kwargs):
        kwargs["color"] = "rgb(212, 80, 121)"
        super().__init__(*args, **kwargs)