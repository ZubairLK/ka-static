#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This script basically downloads topictree from khan academy
# Then parses it and creates a folder Khan Academy with files.
# Kept simple on purpose to just see how parsing the topic tree json works in python
import json
import pprint
import inspect
import os
import re
import urllib

global_index = 0
global_level = 0

#http://stackoverflow.com/questions/3663450/python-remove-substring-only-at-the-end-of-string

def rchop(thestring, ending):
  if thestring.endswith(ending):
    return thestring[:-len(ending)]
  return thestring
#somestring = rchop(somestring, ' rec')

def make_video_file(data, dirname, title):
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
#		print "No mp4 or mp4 for some videos"
#		print dirname
#		print global_index
#		print video_title
#		for key in data["download_urls"]:
#			print key
		return

	if title == "New_and_noteworthy":
		directory = dirname
	else:
		directory = rchop(dirname , title)
#		directory = dirname + title
#		directory = dirname

#	print directory
#	directory = re.sub('[^A-Za-z0-9]+', '_', directory)
#	print dirname
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

	directory = directory + "/" + title
	if not os.path.exists(directory):
		os.makedirs(directory)

	fp = open(directory + "/" + str(global_index) + "_" + video_title + ".html", "wb")
	fp_head = open("head.html", "rb")
	fp_tail = open("tail.html", "rb")

	fp.write(fp_head.read())
	fp.write("<p>")
	fp.write("Video Title : ")
	fp.write(full_title + "\n")
	fp.write("</p>")

	fp.write("<p>")
	fp.write("Video Description : ")
	fp.write(full_description + "\n")
	fp.write("</p>")


#	fp.write("<p>")
#	fp.write("Download URL : ")
#	fp.write(download_url + "\n")
#	fp.write("</p>")

	fp.write("<video width=\"80%\" controls>")
	fp.write("<source src=" + download_url + " type=\"video/mp4\">")
	fp.write("Your browser does not support HTML5 video. Direct link " + download_url)
	fp.write("</video>")

	fp.write("<p>")
	fp.write("Video ID : ")
	fp.write(id + "\n")
	fp.write("</p>")
	fp.write(fp_tail.read())

	fp.close()

def list_dict_keys(data, level, dirname, title):
#	print type(data)
	global global_index
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
				make_video_file(data, dirname, title)

#				list_dict_keys(data[key], level, dirname, title)
#			if key == 'mp4':
#				print base + data[key]
			if key == 'children':
				# Write some metadata in folder before proceeding to child node.
				if not os.path.exists(dirname):
					os.makedirs(dirname)
				fp = open(dirname + "/metadata", "wb")
				fp.write(data['description'].encode('utf-8'))
				fp.close
				# Enter child node.
				list_members(data[key], level + 1, dirname, title)

def list_members(data, level, dirname, title):
	for index, item in enumerate(data):
		if type(data[index]) is dict:
			list_dict_keys(data[index], level, dirname, title)

def create_index_html(mydirname, dirnames):
#	print mydirname
#	print dirnames
	global global_level
	global_level = global_level + 1
#	print global_level
#	print mydirname
#	print dirnames
	if mydirname.endswith("fonts") is True:
		return
	if mydirname.endswith("css") is True:
		return
	if mydirname.endswith("js") is True:
		return
	fp = open(mydirname + "/index.html", "wb")
	fp_head = open("head.html", "rb")
	fp_tail = open("tail.html", "rb")
	fp.write(fp_head.read())

	if dirnames:
#		print "here"
		for index, item in enumerate(dirnames):
			if dirnames[index] == "fonts":
				continue

			if dirnames[index] == "css":
				continue

			if dirnames[index] == "js":
				continue

#			print mydirname
#			print "    " + dirnames[index]


			fp.write("<div class=\"col-sm-4\">")

			fp.write("<p>")
			fp.write("<a href=" + dirnames[index] + "/index.html" + ">" + dirnames[index] + "</a>")
			fp.write("</p>")

			if dirnames[index] == "New_and_noteworthy":
				fp_meta = open(mydirname + "/" + "/metadata", "r")
			else:
				fp_meta = open(mydirname + "/" + dirnames[index] + "/metadata", "r")

			# Writing description	
			fp.write("<p>")
			fp.write(fp_meta.read())
			fp_meta.close()
			fp.write("</p>")

		        fp.write("</div>")
	else:
#		print "here2"

#		print dirnames
#		print os.listdir( mydirname )
		files = [f for f in os.listdir(mydirname) if os.path.isfile(os.path.join(mydirname, f))]
#		print files

		if mydirname.endswith("New_and_noteworthy"):
			mydirname = rchop(mydirname, "New_and_noteworthy")

		fp_meta = open(mydirname + "/" + "metadata", "r")
		fp.write("<p>")
		fp.write(fp_meta.read())
		fp_meta.close()
		fp.write("</p>")

		for f in files:
			if f == "index.html":
				continue
			if f == "metadata":
				continue
#			print f
			fp.write("<p>")
			fp.write("<a href=" + f + ">" + f + "</a>")
			fp.write("\n")
			fp.write("</p>")


		    # do something
#		files = filter(os.path.isfile, os.listdir( mydirname ) )


	fp.write(fp_tail.read())

def create_index(mydirname):
	mydirname = mydirname + "/Khan_Academy"
	for dirname, dirnames, filenames in os.walk(mydirname):
		create_index_html(dirname, dirnames)

# Main 

if not os.path.exists('topictree'):
	print "Downloading Topictree JSON. Roughly 60+MB. This can take a while"
	topictree = urllib.urlretrieve("http://www.khanacademy.org/api/v1/topictree", "topictree")

print "Downloaded Topic Tree. Now parsing"

with open('topictree') as data_file:
    data = json.load(data_file)
# print json.dumps(data)

list_dict_keys(data,0, ".", "title")
create_index(".")

quit()
