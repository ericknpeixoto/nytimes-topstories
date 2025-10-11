  WITH organizations AS (
    SELECT 
      ref_date,
      explode(ds_organizations) AS organization
    FROM silver.nytimes.top_stories
    WHERE {date_filter}
  )

  SELECT 
    organization, 
    COUNT(*) AS stories,
    CURRENT_DATE() AS ref_date
  FROM organizations
  WHERE organization IS NOT NULL
    AND organization <> ''
  GROUP BY organization
  ORDER BY stories DESC