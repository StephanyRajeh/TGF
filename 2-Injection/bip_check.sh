
file="$1"
percentage="$2"

# check original file
zcat "$file".gz | tr -d "\r" | cut -d" " -f1 | sort -n -c
if test $? -ne 0
 then echo "PROBLEM!!! original file unsorted"; exit
fi
zcat "$file".gz | tr -d "\r" | awk '{if (NF!=3){ print "PROBLEM!!! invalid number of fields in original file: $0"; exit -1;}}'
if test $? -ne 0
 then exit
fi

n_total=`zcat "$file"_"$percentage"_injected.gz | wc -l`
echo "$n_total" lines
n_zero=`zcat "$file"_"$percentage"_injected.gz | awk 'BEGIN{n=0}{if ($4==0) n+=1;}END{print n;}'`
echo "$n_zero" zeroes
n_one=`zcat "$file"_"$percentage"_injected.gz | awk 'BEGIN{n=0}{if ($4==1) n+=1;}END{print n;}'`
echo "$n_one" ones

n_original=`zcat "$file".gz | tr -d "\r" | wc -l`
echo "$n_zero" "$n_original" | awk '{if ($1!=$2){ print "PROBLEM!!! original number of lines",$2,"differs from number of zeroes",$1; exit -1;}}'
if test $? -ne 0
 then exit
fi

echo "$n_total" "$n_zero" "$n_one" | awk '{if ($1!=$2+$3){ print "PROBLEM!!! total number of lines",$1,"differs from the sum of zeroes",$2,"and ones",$3; exit -1;}}'
if test $? -ne 0
 then exit
fi

let to_add=$percentage*$n_zero/100
echo "$n_one" "$to_add" | awk '{if ($1!=$2){ print "PROBLEM!!! number of ones",$1,"inconsistent with number to add",$2; exit -1;}}'
if test $? -ne 0
 then exit
fi

echo "checking temporal order"

zcat "$file"_"$percentage"_injected.gz | cut -d" " -f1 | sort -n -c
if test $? -ne 0
 then echo "PROBLEM!!! bad temporal ordering"; exit
fi

# todo? check nodes

echo "checking loops, duplicates, etc (may be long)"

n_ok=`zcat "$file"_"$percentage"_injected.gz | cut -d" " -f1,2,3 | awk '{if ($2!=$3) print $0;}' | sort -T. -S10g -u --parallel=30 | wc -l`

echo "$n_total" "$n_ok" | awk '{if ($1!=$2){ print "PROBLEM!!! loops or duplicate are present: n_ok=",$2,"n_total=",$1; exit -1;}}'
if test $? -ne 0
 then exit
fi

echo "everything seems ok"

