# New York Times - Top Stories
*Beyond the headlines: What insights can we uncover from the news displayed in the front page of the world's biggest newspaper?*

----

\
The New York Times provides API endpoints that allow users to get data from their website, including news from a specific period, reviews and the top stories - which is the data source of this project.

This project aims build a pipeline that allow us to get the Top Stories of each day, save then to corresponding data lakers - Bronze, Silver and Gold - and analyze the data to identify recurring topics, build ML models etc.

\
**Credits**

All the data used in this project is provided by the New York Times at https://developer.nytimes.com/.

This project is based in the "Lago do Mago" project built by Teo Me Why. Téo provides free courses about data analytics, engineering and machine learning. I highly recommend his channel for anyone who wants to learn about data, look at https://www.youtube.com/@teomewhy.


## **Project Details**

\
This projects consists in two parts:

\
The first one is a data pipeline created with Databricks and AWS to extract, load and transform the data from de NY Times API into a cleaned and well-structured data that allows us to analyze the top stories displayed in the website.

\
The second part aims to be a Data Analytics and Science project, using the data delivered by the data pipeline to find insights about the news. More details will be added in future updates...


### 1. Data Pipeline

\
The pipeline has been built using the Medallion Architecture. It divides the process in Raw, Bronze, Silver and Gold Data Layers, each one with specific level of cleaning and treatments. The picture bellow illustrates how the workflow has been designed.

\
<img width="1252" height="695" alt="image" src="Pipeline Screenshot.png" />


#### 1.1 Data Layers

\
**1.1.1 Raw Data Layer**

The raw data is extracted ins JSON format from the NY Times API through a Lambda Function scheduled to run daily at 7 p.m (UTC). The data is saved in a S3 Bucket in AWS without additional treatment but the inclusion of the reference date of when the news were extracted.

\
**1.1.2 Bronze Data Layer**

With the raw data saved to S3, we read this data using a Scheduled Job in Databricks. The python code uses Databricks Autoloader to identify new files that have been added to the S3 Bucket, proccess the new data and add then into a Delta Table, adding the ingestion date to it's contents. No further treatments are made

\
**1.1.3 Silver Data Layer**

This is where we start to do some treatments in our data. The columns are renamed for better readbility, the "author" collumn is treated to keep a pattern with the other list columns, and we also remove the columns that won't be useful in our future analysis. The Silver table is updated using the Delta Change Data Feed feature, allowing us to identify changes made to the Bronze table, and processing only this new data into the Silver table, improving running time and costs.

\
**List of Transformations:**


| Bronze || Silver ||
|--|--|--|--|
|Bronze Column Name | Bronze Column Type | Silver Column Name | Silver Column Type |
| title | string | ds_headline | string |
| abstract | string | ds_lead | string |
| byline | string | ds_authors | array |
| section | string | ds_section | string |
| subsection | string | ds_subsection | string |
| url | string | ds_url | string |
| geo_facet | array | ds_locations | array
| des_facet | array | ds_topics | array
| org_facet | array | ds_organizations | array
| perc_facet | array | ds_persons | array
| published_date | string | - | -
| ref_date | string | - | -
| short_url | string | removed | -
| multimedia | array | removed | - 
| item_type | string | removed |-
| kicker | string | removed | -
| material_type_facet | string | removed | -
| created_date | string | removed | - 
| uri | string | removed | - 

\
**1.1.4 Gold Data Layer**

The gold layer aims to serve the analytics proccess, so it contains tables optimized with summarized data. It contains:

- Daily Trending Topics: a simple count of the stories for each topic and day
- Last Month Top Authors: a count of how many stories each author had in the main page in the last 30 days.
- Weekly Trending Persons: a count of how many times each public figure is mentioned in the stories each week
- Last Month Trendings Organizations: a count of how many stories each organizations (enterprises, political parties etc) had in the main page in the last 30 day

Since the Stories's topics,authors and persons are a array-like information, I had to explode it to identify cases where, for an example, an author has worked alonged with others, and so I've counted it as a story for each one of them.

In the coming updates, the code will be refactored the gold layer ingestions keeps a pattern with the other layers.

#### 1.2 Databricks Workflows

*Coming in future updates...*



### 2. Data Analysis

*Coming in future updates...*


