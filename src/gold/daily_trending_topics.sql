  WITH topics AS (
    SELECT
      ref_date,
      explode(ds_topics) AS topic
    FROM silver.nytimes.top_stories
    WHERE {date_filter}
  )

  SELECT
    ref_date,
    topic,
    COUNT(*) AS stories
  FROM topics
  GROUP BY ref_date, topic
  ORDER BY ref_date DESC, stories DESC