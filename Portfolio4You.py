import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
import pandas as pd
from pdf import create_pdf
mpl.use('Agg')

 

df = pd.read_csv("./stock.csv",names=['Wertpapier','ETF','DIV','Rendite_2015','Rendite_2016','Rendite_2017','Rendite_2018','Rendite_2019','Kategorie'])


def create_portfolio(cat_list,basic,etf,div=False):   # returns a portfolio based on preferences, yields multiplied with weigth in port
    #generate basic portfolio
    basic_port= df.query('Kategorie == "Basic"')
    #weight of etfs from basis port in  main portfolio
    basic_weight = round(basic/len(basic_port),6) 
    #calc weigth of one category in main portfolio                                                  
    amount_cat= len(cat_list)
    perc_cat=(1-basic) / amount_cat
    #calc weight of category specific etf in main portfolio
    spec_etf_weight=perc_cat*etf
    #Calc weight of category specific stocks/stock in main portfolio 
    if(etf<1.0):
        spec_port_weigth= perc_cat*(1-etf)
        amount_stk=get_amount_stk(spec_port_weigth)
        spec_stk_weight=spec_port_weigth/amount_stk

    #add categoric specific etfs to portfolio , multiply yield with weight
    cat_etf_port = df.query("Kategorie == @cat_list")
    cat_etf_port= cat_etf_port.query('ETF == "True"')
    s = cat_etf_port.select_dtypes(include=[np.number])*spec_etf_weight
    cat_etf_port[s.columns]=s
    cat_etf_port['Weight'] = spec_etf_weight

    #add basic etfs to portfolio , multiply yield with weight
    s = basic_port.select_dtypes(include=[np.number])*basic_weight
    basic_port[s.columns]=s
    basic_port['Weight'] = basic_weight
    
    #concat portfolio
    port = pd.concat([basic_port,cat_etf_port])

    #add stocks to portfolio, yield multiplied 
    if(etf<1.0):
        for i in cat_list:
            cat_port= df.query('Kategorie == @i')
            cat_port= cat_port.query('ETF == "False"')
            if div == True:
                cat_port=cat_port.sort_values(by='DIV', ascending=False)
            cat_port.drop(cat_port.tail(8-amount_stk).index,inplace=True)
            s = cat_port.select_dtypes(include=[np.number])*spec_stk_weight
            cat_port[s.columns]=s
            cat_port['Weight'] = spec_stk_weight
            port = pd.concat([port,cat_port])

    return port
    
def get_amount_stk(spec_port_weight):      # mapping function to find the approachable amount of stocks
    spec_port_weight=spec_port_weight*100
    if (spec_port_weight < 1):
        return 1 
    elif(spec_port_weight<8):
        return round(spec_port_weight)
    else:
        return 8


# plots history from 2015-2019 if spent 100 $ at beginning of 2015.
# saves it in temp directory as png file to add it to pdf file
def plot_port_history(yields):             
    
    values = yields.values
    values = values.round(2) 
    values /=100
    
    year = [2015,2016,2017,2018,2019]
    capital = 100
    start= capital
    port_value=[]

    for i in values:
        if i >= 0:
            x = 1 + i
        else :
            x = 1 - i
        capital = capital * x
        port_value.append(capital) 

    plt.plot(year,port_value)
    plt.xlabel('Year')
    plt.ylabel('Portfolio Value')
    plt.title('Value of Portfolio')
    plt.xticks(np.arange(2015,2020,1))
    performance= capital/100
    plt.savefig("./temp/history.png")
    return performance

# creates pie chart for porrtfolio allocation
# saves it in temp directory as png file to add it to pdf file
def create_pie(weight):                     
    fig, ax = plt.subplots(1, 1, figsize=(12,6))
    weights =weight['Weight'] 
    labels = weight['Wertpapier']
    pie = ax.pie(weights, startangle=0,labels=labels)
    plt.savefig("./temp/port_alloc.png")

# creats pie chart for portfolio allocation by category
# saves it in temp directory as png file to add it to pdf file
def create_pie_cat(cat_alloc):                 
    x = cat_alloc.Kategorie.unique()
    x= x.ravel()
    s=cat_alloc.groupby(['Kategorie']).sum().values
    s= s.ravel()
    df = pd.DataFrame({'Kategorie':x, 'Sum':s})

    fig, ax = plt.subplots(1, 1, figsize=(12,6))
    fig.suptitle('Your Portfolio by Categories:')
    values =df['Sum'] 
    labels = df['Kategorie']
    pie = ax.pie(values, startangle=0,labels=labels,autopct='%1.1f%%')
    
    plt.savefig("./temp/cat_alloc.png")
    
def main(cat_list,basic,etf,div):
    
    #generate portfolio on preferences
    portfolio = create_portfolio(cat_list=cat_list,basic=basic,etf=etf,div=div)
    #yields of portfolio
    yields = portfolio.iloc[:,3:8].sum().round(2)
    #plot history of this portfolio
    perf=plot_port_history(yields)
    perf = round(perf,4) * 100
    #plot Pie Chart of portfolio allocation by Stocks
    weight = portfolio.loc[:,['Wertpapier','Weight']]
    create_pie(weight)
    #plot pie chart of portfolio allocation by cat
    cat_alloc= portfolio.loc[:,['Wertpapier','Weight','Kategorie']]
    create_pie_cat(cat_alloc)
    
    # sets up the parsing of arguments to the create pdf function
    stocks= portfolio['Wertpapier'].tolist()
    weights = portfolio['Weight'].tolist()
    yd=yields.values.reshape(-1, 1)
    yr =[2015,2016,2017,2018,2019]

    #create pdf
    create_pdf(stocks,weights,yd,yr,perf)
