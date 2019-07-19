from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import time
from selenium.webdriver.chrome.options import Options  
from selenium import webdriver
import os
import dialogflow
import pusher 
import sys
app = Flask(__name__)

#Setting up SQL Database
DATABASE_URL = os.environ['HOST']

#setting up pusher client
pusher_client = pusher.Pusher(
    app_id=os.getenv('PUSHER_APP_ID'),
    key=os.getenv('PUSHER_KEY'),
    secret=os.getenv('PUSHER_SECRET'),
    cluster=os.getenv('PUSHER_CLUSTER'))
#Globalvar for filter list

filterList = None

#Route for the main page, renders the home template
@app.route('/')
def home():
   return render_template("home.html")

@app.route('/', methods=["POST", "GET"])
def pageRoute():
    if request.method == 'POST':
        return redirect(url_for("chatbot"))

@app.route('/Chatbot')
def chatbot():
    return render_template("chatbot.html")

@app.route('/Chatbot', methods=["POST", "GET"])
def pageRoute2():
    if request.method == 'POST':
        print("test message")
        return redirect(url_for("results"))

@app.route('/Results', methods=["POST", "GET"])
def results():
    global filterList
    filterList = filterList.split(",")
    keyword = filterList[0]
    filterCategory = wordToUrlChunk(filterList[1])
    filterName = filterList[2]
    filterDictionary = {filterCategory : [filterName]}
    finalUrl = urlCreator(keyword, filterDictionary)
    PDFs = pdfReturner(finalUrl)
    time.sleep(2)
    return render_template("result.html", PDFs = PDFs, url = finalUrl)

@app.route('/send_message', methods=['POST'])
def send_message():
    message = request.form['message']
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    fulfillment_text = detect_intent_texts(project_id, "unique", message, 'en')
    time.sleep(1)
    pusher_client.trigger('ROKbot', 'new_message', {'message' : fulfillment_text})
    return jsonify(fulfillment_text)

@app.route('/filter_process', methods=['POST'])
def filterProcess():
    global filterList
    filterList = request.form["filterList"]
    return filterList
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
    finalURL = finalURL.replace(" ", "%2520")
    return finalURL


#Sends data to dialogflow
def detect_intent_texts(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    if text:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = session_client.detect_intent(
            session=session, query_input=query_input)

        return response.query_result.fulfillment_text

def wordToUrlChunk(word):
    word = word.lower()
    if word == "publication type":
        return "doc_type_full_s"
    elif word == "solutions":
        return "solution_ss"
    elif word == "industries":
        return "industry_ss"
    elif word == "services":
        return "service_ss"

def pdfReturner(fullURL):
    PDFs = []
    #Creates an invisible browser (headless) to load the page manually (allows JS to render) and then pulls in all the relevant links
    options = Options()
    options.add_argument('--headless')
    browser = webdriver.Chrome()
    browser.get(fullURL)
    tags = browser.find_elements_by_css_selector("div.literature.ra a")

    #for each tag pulled from the website, add the URL of that tag to the PDF list if it isn't none
    for tag in tags:
        if (tag.get_attribute("href") != None):
            PDFs.append(tag.get_attribute("href"))
    if len(PDFs) > 5:
        PDFs = PDFs[0:5]
    return PDFs
    
   