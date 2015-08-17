# CAMIKraken #

This small repository contains a Dockerfile that installs Kraken, as well as shell and python scripts to convert the output to comply with the [CAMI](www.cami-challenge.org) competition [output format](https://github.com/CAMI-challenge/contest_information/blob/master/file_formats/CAMI_TP_specification.mkd).

The Dockerfile complies with the [Bioboxes profiling format 0.9](https://github.com/bioboxes/rfc/tree/master/data-format).

## Obtaining the docker ##
You can either pull from Dockerhub:
```bash
docker pull dkoslicki/camikraken
```
Or pull this repository and compile yourself:
```bash
git clone https://gihub.com/dkoslicki/CAMIKraken.git
cd CAMIKraken/Docker
docker build -t username/imagename .
```

## Training ##
There is a ``training`` task in this docker that will train Kraken using the default training parameters. The taxonomy is specified by providing a file called ``taxonomy.tar.gz`` that contains the files: ``names.dmp, nodes.dmp`` and ``gi_taxid_nucl.dmp``. The fasta file(s) containing the training organisms will need to be provided to the docker, with a file (called ``sample.fna.list``) that lists which files to train on.

Note that training on the NCBI bacterial genomes can take approximately 4 hours (using 48 cores and ~180GB of RAM).

An example command for training using the docker is:
```bash
docker run --rm -e "DCKR_THREADS=48" -v /path/to/output:/dckr/mnt/output:rw -v /path/to/TrainingData:/dckr/mnt/input:ro -t dkoslicki/camikraken train
```
Where the folder ``/path/to/TrainingData`` has the files ``taxonomy.tar.gz``, ``sample.fna.list``, and the files listed in ``sample.fna.list``.

## Testing ##
After training is complete, the default task will classify an input metagenome. An example command would be:
```bash
docker run --rm -e "DCKR_THREADS=48" -v /path/to/Database:/dckr/mnt/camiref/Database:ro -v /path/to/output:/dckr/mnt/output:rw -v /path/to/input:/dckr/mnt/input:ro -t dkoslicki/camikraken default
```
Where the folder ``/path/to/Database`` was produced by the ``train`` task. The folder ``/path/to/input`` must have a file called ``sample.fq.gz.list`` that lists the files present in ``/path/to/input`` that you wish to have classified.
