# crypto_temp
Crypto Analysis

Workflow:

![image](https://github.com/user-attachments/assets/98ed60da-4b14-498b-a953-cb6ea453109d)

Data Load:
In order to investigate the correlation between temperature variations and cryptocurrency price fluctuations, we took one year's worth of historical data from:

CoinGecko API: For retrieving cryptocurrency price, market cap, and trading volume data.
Meteostat API: For fetching historical temperature data across four U.S. states.

A Lambda function in Python automates data extraction, with API credentials securely stored as environment variables. The function:
1. Fetches daily crypto and weather data.
2. Stores the raw JSON files in an Amazon S3 bucket.
3. Triggers an AWS Glue Job for transformation and cataloging.t



Data Transformation: AWS Glue
AWS Glue processes the raw data using PySpark, structuring it for analysis.
Raw Data Processing: Extracts essential fields from JSON files:

Crypto Data: crypto_name, price,timestamp.
Weather Data: state, temperature, humidity, timestamp.

1. Flattening nested JSON structures.
2. Standardizing timestamps for data alignment.
3. Cleaning missing or inconsistent values.
Storage: Saves transformed data in Amazon S3  as partitioned parquet files, organized by date and state for efficient querying.



Data Analysis: AWS Athena
AWS Athena enables serverless SQL queries to analyze crypto-weather interactions.
SQL Queries to Identify Correlations:
Crypto price trends vs. temperature: Analyzing how temperature changes across different states align with price fluctuations.
Crypto market volatility: Examining how trading volume and price fluctuations vary across different weather conditions.



Data Visualization: Tableau
Tableau was used to generate the visualizations to analyze crypto-weather interactions.

Visualizations Created:
Crypto Price Trends vs. Temperature: Examines the relationship between daily temperature changes and cryptocurrency price movements.
Crypto Market Volatility: Analyzes trading volume fluctuations in different states under varying temperature conditions.

![image](https://github.com/user-attachments/assets/3bd4174a-f3f5-4f1a-b08f-51c8bfba3b8c)



Key Features:
 Automated Pipeline: End-to-end ETL workflow using AWS services.
 Scalable Analytics: Athena queries enable efficient analysis of large datasets.
 Real-World Insights: Investigating external factors influencing digital asset markets.
 Historical Data Trends: A full year of crypto-weather data analyzed for long-term patterns.

Tools & Technologies Used
   Data Sources: CoinGecko, Meteostat. 
   
   AWS Lambda - Automates API data extraction.
   
   Amazon S3 - Stores raw and processed datasets.
   
   AWS Glue - Processes and catalogs structured data.
   
   AWS Athena - Enables SQL-based analytics.
   
   Tableau - Visualizes data-driven insights.
   
   Python, PySpark - Data transformation and processing.
   
   JSON, CSV - Data formats for storage.
   
   AWS IAM Roles - Secure access management.

This project showcases how temperature variations may influence cryptocurrency price trends and volatility, providing unique insights into external factors affecting digital financial markets. Looking forward to exploring more interdisciplinary data science projects!








