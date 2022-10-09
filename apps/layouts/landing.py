from dash import html
import dash_bootstrap_components as dbc

layout = html.Div([dbc.Container([html.Div([
    html.Div(html.Img(src="/assets/vaxissoft-logo.png", className="vaxis-logo")),
    html.Div("Who we are", className="landing-heading-1 semi-bold"),
    html.Div(html.Img(src="/assets/logo+title.png", className="landing-logo")),
], className="d-flex justify-content-between", id="landing-heading"),
    html.Div(html.Div("""VAXIS-SOFT is a new team dedicated to software development established in 2021. Our production team is technically in the upper reaches of
                the industry, with experienced staff in front-end, back-end and design. We pay more attention to expressing our customers' products
                clearly and accurately. We have a small team of 6 developers, each specialising in different fields to create a team that is ready to
                tackle any design challenge.""", className="landing-text"), id="landing-body"),
    html.Div(
        html.Div("""Our team vision""", className="d-flex justify-content-center align-items-center vision-border-1"),
        className="d-flex justify-content-center"),
    html.Div(html.Div("""\"Adhering to the principle of honest, standardization and efficiency, winning the market with technology, gaining credibility with creative services, 
                and providing customers with high-quality, efficient and fast services. Facing the future, insist on independent innovation.\"""",
                      className="d-flex justify-content-center align-items-center vision-border-2"),
             className="d-flex justify-content-center"),
    html.Div(html.Div("What you want to know", className="landing-heading-2"),
             className="d-flex justify-content-center"),
    html.Div([html.Div("What are the average screen times of schools in my surrounding area?",
                       className="d-flex align-items-center misc-border-left"),
              html.Div("What are the most popular apps at my school?",
                       className="d-flex align-items-center misc-border-right")],
             className="d-flex justify-content-between"),
    html.Div([html.Div("How much time do students in my school spend on screens?",
                       className="d-flex align-items-center misc-border-left"),
              html.Div("Is there a link between my classes NAPLAN results and their device use?",
                       className="d-flex align-items-center misc-border-right")],
             className="d-flex justify-content-between"),
    html.Div("Find answers to these questions and more in our OLPC Dashboard",
             className="d-flex justify-content-center"),
    html.Div(
        html.A("visit website", href="/app", className="d-flex justify-content-center align-items-center home-button"),
        className="d-flex justify-content-center"),
], className="landing-card"), html.Br()])
