import datetime, time

def calculate(soil,suhu,rain,weather,forecast,forecast2):
	# START FUZZIFIKASI
	# inisialisasi linguistik
	basah 	= 0;
	sedang	= 0;
	kering	= 0;

	panas	= 0;
	sejuk	= 0;
	dingin	= 0;

	hujan 	  = 0;
	tdk_hujan = 0;

	w_cerah	  = 0;
	w_mendung = 0;
	w_hujan	  = 0;

	f_cerah	  = 0;
	f_mendung = 0;
	f_hujan   = 0;

	f2_cerah  = 0;
	f2_mendung= 0;
	f2_hujan  = 0;

	#inisialisasi batas
	l_kering = 0;
	u_kering = 100;
	l_sedang = 150;
	u_sedang = 200;
	l_basah	 = 225;
	u_basah  = 255;

	l_dingin = 0;
	u_dingin = 16;
	l_sejuk	 = 18;
	u_sejuk	 = 28;
	l_panas	 = 36;
	u_panas	 = 100;

	# hitung linguistik
	#soil
	if soil < u_kering:
		kering = 1;
	elif soil >= u_kering and soil <= l_sedang:
		kering = (soil * (-1.0) + l_sedang) / (l_sedang - u_kering);
		sedang = (soil - u_kering) * 1.0 / (l_sedang - u_kering);
	elif soil >= l_sedang and soil < u_sedang:
		sedang = 1;
	elif soil >= u_sedang and soil <= l_basah:
		sedang = (soil * (-1.0) + l_basah) / (l_basah - u_sedang);
		basah = (soil - u_sedang) * 1.0 / (l_basah - u_sedang);
	elif soil >= l_basah:
		basah = 1;

	#temperature
	if suhu < u_dingin:
		dingin = 1;
	elif suhu >= u_dingin and suhu <= l_sejuk:
		dingin = (suhu * (-1.0) + l_sejuk) / (l_sejuk - u_dingin);
		sejuk  = (suhu - u_dingin) * 1.0 / (l_sejuk - u_dingin);
	elif suhu >= l_sejuk and suhu <= u_sejuk:
		sejuk = 1;
	elif suhu >= u_sejuk and suhu <= l_panas:
		sejuk = (suhu * (-1.0) + l_panas) / (l_panas - u_sejuk);
		panas = (suhu - u_sejuk) * 1.0 / (l_panas - u_sejuk);
	elif suhu > l_panas:
		panas = 1;

	# sensor rain
	if rain == 1:
		hujan = 1;
	else :
		tdk_hujan = 1;

	#sensor weather
	if weather == 0:
		w_cerah 	= 1;
	elif weather == 1:
		w_mendung 	= 1;
	elif weather == 2:
		w_hujan 	= 1;

	if forecast == 0:
		f_cerah 	= 1;
	elif forecast == 1:
		f_mendung 	= 1;
	elif forecast == 2:
		f_hujan 	= 1;
	
	if forecast2 == 0:
		f2_cerah 	= 1;
	elif forecast2 == 1:
		f2_mendung 	= 1;
	elif forecast2 == 2:
		f2_hujan 	= 1;
	
	#print linguistik
	print "SOIL";
	print "BASAH  : "+str(basah);
	print "SEDANG : "+str(sedang);
	print "KERING : "+str(kering);

	print "SUHU";
	print "DINGIN : "+str(dingin);
	print "SEJUK  : "+str(sejuk);
	print "PANAS  : "+str(panas);

	print "HUJAN";
	print "HUJAN  	 : "+str(hujan);
	print "TDK_HUJAN : "+str(tdk_hujan);

	print "CURRENT WEATHER";
	print "CERAH  : "+str(w_cerah);
	print "MENDUNG: "+str(w_mendung);
	print "HUJAN  : "+str(w_hujan);

	print "FORECAST 1";
	print "CERAH  : "+str(f_cerah);
	print "MENDUNG: "+str(f_mendung);
	print "HUJAN  : "+str(f_hujan);

	print "FORECAST 2";
	print "CERAH  : "+str(f2_cerah);
	print "MENDUNG: "+str(f2_mendung);
	print "HUJAN  : "+str(f2_hujan);
	#Inferensi
	nkRendah=[];
	nkTinggi=[];
	rendah=0;
	tinggi=0;

	for i in range(324):
 		nkRendah.append(0);
 		nkTinggi.append(0);

 	if basah and panas and hujan and w_cerah and f_cerah and f2_cerah:
 		nkRendah[0]=min(basah,panas,hujan,w_cerah,f_cerah,f2_cerah);

 	if basah and panas and hujan and w_cerah and f_cerah and f2_mendung:
 		nkRendah[1]=min(basah,panas,hujan,w_cerah,f_cerah,f2_mendung);

 	if basah and panas and hujan and w_cerah and f_cerah and f2_hujan:
 		nkRendah[2]=min(basah,panas,hujan,w_cerah,f_cerah,f2_hujan);

 	if basah and panas and hujan and w_cerah and f_mendung and f2_cerah:
 		nkRendah[3]=min(basah,panas,hujan,w_cerah,f_mendung,f2_cerah);
 	
 	if basah and panas and hujan and w_cerah and f_mendung and f2_mendung:
 		nkRendah[4]=min(basah,panas,hujan,w_cerah,f_mendung,f2_mendung);
 	
 	if basah and panas and hujan and w_cerah and f_mendung and f2_hujan:
 		nkRendah[5]=min(basah,panas,hujan,w_cerah,f_mendung,f2_hujan);

 	if basah and panas and hujan and w_cerah and f_hujan and f2_cerah:
 		nkRendah[6]=min(basah,panas,hujan,w_cerah,f_hujan,f2_cerah);

 	if basah and panas and hujan and w_cerah and f_hujan and f2_mendung:
 		nkRendah[7]=min(basah,panas,hujan,w_cerah,f_hujan,f2_mendung);
 	
 	if basah and panas and hujan and w_cerah and f_hujan and f2_huan:
 		nkRendah[8]=min(basah,panas,hujan,w_cerah,f_hujan,f2_hujan);

 	if basah and panas and hujan and w_mendung and f_cerah and f2_cerah:
 		nkRendah[9]=min(basah,panas,hujan,w_mendung,f_cerah,f2_cerah);

 	if basah and panas and hujan and w_mendung and f_cerah and f2_mendung:
 		nkRendah[10]=min(basah,panas,hujan,w_mendung,f_cerah,f2_mendung);

 	if basah and panas and hujan and w_mendung and f_cerah and f2_hujan:
 		nkRendah[11]=min(basah,panas,hujan,w_mendung,f_cerah,f2_hujan);

 	if basah and panas and hujan and w_mendung and f_mendung and f2_cerah:
 		nkRendah[12]=min(basah,panas,hujan,w_mendung,f_mendung,f2_cerah);

 	if basah and panas and hujan and w_mendung and f_mendung and f2_mendung:
 		nkRendah[13]=min(basah,panas,hujan,w_mendung,f_mendung,f2_mendung);

 	if basah and panas and hujan and w_mendung and f_mendung and f2_hujan:
 		nkRendah[14]=min(basah,panas,hujan,w_mendung,f_mendung,f2_hujan);

 	if basah and panas and hujan and w_mendung and f_hujan and f2_cerah:
 		nkRendah[15]=min(basah,panas,hujan,w_mendung,f_hujan,f2_cerah);

 	if basah and panas and hujan and w_mendung and f_hujan and f2_mendung:
 		nkRendah[16]=min(basah,panas,hujan,w_mendung,f_hujan,f2_mendung);

 	if basah and panas and hujan and w_mendung and f_hujan and f2_hujan:
 		nkRendah[17]=min(basah,panas,hujan,w_mendung,f_hujan,f2_hujan);

 	if basah and panas and hujan and w_hujan and f_cerah and f2_cerah:
 		nkRendah[18]=min(basah,panas,hujan,w_hujan,f_cerah,f2_cerah);

 	if basah and panas and hujan and w_hujan and f_cerah and f2_mendung:
 		nkRendah[19]=min(basah,panas,hujan,w_hujan,f_cerah,f2_mendung);

 	if basah and panas and hujan and w_hujan and f_cerah and f2_hujan:
 		nkRendah[20]=min(basah,panas,hujan,w_hujan,f_cerah,f2_hujan);

 	if basah and panas and hujan and w_hujan and f_mendung and f2_cerah:
 		nkRendah[21]=min(basah,panas,hujan,w_hujan,f_mendung,f2_cerah);

 	if basah and panas and hujan and w_hujan and f_mendung and f2_mendung:
 		nkRendah[22]=min(basah,panas,hujan,w_hujan,f_mendung,f2_mendung);

 	if basah and panas and hujan and w_hujan and f_mendung and f2_hujan:
 		nkRendah[23]=min(basah,panas,hujan,w_hujan,f_mendung,f2_hujan);

 	if basah and panas and hujan and w_hujan and f_hujan and f2_cerah:
 		nkRendah[24]=min(basah,panas,hujan,w_hujan,f_hujan,f2_cerah);

 	if basah and panas and hujan and w_hujan and f_hujan and f2_mendung:
 		nkRendah[25]=min(basah,panas,hujan,w_hujan,f_hujan,f2_mendung);

 	if basah and panas and hujan and w_hujan and f_hujan and f2_hujan:
 		nkRendah[26]=min(basah,panas,hujan,w_hujan,f_hujan,f2_hujan);

 	if basah and panas and tdk_hujan and w_cerah and f_cerah and f2_cerah:
 		nkRendah[27]=min(basah,panas,tdk_hujan,w_cerah,f_cerah,f2_cerah);

 	if basah and panas and tdk_hujan and w_cerah and f_cerah and f2_mendung:
 		nkRendah[28]=min(basah,panas,tdk_hujan,w_cerah,f_cerah,f2_mendung);

 	if basah and panas and tdk_hujan and w_cerah and f_cerah and f2_hujan:
 		nkRendah[29]=min(basah,panas,tdk_hujan,w_cerah,f_cerah,f2_hujan);

 	if basah and panas and tdk_hujan and w_cerah and f_mendung and f2_cerah:
 		nkRendah[30]=min(basah,panas,tdk_hujan,w_cerah,f_mendung,f2_cerah);
 	
 	if basah and panas and tdk_hujan and w_cerah and f_mendung and f2_mendung:
 		nkRendah[31]=min(basah,panas,tdk_hujan,w_cerah,f_mendung,f2_mendung);
 	
 	if basah and panas and tdk_hujan and w_cerah and f_mendung and f2_hujan:
 		nkRendah[32]=min(basah,panas,tdk_hujan,w_cerah,f_mendung,f2_hujan);

 	if basah and panas and tdk_hujan and w_cerah and f_hujan and f2_cerah:
 		nkRendah[33]=min(basah,panas,tdk_hujan,w_cerah,f_hujan,f2_cerah);

 	if basah and panas and tdk_hujan and w_cerah and f_hujan and f2_mendung:
 		nkRendah[34]=min(basah,panas,tdk_hujan,w_cerah,f_hujan,f2_mendung);
 	
 	if basah and panas and tdk_hujan and w_cerah and f_hujan and f2_huan:
 		nkRendah[35]=min(basah,panas,tdk_hujan,w_cerah,f_hujan,f2_hujan);

 	if basah and panas and tdk_hujan and w_mendung and f_cerah and f2_cerah:
 		nkRendah[36]=min(basah,panas,tdk_hujan,w_mendung,f_cerah,f2_cerah);

 	if basah and panas and tdk_hujan and w_mendung and f_cerah and f2_mendung:
 		nkRendah[37]=min(basah,panas,tdk_hujan,w_mendung,f_cerah,f2_mendung);

 	if basah and panas and tdk_hujan and w_mendung and f_cerah and f2_hujan:
 		nkRendah[38]=min(basah,panas,tdk_hujan,w_mendung,f_cerah,f2_hujan);

 	if basah and panas and tdk_hujan and w_mendung and f_mendung and f2_cerah:
 		nkRendah[39]=min(basah,panas,tdk_hujan,w_mendung,f_mendung,f2_cerah);

 	if basah and panas and tdk_hujan and w_mendung and f_mendung and f2_mendung:
 		nkRendah[40]=min(basah,panas,tdk_hujan,w_mendung,f_mendung,f2_mendung);

 	if basah and panas and tdk_hujan and w_mendung and f_mendung and f2_hujan:
 		nkRendah[41]=min(basah,panas,tdk_hujan,w_mendung,f_mendung,f2_hujan);

 	if basah and panas and tdk_hujan and w_mendung and f_hujan and f2_cerah:
 		nkRendah[42]=min(basah,panas,tdk_hujan,w_mendung,f_hujan,f2_cerah);

 	if basah and panas and tdk_hujan and w_mendung and f_hujan and f2_mendung:
 		nkRendah[43]=min(basah,panas,tdk_hujan,w_mendung,f_hujan,f2_mendung);

 	if basah and panas and tdk_hujan and w_mendung and f_hujan and f2_hujan:
 		nkRendah[44]=min(basah,panas,tdk_hujan,w_mendung,f_hujan,f2_hujan);

 	if basah and panas and tdk_hujan and w_hujan and f_cerah and f2_cerah:
 		nkRendah[45]=min(basah,panas,tdk_hujan,w_hujan,f_cerah,f2_cerah);

 	if basah and panas and tdk_hujan and w_hujan and f_cerah and f2_mendung:
 		nkRendah[46]=min(basah,panas,tdk_hujan,w_hujan,f_cerah,f2_mendung);

 	if basah and panas and tdk_hujan and w_hujan and f_cerah and f2_hujan:
 		nkRendah[47]=min(basah,panas,tdk_hujan,w_hujan,f_cerah,f2_hujan);

 	if basah and panas and tdk_hujan and w_hujan and f_mendung and f2_cerah:
 		nkRendah[48]=min(basah,panas,tdk_hujan,w_hujan,f_mendung,f2_cerah);

 	if basah and panas and tdk_hujan and w_hujan and f_mendung and f2_mendung:
 		nkRendah[49]=min(basah,panas,tdk_hujan,w_hujan,f_mendung,f2_mendung);

 	if basah and panas and tdk_hujan and w_hujan and f_mendung and f2_hujan:
 		nkRendah[50]=min(basah,panas,tdk_hujan,w_hujan,f_mendung,f2_hujan);

 	if basah and panas and tdk_hujan and w_hujan and f_hujan and f2_cerah:
 		nkRendah[51]=min(basah,panas,tdk_hujan,w_hujan,f_hujan,f2_cerah);

 	if basah and panas and tdk_hujan and w_hujan and f_hujan and f2_mendung:
 		nkRendah[52]=min(basah,panas,tdk_hujan,w_hujan,f_hujan,f2_mendung);

 	if basah and panas and tdk_hujan and w_hujan and f_hujan and f2_hujan:
 		nkRendah[53]=min(basah,panas,tdk_hujan,w_hujan,f_hujan,f2_hujan);
	
	if basah and sejuk and hujan and w_cerah and f_cerah and f2_cerah:
 		nkRendah[54]=min(basah,sejuk,hujan,w_cerah,f_cerah,f2_cerah);

 	if basah and sejuk and hujan and w_cerah and f_cerah and f2_mendung:
 		nkRendah[55]=min(basah,sejuk,hujan,w_cerah,f_cerah,f2_mendung);

 	if basah and sejuk and hujan and w_cerah and f_cerah and f2_hujan:
 		nkRendah[56]=min(basah,sejuk,hujan,w_cerah,f_cerah,f2_hujan);

 	if basah and sejuk and hujan and w_cerah and f_mendung and f2_cerah:
 		nkRendah[57]=min(basah,sejuk,hujan,w_cerah,f_mendung,f2_cerah);
 	
 	if basah and sejuk and hujan and w_cerah and f_mendung and f2_mendung:
 		nkRendah[58]=min(basah,sejuk,hujan,w_cerah,f_mendung,f2_mendung);
 	
 	if basah and sejuk and hujan and w_cerah and f_mendung and f2_hujan:
 		nkRendah[59]=min(basah,sejuk,hujan,w_cerah,f_mendung,f2_hujan);

 	if basah and sejuk and hujan and w_cerah and f_hujan and f2_cerah:
 		nkRendah[60]=min(basah,sejuk,hujan,w_cerah,f_hujan,f2_cerah);

 	if basah and sejuk and hujan and w_cerah and f_hujan and f2_mendung:
 		nkRendah[61]=min(basah,sejuk,hujan,w_cerah,f_hujan,f2_mendung);
 	
 	if basah and sejuk and hujan and w_cerah and f_hujan and f2_huan:
 		nkRendah[62]=min(basah,sejuk,hujan,w_cerah,f_hujan,f2_hujan);

 	if basah and sejuk and hujan and w_mendung and f_cerah and f2_cerah:
 		nkRendah[63]=min(basah,sejuk,hujan,w_mendung,f_cerah,f2_cerah);

 	if basah and sejuk and hujan and w_mendung and f_cerah and f2_mendung:
 		nkRendah[64]=min(basah,sejuk,hujan,w_mendung,f_cerah,f2_mendung);

 	if basah and sejuk and hujan and w_mendung and f_cerah and f2_hujan:
 		nkRendah[65]=min(basah,sejuk,hujan,w_mendung,f_cerah,f2_hujan);

 	if basah and sejuk and hujan and w_mendung and f_mendung and f2_cerah:
 		nkRendah[66]=min(basah,sejuk,hujan,w_mendung,f_mendung,f2_cerah);

 	if basah and sejuk and hujan and w_mendung and f_mendung and f2_mendung:
 		nkRendah[67]=min(basah,sejuk,hujan,w_mendung,f_mendung,f2_mendung);

 	if basah and sejuk and hujan and w_mendung and f_mendung and f2_hujan:
 		nkRendah[68]=min(basah,sejuk,hujan,w_mendung,f_mendung,f2_hujan);

 	if basah and sejuk and hujan and w_mendung and f_hujan and f2_cerah:
 		nkRendah[69]=min(basah,sejuk,hujan,w_mendung,f_hujan,f2_cerah);

 	if basah and sejuk and hujan and w_mendung and f_hujan and f2_mendung:
 		nkRendah[70]=min(basah,sejuk,hujan,w_mendung,f_hujan,f2_mendung);

 	if basah and sejuk and hujan and w_mendung and f_hujan and f2_hujan:
 		nkRendah[71]=min(basah,sejuk,hujan,w_mendung,f_hujan,f2_hujan);

 	if basah and sejuk and hujan and w_hujan and f_cerah and f2_cerah:
 		nkRendah[72]=min(basah,sejuk,hujan,w_hujan,f_cerah,f2_cerah);

 	if basah and sejuk and hujan and w_hujan and f_cerah and f2_mendung:
 		nkRendah[73]=min(basah,sejuk,hujan,w_hujan,f_cerah,f2_mendung);

 	if basah and sejuk and hujan and w_hujan and f_cerah and f2_hujan:
 		nkRendah[74]=min(basah,sejuk,hujan,w_hujan,f_cerah,f2_hujan);

 	if basah and sejuk and hujan and w_hujan and f_mendung and f2_cerah:
 		nkRendah[75]=min(basah,sejuk,hujan,w_hujan,f_mendung,f2_cerah);

 	if basah and sejuk and hujan and w_hujan and f_mendung and f2_mendung:
 		nkRendah[76]=min(basah,sejuk,hujan,w_hujan,f_mendung,f2_mendung);

 	if basah and sejuk and hujan and w_hujan and f_mendung and f2_hujan:
 		nkRendah[77]=min(basah,sejuk,hujan,w_hujan,f_mendung,f2_hujan);

 	if basah and sejuk and hujan and w_hujan and f_hujan and f2_cerah:
 		nkRendah[78]=min(basah,sejuk,hujan,w_hujan,f_hujan,f2_cerah);

 	if basah and sejuk and hujan and w_hujan and f_hujan and f2_mendung:
 		nkRendah[79]=min(basah,sejuk,hujan,w_hujan,f_hujan,f2_mendung);

 	if basah and sejuk and hujan and w_hujan and f_hujan and f2_hujan:
 		nkRendah[80]=min(basah,sejuk,hujan,w_hujan,f_hujan,f2_hujan);

 	if basah and sejuk and tdk_hujan and w_cerah and f_cerah and f2_cerah:
 		nkRendah[81]=min(basah,sejuk,tdk_hujan,w_cerah,f_cerah,f2_cerah);

 	if basah and sejuk and tdk_hujan and w_cerah and f_cerah and f2_mendung:
 		nkRendah[82]=min(basah,sejuk,tdk_hujan,w_cerah,f_cerah,f2_mendung);

 	if basah and sejuk and tdk_hujan and w_cerah and f_cerah and f2_hujan:
 		nkRendah[83]=min(basah,sejuk,tdk_hujan,w_cerah,f_cerah,f2_hujan);

 	if basah and sejuk and tdk_hujan and w_cerah and f_mendung and f2_cerah:
 		nkRendah[84]=min(basah,sejuk,tdk_hujan,w_cerah,f_mendung,f2_cerah);
 	
 	if basah and sejuk and tdk_hujan and w_cerah and f_mendung and f2_mendung:
 		nkRendah[85]=min(basah,sejuk,tdk_hujan,w_cerah,f_mendung,f2_mendung);
 	
 	if basah and sejuk and tdk_hujan and w_cerah and f_mendung and f2_hujan:
 		nkRendah[86]=min(basah,sejuk,tdk_hujan,w_cerah,f_mendung,f2_hujan);

 	if basah and sejuk and tdk_hujan and w_cerah and f_hujan and f2_cerah:
 		nkRendah[87]=min(basah,sejuk,tdk_hujan,w_cerah,f_hujan,f2_cerah);

 	if basah and sejuk and tdk_hujan and w_cerah and f_hujan and f2_mendung:
 		nkRendah[88]=min(basah,sejuk,tdk_hujan,w_cerah,f_hujan,f2_mendung);
 	
 	if basah and sejuk and tdk_hujan and w_cerah and f_hujan and f2_huan:
 		nkRendah[89]=min(basah,sejuk,tdk_hujan,w_cerah,f_hujan,f2_hujan);

 	if basah and sejuk and tdk_hujan and w_mendung and f_cerah and f2_cerah:
 		nkRendah[90]=min(basah,sejuk,tdk_hujan,w_mendung,f_cerah,f2_cerah);

 	if basah and sejuk and tdk_hujan and w_mendung and f_cerah and f2_mendung:
 		nkRendah[91]=min(basah,sejuk,tdk_hujan,w_mendung,f_cerah,f2_mendung);

 	if basah and sejuk and tdk_hujan and w_mendung and f_cerah and f2_hujan:
 		nkRendah[92]=min(basah,sejuk,tdk_hujan,w_mendung,f_cerah,f2_hujan);

 	if basah and sejuk and tdk_hujan and w_mendung and f_mendung and f2_cerah:
 		nkRendah[93]=min(basah,sejuk,tdk_hujan,w_mendung,f_mendung,f2_cerah);

 	if basah and sejuk and tdk_hujan and w_mendung and f_mendung and f2_mendung:
 		nkRendah[94]=min(basah,sejuk,tdk_hujan,w_mendung,f_mendung,f2_mendung);

 	if basah and sejuk and tdk_hujan and w_mendung and f_mendung and f2_hujan:
 		nkRendah[95]=min(basah,sejuk,tdk_hujan,w_mendung,f_mendung,f2_hujan);

 	if basah and sejuk and tdk_hujan and w_mendung and f_hujan and f2_cerah:
 		nkRendah[96]=min(basah,sejuk,tdk_hujan,w_mendung,f_hujan,f2_cerah);

 	if basah and sejuk and tdk_hujan and w_mendung and f_hujan and f2_mendung:
 		nkRendah[97]=min(basah,sejuk,tdk_hujan,w_mendung,f_hujan,f2_mendung);

 	if basah and sejuk and tdk_hujan and w_mendung and f_hujan and f2_hujan:
 		nkRendah[98]=min(basah,sejuk,tdk_hujan,w_mendung,f_hujan,f2_hujan);

 	if basah and sejuk and tdk_hujan and w_hujan and f_cerah and f2_cerah:
 		nkRendah[99]=min(basah,sejuk,tdk_hujan,w_hujan,f_cerah,f2_cerah);

 	if basah and sejuk and tdk_hujan and w_hujan and f_cerah and f2_mendung:
 		nkRendah[100]=min(basah,sejuk,tdk_hujan,w_hujan,f_cerah,f2_mendung);

 	if basah and sejuk and tdk_hujan and w_hujan and f_cerah and f2_hujan:
 		nkRendah[101]=min(basah,sejuk,tdk_hujan,w_hujan,f_cerah,f2_hujan);

 	if basah and sejuk and tdk_hujan and w_hujan and f_mendung and f2_cerah:
 		nkRendah[102]=min(basah,sejuk,tdk_hujan,w_hujan,f_mendung,f2_cerah);

 	if basah and sejuk and tdk_hujan and w_hujan and f_mendung and f2_mendung:
 		nkRendah[103]=min(basah,sejuk,tdk_hujan,w_hujan,f_mendung,f2_mendung);

 	if basah and sejuk and tdk_hujan and w_hujan and f_mendung and f2_hujan:
 		nkRendah[104]=min(basah,sejuk,tdk_hujan,w_hujan,f_mendung,f2_hujan);

 	if basah and sejuk and tdk_hujan and w_hujan and f_hujan and f2_cerah:
 		nkRendah[105]=min(basah,sejuk,tdk_hujan,w_hujan,f_hujan,f2_cerah);

 	if basah and sejuk and tdk_hujan and w_hujan and f_hujan and f2_mendung:
 		nkRendah[106]=min(basah,sejuk,tdk_hujan,w_hujan,f_hujan,f2_mendung);

 	if basah and sejuk and tdk_hujan and w_hujan and f_hujan and f2_hujan:
 		nkRendah[107]=min(basah,sejuk,tdk_hujan,w_hujan,f_hujan,f2_hujan);

 	if basah and dingin and hujan and w_cerah and f_cerah and f2_cerah:
 		nkRendah[108]=min(basah,dingin,hujan,w_cerah,f_cerah,f2_cerah);

 	if basah and dingin and hujan and w_cerah and f_cerah and f2_mendung:
 		nkRendah[109]=min(basah,dingin,hujan,w_cerah,f_cerah,f2_mendung);

 	if basah and dingin and hujan and w_cerah and f_cerah and f2_hujan:
 		nkRendah[110]=min(basah,dingin,hujan,w_cerah,f_cerah,f2_hujan);

 	if basah and dingin and hujan and w_cerah and f_mendung and f2_cerah:
 		nkRendah[111]=min(basah,dingin,hujan,w_cerah,f_mendung,f2_cerah);
 	
 	if basah and dingin and hujan and w_cerah and f_mendung and f2_mendung:
 		nkRendah[112]=min(basah,dingin,hujan,w_cerah,f_mendung,f2_mendung);
 	
 	if basah and dingin and hujan and w_cerah and f_mendung and f2_hujan:
 		nkRendah[113]=min(basah,dingin,hujan,w_cerah,f_mendung,f2_hujan);

 	if basah and dingin and hujan and w_cerah and f_hujan and f2_cerah:
 		nkRendah[114]=min(basah,dingin,hujan,w_cerah,f_hujan,f2_cerah);

 	if basah and dingin and hujan and w_cerah and f_hujan and f2_mendung:
 		nkRendah[115]=min(basah,dingin,hujan,w_cerah,f_hujan,f2_mendung);
 	
 	if basah and dingin and hujan and w_cerah and f_hujan and f2_huan:
 		nkRendah[116]=min(basah,dingin,hujan,w_cerah,f_hujan,f2_hujan);

 	if basah and dingin and hujan and w_mendung and f_cerah and f2_cerah:
 		nkRendah[117]=min(basah,dingin,hujan,w_mendung,f_cerah,f2_cerah);

 	if basah and dingin and hujan and w_mendung and f_cerah and f2_mendung:
 		nkRendah[118]=min(basah,dingin,hujan,w_mendung,f_cerah,f2_mendung);

 	if basah and dingin and hujan and w_mendung and f_cerah and f2_hujan:
 		nkRendah[119]=min(basah,dingin,hujan,w_mendung,f_cerah,f2_hujan);

 	if basah and dingin and hujan and w_mendung and f_mendung and f2_cerah:
 		nkRendah[120]=min(basah,dingin,hujan,w_mendung,f_mendung,f2_cerah);

 	if basah and dingin and hujan and w_mendung and f_mendung and f2_mendung:
 		nkRendah[121]=min(basah,dingin,hujan,w_mendung,f_mendung,f2_mendung);

 	if basah and dingin and hujan and w_mendung and f_mendung and f2_hujan:
 		nkRendah[122]=min(basah,dingin,hujan,w_mendung,f_mendung,f2_hujan);

 	if basah and dingin and hujan and w_mendung and f_hujan and f2_cerah:
 		nkRendah[123]=min(basah,dingin,hujan,w_mendung,f_hujan,f2_cerah);

 	if basah and dingin and hujan and w_mendung and f_hujan and f2_mendung:
 		nkRendah[124]=min(basah,dingin,hujan,w_mendung,f_hujan,f2_mendung);

 	if basah and dingin and hujan and w_mendung and f_hujan and f2_hujan:
 		nkRendah[125]=min(basah,dingin,hujan,w_mendung,f_hujan,f2_hujan);

 	if basah and dingin and hujan and w_hujan and f_cerah and f2_cerah:
 		nkRendah[126]=min(basah,dingin,hujan,w_hujan,f_cerah,f2_cerah);

 	if basah and dingin and hujan and w_hujan and f_cerah and f2_mendung:
 		nkRendah[127]=min(basah,dingin,hujan,w_hujan,f_cerah,f2_mendung);

 	if basah and dingin and hujan and w_hujan and f_cerah and f2_hujan:
 		nkRendah[128]=min(basah,dingin,hujan,w_hujan,f_cerah,f2_hujan);

 	if basah and dingin and hujan and w_hujan and f_mendung and f2_cerah:
 		nkRendah[129]=min(basah,dingin,hujan,w_hujan,f_mendung,f2_cerah);

 	if basah and dingin and hujan and w_hujan and f_mendung and f2_mendung:
 		nkRendah[130]=min(basah,dingin,hujan,w_hujan,f_mendung,f2_mendung);

 	if basah and dingin and hujan and w_hujan and f_mendung and f2_hujan:
 		nkRendah[131]=min(basah,dingin,hujan,w_hujan,f_mendung,f2_hujan);

 	if basah and dingin and hujan and w_hujan and f_hujan and f2_cerah:
 		nkRendah[132]=min(basah,dingin,hujan,w_hujan,f_hujan,f2_cerah);

 	if basah and dingin and hujan and w_hujan and f_hujan and f2_mendung:
 		nkRendah[133]=min(basah,dingin,hujan,w_hujan,f_hujan,f2_mendung);

 	if basah and dingin and hujan and w_hujan and f_hujan and f2_hujan:
 		nkRendah[134]=min(basah,dingin,hujan,w_hujan,f_hujan,f2_hujan);

 	if basah and dingin and tdk_hujan and w_cerah and f_cerah and f2_cerah:
 		nkRendah[135]=min(basah,dingin,tdk_hujan,w_cerah,f_cerah,f2_cerah);

 	if basah and dingin and tdk_hujan and w_cerah and f_cerah and f2_mendung:
 		nkRendah[136]=min(basah,dingin,tdk_hujan,w_cerah,f_cerah,f2_mendung);

 	if basah and dingin and tdk_hujan and w_cerah and f_cerah and f2_hujan:
 		nkRendah[137]=min(basah,dingin,tdk_hujan,w_cerah,f_cerah,f2_hujan);

 	if basah and dingin and tdk_hujan and w_cerah and f_mendung and f2_cerah:
 		nkRendah[138]=min(basah,dingin,tdk_hujan,w_cerah,f_mendung,f2_cerah);
 	
 	if basah and dingin and tdk_hujan and w_cerah and f_mendung and f2_mendung:
 		nkRendah[139]=min(basah,dingin,tdk_hujan,w_cerah,f_mendung,f2_mendung);
 	
 	if basah and dingin and tdk_hujan and w_cerah and f_mendung and f2_hujan:
 		nkRendah[140]=min(basah,dingin,tdk_hujan,w_cerah,f_mendung,f2_hujan);

 	if basah and dingin and tdk_hujan and w_cerah and f_hujan and f2_cerah:
 		nkRendah[141]=min(basah,dingin,tdk_hujan,w_cerah,f_hujan,f2_cerah);

 	if basah and dingin and tdk_hujan and w_cerah and f_hujan and f2_mendung:
 		nkRendah[142]=min(basah,dingin,tdk_hujan,w_cerah,f_hujan,f2_mendung);
 	
 	if basah and dingin and tdk_hujan and w_cerah and f_hujan and f2_huan:
 		nkRendah[143]=min(basah,dingin,tdk_hujan,w_cerah,f_hujan,f2_hujan);

 	if basah and dingin and tdk_hujan and w_mendung and f_cerah and f2_cerah:
 		nkRendah[144]=min(basah,dingin,tdk_hujan,w_mendung,f_cerah,f2_cerah);

 	if basah and dingin and tdk_hujan and w_mendung and f_cerah and f2_mendung:
 		nkRendah[145]=min(basah,dingin,tdk_hujan,w_mendung,f_cerah,f2_mendung);

 	if basah and dingin and tdk_hujan and w_mendung and f_cerah and f2_hujan:
 		nkRendah[146]=min(basah,dingin,tdk_hujan,w_mendung,f_cerah,f2_hujan);

 	if basah and dingin and tdk_hujan and w_mendung and f_mendung and f2_cerah:
 		nkRendah[147]=min(basah,dingin,tdk_hujan,w_mendung,f_mendung,f2_cerah);

 	if basah and dingin and tdk_hujan and w_mendung and f_mendung and f2_mendung:
 		nkRendah[148]=min(basah,dingin,tdk_hujan,w_mendung,f_mendung,f2_mendung);

 	if basah and dingin and tdk_hujan and w_mendung and f_mendung and f2_hujan:
 		nkRendah[149]=min(basah,dingin,tdk_hujan,w_mendung,f_mendung,f2_hujan);

 	if basah and dingin and tdk_hujan and w_mendung and f_hujan and f2_cerah:
 		nkRendah[150]=min(basah,dingin,tdk_hujan,w_mendung,f_hujan,f2_cerah);

 	if basah and dingin and tdk_hujan and w_mendung and f_hujan and f2_mendung:
 		nkRendah[151]=min(basah,dingin,tdk_hujan,w_mendung,f_hujan,f2_mendung);

 	if basah and dingin and tdk_hujan and w_mendung and f_hujan and f2_hujan:
 		nkRendah[152]=min(basah,dingin,tdk_hujan,w_mendung,f_hujan,f2_hujan);

 	if basah and dingin and tdk_hujan and w_hujan and f_cerah and f2_cerah:
 		nkRendah[153]=min(basah,dingin,tdk_hujan,w_hujan,f_cerah,f2_cerah);

 	if basah and dingin and tdk_hujan and w_hujan and f_cerah and f2_mendung:
 		nkRendah[154]=min(basah,dingin,tdk_hujan,w_hujan,f_cerah,f2_mendung);

 	if basah and dingin and tdk_hujan and w_hujan and f_cerah and f2_hujan:
 		nkRendah[155]=min(basah,dingin,tdk_hujan,w_hujan,f_cerah,f2_hujan);

 	if basah and dingin and tdk_hujan and w_hujan and f_mendung and f2_cerah:
 		nkRendah[156]=min(basah,dingin,tdk_hujan,w_hujan,f_mendung,f2_cerah);

 	if basah and dingin and tdk_hujan and w_hujan and f_mendung and f2_mendung:
 		nkRendah[157]=min(basah,dingin,tdk_hujan,w_hujan,f_mendung,f2_mendung);

 	if basah and dingin and tdk_hujan and w_hujan and f_mendung and f2_hujan:
 		nkRendah[158]=min(basah,dingin,tdk_hujan,w_hujan,f_mendung,f2_hujan);

 	if basah and dingin and tdk_hujan and w_hujan and f_hujan and f2_cerah:
 		nkRendah[159]=min(basah,dingin,tdk_hujan,w_hujan,f_hujan,f2_cerah);

 	if basah and dingin and tdk_hujan and w_hujan and f_hujan and f2_mendung:
 		nkRendah[160]=min(basah,dingin,tdk_hujan,w_hujan,f_hujan,f2_mendung);

 	if basah and dingin and tdk_hujan and w_hujan and f_hujan and f2_hujan:
 		nkRendah[161]=min(basah,dingin,tdk_hujan,w_hujan,f_hujan,f2_hujan);
	


 	if sedang and panas and hujan and w_cerah and f_cerah and f2_cerah:
 		nkRendah[162]=min(sedang,panas,hujan,w_cerah,f_cerah,f2_cerah);

 	if sedang and panas and hujan and w_cerah and f_cerah and f2_mendung:
 		nkRendah[163]=min(sedang,panas,hujan,w_cerah,f_cerah,f2_mendung);

 	if sedang and panas and hujan and w_cerah and f_cerah and f2_hujan:
 		nkRendah[164]=min(sedang,panas,hujan,w_cerah,f_cerah,f2_hujan);

 	if sedang and panas and hujan and w_cerah and f_mendung and f2_cerah:
 		nkRendah[165]=min(sedang,panas,hujan,w_cerah,f_mendung,f2_cerah);
 	
 	if sedang and panas and hujan and w_cerah and f_mendung and f2_mendung:
 		nkRendah[166]=min(sedang,panas,hujan,w_cerah,f_mendung,f2_mendung);
 	
 	if sedang and panas and hujan and w_cerah and f_mendung and f2_hujan:
 		nkRendah[167]=min(sedang,panas,hujan,w_cerah,f_mendung,f2_hujan);

 	if sedang and panas and hujan and w_cerah and f_hujan and f2_cerah:
 		nkRendah[168]=min(sedang,panas,hujan,w_cerah,f_hujan,f2_cerah);

 	if sedang and panas and hujan and w_cerah and f_hujan and f2_mendung:
 		nkRendah[169]=min(sedang,panas,hujan,w_cerah,f_hujan,f2_mendung);
 	
 	if sedang and panas and hujan and w_cerah and f_hujan and f2_huan:
 		nkRendah[170]=min(sedang,panas,hujan,w_cerah,f_hujan,f2_hujan);

 	if sedang and panas and hujan and w_mendung and f_cerah and f2_cerah:
 		nkRendah[171]=min(sedang,panas,hujan,w_mendung,f_cerah,f2_cerah);

 	if sedang and panas and hujan and w_mendung and f_cerah and f2_mendung:
 		nkRendah[172]=min(sedang,panas,hujan,w_mendung,f_cerah,f2_mendung);

 	if sedang and panas and hujan and w_mendung and f_cerah and f2_hujan:
 		nkRendah[173]=min(sedang,panas,hujan,w_mendung,f_cerah,f2_hujan);

 	if sedang and panas and hujan and w_mendung and f_mendung and f2_cerah:
 		nkRendah[174]=min(sedang,panas,hujan,w_mendung,f_mendung,f2_cerah);

 	if sedang and panas and hujan and w_mendung and f_mendung and f2_mendung:
 		nkRendah[175]=min(sedang,panas,hujan,w_mendung,f_mendung,f2_mendung);

 	if sedang and panas and hujan and w_mendung and f_mendung and f2_hujan:
 		nkRendah[176]=min(sedang,panas,hujan,w_mendung,f_mendung,f2_hujan);

 	if sedang and panas and hujan and w_mendung and f_hujan and f2_cerah:
 		nkRendah[177]=min(sedang,panas,hujan,w_mendung,f_hujan,f2_cerah);

 	if sedang and panas and hujan and w_mendung and f_hujan and f2_mendung:
 		nkRendah[178]=min(sedang,panas,hujan,w_mendung,f_hujan,f2_mendung);

 	if sedang and panas and hujan and w_mendung and f_hujan and f2_hujan:
 		nkRendah[179]=min(sedang,panas,hujan,w_mendung,f_hujan,f2_hujan);

 	if sedang and panas and hujan and w_hujan and f_cerah and f2_cerah:
 		nkRendah[180]=min(sedang,panas,hujan,w_hujan,f_cerah,f2_cerah);

 	if sedang and panas and hujan and w_hujan and f_cerah and f2_mendung:
 		nkRendah[181]=min(sedang,panas,hujan,w_hujan,f_cerah,f2_mendung);

 	if sedang and panas and hujan and w_hujan and f_cerah and f2_hujan:
 		nkRendah[182]=min(sedang,panas,hujan,w_hujan,f_cerah,f2_hujan);

 	if sedang and panas and hujan and w_hujan and f_mendung and f2_cerah:
 		nkRendah[183]=min(sedang,panas,hujan,w_hujan,f_mendung,f2_cerah);

 	if sedang and panas and hujan and w_hujan and f_mendung and f2_mendung:
 		nkRendah[184]=min(sedang,panas,hujan,w_hujan,f_mendung,f2_mendung);

 	if sedang and panas and hujan and w_hujan and f_mendung and f2_hujan:
 		nkRendah[185]=min(sedang,panas,hujan,w_hujan,f_mendung,f2_hujan);

 	if sedang and panas and hujan and w_hujan and f_hujan and f2_cerah:
 		nkRendah[186]=min(sedang,panas,hujan,w_hujan,f_hujan,f2_cerah);

 	if sedang and panas and hujan and w_hujan and f_hujan and f2_mendung:
 		nkRendah[187]=min(sedang,panas,hujan,w_hujan,f_hujan,f2_mendung);

 	if sedang and panas and hujan and w_hujan and f_hujan and f2_hujan:
 		nkRendah[188]=min(sedang,panas,hujan,w_hujan,f_hujan,f2_hujan);

 	if sedang and panas and tdk_hujan and w_cerah and f_cerah and f2_cerah:
 		nkRendah[189]=min(sedang,panas,tdk_hujan,w_cerah,f_cerah,f2_cerah);

 	if sedang and panas and tdk_hujan and w_cerah and f_cerah and f2_mendung:
 		nkRendah[190]=min(sedang,panas,tdk_hujan,w_cerah,f_cerah,f2_mendung);

 	if sedang and panas and tdk_hujan and w_cerah and f_cerah and f2_hujan:
 		nkRendah[191]=min(sedang,panas,tdk_hujan,w_cerah,f_cerah,f2_hujan);

 	if sedang and panas and tdk_hujan and w_cerah and f_mendung and f2_cerah:
 		nkRendah[192]=min(sedang,panas,tdk_hujan,w_cerah,f_mendung,f2_cerah);
 	
 	if sedang and panas and tdk_hujan and w_cerah and f_mendung and f2_mendung:
 		nkRendah[193]=min(sedang,panas,tdk_hujan,w_cerah,f_mendung,f2_mendung);
 	
 	if sedang and panas and tdk_hujan and w_cerah and f_mendung and f2_hujan:
 		nkRendah[194]=min(sedang,panas,tdk_hujan,w_cerah,f_mendung,f2_hujan);

 	if sedang and panas and tdk_hujan and w_cerah and f_hujan and f2_cerah:
 		nkRendah[195]=min(sedang,panas,tdk_hujan,w_cerah,f_hujan,f2_cerah);

 	if sedang and panas and tdk_hujan and w_cerah and f_hujan and f2_mendung:
 		nkRendah[196]=min(sedang,panas,tdk_hujan,w_cerah,f_hujan,f2_mendung);
 	
 	if sedang and panas and tdk_hujan and w_cerah and f_hujan and f2_huan:
 		nkRendah[197]=min(sedang,panas,tdk_hujan,w_cerah,f_hujan,f2_hujan);

 	if sedang and panas and tdk_hujan and w_mendung and f_cerah and f2_cerah:
 		nkRendah[198]=min(sedang,panas,tdk_hujan,w_mendung,f_cerah,f2_cerah);

 	if sedang and panas and tdk_hujan and w_mendung and f_cerah and f2_mendung:
 		nkRendah[199]=min(sedang,panas,tdk_hujan,w_mendung,f_cerah,f2_mendung);

 	if sedang and panas and tdk_hujan and w_mendung and f_cerah and f2_hujan:
 		nkRendah[200]=min(sedang,panas,tdk_hujan,w_mendung,f_cerah,f2_hujan);

 	if sedang and panas and tdk_hujan and w_mendung and f_mendung and f2_cerah:
 		nkRendah[201]=min(sedang,panas,tdk_hujan,w_mendung,f_mendung,f2_cerah);

 	if sedang and panas and tdk_hujan and w_mendung and f_mendung and f2_mendung:
 		nkRendah[202]=min(sedang,panas,tdk_hujan,w_mendung,f_mendung,f2_mendung);

 	if sedang and panas and tdk_hujan and w_mendung and f_mendung and f2_hujan:
 		nkRendah[203]=min(sedang,panas,tdk_hujan,w_mendung,f_mendung,f2_hujan);

 	if sedang and panas and tdk_hujan and w_mendung and f_hujan and f2_cerah:
 		nkRendah[204]=min(sedang,panas,tdk_hujan,w_mendung,f_hujan,f2_cerah);

 	if sedang and panas and tdk_hujan and w_mendung and f_hujan and f2_mendung:
 		nkRendah[205]=min(sedang,panas,tdk_hujan,w_mendung,f_hujan,f2_mendung);

 	if sedang and panas and tdk_hujan and w_mendung and f_hujan and f2_hujan:
 		nkRendah[206]=min(sedang,panas,tdk_hujan,w_mendung,f_hujan,f2_hujan);

 	if sedang and panas and tdk_hujan and w_hujan and f_cerah and f2_cerah:
 		nkRendah[207]=min(sedang,panas,tdk_hujan,w_hujan,f_cerah,f2_cerah);

 	if sedang and panas and tdk_hujan and w_hujan and f_cerah and f2_mendung:
 		nkRendah[208]=min(sedang,panas,tdk_hujan,w_hujan,f_cerah,f2_mendung);

 	if sedang and panas and tdk_hujan and w_hujan and f_cerah and f2_hujan:
 		nkRendah[209]=min(sedang,panas,tdk_hujan,w_hujan,f_cerah,f2_hujan);

 	if sedang and panas and tdk_hujan and w_hujan and f_mendung and f2_cerah:
 		nkRendah[210]=min(sedang,panas,tdk_hujan,w_hujan,f_mendung,f2_cerah);

 	if sedang and panas and tdk_hujan and w_hujan and f_mendung and f2_mendung:
 		nkRendah[211]=min(sedang,panas,tdk_hujan,w_hujan,f_mendung,f2_mendung);

 	if sedang and panas and tdk_hujan and w_hujan and f_mendung and f2_hujan:
 		nkRendah[212]=min(sedang,panas,tdk_hujan,w_hujan,f_mendung,f2_hujan);

 	if sedang and panas and tdk_hujan and w_hujan and f_hujan and f2_cerah:
 		nkRendah[213]=min(sedang,panas,tdk_hujan,w_hujan,f_hujan,f2_cerah);

 	if sedang and panas and tdk_hujan and w_hujan and f_hujan and f2_mendung:
 		nkRendah[214]=min(sedang,panas,tdk_hujan,w_hujan,f_hujan,f2_mendung);

 	if sedang and panas and tdk_hujan and w_hujan and f_hujan and f2_hujan:
 		nkRendah[215]=min(sedang,panas,tdk_hujan,w_hujan,f_hujan,f2_hujan);
	
	if sedang and sejuk and hujan and w_cerah and f_cerah and f2_cerah:
 		nkRendah[216]=min(sedang,sejuk,hujan,w_cerah,f_cerah,f2_cerah);

 	if sedang and sejuk and hujan and w_cerah and f_cerah and f2_mendung:
 		nkRendah[217]=min(sedang,sejuk,hujan,w_cerah,f_cerah,f2_mendung);

 	if sedang and sejuk and hujan and w_cerah and f_cerah and f2_hujan:
 		nkRendah[218]=min(sedang,sejuk,hujan,w_cerah,f_cerah,f2_hujan);

 	if sedang and sejuk and hujan and w_cerah and f_mendung and f2_cerah:
 		nkRendah[219]=min(sedang,sejuk,hujan,w_cerah,f_mendung,f2_cerah);
 	
 	if sedang and sejuk and hujan and w_cerah and f_mendung and f2_mendung:
 		nkRendah[220]=min(sedang,sejuk,hujan,w_cerah,f_mendung,f2_mendung);
 	
 	if sedang and sejuk and hujan and w_cerah and f_mendung and f2_hujan:
 		nkRendah[221]=min(sedang,sejuk,hujan,w_cerah,f_mendung,f2_hujan);

 	if sedang and sejuk and hujan and w_cerah and f_hujan and f2_cerah:
 		nkRendah[222]=min(sedang,sejuk,hujan,w_cerah,f_hujan,f2_cerah);

 	if sedang and sejuk and hujan and w_cerah and f_hujan and f2_mendung:
 		nkRendah[223]=min(sedang,sejuk,hujan,w_cerah,f_hujan,f2_mendung);
 	
 	if sedang and sejuk and hujan and w_cerah and f_hujan and f2_huan:
 		nkRendah[224]=min(sedang,sejuk,hujan,w_cerah,f_hujan,f2_hujan);

 	if sedang and sejuk and hujan and w_mendung and f_cerah and f2_cerah:
 		nkRendah[225]=min(sedang,sejuk,hujan,w_mendung,f_cerah,f2_cerah);

 	if sedang and sejuk and hujan and w_mendung and f_cerah and f2_mendung:
 		nkRendah[226]=min(sedang,sejuk,hujan,w_mendung,f_cerah,f2_mendung);

 	if sedang and sejuk and hujan and w_mendung and f_cerah and f2_hujan:
 		nkRendah[227]=min(sedang,sejuk,hujan,w_mendung,f_cerah,f2_hujan);

 	if sedang and sejuk and hujan and w_mendung and f_mendung and f2_cerah:
 		nkRendah[228]=min(sedang,sejuk,hujan,w_mendung,f_mendung,f2_cerah);

 	if sedang and sejuk and hujan and w_mendung and f_mendung and f2_mendung:
 		nkRendah[229]=min(sedang,sejuk,hujan,w_mendung,f_mendung,f2_mendung);

 	if sedang and sejuk and hujan and w_mendung and f_mendung and f2_hujan:
 		nkRendah[230]=min(sedang,sejuk,hujan,w_mendung,f_mendung,f2_hujan);

 	if sedang and sejuk and hujan and w_mendung and f_hujan and f2_cerah:
 		nkRendah[231]=min(sedang,sejuk,hujan,w_mendung,f_hujan,f2_cerah);

 	if sedang and sejuk and hujan and w_mendung and f_hujan and f2_mendung:
 		nkRendah[232]=min(sedang,sejuk,hujan,w_mendung,f_hujan,f2_mendung);

 	if sedang and sejuk and hujan and w_mendung and f_hujan and f2_hujan:
 		nkRendah[233]=min(sedang,sejuk,hujan,w_mendung,f_hujan,f2_hujan);

 	if sedang and sejuk and hujan and w_hujan and f_cerah and f2_cerah:
 		nkRendah[234]=min(sedang,sejuk,hujan,w_hujan,f_cerah,f2_cerah);

 	if sedang and sejuk and hujan and w_hujan and f_cerah and f2_mendung:
 		nkRendah[235]=min(sedang,sejuk,hujan,w_hujan,f_cerah,f2_mendung);

 	if sedang and sejuk and hujan and w_hujan and f_cerah and f2_hujan:
 		nkRendah[236]=min(sedang,sejuk,hujan,w_hujan,f_cerah,f2_hujan);

 	if sedang and sejuk and hujan and w_hujan and f_mendung and f2_cerah:
 		nkRendah[237]=min(sedang,sejuk,hujan,w_hujan,f_mendung,f2_cerah);

 	if sedang and sejuk and hujan and w_hujan and f_mendung and f2_mendung:
 		nkRendah[238]=min(sedang,sejuk,hujan,w_hujan,f_mendung,f2_mendung);

 	if sedang and sejuk and hujan and w_hujan and f_mendung and f2_hujan:
 		nkRendah[239]=min(sedang,sejuk,hujan,w_hujan,f_mendung,f2_hujan);

 	if sedang and sejuk and hujan and w_hujan and f_hujan and f2_cerah:
 		nkRendah[240]=min(sedang,sejuk,hujan,w_hujan,f_hujan,f2_cerah);

 	if sedang and sejuk and hujan and w_hujan and f_hujan and f2_mendung:
 		nkRendah[241]=min(sedang,sejuk,hujan,w_hujan,f_hujan,f2_mendung);

 	if sedang and sejuk and hujan and w_hujan and f_hujan and f2_hujan:
 		nkRendah[242]=min(sedang,sejuk,hujan,w_hujan,f_hujan,f2_hujan);

 	if sedang and sejuk and tdk_hujan and w_cerah and f_cerah and f2_cerah:
 		nkRendah[243]=min(sedang,sejuk,tdk_hujan,w_cerah,f_cerah,f2_cerah);

 	if sedang and sejuk and tdk_hujan and w_cerah and f_cerah and f2_mendung:
 		nkRendah[244]=min(sedang,sejuk,tdk_hujan,w_cerah,f_cerah,f2_mendung);

 	if sedang and sejuk and tdk_hujan and w_cerah and f_cerah and f2_hujan:
 		nkRendah[245]=min(sedang,sejuk,tdk_hujan,w_cerah,f_cerah,f2_hujan);

 	if sedang and sejuk and tdk_hujan and w_cerah and f_mendung and f2_cerah:
 		nkRendah[246]=min(sedang,sejuk,tdk_hujan,w_cerah,f_mendung,f2_cerah);
 	
 	if sedang and sejuk and tdk_hujan and w_cerah and f_mendung and f2_mendung:
 		nkRendah[247]=min(sedang,sejuk,tdk_hujan,w_cerah,f_mendung,f2_mendung);
 	
 	if sedang and sejuk and tdk_hujan and w_cerah and f_mendung and f2_hujan:
 		nkRendah[248]=min(sedang,sejuk,tdk_hujan,w_cerah,f_mendung,f2_hujan);

 	if sedang and sejuk and tdk_hujan and w_cerah and f_hujan and f2_cerah:
 		nkRendah[249]=min(sedang,sejuk,tdk_hujan,w_cerah,f_hujan,f2_cerah);

 	if sedang and sejuk and tdk_hujan and w_cerah and f_hujan and f2_mendung:
 		nkRendah[250]=min(sedang,sejuk,tdk_hujan,w_cerah,f_hujan,f2_mendung);
 	
 	if sedang and sejuk and tdk_hujan and w_cerah and f_hujan and f2_huan:
 		nkRendah[251]=min(sedang,sejuk,tdk_hujan,w_cerah,f_hujan,f2_hujan);

 	if sedang and sejuk and tdk_hujan and w_mendung and f_cerah and f2_cerah:
 		nkRendah[252]=min(sedang,sejuk,tdk_hujan,w_mendung,f_cerah,f2_cerah);

 	if sedang and sejuk and tdk_hujan and w_mendung and f_cerah and f2_mendung:
 		nkRendah[253]=min(sedang,sejuk,tdk_hujan,w_mendung,f_cerah,f2_mendung);

 	if sedang and sejuk and tdk_hujan and w_mendung and f_cerah and f2_hujan:
 		nkRendah[254]=min(sedang,sejuk,tdk_hujan,w_mendung,f_cerah,f2_hujan);

 	if sedang and sejuk and tdk_hujan and w_mendung and f_mendung and f2_cerah:
 		nkRendah[255]=min(sedang,sejuk,tdk_hujan,w_mendung,f_mendung,f2_cerah);

 	if sedang and sejuk and tdk_hujan and w_mendung and f_mendung and f2_mendung:
 		nkRendah[256]=min(sedang,sejuk,tdk_hujan,w_mendung,f_mendung,f2_mendung);

 	if sedang and sejuk and tdk_hujan and w_mendung and f_mendung and f2_hujan:
 		nkRendah[257]=min(sedang,sejuk,tdk_hujan,w_mendung,f_mendung,f2_hujan);

 	if sedang and sejuk and tdk_hujan and w_mendung and f_hujan and f2_cerah:
 		nkRendah[258]=min(sedang,sejuk,tdk_hujan,w_mendung,f_hujan,f2_cerah);

 	if sedang and sejuk and tdk_hujan and w_mendung and f_hujan and f2_mendung:
 		nkRendah[259]=min(sedang,sejuk,tdk_hujan,w_mendung,f_hujan,f2_mendung);

 	if sedang and sejuk and tdk_hujan and w_mendung and f_hujan and f2_hujan:
 		nkRendah[260]=min(sedang,sejuk,tdk_hujan,w_mendung,f_hujan,f2_hujan);

 	if sedang and sejuk and tdk_hujan and w_hujan and f_cerah and f2_cerah:
 		nkRendah[261]=min(sedang,sejuk,tdk_hujan,w_hujan,f_cerah,f2_cerah);

 	if sedang and sejuk and tdk_hujan and w_hujan and f_cerah and f2_mendung:
 		nkRendah[262]=min(sedang,sejuk,tdk_hujan,w_hujan,f_cerah,f2_mendung);

 	if sedang and sejuk and tdk_hujan and w_hujan and f_cerah and f2_hujan:
 		nkRendah[263]=min(sedang,sejuk,tdk_hujan,w_hujan,f_cerah,f2_hujan);

 	if sedang and sejuk and tdk_hujan and w_hujan and f_mendung and f2_cerah:
 		nkRendah[264]=min(sedang,sejuk,tdk_hujan,w_hujan,f_mendung,f2_cerah);

 	if sedang and sejuk and tdk_hujan and w_hujan and f_mendung and f2_mendung:
 		nkRendah[265]=min(sedang,sejuk,tdk_hujan,w_hujan,f_mendung,f2_mendung);

 	if sedang and sejuk and tdk_hujan and w_hujan and f_mendung and f2_hujan:
 		nkRendah[266]=min(sedang,sejuk,tdk_hujan,w_hujan,f_mendung,f2_hujan);

 	if sedang and sejuk and tdk_hujan and w_hujan and f_hujan and f2_cerah:
 		nkRendah[267]=min(sedang,sejuk,tdk_hujan,w_hujan,f_hujan,f2_cerah);

 	if sedang and sejuk and tdk_hujan and w_hujan and f_hujan and f2_mendung:
 		nkRendah[268]=min(sedang,sejuk,tdk_hujan,w_hujan,f_hujan,f2_mendung);

 	if sedang and sejuk and tdk_hujan and w_hujan and f_hujan and f2_hujan:
 		nkRendah[269]=min(sedang,sejuk,tdk_hujan,w_hujan,f_hujan,f2_hujan);

 	if sedang and dingin and hujan and w_cerah and f_cerah and f2_cerah:
 		nkRendah[270]=min(sedang,dingin,hujan,w_cerah,f_cerah,f2_cerah);

 	if sedang and dingin and hujan and w_cerah and f_cerah and f2_mendung:
 		nkRendah[271]=min(sedang,dingin,hujan,w_cerah,f_cerah,f2_mendung);

 	if sedang and dingin and hujan and w_cerah and f_cerah and f2_hujan:
 		nkRendah[272]=min(sedang,dingin,hujan,w_cerah,f_cerah,f2_hujan);

 	if sedang and dingin and hujan and w_cerah and f_mendung and f2_cerah:
 		nkRendah[273]=min(sedang,dingin,hujan,w_cerah,f_mendung,f2_cerah);
 	
 	if sedang and dingin and hujan and w_cerah and f_mendung and f2_mendung:
 		nkRendah[274]=min(sedang,dingin,hujan,w_cerah,f_mendung,f2_mendung);
 	
 	if sedang and dingin and hujan and w_cerah and f_mendung and f2_hujan:
 		nkRendah[275]=min(sedang,dingin,hujan,w_cerah,f_mendung,f2_hujan);

 	if sedang and dingin and hujan and w_cerah and f_hujan and f2_cerah:
 		nkRendah[276]=min(sedang,dingin,hujan,w_cerah,f_hujan,f2_cerah);

 	if sedang and dingin and hujan and w_cerah and f_hujan and f2_mendung:
 		nkRendah[277]=min(sedang,dingin,hujan,w_cerah,f_hujan,f2_mendung);
 	
 	if sedang and dingin and hujan and w_cerah and f_hujan and f2_huan:
 		nkRendah[278]=min(sedang,dingin,hujan,w_cerah,f_hujan,f2_hujan);

 	if sedang and dingin and hujan and w_mendung and f_cerah and f2_cerah:
 		nkRendah[279]=min(sedang,dingin,hujan,w_mendung,f_cerah,f2_cerah);

 	if sedang and dingin and hujan and w_mendung and f_cerah and f2_mendung:
 		nkRendah[280]=min(sedang,dingin,hujan,w_mendung,f_cerah,f2_mendung);

 	if sedang and dingin and hujan and w_mendung and f_cerah and f2_hujan:
 		nkRendah[281]=min(sedang,dingin,hujan,w_mendung,f_cerah,f2_hujan);

 	if sedang and dingin and hujan and w_mendung and f_mendung and f2_cerah:
 		nkRendah[282]=min(sedang,dingin,hujan,w_mendung,f_mendung,f2_cerah);

 	if sedang and dingin and hujan and w_mendung and f_mendung and f2_mendung:
 		nkRendah[283]=min(sedang,dingin,hujan,w_mendung,f_mendung,f2_mendung);

 	if sedang and dingin and hujan and w_mendung and f_mendung and f2_hujan:
 		nkRendah[284]=min(sedang,dingin,hujan,w_mendung,f_mendung,f2_hujan);

 	if sedang and dingin and hujan and w_mendung and f_hujan and f2_cerah:
 		nkRendah[285]=min(sedang,dingin,hujan,w_mendung,f_hujan,f2_cerah);

 	if sedang and dingin and hujan and w_mendung and f_hujan and f2_mendung:
 		nkRendah[286]=min(sedang,dingin,hujan,w_mendung,f_hujan,f2_mendung);

 	if sedang and dingin and hujan and w_mendung and f_hujan and f2_hujan:
 		nkRendah[287]=min(sedang,dingin,hujan,w_mendung,f_hujan,f2_hujan);

 	if sedang and dingin and hujan and w_hujan and f_cerah and f2_cerah:
 		nkRendah[288]=min(sedang,dingin,hujan,w_hujan,f_cerah,f2_cerah);

 	if sedang and dingin and hujan and w_hujan and f_cerah and f2_mendung:
 		nkRendah[289]=min(sedang,dingin,hujan,w_hujan,f_cerah,f2_mendung);

 	if sedang and dingin and hujan and w_hujan and f_cerah and f2_hujan:
 		nkRendah[290]=min(sedang,dingin,hujan,w_hujan,f_cerah,f2_hujan);

 	if sedang and dingin and hujan and w_hujan and f_mendung and f2_cerah:
 		nkRendah[291]=min(sedang,dingin,hujan,w_hujan,f_mendung,f2_cerah);

 	if sedang and dingin and hujan and w_hujan and f_mendung and f2_mendung:
 		nkRendah[292]=min(sedang,dingin,hujan,w_hujan,f_mendung,f2_mendung);

 	if sedang and dingin and hujan and w_hujan and f_mendung and f2_hujan:
 		nkRendah[293]=min(sedang,dingin,hujan,w_hujan,f_mendung,f2_hujan);

 	if sedang and dingin and hujan and w_hujan and f_hujan and f2_cerah:
 		nkRendah[294]=min(sedang,dingin,hujan,w_hujan,f_hujan,f2_cerah);

 	if sedang and dingin and hujan and w_hujan and f_hujan and f2_mendung:
 		nkRendah[295]=min(sedang,dingin,hujan,w_hujan,f_hujan,f2_mendung);

 	if sedang and dingin and hujan and w_hujan and f_hujan and f2_hujan:
 		nkRendah[296]=min(sedang,dingin,hujan,w_hujan,f_hujan,f2_hujan);

 	if sedang and dingin and tdk_hujan and w_cerah and f_cerah and f2_cerah:
 		nkRendah[297]=min(sedang,dingin,tdk_hujan,w_cerah,f_cerah,f2_cerah);

 	if sedang and dingin and tdk_hujan and w_cerah and f_cerah and f2_mendung:
 		nkRendah[298]=min(sedang,dingin,tdk_hujan,w_cerah,f_cerah,f2_mendung);

 	if sedang and dingin and tdk_hujan and w_cerah and f_cerah and f2_hujan:
 		nkRendah[299]=min(sedang,dingin,tdk_hujan,w_cerah,f_cerah,f2_hujan);

 	if sedang and dingin and tdk_hujan and w_cerah and f_mendung and f2_cerah:
 		nkRendah[300]=min(sedang,dingin,tdk_hujan,w_cerah,f_mendung,f2_cerah);
 	
 	if sedang and dingin and tdk_hujan and w_cerah and f_mendung and f2_mendung:
 		nkRendah[301]=min(sedang,dingin,tdk_hujan,w_cerah,f_mendung,f2_mendung);
 	
 	if sedang and dingin and tdk_hujan and w_cerah and f_mendung and f2_hujan:
 		nkRendah[302]=min(sedang,dingin,tdk_hujan,w_cerah,f_mendung,f2_hujan);

 	if sedang and dingin and tdk_hujan and w_cerah and f_hujan and f2_cerah:
 		nkRendah[303]=min(sedang,dingin,tdk_hujan,w_cerah,f_hujan,f2_cerah);

 	if sedang and dingin and tdk_hujan and w_cerah and f_hujan and f2_mendung:
 		nkRendah[304]=min(sedang,dingin,tdk_hujan,w_cerah,f_hujan,f2_mendung);
 	
 	if sedang and dingin and tdk_hujan and w_cerah and f_hujan and f2_huan:
 		nkRendah[305]=min(sedang,dingin,tdk_hujan,w_cerah,f_hujan,f2_hujan);

 	if sedang and dingin and tdk_hujan and w_mendung and f_cerah and f2_cerah:
 		nkRendah[306]=min(sedang,dingin,tdk_hujan,w_mendung,f_cerah,f2_cerah);

 	if sedang and dingin and tdk_hujan and w_mendung and f_cerah and f2_mendung:
 		nkRendah[307]=min(sedang,dingin,tdk_hujan,w_mendung,f_cerah,f2_mendung);

 	if sedang and dingin and tdk_hujan and w_mendung and f_cerah and f2_hujan:
 		nkRendah[308]=min(sedang,dingin,tdk_hujan,w_mendung,f_cerah,f2_hujan);

 	if sedang and dingin and tdk_hujan and w_mendung and f_mendung and f2_cerah:
 		nkRendah[309]=min(sedang,dingin,tdk_hujan,w_mendung,f_mendung,f2_cerah);

 	if sedang and dingin and tdk_hujan and w_mendung and f_mendung and f2_mendung:
 		nkRendah[310]=min(sedang,dingin,tdk_hujan,w_mendung,f_mendung,f2_mendung);

 	if sedang and dingin and tdk_hujan and w_mendung and f_mendung and f2_hujan:
 		nkRendah[311]=min(sedang,dingin,tdk_hujan,w_mendung,f_mendung,f2_hujan);

 	if sedang and dingin and tdk_hujan and w_mendung and f_hujan and f2_cerah:
 		nkRendah[312]=min(sedang,dingin,tdk_hujan,w_mendung,f_hujan,f2_cerah);

 	if sedang and dingin and tdk_hujan and w_mendung and f_hujan and f2_mendung:
 		nkRendah[313]=min(sedang,dingin,tdk_hujan,w_mendung,f_hujan,f2_mendung);

 	if sedang and dingin and tdk_hujan and w_mendung and f_hujan and f2_hujan:
 		nkRendah[314]=min(sedang,dingin,tdk_hujan,w_mendung,f_hujan,f2_hujan);

 	if sedang and dingin and tdk_hujan and w_hujan and f_cerah and f2_cerah:
 		nkRendah[315]=min(sedang,dingin,tdk_hujan,w_hujan,f_cerah,f2_cerah);

 	if sedang and dingin and tdk_hujan and w_hujan and f_cerah and f2_mendung:
 		nkRendah[316]=min(sedang,dingin,tdk_hujan,w_hujan,f_cerah,f2_mendung);

 	if sedang and dingin and tdk_hujan and w_hujan and f_cerah and f2_hujan:
 		nkRendah[317]=min(sedang,dingin,tdk_hujan,w_hujan,f_cerah,f2_hujan);

 	if sedang and dingin and tdk_hujan and w_hujan and f_mendung and f2_cerah:
 		nkRendah[318]=min(sedang,dingin,tdk_hujan,w_hujan,f_mendung,f2_cerah);

 	if sedang and dingin and tdk_hujan and w_hujan and f_mendung and f2_mendung:
 		nkRendah[319]=min(sedang,dingin,tdk_hujan,w_hujan,f_mendung,f2_mendung);

 	if sedang and dingin and tdk_hujan and w_hujan and f_mendung and f2_hujan:
 		nkRendah[320]=min(sedang,dingin,tdk_hujan,w_hujan,f_mendung,f2_hujan);

 	if sedang and dingin and tdk_hujan and w_hujan and f_hujan and f2_cerah:
 		nkRendah[321]=min(sedang,dingin,tdk_hujan,w_hujan,f_hujan,f2_cerah);

 	if sedang and dingin and tdk_hujan and w_hujan and f_hujan and f2_mendung:
 		nkRendah[322]=min(sedang,dingin,tdk_hujan,w_hujan,f_hujan,f2_mendung);

 	if sedang and dingin and tdk_hujan and w_hujan and f_hujan and f2_hujan:
 		nkRendah[323]=min(sedang,dingin,tdk_hujan,w_hujan,f_hujan,f2_hujan);
	
	
	#nkRendah.append(5);
	#nkRendah.insert(1,6);

	
	return str(nkRendah[0]) + ', ' + str(min(10,20,30,40,50,60,70,0.5)) + ', ' + str(basah);
