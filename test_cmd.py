# streaming.py
#!/usr/bin/env python3
import os
import urllib3
import certifi

name_set = "Adobe Acrobat Reader DC"

urlset = [
"ftp://ftp.adobe.com/pub/adobe/reader/win/AcrobatDC/2000920063/AcroRdrDC2000920063_en_US.exe",
"ftp://ftp.adobe.com/pub/adobe/reader/win/AcrobatDC/2000920067/AcroRdrDCUpd2000920067.msp"]
def check_programs():
	stream = os.popen('wmic product get name')
	#stream = ['wmic product get name', 'wmic product get name', ' ', 'wmic product get name', '  ']

	# remove empty string
	prod_list = []
	for x in stream:
		x = x.strip()
		if x:
			prod_list.append(x)
	return(prod_list)

def check_install(args):
	for val in args:
		if val == name_set:
			return 1

def download(args):
	if args == 0:
		print('arg zero')
	elif args == 1:
		local_filename = urlset[args].split('/')[-1]
		print(urlset[args])
		http = urllib3.PoolManager()
		resp = http.request('GET', str(urlset[args]), preload_content=False)
		with open(local_filename, 'wb') as f:
			for chunk in resp.stream(1024):
				f.write(chunk)
		resp.release_conn()


	'''
	
	if resp.status == 200:
		print("download . . . . . Ok!")
	else:
		print("error!")
		'''
'''
def inst(args):
	# For cmd 
	wmic /OUTPUT:c:\\temp\\temp_my_software.txt product get name
	AcroRdrDC2000920063_en_US.exe /sAll

http = urllib3.PoolManager(ca_certs=certifi.where())
'''
#list_prog = check_programs()

list_prog = ["Python 3.8.2 Documentation (64-bit)",
"Microsoft Visual C++ 2008 Redistributable - x64 9.0.30729.6161",
"Adobe Acrobat Reader DC",
"Python 3.7.5 Executables (64-bit symbols)",
"Microsoft .NET Core AppHost Pack - 3.1.4 (x64_arm64)",
"Џ®бв ўйЁЄ OLE DB ¤«п Microsoft Analysis Services"]

ch_ins = check_install(list_prog)
download(ch_ins)