CREATE SCHEMA us_census;

CREATE TABLE us_census.poverty_by_zipcode (
    id SERIAL PRIMARY KEY,
    population double precision,
    population_at_or_above_poverty double precision,
    zipcode varchar(10) UNIQUE
);