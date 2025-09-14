SELECT
  title AS ds_headline,
  abstract AS ds_lead,
  SPLIT(REPLACE(REPLACE(byline, 'By ', ''), ' and ', ', '), ', ') AS ds_authors,
  section AS ds_section,
  subsection AS ds_subsection,
  url AS ds_url,
  geo_facet AS ds_locations,
  des_facet AS ds_topics,
  org_facet AS ds_organizations,
  per_facet AS ds_persons,
  published_date,
  ref_date AS ref_date
FROM bronze.nytimes.top_stories
