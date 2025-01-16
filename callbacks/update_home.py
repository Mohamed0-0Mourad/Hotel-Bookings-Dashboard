from dash import Input, Output
import charts

def register_callbacks(app):
    @app.callback(Output("line", "figure"), [Input("year", "value")])
    def update_line(year):
        return charts.trend_line(year)

    @app.callback(Output("marketS", "figure"), [Input("year", "value")])
    def update_scatter(year):
        return charts.marketVsCanc_bar(year)

    @app.callback(Output("room_type", "figure"), [Input("room_handle", "value"), Input("year", "value")])
    def update_bar(room_handle, year):
        return charts.room_bar(room_handle, year)
    
    @app.callback(Output("country_pie", "figure"), [Input("meal_pref", "value"), Input("year", "value")])
    def update_pie(meal_pref, year):
        return charts.country_pie(meal_pref, year)

    @app.callback(Output("park_hist", "figure"), [Input("year", "value")])
    def update_hist(year):
        return charts.park_hist(year)
