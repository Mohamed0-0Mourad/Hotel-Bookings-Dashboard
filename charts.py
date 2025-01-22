import pandas as pd
from preproccessing import del_outliers
import plotly.express as px

df = pd.read_csv("hotel_bookings.csv")

def month_numeric(month, to:bool = True):
    con = {"January":1, "February":2, "March":3, "April":4, "May":5, "June":6, "July":7, "August":8, "September":9, "October":10, "November":11, "December":12}
    if(to):
        return con[month]
    else: 
        rev = dict(zip(con.values(), con.keys()))
        return rev[month]

canc = df[df['is_canceled'] == 1]
def trend_line(year:int):
    canceled = canc[df['arrival_date_year'] == year]
    canceled = canceled.groupby("arrival_date_month")['is_canceled'].value_counts().reset_index()
    canceled['numeric_month'] = canceled['arrival_date_month'].apply(month_numeric)
    canceled.sort_values("numeric_month", inplace=True)
    trend = px.line(canceled, 
    "arrival_date_month", "count", hover_name="count",
    color_discrete_sequence= ['#FEA98A'])
    trend.update_xaxes(dtick = 1)
    trend.update_layout(dict(
        paper_bgcolor="#F0F0D7", title = "Cancels Trend", xaxis_title = "Arrival Month", yaxis_title="Cancels"
        ,plot_bgcolor= "#F0F0D7"
    ))
    trend.update_traces(line=dict(width=4))
    # print(canceled) 
    # trend=px.bar(canceled,
    # facet_col="arrival_date_year", x = "arrival_date_month", y="is_canceled", 
    # color= "is_canceled", color_continuous_scale=px.colors.sequential.Reds,
    # )
    # trend.show()
    return trend

def lead_table():
    df['lead_time'] = del_outliers(df['lead_time'])
    lead = df.groupby("hotel")['lead_time'].mean()
    hotel_t = lead.iloc[0]
    resort_t = lead.iloc[1]
    return hotel_t, resort_t

def spVsCanc_scatter():
    sp = canc.groupby("total_of_special_requests")['is_canceled'].value_counts().reset_index()

    sc = px.line(sp, "total_of_special_requests", "count", 
                 color_discrete_sequence=["#FEA98A"], markers = 1, hover_name="count"
                )
    
    sc.update_layout({
        "title": "Total canceled customers and thier number of special requests",
        "xaxis_title": "No. Special Requests",
        "yaxis_title": "Canceled Customers", "paper_bgcolor":"#F0F0D7","plot_bgcolor": "#F0F0D7"
    })
    sc.update_traces(marker=dict(symbol="x", size=15, color="#FEA98A"),line=dict(width=4)) 
    return sc

def cancel_table():
    drpd_canc = canc.dropna(subset="children")
    tot = drpd_canc.shape[0]
    rep = drpd_canc.groupby("is_canceled")['is_repeated_guest'].value_counts()
    rep_perc = 100 * rep[1,1] / tot
    childs = drpd_canc.groupby("is_canceled")['children'].value_counts()
    child_perc = 100-(100*childs[1,float(0)]/tot)
    ftot = format(tot, ',')
    return ftot, rep_perc, child_perc

def marketVsCanc_bar(year):
    mar = canc[canc['arrival_date_year'] == year]
    mar = mar.groupby("is_canceled")['market_segment'].value_counts().sort_values(ascending=1).reset_index()

    g = px.bar(mar, 'count', 'market_segment', 
        orientation='h', color_discrete_sequence=["#FEA98A"], hover_name= "count"
        )
    
    g.update_layout(dict(
        title = "Market Segments Contribution to Cancelations",
        xaxis_title = "Cancelations", 
        yaxis_title= "Market Segments", paper_bgcolor="#F0F0D7",plot_bgcolor= "#F0F0D7"
    ))
    return g 

def room_bar(assigned_reserved:str, year:int):
    cnt = df.groupby("arrival_date_year")[f"{assigned_reserved}_room_type"].value_counts().sort_values(ascending=1)
    cnt = cnt[year].reset_index()

    g= px.bar(cnt, "count",f"{assigned_reserved}_room_type",
           orientation='h', color_discrete_sequence=["#FEA98A"], hover_name="count"
           )
    g.update_layout(dict(
        title = f"Most frequently {assigned_reserved} room types",
        xaxis_title = f"{assigned_reserved.capitalize()} Count",
        yaxis_title = "Room Type", paper_bgcolor="#F0F0D7",plot_bgcolor= "#F0F0D7"
    ))
    return g

countries = df.dropna(subset="country")
def country_pie(meal:str, year):
    m = countries[countries['meal'] == meal]
    m = m.groupby(["arrival_date_year"])['country'].value_counts().sort_values(ascending=0)
    m = m[year].reset_index()

    g = px.pie(m.iloc[:5], "country", "count", hover_name="count"
               ,labels = "country"#,color_discrete_sequence=['green']*10
               , hole= 0.3,color_discrete_sequence=px.colors.qualitative.Pastel1)
    g.update_traces(
        textinfo='label+percent',
        textfont_size=14, textfont_weight='bold'#,rotation = -180
    )
    g.update_layout(dict(title = "Meal prefrence across diffrent nationalities", paper_bgcolor="#F0F0D7",plot_bgcolor= "#F0F0D7"))
    # g.show()
    return g

park = df.groupby(["arrival_date_year","customer_type"])['required_car_parking_spaces'].value_counts().sort_values(ascending=0)
def park_hist(year:int):
    p = park[year].reset_index()
    hist=px.histogram(p,'required_car_parking_spaces', "count", 
                 nbins=p["required_car_parking_spaces"].shape[0]
                 , facet_col="customer_type", color_discrete_sequence=["#FEA98A"]
                 ,facet_col_spacing=0.0, hover_name="count"
                 )
    hist.for_each_xaxis(lambda axis: axis.update(title=None))
    hist.for_each_yaxis(lambda axis: axis.update(title=None))
    hist.for_each_annotation(lambda a: a.update(text=a.text.split('=')[-1]))
    hist.update_layout(dict(
        title = "Requiered parking lots distribution per cutomer type",
        xaxis_title="Parking lots per customer", yaxis_title="Count of customers", paper_bgcolor="#F0F0D7"
        ,plot_bgcolor= "#F0F0D7"    
    ))
    # hist.show()
    return hist

if __name__ == "__main__":
    # print(df.info())
    # print(df['meal'].unique())
    # print(df['children'].unique())
    lead_table()
