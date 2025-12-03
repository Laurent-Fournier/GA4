#!/usr/bin/env python
"""
Documentation
https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema
https://analytics.google.com/analytics/web/

Installation
pip install google-analytics-data
pip install python-dotenv
pip install mysql-connector-python

Usage : 
cd ~/www/ga4/
source env/bin/activate
python scripts/ga4_calls.py --website=jenniferperseverante
python scripts/ga4_calls.py --website=transbeaute
"""

import argparse
import json
import os
import sys
import time
import mysql.connector

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (DateRange, Dimension, Metric, MetricType, RunReportRequest)

from dotenv import load_dotenv

class GA4:
    def __init__(self):

        load_dotenv()  # load variables from .env
        
        # Get the current script's directory path
        self.current_path = os.path.abspath(os.path.dirname(sys.argv[0]))
        
        self.connexion = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME'),
        )
        self.cursor = self.connexion.cursor(dictionary=True)


    # ----------------------------------
    # Execute a specific GA4 API call
    # ----------------------------------
    def run_report(self, client, google_analytics_call):
        print('run_report...')

    
    # ----------------------------
    # Process all GA4 API calls
    # ----------------------------
    def process_calls(self, website):
        """
        Processes all configured GA4 API calls for a specific website.
        :param website: The identifier of the website whose data should be processed.
        """
        print(f"Start Processing GA4 calls for website '{website}'")
        print(f"Current path : {self.current_path}")
        
        # 1°) Load GA4 Calls setup file
        ga4_calls_file = f'{self.current_path}/conf/ga4_calls.json'
        print(f"GA4 calls file: {ga4_calls_file}")
        with open(ga4_calls_file, 'r') as file:
            self.ga4_calls = json.load(file)        

        # 2°) Load website-specific configuration
        website_config_file = f'{self.current_path}/conf/{website}.json'
        with open(website_config_file, 'r') as config_file:
            config_data = json.load(config_file)
            self.account_id = config_data["account_id"]
            self.site_name = config_data["site_name"]
            self.site_url = config_data["site_url"]
            self.ga4_property_id = config_data["ga4_property_id"]
            self.ga4_credential_filename = config_data["ga4_credential_filename"]

        # 3°) Set GA4 API credentials
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f'{self.current_path}/conf/{self.ga4_credential_filename}'
        client = BetaAnalyticsDataClient()

        # Iterate through all configured GA4 API calls
        for key, google_analytics_call in self.ga4_calls.items():
            table_name = google_analytics_call['table_name']
            print(f"Processing table: {table_name}")

            if google_analytics_call.get('is_active', 0) != 1:
                print(f"--- Skipping inactive call for table: {table_name}")
            else:
                print(f"--- Executing active call for table: {table_name}")
                self.run_report(client, google_analytics_call)
                
            for key, google_analytics_call in self.ga4_calls.items():
                print(google_analytics_call['table_name'])
                if google_analytics_call['is_active'] != 1:
                    print('--- inactive')
                else:
                    print('--- active')
                    # --------------------------------------------
                    print('------> run_report')
                    #self.run_report(client, google_analytics_call)
                    # --------------------------------------------

            
        print('✅ GA4 processed successfully!') 

    
    # -----------
    # Run !!
    # -----------
    def run(self):
        """
        Main function to execute GA4 API calls for traffic data.
        This function handles logging setup, argument parsing, and processes the specified website configuration.
        """
        # Start time tracking for execution duration
        start_time = time.time()

        # Parse script arguments
        parser = argparse.ArgumentParser(
            description="run GA4 API calls",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        parser.add_argument("-w", "--website", default="UNKNOWN", help="Website config filename")
        args = parser.parse_args()

        # Check if a valid website config filename is provided
        if args.website == 'UNKNOWN':
            print('[ERROR] Need a config filename')
            quit()
        else:
            self.process_calls(args.website)  # process GA4 calls

        # Calculate and log the total execution time
        interval = time.time() - start_time
        print(f'Total time execution: {round(interval / 60, 1)} minutes')



if __name__ == "__main__":
    GA4().run()