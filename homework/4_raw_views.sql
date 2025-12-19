-- Replace <username> with your username (same as used in the notebook)
-- Bucket name: <username>-wikidata
-- Database name: <username>

DROP TABLE IF EXISTS catheloni.raw_views;

CREATE EXTERNAL TABLE catheloni.raw_views (
    title STRING,
    views INT,
    rank INT,
    date STRING,
    retrieved_at STRING
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://catheloni-wikidata/raw-views/';
