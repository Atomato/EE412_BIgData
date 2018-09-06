import re
import sys
from pyspark import SparkConf, SparkContext

def select_alphabet(s):
	if 64<ord(s[0])<91 or 96<ord(s[0])<123:
		return True
	else:
		return False

conf = SparkConf()
sc = SparkContext(conf=conf)

lines = sc.textFile(sys.argv[1])

words = lines.flatMap(lambda l: re.split(r'[^\w]+', l))
words = words.filter(lambda l: len(l) != 0) # discard '' key

alphabets = words.filter(select_alphabet)
alphabets = alphabets.map(lambda l: l.lower())

pairs = alphabets.map(lambda w: (w, 1))
counts = pairs.reduceByKey(lambda n1, n2: n1 + n2)

first_letter = counts.map(lambda l: (l[0][0], 1)) # map to first letter
unique_count = first_letter.reduceByKey(lambda n1, n2: n1 + n2)

unique_count.saveAsTextFile(sys.argv[2])
sc.stop()
