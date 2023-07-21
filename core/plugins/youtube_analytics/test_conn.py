from query import YouTubeQueryHook
from report import YouTubeReportHook
import argparse
import json
import logging

logger = logging.getLogger(__name__)

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


# credentials = {
#     'key': '',
#     'client_id': '',
#     'client_secret': '',
#     'refresh_token': '',
# }

f = open('youtube_credential_secret.json')
credentials = json.loads(f.read())

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
# print(yt_report_hook.get_report_types())
# yt_report_hook.create_reporting_job('channel_demographics_a1', 'Channel Demographics')
job_info = yt_report_hook.list_reporting_jobs()
print(job_info)
report_info = []
for job in job_info:
    job_id = job['id']
    report_url_info = yt_report_hook.retrieve_reports(job_id=job_id)
    for report_url in report_url_info:
        report_info.append({
            'job_id': job_id,
            'name': job['name'],
            'report_type': job['report_type'],
            'report_url': report_url['report_url'],
            'start_time': report_url['start_time'],
            'end_time': report_url['end_time'],
        })
print(report_info)

#     report_urls = yt_report_hook.retrieve_reports(job_id=job_id)
#     print(report_urls)
    # for report_url in report_urls:

# yt_report_hook.retrieve_reports(
#     job_id='f30b7cfe-bc68-4195-a533-e64389538ae5')
# print(query_result)
