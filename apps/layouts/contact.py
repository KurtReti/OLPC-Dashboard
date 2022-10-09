from dash import html
import dash_bootstrap_components as dbc


def create_contact(pic, name, role, desc, email):
    return dbc.Row([dbc.Col(html.Img(src=f"/assets/{pic}-contact-pic.png", className="contact-photo"), md=2, sm=12),
              dbc.Col([name, html.P(role)],
                       md=3, sm=12),
              dbc.Col(desc,
                       md=4, sm=12),
              dbc.Col(f"Email: {email}",
                       md=3, sm=12),
              ], className="align-items-center contact-row")


text = "This app was developed by VAXIS-SOFT. This page details background information about the developers and how to contact them."
layout = dbc.CardBody([html.Div(
    [html.Div(html.Img(src="/assets/OLPCLogo.png", className="olpc-logo"), className="me-auto"),
     html.Div(text, className="home-intro")],
    className="d-flex"
    ),
    create_contact("kris", "Kris Godina", "Team Lead / Project Management", "Bachelor of Computer Science, Software Engineering (Dean's Scholar)", "kris.godina@outlook.com"),
    create_contact("mruse", "Matthew Ruse", "Lead Backend/Database Developer", "Bachelor of Computer Science, Software Engineering (Dean's Scholar)", "matthew.ruse@gmail.com"),
    create_contact("andrew", "Andrew Day", "Frontend Designer", "Bachelor of Computer Science, Game and Mobile Development", "a.william.day@gmail.com"),
    create_contact("jonah", "Jonah Vanderschoor", "Team lead / Full Stack Developer", "Bachelor of Computer science, Big Data", "jonahvander13@gmail.com"),
    create_contact("kurt", "Kurt Reti", "Frontend Designer", "Bachelor of Computer Science, Software Engineering & Cybersecurity", "kurt.reti@gmail.com"),
    create_contact("yilei", "Yilei Yang", "Frontend Designer/Marketing", "Bachelor of Information Technology, Network Design and Management", "yy211@uowmail.edu.au"),
])
