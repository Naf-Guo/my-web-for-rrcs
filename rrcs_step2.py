import numpy as np
import time

class PDB(object):
	def __init__(self, pdbid):
		self.pdbid = pdbid
		self.moleculars = {}
	def get_molecular(self, name):
		if name not in self.moleculars.keys():
			self.moleculars[name] = Molecular(self, name)
		return self.moleculars[name]
	def get_all_mol_name(self):
		List = []
		for key in self.moleculars.keys():
			List.append(key)
		return List

class Molecular(object):
	def __init__(self, PDB, name):
		self.PDB = PDB
		self.name = name
		self.atoms = {}
	def get_atom(self, atom_type):
		if atom_type not in self.atoms.keys():
			self.atoms[atom_type] = Atom(self, atom_type)
		return self.atoms[atom_type]
	def get_XYZ(self):
		List = []
		for atom in self.atoms.values():
			List.append(atom.get_XYZ())
		return List
	def get_all_atom_name(self):
		List = []
		for key in self.atoms.keys():
			List.append(key)
		return List

class Atom(object):
	def __init__(self, molecular, atom_type):
		self.molecular = molecular
		self.atom_type = atom_type
		self.coordinate = None
		self.occ = None
	def add_XYZ(self, x, y, z, occ):
		self.coordinate = [x, y, z]
		self.occ = occ
	def get_XYZ(self):
		return self.coordinate
	def cal_distance(self, another):
		coordinate_1 = np.array(self.get_XYZ())
		coordinate_2 = np.array(another.get_XYZ())
		if (coordinate_1[0] - coordinate_2[0] > 4.62) or (coordinate_1[1] - coordinate_2[1] > 4.62) or (coordinate_1[2] - coordinate_2[2] > 4.62):
			return 5
		if np.shape(np.shape(coordinate_2))[0] == 1:
			distance = (np.sum((coordinate_1 - coordinate_2)**2))**0.5
		else:
			distance = (np.sum((coordinate_1 - coordinate_2)**2, axis = 1))**0.5
		return distance

def importPDB(filename, lines):
	All = PDB(filename)
	for line in lines:
		if line[0:4] == 'ATOM' :
			mol = line[17:20].strip() + '_' + line[21:22] + '_' + line[22:26].strip()
			atom = line[12:16].strip() + '_' + line[6:11].strip()
			x = float(line[30:38].strip())
			y = float(line[38:46].strip())
			z = float(line[46:54].strip())
			occ = float(line[54:60].strip())
			All.get_molecular(mol).get_atom(atom).add_XYZ(x, y, z, occ)
		"""if line[0:6] == 'HETATM' and line[17:20].strip() not in ('HOH', 'DUM') :
			mol = line[17:20].strip() + line[21:22] + line[22:26].strip()
			atom = line[12:16].strip() + line[6:11].strip()
			x = float(line[30:38].strip())
			y = float(line[38:46].strip())
			z = float(line[46:54].strip())
			All.get_molecular(mol).get_atom(atom).add_XYZ(x, y, z)"""
	return All

def findmol(PDBClass, res = None, chain = None, index = None):
	list1 = PDBClass.get_all_mol_name()
	set1 = []
	set2 = []
	set3 = []
	if not res and not chain and not index:
		print ("Error: please specify residue")
		return list1
	if res!=None:
		for mol in list1:
			#print (mol)
			RES = mol.split('_')[0]
			if res == RES:
				set1.append(mol)
	else:
		set1 = list1
	if chain!=None:
		for mol in list1:
			#print (mol)
			CHAIN = mol.split('_')[1]
			if chain == CHAIN:
				set2.append(mol)
	else:
		set2 = list1
	if index!=None:
		for mol in list1:
			#print (mol)
			INDEX = int(mol.split('_')[2])
			if index == INDEX:
				set3.append(mol)
	else:
		set3 = list1
	set1 = set(set1)
	set2 = set(set2)
	set3 = set(set3)
	final = set1 & set2 & set3
	return final

def findatom(PDBClass, res = None, chain = None, res_index = None, atom = None, atom_index = None):
	if res != None and res_index != None and chain != None and atom == None:
		name = res + '_' + str(chain) + '_' + str(res_index)
		return PDBClass.get_molecular(name).get_all_atom_name()
	if res != None and res_index != None and atom != None and chain != None:
		name = res + '_' + str(chain) + '_' + str(res_index)
		for item in PDBClass.get_molecular(name).get_all_atom_name():
			atom_type = item.split('_')[0]
			if atom == atom_type:
				return (name,item)
	atom_list = []
	list1 = PDBClass.get_all_mol_name()
	if atom_index != None:
		for mol in list1:
			atom_list = PDBClass.get_molecular(mol).get_all_atom_name()
			for item in atom_list:
				atom_type = item.split('_')[0]
				atom_num = int(item.split('_')[1])
				if atom_index == atom_num:
					return (mol,item)
	print ("Error: atom can not be found under given parameters")

def calculate_mol(f, res1, chain1, index1, res2, chain2, index2):
	aminolist = ['ALA','GLY','VAL','ILE','LEU','MET','SER','THR','PRO','CYS','PHE','TYR','HIS','TRP','GLU','ASP','GLN','ASN','ARG','LYS']
	name1 = res1 + '_' + chain1 + '_' + str(index1)
	name2 = res2 + '_' + chain2 + '_' + str(index2)
	result = []
	Allscore = 0.0
	if chain1 == chain2 and abs(index1 - index2) < 5 or (res1 not in aminolist or res2 not in aminolist):	
		for atom1 in f.get_molecular(name1).get_all_atom_name():
			#print (atom1)
			if atom1.split('_')[0] in ('C', 'O', 'N', 'CA'):
				continue
			for atom2 in f.get_molecular(name2).get_all_atom_name():
				#print (atom2)
				if atom2.split('_')[0] in ('C', 'O', 'N', 'CA'):
					continue
				dis = f.get_molecular(name1).get_atom(atom1).cal_distance(f.get_molecular(name2).get_atom(atom2))
				#print ("%s %s %s %s %.3f" % (name1, atom1, name2, atom2, dis))
				if dis >= 4.63:
					score = 0
				elif dis <= 3.23:
					score = 1.0 * f.get_molecular(name1).get_atom(atom1).occ * f.get_molecular(name2).get_atom(atom2).occ
				else:
					score = (1 - (dis - 3.23)/1.4) * f.get_molecular(name1).get_atom(atom1).occ * f.get_molecular(name2).get_atom(atom2).occ
				Allscore = Allscore + score
	else:
		for atom1 in f.get_molecular(name1).get_all_atom_name():
			#print (atom1)
			for atom2 in f.get_molecular(name2).get_all_atom_name():
				#print (atom2)
				dis = f.get_molecular(name1).get_atom(atom1).cal_distance(f.get_molecular(name2).get_atom(atom2))
				#print ("%s %s %s %s %.3f" % (name1, atom1, name2, atom2, dis))
				if dis >= 4.63:
					score = 0
				elif dis <= 3.23:
					score = 1.0 * f.get_molecular(name1).get_atom(atom1).occ * f.get_molecular(name2).get_atom(atom2).occ
				else:
					score = (1 - (dis - 3.23)/1.4) * f.get_molecular(name1).get_atom(atom1).occ * f.get_molecular(name2).get_atom(atom2).occ
				#print (score)				
				Allscore = Allscore + score
	if Allscore > 0:
		#print ("%s %s %i %s %s %i %.6f" % (chain1, res1, index1, chain2, res2, index2, Allscore))
		result.append("%s %s %i %s %s %i %.6f" % (chain1, res1, index1, chain2, res2, index2, Allscore))
	return result
			
def calculate_atom(f, atom1_index, atom2_index):
	name1 = findatom(f,atom_index = atom1_index)
	name2 = findatom(f,atom_index = atom2_index)
	atom1 = f.get_molecular(name1[0]).get_atom(name1[1])
	atom2 = f.get_molecular(name2[0]).get_atom(name2[1])
	dis = atom1.cal_distance(atom2)
	#print ("%s %s : %.3f" % (name1, name2, dis))
	return dis

def main(filename, lines):
	f = importPDB(filename, lines)
	list1 = f.get_all_mol_name()
	length = len(list1)
	result = []
	for i in range(0, length):
		mol1 = list1[i]
		res1 = mol1.split('_')[0]
		chain1 = mol1.split('_')[1]
		index1 = int(mol1.split('_')[2])
		for j in range(i+1, length):
			mol2 = list1[j]
			res2 = mol2.split('_')[0]
			chain2 = mol2.split('_')[1]
			index2 = int(mol2.split('_')[2])
			result = result + calculate_mol(f, res1, chain1, index1, res2, chain2, index2)
	return result
#print ("-------------------------------------")
#print ("PDBClass.main(PDB) would calculate the map of given PDB file")
#print ("EG: PDBClass.main('5XR8'), the result file would be 5XRBresult")
#print ("if you want to calculate specific residue pairs:")
#print ("f = PDBClass.importPDB(PDB)")
#print ("fw = open(outputfilename, 'w')")
#print ("PDBClass.calculate_mol(f, fw, residue1, chain1, index1, residue2, chain2, index2)")
#print ("and you should get the result in outputfilename")
#print ("-------------------------------------")
