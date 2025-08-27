# New York Times - Top Stories
The New York Times provides API endpoints that allow users to get data from their website, including news from a specific period, reviews and the top stories - which is the data source of this project.

Data provided by the New York Times at https://developer.nytimes.com/.

This project aims build a pipeline that allow us to get the Top Stories of each day, save then to corresponding data lakers - Bronze, Silver and Gold - and analyze the data to identify recurring topics, build ML models etc. 

**Project's Architecture**

This first version includes an Lambda Function that runs once a day até 14 p.m to get the top stories from the API, and save then to a S3 Bucket in AWS. The data is then readed by a Scheduled Job in Databricks, that identifies when a new file has been added to the Bucket, and triggers a Python code that compiles all the files in the bucket and save then into a Delta Table in a Bronze Layer dataset.


<img width="1195" height="727" alt="Architecture" src="https://github.com/user-attachments/assets/5326bc02-4b63-4094-86f5-9a1cdfb0a259" />


**Backlog**

- Implement an incremental update in the bronze layer
- Build silver and gold layers

