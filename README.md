# New York Times - Top Stories
*Beyond the headlines: What insights can we uncover from the news displayed in the front page of the world's biggest newspaper?*

___

##About this project

The New York Times provides API endpoints that allow users to get data from their website, including news from a specific period, reviews and the top stories - which is the data source of this project.

This project aims build a pipeline that allow us to get the Top Stories of each day, save then to corresponding data lakers - Bronze, Silver and Gold - and analyze the data to identify recurring topics, build ML models etc.

**Credits**

All the data used in this project is provided by the New York Times at https://developer.nytimes.com/.

This project is based in the "Lago do Mago" project built by Teo Me Why. Téo provides free courses about data analytics, engineering and machine learning.

His videos can be found at https://www.youtube.com/@teomewhy

##**Project's Architecture**

### Ingestion Pipelines
The Medallion Architecture is the foundation of the data structure of the project.

<img width="1195" height="727" alt="Architecture" src="https://github.com/user-attachments/assets/5326bc02-4b63-4094-86f5-9a1cdfb0a259" />

**1. Raw Data Layer**

The raw data is extracted from the NY Times API through a Lambda Function scheduled to run daily at 19 p.m (UTC). The data is saved in a S3 Bucket in AWS without additional treatments, with the exception of including the reference date which the news were extracted.

**2. Bronze Data Layer**

With the raw data saved to S3, we read this data using a Scheduled Job in Databricks. The python code uses Databricks Autoloader to identify new files that have been added to the S3 Bucket, proccess the new data and add then into a Delta Table, adding the ingestion date to it's contents. No further treatments are made

**3. Silver Data Layer**

*Coming in future updates...*


**4. Gold Data Layer**

*Coming in future updates...*


### Data Analysis
*Coming in future updates...*


