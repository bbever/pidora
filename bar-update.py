#!/usr/bin/env python

import sys, csv, subprocess, os, json, requests
from time import gmtime, strftime

def process(command, new = False):
	if new:
		with open(os.devnull, "w") as fnull: result = subprocess.Popen(command, stdout = fnull, stderr = fnull)
	else:
		with open(os.devnull, "w") as fnull: result = subprocess.call(command, stdout = fnull, stderr = fnull)
def buildJSON(title, artist, album, artURL, loved, explainURL, songDuration = 0, songPlayed = 0):
	data = '{"title": ' + json.dumps(title) + ',"artist": ' + json.dumps(artist) + ',"album": ' + json.dumps(album) + ',"artURL": ' + json.dumps(artURL) + ',"loved": ' + str(bool(loved)).lower() + ',"explainURL": ' + json.dumps(explainURL) + ', "songDuration": ' + str(songDuration) + ', "songPlayed": ' + str(songPlayed) + '}'
	return json.loads(data)
def sendRequest(url, method, songData):
	requests.post(url, params=dict(json=json.dumps(dict(method=method, id=1, songData=songData))))
www = os.path.dirname(os.path.abspath(__file__)) + "/"
url = "http://localhost:8080/api"

event = sys.argv[1]
lines = sys.stdin.readlines()
fields = dict([line.strip().split("=", 1) for line in lines])

artist = fields["artist"]
title = fields["title"]
album = fields["album"]
coverArt = fields["coverArt"]
rating = int(fields["rating"])
detailUrl = fields["detailUrl"].split('?dc')[0]
songDuration = fields["songDuration"]
songPlayed = fields["songPlayed"]

if event == "songstart" or event == "songexplain":
	sendRequest(url, "SetSongInfo", buildJSON(title, artist, album, coverArt, rating, detailUrl))
#elif event == "songfinish":
#	import feedparser
#	feed = feedparser.parse("http://www.npr.org/rss/podcast.php?id=500005")
#	if not os.path.lexists(www + "lastNews"): open(www + "lastNews", "w").write("-1")
#	lastNews = int(open(www + "lastNews", "r").read())
#	currNews = feed.entries[0].updated_parsed.tm_hour
#	currHour = int(strftime("%H", gmtime()))
#	currMin = int(strftime("%M", gmtime()))
#	if currNews != lastNews and currNews == currHour:
#		open(www + "lastNews", "w").write(str(feed.entries[0].updated_parsed.tm_hour))
#		sendRequest(url, "SetSongInfo", buildJSON(feed.entries[0].title, feed.feed.title, feed.feed.title, "http://media.npr.org/images/podcasts/2013/primary/hourly_news_summary.png", 0, None))
#		process(["mpg123", feed.entries[0].id])
elif event == "songlove":
	sendRequest(url, "SetSongInfo", buildJSON(title, artist, album, coverArt, rating, detailUrl))
elif event == "usergetstations" or event == "stationcreate" or event == "stationdelete" or event == "stationrename":				# Code thanks to @officerNordBerg on GitHub
	stationCount = int(fields["stationCount"])
	stations = ""
	for i in range(0, stationCount):
		stations += "%s="%i + fields["station%s"%i] + "|"
	stations = stations[0:len(stations) - 1]
	open(www + "stationList", "w").write(stations)
