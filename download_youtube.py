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


query = st.text_input("Search YouTube")
order_options = ['date','rating','title','videoCount','viewCount']
selected_order = st.selectbox("Select an Order", order_options)

search_btn = st.button("Search!", key='search')
if st.session_state.get('button') != True:
    st.session_state['button'] = search_btn
if st.session_state['button'] == True:
	nextToken = None
	videoId = []
	channelId = []
	title = []
	publishedAt = []
	description = []
	views = []
	likes = []
	comments = []
	favorites = []
	while True:
		response = youtube.search().list(
			q=query, 
			order=selected_order,
			part='id', 
			type='video', 
			maxResults=50, 
			pageToken=nextToken
		).execute()

		try:
			nextToken = response['nextPageToken']
		except:
			break

		if len(response['items']) > 1000:
			break
	
		ids = [i['id']['videoId'] for i in response['items']]
		response = youtube.videos().list(
			part='statistics, snippet',
			id=ids
		).execute()
		
		batch_length = len([i['id'] for i in response['items']])

		videoId += [i['id'] for i in response['items']]
		channelId += [i['snippet']['channelId'] for i in response['items']]
		title += [i['snippet']['title'] for i in response['items']]
		publishedAt += [i['snippet']['publishedAt'] for i in response['items']]
		description += [i['snippet']['description'] for i in response['items']]
		try:
			views += [i['statistics']['viewCount'] for i in response['items']]
		except:
			views += [0]*batch_length
		try:
			likes += [i['statistics']['likeCount'] for i in response['items']]
		except:
			likes += [0]*batch_length
		try:
			comments += [i['statistics']['commentCount'] for i in response['items']]
		except:
			comments += [0]*batch_length
		try:
			favorites += [i['statistics']['favoriteCount'] for i in response['items']]
		except:
			favorites += [0]*batch_length
	
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
	
	
	


	
	









