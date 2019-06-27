from flask import Flask, render_template, request, redirect, url_for
import requests
import time
from selenium.webdriver.chrome.options import Options  
from selenium import webdriver
app = Flask(__name__)

#Creating global variables that can be passed from page to page
#global fulLURL
#global PDFs
#PDFs = []
#fullURL = None


#Route for the main page, renders the home template
@app.route('/')
def home():
   return render_template("home.html")


@app.route('/Chatbot')
def results():
    return render_template("chatbot.html")
    
#-----------------------------------------FUNCTIONS--------------------------------
def urlCreator(keyword, filterDictionary):
    #First part of the URL
    urlStart = "https://www.rockwellautomation.com/search/ra_en_NA;keyword="

    #Browser automatically handles the rendering of keyword input
    #I want to be given a dictionary for the filters where the filter category is the key and all the entered filter types are the values
    filterSection = ""
    dictPosCounter = 0
    for filterCategory, filterTypeList in filterDictionary.items():
        #Creating a filter chucnk for each filter category, add them all together at end
        filterBody = ""
        counter = 0
        numFilters = len(filterTypeList)
        for filter in filterTypeList:
            #applying custom url codes derived from pattern analysis
            filter = filter.replace(" ", "%2520")
            filter = filter.replace("/", "%252F")
            print("FILTER IS " + filter)
            #if you're on the last one, end it
            if (counter == numFilters - 1):
                filterBody += (filter + "%2522%2529")
                counter += 1
            #add an or statement and go on to the next
            else:
                filterBody += (filter + "%2522%2520OR%2520%2522")
                counter += 1
        if (dictPosCounter == 0):
            filterHeader = filterCategory + "%253A%2528%2522"
        else:
            filterHeader = "%253B" + filterCategory + "%253A%2528%2522"
        filterSection += (filterHeader + filterBody)
        dictPosCounter += 1
    finalURL = urlStart + keyword + ";startIndex=0;activeTab=Literature;spellingCorrect=true;" + "facets=" + filterSection + ";languages=en;locales=en_NA,en_GLOBAL;sort=bma;"
    print(finalURL)
    return finalURL


#Works https://www.rockwellautomation.com/search/ra_en_NA;keyword=voltage;startIndex=0;activeTab=Literature;spellingCorrect=true;facets=service_ss%253A%2528%2522Asset%2520Management%2520Services%2522%2529;languages=en;locales=en_NA,en_GLOBAL;sort=bma
#Tests https://www.rockwellautomation.com/search/ra_en_NA;keyword=voltage;startIndex=0;activeTab=Literature;spellingCorrect=true;facets=service_ss%253A%2528%2522Asset%2520Management%2520Services%2552%2529;languages=en;locales=en_NA,en_GLOBAL;sort=bma