CREATE VIEW us_census.labeled_poverty_rates AS
            (
                        WITH poverty_level_labels AS
                        (
                               SELECT 1              AS id,
                                      'Impoverished' AS poverty_level_label,
                                      0.5            AS MIN,
                                      99             AS MAX
                               UNION
                               SELECT 2              AS id,
                                      'High Poverty' AS poverty_level_label,
                                      0.33           AS MIN,
                                      0.5            AS MAX
                               UNION
                               SELECT 3                AS id,
                                      'Middle Poverty' AS poverty_level_label,
                                      0.1              AS MIN,
                                      0.33             AS MAX
                               UNION
                               SELECT 4             AS id,
                                      'Low Poverty' AS poverty_level_label,
                                      0             AS MIN,
                                      0.1           AS MAX ),
                        population_labels AS
                        (
                               SELECT 1                 AS id,
                                      'High Population' AS population_label,
                                      10000             AS MIN,
                                      99999999          AS MAX
                               UNION
                               SELECT 2                   AS id,
                                      'Medium Population' AS population_label,
                                      500                 AS MIN,
                                      10000               AS MAX
                               UNION
                               SELECT 3                AS id,
                                      'Low Population' AS population_label,
                                      0                AS MIN,
                                      500              AS MAX ),
                        poverty_levels AS
                        (
                               SELECT (population-population_at_or_above_poverty)*1.0/population AS poverty_rate,
                                      zipcode,
                                      population
                               FROM   us_census.poverty_by_zipcode
                               WHERE  population IS NOT NULL
                               AND    population > 0 )
                 SELECT   zipcode,
                          population,
                          poverty_rate,
                          population_label,
                          poverty_level_label
                 FROM     poverty_level_labels pll
                 JOIN     poverty_levels pl
                 ON       pl.poverty_rate >= pll.min
                 AND      pl.poverty_rate < pll.max
                 JOIN     population_labels ppl
                 ON       pl.population >= ppl.min
                 AND      pl.population < ppl.max
                 ORDER BY zipcode
            )