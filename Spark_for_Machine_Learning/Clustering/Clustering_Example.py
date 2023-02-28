from pyspark.sql import SparkSession
from pyspark.ml.clustering import KMeans

spark = SparkSession.builder.appName('cluster').getOrCreate()


# Import the data that is already nicely formatted into label and features:
data = spark.read.format('libsvm').load('sample_kmeans_data.txt')
data.show()

final_data = data.select("features")
final_data.show()

# Set and train a k-means model:
# "setSeed" allows to save the same random set of numbers.
kmeans = KMeans().setK(3).setSeed(1)
model = kmeans.fit(final_data)

# Evaluate clustering by computing Within Set Sum of Squared Errors (WSSSE):
wssse = model.computeCost(final_data)
print("Within Set Sum of Squared Errors = " + str(wssse))


# Shows the results:
centers = model.clusterCenters()
print("Cluster Centers: ")
for center in centers:
    print(center)
# Display a table that shows at each cluster the feature or value was assigned:
results = model.transform(final_data)
results.show()
