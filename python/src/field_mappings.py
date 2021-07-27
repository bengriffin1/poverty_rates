# This file contains mappings between US Census Field Names and Postgres Tables
# If additional tables from US Census are needed, add them here
# "retrieve" flags whether this field needs to be requested from US Census (some fields are default returned)

TABLES = [
    {
        "pg_schema": "us_census",
        "pg_table": "poverty_by_zipcode",
        "us_census_data_set": "acs5",
        "primary_key": "zipcode",
        "fields": [
            {
                "pg_field": "population",
                "us_census_field": "B17020_001E",
                "retrieve": True,
            },
            {
                "pg_field": "population_at_or_above_poverty",
                "us_census_field": "B17020_010E",
                "retrieve": True,
            },
            {
                "pg_field": "zipcode",
                "us_census_field": "zip code tabulation area",
                "retrieve": False,
            },
        ],
    }
]
