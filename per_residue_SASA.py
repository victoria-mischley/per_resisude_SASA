from pyrosetta import *
from pyrosetta.rosetta.core.scoring.sasa import SasaCalc
import argparse
from pathlib import Path
import pandas as pd 
init()


def args():
	parser = argparse.ArgumentParser(description='Combine dataframes')

	# Add command line arguments
	parser.add_argument('--file_path', type=str, help='path to location of file')
	# Parse the command line arguments
	args = parser.parse_args()

	return args

def main(file_path):
    file_name = file_path.name
    folder_name = file_path.parent
    pose = pose_from_pdb(f"{file_path}")
    sasa_calc = SasaCalc()
    sasa_calc.calculate(pose)
    sasa_list = []
    residue_list = []
    all_sasa = sasa_calc.get_residue_sasa()
    for i in range(1, pose.total_residue() + 1):
        Residue = i
        sasa_list.append(all_sasa[i])
        residue_list.append(i)
    
    df = pd.DataFrame({'Residue': residue_list, 'SASA': sasa_list})
    output_file_path = f"{folder_name}/{file_name}_per_res_SASA.csv"
    df.to_csv(output_file_path, index = False)


        

if __name__ == '__main__':
    args = args()
    file_path = Path(args.file_path)
    main(file_path)

