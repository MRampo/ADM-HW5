most_popular=$(awk -F'/t' 'BEGIN { SUBSEP = OFS = FS } { s[$1,$2] += 1} END { for (i in s) { print  s[i], i } }' hero-network.csv  | sort -k1 -n  | tail -n 1 | awk -F'/t' '{print $2}')

n_comic_per_hero=$(awk -F',' 'BEGIN {} { s[$1] += 1} END { for (i in s) { print  s[i],i}}' edges.csv | sort -k1 -n -r  | head -n 10 )

average_hero_comic=$(awk -F',' 'BEGIN {} {f[$NF]++ c++} END {{ for (i in f) {x++}} print c/x }' edges.csv ) 


echo $most_popular
echo $n_comic_per_hero
echo $average_hero_comic