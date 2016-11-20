## Khan Academy ##

Khan Academy is a non-profit that creates educational content.

For further detail, check out

https://www.khanacademy.org/

https://en.wikipedia.org/wiki/Khan_Academy

---
## Khan Academy Static Downloader ##

Khan Academy Static Downloader is a script that uses the Khan Academy API to download all video lectures from their website.

The script then automatically creates a static html website.

## Why make a script and download all the videos? ##

Because the people who need these the most are the people without Internet access

## Why make a 'static' html website? ##

So that the entire video 'library' from Khan Academy can be made available to people using the most minimal piece of hardware.
- A simple WiFi router with a USB port to serve static web-pages
- A flash drive

---

## Demo ## 

Check out https://zubairlk.github.io/ka-static-demo/

## Usage ## 

Run two scripts

	./dl_and_create.py
	./bootstrap.sh

The static HTML website will be availble in the Khan_Academy folder.

Use the in built python webserver to check

	cd Khan_Academy
	python -m SimpleHTTPServer

Then open your browser and go to address localhost:8000

## Todo ##

- Add support for a command line parameter to actually download all videos.
  At the moment, it simply creates a static html website that points to the youtube urls

## Other inspirational projects ##

This work is inspired by the following projects:

- https://www.facebook.com/3kay.pk

- Khan Academy on a Stick http://khan.mujica.org/

- Rachel Plus https://racheloffline.org/

- KA-Lite https://learningequality.org/ka-lite/

---

## Feedback ##

Use the Github Issues tab to submit an issue

Pull requests welcome

---

### License ###

MIT

