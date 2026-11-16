-- Databricks notebook source
-- Franchise customer feedback: medallion pipeline (bronze -> silver -> gold)
--
-- Source data: samples.bakehouse (Databricks sample datasets)
-- Tables are created in the notebook's current catalog and schema.

-- COMMAND ----------


-- 0. EXPLORE THE SOURCES
-- ============================================================

SELECT * FROM samples.bakehouse.media_customer_reviews LIMIT 10;

-- COMMAND ----------

SELECT * FROM samples.bakehouse.sales_franchises LIMIT 10;

-- COMMAND ----------

-- Check the exact column names before building the bronze tables
DESCRIBE samples.bakehouse.media_customer_reviews;

-- COMMAND ----------


-- 1. BRONZE: raw copies of the source tables
-- ============================================================

-- Customer reviews
CREATE OR REPLACE TABLE bronze_customer_reviews AS
SELECT
    review,
    franchise_id AS franchiseID,   -- if DESCRIBE shows franchiseID, remove the alias
    review_date,
    new_id
FROM samples.bakehouse.media_customer_reviews;

-- COMMAND ----------

-- Franchises
CREATE OR REPLACE TABLE bronze_sales_franchises AS
SELECT * FROM samples.bakehouse.sales_franchises;

-- COMMAND ----------

-- Check: both tables should contain rows
SELECT 'bronze_customer_reviews' AS table_name, COUNT(*) AS row_count FROM bronze_customer_reviews
UNION ALL
SELECT 'bronze_sales_franchises', COUNT(*) FROM bronze_sales_franchises;

-- COMMAND ----------

-- ============================================================
-- 2. SILVER: clean and join
--    - keeps only reviews that have text
--    - trims whitespace from reviews
--    - upper-cases city and country
--    - adds the franchise location to each review
-- ============================================================

CREATE OR REPLACE TABLE silver_franchise_feedback AS
SELECT
    r.franchiseID,
    UPPER(f.city)    AS city,
    UPPER(f.country) AS country,
    TRIM(r.review)   AS review,
    r.review_date    AS review_timestamp
FROM bronze_customer_reviews AS r
INNER JOIN bronze_sales_franchises AS f
    ON r.franchiseID = f.franchiseID
WHERE r.review IS NOT NULL
  AND TRIM(r.review) <> '';

-- COMMAND ----------

SELECT * FROM silver_franchise_feedback LIMIT 100;

-- COMMAND ----------

-- ============================================================
-- 3. GOLD: business aggregation
--    Number of reviews received per city and country
-- ============================================================

CREATE OR REPLACE TABLE gold_city_feedback AS
SELECT
    city,
    country,
    COUNT(review) AS total_review_received
FROM silver_franchise_feedback
GROUP BY city, country;

-- COMMAND ----------

SELECT *
FROM gold_city_feedback
ORDER BY total_review_received DESC;

-- COMMAND ----------

-- The gold table can now be used to analyze where franchise reviews
-- come from, by country and city.
