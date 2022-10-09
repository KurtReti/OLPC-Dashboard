import apps.plotly_templates.colourblind_template as colourblind_template
import apps.plotly_templates.default_template as default_template
import apps.plotly_templates.dark_template as dark_template
import plotly.express as px


def get_template(colourblind_mode, dark_mode, text_size, text_font):
    """
    Get the template based on accessibility settings
    :param colourblind_mode:
    :param dark_mode: boolean
    :param text_size: int
    :param text_font: string
    :return: dict of plotly template info
    """
    if colourblind_mode and not dark_mode:
        return colourblind_template.template(text_size, text_font)
    elif not colourblind_mode and dark_mode:
        return dark_template.template(text_size, text_font)
    else:
        return default_template.template(text_size, text_font)


def get_colours(colourblind_mode, dark_mode):
    """
    Get the colours based on accessibility settings
    :param colourblind_mode: boolean
    :param dark_mode: boolean
    :return: list of hex/rgb colours
    """
    if colourblind_mode:
        return [
            "#ffffd9",
            "#edf8b1",
            "#c7e9b4",
            "#7fcdbb",
            "#41b6c4",
            "#1d91c0",
            "#225ea8",
            "#253494",
            "#081d58"
        ]
    elif dark_mode:
        return [
            "rgb(217,217,217)",
            "rgb(189,189,189)",
            "rgb(150,150,150)",
            "rgb(115,115,115)",
            "rgb(82,82,82)",
            "rgb(37,37,37)"
        ]
    else:
        return px.colors.sequential.Rainbow
