import os
import google.oauth2.credentials
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/yt-analytics.readonly',
          'https://www.googleapis.com/auth/yt-analytics-monetary.readonly']
API_SERVICE_NAME = 'youtubereporting'
API_VERSION = 'v1'


class YouTubeReportHook:
    """
    Plugin to retrieve YouTube Report for User
    Ex. yt_report_hook = YouTubeReportHook(**credentials)
        yt_report_hook 
    """
    def __init__(self, **kwargs):
        self.service = self.get_service(**kwargs)

    def get_service(self, **kwargs):
        """
        credentials = {
        'key': YOUTUBE_ACCESS_TOKEN,
        'client_id': YOUTUBE_CLIENT_ID,
        'client_secret': YOUTUBE_CLIENT_SECRET,
        'refresh_token': YOUTUBE_REFRESH_TOKEN
        }
        """
        credentials = google.oauth2.credentials.Credentials.from_authorized_user_info(
            {
                'key': kwargs.get('key'),
                'client_id': kwargs.get('client_id'),
                'client_secret': kwargs.get('client_secret'),
                'refresh_token': kwargs.get('refresh_token'),
            },
            scopes=SCOPES
        )
        return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    def remove_empty_kwargs(**kwargs):
        good_kwargs = {}
        if kwargs is not None:
            for key, value in kwargs.iteritems():
                if value:
                    good_kwargs[key] = value
        return good_kwargs

    def get_report_types(self):
        """
        GET default report types
        """
        results = self.service.reportTypes().list().execute()
        reportTypes = results['reportTypes']

        if 'reportTypes' in results and results['reportTypes']:
            for reportType in reportTypes:
                print(f"Report type id: {reportType['id']} name: {reportType['name']}")
        else:
            print('No report types found')
            return False

        return True

    def create_reporting_job(self, report_type_id, report_name):
        """
        Select a desired report type and name
        """
        reporting_job = self.service.jobs().create(
            body=dict(
                reportTypeId=report_type_id,
                name=report_name,
            )
        ).execute()

        print('Reporting job "%s" created for reporting type "%s" at "%s"'
              % (reporting_job['name'], reporting_job['reportTypeId'], reporting_job['createTime']))

    def list_reporting_jobs(self):
        """
        List all jobs for the current account
        """
        # Potentially, return list of job_ids
        results = self.service.jobs().list().execute()

        if 'jobs' in results and results['jobs']:
            jobs = results['jobs']
            for job in jobs:
                print('Reporting job id: %s\n name: %s\n for reporting type: %s\n'
                      % (job['id'], job['name'], job['reportTypeId']))
        else:
            print('No jobs found')
            return False

        return True

    def retrieve_reports(self, job_id):
        """
        Get reports within the job
        """
        try:
            results = self.service.jobs().reports().list(
                jobId=job_id,
                onBehalfOfContentOwner=''
            ).execute()
            if 'reports' in results and results['reports']:
                reports = results['reports']
                for report in reports:
                    print('Report dates: %s to %s\n       download URL: %s\n'
                          % (report['startTime'], report['endTime'], report['downloadUrl']))
            else:
                print("No reports found.")
        except Exception as e:
            print(f"An error occurred: {str(e)}")
