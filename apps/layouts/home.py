from dash import dcc, html
import dash_bootstrap_components as dbc


def create_card(title, desc, link_name, link):
    return dbc.Col(
        dbc.Card([
        dbc.CardHeader(title, className="box-heading"),
        dbc.CardBody(
            desc,
            className="box-text",
        ),
        dbc.CardFooter(dcc.Link(link_name, href=link,
                 className="d-flex justify-content-center align-items-center box-button")),
    ]), md=12, lg=4, style={"marginBottom": "1.5rem"}
)


card1 = create_card("Total number of devices",  "For the number of devices by state, suburb, postcode or school, visit the devices dashboard.", "Devices dashboard", "/app/dashboard/devices")

card2 = create_card("Average naplan scores",  "For naplan results by State, Suburb, Postcode or school, visit the naplan dashboard.", "Naplan dashboard", "/app/dashboard/naplan")

card3 = create_card("Average screen-on time",  "For information about the usage statistics of OLPC devices, visit the apps dashboard.", "Apps dashboard", "/app/dashboard/apps")

card4 = create_card("Top rated school by naplan results",  "For naplan rankings and statistics by school, visit the naplan dashboard.", "Naplan dashboard", "/app/dashboard/naplan")

card5 = create_card("Most popular app",  "For statistics relating to apps, including category breakdown, visit the apps dashboard.", "Apps dashboard", "/app/dashboard/apps")

card6 = create_card("Compare App Usage",  "To compare State, Suburbs, Postcode or Schools by App Usage and Naplan Results.", "Compare dashboard", "/app/dashboard/compare")

text = "Welcome to the OLPC dashboard. Select a card here on the home screen if you know what you are looking for, or if you are interested in viewing all available data navigate to the ‘Dashboard’ tab at the top of your screen. "

layout = dbc.CardBody([html.Div(
    [html.Div(html.Img(src="/assets/OLPCLogo.png", className="olpc-logo"), className="me-auto"),
     html.Div(text, className="home-intro")],
    className="d-flex"
),
    dbc.Row([
        card1,
        card2,
        card3
    ]),
    dbc.Row([
        card4,
        card5,
        card6
    ]),
    html.Br(),
    html.P(["Data obtained from ", html.A("OLPC", href="https://laptop.org/"), " and ",
            html.A("MySchool", href="https://www.myschool.edu.au/")],
           style={"text-align": "center"})])
