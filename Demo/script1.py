from flask import Flask, render_template
from pandas_datareader import data
import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from bokeh.resources import CDN

app = Flask(__name__)

@app.route('/')
def home():
    today = date.today()
    oneYearAgo = today - relativedelta(years=1 )
    ticker = "AAPL"

    start=datetime.datetime(2018, 10, 15)
    end=today

    df = data.DataReader(name=ticker, data_source="yahoo", start=start, end=end)

    def inc_dec(c,o):
        if c > o:
            value="Increase"
        elif c < o:
            value="Decrease"
        else:
            value="Equal"
        return value

    df["Status"]=[inc_dec(c, o) for c, o in zip(df.Close, df.Open)]
    df["Middle"]=(df.Open+df.Close)/2
    df["Height"]=abs(df.Open-df.Close)

    p = figure(x_axis_type="datetime", width=1000, height=300, sizing_mode='scale_both')
    p.title.text=ticker
    p.grid.grid_line_alpha=0.3

    hours_12 = 12*60*60*1000

    p.segment(df.index, df.High, df.index, df.Low, color="black")

    p.rect(df.index[df.Status=="Increase"], df.Middle[df.Status=="Increase"],
           hours_12, df.Height[df.Status=="Increase"], fill_color="#ABD7B0", line_color="black")

    p.rect(df.index[df.Status=="Decrease"], df.Middle[df.Status=="Decrease"],
           hours_12, df.Height[df.Status=="Decrease"], fill_color="#EB5353", line_color="black")

    script1, div1 = components(p)
    cdn_js=CDN.js_files[0]

    return render_template("home.html",
    script1=script1,
    div1=div1,
    cdn_js=cdn_js)

if __name__ == "__main__":
        app.run(debug=True)
