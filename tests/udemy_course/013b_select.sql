SELECT
    name,
    population / area AS population_density
FROM cities
WHERE population / area > 6000;
