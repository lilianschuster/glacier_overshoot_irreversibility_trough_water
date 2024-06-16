#!/bin/bash
#
#SBATCH --job-name=oversh_hydro
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --time=09:00:00 #72
#SBATCH --mail-user=lilian.schuster@uibk.ac.at
#SBATCH --qos=normal

# Abort whenever a single step fails. Without this, bash will just continue on errors.
set -e

# Current RGI region
OGGM_GLACIER_JOB=$SLURM_ARRAY_TASK_ID
export OGGM_GLACIER_JOB
echo "OGGM_GLACIER_JOB number : $OGGM_GLACIER_JOB"

# On every node, when slurm starts a job, it will make sure the directory
# /work/username exists and is writable by the jobs user.
# We create a sub-directory there for this job to store its runtime data at.
OGGM_WORKDIR="/work/$SLURM_JOB_USER/$SLURM_JOB_ID/wd"
mkdir -p "$OGGM_WORKDIR"
export OGGM_WORKDIR
echo "Workdir for this run: $OGGM_WORKDIR"

# Use the local data download cache
export OGGM_DOWNLOAD_CACHE=/home/data/download
export OGGM_DOWNLOAD_CACHE_RO=1
export OGGM_EXTRACT_DIR="/work/$SLURM_JOB_USER/$SLURM_JOB_ID/oggm_tmp"
export OGGM_USE_MULTIPROCESSING=1

# Try to make mp better
# export OGGM_USE_MP_SPAWN=1

# Link www fmaussion data here to avoid useless downloads
mkdir -p "$OGGM_WORKDIR/cache/cluster.klima.uni-bremen.de"
ln -s /home/www/fmaussion "$OGGM_WORKDIR/cache/cluster.klima.uni-bremen.de/~fmaussion"
ln -s /home/www/lschuster "$OGGM_WORKDIR/cache/cluster.klima.uni-bremen.de/~lschuster"


# Add other useful defaults
export LRU_MAXSIZE=1000

OGGM_OUTDIR="/work/$SLURM_JOB_USER/$SLURM_JOB_ID/out"
export OGGM_OUTDIR
echo "Output dir for this run: $OGGM_OUTDIR"

# All commands in the EOF block run inside of the container
# Adjust container version to your needs, they are guaranteed to never change after their respective day has passed.
srun -n 1 -c "${SLURM_JOB_CPUS_PER_NODE}" singularity exec /home/users/lschuster/images/oggm_20230222.sif bash -s <<EOF
  set -e
  # Setup a fake home dir inside of our workdir, so we don't clutter the actual shared homedir with potentially incompatible stuff.
  export HOME="$OGGM_WORKDIR/fake_home"
  mkdir "\$HOME"
  # Create a venv that _does_ use system-site-packages, since everything is already installed on the container.
  # We cannot work on the container itself, as the base system is immutable.
  python3 -m venv --system-site-packages "$OGGM_WORKDIR/oggm_env"
  source "$OGGM_WORKDIR/oggm_env/bin/activate"
  # Make sure latest pip is installed
  # pip install --upgrade pip setuptools
  # install same OGGM as for the preprocessed gdirs (basically corresponds to oggm v1.6.1)
  #pip install --no-deps "git+https://github.com/OGGM/oggm.git@TODO
  #https://github.com/pat-schmitt/oggm/commit/b45b78bbfa95ed1f625c657e67393eaf89d2b72e
  #pip install --no-deps "git+https://github.com/pat-schmitt/oggm.git@6b133cb76c32ca855743485fcb80aaccd54fb0ae"
  # pip install --no-deps "git+https://github.com/OGGM/oggm.git@03248bd82ed391b231ddc7d6f8fb4b7917fa6fdb"
  # correct version for v2023.3 gdirs: 
  pip install --no-deps "git+https://github.com/OGGM/oggm.git@f8a1745d75a2921a44a6ef3ebc93757664b894ba"

  # Increase number of allowed open file descriptors
  ulimit -n 65000
  # Finally, the run
  python 0_run_with_hydro_oversh_stab_per_rgi_reg_2500incl.py $1
EOF

# Write out
echo "Copying files..."
rsync -avzh "$OGGM_OUTDIR/" output

# Print a final message so you can actually see it being done in the output log.
echo "SLURM DONE"
