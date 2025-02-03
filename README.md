# TGF
A repository of the paper: Trivial Graph Features and Old-School Learning for Anomalous Link Detection in Link Streams

In this repository, we demonstrate preprocessing, injection, feature generation, and learning using two datasets as illustrative examples. One dataset is MovieLens, a bipartite link stream, while the other is UCI Messages, a unipartite link stream. <br>

Reference datasets can be downloaded from: http://konect.cc/networks/ and http://snap.stanford.edu/jodie/. <br>

Large scale datasets and their generated features will be provided after acceptance as they are hosted on the lab's server, which could reveal the authors' identities.

## Phase 1: Preprocessing
### Description
Preprocess the link stream to have it in the format of ($`t_i, u_i, v_i`$) where $`t_i < t_{i+1}`$ and to remove loops, directions, and duplicates.

### Usage
Folder "1-PreprocessingOfDatasets" contains the notebooks to preprocess unipartite and bipartite networks.

## Phase 2: Injecting anomalies in the link stream 
### Description
If ground truth is unavailable, anomalous links are injected.
Formally, injected links are created by randomly sampling a timestamp from the link sequence $S = (t_1,u_1,v_1), (t_2,u_2,v_2),\ \dots, \(t_\ell,u_\ell,v_\ell)$, and two distinct nodes from the sets $U$ and $V$ of first and second position nodes, ensuring the sampled link doesn’t exist in $S$. For bipartite datasets, $u$ is sampled from $U$ and $v$ from $V$.

### Usage
Folder "2-Injection" contains the scripts to inject anomalies in unipartite and bipartite networks.

Suppose we have a ___unipartite___ link stream named "data.gz". To inject 10% anomalies in it, the following scripts should be executed in sequence:
./build_injectable.sh data 20 <br>
./inject.sh data 10 <br>
./check.sh data 10 <br>
$\rightarrow$ The file "data_10_injected.gz" is the file to be used in the next phase.

Suppose we have a ___bipartite___ link stream named "data.gz". To inject 10% anomalies in it, the following scripts should be executed in sequence:
./bip_build_injectable.sh data 20 <br>
./inject.sh data 10 <br>
./bip_check.sh data 10 <br>
$\rightarrow$ The file "data_10_injected.gz" is the file to be used in the next phase.

<h6>Note: We set 20% at the start to have a larger sample of the sets $T$, $U$, and $V$, but any value could be set as long as it is greater than 10%.</h6>

## Phase 3: Generating features

### Description
Given a link stream ($`t_i, u_i, v_i`$) with its labels, aggregate the stream into either $H$-type (by size) or a $G$-type (by duration) history graphs and compute the features for each interaction ($`u_i,v_i`$).

### Usage
Folder "3-FeatureGeneration" contains the code to generate the features given a link stream. Following is the command to be used:
```
zcat input.gz | python3 main.py [-H s] [-G d] [-bip] [-int] [-check N] | gzip -c > output.json.gz
```
-H s or -G d: Either must be chosen to set the type of the history graph and the size ($s$) or duration ($d$) <br>
-bip: Should be set if the network is bipartite <br>
-int: A switch indicating if node labels are integers <br>
-check N: Enforces a verification of data structures and computations every N lines (costly)

> Example on ___unipartite___ data_10_injected.gz: zcat data_10_injected.gz | python3 main.py -H 1000 | gzip -c > data_10_injected_H1000.gz <br>
$`\rightarrow`$ Generates the $`O(1)`$ features of the link stream data_10_injected.gz with $H$-type history graph of size $`s`$ = 1000

> Example on ___bipartite___ data_10_injected.gz: zcat data_10_injected.gz | python3 main.py -H 1000 -bip | gzip -c > data_10_injected_H1000.gz <br>
$`\rightarrow`$ Generates the $`O(1)`$ features of the link stream data_10_injected.gz with $H$-type history graph of size $`s`$ = 1000

> Example on ___unipartite___ data_10_injected.gz: zcat data_10_injected.gz | python3 main.py -G 50 | gzip -c > data_10_injected_G50.gz <br>
$`\rightarrow`$ Generates the $`O(1)`$ features of the link stream data_10_injected.gz with $G$-type history graph of duration $`d`$ = 50 (suppose $t$ is in seconds, thus 50 represents 50 seconds in the past)

> Example on ___bipartite___ data_10_injected.gz: zcat data_10_injected.gz | python3 main.py -G 50 -bip | gzip -c > data_10_injected_G50.gz <br>
$`\rightarrow`$ Generates the $`O(1)`$ features of the link stream data_10_injected.gz with $G$-type history graph of duration $`d`$ = 50 (suppose $t$ is in seconds, thus 50 represents 50 seconds in the past)

<h6>Note: zcat is not mandatory, the command to generate features could also be executed as follows: cat input.txt | python3 main.py [-H s] [-G d] [-bip] [-int] [-check N] > output.json</h6>

## Phase 4: Learning and testing

### Description
Given a link stream ($`t_i, u_i, v_i`$) and its graph features based on its history graph, apply machine learning using the Random Forest Classifier for link anomaly detection.

### Usage
Folder "4-LearningAndTesting" contains the notebooks to conduct the learning (classical and with sliding windows) and testing process of the trained model in a unipartite (UCI Messages) and a bipartite network (MovieLens).
In this folder, there are 5 main subfolders:
1. HTypeHistoryGraphs: Learning is performed on multiple instances of $H$-type history graphs of varying sizes.
2. GTypeHistoryGraphs: Learning is performed on multiple instances of $G$-type history graphs of varying durations.
3. CombiningHTypeHistoryGraphs: Learning is performed on multiple instances of $H$-type history graphs of varying sizes combined together.
4. CombiningGTypeHistoryGraphs: Learning is performed on multiple instances of $G$-type history graphs of varying durations combined together.
5. CombiningHandGTypeHistoryGraphs: Learning is performed on multiple instances of $H$-type and $G$-type history graphs of varying sizes and durations combined together.

<h6>Note: If learning is to be done on large dynamic networks, refer to the folder "4-LearningAndTesting-LargeNetworks", where a sampling technique is applied initially so the features are not entirely loaded into the memory and a chunking technique is used for testing. Similarly is the case for TGF with sliding windows. </h6>
