import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import smtplib, os, sys, socket, codecs
from smtplib import SMTPException
import pandas as pd
from collections import OrderedDict
from datetime import date
import numpy as np 

file_urls = codecs.open('urls.csv','r','utf-8')

sitename1 = []
title1 = []
sitedesc1 = []
expandedurl = []

# Where the output will be stored
filename = "scraping_result.csv"

f = open(filename, "a")
f.seek(0)
f.truncate()

# Setting a fake agent to make google "think" a browser is sending requests
ua = UserAgent()
header = {'user-agent':ua.chrome}

def enrich_url():
	# Enriching part of URLs
	for enrich_url in file_urls:

		try:
			if(len(enrich_url)==0):
				continue
			else:
				# print("______________")

				if(enrich_url[0:5] == "https"):
					if(enrich_url[-1] == "\n"):
						website = requests.get(enrich_url[:-2], headers=header)
					else:
						website = requests.get(enrich_url, headers=header)
				else:
					if(enrich_url[-1] == "\n"):
						website = requests.get("https://" + enrich_url[:-2], headers=header)
					else:
						website = requests.get("https://" + enrich_url, headers=header)

				# We're using html.parser since it's in Python already / no need to extra-install
				soup = BeautifulSoup(website.content, 'html.parser')

				# For URL enrichment, we get the title from meta og:title and the expanded url as well 
				title = soup.find("meta",  property="og:title")
				url = soup.find("meta",  property="og:url")
				sitename = soup.find("meta", property="og:site_name")
				description = soup.find("meta", property="og:description")

				# Checking result
				sitename1.append(sitename["content"])
				title1.append(title["content"])
				sitedesc1.append(description["content"])
				expandedurl.append(url["content"])

				print("Site name: ", sitename["content"] if sitename else "	")
				print("HTML Title: ", title["content"] if title else "	")
				print("Site description: ", description["content"] if description else "	")
				print("Expanded URL: ", url["content"] if url else "	", "\n")

		except:
			# print("URL: ", enrich_url)
			# print("Unverified URL\n")
			# Note: "continue" works on exceptions only if you're in a loop
			continue

	raw_data = {'site_name': sitename1,
				'html_title': title1,
				'site_desc': sitedesc1,
				'expanded_url': expandedurl}

	df = pd.DataFrame(raw_data, columns = ['site_name', 'html_title', 'site_desc', 'expanded_url'])
	# Trying to add duplicates
	# df.drop_duplicates(subset=['site_name','html_title'], keep = False)
	df.to_csv(f)


output = enrich_url()

def read_file():
	file = open('scraping_result.txt')
	data = file.read()
	file.close()
	return data

f.close()