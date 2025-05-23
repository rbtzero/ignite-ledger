#!/usr/bin/env python
"""
mknot_skim.py  – skim CMS open-data JetHT AOD to a light mono-jet tree

Run inside a CMSSW_5_3_32 environment:

  cmsRun mknot_skim.py inputFiles=file:JetHT.root maxEvents=100000

Outputs skim.root with branches (jet_pt,jet_px,jet_py,jet_pz, pfMet, pfMetPx, pfMetPy).
"""
import FWCore.ParameterSet.Config as cms, sys

process = cms.Process("SKIM")
process.load("FWCore.MessageService.MessageLogger_cfi")

maxEvents = int(getattr(sys, "maxEvents", 100000))
inputFiles = cms.untracked.vstring(sys.argv[2:]) if len(sys.argv)>2 else cms.untracked.vstring("file:JetHT.root")

process.maxEvents = cms.untracked.PSet(input = cms.untracked.int32(maxEvents))
process.source = cms.Source("PoolSource", fileNames = inputFiles)

process.load("PhysicsTools.Heppy.simpleJetSkim_cfi")
process.simpleJetSkim.jetPtMin   = 200.0
process.simpleJetSkim.minJets    = 1
process.simpleJetSkim.vetoLeptons= True

process.TFileService = cms.Service("TFileService", fileName = cms.string("skim.root"))
process.p = cms.Path(process.simpleJetSkim) 