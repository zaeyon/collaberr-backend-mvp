import os
import google.oauth2.credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']
API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'


class YouTubeQueryHook:
    """
    Plugin to retrieve YouTube Report for User
    Ex. youtube_hook = YouTubeQueryHook(key, client_id, client_secret, refresh_token)
        query_result = hook.get_query(channel_id, start_date, end_date, metrics, dimensions, sort)
    """
    def __init__(self, key, client_id, client_secret, refresh_token):
        self.service = self.get_service(key, client_id, client_secret, refresh_token)

    def get_service(self, key, client_id, client_secret, refresh_token):
        """
        Initialize API call with given credentials
        key=OAuth access token
        """
        credentials = google.oauth2.credentials.Credentials.from_authorized_user_info(
            {
                'key': key,
                'client_id': client_id,
                'client_secret': client_secret,
                'refresh_token': refresh_token,
            },
            scopes=SCOPES
        )
        return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    def execute_api_request(self, client_library_function, **kwargs):
        response = client_library_function(**kwargs).execute()
        return response

    def get_query(self, channel_id, start_date, end_date, metrics, dimensions, sort):
        """
        ids: channel_id of user
        metrics: metrics for query
        dimenions: time period or others
        """
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
        response = self.execute_api_request(
            self.service.reports().query,
            ids='channel==' + channel_id,
            startDate=start_date,
            endDate=end_date,
            metrics=metrics,
            dimensions=dimensions,
            sort=sort
        )
        return response
