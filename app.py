from flask import Flask, request, render_template, redirect
from flask.helpers import url_for
from flask import json
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def home():
    job = request.form.get("job")
    province = request.form.get("province")
    if job == "" or job == None:
        return render_template("index.html")
    if province == "" or province == None:
        return render_template("index.html")
    else:
        return render_template("next.html",salary=json.dumps(salary(job, province)))


def salary(job,provinceincanada):
    careerandtag=[("Mechanical Engineer", 2757), ("Electrical Engineer", 17815), ("Civil Engineer",22376), ("Computer Engineer", 2866),
    ("Family Physician",24431), ("Specialist Physician",4049),("Software Engineer", 5485),("Pharmacist",18196),("Architect",17867),
    ("Chef",16420),("Financial Analyst", 12417),("Highschool Teacher", 15904), ("Elementary teacher", 2205), ("Professor", 4643),
    ("Plumber", 4747),("Welder", 23242),("Hairstylist", 16452),("Lawyer",15815),("Accountant",113)]
    for tuples in careerandtag:
        if tuples[0]==job:
            number=tuples[1]
    if not number:
        return("We failed :(", [0,0,0])
    string="https://www.jobbank.gc.ca/wagereport/occupation/" + str(number)
    r=requests.get(string)
    soup = BeautifulSoup(r.text,"html.parser")
    provincetags=[]
    officialprovinces=[]
    wage=[]
    actualwage=[]
    hourlywage=False
    for province in soup.find_all("tr",{"class":"areaGroup province prov"}):
        for wages in province.find_all("td"):
            actualwages=wages.text
            wage.append(actualwages)
        for province_name in province.find_all("strong"):
            province_name2=province_name.text
            provincetags.append(province_name2)
    for provinces in provincetags:
        provinces=str(provinces)
        officialprovinces.append(provinces)
    for salary in wage:
        salary=str(salary)
        if salary.find('.'):
            hourlywage=True
            salary=salary.strip()
        actualwage.append(salary)
    actual_wages=[actualwage[i:i+3] for i in range(0, len(actualwage), 3)]
    newdict=dict(zip(officialprovinces,actual_wages))
    for key in newdict:
        if key==provinceincanada:
            salaries=newdict[key]
    annualSalaryList = []
    for i in range(0, 3):
        sal = salaries[i]

        if sal == 'N/A':
            return([0,0,0])

        sal = float(sal)
        if sal < 1000:
            sal=int(sal*40*50)
            annualSalaryList.append(sal)
    return(annualSalaryList)

if __name__ == "__main__":
    app.run()