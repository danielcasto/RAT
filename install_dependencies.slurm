#!/bin/bash

#SBATCH --job-name=install_dependencies_for_RATPoison
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user={YOUR_EMAIL_HERE}
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=16gb
#SBATCH --time=10:00:00
#SBATCH --output=install_dependencies_for_RATPoison%j.log

date; hostname; pwd

module load conda

conda create -n "rat_poison_env" python=3.9.7
conda activate rat_poison_env

pip install -r {PATH_TO_REQUIREMENTS.TXT}

conda deactivate

### To use this conda environment, in an interactive session (NOT login node), enter command:
###     export PATH={PATH_TO_CONDA_ENV}/bin:$PATH
###
### Then, in the RAT repository, run command:
###     python main.py

date