# matplotlib Finance indicators

### Python , matplotlib

## Description

A large project where I learned more in depth about matplotlib, and the implementation of stock chart with indicators
When running a project, the user needs to enter a name for a share, or choose a random count, for example: i inputed Google stock (GOOG)

```
Enter a Symbol(or press enter for a random one) to show his data: GOOG
Display data for the stock: 'GOOG'
```

then the program ask you how many time back do you want to display, I inputed for example 1 year (1y)

```
Do you want to define range of time back ? (default is 10 years)
If so, enter number(>0) and char(y|m|d) else press Enter
Times: 1y
```

the program import data from the internet (quandl database) and save it in csv file 

```
there hasn't allrady a file data
Generate file data of stock: 'GOOG'
Between the times: start 2017-05-23 - end 2018-05-23
File 'GOOG.csv' created!
```

then plot the graphs functionalities of:
+  High minus Low
+  candle stick ohlc
+  volume
+  moving average 

you can zoom it and so on... 



Installing required packages

```python
pip install numpy 
pip install matplotlib
pip install pandas==0.21.0
pip install pandas_datareader
pip install beatifulsoup4
pip install scikit_learn
pip install sklearn
pip install https://github.com/matplotlib/mpl_finance/archive/master.zip
```

___

The program running will give you the following images:

<div width=100%>
<img src="https://profile.fcdn.co.il/images2/0__05b05c7b60c56d.jpg" width="700" style="padding:1px;
                   border:1px solid #021a40; 
                  display: block;
                  margin-left: auto;
                  margin-right: auto "> 

<img src="https://profile.fcdn.co.il/images2/0__05b05c7d263198.jpg" width="700" style="padding:1px;
                   border:1px solid #021a40; 
                  display: block;
                  margin-left: auto;
                  margin-right: auto "> 
</div>


Enjoy...
