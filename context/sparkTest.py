from pyspark import SparkContext
from pyspark.sql import SQLContext
# from pyspark.sql import SparkSession
# spark = SparkSession.builder.appName("Python Spark SQL data source example").getOrCreate()

sc = SparkContext(appName="mySparkTest")
sqlContext = SQLContext(sc)

import plotly.offline as offline
import plotly.graph_objs as go
import pandas as pd
import requests
requests.packages.urllib3.disable_warnings()




df = sqlContext.read.load("message.csv", format="csv", sep=",", inferSchema="true", header="true")
#print((df.head(2)))
#df.select("id", "version").head(2)
#df.select("id", "version").write.save("idVersion.parquet")
# df.show(3)
# print(df.columns)

#######################################
# possible code correction: switch from "trip_id" to "vin"
#######################################

df.groupBy("vin").count().show()

df_pandas = df.groupBy("vin").count().toPandas()
df_pandas = df_pandas.iloc[1:8,] # select first 8 rows
data = [go.Bar(x=df_pandas["vin"], y=df_pandas["count"])]
print("Writing plot to outputPlot.html")
offline.plot(data, filename='outputPlot.html')




