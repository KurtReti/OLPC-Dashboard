import plotly.graph_objects as go


def template(scale=0, text_font="Arial"):
    """
    Return the dash template with scaled text and selected front
    :param scale: int
    :param text_font: string
    :return: dict
    """
    return dict(
        layout=go.Layout(font_family=text_font,
                         font_color= "white",
                         yaxis=dict(
                             title_font_size=16 + 2 * int(scale),
                         ),
                         xaxis=dict(
                             title_font_size=14 + 2 * int(scale),
                             tickfont_size=10 + 2 * int(scale),
                         ),
                         legend=dict(
                             font_color="#FFFFFF",
                             font_size=10 + 2 * int(scale)
                         ),
                         coloraxis=dict(
                             colorbar=dict(
                                 tickfont_size=10 + 2 * int(scale)
                             )
                         ),
                         uniformtext_minsize=10 + 2 * int(scale),
                         uniformtext_mode='hide',
                         hoverlabel=dict(
                             font_size=10 + 2 * int(scale)
                         ),
                         paper_bgcolor='rgb(22, 27, 34)',
                         plot_bgcolor='rgb(22, 27, 34)',
                         modebar_bgcolor='rgba(0, 0, 0, 0)',
                         modebar_color='white',
                         modebar_activecolor='lightgray',
                         ))
