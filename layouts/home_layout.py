from dash import Dash, dcc, html
from pandas import read_csv
import charts

df = read_csv("hotel_bookings.csv")

def get_sidebar():
    year = dcc.RadioItems(df['arrival_date_year'].unique(), 2017, id="year"
                          ,className="text-white p-2")
    room_handle = dcc.RadioItems(["assigned", 'reserved'], 'reserved', id="room_handle"
                          ,className="text-white p-2")
    meal = dcc.Dropdown(df['meal'].unique(), 'BB', id="meal_pref",
                        className="text-dark p-2", clearable=False)        
    sidebar = html.Div([
        html.Br(),
        html.H2("Hotel Booking Analysis", className="text-left fw-bold fs-1"),
        html.Br(),
        html.H3("Arrival Year", className="fs-4"),
        year,
        html.Br(),html.Br(),html.Br(),html.Br(), html.Br(),
        html.H3("Room Handling", className="fs-4"),
        room_handle,
        html.Br(),html.Br(),html.Br(),html.Br(),html.Br(),
        html.H3("Meal Prefrence Dropdown", className="fs-4 md-20"),
        meal
        ], className="col-md-2 text-white", style={"background-color": "#AAB99A"}
    )
    return sidebar

def get_main_content():
    tot, rep_perc, child_perc = charts.cancel_table()
    hotel_t, resort_t = charts.lead_table()
    main_content = html.Div([        
        html.Div([
            html.Div([
                html.H5("Total Cancels", className="text-center fw-bold"),
                html.H5(str(tot),className="text-center fw-bold" ),
                html.Hr(style= {"width": "350px", "border-top": "5px solid #AAB99A", "margin": "10px auto"}),
                html.Div([
                    html.Div([
                        html.H6("Repeated Guests", className="text-center fw-bold"),
                        html.H6(f"{rep_perc:.2f} %",className="text-center")
                        ], className = "col"),
                    html.Div([
                        html.H6("With Children", className="text-center fw-bold"),
                        html.H6(f"{child_perc:.2f} %", className="text-center")
                    ], className= "col")        
                ], className = "row", style={"background-color": "#F0F0D7"})
                ],className = "col"),
            html.Div([
                html.H5("Average Lead Time", className = "text-center fw-bold"),
                html.H6("(according to type)", className="text-center fw-bold"),
                html.Hr(className="tm-10",style={"width": "350px", "border-top": "5px solid #AAB99A", "margin": "10px auto"}),
                html.Div([
                    html.Div([
                        html.H6("City Hotel", className="text-center fw-bold"),
                        html.H6((f"%0.2f" % hotel_t),className="text-center")
                        ], className = "col"),
                    html.Div([
                        html.H6("Resort Hotel", className="text-center fw-bold"),
                        html.H6(f"%0.2f"%resort_t,className="text-center")
                    ], className= "col")        
                ], className = "row", style={"background-color": "#F0F0D7"})
            ], className= "col")        
        ], className = "row"),
        
        html.Div([
            dcc.Graph(id="line",className="col-md-6"),
            dcc.Graph(id="special", figure=charts.spVsCanc_scatter(), className="col-md-6")
        ],className="row",style={"background-color": "#F0F0D7", "height": "250px"}),
        html.Div([
            dcc.Graph(id="marketS", className="col-md-6"),
            dcc.Graph(id="room_type", className ="col-md-6")
        ],className="row",  style={"background-color": "#F0F0D7", "height": "250px"}),
        html.Div([ 
            dcc.Graph(id = "country_pie", className = "col-md-5"),
            dcc.Graph(id="park_hist", className="col-md-7")
        ],className="row", style={"background-color": "#F0F0D7", "height": "300px"})
    ], className="col-md-10",  style={"background-color": "#F0F0D7"})
    return main_content

def get_layout():
    main_content = get_main_content()
    sidebar = get_sidebar()
    layout = html.Div([
        html.Div([sidebar, main_content], className = "row")
    ], className="container-fluid")
    
    return layout
