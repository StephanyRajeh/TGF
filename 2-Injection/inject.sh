
file="$1"
percentage="$2"
Ntotal=`cat "$file".wc`
let N=$percentage*$Ntotal/100

echo "build list of $N triplets ($percentage percent of $Ntotal) to inject"

cat "$file".tuv_injectable | shuf | head -n "$N" | sort -S10g -T. -nk1,1 --parallel=30 | awk '{print $0,1;}' > "$file"_"$percentage".tuv_toinject

Nobtained=`cat "$file"_"$percentage".tuv_toinject | wc -l`

echo "perform injection of $Nobtained triplets"

zcat "$file".gz | tr -d '\r' | awk '{print $0,0;}' | sort -S10g -T. -nk1,1 -m - "$file"_"$percentage".tuv_toinject | gzip -c > "$file"_"$percentage"_injected.gz

echo "done."
