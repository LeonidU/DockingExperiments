from pathlib import Path
import sys
import os
import numpy as np
import torch

from chai_lab.chai1 import run_inference

# We use fasta-like format for inputs.
# Every record may encode protein, ligand, RNA or DNA
#  see example below


protein = """
>protein|Hsosn_jg38733.t1
MSLTAFAVVLLLMVALGTFIYFRRATTSDGGHKPPPGPIGLPLIGSLHMLGKLPHRNLYEMSRKYGPIMS
LRLGLIPTIVVSSPAAAELFLKTHDTNFANRPTVQLAVEHFYGSKTMLFAEFGGYWRSVRKFCTLELLSP
KKIDSMAWLRREELGFMVESLKDAARTGQVVDVSGKVAGLMEDVTCRMLLGKSGDDRFDLREVLKELTKT
AGEFNVADFIPFLRALDLQGITRRTKVAGQELDKILEIIIDDHEQEASEGHGNLERDFVDVLLSLKNNPT
SRRGCPGLTAPRAEHVLAIPKIRQI
"""

stat = open(sys.argv[2], 'w')
for chem in open(sys.argv[1], 'r'):
	chem = chem.rstrip("\n")
	smiles, name = chem.split("\t")
	print(name)
	structure = protein+">ligand|"+name+"\n"+smiles
	fasta_path = Path("/tmp/example.fasta")
	fasta_path.write_text(structure)
	output_dir = Path("outputs")
	output_cif_paths = run_inference(fasta_file=fasta_path, output_dir=output_dir,num_trunk_recycles=3,num_diffn_timesteps=200,seed=42,device=torch.device("cuda:0"),use_esm_embeddings=True)
	scores = np.load(output_dir.joinpath("scores.model_idx_0.npz"))
	stat.write("Hsosn_jg38733\t"+name+"\t"+str(scores["aggregate_score"][0])+"\t"+str(scores["ptm"][0])+"\t"+str(scores["iptm"][0])+"\t"+str(scores["chain_intra_clashes"])+"\n")
	os.system("mv outputs \""+name+"\"")
