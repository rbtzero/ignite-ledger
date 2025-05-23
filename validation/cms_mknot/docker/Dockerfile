# CMS open-data container with the M-knot skim scripts baked in
FROM cmsopendata/cmssw_7_6_7-slc6_amd64_gcc493:latest

# copy the analysis scripts into the container work area
WORKDIR /work
COPY scripts/mknot_skim.py /work/
COPY scripts/mknot_hist.py /work/

# default entry prints help
CMD ["/bin/bash","-c","echo 'Run ./run_mknot.sh on the host; it will launch this container with the right mounts.'"] 