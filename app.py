from flask import Flask, render_template, request
import os 
import numpy as np
import pandas as pd
from src.CREDIT_UTILITY.pipeline.prediction import PredictionPipeline

app = Flask(__name__) # initializing a flask app

@app.route('/',methods=['GET'])  # route to display the home page
def homePage():
    return render_template("index.html")


@app.route('/train',methods=['GET'])  # route to train the pipeline
def training():
    os.system("python main.py")
    return "Training Successful!" 


@app.route('/predict',methods=['POST','GET']) # route to show the predictions in a web UI
def index():
    if request.method == 'POST':
        try:
            #  reading the inputs given by the user
            NumDots=int(request.form['NumDots'])
            SubdomainLevel=int(request.form['SubdomainLevel'])
            PathLevel=int(request.form['PathLevel'])
            UrlLength=int(request.form['UrlLengt'])
            NumDash=int(request.form['NumDash'])
            NumDashInHostname=int(request.form['NumDashInHostname'])
            AtSymbol=int(request.form['AtSymbol'])
            TildeSymbol=int(request.form['TildeSymbol'])
            NumUnderscore=int(request.form['NumUnderscore'])
            NumPercent=int(request.form['NumPercent'])
            NumQueryComponents=int(request.form['NumQueryComponents'])
            NumAmpersand=int(request.form['NumAmpersand'])
            NumHash=int(request.form['NumHash'])
            NumNumericChars=int(request.form['NumNumericChars'])
            NoHttps=int(request.form['NoHttps'])
            RandomString=int(request.form['RandomString'])
            IpAddress=int(request.form['IpAddress'])
            DomainInSubdomains=int(request.form['DomainInSubdomain'])
            DomainInPaths=int(request.form['DomainInPaths'])
            HttpsInHostname=int(request.form['HttpsInHostname'])
            HostnameLength=int(request.form['HostnameLength'])
            PathLength=int(request.form['PathLength'])
            QueryLength=int(request.form['QueryLength'])
            DoubleSlashInPath=int(request.form['DoubleSlashInPath'])
            NumSensitiveWords=int(request.form['NumSensitiveWords'])
            EmbeddedBrandName=int(request.form['EmbeddedBrandName'])
            PctExtHyperlinks=int(request.form['PctExtHyperlinks'])
            PctExtResourceUrls=int(request.form['PctExtResourceUrls'])
            ExtFavicon=int(request.form['ExtFavicon'])
            InsecureForms=int(request.form['InsecureForms'])
            RelativeFormAction=int(request.form['RelativeFormAction'])
            ExtFormAction=int(request.form['ExtFormAction'])
            AbnormalFormAction=int(request.form['AbnormalFormAction'])
            PctNullSelfRedirectHyperlinks=int(request.form['PctNullSelfRedirectHyperlinks'])
            FrequentDomainNameMismatch=int(request.form['FrequentDomainNameMismatch'])
            FakeLinkInStatusBar=int(request.form['FakeLinkInStatusBar'])
            RightClickDisabled=int(request.form['RightClickDisabled'])
            PopUpWindow=int(request.form['PopUpWindow'])
            SubmitInfoToEmail=int(request.form['SubmitInfoToEmail'])
            IframeOrFrame=int(request.form['IframeOrFrame'])
            MissingTitle=int(request.form['MissingTitle'])
            ImagesOnlyInForm=int(request.form['ImagesOnlyInForm'])
            SubdomainLevelRT=int(request.form['SubdomainLevelRT'])
            UrlLengthRT=int(request.form['UrlLengthRT'])
            PctExtResourceUrlsRT=int(request.form['PctExtResourceUrlsRT'])
            AbnormalExtFormActionR=int(request.form['AbnormalExtFormActionR'])
            ExtMetaScriptLinkRT=int(request.form['ExtMetaScriptLinkRT'])
            PctExtNullSelfRedirectHyperlinksRT=int(request.form['PctExtNullSelfRedirectHyperlinksRT'])

            data = [NumDots,SubdomainLevel,PathLevel,UrlLength,NumDash,NumDashInHostname,AtSymbol,TildeSymbol,NumUnderscore,NumPercent,NumQueryComponents,NumAmpersand,NumHash,NumNumericChars,NoHttps,RandomString,IpAddress,DomainInSubdomains,DomainInPaths,HttpsInHostname,HostnameLength,PathLength,QueryLength,DoubleSlashInPath,NumSensitiveWords,EmbeddedBrandName,PctExtHyperlinks,PctExtResourceUrls,ExtFavicon,InsecureForms,RelativeFormAction,ExtFormAction,AbnormalFormAction,PctNullSelfRedirectHyperlinks,FrequentDomainNameMismatch,FakeLinkInStatusBar,RightClickDisabled,PopUpWindow,SubmitInfoToEmail,IframeOrFrame,MissingTitle,ImagesOnlyInForm,SubdomainLevelRT,UrlLengthRT,PctExtResourceUrlsRT,AbnormalExtFormActionR,ExtMetaScriptLinkRT,PctExtNullSelfRedirectHyperlinksRT]
            data = np.array(data).reshape(1, 48)
            
            print("Before Prediction")

            obj = PredictionPipeline()
            predict = obj.predict(data)

            return render_template('results.html', prediction = str(predict))

        except Exception as e:
            print('The Exception message is: ',e)
            return 'something is wrong'

    else:
        return render_template('index.html')


if __name__ == "__main__":
	# app.run(host="0.0.0.0", port = 8080, debug=True)
	app.run(host="0.0.0.0", port = 8080)