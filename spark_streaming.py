
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import pyspark.sql.functions as f
import json
import re
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import sys
from pyspark.sql.types import *
from textblob import TextBlob
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from pyspark.sql.types import StructType, StructField, StringType, IntegerType


def nlkt_analysis(text):
    
    if(type(text) != type('str')): return
    
    try:
        sia = SentimentIntensityAnalyzer()
        text = regex_(text)
        temp = sia.polarity_scores(text)["compound"]

        if temp == 0.0:
            return temp
        elif temp > 0.0:
            return 1.0
        else:
            return -1.0

    except Exception as e: 
        print(e)
        return e
def regex_(text):
        # 영어, 숫자, 특수만문자 제외 삭제.
        pattern = '(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+/(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
        text = re.sub(pattern, '', text)
        pattern = '(http|ftp|https)://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'  # URL제거
        text = re.sub(pattern, '', text)
        pattern = '(http|ftp|https):// (?:[-\w.]|(?:%[\da-fA-F]{2}))+'  # URL제거
        text = re.sub(pattern, '', text)
        only_english = re.sub('[^ a-zA-Z]', '', text)
        only_english = only_english.lower()

        if bool(only_english and only_english.strip()) and len(only_english) >= 10:
            return only_english
        
        return text

def apply_blob(text):
    try:   
         text = twitter_cleantext(text)
         temp = TextBlob(text).sentiment[0]
         if temp == 0.0:
             return temp
         elif temp > 0.0:
             return 1.0
         else:
             return -1.0

    except: return 5.0

def twitter_cleantext(tweet):
    return ' '.join(re.sub(r"(@[A-Za-z0-9+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ", tweet).split()) 
       
if __name__ == "__main__":
    spark = SparkSession \
            .builder \
            .appName("TwitterStreamingAPI") \
            .config("spark.mongodb.input.uri","mongodb://127.0. 0.1:27017/tweet.kafka_tweet")\
            .config("spark.mongodb.output.uri","mongodb://127.0. 0.1:27017/tweet.kafka_tweet")\
            .getOrCreate()
            #.config("spark.jars", "/root/spark/jars/spark-sql-kafka-0-10_2.11-2.3.0.jar,/root/kafka/libs/kafka-clients-2.2.2.jar") \
            #.config("spark.executor.extraClassPath", "/root/spark/jars/spark-sql-kafka-0-10_2.11-2.3.0.jar,/root/kafka/libs/kafka-clients-2.2.2.jar") \
            #.config("spark.executor.extraLibrary", "/root/spark/jars/spark-sql-kafka-0-10_2.11-2.3.0.jar,/root/kafka/libs/kafka-clients-2.2.2.jar") \
            #.config("spark.driver.extraClassPath", "/root/spark/jars/spark-sql-kafka-0-10_2.11-2.3.0.jar,/root/kafka/libs/kafka-clients-2.2.2.jar") \
            #.getOrCreate()

    spark.sparkContext.setLogLevel("ERROR")
    
    kafka_df = spark.readStream.format("kafka").option("partition.assignment.strategy","range").option("kafka.bootstrap.servers", "localhost:9092").option("subscribe", "test2").option("startingOffsets", "latest").load()
    kafka_df.printSchema()
    kafka_df1 = kafka_df.selectExpr("CAST(value AS STRING)", "timestamp")
    
    transaction_detail_schema = StructType() \
            .add("id", StringType()) \
            .add("text", StringType()) \
            .add("created_at", StringType())\
    
    kafka_df2 = kafka_df1 \
            .select(from_json(col("value"), transaction_detail_schema).alias("transaction_detail"), "timestamp")

    kafka_df3 = kafka_df2.select("transaction_detail.*", "timestamp")
 
    udf_blob = udf(apply_blob, StringType())
    
    udf_nlkt = udf(nlkt_analysis, StringType())
    
    new_df = kafka_df3.withColumn("status", udf_nlkt("text"))
    new_df = new_df.drop("text")

    def write_mongo_row(df, epoch_id):
        mongoURL = "mongodb://117.17.189.6:27017/tweet.kafka_tweet"
        df.write.format("com.mongodb.spark.sql.DefaultSource").mode("append").option("uri", mongoURL).save()
        df.show()
        pass
    query = new_df.writeStream.trigger(processingTime='1 seconds').foreachBatch(write_mongo_row).start() 
    print('---------------------------------------------')
    query.awaitTermination()

    spark.stop()
