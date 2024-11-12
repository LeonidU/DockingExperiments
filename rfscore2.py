import os
import sys
from os import listdir
from os.path import isfile, join
import subprocess

# RF-Score v2 is a machine learning-based scoring function for predicting binding affinities of protein-ligand complexes.
# Computation based on AutoDock Vina docking scores and RF-Score v2 scoring function.
# Arguments:
# Arg1: Directory with folded (PDB) ligands
# Arg2: Directory with folded (PDB) proteins
# Output: Tab-separated file with ligand, protein, RF-Score v2, and affinity

def run(command):
    print(command)
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=False)
    # Wait for the process to finish and get the output
    stdout, stderr = process.communicate()
    print(stdout)
    print(stderr)
    # Check if there was any error
    if process.returncode != 0:
        print('An error occurred:', stderr.decode())
    else:
        print('Command executed successfully.')


f = open(sys.argv[2] 'w')
#Here I make for-loop for all ligands and proteins
for ligand in os.listdir(sys.argv[1]):
    for protein in os.listdir(sys.argv[2]):
        #Here I make for-loop for all ligands and proteins
        print("oddt_cli -n 50 %s --dock autodock_vina --receptor %s --score rfscore_v2 -O output_proteins.sdf"  % (sys.argv[1]+"/"+ligand, sys.argv[2]+"/"+protein))
        run(["oddt_cli", "-n", "50", "%s" % sys.argv[1]+"/"+ligand, "--dock", "autodock_vina",  "--receptor", "%s" % sys.argv[2]+"/"+protein,  "--score", "rfscore_v2", "-O", "output_proteins.sdf"])
        rfscore_flag, affinity_flag = False, False
        rfscore, affinity = 0.0, 0.0
        for elem in open("output_proteins.sdf", 'r'):
            if rfscore_flag:
                rfscore = float(elem)
                rfscore_flag = False
            if affinity_flag:
                affinity = float(elem)
                affinity_flag = False
            if "rfscore_v2" in elem:
                rfscore_flag = True
            if "affinity" in elem:
                affinity_flag = True
            if "$$$$" in elem:
                break
        #Here I write results to file
        f.write("%s\t%s\t%f\t%f\n" % (ligand, protein, rfscore, affinity))

f.close()
