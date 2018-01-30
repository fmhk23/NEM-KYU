import binascii
import configparser
import datetime
import calendar
import json
import math
import requests
import pandas as pd
from bokeh.embed import components
from bokeh.plotting import figure
from collections import namedtuple
from flask import Flask, flash, render_template, request, redirect, session, url_for
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from flask.ext.misaka import Misaka
from functools import partial

app = Flask(__name__)
Bootstrap(app)
datepicker(app)
Misaka(app)

inifile = configparser.ConfigParser()
inifile.read("./config.ini")

app.secret_key = inifile.get("app", "secret")

timestamp_nem = datetime.datetime.now() - datetime.datetime(2015, 3, 29, 0, 6, 25)
timestamp_nem = timestamp_nem.total_seconds()
timestamp_nem = int(timestamp_nem)
timestamp_nem_deadline = timestamp_nem + 3600

RPA = {
    "transaction":
    {
        "timeStamp": timestamp_nem,
        "amount": 1000000, # 1000000 = one time.
        "fee": 300000,   # 0.2 xems
        "recipient": inifile.get("company_info", "address"),
        "type": 257,
        "deadline": timestamp_nem_deadline,
        "message":
        {
            "payload": "",
            "type": 1
        },
        "version": -1744830462,
        "signer": inifile.get("employee_info", "signer"),
        "mosaics":
        [{
            "mosaicId":
            {
                "namespaceId": inifile.get("mosaic", "namespace"),
                "name": inifile.get("mosaic", "mosaic")
            },
            "quantity": 1
        }]
    },
    "privateKey": inifile.get("employee_info", "privatekey")
}

SN = 'http://127.0.0.1:7890'

# Read description markdown
content = ""
with open("./doc/description.md", "r") as f:
  content = f.read()

def get_transactions(req):
    transactions = requests.get(req).content
    transactions = json.loads(transactions)
    transactions = transactions["data"]

    return transactions

# Retrieve transactions which include designated Namespace:mosaic.
def check_mosaic(t):
    t = t["transaction"]
    if "mosaics" in t:
        return True
    else:
        return False

# return mosaic data table from mosaic transactions
def generate_table(x):
    df = pd.DataFrame(columns = ["id","time","namespace","mosaic","quantity","message","signer"])
    
    for i in x:
        
        mosaics = i["transaction"]["mosaics"]
        time = i["transaction"]["timeStamp"]
        signer = i["transaction"]["signer"]
        metaid = i["meta"]["id"]

        try:
            message = i["transaction"]["message"]["payload"]
            message = binascii.unhexlify(message)
        except:
            message = ""

        for j in mosaics:
            namespace = j["mosaicId"]["namespaceId"]
            mosaic = j["mosaicId"]["name"]
            quantity = j["quantity"]
            
            series = pd.Series([metaid, time, namespace, mosaic, quantity, message, signer], index = df.columns)
            df = df.append(series, ignore_index = True)

    return df
        
def get_mosaic_definition(x):
    df = pd.DataFrame(columns = ["namespace", "mosaic", "supply"])
    
    for i in x:
        namespace = i["id"]["namespaceId"]
        name = i["id"]["name"]
        supply = i["properties"][1]["value"]

        series = pd.Series([namespace, name, supply], index = df.columns)
        df = df.append(series, ignore_index = True)

    return df

# Flask Apps
@app.route('/')
def description():
    return render_template("description.html", text = content)

@app.route('/apply_holiday', methods = ['GET', 'POST'])
def apply_holiday():
    addr = inifile.get("employee_info", "address")
    req = SN + '/account/mosaic/owned?address=' + addr
    balance =requests.get(req).content
    balance = json.loads(balance) #json-> dict
    balance = balance['data']
    remained_holidays = [i['quantity'] for i in balance if i['mosaicId']['namespaceId'] == 'company_a' and i['mosaicId']['name'] == 'holiday2018'][0]
    remained_holidays = str(remained_holidays)
    
    remained_xem = [i['quantity'] for i in balance if i['mosaicId']['namespaceId'] == 'nem' and i['mosaicId']['name'] == 'xem'][0]
    remained_xem = remained_xem * 0.000001
    remained_xem = "{0:.3f}".format(remained_xem)

    if request.method == 'POST':
        # Update Message
        date = request.form['datepicker']

        if date == "":
            flash("Error: Select the date!", "status")
            return redirect(url_for("apply_holiday"))

        try:
            date_ja = date[6:10] + "-" + date[0:2] + "-" + date[3:5]
            date_byte = binascii.hexlify(date_ja.encode('utf-8'))
            date_hex = str(date_byte)
            date_hex = date_hex[2:-1]
        except:
            flash("Error: Select the date!", "status")
            return render_template('index.html', holidays =remained_holidays)

        RPA["transaction"]["message"]["payload"] = date_hex

        # Update Time
        timestamp_nem = datetime.datetime.now() - datetime.datetime(2015, 3, 29, 0, 6, 25)
        timestamp_nem = timestamp_nem.total_seconds()
        timestamp_nem = int(timestamp_nem)
        timestamp_nem_deadline = timestamp_nem + 3600
        
        RPA["transaction"]["timeStamp"] = timestamp_nem
        RPA["transaction"]["deadline"] = timestamp_nem_deadline
        
        # Create Transaction request
        req = SN + '/transaction/prepare-announce'
        responce = requests.post(req, json = RPA)

        if responce.status_code == 200:
            flash("You have applied the holiday successfully!", "status")
        else:
            flash("Error: Something happened while generating transaction.", "status")

        return redirect(url_for('apply_holiday'))
    else:
        return render_template('index.html', holidays = remained_holidays, xem = remained_xem) 

@app.route('/dashboard', methods = ['GET','POST'])
def dashboard():
    # Determine which namespace
    feature_namespace = request.args.get("namespace")
    if feature_namespace == None:
        feature_namespace = "company_a"
    # Determine which mosaic
    feature_mosaic = request.args.get("mosaic")
    if feature_mosaic == None:
        feature_mosaic = "holiday2018"

    feature_space_mosaic = feature_namespace + "-" + feature_mosaic
    # Determine which address(company)
    company = request.args.get("address")
    if company == None:
        company = 'TCJ2QE7WZQLYWAF5EKEY2H3T57A2NP54W7HBSN5L'
    
    # Generate income mosaic pandas table from transactions.
    req = SN + '/account/transfers/incoming?address=' + company # + '&pageSize=100'
    
    incomes = get_transactions(req)
    incomes_len = len(incomes)
    
    mosaic_incomes = filter(check_mosaic, incomes)
    mosaic_incomes = list(mosaic_incomes)

    df = generate_table(mosaic_incomes)
    
    # Retrieve income mosaic transactions.
    begin = datetime.datetime(2018, 1, 10, 0, 0, 0) - datetime.datetime(2015, 3, 29, 0, 6, 25)
    begin = begin.total_seconds()
    begin = int(begin)
    
    while True:
        if incomes_len == 25:
            try:
                oldest_transaction_time = mosaic_incomes[-1]["transaction"]["timeStamp"]
                oldest_transaction_id = mosaic_incomes[-1]["meta"]["id"]
                if oldest_transaction_time > begin:
                    req = req + "&id=" + str(oldest_transaction_id)
                    # Duplicated with former: Need to review
                    incomes = get_transactions(req)
                    incomes_len = len(incomes)
                    mosaic_incomes = filter(check_mosaic, incomes)
                    mosaic_incomes = list(mosaic_incomes)
                    additional_df = generate_table(mosaic_incomes)
                    df = df.append(additional_df, ignore_index = True)
            except:
                break
        else:
            break
    df["space_mosaic"] = df["namespace"] + "-" + df["mosaic"]
    
    # Get Mosaic Definitions
    req_mosaics = SN + "/account/mosaic/definition/page?address=" + company
    mosaic_def = requests.get(req_mosaics).content
    mosaic_def = json.loads(mosaic_def)
    mosaic_def = mosaic_def["data"]
    
    mosaic_table = get_mosaic_definition(mosaic_def)
    mosaic_table["space_mosaic"] = mosaic_table["namespace"] + "-" + mosaic_table["mosaic"]
    
    # Calculate paid-holiday%
    send_sum = df.groupby("space_mosaic")["quantity"].sum()
    send_sum_table = pd.DataFrame({"space_mosaic":send_sum.index, "received_sum":send_sum.values})
    
    mosaic_table = pd.merge(mosaic_table, send_sum_table, on = "space_mosaic")
    
    mosaic_table_figure = mosaic_table[mosaic_table.space_mosaic == feature_space_mosaic]
    offered_percent = mosaic_table_figure.received_sum.values / int(mosaic_table_figure.supply.values)
    
    # Generate plot.
    p = figure(
        title="Requested paid holiday ratio", 
        x_axis_label='x', 
        y_axis_label='y',
        y_axis_type="linear"
    )
    
    Data = namedtuple('Data', ('name', 'value', 'color'))
    rates = [Data("Requested", offered_percent , "#7FC97F"), Data("Not Requested", 1 - offered_percent, "#DD1C77")]
    
    start_angle = 0

    for rate in rates:
        p.annular_wedge(
            x=0, 
            y=0,
            inner_radius=0.2, 
            outer_radius=0.5, 
            start_angle=math.pi * 2 * start_angle, 
            end_angle=math.pi * 2 * (start_angle + rate.value),
            color=rate.color,
            legend=rate.name
        )
        start_angle += rate.value
    
    script, div = components(p)
    selected_namespace = mosaic_table_figure.namespace.values[0]
    selected_mosaic = mosaic_table_figure.mosaic.values[0]
    
    return render_template('dashboard.html',
        t = script, r = div,
        selected_namespace = selected_namespace, selected_mosaic = selected_mosaic,
        mosaics = list(mosaic_table[mosaic_table.namespace == selected_namespace].mosaic),
        address = company, df = mosaic_table_figure.to_html()
        )

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
