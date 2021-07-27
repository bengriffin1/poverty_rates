from census import Census
import os, logging

# This is a wrapper around the US Census Data python library.
# It assumes the API Key has been set in the environment, or is set in the init override

API_KEY_ENV_VAR = "US_CENSUS_API_KEY"


class USCensusAPIWrapper:
    def __init__(self, api_key=os.getenv(API_KEY_ENV_VAR, None)):
        if api_key == None:
            logging.error(
                "API Key not set! Environment variable {} must be set, or an override must be provided in the class initialization".format(
                    API_KEY_ENV_VAR
                )
            )
        self.census_connector = Census(os.getenv(API_KEY_ENV_VAR))

    def get_data_for_zipcodes(self, fields, zipcodes="*"):
        data = self.census_connector.acs5.zipcode(fields, zipcodes)
        return data

    def search_tables(self, search_term):
        tables = self.census_connector.acs5.tables()
        return_list = []
        for table in tables:
            if search_term in table["description"].lower():
                return_list.append(table)
        if len(return_list) == 0:
            logging.warning("No results found in search")
        return return_list
