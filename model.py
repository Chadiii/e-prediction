from pandas import read_csv
from datetime import datetime, timedelta
from pandas import Series
import numpy
from statsmodels.tsa.arima_model import ARIMA
import json


class Model():
    series = Series()
    model = None
    predictions = list()
    params = (2,1,2)
    steps = 7
    
    @classmethod
    def download(cls):
        def parser(x):
            return datetime.strptime(x, '%d/%m/%Y')
        cls.series = read_csv('daily1.csv', header=0, parse_dates=[0], index_col=0, squeeze=True, date_parser=parser)

    @classmethod
    def fitModel(cls):
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
        som = int(numpy.sum(cls().series))
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
        cls.savePredictions()
    
    
    
    @classmethod
    def savePredictions(cls):
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
    def loadPredictions(cls):
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
        if(len(cls.predictions)==0):
            cls.fitModel()
            
            
    
    @classmethod
    def getData(cls):
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

        return dataList
    
    
    @classmethod
    def getPredictions(cls):
        if len(cls.predictions) == 0:
            cls.loadPredictions()
        return cls.predictions

        
#Model().getData()    
        
#Model().getPredictions()
        
        
        