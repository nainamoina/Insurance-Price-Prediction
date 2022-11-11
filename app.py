from flask import Flask, render_template, request, jsonify, redirect
from flask_sqlalchemy import SQLAlchemy
import pickle
import numpy as np
import sklearn
import os
currentdirectory = os.path.dirname(os.path.abspath(__file__))

app = Flask("__name__")
model = pickle.load(open('finalized_model.pickle', 'rb'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Nainamoina@localhost/flasksql'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app) #SQLAlchemy is a library that facilitates the communication between Python programs and databases

# Create a table named Insurance with columns 
class Insurance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(80), nullable=False)
    LastName = db.Column(db.String(80), nullable=False)
    Age = db.Column(db.String(80), nullable=False)
    Email = db.Column(db.String(80), nullable=False)
    Gender = db.Column(db.String(80), nullable=False)
    BMI = db.Column(db.String(80), nullable=False)
    Children = db.Column(db.String(80), nullable=False)
    Smoker = db.Column(db.String(80), nullable=False)
    Region = db.Column(db.String(80), nullable=False)
    Insurance_Price = db.Column(db.String(80), nullable=False)



    def __init__(self, FirstName, LastName,Age,Email,Gender,BMI,Children,Smoker,Region,Insurance_Price):
        self.FirstName = FirstName
        self.LastName = LastName
        self.Age = Age
        self.Email = Email
        self.Gender = Gender
        self.BMI = BMI
        self.Children = Children
        self.Smoker = Smoker
        self.Region = Region
        self.Insurance_Price = Insurance_Price

        def __repr__(self):
            return 'User %r' % self.FirstName

def numberFormat(value):
    return format(int(value), ',d')
# App Routing means mapping the URLs to a specific function that will handle the logic for that URL
@app.route('/',methods=['GET'])
def Home():
    return render_template("Insurancepriceprediction.html")

@app.route("/", methods = ['GET','POST'])
def main():
    alert_message = False
    success_message = False
    try:
        if request.method == 'POST':
            FirstName = request.form["FirstName"]
            LastName = request.form["LastName"]
            age = int(request.form["Age"])
            Email = request.form["Email"]
            sex = request.form["Gender"]
            if (sex == 'Male'):
                sex = 1
            else:
                sex = 0
            bmi = float(request.form["BMI"])
            children = int(request.form["Children"])
            smoker = request.form["Smoker"]
            if (smoker == 'Yes'):
                smoker = 1
            else:
                smoker = 0
            region = request.form["Region"]
            if (region == "Southwest"):
                region = 3
            elif(region == "Southeast"):
                region = 2
            elif(region == "Northwest"):
                region = 1
            else:
                region = 0
            test = [[age,bmi,smoker,children,region,sex]]
            if bmi < 100:

                prediction = model.predict(test)

                if prediction < 0:
                    alert_message = "Please enter relevant information."
                else:
                    success_message = f'Predicted Insurance Price : $ {numberFormat(prediction[0])}'
                Insurance_Price = prediction[0]

                entry = Insurance(FirstName,LastName,age,Email,sex,bmi,children,smoker,region,Insurance_Price)

                db.session.add(entry)
                db.session.commit()
            else:
                 alert_message = "Please enter relevant information."
    except:
        alert_message = "Please enter relevant information."
    return render_template('Insurancepriceprediction.html',alert_message = alert_message,success_message = success_message)


if __name__ == '__main__':
    db.create_all()
    app.run()

    