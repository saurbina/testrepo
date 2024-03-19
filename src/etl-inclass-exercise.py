# Databricks notebook source
# MAGIC %md #### Workshop for ETL

# COMMAND ----------

from pyspark.sql.functions import datediff, current_date, avg
from pyspark.sql.types import IntegerType



# COMMAND ----------

df_laptimes = spark.read.csv('s3://columbia-gr5069-main/raw/lap_times.csv', header=True)

# COMMAND ----------

display(df_laptimes)

# COMMAND ----------

df_driver = spark.read.csv('s3://columbia-gr5069-main/raw/drivers.csv', header=True)
df_driver.count()

# COMMAND ----------

display(df_driver)

# COMMAND ----------

# MAGIC %md #### Transform Data

# COMMAND ----------

df_driver = df_driver.withColumn('age', datediff(current_date(), df_driver.dob)/365) 

# COMMAND ----------

df_driver = df_driver.withColumn('age', df_driver['age'].cast(IntegerType()))

# COMMAND ----------

display(df_driver)

# COMMAND ----------

df_lap_driver = df_driver.select('driverId','nationality', 'age', 'forename', 'surname').join(df_laptimes, on = ['driverId'])

# COMMAND ----------

display(df_lap_driver)

# COMMAND ----------

# MAGIC %md ### Agregate by Age

# COMMAND ----------

df_lap_driver = df_lap_driver.groupBy('nationality','Age').agg(avg('milliseconds'))


# COMMAND ----------

df_lap_driver = df_lap_driver.withColumn('milliseconds', df_lap_driver['avg(milliseconds)'].cast(IntegerType()))

# COMMAND ----------

display(df_lap_driver)

# COMMAND ----------

# MAGIC %md #### Storing Data in S3

# COMMAND ----------

df_lap_driver.write.csv('s3://sau2113-gr5069/processed/in_class_workshop/laptimes_by_drivers.csv')
