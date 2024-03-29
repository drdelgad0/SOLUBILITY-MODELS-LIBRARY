# -*- coding: utf-8 -*-
"""Libreria Solubilidad en Python.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xas6eyanWmcYjV1Wj8Ev18XhOa5yP_U6
"""

from pandas.core.indexes import extension
import pandas as pd
import numpy as np
from IPython.display import display, Math, Latex, Markdown,HTML
from IPython.core.display import display, HTML
from scipy.optimize import curve_fit
import plotly.graph_objects as go
from google.colab import files



def func(T,A,B,C):
    return np.exp(A + B/T + C*np.log(T))

class dataframe:
    
    def __init__(self,url):
        self.url =url
    
    @property
    def value_temp(self):
        df = pd.read_csv(self.url)
        temp = pd.DataFrame(df["T"])
        return temp
        
    @property
    def show(self):
        df = pd.read_csv(self.url)
        return df

# CLASE PARA EL MODELO APELBLAT MODIFICADO

class modified_apelblat_model(dataframe):
    
    @property
    def equation(self):
        salida = display(HTML('<h2> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Modified Apelblat Equation</h2>'))
        display(Math(r'$$\ln(x)=A + \dfrac{B}{T} + C\ln{T}$$'))
        return salida


    def parameters(self, method="lm", maxfev=20000, sd = True):
        
        df = pd.read_csv(self.url)
        W = list(df.columns[1:])

        para_A = []
        para_B = []
        para_C = []

        desv_para_A = []
        desv_para_B = []
        desv_para_C = []

        for i in W:
            xdat = df["T"].values
            ydat = (df[i].values)
            popt,mcov = curve_fit(func,xdat,ydat,method=method ,maxfev=maxfev)

            para_A.append(popt[0])
            para_B.append(popt[1])
            para_C.append(popt[2])

            desv_para_A.append(np.sqrt((np.diag(mcov))[0]))
            desv_para_B.append(np.sqrt((np.diag(mcov))[1]))
            desv_para_C.append(np.sqrt((np.diag(mcov))[2]))

        if sd == True:
            DF = pd.DataFrame({"x":df.columns[1:],'A':para_A,"σ_A":desv_para_A,'B':para_B,"σ_B":desv_para_B,'C':para_C,"σ_C":desv_para_C})
        else:
            DF = pd.DataFrame({"x":df.columns[1:],'A':para_A,'B':para_B,'C':para_C})
        return  DF
    
    
    def values_exp(self,temp = True):

        df = pd.read_csv(self.url)
        W = list(df.columns[1:])

        C_temp = []
        C_exp  = []
       
        for i in W:

            xdat = df["T"].values
            Xdat = xdat.tolist()

            ydat = (df[i].values)
            Ydat =  ydat.tolist()

            C_temp += Xdat
            C_exp  += Ydat
 
        arr_tem = np.array(C_temp)
        arr_exp = np.array(C_exp)

        if temp == True: 
            data_frame = pd.DataFrame({'Temperatura': arr_tem,'Xexp':arr_exp})
        else : 
            data_frame = pd.DataFrame({'Xexp':arr_exp})
            
        return data_frame


    def values_cal(self,method="lm", maxfev=20000,temp = True, RD = False):

        df = pd.read_csv(self.url)
        W  = list(df.columns[1:])

        para_A = []
        para_B = []
        para_C = []


        C_temp = []
        C_cal  = []
        C_RD   = []

        for i in W:
            xdat = df["T"].values
            ydat = (df[i].values)
            popt,mcov = curve_fit(func,xdat,ydat,method=method,maxfev=maxfev)

            para_A.append(popt[0])
            para_B.append(popt[1])
            para_C.append(popt[2])

        for i in W:
            xdat = df["T"].values
            Xdat = xdat.tolist()

            ydat = (df[i].values)
            Ydat =  ydat.tolist()

            ymodel = (func(xdat,para_A[W.index(i)],para_B[W.index(i)],para_C[W.index(i)]))
            Ymodel = ymodel.tolist()

            Relative_differences = ((ydat - ymodel)/ydat).tolist()


            C_temp += Xdat
            C_cal  += Ymodel
            C_RD   += Relative_differences
 

        arr_tem = np.array(C_temp)
        arr_cal = np.array(C_cal)
        arr_RD  = np.array(C_RD )
        
        if  temp == True  and RD == False:
            data_frame = pd.DataFrame({'Temperatura': arr_tem,'Xcal':arr_cal})
        elif temp == True and RD == True:
            data_frame = pd.DataFrame({'Temperatura': arr_tem,'Xcal':arr_cal,'RD':arr_RD})
        elif temp == False and RD == False:
            data_frame = pd.DataFrame({'Xcal':arr_cal})
        elif temp == False and RD == True:
            data_frame = pd.DataFrame({'Xcal':arr_cal,'RD':arr_RD})
        return data_frame

    def values(self,method="lm", maxfev=20000, temp = True):

        df = pd.read_csv(self.url)
        W  = list(df.columns[1:])

        para_A = []
        para_B = []
        para_C = []

        C_temp = []
        C_exp  = []
        C_cal  = []
        C_RD   = []

        for i in W:
            xdat = df["T"].values
            ydat = (df[i].values)
            popt,mcov = curve_fit(func,xdat,ydat,method=method,maxfev=maxfev)

            para_A.append(popt[0])
            para_B.append(popt[1])
            para_C.append(popt[2])


        for i in W:
  
            xdat = df["T"].values
            Xdat = xdat.tolist()

            ydat = (df[i].values)
            Ydat =  ydat.tolist()

            ymodel = (func(xdat,para_A[W.index(i)],para_B[W.index(i)],para_C[W.index(i)]))
            Ymodel = ymodel.tolist()

            RD = ((ydat - ymodel)/ydat).tolist()


            C_temp += Xdat
            C_exp  += Ydat
            C_cal  += Ymodel
            C_RD   += RD
 

        arr_tem = np.array(C_temp)
        arr_exp = np.array(C_exp)
        arr_cal = np.array( C_cal)
        arr_RD  = np.array( C_RD )

        if temp == True: 
            data_frame = pd.DataFrame({'Temperatura': arr_tem,'Xexp':arr_exp,'Xcal':arr_cal,'RD':arr_RD})
        else:
            data_frame = pd.DataFrame({'Xexp':arr_exp,'Xcal':arr_cal,'RD':arr_RD})

        return data_frame

    def statistic_MAPE(self,method="lm", maxfev=20000, opt= "all"):


        df = pd.read_csv(self.url)
        W  = list(df.columns[1:])

        para_A = []
        para_B = []
        para_C = []

        C_temp = []
        C_exp  = []
        C_cal  = []
        C_RD   = []

        for i in W:
            xdat = df["T"].values
            ydat = (df[i].values)
            popt,mcov = curve_fit(func,xdat,ydat,method=method,maxfev=maxfev)

            para_A.append(popt[0])
            para_B.append(popt[1])
            para_C.append(popt[2])


        for i in W:
  
            xdat = df["T"].values
            Xdat = xdat.tolist()

            ydat = (df[i].values)
            Ydat =  ydat.tolist()

            ymodel = (func(xdat,para_A[W.index(i)],para_B[W.index(i)],para_C[W.index(i)]))
            Ymodel = ymodel.tolist()

            RD = ((ydat - ymodel)/ydat).tolist()


            C_temp += Xdat
            C_exp  += Ydat
            C_cal  += Ymodel
            C_RD   += RD
 

        arr_tem = np.array( C_temp)
        arr_exp = np.array( C_exp)
        arr_cal = np.array( C_cal)
        arr_RD  = np.array( C_RD )

        data_frame = pd.DataFrame({'Temperatura': arr_tem,'Xexp':arr_exp,'Xcal':arr_cal,'RD':arr_RD})

        
        MAPES = []
        INDEX = []

        Temp = df["T"].values

        for i in range(len(Temp)):
            df_mask = data_frame['Temperatura'] == Temp[i]
            data_filter = data_frame[df_mask]
            MAPE = sum(abs(data_filter["RD"]))*100/len(data_filter['Temperatura'])
            MAPES.append(MAPE)
            INDEX.append("T"+str(i+1))


        if opt == "all": 

            data_mape = print("Mean Absolute Percentage Error, MAPE =",sum(MAPES)/len(Temp))
        else:
            data_mape = pd.DataFrame({"T":INDEX,"Temp":Temp,"MAPE":MAPES})

        return data_mape

    def statistic_RMSD(self,method="lm", maxfev=20000):


        df = pd.read_csv(self.url)
        W  = list(df.columns[1:])

        para_A = []
        para_B = []
        para_C = []

        C_temp = []
        C_exp  = []
        C_cal  = []
        C_RD   = []

        for i in W:
            xdat = df["T"].values
            ydat = (df[i].values)
            popt,mcov = curve_fit(func,xdat,ydat,method=method,maxfev=maxfev)

            para_A.append(popt[0])
            para_B.append(popt[1])
            para_C.append(popt[2])


        for i in W:
  
            xdat = df["T"].values
            Xdat = xdat.tolist()

            ydat = (df[i].values)
            Ydat =  ydat.tolist()

            ymodel = (func(xdat,para_A[W.index(i)],para_B[W.index(i)],para_C[W.index(i)]))
            Ymodel = ymodel.tolist()

            RD = ((ydat - ymodel)/ydat).tolist()


            C_temp += Xdat
            C_exp  += Ydat
            C_cal  += Ymodel
            C_RD   += RD
 

        arr_tem = np.array( C_temp)
        arr_exp = np.array( C_exp)
        arr_cal = np.array( C_cal)
        

        ss_res = np.sum((arr_cal - arr_exp)**2 )
        RMSD = (np.sqrt(ss_res/len(arr_exp)))

        return print("Root Mean Square Deviation, RMSD =",RMSD )


    def statistic_AIC(self,method="lm", maxfev=20000, opt ="corrected"):


        df = pd.read_csv(self.url)
        W  = list(df.columns[1:])

        para_A = []
        para_B = []
        para_C = []

        C_temp = []
        C_exp  = []
        C_cal  = []
        C_RD   = []

        for i in W:
            xdat = df["T"].values
            ydat = (df[i].values)
            popt,mcov = curve_fit(func,xdat,ydat,method=method,maxfev=maxfev)

            para_A.append(popt[0])
            para_B.append(popt[1])
            para_C.append(popt[2])


        for i in W:
  
            xdat = df["T"].values
            Xdat = xdat.tolist()

            ydat = (df[i].values)
            Ydat =  ydat.tolist()

            ymodel = (func(xdat,para_A[W.index(i)],para_B[W.index(i)],para_C[W.index(i)]))
            Ymodel = ymodel.tolist()

            RD = ((ydat - ymodel)/ydat).tolist()


            C_temp += Xdat
            C_exp  += Ydat
            C_cal  += Ymodel
            C_RD   += RD
 

        arr_tem = np.array( C_temp)
        arr_exp = np.array( C_exp)
        arr_cal = np.array( C_cal)
        arr_RD  = np.array(C_RD )
        
        k = 3
        N =len(arr_RD)
        ss_res = np.sum((arr_cal - arr_exp)**2 )
        AIC = N*np.log(ss_res/N)+2*k
        
        AICc = abs(AIC +((2*k**2+2*k)/(N-k-1)))
        
        if opt =="corrected":
            aic = print("Akaike Information Criterion corrected , AICc =",AICc)
        else:
            aic = print("Akaike information criterion, AIC =",AIC )
        return aic

    def statistic_RS(self,method="lm", maxfev=20000):


        df = pd.read_csv(self.url)
        W  = list(df.columns[1:])

        para_A = []
        para_B = []
        para_C = []

        C_temp = []
        C_exp  = []
        C_cal  = []
        C_RD   = []

        for i in W:
            xdat = df["T"].values
            ydat = (df[i].values)
            popt,mcov = curve_fit(func,xdat,ydat,method=method,maxfev=maxfev)

            para_A.append(popt[0])
            para_B.append(popt[1])
            para_C.append(popt[2])


        for i in W:
  
            xdat = df["T"].values
            Xdat = xdat.tolist()

            ydat = (df[i].values)
            Ydat =  ydat.tolist()

            ymodel = (func(xdat,para_A[W.index(i)],para_B[W.index(i)],para_C[W.index(i)]))
            Ymodel = ymodel.tolist()

            RD = ((ydat - ymodel)/ydat).tolist()


            C_temp += Xdat
            C_exp  += Ydat
            C_cal  += Ymodel
            C_RD   += RD
 

        arr_tem = np.array( C_temp)
        arr_exp = np.array( C_exp)
        arr_cal = np.array( C_cal)
        arr_RD  = np.array(C_RD )
       
        ss_res = np.sum((arr_cal - arr_exp)**2 )
        ss_tot = np.sum( (arr_exp - np.mean(arr_exp) )**2  )

        R2 = 1 - (ss_res / ss_tot)
            
        return print("Coefficient of Determination, R^2 =",R2)

    def statistics(self,method="lm", maxfev=20000):


        df = pd.read_csv(self.url)
        W  = list(df.columns[1:])

        para_A = []
        para_B = []
        para_C = []

        C_temp = []
        C_exp  = []
        C_cal  = []
        C_RD   = []

        for i in W:
            xdat = df["T"].values
            ydat = (df[i].values)
            popt,mcov = curve_fit(func,xdat,ydat,method=method,maxfev=maxfev)

            para_A.append(popt[0])
            para_B.append(popt[1])
            para_C.append(popt[2])


        for i in W:
  
            xdat = df["T"].values
            Xdat = xdat.tolist()

            ydat = (df[i].values)
            Ydat =  ydat.tolist()

            ymodel = (func(xdat,para_A[W.index(i)],para_B[W.index(i)],para_C[W.index(i)]))
            Ymodel = ymodel.tolist()

            RD = ((ydat - ymodel)/ydat).tolist()


            C_temp += Xdat
            C_exp  += Ydat
            C_cal  += Ymodel
            C_RD   += RD
 

        arr_tem = np.array( C_temp)
        arr_exp = np.array( C_exp)
        arr_cal = np.array( C_cal)
        arr_RD  = np.array(C_RD )

        MAPE = sum(abs(arr_RD))*100/len(arr_RD)

        ss_res = np.sum((arr_cal - arr_exp)**2 )
        ss_tot = np.sum( (arr_exp - np.mean(arr_exp) )**2  )

        R2 = 1 - (ss_res / ss_tot)

        ss_res = np.sum((arr_cal - arr_exp)**2 )
        RMSD = (np.sqrt(ss_res/len(arr_exp)))


        k = 3
        N =len(arr_RD)
        ss_res = np.sum((arr_cal - arr_exp)**2 )
        AIC = N*np.log(ss_res/N)+2*k
        AICc = abs(AIC +((2*k**2+2*k)/(N-k-1)))

        ss_res = np.sum((arr_cal - arr_exp)**2 )
        ss_tot = np.sum( (arr_exp - np.mean(arr_exp) )**2  )

        R2 = 1 - (ss_res / ss_tot)

        col1 = np.array(["MAPE","RMSD","AICc","R^2"])
        col2 = np.array([MAPE,RMSD,AICc,R2])
        estadis = pd.DataFrame({"statistics":col1,"values":col2})
            
        return estadis

    def summary_data(self,method="lm", maxfev=20000, temp = True, sd =True,name= "modified_apelblat"):
        
        nombre = name
        DATA = pd.concat([self.values(method = method, maxfev = maxfev, temp = temp),self.statistic_MAPE(method = method, maxfev = maxfev,opt="temp"),self.parameters(method = method, maxfev = maxfev, sd = sd ),self.statistics(method = method, maxfev = maxfev)], axis=1)
        
        
        url_1 = "/content/sample_data/"+ nombre +".xlsx"
        url_3 = "/content/sample_data/"+ nombre +".csv"
        DATA.to_excel(url_1,sheet_name='Modified_Apelblat')
        DATA.to_csv(url_3)
        return DATA

    def plot(self,method="lm", maxfev=20000, name = "modified_apelblat" ):

        nombre= name
        
        url_2 = "/content/sample_data/"+ nombre+".pdf"

        df = pd.read_csv(self.url)
        W  = list(df.columns[1:])

        para_A = []
        para_B = []
        para_C = []

        C_temp = []
        C_exp  = []
        C_cal  = []
        C_RD   = []

        for i in W:
            xdat = df["T"].values
            ydat = (df[i].values)
            popt,mcov = curve_fit(func,xdat,ydat,method=method,maxfev=maxfev)

            para_A.append(popt[0])
            para_B.append(popt[1])
            para_C.append(popt[2])


        for i in W:
  
            xdat = df["T"].values
            Xdat = xdat.tolist()

            ydat = (df[i].values)
            Ydat =  ydat.tolist()

            ymodel = (func(xdat,para_A[W.index(i)],para_B[W.index(i)],para_C[W.index(i)]))
            Ymodel = ymodel.tolist()

            RD = ((ydat - ymodel)/ydat).tolist()


            C_temp += Xdat
            C_exp  += Ydat
            C_cal  += Ymodel
            C_RD   += RD
 

        arr_tem = np.array( C_temp)
        arr_exp = np.array( C_exp)
        arr_cal = np.array( C_cal)
        arr_RD  = np.array(C_RD )

        fig = go.Figure()


        numerofilas = len(df["T"])
        numerocolumnas = len(df.columns )-2
        L = [numerofilas*i for i in range(numerocolumnas+2)]

        X = np.linspace(min(arr_cal),max(arr_exp),200)

        for i in range(11):
            fig.add_trace(go.Scatter(x=arr_cal[L[i]:L[i+1]], y=arr_exp[L[i]:L[i+1]],name=" w"+str(i) ,mode='markers',marker=dict(size=6,line=dict(width=0.5,color='DarkSlateGrey'))))


        fig.add_trace(go.Scatter(x=X,y=X,name="$x_{exp}=x_{cal}$"))


        fig.update_xaxes(title = "$x_{cal}$", title_font=dict(size=30, family='latex', color='rgb(1,21,51)'))
        fig.update_yaxes(title = "$x_{exp}$ ",title_font=dict(size=30,family='latex', color='rgb(1,21,51)'))
        fig.update_layout(title='',title_font=dict(size=26, family='latex', color= "rgb(1,21,51)"),width=1010, height=550)
        fig.update_layout(legend=dict(orientation="h",y=1.2,x=0.03),title_font=dict(size=40, color='rgb(1,21,51)'))
        fig.write_image(url_2)
        return fig.show()

    
    
    def summary_download(self,name = "modified_apelblat",ext= "xlsx"):
        nombre = name
        extension = ext
        url_1 = "/content/sample_data/"+ nombre +"."+extension
        return files.download(url_1)

    def plot_download(self,name = "modified_apelblat"):
        nombre = name
        url_2 = "/content/sample_data/"+ nombre+".pdf"
        return files.download(url_2)