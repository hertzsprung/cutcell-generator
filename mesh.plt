set yrange [0:10e3]

plot 'faces.dat' using 1:2:($3-$1):($4-$2) with vectors nohead, \
     'vertices.dat' using 1:2 with points
