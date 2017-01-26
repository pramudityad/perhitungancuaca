import datetime, time

def calculate(soil,suhu,rain,weather,forecast):
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
	l_panas	 = 30;
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

	
	return str(kering) + ', ' + str(sedang) + ', ' + str(basah);
