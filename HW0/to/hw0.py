import re
import sys
from pyspark import SparkConf, SparkContext

def select_alphabet(s):
	if len(s) is not 0:
		return s

conf = SparkConf()
sc = SparkContext(conf=conf)

lines = sc.textFile(sys.argv[1])

words = lines.flatMap(lambda l: re.split(r'[^\w]+', l))

words = words.filter(lambda l: len(l) != 0)

pairs = words.map(lambda w: (w, 1))

counts = pairs.reduceByKey(lambda n1, n2: n1 + n2)

counts.saveAsTextFile(sys.argv[2])
sc.stop()
