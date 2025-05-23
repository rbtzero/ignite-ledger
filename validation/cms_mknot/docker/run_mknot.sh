#!/usr/bin/env bash
# run_mknot.sh – one-shot driver that pulls a small subset of CMS JetHT 2015 AOD
# via XRootD (no local download), runs the skim & histogram in the CMSSW_7_6_7
# container, and copies out skim.root + mrecoil_edge.png.
#
# Usage: ./run_mknot.sh  [--nevents 100000]
# Requires Docker (or alias to podman).

set -euo pipefail
NEVT=${1:-100000}
OUTDIR=$(pwd)/validation/cms_mknot
mkdir -p "$OUTDIR/data" "$OUTDIR/plots"

IMG=cms_mknot:latest
# build the container (idempotent)
DOCKER_BUILDKIT=1 docker build -t $IMG -f validation/cms_mknot/docker/Dockerfile .

# small file list: first 5 JetHT 2015D AOD files (≈15 GB, streamed)
read -r -d '' FILELIST <<'EOF'
root://xrootd-cms.infn.it//store/data/Run2015D/JetHT/AOD/16Dec2015-v1/50000/0013C986-899C-E611-AAA0-0CC47A4D7600.root
root://xrootd-cms.infn.it//store/data/Run2015D/JetHT/AOD/16Dec2015-v1/50000/00373137-7A9C-E611-B6AE-0CC47A78A456.root
root://xrootd-cms.infn.it//store/data/Run2015D/JetHT/AOD/16Dec2015-v1/50000/0054A0A3-649C-E611-A55B-0CC47A4D7600.root
root://xrootd-cms.infn.it//store/data/Run2015D/JetHT/AOD/16Dec2015-v1/50000/02FBB650-899C-E611-A65A-0CC47A4D761E.root
root://xrootd-cms.infn.it//store/data/Run2015D/JetHT/AOD/16Dec2015-v1/50000/04771A64-7A9C-E611-A6BA-0CC47A78A4B2.root
EOF

# run the skim inside the container
cat > /tmp/mknot_cfg.py <<PY
import FWCore.ParameterSet.Config as cms
process = cms.Process('SKIM')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.maxEvents = cms.untracked.PSet(input=cms.untracked.int32($NEVT))
process.source = cms.Source('PoolSource', fileNames = cms.untracked.vstring(${FILELIST//$'\n'/,}))
process.load('PhysicsTools.Heppy.simpleJetSkim_cfi')
process.simpleJetSkim.jetPtMin = 200.0
process.simpleJetSkim.minJets  = 1
process.simpleJetSkim.vetoLeptons = True
process.TFileService = cms.Service('TFileService', fileName=cms.string('skim.root'))
process.p = cms.Path(process.simpleJetSkim)
PY

docker run --rm -v /tmp/mknot_cfg.py:/work/mknot_cfg.py -v "$OUTDIR":/out $IMG \
    bash -c "cmsRun mknot_cfg.py && python mknot_hist.py skim.root /out/plots/mrecoil_edge.png && mv skim.root /out/data/"

echo "Outputs written to validation/cms_mknot/{data,plots}" 