import sys, time, json
from collections import deque
from DSC_lib import DSC
# designed for Python 3 / pypy3 with as few libraries as possible

# ignores self-loops (u=v)
# either undirected (no distinction between u v and v u) or bipartite (top bottom) links

# read and set parameters
def usage():
	sys.stderr.write("Usage:\n zcat input.gz | python3 %s [-H s] [-G d] [-bip] [-int] [-check N] | gzip -c > output.json.gz\n"%sys.argv[0])
	sys.stderr.write("Input: sequence of lines of the form \"t u v l\" where t is an int, l is a label indicating if the line is normal or not (either 0 or 1).\n")
	sys.stderr.write("Exactly one among -H and -G must appear.\n")
	sys.stderr.write("-bip is a switch telling if the input graph should be handled as a bipartie graph.\n")
	sys.stderr.write("-int is a switch telling if nodes are integers (faster?).\n")
	sys.stderr.write("-check N enforces a costly verification of data structures and computations every N lines.\n")
	sys.exit()
bool_parameters = {"-bip":False, "-int":False, "-check":False}
sys.stderr.write(str(sys.argv)+'\n')
sys.stderr.flush()
history_type,check_period = None,1000
i=1
def get_int():
	global i
	i += 1
	if not (i<len(sys.argv) and sys.argv[i].isdigit()):
		usage()
	return(int(sys.argv[i]))
while i<len(sys.argv):
	if sys.argv[i]=="-H" or sys.argv[i]=="-G" :
		history_type = sys.argv[i][1]
		size = get_int()
	elif sys.argv[i] in bool_parameters:
		bool_parameters[sys.argv[i]] = True
		if sys.argv[i] == "-check":
			check_period = get_int()
	else:
		sys.stderr.write("Unknown parameter: %s\n"%sys.argv[i])
		usage()
	i += 1

if history_type==None or size<=0:
	usage()

bip = bool_parameters["-bip"]

Q = deque()
if bip:
	top_degrees,bot_degrees,top_weighted_degrees,bot_weighted_degrees = DSC(),DSC(),DSC(),DSC()
else:
	degrees,weighted_degrees = DSC(),DSC()
link_weights = DSC()

def link_arrival(t,u,v):
	Q.append((t,u,v))
	if bip:
		if not top_degrees.has_counter(u):
			top_degrees.add(u)
			top_weighted_degrees.add(u)
		top_weighted_degrees.increase(u)
		if not bot_degrees.has_counter(v):
			bot_degrees.add(v)
			bot_weighted_degrees.add(v)
		bot_weighted_degrees.increase(v)
		if not link_weights.has_counter((u,v)):
			link_weights.add((u,v))
			top_degrees.increase(u)
			bot_degrees.increase(v)
	else:
		if not degrees.has_counter(u):
			degrees.add(u)
			weighted_degrees.add(u)
		weighted_degrees.increase(u)
		if not degrees.has_counter(v):
			degrees.add(v)
			weighted_degrees.add(v)
		weighted_degrees.increase(v)
		if not link_weights.has_counter((u,v)):
			link_weights.add((u,v))
			degrees.increase(u)
			degrees.increase(v)
	link_weights.increase((u,v))

def link_departure(t,u,v):
	link_weights.decrease((u,v))
	if link_weights.val((u,v)) == 0:
		link_weights.remove((u,v))
		if bip:
			top_degrees.decrease(u)
			bot_degrees.decrease(v)
		else:
			degrees.decrease(u)
			degrees.decrease(v)
	if bip:
		param = ((u,top_degrees,top_weighted_degrees),(v,bot_degrees,bot_weighted_degrees))
	else :
		param = ((u,degrees,weighted_degrees),(v,degrees,weighted_degrees))
	for (x,deg,wdeg) in param:
		wdeg.decrease(x)
		if wdeg.val(x) == 0:
			wdeg.remove(x)
			deg.remove(x)

def fill_result(u,v):
	result["number_of_nodes"] = degrees.len()
	result["degrees_nb_one"] = degrees.distrib.get(1,0)
	result["degrees_nb_two"] = degrees.distrib.get(2,0)
	result["degrees_min"] = degrees.min()
	result["degrees_max"] = degrees.max()
	result["degrees_median"] = degrees.median()
	result["weighted_degrees_nb_one"] = weighted_degrees.distrib.get(1,0)
	result["weighted_degrees_nb_two"] = weighted_degrees.distrib.get(2,0)
	result["weighted_degrees_min"] = weighted_degrees.min()
	result["weighted_degrees_max"] = weighted_degrees.max()
	result["weighted_degrees_median"] = weighted_degrees.median()
	if degrees.val(u) > degrees.val(v):
		(u,v) = (v,u)
	result["u_degree"] = degrees.val(u)
	result["v_degree"] = degrees.val(v)
	result["u_same_degree"] = degrees.distrib[degrees.val(u)]
	result["v_same_degree"] = degrees.distrib[degrees.val(v)]
	result["u_greater_degree"] = degrees.val2pos[degrees.val(u)]
	result["v_greater_degree"] = degrees.val2pos[degrees.val(v)]
	result["u_weighted_degree"] = weighted_degrees.val(u)
	result["v_weighted_degree"] = weighted_degrees.val(v)
	result["u_same_weighted_degree"] = weighted_degrees.distrib[weighted_degrees.val(u)]
	result["v_same_weighted_degree"] = weighted_degrees.distrib[weighted_degrees.val(v)]
	result["u_greater_weighted_degree"] = weighted_degrees.val2pos[weighted_degrees.val(u)]
	result["v_greater_weighted_degree"] = weighted_degrees.val2pos[weighted_degrees.val(v)]

def bip_fill_result(u,v):
	result["top_number_of_nodes"] = top_degrees.len()
	result["top_degrees_nb_one"] = top_degrees.distrib.get(1,0)
	result["top_degrees_nb_two"] = top_degrees.distrib.get(2,0)
	result["top_degrees_min"] = top_degrees.min()
	result["top_degrees_max"] = top_degrees.max()
	result["top_degrees_median"] = top_degrees.median()
	result["top_weighted_degrees_nb_one"] = top_weighted_degrees.distrib.get(1,0)
	result["top_weighted_degrees_nb_two"] = top_weighted_degrees.distrib.get(2,0)
	result["top_weighted_degrees_min"] = top_weighted_degrees.min()
	result["top_weighted_degrees_max"] = top_weighted_degrees.max()
	result["top_weighted_degrees_median"] = top_weighted_degrees.median()
	#
	result["bot_number_of_nodes"] = bot_degrees.len()
	result["bot_degrees_nb_one"] = bot_degrees.distrib.get(1,0)
	result["bot_degrees_nb_two"] = bot_degrees.distrib.get(2,0)
	result["bot_degrees_min"] = bot_degrees.min()
	result["bot_degrees_max"] = bot_degrees.max()
	result["bot_degrees_median"] = bot_degrees.median()
	result["bot_weighted_degrees_nb_one"] = bot_weighted_degrees.distrib.get(1,0)
	result["bot_weighted_degrees_nb_two"] = bot_weighted_degrees.distrib.get(2,0)
	result["bot_weighted_degrees_min"] = bot_weighted_degrees.min()
	result["bot_weighted_degrees_max"] = bot_weighted_degrees.max()
	result["bot_weighted_degrees_median"] = bot_weighted_degrees.median()
	#
	result["u_degree"] = top_degrees.val(u)
	result["v_degree"] = bot_degrees.val(v)
	result["u_same_degree"] = top_degrees.distrib[top_degrees.val(u)]
	result["v_same_degree"] = bot_degrees.distrib[bot_degrees.val(v)]
	result["u_greater_degree"] = top_degrees.val2pos[top_degrees.val(u)]
	result["v_greater_degree"] = bot_degrees.val2pos[bot_degrees.val(v)]
	result["u_weighted_degree"] = top_weighted_degrees.val(u)
	result["v_weighted_degree"] = bot_weighted_degrees.val(v)
	result["u_same_weighted_degree"] = top_weighted_degrees.distrib[top_weighted_degrees.val(u)]
	result["v_same_weighted_degree"] = bot_weighted_degrees.distrib[bot_weighted_degrees.val(v)]
	result["u_greater_weighted_degree"] = top_weighted_degrees.val2pos[top_weighted_degrees.val(u)]
	result["v_greater_weighted_degree"] = bot_weighted_degrees.val2pos[bot_weighted_degrees.val(v)]

def check():
	degrees.check()
	weighted_degrees.check()
	link_weights.check()
	check_neighborhood,check_weighted_degrees,check_link_weights,check_nodes,check_links = {},{},{},set(),set()
	for (t,u,v) in Q:
		check_link_weights[(u,v)] = check_link_weights.get((u,v),0) + 1
		check_links.add((u,v))
		check_weighted_degrees[u] = check_weighted_degrees.get(u,0) + 1
		check_nodes.add(u)
		check_neighborhood[u] = check_neighborhood.get(u,set())
		check_weighted_degrees[v] = check_weighted_degrees.get(v,0) + 1
		check_nodes.add(v)
		check_neighborhood[v] = check_neighborhood.get(v,set())
		check_neighborhood[u].add(v)
		check_neighborhood[v].add(u)
	for v in check_nodes:
		assert(degrees.val(v)==len(check_neighborhood[v]))
		assert(weighted_degrees.val(v)==check_weighted_degrees[v])
	for u,v in check_links:
		assert(link_weights.val((u,v))==check_link_weights[(u,v)])
			
def bip_check():
	top_degrees.check()
	bot_degrees.check()
	top_weighted_degrees.check()
	bot_weighted_degrees.check()
	link_weights.check()
	top_check_neighborhood,top_check_weighted_degrees,top_check_nodes = {},{},set()
	bot_check_neighborhood,bot_check_weighted_degrees,bot_check_nodes = {},{},set()
	check_link_weights,check_links = {},set()
	for (t,u,v) in Q:
		check_link_weights[(u,v)] = check_link_weights.get((u,v),0) + 1
		check_links.add((u,v))
		top_check_weighted_degrees[u] = top_check_weighted_degrees.get(u,0) + 1
		top_check_nodes.add(u)
		top_check_neighborhood[u] = top_check_neighborhood.get(u,set())
		bot_check_weighted_degrees[v] = bot_check_weighted_degrees.get(v,0) + 1
		bot_check_nodes.add(v)
		bot_check_neighborhood[v] = bot_check_neighborhood.get(v,set())
		top_check_neighborhood[u].add(v)
		bot_check_neighborhood[v].add(u)
	for v in top_check_nodes:
		assert(top_degrees.val(v)==len(top_check_neighborhood[v]))
		assert(top_weighted_degrees.val(v)==top_check_weighted_degrees[v])
	for v in bot_check_nodes:
		assert(bot_degrees.val(v)==len(bot_check_neighborhood[v]))
		assert(bot_weighted_degrees.val(v)==bot_check_weighted_degrees[v])
	for u,v in check_links:
		assert(link_weights.val((u,v))==check_link_weights[(u,v)])

# process input links one by one
nb_lines,nb_loops,output,global_computation_time = 0,0,False,0
for line in sys.stdin:
	link_begin_time = time.process_time()

	l = line.strip().split()
	assert(len(l)==4)
	[t,u,v,label] = l
	assert(label in ('0','1'))
	label=int(label)
	t = int(t)
	if bool_parameters["-int"]:
		u,v = int(u),int(v)
	if not bip:
		# ignore link direction
		u,v = min(u,v),max(u,v)
		if u==v: # ignore self-loops
			nb_loops += 1
			continue

	link_arrival(t,u,v)

	# manage links to remove
	if history_type=='G':
		(t_,u_,v_) = Q[0]
		while t - t_ > size:
			Q.popleft()
			link_departure(t_,u_,v_)
			(t_,u_,v_) = Q[0]
			output = True
	else: # history_type=='H':
		while len(Q) > size:
			(t_,u_,v_) = Q.popleft()
			link_departure(t_,u_,v_)
			output = True

	link_end_time = time.process_time()

	result = {"t":t, "u":u, "v":v, "is_fraud":label, "history_type":history_type, "history_size":size, "bip":bip}
	result["cost"] = link_end_time-link_begin_time
	if output:
		if bip:
			bip_fill_result(u,v)
		else:
			fill_result(u,v)
		result["number_of_links"] = link_weights.len()
		result["total_weight"] = link_weights.total
		result["link_weights_nb_one"] = link_weights.distrib.get(1,0)
		result["link_weights_nb_two"] = link_weights.distrib.get(2,0)
		result["link_weights_min"] = link_weights.min()
		result["link_weights_max"] = link_weights.max()
		result["link_weights_median"] = link_weights.median()
		result["u_v_weight"] = link_weights.val((u,v))
		result["u_v_same_weight"] = link_weights.distrib[link_weights.val((u,v))]
		result["u_v_greater_weight"] = link_weights.val2pos[link_weights.val((u,v))]

	global_computation_time += result["cost"]
	sys.stdout.write(json.dumps(result))
	sys.stdout.write("\n")

	nb_lines += 1
	if nb_lines%check_period == 0:
		sys.stderr.write("\r%d lines processed."%nb_lines)
		sys.stderr.flush()
		if bool_parameters["-check"]: # costly
			if bip:
				bip_check()
			else:
				check()

sys.stderr.write("\n")
sys.stderr.write("Global computation time: %g\n"%global_computation_time)
if nb_loops>0:
	sys.stderr.write("warning: %d self-loops.\n"%nb_loops)


