# usage: ./cmde base_file_name percentage
# output in file "tuv_injectable"

file="$1"
percentage="$2"

zcat "$file".gz | tr -d "\r" | wc -l > "$file".wc
Ntotal=`cat "$file".wc`
let N=$percentage*$Ntotal/100

echo "number of triplets to sample : $N ($percentage % of $Ntotal)"

echo "building timestamp and node sets"

zcat "$file".gz | tr -d "\r" | cut -d" " -f1 | uniq | sort -S10g -T. -u --parallel=30 | gzip -c > "$file".T.gz
zcat "$file".gz | tr -d "\r" | cut -d" " -f2 | sort -S10g -T. -u --parallel=30 | gzip -c > "$file".X.gz
zcat "$file".gz | tr -d "\r" | cut -d" " -f3 | sort -S10g -T. -u --parallel=30 | gzip -c > "$file".Y.gz

zcat "$file".X.gz "$file".Y.gz | sort -S10g -T. -u --parallel=30 | gzip -c > "$file".V.gz

echo "sampling $N random triplets"

zcat "$file".T.gz | python3 random_sample.py "$N" > "$file".T_sampled
zcat "$file".V.gz | python3 random_sample.py "$N" > "$file".U_sampled
zcat "$file".V.gz | python3 random_sample.py "$N" > "$file".V_sampled

paste -d" " "$file".T_sampled "$file".U_sampled "$file".V_sampled > "$file".tuv_samples

echo "raw sampling performed"

echo "removing loops, duplicates, etc"

cat "$file".tuv_samples | awk '{if ($2!=$3) print($0);}' | awk '{if ($2>$3) print($1,$3,$2); else print($1,$2,$3);}' | sort -S10g -T. -u --parallel=30 | sort -S10g -T. -nk1,1 --parallel=30 > "$file".tuv_samples.clean

echo "removing the ones existing in the original file"

zcat "$file".gz | tr -d "\r" | sort -S10g -T. -nk1,1 -m "$file".tuv_samples.clean - | uniq -c | awk '{if ($1>=2) print $2,$3,$4;}' > "$file".doubles

cat "$file".doubles "$file".tuv_samples.clean | sort -S10g -T. --parallel=30 | uniq -c | awk '{if ($1==1) print $2,$3,$4;}' > "$file".tuv_injectable

finalN=`cat "$file".tuv_injectable | wc -l`

echo "done: built $finalN injectable triplets for \"$file\" (from $N)."
