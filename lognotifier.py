# imports needed libraries for code
import time
import requests
import json
import glob
import os
from datetime import datetime, timezone, timedelta

# variables used in script
fileSend = False
configCheck = False
currentTime = datetime.now()

# loads config into variables to use in script
while configCheck == False: # loop to ensure config gets loaded, will retry if it fails
    try:
        with open("config/config.json") as config: # opens config and stores values in variables
            configJson = json.load(config)
            logfolders = configJson["logfolders"]
            webhookurl = configJson["webhookurl"]
            daystosend = configJson["daystosend"]
            daystodelete = configJson["daystodelete"]
            maxfilesize = configJson["maxfilesize"]
            config.close()
        configCheck = True # stops loop when loaded succesfully
        print("<LOGNOTIFIER> succesfully loaded config") # log message
    except Exception as e: # catches exception
        print("<LOGNOTIFIER> An exception occurred whilst trying to load the config: ", str(e)) # log message
        print("<LOGNOTIFIER> trying again in 1 minute") # log message
        time.sleep(60)
    
# main script
try:
    dayscheck = currentTime - timedelta(days=int(daystosend)) # calculates time until wich to send the logs
    daysdelete = currentTime - timedelta(days=int(daystodelete)) # calculates time until wich to delete the logs
    rl = requests.post(webhookurl, data={"content": "<LOGNOTIFIER> sending logs from the last " + daystosend + " days"})
    for folder in logfolders: # loops trough logfolders defined in config
        folder = folder + "\\*"
        print("<LOGNOTIFIER> checking folder: " + folder) # log message
        list_of_files = glob.glob(folder)
        for file in list_of_files: # loops trough files in logfolder selected by former loop
            x=os.stat(file)
            ageOfFile= x.st_mtime # gets age of file in unix timestamp
            print("<LOGNOTIFIER> age of file: " + str(ageOfFile)) # log message
            if ageOfFile > dayscheck.timestamp(): # checks if file is older then days to check defined in config
                with open(file) as logFile: # opens file to check size
                    fileSize = os.path.getsize(file)
                    if fileSize <= (int(maxfilesize)*1000000): # checks if file is not bigger then max filesize
                        rl = requests.post(webhookurl, files={"file": logFile}, data={"content": ""}) # sends file to webhook
                        fileSend = True # saves value for later use
                        print("<LOGNOTIFIER> " + file + " is posted to webhook") # log message
                    else:
                        rl = requests.post(webhookurl, data={"content": file + " is too big to send"}) # sends error message to webhook
                        print("<LOGNOTIFIER> " + file + " was too big to send to webhook") # log message
            else:
                if daystodelete != "":
                    if ageOfFile < daysdelete.timestamp(): # checks if file is older then days to delete defined in config
                        os.remove(file) # removes file
                        print("<LOGNOTIFIER> " + file + " deleted because it is older then " + daystodelete + " days") # log message
                    else:
                        print("<LOGNOTIFIER> " + file + " left untouched because it is not older then " + daystodelete + " days") # log message
                else:
                    print("<LOGNOTIFIER> " + file + " left untouched because daystodelte is not set") # log message
    if fileSend == False: # checks if any logs were send to webhook
        rl = requests.post(webhookurl, data={"content": "<LOGNOTIFIER> No logs to send"}) # sends message to webhook if no logs to send
except Exception as e:
    print("<LOGNOTIFIER> An exception occurred:", str(e)) # log message