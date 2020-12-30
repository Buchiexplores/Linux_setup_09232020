# Author: Abuchi Okeke
# Version: 0.0.5
# Date: 03/11/2020
# Description: #


# import modules
from pyspark.sql import SparkSession
from kafka import KafkaConsumer
from json import loads
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
#import findspark
#findspark.init()

from pyspark import SparkContext
import matplotlib.animation as animation
import seaborn as sns
from pandas.plotting import register_matplotlib_converters
import configparser
from pyspark.sql import types as ty
from pyspark.sql.types import StructField, FloatType, IntegerType, StructType

register_matplotlib_converters()
# Use white grid plot background from seaborn
sns.set(font_scale=1.5, style="whitegrid")

# set database configuration path here
auth_path = '/home/fieldemployee/bin/conf/db.ini'

# Get current date time
date_time = (datetime.now().strftime('%Y%m%d%H%M%S'))
config = configparser.ConfigParser()
config.read(auth_path)

# # get auth details for mysql
# mysql_user = config['mysql']['user']
# mysql_password = config['mysql']['password']
# mysql_driver_format = config['mysql']['driver_format']
# #mysql_url = config['mysql']['url']
# mysql_url = 'jdbc:mysql://localhost:3306/stockdb?useSSL=false'
# mysql_connector_path = config['mysql']['driver_connector']

# sqlserver
sqlserver_user = config['sqlserver']['user']
sqlserver_password = config['sqlserver']['password']
sqlserver_driver_format = config['sqlserver']['driver_format']
#sqlserver_url = config['sqlserver']['url']
sqlserver_url = 'jdbc:sqlserver://localhost:1433;databaseName=stockdb'
sqlserver_connector_path = config['sqlserver']['driver_connector']

# Create Spark Session
spark = SparkSession \
    .builder \
    .appName("Api_Spark_DF") \
    .master("local[*]") \
    .config("spark.jars", sqlserver_connector_path) \
    .enableHiveSupport() \
    .getOrCreate()

# sc = SparkContext("Api_Spark_DF", "local[*]")

# funtion to save to RDBMS
def save_to_rdbms(tb_df, table, user, password, driver_format, url):
    tb_df.write \
        .format(driver_format) \
        .mode('overwrite') \
        .option('url', url) \
        .option('user', user) \
        .option('password', password) \
        .option('dbtable', table) \
        .save()

Schema = ty.StructType() \
         .add("date", ty.FloatType()) \
         .add("close", ty.FloatType()) \


# Schema = ty.StructType() \
#          .add("Date", ty.MapType(ty.StringType(), ty.StructType() \
#          .add("open", ty.FloatType()) \
#          .add("high", ty.FloatType()) \
#          .add("low", ty.FloatType()) \
#          .add("close", ty.FloatType()) \
#          .add("volume", ty.IntegerType())))


# data_schema = [StructField('open',FloatType(),True),
#  StructField('high',FloatType(),True),
#  StructField('low',FloatType(),True),
#  StructField('close',FloatType(),True),
#  StructField('volume',IntegerType(),True)]
# struc = StructType(fields=data_schema)

# Get authentication details



# create consumer object
KAFKA_CONSUMER_GROUP_NAME_CONS = "test_consumer_group"
KAFKA_TOPIC_NAME_CONS = "testtopic30"
# KAFKA_OUTPUT_TOPIC_NAME_CONS = "outputtopic"
KAFKA_BOOTSTRAP_SERVERS_CONS = 'localhost:9092'

print("Kafka Consumer Application Started ... ")
# auto_offset_reset='latest'
# auto_offset_reset='earliest'
consumer = KafkaConsumer(
    KAFKA_TOPIC_NAME_CONS,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS_CONS,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id=KAFKA_CONSUMER_GROUP_NAME_CONS,
    value_deserializer=lambda x: loads(x.decode('utf-8')))

# df_values = pd.DataFrame(columns=[])
for r in consumer:
    print("Key: ", r.key)
    response = r.value
    # print("response received: ", response['2020-10-02 04:45:00'])
    # dict = response['Time Series (5min)']
    # # print(dict.values)
    # values =dict.values()
    # # print(type(dict(values)))
    #spdf = spark.createDataFrame(response, schema=Schema)

    #print(response)
    #spdf = spark.read.json(response)
    #numSlices = 1000
    spdf = spark.read.json(spark.sparkContext.parallelize([response]))
    #spdf = spark.read.json(spark.sparkContext.parallelize(response))
    #df.show(truncate=False)
    spdf.show(10)

    # # keys = {'Dates': dict.keys()}
    # last_refreshed = response["Meta Data"]["3. Last Refreshed"]
    # # Get current date time
    # date_time = (datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    #
    # df_keys = pd.DataFrame(dict.keys())
    # df_values = pd.DataFrame(dict.values())
    # df_keys.index.name = 'dt'
    #
    # df_keys.rename(columns={0: 'dates'}, inplace=True)
    # df_values.rename(columns={'1. open': 'open', '2. high': 'high', '3. low': 'low',
    #                           '4. close': 'close', '5. volume': 'volume'}, inplace=True)
    #
    # df_keys['dates'] = pd.to_datetime(df_keys['dates'], infer_datetime_format=True)
    # # df_keys['Dates'] = df_keys['Dates'].to_datetime()
    #
    # # print(type(df_keys['Dates'][0]))
    # df_keys.set_index('dates', inplace=True)
    # print(df_values.head())
    # df_values[["open", "high", "low", "close"]] = df_values[["open", "high", "low", "close"]].astype(float)
    # df_values["volume"] = df_values["volume"].astype(int)
    # df_values['dates'] = df_keys.index.values
    #
    #
    # df_values['SMA1'] = df_values['close'].rolling(window=50).mean()
    # df_values['SMA2'] = df_values['close'].rolling(window=200).mean()
    # df_values.fillna(0, inplace=True)
    #
    # spark_hive_df = spark.createDataFrame(df_values)
    # # save to Hive
    # spark_hive_df.write.format('parquet').mode('overwrite').saveAsTable("dsl.stocks")
    #
    #
    # print(df_values.head())
    # print(df_keys.info())
    # print(df_values.describe())
    #
    # # join dataframes.
    #
    # # df_keys = pd.DataFrame(dict.keys())
    #
    # # Spark Take over #####################################################
    # # Create a Spark DataFrame from a pandas DataFrame using Arrow
    # spark_df = spark.createDataFrame(df_values)
    #
    # # Save to postgres Mysql database
    # save_to_rdbms(spark_df, "stocks_dev", sqlserver_user, sqlserver_password, sqlserver_driver_format,
    #               sqlserver_url)
    #
    # spark_df.show(5)
    # print("completed")

    # spark_df.write.format("orc").saveAsTable("dsl.stocks")
    # df_values['SMA1'] = df_values['SMA1'].replace({'0': pd.np.nan, 0: pd.np.nan}, inplace=True)
    # df_values['SMA2'] = df_values['SMA2'].replace({'0': pd.np.nan, 0: pd.np.nan}, inplace=True)

    # cols = ["SMA1", "SMA2"]
    # df_values[cols] = df_values[cols].replace({'0': np.nan, 0: np.nan})

    # df_values.replace(0, np.nan, inplace=True)
    #
    # fig, ax = plt.subplots(figsize=(10, 10))
    #
    # ax.plot(df_keys.index.values, df_values['SMA1'], 'g--', label="SMA1")
    # ax.plot(df_keys.index.values, df_values['SMA2'], 'r--', label="SMA2")
    # ax.plot(df_keys.index.values, df_values['close'], label="close")
    # # Set title and labels for axes
    # ax.set(xlabel="Date",
    #        ylabel="$ Price",
    #        title="IBM Intraday (5min) Stock Price" + " last refreshed: " + last_refreshed + "\n" + "Date & Time Now: " + date_time)
    # # ax.set_xlabel('X_axi', fontsize=20);
    # # ax.set_ylabel('Y_axis', fontsize=20);
    # plt.setp(ax.get_xticklabels(), rotation=45)
    # plt.setp(ax.get_xticklabels(), size=10)
    # plt.legend()
    #plt.show()
