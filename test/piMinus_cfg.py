import os
import FWCore.ParameterSet.Config as cms
import EventFilter.L1TXRawToDigi.util as util

## Define the process
from Configuration.StandardSequences.Eras import eras
process = cms.Process("HFCALIB",eras.Run2_2017)

## Load all kinds of stuff
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi') # New
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff') # New
process.load('SimGeneral.MixingModule.mixNoPU_cfi') # New
# process.load('Configuration.StandardSequences.SimL1EmulatorRepack_FullMC_cff') # New; results in error whereby 0 digis are in collections
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
'/store/mc/PhaseISpring17DR/SinglePion_PT0to200/GEN-SIM-RAW/NoPUNZS_90X_upgrade2017_realistic_v20_ext1-v1/100000/00C7D4EA-7B37-E711-BCCB-0CC47A0AD6F8.root'
        )
)
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.MessageLogger.cerr.FwkReport.reportEvery = 100

## GlobalTag
from Configuration.AlCa.GlobalTag import GlobalTag
# Get updated tag from https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideFrontierConditions
process.GlobalTag = GlobalTag(process.GlobalTag,'90X_upgrade2017_realistic_v20','')
# Get updated tag from https://twiki.cern.ch/twiki/bin/view/CMS/HcalLUTCorrsTags2009
process.GlobalTag.toGet = cms.VPSet(
  cms.PSet(record = cms.string("HcalLUTCorrsRcd"),
           tag = cms.string("HcalLUTCorrs_2017plan1_v2.0_mc"),
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
             tag = cms.string("HcalLutMetadata_2017plan1_v3.0_mc")
             ),
         cms.PSet(record = cms.string("HcalElectronicsMapRcd"),
             # Get updated tag from https://twiki.cern.ch/twiki/bin/view/CMS/HcalElectronicsMapTags2009
             tag = cms.string("HcalElectronicsMap_2017plan1_v3.0_mc")
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

process.tree = cms.EDAnalyzer("PionCalibrations",
        triggerPrimitives = cms.InputTag("simHcalTriggerPrimitiveDigis","","HFCALIB"),
        eTriggerPrimitives = cms.InputTag("ecalDigis:EcalTriggerPrimitives"),
        genSrc = cms.InputTag("genParticles"),
        doClosure = cms.untracked.bool(False)
)

process.p = cms.Path(process.hcalDigis * process.ecalDigis * process.simHcalTriggerPrimitiveDigis *process.tree)
