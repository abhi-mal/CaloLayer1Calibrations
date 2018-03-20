from subprocess import Popen
from sys import argv, exit, stdout, stderr

import ROOT
import os
import math

sf_errors = []

try:
    #try to load the function
    ROOT.langaufun
except AttributeError:
    #try to compile the function
    pkgdir = os.path.dirname(__file__)
    if len(pkgdir) == 0:
        pkgdir = "."
    path = os.sep.join((pkgdir, "langaus.C"))
    path = os.path.abspath(path)
    if not os.path.exists(path):
        raise Exception("ERROR: file does not exist ", path)
    ROOT.gROOT.ProcessLine(".L " + path +"+")

ROOT.gROOT.SetStyle("Plain")
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

######## File #########
if len(argv) != 2:
   print 'Usage: python plotPiMinus_majorUpdate.py output_from_computeHCALcalibs_MC_364_majorUpdate.root'
   exit()

infile = argv[1]
ntuple_file = ROOT.TFile(infile)

######## LABEL & SAVE WHERE #########
# saveWhere='/nfs_scratch/jjbuchanan/calibrations_Jan2017/MonteCarlo/CMSSW_9_2_8/src/L1Trigger/CaloLayer1Calibrations/bin/SinglePion/'
saveWhere = ''
text_file = open("hcalcalibs_MC_p_mode_noLowerLimit.txt","w")
text_file = open("hcalcalibs_MC_HBHE.txt","w")
text_file_HF = open("hcalcalibs_MC_HF.txt","w")

def GetMedian(histo):
  integral = histo.GetIntegral()
  if integral==0:
    return 0
  else:
    median_i = 0
    for j in range(0,histo.GetNbinsX()):
      if integral[j]<0.5:
        median_i = j
    if integral[median_i] == 0:
      return -1.0
    else:
      median_x = histo.GetBinCenter(median_i) + (histo.GetBinCenter(median_i+1)-histo.GetBinCenter(median_i))*(0.5-integral[median_i])/(integral[median_i+1]-integral[median_i])
      return median_x

# To grab
# histos_resolution_3x3 = []
histos_resolution_5x5 = []
# histos_genpt_3x3 = []
histos_genpt_5x5 = []
# histos_summed33e_3x3 = []
histos_summed33e_5x5 = []
# histos_summed55e_3x3 = []
histos_summed55e_5x5 = []
# histos_summed33h_3x3 = []
histos_summed33h_5x5 = []
# histos_summed55h_3x3 = []
histos_summed55h_5x5 = []
# histos_sumCorr33e_3x3 = []
histos_sumCorr33e_5x5 = []
# histos_sumCorr55e_3x3 = []
histos_sumCorr55e_5x5 = []
# histos_sumCorr33h_3x3 = []
histos_sumCorr33h_5x5 = []
# histos_sumCorr55h_3x3 = []
histos_sumCorr55h_5x5 = []
# histos_ECALisolation_eta_folded_3x3 = []
histos_ECALisolation_eta_folded_5x5 = []
# histos_HCALisolation_eta_folded_3x3 = []
histos_HCALisolation_eta_folded_5x5 = []
# histos_corrECALisolation_eta_folded_3x3 = []
histos_corrECALisolation_eta_folded_5x5 = []
# histos_corrHCALisolation_eta_folded_3x3 = []
histos_corrHCALisolation_eta_folded_5x5 = []
# histos_scaleFactor_phi_3x3 = []
histos_scaleFactor_phi_5x5 = []
# histos_scaleFactor_phi_barrel_3x3 = []
histos_scaleFactor_phi_barrel_5x5 = []
# histos_scaleFactor_phi_endcap_3x3 = []
# histos_scaleFactor_phi_endcap_pos_3x3 = []
# histos_scaleFactor_phi_endcap_neg_3x3 = []
histos_scaleFactor_phi_endcap_5x5 = []
histos_scaleFactor_phi_endcap_pos_5x5 = []
histos_scaleFactor_phi_endcap_neg_5x5 = []
# histos_scaleFactor_phi_HF_3x3 = []
# histos_scaleFactor_phi_HF_pos_3x3 = []
# histos_scaleFactor_phi_HF_neg_3x3 = []
histos_scaleFactor_phi_HF_5x5 = []
histos_scaleFactor_phi_HF_pos_5x5 = []
histos_scaleFactor_phi_HF_neg_5x5 = []
# histos_scaleFactor_eta_3x3 = []
histos_scaleFactor_eta_5x5 = []
# histos_scaleFactor_eta_folded_3x3 = []
histos_scaleFactor_eta_folded_5x5 = []
# To compute
# histos_HCALisolation_ETbin_foldedEta_3x3 = []
histos_HCALisolation_ETbin_foldedEta_5x5 = []
# histos_scaleFactor_ETbin_phi_3x3 = []
histos_scaleFactor_ETbin_phi_5x5 = []
# histos_scaleFactor_ETbin_phi_barrel_3x3 = []
histos_scaleFactor_ETbin_phi_barrel_5x5 = []
# histos_scaleFactor_ETbin_phi_endcap_3x3 = []
# histos_scaleFactor_ETbin_phi_endcap_pos_3x3 = []
# histos_scaleFactor_ETbin_phi_endcap_neg_3x3 = []
histos_scaleFactor_ETbin_phi_endcap_5x5 = []
histos_scaleFactor_ETbin_phi_endcap_pos_5x5 = []
histos_scaleFactor_ETbin_phi_endcap_neg_5x5 = []
# histos_scaleFactor_ETbin_phi_HF_3x3 = []
# histos_scaleFactor_ETbin_phi_HF_pos_3x3 = []
# histos_scaleFactor_ETbin_phi_HF_neg_3x3 = []
histos_scaleFactor_ETbin_phi_HF_5x5 = []
histos_scaleFactor_ETbin_phi_HF_pos_5x5 = []
histos_scaleFactor_ETbin_phi_HF_neg_5x5 = []
# histos_scaleFactor_ETbin_eta_3x3 = []
histos_scaleFactor_ETbin_eta_5x5 = []
# histos_scaleFactor_ETbin_foldedEta_3x3 = []
histos_scaleFactor_ETbin_foldedEta_5x5 = []

for i in range(0,14):
  # To grab
  # hname_resolution_3x3 = "histos_resolution_3x3_ETbin%d" % i # Each histogram must have a unique name
  # histos_resolution_3x3.append(ntuple_file.Get(hname_resolution_3x3))
  hname_resolution_5x5 = "histos_resolution_5x5_ETbin%d" % i # Each histogram must have a unique name
  histos_resolution_5x5.append(ntuple_file.Get(hname_resolution_5x5))
  # hname_genpt_3x3 = "histos_genpt_3x3_ETbin%d" % i
  # histos_genpt_3x3.append(ntuple_file.Get(hname_genpt_3x3))
  hname_genpt_5x5 = "histos_genpt_5x5_ETbin%d" % i
  histos_genpt_5x5.append(ntuple_file.Get(hname_genpt_5x5))
  # hname_summed33e_3x3 = "histos_summed33e_3x3_ETbin%d" % i
  # histos_summed33e_3x3.append(ntuple_file.Get(hname_summed33e_3x3))
  hname_summed33e_5x5 = "histos_summed33e_5x5_ETbin%d" % i
  histos_summed33e_5x5.append(ntuple_file.Get(hname_summed33e_5x5))
  # hname_summed55e_3x3 = "histos_summed55e_3x3_ETbin%d" % i
  # histos_summed55e_3x3.append(ntuple_file.Get(hname_summed55e_3x3))
  hname_summed55e_5x5 = "histos_summed55e_5x5_ETbin%d" % i
  histos_summed55e_5x5.append(ntuple_file.Get(hname_summed55e_5x5))
  # hname_summed33h_3x3 = "histos_summed33h_3x3_ETbin%d" % i
  # histos_summed33h_3x3.append(ntuple_file.Get(hname_summed33h_3x3))
  hname_summed33h_5x5 = "histos_summed33h_5x5_ETbin%d" % i
  histos_summed33h_5x5.append(ntuple_file.Get(hname_summed33h_5x5))
  # hname_summed55h_3x3 = "histos_summed55h_3x3_ETbin%d" % i
  # histos_summed55h_3x3.append(ntuple_file.Get(hname_summed55h_3x3))
  hname_summed55h_5x5 = "histos_summed55h_5x5_ETbin%d" % i
  histos_summed55h_5x5.append(ntuple_file.Get(hname_summed55h_5x5))
  # hname_sumCorr33e_3x3 = "histos_sumCorr33e_3x3_ETbin%d" % i
  # histos_sumCorr33e_3x3.append(ntuple_file.Get(hname_sumCorr33e_3x3))
  hname_sumCorr33e_5x5 = "histos_sumCorr33e_5x5_ETbin%d" % i
  histos_sumCorr33e_5x5.append(ntuple_file.Get(hname_sumCorr33e_5x5))
  # hname_sumCorr55e_3x3 = "histos_sumCorr55e_3x3_ETbin%d" % i
  # histos_sumCorr55e_3x3.append(ntuple_file.Get(hname_sumCorr55e_3x3))
  hname_sumCorr55e_5x5 = "histos_sumCorr55e_5x5_ETbin%d" % i
  histos_sumCorr55e_5x5.append(ntuple_file.Get(hname_sumCorr55e_5x5))
  # hname_sumCorr33h_3x3 = "histos_sumCorr33h_3x3_ETbin%d" % i
  # histos_sumCorr33h_3x3.append(ntuple_file.Get(hname_sumCorr33h_3x3))
  hname_sumCorr33h_5x5 = "histos_sumCorr33h_5x5_ETbin%d" % i
  histos_sumCorr33h_5x5.append(ntuple_file.Get(hname_sumCorr33h_5x5))
  # hname_sumCorr55h_3x3 = "histos_sumCorr55h_3x3_ETbin%d" % i
  # histos_sumCorr55h_3x3.append(ntuple_file.Get(hname_sumCorr55h_3x3))
  hname_sumCorr55h_5x5 = "histos_sumCorr55h_5x5_ETbin%d" % i
  histos_sumCorr55h_5x5.append(ntuple_file.Get(hname_sumCorr55h_5x5))
  # To compute
  # hname_HCALisolation_ETbin_foldedEta_3x3 = "histos_HCALisolation_foldedEta_3x3_ETbin%d" % i # Each histogram must have a unique name
  # histos_HCALisolation_ETbin_foldedEta_3x3.append(ROOT.TH1F(hname_HCALisolation_ETbin_foldedEta_3x3,"",41,0,41))
  hname_HCALisolation_ETbin_foldedEta_5x5 = "histos_HCALisolation_foldedEta_5x5_ETbin%d" % i # Each histogram must have a unique name
  histos_HCALisolation_ETbin_foldedEta_5x5.append(ROOT.TH1F(hname_HCALisolation_ETbin_foldedEta_5x5,"",41,0,41))
  # histos_HCALisolation_eta_folded_3x3.append([])
  histos_HCALisolation_eta_folded_5x5.append([])
  # hname_scaleFactor_ETbin_phi_3x3 = "histos_scaleFactor_phi_3x3_ETbin%d" % i # Each histogram must have a unique name
  # histos_scaleFactor_ETbin_phi_3x3.append(ROOT.TH1F(hname_scaleFactor_ETbin_phi_3x3,"",72,0,72))
  hname_scaleFactor_ETbin_phi_5x5 = "histos_scaleFactor_phi_5x5_ETbin%d" % i # Each histogram must have a unique name
  histos_scaleFactor_ETbin_phi_5x5.append(ROOT.TH1F(hname_scaleFactor_ETbin_phi_5x5,"",72,0,72))
  # hname_scaleFactor_ETbin_phi_barrel_3x3 = "histos_scaleFactor_phi_barrel_3x3_ETbin%d" % i # Each histogram must have a unique name
  # histos_scaleFactor_ETbin_phi_barrel_3x3.append(ROOT.TH1F(hname_scaleFactor_ETbin_phi_barrel_3x3,"",72,0,72))
  hname_scaleFactor_ETbin_phi_barrel_5x5 = "histos_scaleFactor_phi_barrel_5x5_ETbin%d" % i # Each histogram must have a unique name
  histos_scaleFactor_ETbin_phi_barrel_5x5.append(ROOT.TH1F(hname_scaleFactor_ETbin_phi_barrel_5x5,"",72,0,72))
  # hname_scaleFactor_ETbin_phi_endcap_3x3 = "histos_scaleFactor_phi_endcap_3x3_ETbin%d" % i # Each histogram must have a unique name
  # histos_scaleFactor_ETbin_phi_endcap_3x3.append(ROOT.TH1F(hname_scaleFactor_ETbin_phi_endcap_3x3,"",72,0,72))
  # hname_scaleFactor_ETbin_phi_endcap_pos_3x3 = "histos_scaleFactor_phi_endcap_pos_3x3_ETbin%d" % i # Each histogram must have a unique name
  # histos_scaleFactor_ETbin_phi_endcap_pos_3x3.append(ROOT.TH1F(hname_scaleFactor_ETbin_phi_endcap_pos_3x3,"",72,0,72))
  # hname_scaleFactor_ETbin_phi_endcap_neg_3x3 = "histos_scaleFactor_phi_endcap_neg_3x3_ETbin%d" % i # Each histogram must have a unique name
  # histos_scaleFactor_ETbin_phi_endcap_neg_3x3.append(ROOT.TH1F(hname_scaleFactor_ETbin_phi_endcap_neg_3x3,"",72,0,72))
  hname_scaleFactor_ETbin_phi_endcap_5x5 = "histos_scaleFactor_phi_endcap_5x5_ETbin%d" % i # Each histogram must have a unique name
  histos_scaleFactor_ETbin_phi_endcap_5x5.append(ROOT.TH1F(hname_scaleFactor_ETbin_phi_endcap_5x5,"",72,0,72))
  hname_scaleFactor_ETbin_phi_endcap_pos_5x5 = "histos_scaleFactor_phi_endcap_pos_5x5_ETbin%d" % i # Each histogram must have a unique name
  histos_scaleFactor_ETbin_phi_endcap_pos_5x5.append(ROOT.TH1F(hname_scaleFactor_ETbin_phi_endcap_pos_5x5,"",72,0,72))
  hname_scaleFactor_ETbin_phi_endcap_neg_5x5 = "histos_scaleFactor_phi_endcap_neg_5x5_ETbin%d" % i # Each histogram must have a unique name
  histos_scaleFactor_ETbin_phi_endcap_neg_5x5.append(ROOT.TH1F(hname_scaleFactor_ETbin_phi_endcap_neg_5x5,"",72,0,72))
  # hname_scaleFactor_ETbin_phi_HF_3x3 = "histos_scaleFactor_phi_HF_3x3_ETbin%d" % i # Each histogram must have a unique name
  # histos_scaleFactor_ETbin_phi_HF_3x3.append(ROOT.TH1F(hname_scaleFactor_ETbin_phi_HF_3x3,"",72,0,72))
  # hname_scaleFactor_ETbin_phi_HF_pos_3x3 = "histos_scaleFactor_phi_HF_pos_3x3_ETbin%d" % i # Each histogram must have a unique name
  # histos_scaleFactor_ETbin_phi_HF_pos_3x3.append(ROOT.TH1F(hname_scaleFactor_ETbin_phi_HF_pos_3x3,"",72,0,72))
  # hname_scaleFactor_ETbin_phi_HF_neg_3x3 = "histos_scaleFactor_phi_HF_neg_3x3_ETbin%d" % i # Each histogram must have a unique name
  # histos_scaleFactor_ETbin_phi_HF_neg_3x3.append(ROOT.TH1F(hname_scaleFactor_ETbin_phi_HF_neg_3x3,"",72,0,72))
  hname_scaleFactor_ETbin_phi_HF_5x5 = "histos_scaleFactor_phi_HF_5x5_ETbin%d" % i # Each histogram must have a unique name
  histos_scaleFactor_ETbin_phi_HF_5x5.append(ROOT.TH1F(hname_scaleFactor_ETbin_phi_HF_5x5,"",72,0,72))
  hname_scaleFactor_ETbin_phi_HF_pos_5x5 = "histos_scaleFactor_phi_HF_pos_5x5_ETbin%d" % i # Each histogram must have a unique name
  histos_scaleFactor_ETbin_phi_HF_pos_5x5.append(ROOT.TH1F(hname_scaleFactor_ETbin_phi_HF_pos_5x5,"",72,0,72))
  hname_scaleFactor_ETbin_phi_HF_neg_5x5 = "histos_scaleFactor_phi_HF_neg_5x5_ETbin%d" % i # Each histogram must have a unique name
  histos_scaleFactor_ETbin_phi_HF_neg_5x5.append(ROOT.TH1F(hname_scaleFactor_ETbin_phi_HF_neg_5x5,"",72,0,72))
  # hname_scaleFactor_ETbin_eta_3x3 = "histos_scaleFactor_eta_3x3_ETbin%d" % i # Each histogram must have a unique name
  # histos_scaleFactor_ETbin_eta_3x3.append(ROOT.TH1F(hname_scaleFactor_ETbin_eta_3x3,"",82,0,82))
  hname_scaleFactor_ETbin_eta_5x5 = "histos_scaleFactor_eta_5x5_ETbin%d" % i # Each histogram must have a unique name
  histos_scaleFactor_ETbin_eta_5x5.append(ROOT.TH1F(hname_scaleFactor_ETbin_eta_5x5,"",82,0,82))
  # hname_scaleFactor_ETbin_foldedEta_3x3 = "histos_scaleFactor_foldedEta_3x3_ETbin%d" % i # Each histogram must have a unique name
  # histos_scaleFactor_ETbin_foldedEta_3x3.append(ROOT.TH1F(hname_scaleFactor_ETbin_foldedEta_3x3,"",41,0,41))
  hname_scaleFactor_ETbin_foldedEta_5x5 = "histos_scaleFactor_foldedEta_5x5_ETbin%d" % i # Each histogram must have a unique name
  histos_scaleFactor_ETbin_foldedEta_5x5.append(ROOT.TH1F(hname_scaleFactor_ETbin_foldedEta_5x5,"",41,0,41))
  # histos_scaleFactor_phi_3x3.append([])
  histos_scaleFactor_phi_5x5.append([])
  # histos_scaleFactor_phi_barrel_3x3.append([])
  histos_scaleFactor_phi_barrel_5x5.append([])
  # histos_scaleFactor_phi_endcap_3x3.append([])
  # histos_scaleFactor_phi_endcap_pos_3x3.append([])
  # histos_scaleFactor_phi_endcap_neg_3x3.append([])
  histos_scaleFactor_phi_endcap_5x5.append([])
  histos_scaleFactor_phi_endcap_pos_5x5.append([])
  histos_scaleFactor_phi_endcap_neg_5x5.append([])
  # histos_scaleFactor_phi_HF_3x3.append([])
  # histos_scaleFactor_phi_HF_pos_3x3.append([])
  # histos_scaleFactor_phi_HF_neg_3x3.append([])
  histos_scaleFactor_phi_HF_5x5.append([])
  histos_scaleFactor_phi_HF_pos_5x5.append([])
  histos_scaleFactor_phi_HF_neg_5x5.append([])
  # histos_scaleFactor_eta_3x3.append([])
  histos_scaleFactor_eta_5x5.append([])
  # histos_scaleFactor_eta_folded_3x3.append([])
  histos_scaleFactor_eta_folded_5x5.append([])
  for j in range(0,72):
    # hname_scaleFactor_phi_3x3 = "histos_scaleFactor_phi_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    # histos_scaleFactor_phi_3x3[i].append(ntuple_file.Get(hname_scaleFactor_phi_3x3))
    hname_scaleFactor_phi_5x5 = "histos_scaleFactor_phi_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_phi_5x5[i].append(ntuple_file.Get(hname_scaleFactor_phi_5x5))
    # hname_scaleFactor_phi_barrel_3x3 = "histos_scaleFactor_phi_barrel_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    # histos_scaleFactor_phi_barrel_3x3[i].append(ntuple_file.Get(hname_scaleFactor_phi_barrel_3x3))
    hname_scaleFactor_phi_barrel_5x5 = "histos_scaleFactor_phi_barrel_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_phi_barrel_5x5[i].append(ntuple_file.Get(hname_scaleFactor_phi_barrel_5x5))
    # hname_scaleFactor_phi_endcap_3x3 = "histos_scaleFactor_phi_endcap_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    # histos_scaleFactor_phi_endcap_3x3[i].append(ntuple_file.Get(hname_scaleFactor_phi_endcap_3x3))
    # hname_scaleFactor_phi_endcap_pos_3x3 = "histos_scaleFactor_phi_endcap_pos_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    # histos_scaleFactor_phi_endcap_pos_3x3[i].append(ntuple_file.Get(hname_scaleFactor_phi_endcap_pos_3x3))
    # hname_scaleFactor_phi_endcap_neg_3x3 = "histos_scaleFactor_phi_endcap_neg_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    # histos_scaleFactor_phi_endcap_neg_3x3[i].append(ntuple_file.Get(hname_scaleFactor_phi_endcap_neg_3x3))
    hname_scaleFactor_phi_endcap_5x5 = "histos_scaleFactor_phi_endcap_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_phi_endcap_5x5[i].append(ntuple_file.Get(hname_scaleFactor_phi_endcap_5x5))
    hname_scaleFactor_phi_endcap_pos_5x5 = "histos_scaleFactor_phi_endcap_pos_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_phi_endcap_pos_5x5[i].append(ntuple_file.Get(hname_scaleFactor_phi_endcap_pos_5x5))
    hname_scaleFactor_phi_endcap_neg_5x5 = "histos_scaleFactor_phi_endcap_neg_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_phi_endcap_neg_5x5[i].append(ntuple_file.Get(hname_scaleFactor_phi_endcap_neg_5x5))
    # hname_scaleFactor_phi_HF_3x3 = "histos_scaleFactor_phi_HF_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    # histos_scaleFactor_phi_HF_3x3[i].append(ntuple_file.Get(hname_scaleFactor_phi_HF_3x3))
    # hname_scaleFactor_phi_HF_pos_3x3 = "histos_scaleFactor_phi_HF_pos_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    # histos_scaleFactor_phi_HF_pos_3x3[i].append(ntuple_file.Get(hname_scaleFactor_phi_HF_pos_3x3))
    # hname_scaleFactor_phi_HF_neg_3x3 = "histos_scaleFactor_phi_HF_neg_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    # histos_scaleFactor_phi_HF_neg_3x3[i].append(ntuple_file.Get(hname_scaleFactor_phi_HF_neg_3x3))
    hname_scaleFactor_phi_HF_5x5 = "histos_scaleFactor_phi_HF_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_phi_HF_5x5[i].append(ntuple_file.Get(hname_scaleFactor_phi_HF_5x5))
    hname_scaleFactor_phi_HF_pos_5x5 = "histos_scaleFactor_phi_HF_pos_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_phi_HF_pos_5x5[i].append(ntuple_file.Get(hname_scaleFactor_phi_HF_pos_5x5))
    hname_scaleFactor_phi_HF_neg_5x5 = "histos_scaleFactor_phi_HF_neg_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_phi_HF_neg_5x5[i].append(ntuple_file.Get(hname_scaleFactor_phi_HF_neg_5x5))
  for j in range(0,82):
    # hname_scaleFactor_eta_3x3 = "histos_scaleFactor_eta_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    # histos_scaleFactor_eta_3x3[i].append(ntuple_file.Get(hname_scaleFactor_eta_3x3))
    hname_scaleFactor_eta_5x5 = "histos_scaleFactor_eta_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_eta_5x5[i].append(ntuple_file.Get(hname_scaleFactor_eta_5x5))
  for j in range(0,41):
    # hname_HCALisolation_eta_folded_3x3 = "histos_HCALisolation_eta_folded_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    # histos_HCALisolation_eta_folded_3x3[i].append( ROOT.TH1F(hname_HCALisolation_eta_folded_3x3,"",2000,0,100) )
    hname_HCALisolation_eta_folded_5x5 = "histos_HCALisolation_eta_folded_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_HCALisolation_eta_folded_5x5[i].append( ROOT.TH1F(hname_HCALisolation_eta_folded_5x5,"",2000,0,100) )
    # hname_scaleFactor_eta_folded_3x3 = "histos_scaleFactor_eta_folded_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    # histos_scaleFactor_eta_folded_3x3[i].append(ntuple_file.Get(hname_scaleFactor_eta_folded_3x3))
    hname_scaleFactor_eta_folded_5x5 = "histos_scaleFactor_eta_folded_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_eta_folded_5x5[i].append(ntuple_file.Get(hname_scaleFactor_eta_folded_5x5))

canvas = ROOT.TCanvas("asdf", "adsf", 800, 800)
pad1 = ROOT.TPad("pad1","",0,0,1,1)
pad1.Draw()
pad1.cd()

last_written = [1.000000]*41

for ETbin in range(0,13):
    for phi in range(0,72):
        # Mean_scaleFactor_3x3 =histos_scaleFactor_phi_3x3[ETbin][phi].GetMean()
        # MeanError_scaleFactor_3x3 =histos_scaleFactor_phi_3x3[ETbin][phi].GetMeanError()
        Mean_scaleFactor_5x5 =histos_scaleFactor_phi_5x5[ETbin][phi].GetMean()
        MeanError_scaleFactor_5x5 =histos_scaleFactor_phi_5x5[ETbin][phi].GetMeanError()
        # histos_scaleFactor_ETbin_phi_3x3[ETbin].SetBinContent(phi+1,Mean_scaleFactor_3x3)
        # histos_scaleFactor_ETbin_phi_3x3[ETbin].SetBinError(phi+1,MeanError_scaleFactor_3x3)
        histos_scaleFactor_ETbin_phi_5x5[ETbin].SetBinContent(phi+1,Mean_scaleFactor_5x5)
        histos_scaleFactor_ETbin_phi_5x5[ETbin].SetBinError(phi+1,MeanError_scaleFactor_5x5)
        
        # Mean_scaleFactor_3x3 =histos_scaleFactor_phi_barrel_3x3[ETbin][phi].GetMean()
        # MeanError_scaleFactor_3x3 =histos_scaleFactor_phi_barrel_3x3[ETbin][phi].GetMeanError()
        # histos_scaleFactor_ETbin_phi_barrel_3x3[ETbin].SetBinContent(phi+1,Mean_scaleFactor_3x3)
        # histos_scaleFactor_ETbin_phi_barrel_3x3[ETbin].SetBinError(phi+1,MeanError_scaleFactor_3x3)
        ############################################################################################
        ### Mode ###
        # rms = histos_scaleFactor_phi_barrel_5x5[ETbin][phi].GetRMS()
        # if rms > 0.2:
        #   histos_scaleFactor_phi_barrel_5x5[ETbin][phi].Rebin(2)
        #   rms = histos_scaleFactor_phi_barrel_5x5[ETbin][phi].GetRMS()
        # tf1 = ROOT.TF1("landaugausfunction", ROOT.langaufun, 0, 5, 4)
        # peakpos = histos_scaleFactor_phi_barrel_5x5[ETbin][phi].GetXaxis().GetBinCenter(histos_scaleFactor_phi_barrel_5x5[ETbin][phi].GetMaximumBin())
        # startwidth = rms / 5.0
        # startmpv = peakpos
        # startnorm = histos_scaleFactor_phi_barrel_5x5[ETbin][phi].Integral()
        # startsigma = rms / 10.0
        # tf1.SetParNames("LandauWidth","LandauMPV","Normalisation","GaussianSigma")
        # tf1.SetParameters(startwidth, startmpv, startnorm, startsigma)
        # histos_scaleFactor_phi_barrel_5x5[ETbin][phi].Fit(tf1, "0L", "", 0.6, 3.0)
        # Mean_scaleFactor_5x5 = float(tf1.GetParameter(1))
        # MeanError_scaleFactor_5x5 = float(tf1.GetParError(1))
        # if math.isnan(Mean_scaleFactor_5x5) or math.isnan(MeanError_scaleFactor_5x5):
        #   Mean_scaleFactor_5x5 = -9999.9
        #   MeanError_scaleFactor_5x5 = 999.9
        # if tf1.GetParameter(0)/tf1.GetParameter(3) < 0.034 or MeanError_scaleFactor_5x5 > 0.03:
        #   tf1_alt = ROOT.TF1("gaus","[2]*TMath::Gaus(x,[0],[1])",0.0,3.0)
        #   # startmean = histos_scaleFactor_phi_barrel_5x5[ETbin][phi].GetMean()
        #   startmean = peakpos
        #   startsigma = histos_scaleFactor_phi_barrel_5x5[ETbin][phi].GetRMS()
        #   startnorm = histos_scaleFactor_phi_barrel_5x5[ETbin][phi].Integral(histos_scaleFactor_phi_barrel_5x5[ETbin][phi].GetXaxis().FindBin(0.6),histos_scaleFactor_phi_barrel_5x5[ETbin][phi].GetXaxis().FindBin(3.0))
        #   tf1_alt.SetParNames("GausMean","GausSigma","GausNorm")
        #   tf1_alt.SetParameters(startmean,startsigma,startnorm)
        #   histos_scaleFactor_phi_barrel_5x5[ETbin][phi].Fit(tf1_alt,"0L","",startmean-0.2,startmean+0.2)
        #   val = float(tf1_alt.GetParameter(0))
        #   err = float(tf1_alt.GetParError(0))
        #   if err < MeanError_scaleFactor_5x5 and not math.isnan(val) and not math.isnan(err):
        #     Mean_scaleFactor_5x5 = val
        #     MeanError_scaleFactor_5x5 = err
        #     tf1 = tf1_alt
        # if abs(MeanError_scaleFactor_5x5/Mean_scaleFactor_5x5) > 1.0:
        #   Mean_scaleFactor_5x5 = -9999.9
        #   MeanError_scaleFactor_5x5 = 999.9
        ############################################################################################
        ### Mean ###
        Mean_scaleFactor_5x5 =histos_scaleFactor_phi_barrel_5x5[ETbin][phi].GetMean()
        MeanError_scaleFactor_5x5 =histos_scaleFactor_phi_barrel_5x5[ETbin][phi].GetMeanError()
        ############################################################################################
        histos_scaleFactor_ETbin_phi_barrel_5x5[ETbin].SetBinContent(phi+1,Mean_scaleFactor_5x5)
        histos_scaleFactor_ETbin_phi_barrel_5x5[ETbin].SetBinError(phi+1,MeanError_scaleFactor_5x5)
        
        # Mean_scaleFactor_3x3 =histos_scaleFactor_phi_endcap_3x3[ETbin][phi].GetMean()
        # MeanError_scaleFactor_3x3 =histos_scaleFactor_phi_endcap_3x3[ETbin][phi].GetMeanError()
        # histos_scaleFactor_ETbin_phi_endcap_3x3[ETbin].SetBinContent(phi+1,Mean_scaleFactor_3x3)
        # histos_scaleFactor_ETbin_phi_endcap_3x3[ETbin].SetBinError(phi+1,MeanError_scaleFactor_3x3)
        # Mean_scaleFactor_3x3 =histos_scaleFactor_phi_endcap_pos_3x3[ETbin][phi].GetMean()
        # MeanError_scaleFactor_3x3 =histos_scaleFactor_phi_endcap_pos_3x3[ETbin][phi].GetMeanError()
        # histos_scaleFactor_ETbin_phi_endcap_pos_3x3[ETbin].SetBinContent(phi+1,Mean_scaleFactor_3x3)
        # histos_scaleFactor_ETbin_phi_endcap_pos_3x3[ETbin].SetBinError(phi+1,MeanError_scaleFactor_3x3)
        # Mean_scaleFactor_3x3 =histos_scaleFactor_phi_endcap_neg_3x3[ETbin][phi].GetMean()
        # MeanError_scaleFactor_3x3 =histos_scaleFactor_phi_endcap_neg_3x3[ETbin][phi].GetMeanError()
        # histos_scaleFactor_ETbin_phi_endcap_neg_3x3[ETbin].SetBinContent(phi+1,Mean_scaleFactor_3x3)
        # histos_scaleFactor_ETbin_phi_endcap_neg_3x3[ETbin].SetBinError(phi+1,MeanError_scaleFactor_3x3)
        #############################################################################################
        ### Mode ###
        # rms = histos_scaleFactor_phi_endcap_5x5[ETbin][phi].GetRMS()
        # if rms > 0.2:
        #   histos_scaleFactor_phi_endcap_5x5[ETbin][phi].Rebin(2)
        #   rms = histos_scaleFactor_phi_endcap_5x5[ETbin][phi].GetRMS()
        # tf1 = ROOT.TF1("landaugausfunction", ROOT.langaufun, 0, 5, 4)
        # peakpos = histos_scaleFactor_phi_endcap_5x5[ETbin][phi].GetXaxis().GetBinCenter(histos_scaleFactor_phi_endcap_5x5[ETbin][phi].GetMaximumBin())
        # startwidth = rms / 5.0
        # startmpv = peakpos
        # startnorm = histos_scaleFactor_phi_endcap_5x5[ETbin][phi].Integral()
        # startsigma = rms / 10.0
        # tf1.SetParNames("LandauWidth","LandauMPV","Normalisation","GaussianSigma")
        # tf1.SetParameters(startwidth, startmpv, startnorm, startsigma)
        # histos_scaleFactor_phi_endcap_5x5[ETbin][phi].Fit(tf1, "0L", "", 0.6, 3.0)
        # Mean_scaleFactor_5x5 = float(tf1.GetParameter(1))
        # MeanError_scaleFactor_5x5 = float(tf1.GetParError(1))
        # if math.isnan(Mean_scaleFactor_5x5) or math.isnan(MeanError_scaleFactor_5x5):
        #   Mean_scaleFactor_5x5 = -9999.9
        #   MeanError_scaleFactor_5x5 = 999.9
        # if tf1.GetParameter(0)/tf1.GetParameter(3) < 0.034 or MeanError_scaleFactor_5x5 > 0.03:
        #   tf1_alt = ROOT.TF1("gaus","[2]*TMath::Gaus(x,[0],[1])",0.0,3.0)
        #   # startmean = histos_scaleFactor_phi_endcap_5x5[ETbin][phi].GetMean()
        #   startmean = peakpos
        #   startsigma = histos_scaleFactor_phi_endcap_5x5[ETbin][phi].GetRMS()
        #   startnorm = histos_scaleFactor_phi_endcap_5x5[ETbin][phi].Integral(histos_scaleFactor_phi_endcap_5x5[ETbin][phi].GetXaxis().FindBin(0.6),histos_scaleFactor_phi_endcap_5x5[ETbin][phi].GetXaxis().FindBin(3.0))
        #   tf1_alt.SetParNames("GausMean","GausSigma","GausNorm")
        #   tf1_alt.SetParameters(startmean,startsigma,startnorm)
        #   histos_scaleFactor_phi_endcap_5x5[ETbin][phi].Fit(tf1_alt,"0L","",startmean-0.2,startmean+0.2)
        #   val = float(tf1_alt.GetParameter(0))
        #   err = float(tf1_alt.GetParError(0))
        #   if err < MeanError_scaleFactor_5x5 and not math.isnan(val) and not math.isnan(err):
        #     Mean_scaleFactor_5x5 = val
        #     MeanError_scaleFactor_5x5 = err
        #     tf1 = tf1_alt
        # if abs(MeanError_scaleFactor_5x5/Mean_scaleFactor_5x5) > 1.0:
        #   Mean_scaleFactor_5x5 = -9999.9
        #   MeanError_scaleFactor_5x5 = 999.9
        #############################################################################################
        ### Mean ###
        Mean_scaleFactor_5x5 =histos_scaleFactor_phi_endcap_5x5[ETbin][phi].GetMean()
        MeanError_scaleFactor_5x5 =histos_scaleFactor_phi_endcap_5x5[ETbin][phi].GetMeanError()
        #############################################################################################
        histos_scaleFactor_ETbin_phi_endcap_5x5[ETbin].SetBinContent(phi+1,Mean_scaleFactor_5x5)
        histos_scaleFactor_ETbin_phi_endcap_5x5[ETbin].SetBinError(phi+1,MeanError_scaleFactor_5x5)
        #############################################################################################
        ### Mode ###
        # rms = histos_scaleFactor_phi_endcap_pos_5x5[ETbin][phi].GetRMS()
        # if rms > 0.2:
        #   histos_scaleFactor_phi_endcap_pos_5x5[ETbin][phi].Rebin(2)
        #   rms = histos_scaleFactor_phi_endcap_pos_5x5[ETbin][phi].GetRMS()
        # tf1 = ROOT.TF1("landaugausfunction", ROOT.langaufun, 0, 5, 4)
        # peakpos = histos_scaleFactor_phi_endcap_pos_5x5[ETbin][phi].GetXaxis().GetBinCenter(histos_scaleFactor_phi_endcap_pos_5x5[ETbin][phi].GetMaximumBin())
        # startwidth = rms / 5.0
        # startmpv = peakpos
        # startnorm = histos_scaleFactor_phi_endcap_pos_5x5[ETbin][phi].Integral()
        # startsigma = rms / 10.0
        # tf1.SetParNames("LandauWidth","LandauMPV","Normalisation","GaussianSigma")
        # tf1.SetParameters(startwidth, startmpv, startnorm, startsigma)
        # histos_scaleFactor_phi_endcap_pos_5x5[ETbin][phi].Fit(tf1, "0L", "", 0.6, 3.0)
        # Mean_scaleFactor_5x5 = float(tf1.GetParameter(1))
        # MeanError_scaleFactor_5x5 = float(tf1.GetParError(1))
        # if math.isnan(Mean_scaleFactor_5x5) or math.isnan(MeanError_scaleFactor_5x5):
        #   Mean_scaleFactor_5x5 = -9999.9
        #   MeanError_scaleFactor_5x5 = 999.9
        # if tf1.GetParameter(0)/tf1.GetParameter(3) < 0.034 or MeanError_scaleFactor_5x5 > 0.03:
        #   tf1_alt = ROOT.TF1("gaus","[2]*TMath::Gaus(x,[0],[1])",0.0,3.0)
        #   # startmean = histos_scaleFactor_phi_endcap_pos_5x5[ETbin][phi].GetMean()
        #   startmean = peakpos
        #   startsigma = histos_scaleFactor_phi_endcap_pos_5x5[ETbin][phi].GetRMS()
        #   startnorm = histos_scaleFactor_phi_endcap_pos_5x5[ETbin][phi].Integral(histos_scaleFactor_phi_endcap_pos_5x5[ETbin][phi].GetXaxis().FindBin(0.6),histos_scaleFactor_phi_endcap_pos_5x5[ETbin][phi].GetXaxis().FindBin(3.0))
        #   tf1_alt.SetParNames("GausMean","GausSigma","GausNorm")
        #   tf1_alt.SetParameters(startmean,startsigma,startnorm)
        #   histos_scaleFactor_phi_endcap_pos_5x5[ETbin][phi].Fit(tf1_alt,"0L","",startmean-0.2,startmean+0.2)
        #   val = float(tf1_alt.GetParameter(0))
        #   err = float(tf1_alt.GetParError(0))
        #   if err < MeanError_scaleFactor_5x5 and not math.isnan(val) and not math.isnan(err):
        #     Mean_scaleFactor_5x5 = val
        #     MeanError_scaleFactor_5x5 = err
        #     tf1 = tf1_alt
        # if abs(MeanError_scaleFactor_5x5/Mean_scaleFactor_5x5) > 1.0:
        #   Mean_scaleFactor_5x5 = -9999.9
        #   MeanError_scaleFactor_5x5 = 999.9
        #############################################################################################
        ### Mean ###
        Mean_scaleFactor_5x5 =histos_scaleFactor_phi_endcap_pos_5x5[ETbin][phi].GetMean()
        MeanError_scaleFactor_5x5 =histos_scaleFactor_phi_endcap_pos_5x5[ETbin][phi].GetMeanError()
        #############################################################################################
        histos_scaleFactor_ETbin_phi_endcap_pos_5x5[ETbin].SetBinContent(phi+1,Mean_scaleFactor_5x5)
        histos_scaleFactor_ETbin_phi_endcap_pos_5x5[ETbin].SetBinError(phi+1,MeanError_scaleFactor_5x5)
        #############################################################################################
        ### Mode ###
        # rms = histos_scaleFactor_phi_endcap_neg_5x5[ETbin][phi].GetRMS()
        # if rms > 0.2:
        #   histos_scaleFactor_phi_endcap_neg_5x5[ETbin][phi].Rebin(2)
        #   rms = histos_scaleFactor_phi_endcap_neg_5x5[ETbin][phi].GetRMS()
        # tf1 = ROOT.TF1("landaugausfunction", ROOT.langaufun, 0, 5, 4)
        # peakpos = histos_scaleFactor_phi_endcap_neg_5x5[ETbin][phi].GetXaxis().GetBinCenter(histos_scaleFactor_phi_endcap_neg_5x5[ETbin][phi].GetMaximumBin())
        # startwidth = rms / 5.0
        # startmpv = peakpos
        # startnorm = histos_scaleFactor_phi_endcap_neg_5x5[ETbin][phi].Integral()
        # startsigma = rms / 10.0
        # tf1.SetParNames("LandauWidth","LandauMPV","Normalisation","GaussianSigma")
        # tf1.SetParameters(startwidth, startmpv, startnorm, startsigma)
        # histos_scaleFactor_phi_endcap_neg_5x5[ETbin][phi].Fit(tf1, "0L", "", 0.6, 3.0)
        # Mean_scaleFactor_5x5 = float(tf1.GetParameter(1))
        # MeanError_scaleFactor_5x5 = float(tf1.GetParError(1))
        # if math.isnan(Mean_scaleFactor_5x5) or math.isnan(MeanError_scaleFactor_5x5):
        #   Mean_scaleFactor_5x5 = -9999.9
        #   MeanError_scaleFactor_5x5 = 999.9
        # if tf1.GetParameter(0)/tf1.GetParameter(3) < 0.034 or MeanError_scaleFactor_5x5 > 0.03:
        #   tf1_alt = ROOT.TF1("gaus","[2]*TMath::Gaus(x,[0],[1])",0.0,3.0)
        #   # startmean = histos_scaleFactor_phi_endcap_neg_5x5[ETbin][phi].GetMean()
        #   startmean = peakpos
        #   startsigma = histos_scaleFactor_phi_endcap_neg_5x5[ETbin][phi].GetRMS()
        #   startnorm = histos_scaleFactor_phi_endcap_neg_5x5[ETbin][phi].Integral(histos_scaleFactor_phi_endcap_neg_5x5[ETbin][phi].GetXaxis().FindBin(0.6),histos_scaleFactor_phi_endcap_neg_5x5[ETbin][phi].GetXaxis().FindBin(3.0))
        #   tf1_alt.SetParNames("GausMean","GausSigma","GausNorm")
        #   tf1_alt.SetParameters(startmean,startsigma,startnorm)
        #   histos_scaleFactor_phi_endcap_neg_5x5[ETbin][phi].Fit(tf1_alt,"0L","",startmean-0.2,startmean+0.2)
        #   val = float(tf1_alt.GetParameter(0))
        #   err = float(tf1_alt.GetParError(0))
        #   if err < MeanError_scaleFactor_5x5 and not math.isnan(val) and not math.isnan(err):
        #     Mean_scaleFactor_5x5 = val
        #     MeanError_scaleFactor_5x5 = err
        #     tf1 = tf1_alt
        # if abs(MeanError_scaleFactor_5x5/Mean_scaleFactor_5x5) > 1.0:
        #   Mean_scaleFactor_5x5 = -9999.9
        #   MeanError_scaleFactor_5x5 = 999.9
        #############################################################################################
        ### Mean ###
        Mean_scaleFactor_5x5 =histos_scaleFactor_phi_endcap_neg_5x5[ETbin][phi].GetMean()
        MeanError_scaleFactor_5x5 =histos_scaleFactor_phi_endcap_neg_5x5[ETbin][phi].GetMeanError()
        #############################################################################################
        histos_scaleFactor_ETbin_phi_endcap_neg_5x5[ETbin].SetBinContent(phi+1,Mean_scaleFactor_5x5)
        histos_scaleFactor_ETbin_phi_endcap_neg_5x5[ETbin].SetBinError(phi+1,MeanError_scaleFactor_5x5)
        
        # Mean_scaleFactor_3x3 =histos_scaleFactor_phi_HF_3x3[ETbin][phi].GetMean()
        # MeanError_scaleFactor_3x3 =histos_scaleFactor_phi_HF_3x3[ETbin][phi].GetMeanError()
        # histos_scaleFactor_ETbin_phi_HF_3x3[ETbin].SetBinContent(phi+1,Mean_scaleFactor_3x3)
        # histos_scaleFactor_ETbin_phi_HF_3x3[ETbin].SetBinError(phi+1,MeanError_scaleFactor_3x3)
        # Mean_scaleFactor_3x3 =histos_scaleFactor_phi_HF_pos_3x3[ETbin][phi].GetMean()
        # MeanError_scaleFactor_3x3 =histos_scaleFactor_phi_HF_pos_3x3[ETbin][phi].GetMeanError()
        # histos_scaleFactor_ETbin_phi_HF_pos_3x3[ETbin].SetBinContent(phi+1,Mean_scaleFactor_3x3)
        # histos_scaleFactor_ETbin_phi_HF_pos_3x3[ETbin].SetBinError(phi+1,MeanError_scaleFactor_3x3)
        # Mean_scaleFactor_3x3 =histos_scaleFactor_phi_HF_neg_3x3[ETbin][phi].GetMean()
        # MeanError_scaleFactor_3x3 =histos_scaleFactor_phi_HF_neg_3x3[ETbin][phi].GetMeanError()
        # histos_scaleFactor_ETbin_phi_HF_neg_3x3[ETbin].SetBinContent(phi+1,Mean_scaleFactor_3x3)
        # histos_scaleFactor_ETbin_phi_HF_neg_3x3[ETbin].SetBinError(phi+1,MeanError_scaleFactor_3x3)
        #############################################################################################
        ### Mode ###
        # rms = histos_scaleFactor_phi_HF_5x5[ETbin][phi].GetRMS()
        # if rms > 0.2:
        #   histos_scaleFactor_phi_HF_5x5[ETbin][phi].Rebin(2)
        #   rms = histos_scaleFactor_phi_HF_5x5[ETbin][phi].GetRMS()
        # tf1 = ROOT.TF1("landaugausfunction", ROOT.langaufun, 0, 5, 4)
        # peakpos = histos_scaleFactor_phi_HF_5x5[ETbin][phi].GetXaxis().GetBinCenter(histos_scaleFactor_phi_HF_5x5[ETbin][phi].GetMaximumBin())
        # startwidth = rms / 5.0
        # startmpv = peakpos
        # startnorm = histos_scaleFactor_phi_HF_5x5[ETbin][phi].Integral()
        # startsigma = rms / 10.0
        # tf1.SetParNames("LandauWidth","LandauMPV","Normalisation","GaussianSigma")
        # tf1.SetParameters(startwidth, startmpv, startnorm, startsigma)
        # histos_scaleFactor_phi_HF_5x5[ETbin][phi].Fit(tf1, "0L", "", 0.6, 3.0)
        # Mean_scaleFactor_5x5 = float(tf1.GetParameter(1))
        # MeanError_scaleFactor_5x5 = float(tf1.GetParError(1))
        # if math.isnan(Mean_scaleFactor_5x5) or math.isnan(MeanError_scaleFactor_5x5):
        #   Mean_scaleFactor_5x5 = -9999.9
        #   MeanError_scaleFactor_5x5 = 999.9
        # if tf1.GetParameter(0)/tf1.GetParameter(3) < 0.034 or MeanError_scaleFactor_5x5 > 0.03:
        #   tf1_alt = ROOT.TF1("gaus","[2]*TMath::Gaus(x,[0],[1])",0.0,3.0)
        #   # startmean = histos_scaleFactor_phi_HF_5x5[ETbin][phi].GetMean()
        #   startmean = peakpos
        #   startsigma = histos_scaleFactor_phi_HF_5x5[ETbin][phi].GetRMS()
        #   startnorm = histos_scaleFactor_phi_HF_5x5[ETbin][phi].Integral(histos_scaleFactor_phi_HF_5x5[ETbin][phi].GetXaxis().FindBin(0.6),histos_scaleFactor_phi_HF_5x5[ETbin][phi].GetXaxis().FindBin(3.0))
        #   tf1_alt.SetParNames("GausMean","GausSigma","GausNorm")
        #   tf1_alt.SetParameters(startmean,startsigma,startnorm)
        #   histos_scaleFactor_phi_HF_5x5[ETbin][phi].Fit(tf1_alt,"0L","",startmean-0.2,startmean+0.2)
        #   val = float(tf1_alt.GetParameter(0))
        #   err = float(tf1_alt.GetParError(0))
        #   if err < MeanError_scaleFactor_5x5 and not math.isnan(val) and not math.isnan(err):
        #     Mean_scaleFactor_5x5 = val
        #     MeanError_scaleFactor_5x5 = err
        #     tf1 = tf1_alt
        # if abs(MeanError_scaleFactor_5x5/Mean_scaleFactor_5x5) > 1.0:
        #   Mean_scaleFactor_5x5 = -9999.9
        #   MeanError_scaleFactor_5x5 = 999.9
        #############################################################################################
        ### Mean ###
        # Mean_scaleFactor_5x5 =histos_scaleFactor_phi_HF_5x5[ETbin][phi].GetMean()
        # MeanError_scaleFactor_5x5 =histos_scaleFactor_phi_HF_5x5[ETbin][phi].GetMeanError()
        #############################################################################################
        # histos_scaleFactor_ETbin_phi_HF_5x5[ETbin].SetBinContent(phi+1,Mean_scaleFactor_5x5)
        # histos_scaleFactor_ETbin_phi_HF_5x5[ETbin].SetBinError(phi+1,MeanError_scaleFactor_5x5)
        #############################################################################################
        ### Mode ###
        # rms = histos_scaleFactor_phi_HF_pos_5x5[ETbin][phi].GetRMS()
        # if rms > 0.2:
        #   histos_scaleFactor_phi_HF_pos_5x5[ETbin][phi].Rebin(2)
        #   rms = histos_scaleFactor_phi_HF_pos_5x5[ETbin][phi].GetRMS()
        # tf1 = ROOT.TF1("landaugausfunction", ROOT.langaufun, 0, 5, 4)
        # peakpos = histos_scaleFactor_phi_HF_pos_5x5[ETbin][phi].GetXaxis().GetBinCenter(histos_scaleFactor_phi_HF_pos_5x5[ETbin][phi].GetMaximumBin())
        # startwidth = rms / 5.0
        # startmpv = peakpos
        # startnorm = histos_scaleFactor_phi_HF_pos_5x5[ETbin][phi].Integral()
        # startsigma = rms / 10.0
        # tf1.SetParNames("LandauWidth","LandauMPV","Normalisation","GaussianSigma")
        # tf1.SetParameters(startwidth, startmpv, startnorm, startsigma)
        # histos_scaleFactor_phi_HF_pos_5x5[ETbin][phi].Fit(tf1, "0L", "", 0.6, 3.0)
        # Mean_scaleFactor_5x5 = float(tf1.GetParameter(1))
        # MeanError_scaleFactor_5x5 = float(tf1.GetParError(1))
        # if math.isnan(Mean_scaleFactor_5x5) or math.isnan(MeanError_scaleFactor_5x5):
        #   Mean_scaleFactor_5x5 = -9999.9
        #   MeanError_scaleFactor_5x5 = 999.9
        # if tf1.GetParameter(0)/tf1.GetParameter(3) < 0.034 or MeanError_scaleFactor_5x5 > 0.03:
        #   tf1_alt = ROOT.TF1("gaus","[2]*TMath::Gaus(x,[0],[1])",0.0,3.0)
        #   # startmean = histos_scaleFactor_phi_HF_pos_5x5[ETbin][phi].GetMean()
        #   startmean = peakpos
        #   startsigma = histos_scaleFactor_phi_HF_pos_5x5[ETbin][phi].GetRMS()
        #   startnorm = histos_scaleFactor_phi_HF_pos_5x5[ETbin][phi].Integral(histos_scaleFactor_phi_HF_pos_5x5[ETbin][phi].GetXaxis().FindBin(0.6),histos_scaleFactor_phi_HF_pos_5x5[ETbin][phi].GetXaxis().FindBin(3.0))
        #   tf1_alt.SetParNames("GausMean","GausSigma","GausNorm")
        #   tf1_alt.SetParameters(startmean,startsigma,startnorm)
        #   histos_scaleFactor_phi_HF_pos_5x5[ETbin][phi].Fit(tf1_alt,"0L","",startmean-0.2,startmean+0.2)
        #   val = float(tf1_alt.GetParameter(0))
        #   err = float(tf1_alt.GetParError(0))
        #   if err < MeanError_scaleFactor_5x5 and not math.isnan(val) and not math.isnan(err):
        #     Mean_scaleFactor_5x5 = val
        #     MeanError_scaleFactor_5x5 = err
        #     tf1 = tf1_alt
        # if abs(MeanError_scaleFactor_5x5/Mean_scaleFactor_5x5) > 1.0:
        #   Mean_scaleFactor_5x5 = -9999.9
        #   MeanError_scaleFactor_5x5 = 999.9
        #############################################################################################
        ### Mean ###
        # Mean_scaleFactor_5x5 =histos_scaleFactor_phi_HF_pos_5x5[ETbin][phi].GetMean()
        # MeanError_scaleFactor_5x5 =histos_scaleFactor_phi_HF_pos_5x5[ETbin][phi].GetMeanError()
        #############################################################################################
        # histos_scaleFactor_ETbin_phi_HF_pos_5x5[ETbin].SetBinContent(phi+1,Mean_scaleFactor_5x5)
        # histos_scaleFactor_ETbin_phi_HF_pos_5x5[ETbin].SetBinError(phi+1,MeanError_scaleFactor_5x5)
        #############################################################################################
        ### Mode ###
        # rms = histos_scaleFactor_phi_HF_neg_5x5[ETbin][phi].GetRMS()
        # if rms > 0.2:
        #   histos_scaleFactor_phi_HF_neg_5x5[ETbin][phi].Rebin(2)
        #   rms = histos_scaleFactor_phi_HF_neg_5x5[ETbin][phi].GetRMS()
        # tf1 = ROOT.TF1("landaugausfunction", ROOT.langaufun, 0, 5, 4)
        # peakpos = histos_scaleFactor_phi_HF_neg_5x5[ETbin][phi].GetXaxis().GetBinCenter(histos_scaleFactor_phi_HF_neg_5x5[ETbin][phi].GetMaximumBin())
        # startwidth = rms / 5.0
        # startmpv = peakpos
        # startnorm = histos_scaleFactor_phi_HF_neg_5x5[ETbin][phi].Integral()
        # startsigma = rms / 10.0
        # tf1.SetParNames("LandauWidth","LandauMPV","Normalisation","GaussianSigma")
        # tf1.SetParameters(startwidth, startmpv, startnorm, startsigma)
        # histos_scaleFactor_phi_HF_neg_5x5[ETbin][phi].Fit(tf1, "0L", "", 0.6, 3.0)
        # Mean_scaleFactor_5x5 = float(tf1.GetParameter(1))
        # MeanError_scaleFactor_5x5 = float(tf1.GetParError(1))
        # if math.isnan(Mean_scaleFactor_5x5) or math.isnan(MeanError_scaleFactor_5x5):
        #   Mean_scaleFactor_5x5 = -9999.9
        #   MeanError_scaleFactor_5x5 = 999.9
        # if tf1.GetParameter(0)/tf1.GetParameter(3) < 0.034 or MeanError_scaleFactor_5x5 > 0.03:
        #   tf1_alt = ROOT.TF1("gaus","[2]*TMath::Gaus(x,[0],[1])",0.0,3.0)
        #   # startmean = histos_scaleFactor_phi_HF_neg_5x5[ETbin][phi].GetMean()
        #   startmean = peakpos
        #   startsigma = histos_scaleFactor_phi_HF_neg_5x5[ETbin][phi].GetRMS()
        #   startnorm = histos_scaleFactor_phi_HF_neg_5x5[ETbin][phi].Integral(histos_scaleFactor_phi_HF_neg_5x5[ETbin][phi].GetXaxis().FindBin(0.6),histos_scaleFactor_phi_HF_neg_5x5[ETbin][phi].GetXaxis().FindBin(3.0))
        #   tf1_alt.SetParNames("GausMean","GausSigma","GausNorm")
        #   tf1_alt.SetParameters(startmean,startsigma,startnorm)
        #   histos_scaleFactor_phi_HF_neg_5x5[ETbin][phi].Fit(tf1_alt,"0L","",startmean-0.2,startmean+0.2)
        #   val = float(tf1_alt.GetParameter(0))
        #   err = float(tf1_alt.GetParError(0))
        #   if err < MeanError_scaleFactor_5x5 and not math.isnan(val) and not math.isnan(err):
        #     Mean_scaleFactor_5x5 = val
        #     MeanError_scaleFactor_5x5 = err
        #     tf1 = tf1_alt
        # if abs(MeanError_scaleFactor_5x5/Mean_scaleFactor_5x5) > 1.0:
        #   Mean_scaleFactor_5x5 = -9999.9
        #   MeanError_scaleFactor_5x5 = 999.9
        #############################################################################################
        ### Mean ###
        # Mean_scaleFactor_5x5 =histos_scaleFactor_phi_HF_neg_5x5[ETbin][phi].GetMean()
        # MeanError_scaleFactor_5x5 =histos_scaleFactor_phi_HF_neg_5x5[ETbin][phi].GetMeanError()
        #############################################################################################
        # histos_scaleFactor_ETbin_phi_HF_neg_5x5[ETbin].SetBinContent(phi+1,Mean_scaleFactor_5x5)
        # histos_scaleFactor_ETbin_phi_HF_neg_5x5[ETbin].SetBinError(phi+1,MeanError_scaleFactor_5x5)
    for eta in range(0,82):
        # Mean_scaleFactor_3x3 =histos_scaleFactor_eta_3x3[ETbin][eta].GetMean()
        # MeanError_scaleFactor_3x3 =histos_scaleFactor_eta_3x3[ETbin][eta].GetMeanError()
        Mean_scaleFactor_5x5 =histos_scaleFactor_eta_5x5[ETbin][eta].GetMean()
        MeanError_scaleFactor_5x5 =histos_scaleFactor_eta_5x5[ETbin][eta].GetMeanError()
        # histos_scaleFactor_ETbin_eta_3x3[ETbin].SetBinContent(eta+1,Mean_scaleFactor_3x3)
        # histos_scaleFactor_ETbin_eta_3x3[ETbin].SetBinError(eta+1,MeanError_scaleFactor_3x3)
        histos_scaleFactor_ETbin_eta_5x5[ETbin].SetBinContent(eta+1,Mean_scaleFactor_5x5)
        histos_scaleFactor_ETbin_eta_5x5[ETbin].SetBinError(eta+1,MeanError_scaleFactor_5x5)
    for foldedEta in range(0,41):
        # Mean_HCALisolation_3x3 =histos_HCALisolation_eta_folded_3x3[ETbin][foldedEta].GetMean()
        # MeanError_HCALisolation_3x3 =histos_HCALisolation_eta_folded_3x3[ETbin][foldedEta].GetMeanError()
        Mean_HCALisolation_5x5 =histos_HCALisolation_eta_folded_5x5[ETbin][foldedEta].GetMean()
        MeanError_HCALisolation_5x5 =histos_HCALisolation_eta_folded_5x5[ETbin][foldedEta].GetMeanError()
        # histos_HCALisolation_ETbin_foldedEta_3x3[ETbin].SetBinContent(foldedEta+1,Mean_HCALisolation_3x3)
        # histos_HCALisolation_ETbin_foldedEta_3x3[ETbin].SetBinError(foldedEta+1,MeanError_HCALisolation_3x3)
        histos_HCALisolation_ETbin_foldedEta_5x5[ETbin].SetBinContent(foldedEta+1,Mean_HCALisolation_5x5)
        histos_HCALisolation_ETbin_foldedEta_5x5[ETbin].SetBinError(foldedEta+1,MeanError_HCALisolation_5x5)
        # Mean_scaleFactor_3x3 =histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].GetMean()
        # MeanError_scaleFactor_3x3 =histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].GetMeanError()
        # histos_scaleFactor_ETbin_foldedEta_3x3[ETbin].SetBinContent(foldedEta+1,Mean_scaleFactor_3x3)
        # histos_scaleFactor_ETbin_foldedEta_3x3[ETbin].SetBinError(foldedEta+1,MeanError_scaleFactor_3x3)
        ##################################################################################################
        ### Mode ###
        rms = histos_scaleFactor_eta_folded_5x5[ETbin][foldedEta].GetRMS()
        if rms > 0.2:
          histos_scaleFactor_eta_folded_5x5[ETbin][foldedEta].Rebin(2)
          rms = histos_scaleFactor_eta_folded_5x5[ETbin][foldedEta].GetRMS()
        tf1 = ROOT.TF1("landaugausfunction", ROOT.langaufun, 0, 5, 4)
        peakpos = histos_scaleFactor_eta_folded_5x5[ETbin][foldedEta].GetXaxis().GetBinCenter(histos_scaleFactor_eta_folded_5x5[ETbin][foldedEta].GetMaximumBin())
        startwidth = rms / 5.0
        startmpv = peakpos
        startnorm = histos_scaleFactor_eta_folded_5x5[ETbin][foldedEta].Integral()
        startsigma = rms / 10.0
        tf1.SetParNames("LandauWidth","LandauMPV","Normalisation","GaussianSigma")
        tf1.SetParameters(startwidth, startmpv, startnorm, startsigma)
        histos_scaleFactor_eta_folded_5x5[ETbin][foldedEta].Fit(tf1, "0L", "", 0.6, 3.0)
        Mean_scaleFactor_5x5 = float(tf1.GetParameter(1))
        MeanError_scaleFactor_5x5 = float(tf1.GetParError(1))
        if math.isnan(Mean_scaleFactor_5x5) or math.isnan(MeanError_scaleFactor_5x5):
          Mean_scaleFactor_5x5 = -9999.9
          MeanError_scaleFactor_5x5 = 999.9
        if tf1.GetParameter(0)/tf1.GetParameter(3) < 0.034 or MeanError_scaleFactor_5x5 > 0.03:
          tf1_alt = ROOT.TF1("gaus","[2]*TMath::Gaus(x,[0],[1])",0.0,3.0)
          startmean = histos_scaleFactor_eta_folded_5x5[ETbin][foldedEta].GetMean()
          startmean = peakpos
          startsigma = histos_scaleFactor_eta_folded_5x5[ETbin][foldedEta].GetRMS()
          startnorm = histos_scaleFactor_eta_folded_5x5[ETbin][foldedEta].Integral(histos_scaleFactor_eta_folded_5x5[ETbin][foldedEta].GetXaxis().FindBin(0.6),histos_scaleFactor_eta_folded_5x5[ETbin][foldedEta].GetXaxis().FindBin(3.0))
          tf1_alt.SetParNames("GausMean","GausSigma","GausNorm")
          tf1_alt.SetParameters(startmean,startsigma,startnorm)
          histos_scaleFactor_eta_folded_5x5[ETbin][foldedEta].Fit(tf1_alt,"0L","",startmean-0.2,startmean+0.2)
          val = float(tf1_alt.GetParameter(0))
          err = float(tf1_alt.GetParError(0))
          if err < MeanError_scaleFactor_5x5 and not math.isnan(val) and not math.isnan(err):
            Mean_scaleFactor_5x5 = val
            MeanError_scaleFactor_5x5 = err
            tf1 = tf1_alt
        if abs(MeanError_scaleFactor_5x5/Mean_scaleFactor_5x5) > 1.0:
          Mean_scaleFactor_5x5 = -9999.9
          MeanError_scaleFactor_5x5 = 999.9
        sf_errors.append('ETbin:%d, foldedEta:%d, err:%f'%(ETbin,foldedEta,MeanError_scaleFactor_5x5))
        ### Draw mode plots ###
        hist_title = 'ETbin = %d, |ieta| = %d' % (ETbin,foldedEta+1)
        histos_scaleFactor_eta_folded_5x5[ETbin][foldedEta].SetTitle(hist_title)
        tf1.Draw()
        tf1.SetLineColor(ROOT.kRed)
        tf1.SetLineWidth(2)
        histos_scaleFactor_eta_folded_5x5[ETbin][foldedEta].Draw("HIST")
        tf1.Draw("SAME")
        saveas='%spiMinus_SF_hist_ETbin%s_ieta%s.png' % (saveWhere,ETbin,foldedEta+1)
        canvas.SaveAs(saveas)
        ##############################################################################################
        ### Mean ###
        # Mean_scaleFactor_5x5 =histos_scaleFactor_eta_folded_5x5[ETbin][foldedEta].GetMean()
        # MeanError_scaleFactor_5x5 =histos_scaleFactor_eta_folded_5x5[ETbin][foldedEta].GetMeanError()
        # hist_title = 'ETbin = %d, |ieta| = %d' % (ETbin,foldedEta+1)
        # histos_scaleFactor_eta_folded_5x5[ETbin][foldedEta].SetTitle(hist_title)
        # histos_scaleFactor_eta_folded_5x5[ETbin][foldedEta].Draw("HIST")
        # saveas='%spiMinus_SF_hist_ETbin%s_ieta%s.png' % (saveWhere,ETbin,foldedEta+1)
        # canvas.SaveAs(saveas)
        ##############################################################################################
        histos_scaleFactor_ETbin_foldedEta_5x5[ETbin].SetBinContent(foldedEta+1,Mean_scaleFactor_5x5)
        histos_scaleFactor_ETbin_foldedEta_5x5[ETbin].SetBinError(foldedEta+1,MeanError_scaleFactor_5x5)

# for ETbin in range(0,13):
#   histos_scaleFactor_ETbin_foldedEta_5x5[ETbin].GetXaxis().SetTitle("Pi- TPG iEta")
#   histos_scaleFactor_ETbin_foldedEta_5x5[ETbin].GetXaxis().SetRangeUser(0,41) # Eta range
#   histos_scaleFactor_ETbin_foldedEta_5x5[ETbin].GetYaxis().SetTitle("GenPt/(corrTPGe+TPGh)")
#   histos_scaleFactor_ETbin_foldedEta_5x5[ETbin].GetYaxis().SetTitleOffset(1.1)
#   histos_scaleFactor_ETbin_foldedEta_5x5[ETbin].GetYaxis().SetRangeUser(0.0,4.0) # Scale factor
#   histos_scaleFactor_ETbin_foldedEta_5x5[ETbin].SetTitle('GenPt/(corrTPGe+TPGh) vs TPG iEta')
#   histos_scaleFactor_ETbin_foldedEta_5x5[ETbin].SetMarkerStyle(23)
#   histos_scaleFactor_ETbin_foldedEta_5x5[ETbin].Draw("pE1")
#   saveas='%sphoton_SF_%s_etbin%d.png' % (saveWhere,squaresize,ETbin)
#   canvas.SaveAs(saveas)

for ETbin in range(0,13):
  for foldedEta in range(0,41):
    Mean_scaleFactor_5x5 = histos_scaleFactor_ETbin_foldedEta_5x5[ETbin].GetBinContent(foldedEta+1)
    if foldedEta < 28:
      if ETbin == 0 and foldedEta == 0:
          text_file.write("   float hcal[364] = {")
      else:
          text_file.write(", ")
      # # Write 1.0 for scale factors < 1.0
      # if Mean_scaleFactor_5x5 < 1.0 or math.isnan(Mean_scaleFactor_5x5):
      if math.isnan(Mean_scaleFactor_5x5):
          text_file.write("%f" % 1.0)
          # text_file.write("%f" % last_written[foldedEta])
      else:
          scalefactor_towrite = Mean_scaleFactor_5x5
          text_file.write("%f" % scalefactor_towrite)
          last_written[foldedEta] = scalefactor_towrite
      if ETbin == 12 and foldedEta == 27:
          text_file.write("};")
    elif foldedEta > 28:
      if ETbin == 0 and foldedEta == 29:
          text_file_HF.write("   float hf[156] = {")
      else:
          text_file_HF.write(", ")
      # # Write 1.0 for scale factors < 1.0
      # if Mean_scaleFactor_5x5 < 1.0 or math.isnan(Mean_scaleFactor_5x5):
      if math.isnan(Mean_scaleFactor_5x5):
          text_file_HF.write("%f" % 1.0)
      else:
          scalefactor_towrite = Mean_scaleFactor_5x5
          text_file_HF.write("%f" % scalefactor_towrite)
          last_written[foldedEta] = scalefactor_towrite
      if ETbin == 12 and foldedEta == 40:
          text_file_HF.write("};")

def draw_histo(squaresize,suffix):
  canvas = ROOT.TCanvas("asdf", "adsf", 800, 800)
  pad1 = ROOT.TPad("pad1","",0,0,1,1)
  pad1.Draw()
  pad1.cd()
  
  histos_orig = []
  histos = []
  for ETbin in range(0,13):
    # if squaresize == '3x3':
    #   if suffix[-len('_iphi'):] == '_iphi':
    #     histos.append(histos_scaleFactor_ETbin_phi_3x3[ETbin])
    #   elif suffix[-len('_iphi_barrel'):] == '_iphi_barrel':
    #     histos.append(histos_scaleFactor_ETbin_phi_barrel_3x3[ETbin])
    #   elif suffix[-len('_iphi_endcap'):] == '_iphi_endcap':
    #     histos.append(histos_scaleFactor_ETbin_phi_endcap_3x3[ETbin])
    #   elif suffix[-len('_iphi_endcap_pos'):] == '_iphi_endcap_pos':
    #     histos.append(histos_scaleFactor_ETbin_phi_endcap_pos_3x3[ETbin])
    #   elif suffix[-len('_iphi_endcap_neg'):] == '_iphi_endcap_neg':
    #     histos.append(histos_scaleFactor_ETbin_phi_endcap_neg_3x3[ETbin])
    #   elif suffix[-len('_HCALisolation'):] == '_HCALisolation':
    #     histos.append(histos_HCALisolation_ETbin_foldedEta_3x3[ETbin])
    #   elif suffix[-len('_unfolded'):] == '_unfolded':
    #     histos_orig.append(histos_scaleFactor_ETbin_eta_3x3[ETbin])
    #     hname_new = 'hist_ETbin%i_trueieta' % i
    #     histos.append(ROOT.TH1F(hname_new,"",58,-29,29))
    #   else:
    #     histos.append(histos_scaleFactor_ETbin_foldedEta_3x3[ETbin])
    if squaresize == '5x5':
      if suffix[-len('_iphi'):] == '_iphi':
        histos.append(histos_scaleFactor_ETbin_phi_5x5[ETbin])
      elif suffix[-len('_iphi_barrel'):] == '_iphi_barrel':
        histos.append(histos_scaleFactor_ETbin_phi_barrel_5x5[ETbin])
      elif suffix[-len('_iphi_endcap'):] == '_iphi_endcap':
        histos.append(histos_scaleFactor_ETbin_phi_endcap_5x5[ETbin])
      elif suffix[-len('_iphi_endcap_pos'):] == '_iphi_endcap_pos':
        histos.append(histos_scaleFactor_ETbin_phi_endcap_pos_5x5[ETbin])
      elif suffix[-len('_iphi_endcap_neg'):] == '_iphi_endcap_neg':
        histos.append(histos_scaleFactor_ETbin_phi_endcap_neg_5x5[ETbin])
      elif suffix[-len('_iphi_HF'):] == '_iphi_HF':
        histos.append(histos_scaleFactor_ETbin_phi_HF_5x5[ETbin])
      elif suffix[-len('_iphi_HF_pos'):] == '_iphi_HF_pos':
        histos.append(histos_scaleFactor_ETbin_phi_HF_pos_5x5[ETbin])
      elif suffix[-len('_iphi_HF_neg'):] == '_iphi_HF_neg':
        histos.append(histos_scaleFactor_ETbin_phi_HF_neg_5x5[ETbin])
      elif suffix[-len('_HCALisolation'):] == '_HCALisolation':
        histos.append(histos_HCALisolation_ETbin_foldedEta_5x5[ETbin])
      elif suffix[-len('_unfolded'):] == '_unfolded':
        histos_orig.append(histos_scaleFactor_ETbin_eta_5x5[ETbin])
        hname_new = 'hist_ETbin%i_trueieta' % ETbin
        histos.append(ROOT.TH1F(hname_new,"",84,-42,42))
      else:
        histos.append(histos_scaleFactor_ETbin_foldedEta_5x5[ETbin])
    else:
      print 'Bad squaresize (must be 5x5), exiting'
      exit(1)

  if suffix[-len('_unfolded'):] == '_unfolded':
    for i in range(0,13):
      for ieta in range(-41,0):
        histos[i].SetBinContent(histos[i].GetXaxis().FindBin(float(ieta)+0.5),histos_orig[i].GetBinContent(ieta+42))
        histos[i].SetBinError(histos[i].GetXaxis().FindBin(float(ieta)+0.5),histos_orig[i].GetBinError(ieta+42))
      for ieta in range(1,42):
        histos[i].SetBinContent(histos[i].GetXaxis().FindBin(float(ieta)-0.5),histos_orig[i].GetBinContent(ieta+41))
        histos[i].SetBinError(histos[i].GetXaxis().FindBin(float(ieta)-0.5),histos_orig[i].GetBinError(ieta+41))

  colors = []
  colors.append(ROOT.kBlack)
  colors.append(ROOT.kGreen+3)
  colors.append(ROOT.kBlue+2)
  colors.append(ROOT.kOrange)
  colors.append(ROOT.kGreen-3)
  colors.append(ROOT.kPink-3)
  colors.append(ROOT.kBlue-6)
  colors.append(ROOT.kYellow+3)
  colors.append(ROOT.kAzure+6)
  colors.append(ROOT.kRed-7)
  colors.append(ROOT.kMagenta+2)
  colors.append(ROOT.kMagenta+3)
  colors.append(ROOT.kMagenta+4)

  for i in range(0,13):
    histos[i].SetMarkerColor(colors[i])
    histos[i].SetLineColor(colors[i])
    histos[i].SetMarkerStyle(23)
    histos[i].GetXaxis().SetTitle("Pi+/- TPG iEta")
    if suffix[-len('_iphi'):] == '_iphi' or suffix[-len('_iphi_barrel'):] == '_iphi_barrel' or suffix[-len('_iphi_endcap'):] == '_iphi_endcap':
      histos[i].GetXaxis().SetTitle("Pi- TPG iPhi")
    histos[i].GetXaxis().SetRangeUser(0,41) # Eta range
    if suffix[-len('_iphi'):] == '_iphi' or suffix[-len('_iphi_barrel'):] == '_iphi_barrel' or suffix[-len('_iphi_endcap'):] == '_iphi_endcap' or suffix[-len('_iphi_endcap_pos'):] == '_iphi_endcap_pos' or suffix[-len('_iphi_endcap_neg'):] == '_iphi_endcap_neg':
      histos[i].GetXaxis().SetRangeUser(0,72) # Phi range
    elif suffix[-len('_unfolded'):] == '_unfolded':
      histos[i].GetXaxis().SetRangeUser(-41,41)
    histos[i].GetYaxis().SetTitle("GenPt/(corrTPGe+TPGh)")
    if suffix[-len('_HCALisolation'):] == '_HCALisolation':
      histos[i].GetYaxis().SetTitle("Isolation [GeV]")
    histos[i].GetYaxis().SetTitleOffset(1.1)
    # histos[i].GetYaxis().SetRangeUser(0.0,4.0) # Old
    histos[i].GetYaxis().SetRangeUser(0.0,3.0) # New
    if suffix[-len('_HCALisolation'):] == '_HCALisolation':
      histos[i].GetYaxis().SetRangeUser(0.0,5.0) # Isolation
    histos[i].SetTitle('GenPt/(corrTPGe+TPGh) vs TPG iEta')
    if suffix[-len('_iphi'):] == '_iphi' or suffix[-len('_iphi_barrel'):] == '_iphi_barrel' or suffix[-len('_iphi_endcap'):] == '_iphi_endcap':
      histos[i].SetTitle('GenPt/(corrTPGe+TPGh) vs TPG iPhi')
    elif suffix[-len('_HCALisolation'):] == '_HCALisolation':
      histos[i].SetTitle('Isolation vs TPG iEta')
    if i == 0:
      histos[i].Draw("pE1")
    else:
      histos[i].Draw("pE1same")

  pad2 = ROOT.TPad("pad2","",0,0,1,1)
  pad2.SetFillColor(0)
  pad2.SetFillStyle(4000)
  pad2.SetFrameFillStyle(0)
  pad2.Draw()
  pad2.cd()
  for i in range(0,13):
    hist_clone = histos[i].Clone()
    hist_clone.GetXaxis().SetTitle("")
    hist_clone.GetXaxis().SetLabelOffset(999)
    hist_clone.GetYaxis().SetTitle("")
    hist_clone.GetYaxis().SetLabelOffset(999)
    if i == 0:
      hist_clone.Draw("pE1 X+ Y+")
    else:
      hist_clone.Draw("pE1same X+ Y+")

  legend1 = ROOT.TLegend(0.17,0.51,0.39,0.85, "HCAL 5x5 TPG Et", "brNDC")
  if suffix[-len('_HCALisolation'):] == '_HCALisolation':
    legend1 = ROOT.TLegend(0.17, 0.55, 0.39, 0.85, "HCAL TPG Et", "brNDC") # Isolation
  legend1.SetFillColor(ROOT.kWhite)
  legend1.SetBorderSize(1)
  legend1.AddEntry(histos[0], "3<Et<6 GeV")
  legend1.AddEntry(histos[1], "6<Et<9 GeV")
  legend1.AddEntry(histos[2], "9<Et<12 GeV")
  legend1.AddEntry(histos[3], "12<Et<15 GeV")
  legend1.AddEntry(histos[4], "15<Et<20 GeV")
  legend1.AddEntry(histos[5], "20<Et<25 GeV")
  legend1.AddEntry(histos[6], "25<Et<30 GeV")
  legend1.AddEntry(histos[7], "30<Et<35 GeV")
  legend1.AddEntry(histos[8], "35<Et<40 GeV")
  legend1.AddEntry(histos[9], "40<Et<45 GeV")
  legend1.AddEntry(histos[10], "45<Et<55 GeV")
  legend1.AddEntry(histos[11], "55<Et<70 GeV")
  legend1.AddEntry(histos[12], "70<Et<90 GeV")


  legend1.Draw("same")
#  saveas='%spiminus_p20_mean_SF_%s_%s.png' % (saveWhere,squaresize,suffix)
  saveas='piminus_p_mode_SF_%s_noLowerLimit.png' % squaresize
  canvas.SaveAs(saveas)
# end def draw_histo()

squaresize = '5x5'
draw_histo(squaresize,'modeCalib')
# draw_histo(squaresize,'modeCalib_iphi_barrel')
# draw_histo(squaresize,'modeCalib_iphi_endcap_pos')
# draw_histo(squaresize,'modeCalib_iphi_endcap_neg')
# draw_histo(squaresize,'modeCalib_unfolded')
# draw_histo(squaresize,'mean_HCALisolation')
