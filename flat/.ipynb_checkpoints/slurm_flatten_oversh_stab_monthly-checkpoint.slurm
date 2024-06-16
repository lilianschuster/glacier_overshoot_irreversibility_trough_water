#!/bin/bash
#
#SBATCH --job-name=flatten_oversh
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=64
#SBATCH --time=3:00:00
#SBATCH --mail-user=lilian.schuster@student.uibk.ac.at
#SBATCH --mail-type=ALL
#SBATCH --qos=high

# Abort whenever a single step fails. Without this, bash will just continue on errors.
set -e

# Load the required environment modules for OGGM
module load oggm-binary-deps/4 python/3.8 
# Activate our local OGGM virtualenv
source ~/oggm_env/bin/activate
# source ./oggm_venv/bin/activate
# On every node, when slurm starts a job, it will make sure the directory
# /work/username exists and is writable by the jobs user.
# We create a sub-directory there for this job to store its runtime data at.


echo "Start ..."

WORKDIR="/work/$SLURM_JOB_USER/$SLURM_JOB_ID"
mkdir -p "$WORKDIR"

# Export the WORKDIR as environment variable so our script can use it to find its working directory.
export WORKDIR

# Use the local data download cache
export OGGM_DOWNLOAD_CACHE=/home/data/download
export OGGM_DOWNLOAD_CACHE_RO=1
export OGGM_EXTRACT_DIR="/work/$SLURM_JOB_USER/$SLURM_JOB_ID/oggm_tmp"

# Run the actual job. The srun invocation starts it as individual step for slurm.
srun -n 1 -c "${SLURM_JOB_CPUS_PER_NODE}" /home/users/lschuster/images/oggm_20230222.sif bash -s <<EOF
	set -e
    python3 /home/www/lschuster/provide/gfdl-esm2m_oversh_stab_uni_bern/flatten_oversh_stab_monthly_files.py $1
EOF

#-c "print('hallo')"

# echo "Start copying..."


# Print a final message so you can actually see it being done in the output log.
echo "SLURM DONE"
