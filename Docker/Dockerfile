#This docker file will create a docker container for the CommonKmers method
#docker run --rm -t -i cami/profiling

FROM cami/profiling

MAINTAINER David Koslicki version: 0.1

#Install required packages
RUN apt-get -y update && \
 apt-get install -y wget && \
 apt-get install -y g++ && \
 apt-get install -y build-essential && \
 apt-get install -y git && \
 apt-get install -y gzip
 
#Install python, biopython
RUN apt-get -y update && \ 
 apt-get install -y python && \
 apt-get install -y python-numpy python-scipy python-dev python-pip && \
 easy_install -f http://biopython.org/DIST/ biopython
 
#Install Jellyfish V1
RUN wget http://www.cbcb.umd.edu/software/jellyfish/jellyfish-1.1.11.tar.gz && \
 tar -xzf jellyfish-1.1.11.tar.gz && \
 rm jellyfish-1.1.11.tar.gz && \
 cd jellyfish-1.1.11 && \
 ./configure && \
 make && \
 make install

#Install Kraken
RUN wget https://github.com/DerrickWood/kraken/archive/v0.10.5-beta.tar.gz && \
 tar -xzf v0.10.5-beta.tar.gz && \
 rm v0.10.5-beta.tar.gz && \
 cp jellyfish-1.1.11/bin/jellyfish kraken-0.10.5-beta && \
 cd kraken-0.10.5-beta && \
 ./install_kraken.sh . || echo "ok"

#Get wrapper/format conversion code
RUN git clone https://github.com/dkoslicki/CAMIKraken.git && \
 cp /CAMIKraken/Docker/default /dckr/etc/tasks.d/default && \
 cp /CAMIKraken/Docker/train /dckr/etc/tasks.d/train && \
 cp /CAMIKraken/src/KrakenToCAMI.py /usr/local/sbin/ && \
 cp /CAMIKraken/src/generate_taxonomy_taxid.py /usr/local/sbin/

