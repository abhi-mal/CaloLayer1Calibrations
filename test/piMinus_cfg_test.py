import os
import FWCore.ParameterSet.Config as cms
import EventFilter.L1TXRawToDigi.util as util

## Define the process
from Configuration.StandardSequences.Eras import eras
# Get era from https://github.com/cms-sw/cmssw/blob/master/Configuration/StandardSequences/python/Eras.py
process = cms.Process("HFCALIB",eras.Run2_2018)

## Load all kinds of stuff
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi') # New
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff') # New
process.load('SimGeneral.MixingModule.mixNoPU_cfi') # New
process.load('Configuration.StandardSequences.MagneticField_cff')
# Alternative if needed:
# process.load('Configuration.StandardSequences.MagneticField_AutoFromDBCurrent_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_condDBv2_cff")
process.load('Configuration.Geometry.GeometryRecoDB_cff')
# Alternatives if needed:
# process.load("Configuration.Geometry.GeometryExtended2017Reco_cff")
# process.load("Configuration.Geometry.GeometryExtended2017Plan1Reco_cff")

process.source = cms.Source("PoolSource",
        fileNames = cms.untracked.vstring(
'/store/mc/RunIISpring18DR/SinglePhoton_FlatPt-0to200_13TeV_FlatRandomPtGun/GEN-SIM-RAW/NZSNoPU_100X_upgrade2018_realistic_v10-v1/100000/04441221-CE21-E811-AF39-A4BF01125810.root'
        )
)
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = 100

## GlobalTag
from Configuration.AlCa.GlobalTag import GlobalTag
# Get updated tag from https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideFrontierConditions
process.GlobalTag = GlobalTag(process.GlobalTag,'100X_upgrade2018_realistic_v11','')
# process.GlobalTag = GlobalTag(process.GlobalTag,'92X_upgrade2017_TSG_For90XSamples_V1','')
# Get updated tag from https://twiki.cern.ch/twiki/bin/view/CMS/HcalLUTCorrsTags2009
process.GlobalTag.toGet = cms.VPSet(
  cms.PSet(record = cms.string("HcalLUTCorrsRcd"),
           tag = cms.string("HcalLUTCorrs_2018_v3.0_mc"),
           # tag = cms.string("HcalLUTCorrs_2017plan1_v2.0_mc"),
           connect = cms.string("frontier://FrontierProd/CMS_CONDITIONS")
          )
)

## To get the CaloTPGTranscoder, which decodes the HCAL compression LUT
process.load("SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff")
# From an email by Aleko: "For simulation you want LUTGenerationMode=True"
process.HcalTPGCoderULUT.LUTGenerationMode = cms.bool(True)

from CondCore.DBCommon.CondDBSetup_cfi import *
process.es_pool = cms.ESSource("PoolDBESSource",
     CondDBSetup,
     timetype = cms.string('runnumber'),
     toGet = cms.VPSet(
         cms.PSet(record = cms.string("HcalLutMetadataRcd"),
             # Get updated tag from https://twiki.cern.ch/twiki/bin/view/CMS/HcalLutMetadataTags2011
             tag = cms.string("HcalLutMetadata_2018_v6.0_mc")
             # tag = cms.string("HcalLutMetadata_2018_v4.0_mc")
             ),
         cms.PSet(record = cms.string("HcalElectronicsMapRcd"),
             # Get updated tag from https://twiki.cern.ch/twiki/bin/view/CMS/HcalElectronicsMapTags2009
             tag = cms.string("HcalElectronicsMap_2018_v3.0_mc")
             # tag = cms.string("HcalElectronicsMap_2017plan1_v3.0_mc")
             )
         ),
     connect = cms.string('frontier://FrontierProd/CMS_CONDITIONS'),
     authenticationMethod = cms.untracked.uint32(0)
     )
process.es_prefer_es_pool = cms.ESPrefer( "PoolDBESSource", "es_pool" )

process.TFileService = cms.Service("TFileService",
        closeFileFast = cms.untracked.bool(True),
        fileName = cms.string('analyzePion.root')
)

# process.simHcalTriggerPrimitiveDigis.inputLabel = cms.VInputTag(cms.InputTag('simHcalUnsuppressedDigis'), cms.InputTag('simHcalUnsuppressedDigis'))
# process.simHcalTriggerPrimitiveDigis.inputUpgradeLabel = cms.VInputTag(cms.InputTag('simHcalUnsuppressedDigis:HBHEQIE11DigiCollection'), cms.InputTag('simHcalUnsuppressedDigis:HFQIE10DigiCollection'))
process.tree = cms.EDAnalyzer("PionCalibrations",
        triggerPrimitives = cms.InputTag("simHcalTriggerPrimitiveDigis","","HFCALIB"),
        eTriggerPrimitives = cms.InputTag("ecalDigis:EcalTriggerPrimitives"),
        genSrc = cms.InputTag("genParticles"),
        doClosure = cms.untracked.bool(False)
)

process.p = cms.Path(process.hcalDigis * process.ecalDigis * process.simHcalTriggerPrimitiveDigis *process.tree)
