  WITH authors AS (
    SELECT 
      ref_date,
      explode(ds_authors) AS author
    FROM silver.nytimes.top_stories
    WHERE {date_filter}
  )

  SELECT 
    author, 
    COUNT(*) AS stories,
    CURRENT_DATE() AS ref_date
  FROM authors
  WHERE author IS NOT NULL
    AND author <> ''
  GROUP BY author
  ORDER BY stories DESC