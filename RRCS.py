from rrcs_step2 import main
from rrcs_step1 import mapping

def cal_rrcs(lines, gpcr_id, filename):
	al = {'ALA':'A','GLY':'G','VAL':'V','ILE':'I','LEU':'L','MET':'M','SER':'S','THR':'T','PRO':'P','CYS':'C','PHE':'F','TYR':'Y','HIS':'H','TRP':'W','GLU':'E','ASP':'D','GLN':'Q','ASN':'N','ARG':'R','LYS':'K'}
	result = main(filename, lines)
	mapnum = mapping(gpcr_id)
	rrcsFinalResult = []
	for line in result:
		res1 = line.split()[1]
		res2 = line.split()[4]
		resn1 = line.split()[2]
		resn2 = line.split()[5]
		score = line.split()[6]
		key1 = al[res1] + resn1
		key2 = al[res2] + resn2
		try:
			rrcsFinalResult.append([mapnum[key1], key1[0], key1[1:], mapnum[key2], key2[0], key2[1:], score])
		except:
			if key1 not in mapnum.keys():
				print ("%s named different in PDB and GPCRDB, a mutation?\n" % key1)
				for key in mapnum.keys():
					if key1[1:] == key[1:]:
						key1 = key
			if key2 not in mapnum.keys():
				print ("%s named different in PDB and GPCRDB, a mutation?\n" % key2)
				for key in mapnum.keys():
					if key2[1:] == key[1:]:
						key2 = key
			rrcsFinalResult.append([mapnum[key1], key1[0], key1[1:], mapnum[key2], key2[0], key2[1:], score])
	return rrcsFinalResult
