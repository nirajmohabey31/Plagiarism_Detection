from flask import Flask, render_template, redirect, request
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired
import re
import pandas as pd
import math

app = Flask(__name__)
app.config['SECRET_KEY'] = '827e763e55e41e32381c13afc4338d5f'

class PlagForm(FlaskForm):
    checkText = TextAreaField('Enter your text here', validators=[DataRequired()])
    submit = SubmitField('Submit')

q = "" 

@app.route('/', methods=['GET', 'POST'])
def index():
    form = PlagForm()
    if form.validate_on_submit():
        universalSetOfUniqueWords = []
        matchPercentage = 0
        lowercaseQuery = form.checkText.data.lower()

        queryWordList = re.sub("[^\w]", " ", lowercaseQuery).split()
        for word in queryWordList:
            if word not in universalSetOfUniqueWords:
                universalSetOfUniqueWords.append(word)

        fd = pd.read_csv("C:/Users/niraj/Plag/data/file_information.csv", "r")
        database1 = fd.read().lower()

        databaseWordList = re.sub("[^\w]", " ", database1).split()
        for word in databaseWordList:
            if word not in universalSetOfUniqueWords:
                universalSetOfUniqueWords.append(word)

        queryTF = []
        databaseTF = []

        for word in universalSetOfUniqueWords:
            queryTfCounter = 0
            databaseTfCounter = 0

            for word2 in queryWordList:
                if word == word2:
                    queryTfCounter += 1
            queryTF.append(queryTfCounter)

            for word2 in databaseWordList:
                if word == word2:
                    databaseTfCounter += 1
            databaseTF.append(databaseTfCounter)

        dotProduct = 0
        for i in range(len(queryTF)):
            dotProduct += queryTF[i] * databaseTF[i]

        queryVectorMagnitude = 0
        for i in range(len(queryTF)):
            queryVectorMagnitude += queryTF[i] ** 2
        queryVectorMagnitude = math.sqrt(queryVectorMagnitude)

        databaseVectorMagnitude = 0
        for i in range(len(databaseTF)):
            databaseVectorMagnitude += databaseTF[i] ** 2
        databaseVectorMagnitude = math.sqrt(databaseVectorMagnitude)
        
        lowercaseQuery = form.checkText.data.lower()

        matchPercentage = (float)(dotProduct / (queryVectorMagnitude * databaseVectorMagnitude)) * 100

        output = "Input query text matches %0.02f%% with database." % matchPercentage
        
        
        
        return redirect('results?query={}&output={}'.format(lowercaseQuery, output))

    return render_template('index.html', form=form)


@app.route('/results')
def results():
	lowercaseQuery = request.args.get('query')
	ans = Requests_ex.main_function(lowercaseQuery)
	return render_template('results.html', output=output, ans=ans)

app.run()