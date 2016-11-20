#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This script basically downloads topictree from khan academy
# Then parses it and creates a temporary folder with files.
# Kept simple on purpose to just see how parsing the topic tree json works in python
import json
import pprint
import inspect
import os
import re
import urllib

global_index = 0

#http://stackoverflow.com/questions/3663450/python-remove-substring-only-at-the-end-of-string

def rchop(thestring, ending):
  if thestring.endswith(ending):
    return thestring[:-len(ending)]
  return thestring
#somestring = rchop(somestring, ' rec')

def make_video_file(data, dirname, title, video_index):
	global global_index
#	for key in data:
#		print key

	video_title = re.sub('[^A-Za-z0-9]+', '_', data["translated_title"])

#	for key in data["download_urls"]:
#		print key

	if "mp4-low" in data["download_urls"]:
		download_url = data["download_urls"]["mp4-low"]
	elif "mp4" in data["download_urls"]:
		download_url = data["download_urls"]["mp4"]
	else:
		# Looks like there is a download_urls json that doesn't have a video.
		print "No mp4 or mp4 for some videos"
		print dirname
#		print global_index
		print video_title
		for key in data["download_urls"]:
			print key

		return

	if title == "New_and_noteworthy":
		directory = dirname
	else:
		directory = rchop(dirname , title)

#	print directory
#	directory = re.sub('[^A-Za-z0-9]+', '_', directory)
#	print directory
#	print video_title
#	print title
#	print global_index
#	print video_index

	if data['translated_title'] is not None:
		full_title = data['translated_title'].encode('utf-8')
	else:
		# Use file name
		full_title = video_title

	if data['translated_description'] is not None:
		full_description = data['translated_description'].encode('utf-8')
	else:
		full_description = "No description"

	id = []
	if data['id'] is not None:
		id = data['id']


	if not os.path.exists(directory):
		os.makedirs(directory)

	fp = open(directory + "/" + str(global_index) + "_" + video_title, "wb")

	fp.write("Video Title : ")
	fp.write(full_title + "\n")

	fp.write("Video Description : ")
	fp.write(full_description + "\n")

	fp.write("Download URL : ")
	fp.write(download_url + "\n")

	fp.write("Video ID : ")
	fp.write(id + "\n")

	fp.close()

def list_dict_keys(data, level, dirname, title):
#	print type(data)
	global global_index
	video_index = 0
	base = ("    " * level)
	if type(data) is dict:
		for key in data:
#			print base + key
#			if key == 'title':
			if key == 'translated_title':
				title = re.sub('[^A-Za-z0-9]+', '_', data[key])
				dirname = dirname + "/" + title
#				print base + dirname
#				print base + data[key]
			if key == 'relative_url':
				continue
				print base + data[key]
			if key == 'translated_youtube_id':
				continue
				print base + data[key]
			if key == 'download_urls':
				# Now that we have recursively reached a node with a video
				# Create a folder and file.
				global_index = global_index + 1
#				video_index = video_index + 1
				make_video_file(data, dirname, title, video_index)

#				list_dict_keys(data[key], level, dirname, title)
#			if key == 'mp4':
#				print base + data[key]
			if key == 'children':
				list_members(data[key], level + 1, dirname, title)

def list_list_keys(data):
	if type(data) is dict:
		for key in dict:
			print key 


def list_members(data, level, dirname, title):
	for index, item in enumerate(data):
		if type(data[index]) is dict:
			list_dict_keys(data[index], level, dirname, title)

if not os.path.exists('topictree'):
	print "Downloading Topictree. This can take a while"
	topictree = urllib.urlretrieve("http://www.khanacademy.org/api/v1/topictree", "topictree")

with open('topictree') as data_file:
    data = json.load(data_file)
# print json.dumps(data)

list_dict_keys(data,0, "myfolder", "title")

quit()
