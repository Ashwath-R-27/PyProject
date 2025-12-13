from flask import Flask, request, render_template, jsonify
import csv

app = Flask(__name__)

@app.route('/login')
def login():
    return render_template('stafflogin.html')

@app.route('/adminlogin')
def index():
    return render_template('adminlogin.html')

@app.route('/home', methods=['POST'])
def adlogverify():
    un = str(request.form['un'])
    pwd = request.form['pwd']
    if un=="PSG":
        if pwd=='123':
            return render_template('home.html')
        else:
            result='password'
            return render_template('adminlogin.html',result=result)
    else:
        result='username'
        return render_template('adminlogin.html',result=result)

@app.route('/dashboard', methods=['POST'])
def logverify():
    un = str(request.form['un'])
    pwd = request.form['pwd']
    filename = "employeedetails.csv"
    with open(filename, "r", newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader)  # To skip the header row
        for row in reader:
            if row[0]==un:
                if row[1]==pwd:
                    return render_template('dashboard.html',name=row[2],id=row[0])
                else:
                    return render_template('stafflogin.html',result="passcode")
        else:
            return render_template('stafflogin.html',result="Staff ID")

sou=0
star=0
bir=0
grav=0
rice=0
drink=0
dessert=0

@app.route('/home/menu')
def menu():
    soup=[]
    starters=[]
    biryani=[]
    gravy=[]
    rice_noodles=[]
    drinks=[]
    desserts=[]
    filename = "menu.csv"
    with open(filename, "r", newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader)  # To skip the header row
        for row in reader:
            if row[4]=='Starters':
                starters.append(row)
            elif row[4]=='Biryani':
                biryani.append(row)
            elif row[4]=='Gravy':
                gravy.append(row)
            elif row[4]=='Rice/Noodles':
                rice_noodles.append(row)
            elif row[4]=='Soup':
                soup.append(row)
            elif row[4]=='Drinks':
                drinks.append(row)
            elif row[4]=='Desserts':
                desserts.append(row)
    return render_template('menu.html',soup=soup,starters=starters,biryani=biryani,gravy=gravy,rice_noodles=rice_noodles,drinks=drinks,desserts=desserts)

@app.route('/home/menu/additem')
def additem():
    return render_template('additem.html')

@app.route('/home/menu/additem/submited', methods=['POST'])
def aditem():
    course=str(request.form['course'])
    name=str(request.form['dishname'])
    category=str(request.form['category'])
    price=int(request.form['price'])
    filename = "menu.csv"
    data=[]
    data.extend([name,category,price,course])
    if course=='Soup':
        global sou
        sou+=1
        data.insert(0,sou)
    elif course=='Starters':
        global star
        star+=1
        data.insert(0,star)
    elif course=='Biryani':
        global bir
        bir+=1
        data.insert(0,bir)
    elif course=='Gravy':
        global grav
        grav+=1
        data.insert(0,grav)
    elif course=='Rice/Noodles':
        global rice
        rice+=1
        data.insert(0,rice)
    elif course=='Drinks':
        global drink
        drink+=1
        data.insert(0,drink)
    else:
        global dessert
        dessert+=1
        data.insert(0,dessert)
    with open(filename, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)
    return render_template('additem.html',result='Successfully added')

@app.route('/home/accounts')
def accounts():
    return render_template('accounts.html')

@app.route('/dashboard/orders')
def orderpg():
    return render_template('orderspg.html')

@app.route('/dashboard/orders/neworder')
def billing():
    records=[]
    filename = "menu.csv"
    with open(filename, "r", newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader)  # To skip the header row
        for row in reader:
            records.append(row)
    return render_template('billing.html',records=records)

@app.route('/preview', methods=['POST'])
def preview():
    order = request.form.getlist('dish')
    if order==[]:
        return render_template('billing.html',value='Please Select any one Dish')
    else:
        filename = "menu.csv"
        with open(filename, "r", newline='', encoding="utf-8") as file:
            orders=[]
            sno=1
            reader = csv.reader(file)
            header = next(reader)  # To skip the header row
            for row in reader:
                if row[0] in order:
                    name=row[1]
                    code=row[0]
                    price=row[3]
                    item=[]
                    item.extend([sno,code,name,price])
                    orders.append(item)
                    sno+=1
        return render_template('orderpreview.html',items=orders)

@app.route('/submitted', methods=['POST'])
def preview_submit():
    filename='orders.csv'
    tbl_no=int(request.form['tbl_num'])
    customer_mobile=str(request.form['customer_mobile_no'])
    for key in request.form:
        if key.startswith("qty_"):
            code=key.replace("qty_","")
            qty=int(request.form[key])
            name=request.form[f'name_{code}']
            price=float(request.form[f'price_{code}'])
            total_price=qty*price
            dish=[]
            dish.extend([tbl_no,code,name,price,qty,total_price])
            with open(filename, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(dish)
    return render_template('orderpreview.html',status="Order Created Successfully")

@app.route('/dashboard/orders/existingorders')
def existingorderpg():
    table=[]
    filename='orders.csv'
    with open(filename, "r", newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader)  # To skip the header row
        for row in reader:
            if int(row[0]) not in table:
                table.append(int(row[0]))
    table.sort()
    return render_template('existingorders.html',tables=table)    

if __name__ == '__main__':
    app.run(debug=True)