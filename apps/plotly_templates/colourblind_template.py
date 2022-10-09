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
                         yaxis=dict(
                             title_font_size=16 + 2 * int(scale),
                         ),
                         xaxis=dict(
                             title_font_size=14 + 2 * int(scale),
                             tickfont_size=10 + 2 * int(scale),
                         ),
                         legend=dict(
                             bgcolor='rgba(255, 255, 255, 0)',
                             bordercolor='rgba(255, 255, 255, 0)',
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
                         paper_bgcolor='rgb(255,255,255)',
                         plot_bgcolor='rgb(255,255,255)',
                         modebar_bgcolor='rgba(0, 0, 0, 0)',
                         modebar_color='#000000',
                         modebar_activecolor='#000000',
                         ))
