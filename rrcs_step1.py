import urllib.request
def mapping(gpcr_id):
	url_base = "http://gpcrdb.org/protein/"
	url_ = url_base + gpcr_id
	f = urllib.request.urlopen(url_)
	content = f.read().decode("utf-8")
	fw = open(gpcr_id + "net", "w")
	fw.write(content)
	fr = open(gpcr_id + "net", "r")
	fw1 = open(gpcr_id + "step1", "w")
	mark1 = "title=\"<div class='no-wrap'>"
	mark2 = "<div class='no-wrap'>Sequence"
	mark3 = "<div class='no-wrap'>GPCRdb"
	location = None
	sequence = None
	gpcrnum  = None
	content = ""
	while True:
		line = fr.readline()
		if not line:
			break
		if (mark1 in line):
			#print (line.split('>')[1].strip())
			location = line.split('>')[1].strip()
			fw1.write("\n" + location + ",")
			content = content + "\n" + location + ","
		if (mark2 in line):
			#print (line.split('#')[1][1:].strip())
			sequence = line.split('#')[1][1:].strip()
			fw1.write(sequence[0] + "," + sequence[1:] + ",")
			content = content + sequence[0] + "," + sequence[1:] + ","
		if (mark3 in line):
			#print (line.split('#')[1][1:].strip())
			gpcrnum  = line.split('#')[1][1:].strip()
			fw1.write(gpcrnum[1:] + ",")
			content = content + gpcrnum[1:] + ","
	lines = content.split('\n')
	mapping = {}
	for line in lines:
		if line == "":
			continue
		location = line.split(',')[0]
		residue = line.split(',')[1]
		number = line.split(',')[2]
		gpcrnum = line.split(',')[3]
		key = residue + number
		if gpcrnum != '':
			mapping[key] = gpcrnum
		else:
			mapping[key] = key
	return mapping

