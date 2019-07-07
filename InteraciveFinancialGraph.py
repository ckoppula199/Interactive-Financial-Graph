from pandas_datareader import data
import datetime
from bokeh.plotting import figure, show, output_file
import sys

company_code = input("Enter Company Code: ")

start = datetime.datetime(2019, 4, 1)
end = datetime.datetime(2019, 7, 1)
df = None

try:
    df = data.DataReader(name=company_code, data_source="yahoo", start=start, end=end)
except:
    print("No such company with code: " + company_code)
    sys.exit("Bad Company Code")

def inc_dec(close, open_):
    if close > open_:
        value = "Increase"
    elif close < open_:
        value = "Decrease"
    else:
        value = "Equal"
    return value

df["Status"] = [inc_dec(close, open_) for close, open_ in zip(df.Close, df.Open)]

df["Middle"] = (df.Open + df.Close)/2
df["Height"] = abs(df.Open - df.Close)
df

p=figure(x_axis_type='datetime', width=1000, height=300, sizing_mode="scale_width")
p.title.text = "Stock Price History: " + company_code
p.grid.grid_line_alpha=0.5

hours_12 = 12*60*60*1000

p.segment(df.index, df.High, df.index, df.Low, color="black")

p.rect(df.index[df.Status == "Increase"], df.Middle[df.Status == "Increase"],
       width=hours_12, height=df.Height[df.Status == "Increase"], fill_color="#CCFF99", line_color="black")

p.rect(df.index[df.Status == "Decrease"], df.Middle[df.Status == "Decrease"],
       width=hours_12, height=df.Height[df.Status == "Decrease"], fill_color="#FF3300", line_color="black")

output_file("cs.html")
show(p)
