import os, collections, hashlib, json, matplotlib.pyplot
import datetime

c = collections.Counter()

path_to_tg = "/home/goracionewport/Downloads/Telegram Desktop/ChatExport_2021-08-18/"
path_to_vk = "/home/goracionewport/Downloads/messages/349719281/"
path_to_tgH = str(int(hashlib.sha256((path_to_tg + path_to_vk).encode('utf-8')).hexdigest(), 16) % 10**8)

# path_to_vkH = str(int(hashlib.sha256(path_to_vk.encode('utf-8')).hexdigest(), 16) % 10**8)

strToMonth = {
	'Jan': '01',
	'Feb': '02',
	'Mar': '03',
	'Apr': '04',
	'May': '05',
	'Jun': '06',
	'Jul': '07',
	'Aug': '08',
	'Sep': '09',
	'Oct': '10',
	'Nov': '11',
	'Dec': '12'
}

def stringToDate(s):
	return datetime.datetime.strptime(s[0:6] + s[8:10] + " 00:00:00", '%d.%m.%y %H:%M:%S')

def process():
	print("Telegram messages analytics initated...")
	ind = 0
	fin = len(os.listdir(path_to_tg))
	# for f in os.listdir(path_to_tg):
	# 	ind += 1
	# 	if (f[0] != 'm'): continue
	# 	print("["+str(ind) + '/' + str(fin) + "] Processing", f, "...")
	# 	F = open(path_to_tg + f, 'r')
	# 	rawf = F.read()

	# 	for i in range(len(rawf) - 5):
	# 		if (rawf[i:i + 6] == 'title='):
	# 			c[rawf[i + 7:i + 17]] += 1

	print("VK messages analytics initated...")
	ind = 0
	fin = len(os.listdir(path_to_vk))
	for f in os.listdir(path_to_vk):
		ind += 1
		if (f[0] != 'm'): continue
		print("["+str(ind) + '/' + str(fin) + "] Processing", f, "...")
		F = open(path_to_vk + f, 'r', encoding='utf-8', errors='ignore')
		rawf = F.read()

		for i in range(len(rawf) - 50):
				if (rawf[i:i + 4] == ', at'):
					rawk = rawf[i:i+40].split()
					# print(rawk)
					day = str(rawk[6][:-1])
					if (len(day) == 1): day = '0' + day
					month = str(strToMonth[rawk[5]])
					year = str(rawk[7][:4])
					# print(day, month, year)
					# c[datetime.date(year, month, day)] += 1
					c[day + '.' + month + '.' + year] += 1
	# os.exit(0)

	print("Writing result to ./cache/" + path_to_tgH + ".hz ...")
	with open('./cache/' + path_to_tgH + '.hz', 'w') as g:
		g.write(json.dumps(c))

if (os.path.isfile('./cache/' + path_to_tgH + '.hz')):
	print("Pre-processed file found. Would you like to update it? (Y/N)")
	r = input()
	if (r == "N" or r == "n"):
		with open('./cache/' + path_to_tgH + '.hz', 'r') as g:
			c = collections.Counter(json.loads(g.read()))
	else: process()
else: process()

rawPlotX = []
rawPlotY = []

for k,v in c.most_common():
	print(k, v)
	rawPlotX.append(stringToDate(k))
	rawPlotY.append(v)

# print(rawPlot)

matplotlib.pyplot.bar(rawPlotX, rawPlotY)
# matplotlib.pyplot.subplots()[1].set_xlim([datetime.date(2021, 6, 1), datetime.date(2021, 9, 1)])
# matplotlib.pyplot.subplots()[1].set_ylim([0, 1500])
matplotlib.pyplot.show()