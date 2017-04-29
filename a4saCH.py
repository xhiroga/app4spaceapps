# coding: UTF-8

import re
import random

import os
import requests

import send
import a4saDAO

"""
channel = a4sa
"""

class a4saCH():

    themes = ["earth", "aero", "mars", "solar-system", "space-station", "tech"]
    sugoroku = ["glacier", "hunting", "earthquake", "drought", "mine"]

    def __init__(self):
        self.dao = a4saDAO.a4saDAO()
        self.gen = send.GenJson()

    def switch(self,sender,text):
        if text in ("Yes","Sure"):
            send.send(self.gen.setText(sender, "Me too!!"))
            send.send(self.gen.setOption(sender, "Which category?",self.themes))
        elif text in self.themes:
            elements = self.dao.getAppsByTheme(text)
            send.send(self.gen.setText(sender, "{0}, it's interesting.".format(text)))
            send.send(self.gen.setTestPlaneList(sender, elements))
        elif text in self.sugoroku:
            self.getByWordShowAll(sender,text)
        elif text == ("Hi"):
            send.send(self.gen.setOption(sender, "Are you interested in space apps??",["Yes", "Sure"]))
        else:
            guessed = self.helpMeIBM(text)
            elements = self.dao.getAppsByTheme(guessed)
            print ("help me IBM!")
            send.send(self.gen.setText(sender, "You have an interest in {0}, right?".format(guessed)))
            send.send(self.gen.setTestPlaneList(sender, elements))
        return

    # send all elements by list format
    def getByWordShowAll(self,sender,text):
        elements = self.dao.getAppsByWord(text)
        for i, elm in enumerate(elements):
            if i%3 == 0:
                print ("amari 0")
                data = self.gen.returnPlaneListNoElements(sender)
            tmp = self.gen.returnPlaneListElement(elm["title"], elm["image_url"], elm["subtitle"], elm["url"], elm["fallback_url"])
            data["message"]["attachment"]["payload"]["elements"].append(tmp)
            if i%3 == 2:
                print ("amari 2")
                send.send(data)
                print ("send this...")
                print (data)
        send.send(self.gen.setText(sender, "Wow, total {0} solutions HIT!".format(str(len(elements)))))

    # return theme
    def helpMeIBM(self,text):
        username = os.environ["IBM_NLC_USER"]
        password = os.environ["IBM_NLC_PASS"]
        classifier = os.environ["IBM_NLC_CLSFR"]

        url = "https://gateway.watsonplatform.net/natural-language-classifier/api/v1/classifiers/{}/classify".format(classifier)
        res = requests.get(url, auth=(username,password), params={"text":text})
        return res.json()["top_class"]
