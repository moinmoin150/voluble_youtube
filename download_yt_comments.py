import streamlit as st
import pandas as pd
import streamlit.components as stc
import base64
import time
from googleapiclient import discovery




timestr = time.strftime("%Y%m%d-%H%M%S")

class FileDownloader(object):
	def __init__(self, data,filename='myfile',file_ext='txt'):
		super(FileDownloader, self).__init__()
		self.data = data
		self.filename = filename
		self.file_ext = file_ext

	def download_data(self):
		b64 = base64.b64encode(self.data.encode()).decode()
		new_filename = "{}_{}_.{}".format(self.filename,timestr,self.file_ext)
		st.markdown("#### Download Video Data ###")
		href = f'<a href="data:file/{self.file_ext};base64,{b64}" download="{new_filename}">Click Here</a>'
		st.markdown(href,unsafe_allow_html=True)
    
 
api_key= st.secrets["api_key"]
youtube = discovery.build('youtube', 'v3', developerKey=api_key)


video_id = st.text_input("Enter a Video ID")

search_btn = st.button("Search!", key='search')
if st.session_state.get('button') != True:
    st.session_state['button'] = search_btn
if st.session_state['button'] == True:
	nextToken = None
	commentID = []
	text = []
	author = []
	publishedAt = []
	updatedAt = []
	likes = []
	replyCount = []
	category = []
	parent_id = []
	while True:
		response = youtube.commentThreads().list(
			part='id,snippet,replies', 
			videoId=video_id,
			pageToken=next_results,
			maxResults = 100,
			fields="nextPageToken,items(id,snippet(topLevelComment(snippet(publishedAt,updatedAt,likeCount,textOriginal,authorDisplayName)),totalReplyCount),replies)"
    		).execute()

		batch_length = len([i['id'] for i in response])

		commentID += [i['id'] for i in response]
		text += [i['snippet']['topLevelComment']['snippet']['textOriginal'] for i in response]
		author += [i['snippet']['topLevelComment']['snippet']['authorDisplayName'] for i in response]
		publishedAt += [i['snippet']['topLevelComment']['snippet']['publishedAt'] for i in response]
		updatedAt += [i['snippet']['topLevelComment']['snippet']['updatedAt'] for i in response]
		try:
			likes += [i['snippet']['topLevelComment']['snippet']['likeCount'] for i in response]
		except:
			likes += [0]*batch_length
		try:
			replyCount += [i['snippet']['totalReplyCount'] for i in response]
		except:
			replyCount += [0]*batch_length
		category += ['top level comments']*batch_length
		parent_id += ['NA']*batch_length
		
		for i in response:
			if i['snippet']['totalReplyCount']>0:
				commentID += [j['id'] for j in i['replies']['comments']]
				text += [j['id'] for j in i['replies']['comments']]
				author += 
				publishedAt +=
				updatedAt += 
				category += ['replies to comments']
				
		try:
			nextToken = response_id['nextPageToken']
		except:
			break

		if len(views) > 1000:
			break
	
	df = pd.DataFrame({
	    'videoId':videoId,
	    'channelId':channelId,
	    'URL':['https://www.youtube.com/watch?v='+str(i) for i in videoId],
	    'title':title,
	    'publishedAt':publishedAt,
	    'description':description,
	    'views':views,
	    'likes':likes,
	    'comments':comments,
	    'favorites':favorites
	})
	st.write('Found ', len(df), ' results')
	
	st.subheader("Preview first 50 rows:")
	st.dataframe(df.head(50))
	download = FileDownloader(df.to_csv(),file_ext='csv').download_data()
	
	
	


	
	









