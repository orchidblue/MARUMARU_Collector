"""	MARUMARU COLLECTOR	"""
"""	     	  BY IML  	"""
"""	shin10256|gmail.com   	"""	
"""	shino1025.blog.me    	"""
"""	github.com/iml1111   	"""	

from selenium import webdriver
from bs4 import BeautifulSoup
import re
import sys
import os
import img2pdf
import requests

dirname = os.path.dirname(os.path.realpath('__file__'))
#dirname = os.path.dirname(os.path.realpath(sys.executable))
Comics_Page = "http://wasabisyrup.com"


def Initializing():
	
	os.system('cls')
	print("   |      |         |      |       ||||||")
	print("  | |    | |       ||     | |      |    |     ")
	print(" ||  |  |  ||     ||  |  |  ||     |              ")
	print(" ||   ||   ||     ||   ||   ||     |    |     ")
	print(" ||   ||   ||     ||   ||   ||     ||||||   Ver. 0.2 by IML")

	print("\n$ HI! THIS IS MARUAMRU COLLECTOR! $\n")
	mode = input("[*] MODE is All or Single ?(a/s) ")
	return mode



def URLparser(URL):
	print("[*] Chrome Driver Starting...")
	print("-------------------------------------\n")
	driver = webdriver.Chrome('./chromedriver')
	driver.set_window_size(600, 400)
	driver.implicitly_wait(1)
	driver.get(URL)
	return driver



def MultiCollect(driver):
	bs0bj = BeautifulSoup(driver.page_source, "html.parser")
	Allcomics =bs0bj.findAll("a",{"href":re.compile("http://www.shencomics.com/archives/.*")})\
		     +bs0bj.findAll("a",{"href":re.compile("http://www.yuncomics.com/archives/.*")})\
		     +bs0bj.findAll("a",{"href":re.compile("http://wasabisyrup.com/archives/.*")})
	Comic_count = 1
	Comic_total = len(Allcomics)	     

	for url in Allcomics:
		drv = URLparser(url.attrs['href'])
		SingleCollect(drv,Comic_count,Comic_total)
		Comic_count += 1
		drv.close()



def SingleCollect(driver,Comic_count,Comic_total):
	print("[*] URL Parsing & Web Crawling...")
	bs0bj = BeautifulSoup(driver.page_source, "html.parser")
	comic_title = Collecting(driver.current_url,bs0bj,Comic_count,Comic_total)

	if comic_title == "Protected":
		print("[*] This comic is Protected! Fail!")
	else:
		filelist = makePDF(comic_title)
		Removing(filelist)



def Collecting(curl,bs0bj,Comic_count,Comic_total):
	os.system('cls')
	print("< Current Progress >")
	print("Total: " + str(Comic_count) + " / " + str(Comic_total))

	protect = bs0bj.find("h2")
	if protect != None :
		return protect.get_text()

	comic_title = bs0bj.find("div",{"class":"article-title"}).attrs['title']
	title_filter = '\\/<>:?!*"|'
	comic_title = comic_title.translate({ ord(x): y for (x, y) in zip(title_filter, "          ") })

	comic_images = bs0bj.findAll("img")
	count = 1

	for img in comic_images:
		imgurl = Comics_Page + img.attrs['data-src']
		imgfile = dirname + "\\" + comic_title + "_(" + "%04d" % count + ").jpg"
		count = count + 1

		print("\n# Link: " + imgurl)
		for i in range(3):
			print("||\t\t\t||\t\t\t||\t\t\t||")
		print("# Downloading to ->  " + imgfile)
		download(curl,imgurl,imgfile)

		os.system('cls')
		print("< Current Progress >")
		print("# Total: " + str(Comic_count) + " / " + str(Comic_total))
		print("# Collecting " + comic_title + "\n# Progress:[", end='')
		for i in range(13):
			if (i / 13) <= (count / len(comic_images)):
				print("ㅁ", end ='')
			else:
				print("   ", end='')
		print(' ]')
		print("Browser: Chrome")

	return comic_title



def download(url,imgurl, file_name):
	header = {
			"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)\
			AppleWebKit 537.36 (KHTML, like Gecko) Chrome",
			"Accept":"text/html,application/xhtml+xml,application/xml;\
			q=0.9,imgwebp,*/*;q=0.8",
			"Referer": url}

	session = requests.Session()
	req = session.get(imgurl, headers = header)

	with open(file_name, "wb") as file:
		file.write(req.content)



def makePDF(comic_title):
	try:
		with open(comic_title + ".pdf", "wb") as f:
			f.write(img2pdf.convert([i for i in os.listdir(dirname) if i.endswith(".jpg")]))
		print("[*] Combing to PDF file.")
	except:
		print("[*] PDF File Can't Make.")
		print("[*] Program Down!")
		sys.exit(1)

	return os.listdir(dirname)



def Removing(filelist):
	for file in filelist:
		path = os.path.join(dirname, file)
		if path.endswith(".jpg"):
			os.remove(path)
	print("[*] Removing image files.")



if __name__ == '__main__':

	mode = Initializing()

	if mode != 'a' and mode != 's':
		print("[*] plz right command.")
		sys.exit(1)

	URL = input("[*] Please input URL(only MARUMARU): ")
	driver= URLparser(URL)

	if mode == 's':
		SingleCollect(driver,1,1)
	else:
		MultiCollect(driver)

	print("[*] Closing Chrome..")
	driver.close()
	print("[*] Complete!")
