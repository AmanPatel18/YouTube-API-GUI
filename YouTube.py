import os
import re
from googleapiclient.discovery import build
from datetime import timedelta

class YouTube:

    # creating service object for YouTube API in constructor
    def __init__(self):
        api_key=os.environ.get('youtube_api')
        self.service= build('youtube','v3',developerKey=api_key)
    
    # function to get the total duration of any playlist
    def playlist_duration(self,pl_id=None):
        
        # defining the regular expressions for matching the hours, minutes and seconds pattern in duration afterwards
        hours_pattern= re.compile(r'(\d+)H')
        minutes_pattern= re.compile(r'(\d+)M')
        seconds_pattern= re.compile(r'(\d+)S')

        total_seconds=0  
        nextPageToken=None
        while True:
            # creating a playlist request for the particular playlist of any channel
            pl_request=self.service.playlistItems().list(
                part='contentDetails',
                playlistId=pl_id,
                maxResults=50,
                pageToken=nextPageToken
            )
            # executing the request and getting the playlist response
            pl_response=pl_request.execute()

            video_id_list=[]
            for item in pl_response['items']:                  # getting the items from the response
                video_id = item['contentDetails']['videoId']   # getting the video id from the playlist
                video_id_list.append(video_id)                 # adding video id into a video id list

            videos=','.join(video_id_list)                     # converting the video id list into a single string
            
            # creating a video request for all the videos in the playlist
            vid_request= self.service.videos().list(part='contentDetails',id=videos)
            # executing the request and getting the response
            vid_response=vid_request.execute()

            for item in vid_response['items']:                 # getting the items from the response
                duration=item['contentDetails']['duration']    # getting the duration for all the videos
                hours=hours_pattern.search(duration)           # getting the hours from the duration
                minutes=minutes_pattern.search(duration)       # getting the minutes from the duration
                seconds=seconds_pattern.search(duration)       # getting the seconds from the duration

                hours=int(hours.group(1)) if hours else 0          # getting the hours as integer from the hours
                minutes=int(minutes.group(1)) if minutes else 0    # getting the miutes as integer from the minutes
                seconds=int(seconds.group(1)) if seconds else 0    # getting the seconds as integer from the seconds
                
                # getting the total seconds from hours,minutes and seconds
                video_seconds=timedelta(hours=hours,minutes=minutes,seconds=seconds).total_seconds()
                total_seconds+=video_seconds                   # adding those video seconds to total seconds

            nextPageToken=pl_response.get('nextPageToken')     # getting the next page token or number 

            # breaking the loop if we get all the pages from the results
            if not nextPageToken:       
                break
        total_seconds= int(total_seconds)                      # converting total seconds from string to integers

        minutes,seconds=divmod(total_seconds,60)               # getting the minutes and seconds from total seconds
        hours,minutes=divmod(minutes,60)                       # getting the hours and minutes from total seconds
        
        playlist_duration=f'{hours}:{minutes}:{seconds}'
        return playlist_duration                              # returning the playlist dyration
    
    # funtion to get the total subscribers of any channel
    def channel_info(self,ch_id=None,username=None):
            # getting the request from the channel for subscribers
            request=self.service.channels().list(part='statistics,brandingSettings',forUsername=username,id=ch_id)
            
            # executing the request and then getting the response
            data= request.execute()

            # getting the channel title from the response
            try:
                title=data['items'][0]['brandingSettings']['channel']['title']
            except:
                pass
            
            # getting the subscribers count from the response
            try:
                subscribers= data['items'][0]['statistics']['subscriberCount']
            except:
                pass
        
            # returning title and subscribers
            return title,subscribers

    # function to get the  sorted most popular videos in a particular playlist of any channel 
    def popular_videos(self,pl_id=None):
        video_list=[]                                          # videos list for storing the views and links
        nextPageToken=None
        while True:
            # creating a request for the items in the playlist
            pl_request=self.service.playlistItems().list(                
                part='contentDetails',
                playlistId=pl_id,
                maxResults=50,
                pageToken=nextPageToken
            )
            # executing the request to get the response
            pl_response=pl_request.execute()

            video_id_list=[]                                                 # list to store all the video's id
            for item in pl_response['items']:
                video_id = item['contentDetails']['videoId']                 # getting the video id from the item
                video_id_list.append(video_id)                               # addding the video id in the list

            videos=','.join(video_id_list)                             # converting video id list ito a single string
              
            # creating a video request to get the videos
            vid_request= self.service.videos().list(part='statistics',id=videos)
            
            # executing the request to get the response
            vid_response=vid_request.execute()

            for item in vid_response['items']:                     # getting the items from the response
                vid_views=item['statistics']['viewCount']          # getting the viewCount from the
                vid_id=item['id']                                  # getting the id from the video
                yt_link=f'https://youtu.be/{vid_id}'               # creating the lin for the video
                
                # adding the url and view count in the videos list
                video_list.append(                                
                    {
                        'views':int(vid_views),
                        'url':yt_link
                    }
                )

            nextPageToken=pl_response.get('nextPageToken')

            if not nextPageToken:
                break
        # sorting the videos on the basis of views in descending order
        video_list.sort(key=lambda vid:vid['views'],reverse=True)

        # returning the video list
        return video_list