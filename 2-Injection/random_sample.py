import sys, random
random.seed()

n = int(sys.argv[1])
sys.stderr.write("sample %d items "%n)

A = []

for l in sys.stdin:
	l = l.strip()
	A.append(l)

sys.stderr.write("in a set of %d\n"%len(A))

while n>0:
	print(random.choice(A))
	n -= 1

