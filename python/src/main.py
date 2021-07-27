from us_census_wrapper import USCensusAPIWrapper
from postgres_wrapper import PostgresWrapper
from us_census_transformer import USCensusTransformer
from field_mappings import TABLES


def collect_load(us_census_wrapper, postgres_wrapper):
    for table in TABLES:
        # Get data from US Census
        census_fields = [f["us_census_field"] for f in table["fields"] if f["retrieve"]]
        data = us_census_wrapper.get_data_for_zipcodes(census_fields)
        # Format data for Postgres
        formatted_data = USCensusTransformer.transform(
            [f["us_census_field"] for f in table["fields"]], data
        )
        # Insert data into Postgres
        result = postgres_wrapper.insert_data(
            table["pg_schema"],
            table["pg_table"],
            [f["pg_field"] for f in table["fields"]],
            formatted_data,
            table["primary_key"],
        )
        print(result)


if __name__ == "__main__":
    # Initialize instances and run
    us_census_wrapper = USCensusAPIWrapper()
    postgres_wrapper = PostgresWrapper()
    collect_load(us_census_wrapper, postgres_wrapper)
