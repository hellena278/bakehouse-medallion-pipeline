# Databricks notebook source
# MAGIC %md
# MAGIC 1- bronze_ingestion

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM samples.bakehouse.media_customer_reviews;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM samples.bakehouse.sales_franchises;

# COMMAND ----------

# MAGIC %md
# MAGIC creating bronze table for customer reviews.

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE IF NOT EXISTS bronze_customer_reviews (
# MAGIC     review STRING,
# MAGIC     franchiseID LONG,
# MAGIC     review_date TIMESTAMP,
# MAGIC     new_id INT
# MAGIC );
# MAGIC SELECT * FROM bronze_customer_reviews
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC Creating bronze table for sales franchise

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE bronze_sales_franchises AS
# MAGIC SELECT * FROM samples.bakehouse.sales_franchises

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM bronze_sales_franchises
# MAGIC

# COMMAND ----------

# MAGIC %md
# MAGIC 02- silver cleaning and join

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE silver_franchise_feedback AS
# MAGIC SELECT 
# MAGIC bronze_customer_reviews.franchiseID,
# MAGIC UPPER (City) AS city,
# MAGIC UPPER (Country) AS country,
# MAGIC TRIM (review) AS review,
# MAGIC review_date AS review_timestamp
# MAGIC FROM bronze_customer_reviews
# MAGIC INNER JOIN bronze_sales_franchises
# MAGIC ON bronze_customer_reviews.franchiseID = bronze_sales_franchises.franchiseID
# MAGIC WHERE review IS NOT NULL
# MAGIC AND review !='';
# MAGIC     
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM silver_franchise_feedback

# COMMAND ----------

# MAGIC %md
# MAGIC 03- gold business aggregations
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE gold_city_feedback AS
# MAGIC SELECT
# MAGIC city,
# MAGIC country,
# MAGIC COUNT (review) AS total_review_received
# MAGIC FROM
# MAGIC silver_franchise_feedback
# MAGIC GROUP BY
# MAGIC city,country
# MAGIC ORDER BY total_review_received DESC
# MAGIC     
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM gold_city_feedback

# COMMAND ----------

# MAGIC %md
# MAGIC NOW the data can be use for analyzing the location and review received from each country and city
# MAGIC