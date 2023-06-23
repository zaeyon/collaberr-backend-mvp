import os
import google.oauth2.credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.http import JsonResponse

# Set up your OAuth 2.0 client credentials
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']
API_SERVICE_NAME = 'youtubeAnalytics'
API_VERSION = 'v2'


def get_youtube_analytics_data(request):
    # Load the stored credentials for the authorized channel owner
    stored_credentials = get_stored_credentials(request.user.id)
    if stored_credentials is None:
        return JsonResponse({'error': 'Authorization credentials not found.'}, status=401)

    # Build the YouTube Analytics API service
    credentials = google.oauth2.credentials.Credentials.from_authorized_user_info(stored_credentials, SCOPES)
    youtube_analytics = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    try:
        # Make API requests to retrieve YouTube Analytics data
        response = youtube_analytics.reports().query(
            ids='channel==MINE',
            startDate='2023-01-01',
            endDate='2023-01-31',
            metrics='views,comments,likes,dislikes,shares',
            dimensions='day'
        ).execute()

        # Process the API response and return the data
        analytics_data = process_analytics_response(response)
        return JsonResponse(analytics_data)

    except HttpError as error:
        return JsonResponse({'error': str(error)}, status=500)
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly']
