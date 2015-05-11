Latency Test
============

This repo contains the codes to carry out Latency Tests on Comet.

Background
----------

Latency is the time delay between simulation and response between 2 nodes. For this test, we send 1 Mb data from one node to another and calculate the time delay. This calculation is carried out using the [OMB Benchmark](https://www.nersc.gov/users/computational-systems/cori/nersc-8-procurement/trinity-nersc-8-rfp/nersc-8-trinity-benchmarks/omb-mpi-tests/) module under the [MVAPICH Package](http://mvapich.cse.ohio-state.edu/benchmarks/) to carry out our Latency tests.

The Comet CPU node architecture is illustrated below:
![Architecture](https://github.com/SDSC-HPC-Consultants/Latency_Test/blob/master/static/Nodes.png)

Recommended Setup
-----------------

Install MVAPICH Benchmark on your local system using the following tarball file:
```
  wget http://mvapich.cse.ohio-state.edu/download/mvapich/osu-micro-benchmarks-4.4.1.tar.gz

  gunzip xvf osu-micro-benchmarks-4.4.1.tar.gz

  tar xvf osu-micro-benchmarks-4.4.1.tar

  cd osu-micro-benchmarks-4.4.1

  ./configure

  make
```

Running Tests
-------------

For running a sample OMB Benchmark Latency Test between nodes comet-10-01 and comet-10-02, 
use the sample Slurm batch script:

```
#!/bin/bash

#SBATCH -o results.out
#SBATCH -e results.err
#SBATCH --nodes 2
#SBATCH --ntasks-per-node 1
#SBATCH -w comet-10-01, comet-10-02 
#SBATCH -t 01:00:00
#SBATCH --mail-type ALL
#SBATCH --mail-user <User Email>
#SBATCH -A use300

#We dont have a root binary for latency and hence using our own
export BINARY = /<path-to-installation>/mpi/pt2pt/osu_latency

#Activate Latency file from OMB Benchmark and ibrun for parallel processing
ibrun -v $BINARY 
```

The entire process of performing OMB Benchmark Latency tests on CPU nodes at L1 switch level is 
automated by the Latency.py script. 
