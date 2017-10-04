import json
import os
from flask import Flask, request, abort
import requests


app = Flask(__name__)

    
@app.route('/leagueapp', methods=['POST']) #route to application specific for groupme callback url.
def get_groupme_text():
    bot_name = "" #botname search string will search for
    bot_ring = "@%s" %bot_name #assumes @botname will trigger call to function to send a message as bot.
    data = request.get_json() #json data posted by groupme
        
    if data['name'] != bot_name and bot_ring in data['text']: #if the message is not from the bot and includes @botname respond
        post_to_bot(data['name'], data['text'])

    return "ok", 200 #return 200 to prevent 500 errors.
    

def post_to_bot(name, keyword):
    bot_id = os.getenv('GROUPME_BOT') #botID of the created groupme bot, enviornment variable
    dictToSend = {'bot_id': bot_id , 'text': ''} # placeholder for JSON dictonary to be sent to groupme.
    headers = {'Content-Type' : 'application/json'} #http header
    url = 'https://api.groupme.com/v3/bots/post' #url for posting to groupme
    next_game_string = "Wednesday October 4 @ 7:00 PM on Field 3 agianst Ninja Kittens (IRISH GREEN)" #hardcoded currently for testing, until lonestar gives me API access
    
    #specific logic for bot keywords
    if "schedule" in keyword: #if someone says schedule return text
        dictToSend['text'] = "Hi %s, your next scheduled game is on: %s" % (name, next_game_string)
    elif "standings" in keyword: #if someone says standings return text
        dictToSend['text'] = "Hi %s, you are currently ranked last, you suck" % name
    else: #catchall response
        dictToSend['text'] = "Hi %s, I'm still being built for now please ask me about \'schedule\' and \'standings\'" % name
    
    return requests.post(url, data=json.dumps(dictToSend), headers=headers) #post data to groupme for bot response
    

#app.run(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080))) #CLOUD9 TESTING




#TODO
#DONE - # set 404 handling for '/' or any other path.
# make sure that i only handle posts from groupme, to /leagueapp test with a proxy.
#DONE - # handle the 500 error, view function did not return a response.
# add in WIFE special logic.
# make a lineup function maybe?
# move over to heroku 
# remove the hardcoded IDs and everything.


