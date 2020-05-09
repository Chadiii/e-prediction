from datetime import datetime, timedelta
#from pandas import Series, DataFrame, read_csv
import pandas as pd
import pmdarima as pm
import json
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import csv





class Model():
    series = pd.Series()
    allData = pd.DataFrame()
    model = None
    predictions = list()
    params = (2,1,2)
    steps = 7
    predIsLoaded = False

    @classmethod
    def update(cls):
        print('update')
        cls.download()
        cls.fitModel()
    
    @classmethod
    def download(cls):
        print('download')
        def parser(x):
            return datetime.strptime(x, '%m/%d/%y')
        cls.allData = pd.read_csv('dailyGeneral.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)
        cls.series = cls.allData['Cases']

    """
    @classmethod
    def fitModel1(cls):
        if cls.series.empty:
            cls.download()
        val = cls.series.values
        val = val.astype('float32')
        val = [x for x in val]
        # fit model
        cls.model = ARIMA(val, order=cls.params)
        cls.model = cls.model.fit(disp=0)

        #predict
        predictions = cls.model.forecast(steps=cls.steps)[0] 
        lastDate = cls.series.index
        lastDate = lastDate[len(lastDate)-1]
        predList = list()
        som = int(cls.series.sum())
        i = 1
        for pred in predictions:
            som = som + int(round(pred, 0))
            predList.append( {
                'date': (lastDate + timedelta(days=i)).strftime("%Y-%m-%d"),
                'ajout': int(round(pred, 0)),
                'cumul': som,
            })
            i = i + 1
        cls.predictions = predList
        cls.savePredictions()"""
    
    @classmethod
    def fitModel(cls):
        print('fitModel')
        if cls.series.empty:
            cls.download()
        cls.model = pm.auto_arima(cls.series.values, start_p=0, start_q=0,
                      test='adf',       # use adftest to find optimal 'd'
                      max_p=5, max_q=5, # maximum p and q
                      m=1,              # frequency of series
                      d=None,           # let model determine 'd'
                      seasonal=False,   # No Seasonality
                      start_P=0, 
                      D=0, 
                      trace=False,
                      error_action='ignore',  
                      suppress_warnings=True, 
                      stepwise=False)
        cls.makePrediction()
        
    @classmethod
    def makePrediction(cls):
        print('makePrediction')
        if(not cls.predIsLoaded):
            cls.loadPredictions(mode='check')
        #predict
        predictions = cls.model.predict(n_periods=cls.steps, return_conf_int=True)[0]
        lastDate = cls.series.index
        lastDate = lastDate[len(lastDate)-1]
        #predList = list()
        som = int(cls.series.sum())
        i = 1
        for pred in predictions:
            som = som + int(round(pred, 0))
            dic = {
                'date': (lastDate + timedelta(days=i)).strftime("%Y-%m-%d"),
                'ajout': int(round(pred, 0)),
                'cumul': som,
            }
            i = i + 1
            
            found = False
            for j in range(len(cls.predictions)-1, -1, -1):
                if cls.predictions[j]["date"] == dic["date"]:
                    cls.predictions[j] = dic
                    found = True
                    break

            if (not found):
                cls.predictions.append(dic)
                
        cls.addLastObservation()
        #cls.predictions = predList
        cls.savePredictions()
    
    @classmethod
    def addLastObservation(cls):
        #addLastObservation in correspondant prediction dict
        print('addObservation')
        date=cls.series.index[len(cls.series.index)-1].strftime("%Y-%m-%d")
        ajout=int(cls.series.values[len(cls.series.values)-1])
        cumul=int(cls.series.sum())
        for j in range(len(cls.predictions)-1, -1, -1):
            if cls.predictions[j]["date"] == date:
                cls.predictions[j]['obsvAjout'] = ajout
                cls.predictions[j]['obsvCumul'] = cumul
                break

        
    
    @classmethod
    def savePredictions(cls):
        print('savePredictions')
        if(not cls.predIsLoaded):
            cls.loadPredictions(mode='check')
        try:
            jsonObject = json.dumps(cls.predictions, indent=4)
            f = open('predFile.json', 'w')
            f.write(jsonObject)
        finally:
            try:
                f.close()
            except:
                print('error')
            
    
    
    @classmethod
    def loadPredictions(cls, mode='normal'):
        print('loadPredictions mode:{}'.format(mode))
        cls.predIsLoaded = True
        try:
            f = open('predFile.json', 'r')
            cls.predictions = json.load(f)
        except:
            cls.predictions = list()
        finally:
            try:
                f.close()
            except:
                print('error')
        if(len(cls.predictions)==0 and mode=='normal'):
            cls.fitModel()
            
            
    
    """@classmethod
    def getData(cls):
        print('getData')
        if cls.series.empty:
            cls.download()
        dataList = list()
        som = 0
        for i in range(cls.series.size):
            som = som + cls.series.values[i-1]
            dataList.append( {
                'date': cls.series.index[i].strftime("%Y-%m-%d"),
                'ajout': int(cls.series.values[i]),
                'cumul': int(som),
            })

        return dataList"""
    
    
    @classmethod
    def getAllData(cls):
        print('getAllData')
        if cls.allData.empty:
            cls.download()
        dataList = list()
        som = {'cases':0, 'deaths':0, 'recovered':0}
        for i in range(len(cls.allData)):
            som['cases'] = som['cases'] + cls.allData.values[i][0]
            som['deaths'] = som['deaths'] + cls.allData.values[i][1]
            som['recovered'] = som['recovered'] + cls.allData.values[i][2]
            dataList.append({
                'date': cls.allData.index[i].strftime("%Y-%m-%d"),
                'casesAjout': int(cls.allData.values[i][0]),
                'casesCumul': int(som['cases']),
                'deathsAjout': int(cls.allData.values[i][1]),
                'deathsCumul': int(som['deaths']),
                'recoveredAjout': int(cls.allData.values[i][2]),
                'recoveredCumul': int(som['recovered']),
            })
        return dataList



    @classmethod
    def getPredictions(cls):
        print('getPredictions')
        if len(cls.predictions) == 0:
            cls.loadPredictions()
        futurePred = list()
        today = datetime.now().strftime("%Y-%m-%d")
        today = datetime.strptime(today, "%Y-%m-%d")
        for p in cls.predictions:
            end_date = datetime.strptime(p["date"], "%Y-%m-%d")
            if (end_date-today).days >=0:
                futurePred.append(p)
        return futurePred
    
    @classmethod
    def getHistoricalPredictions(cls):
        print('getHistoricalPredictions')
        if len(cls.predictions) == 0:
            cls.loadPredictions()
        data = cls.getAllData()
        historicalPred = list()
        today = datetime.now().strftime("%Y-%m-%d")
        today = datetime.strptime(today, "%Y-%m-%d")
        for j in range(len(cls.predictions)):
            end_date = datetime.strptime(cls.predictions[j]["date"], "%Y-%m-%d")
            if (end_date-today).days <0:
                if len(cls.predictions[j])==3:
                    for d in data[::-1]:
                        if d["date"] == cls.predictions[j]["date"]:
                            cls.predictions[j]['obsvAjout'] = d["casesAjout"]
                            cls.predictions[j]['obsvCumul'] = d["casesCumul"]
                            break
                historicalPred.append(cls.predictions[j])
        return historicalPred


    @classmethod
    def getPredictionsErrors(cls):
        print('getPredictionsErrors')
        if len(cls.predictions) == 0:
            cls.loadPredictions()
        data = cls.getAllData()
        predErrors = list()
        today = datetime.now().strftime("%Y-%m-%d")
        today = datetime.strptime(today, "%Y-%m-%d")
        for j in range(len(cls.predictions)):
            end_date = datetime.strptime(cls.predictions[j]["date"], "%Y-%m-%d")
            if (end_date-today).days <0:
                if len(cls.predictions[j])==3:
                    for d in data[::-1]:
                        if d["date"] == cls.predictions[j]["date"]:
                            cls.predictions[j]['obsvAjout'] = d["casesAjout"]
                            cls.predictions[j]['obsvCumul'] = d["casesCumul"]
                            break
                if len(cls.predictions[j])==5:
                    predErrors.append(
                        {
                            'date': cls.predictions[j]['date'],
                            'error': cls.predictions[j]['ajout'] - cls.predictions[j]['obsvAjout'],
                        }
                    )
        return predErrors














class APIModel():
    
    @classmethod
    def checker(cls):
        sched = BackgroundScheduler() # Scheduler object
        sched.start()
        
        def fetch_data_from_api():
            print("Ckeck api -- {} ".format(datetime.now().strftime("%b %d %Y %H:%M:%S")))
            cls.makeRequest()
        
        # add your job here
        sched.add_job(fetch_data_from_api, 'interval', hours=3, id='apiChecker')
    
    @classmethod
    def makeRequest(cls):
        print('makeRequest')
        try:
            response = requests.get("https://corona.lmao.ninja/v2/historical/Morocco?lastdays=all")
        except:
            print('exception occured while making request')
        if (response.status_code==200):
            data = json.loads(response.text)
            cls.formatAndSave(data)
        return response.text

    @classmethod
    def formatAndSave(cls, data):
        print('formatAndSave')
        try:
            data = data['timeline']

            """# only new cases
            dailyData = [["Dates", "Daily"]]
            precedt = 0
            for d in data['cases'].items():
                if d[1]>0 :
                    dailyData.append([d[0], d[1]-precedt])
                    precedt = d[1]
            with open('daily.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(dailyData)
            print('daily.csv saved')"""
            
            # new cases, deaths and recovered
            allDailyData = [["Dates", "Cases", "Deaths", "Recovered"]]
            preced = {'cases':0, 'recovered':0, 'deaths':0}
            cases = [(k,v) for k,v in data['cases'].items()]
            deaths = [(k,v) for k,v in data['deaths'].items()]
            recovered = [(k,v) for k,v in data['recovered'].items()]
            for i in range(len(cases)):
                if cases[i][1]>0 :
                    allDailyData.append(
                            [cases[i][0], 
                            cases[i][1]-preced['cases'],
                            deaths[i][1]-preced['deaths'],
                            recovered[i][1]-preced['recovered'],])
                    preced['cases'] = cases[i][1]
                    preced['deaths'] = deaths[i][1]
                    preced['recovered'] = recovered[i][1]
            with open('dailyGeneral.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(allDailyData)
            print('dailyGeneral.csv saved')

            Model().update()
                
        except:
            print('exception occured while making formatAndSave')