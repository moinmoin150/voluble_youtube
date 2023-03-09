import streamlit as st
import pandas as pd
import streamlit.components as stc
import base64
import time
import datetime
import requests
import tweepy
import math

timestr = time.strftime("%Y%m%d-%H%M%S")

class FileDownloader(object):
	def __init__(self, data,filename='myfile',file_ext='txt'):
		super(FileDownloader, self).__init__()
		self.data = data
		self.filename = filename
		self.file_ext = file_ext

	def download_id(self):
		b64 = base64.b64encode(self.data.encode()).decode()
		new_filename = "{}_{}_.{}".format(self.filename,timestr,self.file_ext)
		st.markdown("#### Download Video Data ###")
		href = f'<a href="data:file/{self.file_ext};base64,{b64}" download="{new_filename}">Click Here</a>'
		st.markdown(href,unsafe_allow_html=True)
		
	def download_dta(self):
		b64 = base64.b64encode(self.data.encode()).decode()
		new_filename = "{}_{}_.{}".format(self.filename,timestr,self.file_ext)
		st.markdown("#### Download Tweets ###")
		href = f'<a href="data:file/{self.file_ext};base64,{b64}" download="{new_filename}">Click Here</a>'
		st.markdown(href,unsafe_allow_html=True)
    
 
api_key= st.secrets["password"]
youtube = discovery.build('youtube', 'v3', developerKey=api_key)

