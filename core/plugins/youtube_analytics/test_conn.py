from youtube_analytics import YouTubeQueryHook
from youtube_reports import YouTubeReportHook
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--content-owner', default='',
                    help='ID of content owner for which you are retrieving jobs and reports.')
parser.add_argument('--include-system-managed', default=True,
                    help='Whether the API response should include system-managed reports')
parser.add_argument('--name', default='',
                    help='Name for the reporting job. The script prompts you to set a name ' +
                         'for the job if you do not provide one using this argument.')
parser.add_argument('--report-type', default=None,
                    help='The type of report for which you are creating a job.')
args = parser.parse_args()

credentials = {
    'key': '',
    'client_id': '',
    'client_secret': '',
    'refresh_token': '',
}

query_params = {
    'channel_id': '',
    'start_date': '2022-01-01',
    'end_date': '2022-01-20',
    'metrics': 'views',
    'dimensions': 'day',
    'sort': 'day',
}

yt_report_hook = YouTubeReportHook(**credentials)
# query_result = youtube_hook.get_query(**query_params)
# yt_report_hook.get_report_types()
# yt_report_hook.create_reporting_job('channel_traffic_source_a2', 'Traffic Source')
# yt_report_hook.list_reporting_jobs()
# yt_report_hook.retrieve_reports(
#     job_id='')
# print(query_result)
