CREATE VIEW catheloni.views AS
    SELECT
        title,
        views,
        date,
        rank,
        cast(from_iso8601_timestamp(retrieved_at) AS TIMESTAMP) as retrieved_at
    FROM catheloni.raw_views
    