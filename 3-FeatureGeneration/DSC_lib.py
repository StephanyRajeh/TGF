
# decreasing sorted counters
class DSC:

	def __init__(self):
		self.values = []
		self.c2pos = {}
		self.pos2c = []
		self.val2pos = {}
		self.distrib = {}
		self.total = 0
		# values is the list of counter values sorted in decreasing order
		# c2pos[c] gives the index of the value of c: values[c2pos[c]]
		# pos2c[i] gives the counter corresponding to index i in "values"
		# val2pos[v] gives the first index of a counter with value v
		# distrib[v] gives the number of counters with value v
		# total is the sum of counters

	def copy(self):
		c = DSC()
		c.values,c.c2pos,c.pos2c,c.val2pos,c.distrib,c.total = self.values.copy(),self.c2pos.copy(),self.pos2c.copy(),self.val2pos.copy(),self.distrib.copy(),self.total
		return(c)

	def len(self):
		return(len(self.values))

	def has_counter(self,c):
		return(c in self.c2pos)

	def val(self,c):
		assert(c in self.c2pos and self.c2pos[c] >= 0 and self.c2pos[c] < len(self.values))
		return(self.values[self.c2pos[c]])

	def write(self,f): # warning: linear cost
		for i in range(len(self.values)):
			f.write("%s: %d "%(self.pos2c[i],self.val(self.pos2c[i])))
			assert(i==0 or (self.values[i-1]>=self.values[i]))
		f.write("\n")
		
	def add(self,c):
		if 0 not in self.distrib:
			self.distrib[0] = 0
			self.val2pos[0] = len(self.values)
		self.distrib[0] += 1
		assert(c not in self.c2pos)
		self.c2pos[c] = len(self.values)
		self.pos2c.append(c)
		self.values.append(0)

	def swap_equal(self,c1,c2):
		assert(self.val(c1)==self.val(c2))
		pos1,pos2 = self.c2pos[c1],self.c2pos[c2]
		self.c2pos[c2],self.pos2c[pos2],self.c2pos[c1],self.pos2c[pos1] = self.c2pos[c1],self.pos2c[pos1],self.c2pos[c2],self.pos2c[pos2]

	def remove(self,c):
		assert(self.val(c)==0)
		self.distrib[0] -= 1
		if self.distrib[0]==0:
			self.distrib.pop(0)
			self.val2pos.pop(0)
		last = self.pos2c[len(self.values)-1]
		self.swap_equal(c,last)
		self.c2pos.pop(c)
		self.pos2c.pop()
		self.values.pop()

	def increase(self,c):
		v = self.val(c)
		first = self.pos2c[self.val2pos[v]]
		self.swap_equal(c,first)
		if v+1 not in self.distrib:
			self.distrib[v+1] = 0
			self.val2pos[v+1] = self.val2pos[v]
		self.distrib[v+1] += 1
		self.distrib[v] -= 1
		self.val2pos[v] += 1
		if self.distrib[v]==0:
			self.distrib.pop(v)
			self.val2pos.pop(v)
		self.values[self.c2pos[c]] += 1
		self.total += 1
	
	def decrease(self,c):
		v = self.val(c)
		assert(v>0)
		last = self.pos2c[self.val2pos[v]+self.distrib[v]-1]
		self.swap_equal(c,last)
		if v-1 not in self.distrib:
			self.distrib[v-1] = 0
			self.val2pos[v-1] = self.val2pos[v]+self.distrib[v]
		self.distrib[v-1] += 1
		self.distrib[v] -= 1
		self.val2pos[v-1] -= 1
		if self.distrib[v]==0:
			self.distrib.pop(v)
			self.val2pos.pop(v)
		self.values[self.c2pos[c]] -= 1
		self.total -= 1

	def min(self):
		if len(self.values)==0:
			return(None)
		return(self.values[-1])

	def max(self):
		if len(self.values)==0:
			return(None)
		return(self.values[0])

	def median(self):
		if len(self.values)==0:
			return(None)
		return(self.values[int(len(self.values)/2)])

	def min_counter(self):
		if len(self.pos2c)==0:
			return(None)
		return(self.pos2c[-1])

	def max_counter(self):
		if len(self.pos2c)==0:
			return(None)
		return(self.pos2c[0])

	def median_counter(self):
		if len(self.pos2c)==0:
			return(None)
		return(self.pos2c[int(len(self.values)/2)])

	def check(self): # slow!
		if len(self.pos2c)!=len(self.values) or len(self.distrib)!=len(self.val2pos):
			return(False)
		distinct_values = {}
		check_total = 0
		for v in self.values:
			check_total += v
			if v not in distinct_values:
				distinct_values[v] = 0
			distinct_values[v] += 1
		if check_total!=self.total:
			return(False)
		for v in distinct_values:
			if v not in self.distrib or v not in self.val2pos:
				return(False)
			if distinct_values[v] != self.distrib[v]:
				return(False)
		for v in self.distrib:
			if self.distrib[v]<=0 or v not in distinct_values:
				return(False)
		for i in range(len(self.values)-1):
			if self.values[i]<self.values[i+1]:
				return(False)
		return(True)
			

