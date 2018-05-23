import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from mpl_finance import candlestick_ohlc
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web
import numpy as np
import datetime as dt
from dateutil.relativedelta import relativedelta
import csv
import re
import time
import random

# Hadriel Benjo


##(26)      0        1              2            3            4              5          6               7                   8                      9                   10                 11               12               13               14                15                16                  17              18               19                20                 21             22             23                      24                 25                                 
themes = ['bmh', 'classic', 'dark_background', 'fast', 'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn-bright', 'seaborn-colorblind', 'seaborn-dark-palette', 'seaborn-dark', 'seaborn-darkgrid', 'seaborn-deep', 'seaborn-muted', 'seaborn-notebook', 'seaborn-paper', 'seaborn-pastel', 'seaborn-poster', 'seaborn-talk', 'seaborn-ticks', 'seaborn-white', 'seaborn-whitegrid', 'seaborn', 'Solarize_Light2', 'tableau-colorblind10', '_classic_test']
style.use(themes[4])


def getSymbolLists(companyListFile = 'secwiki_tickers.csv'):
    '''
        This function get name of the file in the currenct direction program
        the file should contain the first line with the labels: 'Ticker', 'Name', 'Sector', 'Industry'
        and return a dictionary of thes data (about some valid Tickers/Symbols on stocks)
    '''
    labels = ['Ticker', 'Name', 'Sector', 'Industry']
    df = {}
    for l in labels:  df[l] = []
    with open(companyListFile) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            for l in labels:
                try:
                    df[l].append(row[l])
                except:
                    print('Cannot file the title {0} in the first line of the file {1}'.format(l, companyListFile))
                    print('Exit program')
                    exit(0)
                    break
    return df

def getRandomSymbol():
    '''
        This function return tuple of a random symbol and the list of all the stocks
    '''
    df = getSymbolLists()
    Symbol = df['Ticker']
    Name = df['Name']
    Sector = df['Sector']
    Industry = df['Industry']

    rand_symbol = random.choice(Symbol)
    #print('chose the next Random Symbol: \'{0}\''.format(rand_symbol))
    return (rand_symbol, Symbol)
   
    
def GraphIt(stockName,  bayAt = 'random', times = None ):
    '''
        This function get:
        *  stockName - need to be a valid ticker/symbol from 'quandl' database
        *  bayAt     - get the price of the stock that bought (optional as random value)
        *  times     - get the peroid of time from now to back , like: '10y' (10 years) , '5m' (5 months)  or '30d' (30 days) (optinal as '10y')
                       a valid param times can be specific time like:
                       ( start = dt.datetime(2000,1,1) , end   = dt.datetime(2016,12,31) )
                                    '2000-01-01'                        '2016-12-31'
                               
        and plot the graphs functionalities of:
        +  High minus Low
        +  candle stick ohlc
        +  volume
        +  moving average
    '''
    
    ## get data stock from internet to csv file
    def generateFile(stockName):
        print('Generate file data of stock: \'{0}\''.format(stockName))
        times_val = None
        if(type(times) is str):
            # get balid date tuple of 2 date (start, end=today)
            def getTimes(times):
                # regular expression to extract the interesting data from the string param
                timeReg    = re.compile('(\d+)\s?(\w)')
                match_time = timeReg.findall(times)
                today      = dt.date.today() 
                diffBy     = match_time[0][1]
                diffAmount = int(match_time[0][0])
                before = 0
                if  (diffBy in ['y', 'Y']):
                    before = relativedelta(months =+ 12*diffAmount)
                elif(diffBy in ['m', 'M']):
                    before = relativedelta(months =+ diffAmount)
                elif(diffBy in ['d', 'D']):
                    before = dt.timedelta(days=diffAmount)

                start = today - before
                return (start, today)
            
            times_val = getTimes(times)

        print('Between the times: start {0} - end {1}'.format(times_val[0], times_val[1]))
        if( (type(times_val) is tuple or type(times_val) is list)  and
             len(times_val) == 2 and
             type(times_val[0]) is dt.date and
             type(times_val[1]) is dt.date):

            start, end = times_val
            # should can be from : 'quandl' or 'google' or 'yahoo' , but for me work only quandl
            try:
                df = web.DataReader(stockName, 'quandl' , start, end) 
                df.iloc[::-1] # for order data that mack present it left to right
                df.to_csv(stockName+'.csv')
                print('File \'{0}.csv\' created!'.format(stockName))
            except:
                plt.close('all')
                print('There ins\'t name symbol \'{0}\' stock in quandl! try another else'.format(stockName))
                main()
                return
        else:
            print('Error: file did not crated...')
            print('Exit program')
            exit(0)
    
    ## convert date from string
    ## the format should be composit from:
    ## %Y - full year. 2018
    ## %y - partial year. 18
    ## %m - number months
    ## %d - number days
    ## %H - hours
    ## %M - minuts
    ## %S - seconds
    ## the format can be use like: '%Y-%m-%d' from the date like '2018-05-23'
    def bytesdate2num(fmt, encoding='utf-8'):
        strconverter = mdates.strpdate2num(fmt)
        def bytesconverter(b):
            s = b.decode(encoding)
            return strconverter(s)
        return bytesconverter

    ## Read data from file to list
    ## I take only the 6 first data, but you cat take more as you wish
    def getData_list(stockName):
        labels = ['Date', 'Open', 'High', 'Low', 'Close','Volume'] #, 'ExDividend','SplitRatio','AdjOpen','AdjHigh','AdjLow','AdjClose','AdjVolume']
        df = []
        with open(stockName+'.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                strintLine = ''
                for l in labels:
                    strintLine = strintLine + row[l] + ',' # Comma separated! 
                strintLine = strintLine[:len(strintLine)-1]# cut the last Comma.
                df.append(strintLine)
        return df

    ## some const - change as you wish
    MA1 = 10
    MA2 = 3
    ## some functionality - get the average of the the values, depend on the window size 
    def moving_average(values, window):
        weights = np.repeat(1.0 , window) / window
        smas = np.convolve(values, weights, 'valid')
        return smas
        # values  = [1,2,3,4,5]
        # window  = 3 (3 cell of 1/3)   |  4   (4 cell of 1/4)
        # weights = [1/3, 1/3, 1/3]     | [1/4, 1/4, 1/4, 1/4]
        # smas    = [2,3,4]  -> [((1+2+3)*weights[0]), ((2+3+4)*weights[1]), ((3+4+5)*weights[2])]

    ## some functionality - get the difference between high and low     
    def high_minus_low(highs, lows):
        return highs-lows
        # hight = [11,12,15,14,13]
        # lows  = [ 5, 6, 2, 6, 7]
        # h_l   = [ 6, 6,13, 8, 6]
        # print(list(map(high_minus_low, highs, lows)))


    ## init the graph configuration and display it
    def show_graph(stockName, bayAt = 'random'):
        plt.close('all')
        
        ## create a fig - we save it in the end of the program(function)
        fig = plt.figure(facecolor='#f0f0f0')

        ## create 3 subplots :
        ## 1   - for the High minus Low lines
        ## 2.a - for the candle sticks
        ## 2.b - for the volume fill line
        ## 3   - for the moving average
        ## notice the sharex is to combine the graphs into one graph
        ax1 = plt.subplot2grid((6,1),(0,0), rowspan=1, colspan=1)
        plt.title(stockName+' Stock')
        plt.ylabel('H-L')

        ax2 = plt.subplot2grid((6,1),(1,0), rowspan=4, colspan=1, sharex = ax1)
        plt.ylabel('Price')
        ax2v = ax2.twinx()
        
        ax3 = plt.subplot2grid((6,1),(5,0), rowspan=1, colspan=1, sharex = ax1)
        plt.ylabel('MAVgs')

        ## get data from file.csv we allrady have        
        df = getData_list(stockName)
        if(df == []):
            print('No data found in thes times, for the stock ' ,stockName )
            return

        ## extract the data from list to numpy array
        date , closep, highp, lowp, openp, volume = np.loadtxt(df,
                                                               delimiter=',', # Comma separated! 
                                                               unpack=True,
                                                               # convert only index 0 (the Date) values
                                                               converters={0: bytesdate2num('%Y-%m-%d')})        

        ## handle subplot ax1 
        ## create data for the moving average plots
        ma1 = moving_average(closep, MA1)
        ma2 = moving_average(closep, MA2)
        start = len(date[MA1:]) # take the larger number (MA1 > MA3)
        h_l = list(map(high_minus_low, highp, lowp))
        ax1.plot_date(date[-start:], h_l[-start:], '-', lw = 1, label='H-L')
        ax1.yaxis.set_major_locator(mticker.MaxNLocator(nbins=4, prune='lower'))

        ## handle subplot ax2.a 
        x = 0
        y = len(date)
        ohlc = []
        while x < y:
            ## create data for the candle sticks graph
            append_me = date[x], openp[x] , highp[x] ,  lowp[x] , closep[x] , volume[x]
            ohlc.append(append_me)
            x += 1    
        candlestick_ohlc(ax2, ohlc[-start:], width=0.4, colorup='#77d879', colordown='#db3f3f')        
        ax2.grid(True, linestyle = '--')
        
        ## handle subplot ax2.b
        ax2v.plot([],[], color='#ff9933', alpha=0.4, label='Volume') # for the legend
        ax2v.fill_between(date[-start:], 0, volume[-start:], facecolor='#ff9933', alpha=0.3)
        ax2v.axes.yaxis.set_ticklabels([])
        ax2v.grid(False)
        ax2v.set_ylim(0,2*volume.max())


        ## Annotation Examples
        ## 
        ## Annotation of the last price 
        bbox_props = dict(boxstyle = 'larrow', fc='w', ec='k', lw=1)
        ax2.annotate(str(closep[0]), (date[0], closep[0]), xytext=(date[0]+0, closep[0]), bbox= bbox_props)        
        ## Annotation example with arrow 
        ax2.annotate('Bad News!', (date[(int)(len(date)/2)], highp[(int)(len(date)/2)]), xytext=(0.4, 0.2), textcoords='axes fraction', arrowprops = dict(facecolor='grey', edgecolor='yellow'))
        ## Font dict example
        font_dict = {'family': 'serif',
                     'color' : 'blue',
                     'size'  : 15}
        ## Hard coded text
        ax2.text(date[-1], closep[-1], 'Text Example', fontdict=font_dict)


        ## handle subplot ax3
        ax3.plot(date[-start:], ma1[-start:], linewidth=1, label=(str(MA1) + 'MA'))
        ax3.plot(date[-start:], ma2[-start:], linewidth=1, label=(str(MA1) + 'MA'))
        ax3.fill_between(date[-start:], ma2[-start:], ma1[-start:],
                         where=(ma1[-start:] < ma2[-start:]),
                         facecolor = 'r', edgecolor = 'r', alpha=0.5)
        ax3.fill_between(date[-start:], ma2[-start:], ma1[-start:],
                         where=(ma1[-start:] > ma2[-start:]),
                         facecolor = 'g', edgecolor = 'g', alpha=0.5)

        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m/%y'))
        ax3.xaxis.set_major_locator(mticker.MaxNLocator(10))
        ax3.yaxis.set_major_locator(mticker.MaxNLocator(nbins=5, prune='upper'))


        ## remove the ticks of the ax1 and ax2 and put the in the bottom ax3
        for label in ax3.xaxis.get_ticklabels():
            label.set_rotation(45)
            label.set_fontsize(10)
        ax3.set_xlabel('Date')
        for label in ax1.yaxis.get_ticklabels():
            label.set_fontsize(10)
        for label in ax2.yaxis.get_ticklabels():
            label.set_fontsize(10)
        for label in ax3.yaxis.get_ticklabels():
            label.set_fontsize(10)
        plt.setp(ax1.get_xticklabels(), visible=False)
        plt.setp(ax2.get_xticklabels(), visible=False)
        plt.subplots_adjust(left=0.11, bottom= 0.24, right=0.90, top=0.90, wspace=0.2, hspace=0.2)


        ## set legend to discribe the line type
        ax1.legend()
        leg = ax1.legend(loc=9, ncol=2, prop={'size': 11})
        leg.get_frame().set_alpha(0.4)
        ax2v.legend()
        leg = ax2v.legend(loc=9, ncol=2, prop={'size': 11})
        leg.get_frame().set_alpha(0.4)
        ax3.legend()
        leg = ax3.legend(loc=9, ncol=2, prop={'size': 11})
        leg.get_frame().set_alpha(0.4)
        
        ## show the graph and save if in a large image after exit the program
        plt.show()
        fig.set_size_inches((11, 8.5), forward=False)
        fig.savefig((''+ stockName + ' Stock.png'), dpi=500)
        
    ##______________________________________________________________________________________________

    ## run the function
    ## first check if the user want to override and loada new range data
    if(times is not None):
        print('there hasn\'t allrady a file data')
        generateFile(stockName)
    
    try:
        show_graph(stockName, bayAt = bayAt)
    except:
        ## if we have exception like Missing Data , we create a new data in range of ten years from now to back
        print('catch exception')
        times = '10y'
        generateFile(stockName)
        ## and try to load and show the graph again
        show_graph(stockName, bayAt = bayAt)

        
##---------------------------------------------------------------------------------------------------------

def getStockNameFromUser():
    stockName = 'EBAY' #'GOOG'
    stockName, Symbols = getRandomSymbol()
    stockName = input('Enter a Symbol(or press enter for a random one) to show his data: ')

    if(len(stockName) > 0):
        con = stockName
        while True:
            if(len(con) > 0):
                if con not in Symbols:
                    print('Notice! the Symbol \'{0}\' isn\'t in the symbol list!\nbut if your shore you can continue...'.format(stockName))
                    con = input('Press Enter to contintue or press any else stock: ')
                    if(len(con) == 0):
                        break
                else:
                    return con
    else:    
        print('Press Enter for another random stock, or press any else key to continue: ')
        while True:    
            stockName = random.choice(Symbols)
            print('Chose a random stock : \'{0}\''.format(stockName), end=' ')
            ExitWhile = input()
            if(len(ExitWhile) > 0):
                break

    return stockName

def getTimesFromUser():
    times = None
    t = input('Do you want to define range of time back ? (default is 10 years)\nIf so, enter number(>0) and char(y|m|d) else press Enter\nTimes: ')
    if(len(t)>0):
        times = t
    return times;

def main():
    stockName = getStockNameFromUser()
    print('Display data for the stock: \'{0}\''.format(stockName))
    times = getTimesFromUser()
    #times = ( dt.datetime(2005,1,1) , dt.datetime(2018,05,23) )
    GraphIt(stockName, times)

if __name__ == "__main__":
    main()
    

