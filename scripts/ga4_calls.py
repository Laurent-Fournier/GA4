#!/usr/bin/env python
"""
Documentation
https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema
https://analytics.google.com/analytics/web/

Installation
pip install google-analytics-data
pip install python-dotenv
pip install mysql-connector-python
pip install mysqlclient

Usage : 
cd ~/www/ga4_site/
source env/bin/activate
python scripts/ga4_calls.py --website=jenniferperseverante
python scripts/ga4_calls.py --website=transbeaute
"""

import argparse
import csv
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
        self.is_connected = False

        load_dotenv()  # load variables from .env
        
        # Get the current script's directory path
        self.current_path = os.path.abspath(os.path.dirname(sys.argv[0]))
        
        self.connexion = mysql.connector.connect(
            host = os.getenv('DB_HOST'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            database = os.getenv('DB_NAME'),
        )
        self.connexion.autocommit = False
        self.cursor = self.connexion.cursor(dictionary=True, buffered=True)
        self.is_connected = True
        print(f"Connected to database {os.getenv('DB_NAME')}")

    def db_getOne(self, sql):
        if self.is_connected:
            self.cursor.execute(sql)
            if self.cursor.rowcount == 0:
                return None
            else:
                return self.cursor.fetchone()[self.cursor.column_names[0]]
    def db_execute(self, sql):
        if self.is_connected:
            try:
                print(f" {sql}")
                self.cursor.execute(sql)
                self.connexion.commit()
            except Exception as err:
                print('------ ERROR ------')
                print('[SQL ERROR] %s' % sql)
                print(err.msg)
                print(err.args)
                print('---------------')
                quit()           


    def convert_date(self, s: str) -> str:
        """
        Converts a date string from 'YYYYMMDD' format to 'YYYY-MM-DD'.
        Sample: 20241209 -> 2024-12-09

        :param s: String representing a date in 'YYYYMMDD' format.
        :return: String in 'YYYY-MM-DD' format.
        :raises ValueError: If the input does not match the expected format.
        """
        if not isinstance(s, str) or len(s) != 8 or not s.isdigit():
            raise ValueError("Input must be an 8-digit string in the 'YYYYMMDD' format.")

        return f'{s[:4]}-{s[4:6]}-{s[6:]}'
    

    def getRequests(self, table_name, dimension_names, dimension_values, metric_names, metric_values):
        """
        Generates SQL queries for checking existence, inserting, and updating Google Analytics data in a table.

        :param table_name: Name of the table to query.
        :param dimension_names: List of dimension column names.
        :param dimension_values: List of values corresponding to the dimensions.
        :param metric_names: List of metric column names.
        :param metric_values: List of values corresponding to the metrics.
        :return: Dictionary containing 'Exists', 'Insert', and 'Update' SQL queries.
        """
        queries = {
            'exists': '',
            'insert': '',
            'update': '',
        }

        # 1°) Construct the "exists" query
        where_clauses = []
        for i, dimension_name in enumerate(dimension_names):
            value = dimension_values[i]

            # Format specific fields if necessary
            if dimension_name == 'date':
                value = f'"{self.convert_date(value)}"'
            elif dimension_name in ['pagePathPlusQueryString', 'sessionDefaultChannelGrouping', 'pageReferrer', 'sessionSource', 'deviceCategory']:
                value = f'"{value}"'
            where_clauses.append(f'{dimension_name}={value}')
            i += 1
        where_condition = ' AND '.join(where_clauses)

        queries['exists'] = (
          f'SELECT COUNT(*) AS nb FROM {table_name} WHERE account_id={self.account_id} AND {where_condition}'
        )

        # 2°) Construct the "insert" query
        fields = ['`account_id`']
        values = [str(self.account_id)]

        # Add dimensions to fields and values
        for i, dimension_name in enumerate(dimension_names):
            value = dimension_values[i]

            if dimension_name == 'date':
                value = f'"{self.convert_date(value)}"'
            elif dimension_name in ['pagePathPlusQueryString', 'sessionDefaultChannelGrouping', 'pageReferrer', 'sessionSource', 'deviceCategory']:
                value = f'"{value}"'

            fields.append(f'`{dimension_name}`')
            values.append(value)

        # Add metrics to fields and values
        for i, metric_name in enumerate(metric_names):
            fields.append(f'`{metric_name}`')
            values.append(str(metric_values[i]))

        queries['insert'] = (
            f'INSERT INTO {table_name} ({", ".join(fields)}) '
            f'VALUES ({", ".join(values)})'
        )

        # Construct the "update" query
        set_clauses = []
        for i, metric_name in enumerate(metric_names):
            value = metric_values[i]
            set_clauses.append(f'`{metric_name}`={value}')

        where_clauses = []
        for i, dimension_name in enumerate(dimension_names):
            value = dimension_values[i]
            if dimension_name == 'date':
                value = f'"{self.convert_date(value)}"'
            elif dimension_name in ['pagePathPlusQueryString', 'sessionDefaultChannelGrouping', 'pageReferrer', 'sessionSource', 'deviceCategory']:
                value = f'"{value}"'

            where_clauses.append(f'`{dimension_name}`={value}')

        queries['update'] = (
            f'UPDATE {table_name} '
            f'SET {", ".join(set_clauses)} '
            f'WHERE account_id={self.account_id} AND {" AND ".join(where_clauses)}'
        )
        return queries

    # ----------------------------------
    # Execute a specific GA4 API call
    # ----------------------------------
    def run_report(self, client, ga4_call):
        """
        Executes a GA4 API call, processes the response, and updates the database.

        :param client: GA4 client to execute the API request.
        :param google_analytics_call: Dictionary containing API call parameters.
        """
        table_name = ga4_call['table_name']

        # Prepare dimensions
        dimension_objects = []
        dimension_names = []
        for dimension_name in ga4_call['dimensions']:
            dimension_objects.append(Dimension(name=dimension_name))
            dimension_names.append(dimension_name)

        # Prepare metrics
        metric_objects = []
        metric_names = []
        for metric_name in ga4_call['metrics']:
            metric_objects.append(Metric(name=metric_name))
            metric_names.append(metric_name)

        # Create and execute the GA4 API report request
        request = RunReportRequest(
            property=f"properties/{self.ga4_property_id}",
            dimensions=dimension_objects,
            metrics=metric_objects,
            date_ranges=[
                DateRange(
                    start_date=ga4_call['date_ranges']['start'],
                    end_date=ga4_call['date_ranges']['end']
                )
            ],
        )
        response = client.run_report(request)

        # Optional: Display the results in the logs
        print("Report result:")
        for row in response.rows:
            row_values = " | ".join(
                [x.value for x in row.dimension_values] +
                [x.value for x in row.metric_values]
            )
            # print(row_values + " |")

        # populate database

        # Handle database truncation if required
        if ga4_call.get('with_truncate', 0) == 1:
            delete_query = f'DELETE FROM {table_name} WHERE account_id={self.account_id}'
            self.db_execute(delete_query)

        # Process each row in the report response
        for row in response.rows:
            # Extract dimension and metric values
            dimension_values = [x.value for x in row.dimension_values]
            metric_values = [x.value for x in row.metric_values]

            # Generate SQL queries for database updates
            requests = self.getRequests(table_name, dimension_names, dimension_values, metric_names, metric_values)
            print(f'SQL: {requests}')

            # Determine if data exists; update or insert accordingly
            if self.db_getOne(requests['exists']) == 1:
                print(f"Executing update: {requests['update']}")
                self.db_execute(requests['update'])
            else:
                print(f"Executing insert: {requests['insert']}")
                self.db_execute(requests['insert'])

                if self.db_getOne(requests['exists']) == 1:
                    print(requests['update'])
                    self.db_execute(requests['update'])
                else:
                    print(requests['insert'])
                    self.db_execute(requests['insert'])

        # Generate a CSV file with the report data (optional)
        csv_filename = f"{self.current_path}/data/{ga4_call['csv_filename']}"
        with open(csv_filename, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)

            # Write column headers
            column_names = dimension_names + metric_names
            writer.writerow(column_names)

            # Write row data
            for row in response.rows:
                row_values = []
                for i, x in enumerate(row.dimension_values):
                    if column_names[i] == 'date':
                        row_values.append(self.convert_date(x.value))
                    else:
                        row_values.append(x.value)
                row_values.extend(x.value for x in row.metric_values)
                writer.writerow(row_values)

        print(f"CSV file generated: {csv_filename} with {len(response.rows)} rows.")


    
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
        # - Daily Active Users, sessions,
        # - Pages vues par les utilisateurs
        # - Nombre de sessions par date et type de source (Organic Search, Direct, Organic Social, Referral, Organic Video, Paid Search...)
        # - Referers
        # - Sources
        # - Requêtes de recherche naturelle Google
        
        for key, ga4_call in self.ga4_calls.items():
            table_name = ga4_call['table_name']

            # 1°) Run reports
            if ga4_call.get('is_active', 0) != 1:
                pass
                # print(f"--- Skipping inactive call for table: {table_name}")
            else:
                print(f"--- Execute ga4 call for table '{table_name}' : {ga4_call['description']}")
                self.run_report(client, ga4_call)
            
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