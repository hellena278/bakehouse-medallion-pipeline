# bakehouse-medallion-pipeline
Franchise Customer Feedback Pipeline (Databricks, SQL)

A small medallion-architecture project built on Databricks' samples.bakehouse data. It turns raw customer reviews into a count of reviews per city and country.

Pipeline
Layer	Table	What it does
Bronze	bronze_customer_reviews	Raw copy of the customer reviews
Bronze	bronze_sales_franchises	Raw copy of the franchise list
Silver	silver_franchise_feedback	Drops empty reviews, trims text, upper-cases city and country, joins reviews to franchise locations
Gold	gold_city_feedback	Total reviews received per city and country
Tools

Databricks · SQL · Delta tables · medallion architecture (bronze, silver, gold)
<img width="612" height="297" alt="bakehouse performance dashboard" src="https://github.com/user-attachments/assets/a2b7c140-5173-45b3-b6ef-06d3123d873d" />
