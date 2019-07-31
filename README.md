# ROKBot
Hey there! ROKBot is a web-scraping, Dialogflow-based chatbot that parses information from Rockwell Automation's literature library. It features a custom-built JQuery UI that allows users to communicate. It has text-to-speech and speech-to-text functionality for ease of use.<br><br>

ROKBot talks users through the process of searching for a Rockwell Product, giving them the option to add and remove filters as necessary. Once the filters have been applied, ROKBot pulls the information from the Literature Library and applies a variety of Python functions on the Flask-implemented backend to generate statistics such as keywords, document length, and a one sentence summary. 
<br><br>
The HTML has hard-coded values as this demo was run for Rockwell Automation's Student Innovation Challenge (Earned 1st Place) and the local network blocks CORS, meaning that ROKBot had difficulties dynamically scraping the data.

#### Contributors:
* Jordan Rodrigues
* Jacob Lebowitz
* Tiger Gamble
<br>
<br>

![Image of the ROKBot GUI](https://github.com/Jordan-Rodrigues/ROKBot/blob/master/readme_images/rokbotPic.png)
