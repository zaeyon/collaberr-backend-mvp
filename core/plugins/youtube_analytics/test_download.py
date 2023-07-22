# from query import YouTubeQueryHook
from report import YouTubeReportHook
import json
import logging
from pathlib import Path
import time

logger = logging.getLogger(__name__)
base_dir = Path(__file__).resolve().parent.parent.parent.parent
f = open(base_dir / 'youtube_credential_secret.json')
credentials = json.loads(f.read())

yt_report_hook = YouTubeReportHook(**credentials)
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
            'start_time': report_url['start_time'][:10],
            'end_time': report_url['end_time'][:10],
        })
print(report_info)
# data_dir = base_dir / 'data'
# for report in report_info:
#     yt_report_hook.download_report(report_url=report['report_url'],
#                                    local_file=f'{data_dir}/{report["report_type"]}/{report["start_time"]}.csv')
#     time.sleep(15)
