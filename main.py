# import charts
from layouts.home_layout import get_layout
from dash import Dash
from callbacks.update_home import register_callbacks

external_css = ["https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css","https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css"]

def main():
    print("Running...")
    app = Dash(__name__, external_stylesheets=external_css)
    app.layout = get_layout()
    register_callbacks(app)
    app.run(debug=True)
    # charts.trend_line(2016)
    # charts.lead_table()
    # charts.spVsCanc_scatter()
    # charts.repeated_table()
    # charts.marketVsCanc_bar(2016)
    # charts.room_bar('reserved', 2016)
    # charts.country_pie("BB", 2016)
    # charts.park_hist(2016)

if __name__ == "__main__":
    main()