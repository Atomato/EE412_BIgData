import re
import sys
from pyspark import SparkConf, SparkContext

conf = SparkConf()
sc = SparkContext(conf=conf)

lines = sc.textFile(sys.argv[1])

tuples = lines.map(lambda l: l.split('\t'))

print(tuples.collect())
for _ in range(3):
	print('\n')
