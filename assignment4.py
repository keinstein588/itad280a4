import os
from flask import Flask, request, redirect, url_for, escape
app = Flask(__name__)

def make_form (errors = {}, data = {}):
    return """<!DOCTYPE html>
<html>

  <head>
    <title>Data Validated</title>
  </head>

  <body>
    <form method="post" \>
        <label> DAY <input type="number" name="day" min = "1" max = "31" value = "{date_data}"/></label><span style = "color:red">{date_message}</span><br>
        <label> MONTH <select name="month" >
          <option value = "Jan">Jan</option>
          <option value = "Feb">Feb</option>
          <option value = "Mar">Mar</option>
          <option value = "Apr">Apr</option>
          <option value = "May">May</option>
          <option value = "Jun">Jun</option>
          <option value = "Jul">Jul</option>
          <option value = "Aug">Aug</option>
          <option value = "Sep">Sep</option>
          <option value = "Oct">Oct</option>
          <option value = "Nov">Nov</option>
          <option value = "Dec">Dec</option>
        </label></select><span style = "color:red">{month_message}</span><br>
        <label> YEAR <input type="number" name="year" min = "1900" max = "2016" value = "{year_data}"/> </label><span style = "color:red">{year_message}</span><br>
        <input type="submit">
</form>
  </body>

</html>""".format(date_message=errors.get("Day",""), month_message=errors.get("Month", ""),year_message=errors.get("Year", ""),
               date_data=escape(data.get("day","")), year_data=escape(data.get("year", "")))

@app.route('/', methods = ["GET", "POST"])
def bday_enter():
    if request.method == "GET":
        form_html = make_form()
        resp = app.make_response(form_html)
        resp.mimetype = "text/html"
        return resp
    else:
        error = False
        messages = {'Day': "", 'Month':"", 'Year':""}
        if int(request.form['day']) < 0 or int(request.form['day']) > 31:
            error = True
            messages['Day'] = "Day must be between 1 and 31"

        if not request.form['month'] in ("Jan", "Feb", "Mar", "Apr", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"):
            error = True
            messages['Month']="Month must be the first three letters of the Month name"

        if int(request.form['year']) < 1900 or int(request.form['year']) > 2016:
            error = True
            messages['Year']="Year must be between 1900 and 2016"

        if error:
            resp = app.make_response(make_form(messages, request.form))
            return resp

        else:
            return redirect(url_for('success'))


@app.route('/success') 
def success():     
    return """<!DOCTYPE html>
<html>

  <head>
    <title>Data Validated</title>
  </head>

  <body>
    <h1>Thanks for entering a valid Brithday!</h1>
  </body>

</html>
"""


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host = '0.0.0.0', port = port)