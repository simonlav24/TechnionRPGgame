f = open("map_big_layer_2","w+")

f.write("960 690\n")
for i in range(1,960*690+1):
	f.write("13 0 ,")
	if i % 960 == 0 and i != 0:
		f.write("\n")


f.close()