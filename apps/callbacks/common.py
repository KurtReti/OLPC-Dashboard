from dash import Input, State
from dash.development.base_component import Component
from app import app
from apps.layouts.accessibility import text_size, text_font, colourblind_mode, dark_mode


def transform_input(i):
    """
    Transforms a Component or dict to a Input
    :param i: dash Component or dict
    :return: Dash Input
    """
    if isinstance(i, Component):
        return Input(i, 'value')
    elif isinstance(i, Input):
        return i
    elif isinstance(i, dict):
        return Input(i, 'value')
    else:
        raise Exception("input must be a dash component or an instance of dash Input")


def transform_state(i):
    """
    Transforms a Component or dict to a State
    :param i: dash Component or dict
    :return: dash State
    """
    if isinstance(i, Component):
        return State(i, 'value')
    elif isinstance(i, State):
        return i
    elif isinstance(i, dict):
        return State(i, 'value')
    else:
        raise Exception("state must be a dash component or an instance of dash State")


def location_filtered_callback(inputs, outputs, states=[], accessibility=[], **kwargs):
    """
    Decorator function to tranform callbacks and simplify dash app.callback
    :param inputs: array of input as either dash Components (which are transformed to to Dash Inputs) or Dash Input instances
    :param outputs: takes an array of Dash Output instances
    :param states: takes an optional argument states which accepts an array of Dash State instances
    :param accessibility: takes an optional boolean accessibility
    :param kwargs: optional key value pairs arguments
    :return: wrapper to be used as a Python decorator
    """
    if accessibility:
        accessibility = [Input(text_size, 'value'),
                         Input(text_font, 'value'),
                         Input(colourblind_mode, 'value'),
                         Input(dark_mode, 'value')]
    # flatten 1 element list
    if isinstance(outputs, list) and len(outputs) == 1:
        outputs = outputs[0]

    def wrapper(func):
        # apply dash callback decorator to register callback
        @app.callback(
            output=outputs,
            inputs=[transform_input(i) for i in inputs] + accessibility,
            state=[transform_state(i) for i in states],
            **kwargs
        )
        def inner(*args, **kwargs):
            return func(*args, **kwargs)

        return inner

    return wrapper
