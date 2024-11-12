import sys, rdkit, meeko
from rdkit.Chem import AllChem
#Ligand folding for docking

for elem in open(sys.argv[1], 'r'):
	smiles = elem.rstrip("\n").split("\t")[-1]
	print(smiles)
	print(elem)
	lig = rdkit.Chem.MolFromSmiles(smiles)
	protonated_lig = rdkit.Chem.AddHs(lig)
	AllChem.EmbedMolecule(protonated_lig)
	meeko_prep = meeko.MoleculePreparation()
	meeko_prep.prepare(protonated_lig)
	lig_pdbqt = meeko_prep.write_pdbqt_string()
	ff = open(elem.rstrip("\n").replace("\\", "_").replace("/","").split("\t")[0]+".pdbqt", 'w')
	ff.write(lig_pdbqt)
	ff.close()
