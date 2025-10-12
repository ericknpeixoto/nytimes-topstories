  WITH persons AS (
    SELECT
      ref_date,
      weekofyear(ref_date) AS week_number,
      explode(ds_persons) AS person
    FROM silver.nytimes.top_stories
    WHERE {date_filter}
  ),

  week_period AS (
    SELECT
      week_number,
      MIN(ref_date) AS week_start,
      MAX(ref_date) AS week_end
    FROM persons
    GROUP BY week_number
  )

  SELECT
    p.week_number,
    week_start,
    week_end,
    concat(
      split_part(regexp_replace(person, '\\s\\(\\d\\d\\d\\d\\-?.?.?.?.', ''), ',', '2'),
      ' ',
      split_part(regexp_replace(person, '\\s\\(\\d\\d\\d\\d\\-?.?.?.?.', ''), ',', '1')
    ) AS person,
    COUNT(*) AS mentions,
    week_end AS ref_date
  FROM persons p
  INNER JOIN week_period ON p.week_number = week_period.week_number
  GROUP BY p.week_number, week_start, week_end, person
  ORDER BY week_number DESC, mentions DESC