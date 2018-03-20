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
if len(argv) != 4:
   print 'Usage: python plotSinglePhoton.py output_from_computeECALcalibs_MC.root squaresize suffix'
   exit()

infile = argv[1]
squaresize = argv[2]
suffix = argv[3]

ntuple_file = ROOT.TFile(infile)

######## LABEL & SAVE WHERE #########
saveWhere='/nfs_scratch/jjbuchanan/calibrations_Jan2017/MonteCarlo/CMSSW_9_2_8/src/L1Trigger/CaloLayer1Calibrations/bin/SinglePhoton/'
text_file = open("ecalcalibs_MC_"+suffix+"_all.txt","w")

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

#####################################
#Get NTUPLE                 #
#####################################

histos_resolution_3x3 = []
histos_resolution_5x5 = []
histos_genpt_3x3 = []
histos_genpt_5x5 = []
histos_summed33e_3x3 = []
histos_summed33e_5x5 = []
histos_summed55e_3x3 = []
histos_summed55e_5x5 = []
histos_isolation_ETbin_phi_3x3 = []
histos_isolation_ETbin_phi_5x5 = []
histos_isolation_ETbin_phi_barrel_3x3 = []
histos_isolation_ETbin_phi_barrel_5x5 = []
histos_isolation_ETbin_phi_endcap_3x3 = []
histos_isolation_ETbin_phi_endcap_5x5 = []
histos_isolation_ETbin_eta_3x3 = []
histos_isolation_ETbin_eta_5x5 = []
histos_isolation_ETbin_foldedEta_3x3 = []
histos_isolation_ETbin_foldedEta_5x5 = []
histos_isolation_phi_3x3 = []
histos_isolation_phi_5x5 = []
histos_isolation_phi_barrel_3x3 = []
histos_isolation_phi_barrel_5x5 = []
histos_isolation_phi_endcap_3x3 = []
histos_isolation_phi_endcap_5x5 = []
histos_isolation_eta_3x3 = []
histos_isolation_eta_5x5 = []
histos_isolation_eta_folded_3x3 = []
histos_isolation_eta_folded_5x5 = []
histos_scaleFactor_ETbin_phi_3x3 = []
histos_scaleFactor_ETbin_phi_5x5 = []
histos_scaleFactor_ETbin_phi_barrel_3x3 = []
histos_scaleFactor_ETbin_phi_barrel_5x5 = []
histos_scaleFactor_ETbin_phi_endcap_3x3 = []
histos_scaleFactor_ETbin_phi_endcap_5x5 = []
histos_scaleFactor_ETbin_eta_3x3 = []
histos_scaleFactor_ETbin_eta_5x5 = []
histos_scaleFactor_ETbin_foldedEta_3x3 = []
histos_scaleFactor_ETbin_foldedEta_5x5 = []
histos_scaleFactor_phi_3x3 = []
histos_scaleFactor_phi_5x5 = []
histos_scaleFactor_phi_barrel_3x3 = []
histos_scaleFactor_phi_barrel_5x5 = []
histos_scaleFactor_phi_endcap_3x3 = []
histos_scaleFactor_phi_endcap_5x5 = []
histos_scaleFactor_eta_3x3 = []
histos_scaleFactor_eta_5x5 = []
histos_scaleFactor_eta_folded_3x3 = []
histos_scaleFactor_eta_folded_5x5 = []
for i in range(0,14):
  hname_resolution_3x3 = "histos_resolution_3x3_ETbin%d" % i # Each histogram must have a unique name
  histos_resolution_3x3.append(ROOT.TH1F(hname_resolution_3x3,"",100,-1,4))
  hname_resolution_5x5 = "histos_resolution_5x5_ETbin%d" % i # Each histogram must have a unique name
  histos_resolution_5x5.append(ROOT.TH1F(hname_resolution_5x5,"",100,-1,4))
  hname_genpt_3x3 = "histos_genpt_3x3_ETbin%d" % i
  histos_genpt_3x3.append(ROOT.TH1F(hname_genpt_3x3,"",200,0,200))
  hname_genpt_5x5 = "histos_genpt_5x5_ETbin%d" % i
  histos_genpt_5x5.append(ROOT.TH1F(hname_genpt_5x5,"",200,0,200))
  hname_summed33e_3x3 = "histos_summed33e_3x3_ETbin%d" % i
  histos_summed33e_3x3.append(ROOT.TH1F(hname_summed33e_3x3,"",200,0,200))
  hname_summed33e_5x5 = "histos_summed33e_5x5_ETbin%d" % i
  histos_summed33e_5x5.append(ROOT.TH1F(hname_summed33e_5x5,"",200,0,200))
  hname_summed55e_3x3 = "histos_summed55e_3x3_ETbin%d" % i
  histos_summed55e_3x3.append(ROOT.TH1F(hname_summed55e_3x3,"",200,0,200))
  hname_summed55e_5x5 = "histos_summed55e_5x5_ETbin%d" % i
  histos_summed55e_5x5.append(ROOT.TH1F(hname_summed55e_5x5,"",200,0,200))
  hname_isolation_ETbin_phi_3x3 = "histos_isolation_phi_3x3_ETbin%d" % i # Each histogram must have a unique name
  histos_isolation_ETbin_phi_3x3.append(ROOT.TH1F(hname_isolation_ETbin_phi_3x3,"",72,0,72))
  hname_isolation_ETbin_phi_5x5 = "histos_isolation_phi_5x5_ETbin%d" % i # Each histogram must have a unique name
  histos_isolation_ETbin_phi_5x5.append(ROOT.TH1F(hname_isolation_ETbin_phi_5x5,"",72,0,72))
  hname_isolation_ETbin_phi_barrel_3x3 = "histos_isolation_phi_barrel_3x3_ETbin%d" % i # Each histogram must have a unique name
  histos_isolation_ETbin_phi_barrel_3x3.append(ROOT.TH1F(hname_isolation_ETbin_phi_barrel_3x3,"",72,0,72))
  hname_isolation_ETbin_phi_barrel_5x5 = "histos_isolation_phi_barrel_5x5_ETbin%d" % i # Each histogram must have a unique name
  histos_isolation_ETbin_phi_barrel_5x5.append(ROOT.TH1F(hname_isolation_ETbin_phi_barrel_5x5,"",72,0,72))
  hname_isolation_ETbin_phi_endcap_3x3 = "histos_isolation_phi_endcap_3x3_ETbin%d" % i # Each histogram must have a unique name
  histos_isolation_ETbin_phi_endcap_3x3.append(ROOT.TH1F(hname_isolation_ETbin_phi_endcap_3x3,"",72,0,72))
  hname_isolation_ETbin_phi_endcap_5x5 = "histos_isolation_phi_endcap_5x5_ETbin%d" % i # Each histogram must have a unique name
  histos_isolation_ETbin_phi_endcap_5x5.append(ROOT.TH1F(hname_isolation_ETbin_phi_endcap_5x5,"",72,0,72))
  hname_isolation_ETbin_eta_3x3 = "histos_isolation_eta_3x3_ETbin%d" % i # Each histogram must have a unique name
  histos_isolation_ETbin_eta_3x3.append(ROOT.TH1F(hname_isolation_ETbin_eta_3x3,"",56,0,56))
  hname_isolation_ETbin_eta_5x5 = "histos_isolation_eta_5x5_ETbin%d" % i # Each histogram must have a unique name
  histos_isolation_ETbin_eta_5x5.append(ROOT.TH1F(hname_isolation_ETbin_eta_5x5,"",56,0,56))
  hname_isolation_ETbin_foldedEta_3x3 = "histos_isolation_foldedEta_3x3_ETbin%d" % i # Each histogram must have a unique name
  histos_isolation_ETbin_foldedEta_3x3.append(ROOT.TH1F(hname_isolation_ETbin_foldedEta_3x3,"",28,0,28))
  hname_isolation_ETbin_foldedEta_5x5 = "histos_isolation_foldedEta_5x5_ETbin%d" % i # Each histogram must have a unique name
  histos_isolation_ETbin_foldedEta_5x5.append(ROOT.TH1F(hname_isolation_ETbin_foldedEta_5x5,"",28,0,28))
  histos_isolation_phi_3x3.append([])
  histos_isolation_phi_5x5.append([])
  histos_isolation_phi_barrel_3x3.append([])
  histos_isolation_phi_barrel_5x5.append([])
  histos_isolation_phi_endcap_3x3.append([])
  histos_isolation_phi_endcap_5x5.append([])
  histos_isolation_eta_3x3.append([])
  histos_isolation_eta_5x5.append([])
  histos_isolation_eta_folded_3x3.append([])
  histos_isolation_eta_folded_5x5.append([])
  hname_scaleFactor_ETbin_phi_3x3 = "histos_scaleFactor_phi_3x3_ETbin%d" % i # Each histogram must have a unique name
  histos_scaleFactor_ETbin_phi_3x3.append(ROOT.TH1F(hname_scaleFactor_ETbin_phi_3x3,"",72,0,72))
  hname_scaleFactor_ETbin_phi_5x5 = "histos_scaleFactor_phi_5x5_ETbin%d" % i # Each histogram must have a unique name
  histos_scaleFactor_ETbin_phi_5x5.append(ROOT.TH1F(hname_scaleFactor_ETbin_phi_5x5,"",72,0,72))
  hname_scaleFactor_ETbin_phi_barrel_3x3 = "histos_scaleFactor_phi_barrel_3x3_ETbin%d" % i # Each histogram must have a unique name
  histos_scaleFactor_ETbin_phi_barrel_3x3.append(ROOT.TH1F(hname_scaleFactor_ETbin_phi_barrel_3x3,"",72,0,72))
  hname_scaleFactor_ETbin_phi_barrel_5x5 = "histos_scaleFactor_phi_barrel_5x5_ETbin%d" % i # Each histogram must have a unique name
  histos_scaleFactor_ETbin_phi_barrel_5x5.append(ROOT.TH1F(hname_scaleFactor_ETbin_phi_barrel_5x5,"",72,0,72))
  hname_scaleFactor_ETbin_phi_endcap_3x3 = "histos_scaleFactor_phi_endcap_3x3_ETbin%d" % i # Each histogram must have a unique name
  histos_scaleFactor_ETbin_phi_endcap_3x3.append(ROOT.TH1F(hname_scaleFactor_ETbin_phi_endcap_3x3,"",72,0,72))
  hname_scaleFactor_ETbin_phi_endcap_5x5 = "histos_scaleFactor_phi_endcap_5x5_ETbin%d" % i # Each histogram must have a unique name
  histos_scaleFactor_ETbin_phi_endcap_5x5.append(ROOT.TH1F(hname_scaleFactor_ETbin_phi_endcap_5x5,"",72,0,72))
  hname_scaleFactor_ETbin_eta_3x3 = "histos_scaleFactor_eta_3x3_ETbin%d" % i # Each histogram must have a unique name
  histos_scaleFactor_ETbin_eta_3x3.append(ROOT.TH1F(hname_scaleFactor_ETbin_eta_3x3,"",56,0,56))
  hname_scaleFactor_ETbin_eta_5x5 = "histos_scaleFactor_eta_5x5_ETbin%d" % i # Each histogram must have a unique name
  histos_scaleFactor_ETbin_eta_5x5.append(ROOT.TH1F(hname_scaleFactor_ETbin_eta_5x5,"",56,0,56))
  hname_scaleFactor_ETbin_foldedEta_3x3 = "histos_scaleFactor_foldedEta_3x3_ETbin%d" % i # Each histogram must have a unique name
  histos_scaleFactor_ETbin_foldedEta_3x3.append(ROOT.TH1F(hname_scaleFactor_ETbin_foldedEta_3x3,"",28,0,28))
  hname_scaleFactor_ETbin_foldedEta_5x5 = "histos_scaleFactor_foldedEta_5x5_ETbin%d" % i # Each histogram must have a unique name
  histos_scaleFactor_ETbin_foldedEta_5x5.append(ROOT.TH1F(hname_scaleFactor_ETbin_foldedEta_5x5,"",28,0,28))
  histos_scaleFactor_phi_3x3.append([])
  histos_scaleFactor_phi_5x5.append([])
  histos_scaleFactor_phi_barrel_3x3.append([])
  histos_scaleFactor_phi_barrel_5x5.append([])
  histos_scaleFactor_phi_endcap_3x3.append([])
  histos_scaleFactor_phi_endcap_5x5.append([])
  histos_scaleFactor_eta_3x3.append([])
  histos_scaleFactor_eta_5x5.append([])
  histos_scaleFactor_eta_folded_3x3.append([])
  histos_scaleFactor_eta_folded_5x5.append([])
  for j in range(0,72):
    hname_isolation_phi_3x3 = "histos_isolation_phi_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_isolation_phi_3x3[i].append(ntuple_file.Get(hname_isolation_phi_3x3))
    hname_isolation_phi_5x5 = "histos_isolation_phi_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_isolation_phi_5x5[i].append(ntuple_file.Get(hname_isolation_phi_5x5))
    hname_scaleFactor_phi_3x3 = "histos_scaleFactor_phi_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_phi_3x3[i].append(ntuple_file.Get(hname_scaleFactor_phi_3x3))
    hname_scaleFactor_phi_5x5 = "histos_scaleFactor_phi_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_phi_5x5[i].append(ntuple_file.Get(hname_scaleFactor_phi_5x5))
    hname_isolation_phi_barrel_3x3 = "histos_isolation_phi_barrel_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_isolation_phi_barrel_3x3[i].append(ntuple_file.Get(hname_isolation_phi_barrel_3x3))
    hname_isolation_phi_barrel_5x5 = "histos_isolation_phi_barrel_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_isolation_phi_barrel_5x5[i].append(ntuple_file.Get(hname_isolation_phi_barrel_5x5))
    hname_scaleFactor_phi_barrel_3x3 = "histos_scaleFactor_phi_barrel_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_phi_barrel_3x3[i].append(ntuple_file.Get(hname_scaleFactor_phi_barrel_3x3))
    hname_scaleFactor_phi_barrel_5x5 = "histos_scaleFactor_phi_barrel_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_phi_barrel_5x5[i].append(ntuple_file.Get(hname_scaleFactor_phi_barrel_5x5))
    hname_isolation_phi_endcap_3x3 = "histos_isolation_phi_endcap_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_isolation_phi_endcap_3x3[i].append(ntuple_file.Get(hname_isolation_phi_endcap_3x3))
    hname_isolation_phi_endcap_5x5 = "histos_isolation_phi_endcap_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_isolation_phi_endcap_5x5[i].append(ntuple_file.Get(hname_isolation_phi_endcap_5x5))
    hname_scaleFactor_phi_endcap_3x3 = "histos_scaleFactor_phi_endcap_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_phi_endcap_3x3[i].append(ntuple_file.Get(hname_scaleFactor_phi_endcap_3x3))
    hname_scaleFactor_phi_endcap_5x5 = "histos_scaleFactor_phi_endcap_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_phi_endcap_5x5[i].append(ntuple_file.Get(hname_scaleFactor_phi_endcap_5x5))
  for j in range(0,56):
    hname_isolation_eta_3x3 = "histos_isolation_eta_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_isolation_eta_3x3[i].append(ntuple_file.Get(hname_isolation_eta_3x3))
    hname_isolation_eta_5x5 = "histos_isolation_eta_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_isolation_eta_5x5[i].append(ntuple_file.Get(hname_isolation_eta_5x5))
    hname_scaleFactor_eta_3x3 = "histos_scaleFactor_eta_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_eta_3x3[i].append(ntuple_file.Get(hname_scaleFactor_eta_3x3))
    hname_scaleFactor_eta_5x5 = "histos_scaleFactor_eta_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_eta_5x5[i].append(ntuple_file.Get(hname_scaleFactor_eta_5x5))
  for j in range(0,28):
    hname_isolation_eta_folded_3x3 = "histos_isolation_eta_folded_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_isolation_eta_folded_3x3[i].append(ntuple_file.Get(hname_isolation_eta_folded_3x3))
    hname_isolation_eta_folded_5x5 = "histos_isolation_eta_folded_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_isolation_eta_folded_5x5[i].append(ntuple_file.Get(hname_isolation_eta_folded_5x5))
    hname_scaleFactor_eta_folded_3x3 = "histos_scaleFactor_eta_folded_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_eta_folded_3x3[i].append(ntuple_file.Get(hname_scaleFactor_eta_folded_3x3))
    hname_scaleFactor_eta_folded_5x5 = "histos_scaleFactor_eta_folded_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_eta_folded_5x5[i].append(ntuple_file.Get(hname_scaleFactor_eta_folded_5x5))

canvas = ROOT.TCanvas("asdf", "adsf", 800, 800)
pad1 = ROOT.TPad("pad1","",0,0,1,1)
pad1.Draw()
pad1.cd()

last_written = [1.000000]*28

for ETbin in range(0,13):
    for phi in range(0,72):
        Mean_isolation_3x3 =histos_isolation_phi_3x3[ETbin][phi].GetMean()
        MeanError_isolation_3x3 =histos_isolation_phi_3x3[ETbin][phi].GetMeanError()
        Mean_isolation_5x5 =histos_isolation_phi_5x5[ETbin][phi].GetMean()
        MeanError_isolation_5x5 =histos_isolation_phi_5x5[ETbin][phi].GetMeanError()
        histos_isolation_ETbin_phi_3x3[ETbin].SetBinContent(phi+1,Mean_isolation_3x3)
        histos_isolation_ETbin_phi_3x3[ETbin].SetBinError(phi+1,MeanError_isolation_3x3)
        histos_isolation_ETbin_phi_5x5[ETbin].SetBinContent(phi+1,Mean_isolation_5x5)
        histos_isolation_ETbin_phi_5x5[ETbin].SetBinError(phi+1,MeanError_isolation_5x5)
        Mean_scaleFactor_3x3 =histos_scaleFactor_phi_3x3[ETbin][phi].GetMean()
        MeanError_scaleFactor_3x3 =histos_scaleFactor_phi_3x3[ETbin][phi].GetMeanError()
        Mean_scaleFactor_5x5 =histos_scaleFactor_phi_5x5[ETbin][phi].GetMean()
        MeanError_scaleFactor_5x5 =histos_scaleFactor_phi_5x5[ETbin][phi].GetMeanError()
        histos_scaleFactor_ETbin_phi_3x3[ETbin].SetBinContent(phi+1,Mean_scaleFactor_3x3)
        histos_scaleFactor_ETbin_phi_3x3[ETbin].SetBinError(phi+1,MeanError_scaleFactor_3x3)
        histos_scaleFactor_ETbin_phi_5x5[ETbin].SetBinContent(phi+1,Mean_scaleFactor_5x5)
        histos_scaleFactor_ETbin_phi_5x5[ETbin].SetBinError(phi+1,MeanError_scaleFactor_5x5)
        
        Mean_isolation_3x3 =histos_isolation_phi_barrel_3x3[ETbin][phi].GetMean()
        MeanError_isolation_3x3 =histos_isolation_phi_barrel_3x3[ETbin][phi].GetMeanError()
        Mean_isolation_5x5 =histos_isolation_phi_barrel_5x5[ETbin][phi].GetMean()
        MeanError_isolation_5x5 =histos_isolation_phi_barrel_5x5[ETbin][phi].GetMeanError()
        histos_isolation_ETbin_phi_barrel_3x3[ETbin].SetBinContent(phi+1,Mean_isolation_3x3)
        histos_isolation_ETbin_phi_barrel_3x3[ETbin].SetBinError(phi+1,MeanError_isolation_3x3)
        histos_isolation_ETbin_phi_barrel_5x5[ETbin].SetBinContent(phi+1,Mean_isolation_5x5)
        histos_isolation_ETbin_phi_barrel_5x5[ETbin].SetBinError(phi+1,MeanError_isolation_5x5)
        Mean_scaleFactor_5x5 =histos_scaleFactor_phi_barrel_5x5[ETbin][phi].GetMean()
        MeanError_scaleFactor_5x5 =histos_scaleFactor_phi_barrel_5x5[ETbin][phi].GetMeanError()
        ###################################################################################################
        ### Mode ###
        # rms = histos_scaleFactor_phi_barrel_3x3[ETbin][phi].GetRMS()
        # if rms > 0.2:
        #   histos_scaleFactor_phi_barrel_3x3[ETbin][phi].Rebin(2)
        #   rms = histos_scaleFactor_phi_barrel_3x3[ETbin][phi].GetRMS()
        # tf1 = ROOT.TF1("landaugausfunction", ROOT.langaufun, 0, 5, 4)
        # peakpos = histos_scaleFactor_phi_barrel_3x3[ETbin][phi].GetXaxis().GetBinCenter(histos_scaleFactor_phi_barrel_3x3[ETbin][phi].GetMaximumBin())
        # startwidth = rms / 5.0
        # startmpv = peakpos
        # startnorm = histos_scaleFactor_phi_barrel_3x3[ETbin][phi].Integral()
        # startsigma = rms / 10.0
        # tf1.SetParNames("LandauWidth","LandauMPV","Normalisation","GaussianSigma")
        # tf1.SetParameters(startwidth, startmpv, startnorm, startsigma)
        # histos_scaleFactor_phi_barrel_3x3[ETbin][phi].Fit(tf1, "0L", "", 0.6, 3.0)
        # Mean_scaleFactor_3x3 = float(tf1.GetParameter(1))
        # MeanError_scaleFactor_3x3 = float(tf1.GetParError(1))
        # if math.isnan(Mean_scaleFactor_3x3) or math.isnan(MeanError_scaleFactor_3x3):
        #   Mean_scaleFactor_3x3 = -9999.9
        #   MeanError_scaleFactor_3x3 = 999.9
        # if float(tf1.GetParameter(0))/float(tf1.GetParameter(3)) < 0.034 or float(MeanError_scaleFactor_3x3) > 0.03:
        #   tf1_alt = ROOT.TF1("gaus","[2]*TMath::Gaus(x,[0],[1])",0.0,3.0)
        #   startmean = peakpos
        #   startsigma = histos_scaleFactor_phi_barrel_3x3[ETbin][phi].GetRMS()
        #   startnorm = histos_scaleFactor_phi_barrel_3x3[ETbin][phi].Integral(histos_scaleFactor_phi_barrel_3x3[ETbin][phi].GetXaxis().FindBin(0.6),histos_scaleFactor_phi_barrel_3x3[ETbin][phi].GetXaxis().FindBin(3.0))
        #   tf1_alt.SetParNames("GausMean","GausSigma","GausNorm")
        #   tf1_alt.SetParameters(startmean,startsigma,startnorm)
        #   histos_scaleFactor_phi_barrel_3x3[ETbin][phi].Fit(tf1_alt,"0L","",startmean-0.2,startmean+0.2)
        #   val = float(tf1_alt.GetParameter(0))
        #   err = float(tf1_alt.GetParError(0))
        #   # if err < MeanError_scaleFactor_3x3 and not math.isnan(val) and not math.isnan(err):
        #   if (abs(val - peakpos) < abs(Mean_scaleFactor_3x3 - peakpos) or (MeanError_scaleFactor_3x3 > 0.05 and err < MeanError_scaleFactor_3x3)) and not math.isnan(val) and not math.isnan(err):
        #     Mean_scaleFactor_3x3 = val
        #     MeanError_scaleFactor_3x3 = err
        #     tf1 = tf1_alt
        #     # Try alternate fit range
        #     tf1_alt.SetParameters(startmean,startsigma,startnorm)
        #     histos_scaleFactor_phi_barrel_3x3[ETbin][phi].Fit(tf1_alt,"0L","",startmean-rms,startmean+rms)
        #     val = float(tf1_alt.GetParameter(0))
        #     err = float(tf1_alt.GetParError(0))
        #     if err < MeanError_scaleFactor_3x3 and not math.isnan(val) and not math.isnan(err):
        #       Mean_scaleFactor_3x3 = val
        #       MeanError_scaleFactor_3x3 = err
        #       tf1 = tf1_alt
        ###################################################################################################
        ### Mean ###
        Mean_scaleFactor_3x3 =histos_scaleFactor_phi_barrel_3x3[ETbin][phi].GetMean()
        MeanError_scaleFactor_3x3 =histos_scaleFactor_phi_barrel_3x3[ETbin][phi].GetMeanError()
        ###################################################################################################
        histos_scaleFactor_ETbin_phi_barrel_3x3[ETbin].SetBinContent(phi+1,Mean_scaleFactor_3x3)
        histos_scaleFactor_ETbin_phi_barrel_3x3[ETbin].SetBinError(phi+1,MeanError_scaleFactor_3x3)
        histos_scaleFactor_ETbin_phi_barrel_5x5[ETbin].SetBinContent(phi+1,Mean_scaleFactor_5x5)
        histos_scaleFactor_ETbin_phi_barrel_5x5[ETbin].SetBinError(phi+1,MeanError_scaleFactor_5x5)
        
        Mean_isolation_3x3 =histos_isolation_phi_endcap_3x3[ETbin][phi].GetMean()
        MeanError_isolation_3x3 =histos_isolation_phi_endcap_3x3[ETbin][phi].GetMeanError()
        Mean_isolation_5x5 =histos_isolation_phi_endcap_5x5[ETbin][phi].GetMean()
        MeanError_isolation_5x5 =histos_isolation_phi_endcap_5x5[ETbin][phi].GetMeanError()
        histos_isolation_ETbin_phi_endcap_3x3[ETbin].SetBinContent(phi+1,Mean_isolation_3x3)
        histos_isolation_ETbin_phi_endcap_3x3[ETbin].SetBinError(phi+1,MeanError_isolation_3x3)
        histos_isolation_ETbin_phi_endcap_5x5[ETbin].SetBinContent(phi+1,Mean_isolation_5x5)
        histos_isolation_ETbin_phi_endcap_5x5[ETbin].SetBinError(phi+1,MeanError_isolation_5x5)
        Mean_scaleFactor_5x5 =histos_scaleFactor_phi_endcap_5x5[ETbin][phi].GetMean()
        MeanError_scaleFactor_5x5 =histos_scaleFactor_phi_endcap_5x5[ETbin][phi].GetMeanError()
        ###################################################################################################
        ### Mode ###
        # rms = histos_scaleFactor_phi_endcap_3x3[ETbin][phi].GetRMS()
        # if rms > 0.2:
        #   histos_scaleFactor_phi_endcap_3x3[ETbin][phi].Rebin(2)
        #   rms = histos_scaleFactor_phi_endcap_3x3[ETbin][phi].GetRMS()
        # tf1 = ROOT.TF1("landaugausfunction", ROOT.langaufun, 0, 5, 4)
        # peakpos = histos_scaleFactor_phi_endcap_3x3[ETbin][phi].GetXaxis().GetBinCenter(histos_scaleFactor_phi_endcap_3x3[ETbin][phi].GetMaximumBin())
        # startwidth = rms / 5.0
        # startmpv = peakpos
        # startnorm = histos_scaleFactor_phi_endcap_3x3[ETbin][phi].Integral()
        # startsigma = rms / 10.0
        # tf1.SetParNames("LandauWidth","LandauMPV","Normalisation","GaussianSigma")
        # tf1.SetParameters(startwidth, startmpv, startnorm, startsigma)
        # histos_scaleFactor_phi_endcap_3x3[ETbin][phi].Fit(tf1, "0L", "", 0.6, 3.0)
        # Mean_scaleFactor_3x3 = float(tf1.GetParameter(1))
        # MeanError_scaleFactor_3x3 = float(tf1.GetParError(1))
        # if math.isnan(Mean_scaleFactor_3x3) or math.isnan(MeanError_scaleFactor_3x3):
        #   Mean_scaleFactor_3x3 = -9999.9
        #   MeanError_scaleFactor_3x3 = 999.9
        # if float(tf1.GetParameter(0))/float(tf1.GetParameter(3)) < 0.034 or float(MeanError_scaleFactor_3x3) > 0.03:
        #   tf1_alt = ROOT.TF1("gaus","[2]*TMath::Gaus(x,[0],[1])",0.0,3.0)
        #   startmean = peakpos
        #   startsigma = histos_scaleFactor_phi_endcap_3x3[ETbin][phi].GetRMS()
        #   startnorm = histos_scaleFactor_phi_endcap_3x3[ETbin][phi].Integral(histos_scaleFactor_phi_endcap_3x3[ETbin][phi].GetXaxis().FindBin(0.6),histos_scaleFactor_phi_endcap_3x3[ETbin][phi].GetXaxis().FindBin(3.0))
        #   tf1_alt.SetParNames("GausMean","GausSigma","GausNorm")
        #   tf1_alt.SetParameters(startmean,startsigma,startnorm)
        #   histos_scaleFactor_phi_endcap_3x3[ETbin][phi].Fit(tf1_alt,"0L","",startmean-0.2,startmean+0.2)
        #   val = float(tf1_alt.GetParameter(0))
        #   err = float(tf1_alt.GetParError(0))
        #   # if err < MeanError_scaleFactor_3x3 and not math.isnan(val) and not math.isnan(err):
        #   if (abs(val - peakpos) < abs(Mean_scaleFactor_3x3 - peakpos) or (MeanError_scaleFactor_3x3 > 0.05 and err < MeanError_scaleFactor_3x3)) and not math.isnan(val) and not math.isnan(err):
        #     Mean_scaleFactor_3x3 = val
        #     MeanError_scaleFactor_3x3 = err
        #     tf1 = tf1_alt
        #     # Try alternate fit range
        #     tf1_alt.SetParameters(startmean,startsigma,startnorm)
        #     histos_scaleFactor_phi_endcap_3x3[ETbin][phi].Fit(tf1_alt,"0L","",startmean-rms,startmean+rms)
        #     val = float(tf1_alt.GetParameter(0))
        #     err = float(tf1_alt.GetParError(0))
        #     if err < MeanError_scaleFactor_3x3 and not math.isnan(val) and not math.isnan(err):
        #       Mean_scaleFactor_3x3 = val
        #       MeanError_scaleFactor_3x3 = err
        #       tf1 = tf1_alt
        ###################################################################################################
        ### Mean ###
        Mean_scaleFactor_3x3 =histos_scaleFactor_phi_endcap_3x3[ETbin][phi].GetMean()
        MeanError_scaleFactor_3x3 =histos_scaleFactor_phi_endcap_3x3[ETbin][phi].GetMeanError()
        ###################################################################################################
        histos_scaleFactor_ETbin_phi_endcap_3x3[ETbin].SetBinContent(phi+1,Mean_scaleFactor_3x3)
        histos_scaleFactor_ETbin_phi_endcap_3x3[ETbin].SetBinError(phi+1,MeanError_scaleFactor_3x3)
        histos_scaleFactor_ETbin_phi_endcap_5x5[ETbin].SetBinContent(phi+1,Mean_scaleFactor_5x5)
        histos_scaleFactor_ETbin_phi_endcap_5x5[ETbin].SetBinError(phi+1,MeanError_scaleFactor_5x5)
    for eta in range(0,56):
        Mean_isolation_3x3 =histos_isolation_eta_3x3[ETbin][eta].GetMean()
        MeanError_isolation_3x3 =histos_isolation_eta_3x3[ETbin][eta].GetMeanError()
        Mean_isolation_5x5 =histos_isolation_eta_5x5[ETbin][eta].GetMean()
        MeanError_isolation_5x5 =histos_isolation_eta_5x5[ETbin][eta].GetMeanError()
        histos_isolation_ETbin_eta_3x3[ETbin].SetBinContent(eta+1,Mean_isolation_3x3)
        histos_isolation_ETbin_eta_3x3[ETbin].SetBinError(eta+1,MeanError_isolation_3x3)
        histos_isolation_ETbin_eta_5x5[ETbin].SetBinContent(eta+1,Mean_isolation_5x5)
        histos_isolation_ETbin_eta_5x5[ETbin].SetBinError(eta+1,MeanError_isolation_5x5)
        Mean_scaleFactor_3x3 =histos_scaleFactor_eta_3x3[ETbin][eta].GetMean()
        MeanError_scaleFactor_3x3 =histos_scaleFactor_eta_3x3[ETbin][eta].GetMeanError()
        Mean_scaleFactor_5x5 =histos_scaleFactor_eta_5x5[ETbin][eta].GetMean()
        MeanError_scaleFactor_5x5 =histos_scaleFactor_eta_5x5[ETbin][eta].GetMeanError()
        histos_scaleFactor_ETbin_eta_3x3[ETbin].SetBinContent(eta+1,Mean_scaleFactor_3x3)
        histos_scaleFactor_ETbin_eta_3x3[ETbin].SetBinError(eta+1,MeanError_scaleFactor_3x3)
        histos_scaleFactor_ETbin_eta_5x5[ETbin].SetBinContent(eta+1,Mean_scaleFactor_5x5)
        histos_scaleFactor_ETbin_eta_5x5[ETbin].SetBinError(eta+1,MeanError_scaleFactor_5x5)
    for foldedEta in range(0,28):
        Mean_isolation_3x3 =histos_isolation_eta_folded_3x3[ETbin][foldedEta].GetMean()
        MeanError_isolation_3x3 =histos_isolation_eta_folded_3x3[ETbin][foldedEta].GetMeanError()
        Mean_isolation_5x5 =histos_isolation_eta_folded_5x5[ETbin][foldedEta].GetMean()
        MeanError_isolation_5x5 =histos_isolation_eta_folded_5x5[ETbin][foldedEta].GetMeanError()
        ### Draw isolation plots ###
        # histos_isolation_eta_folded_3x3[ETbin][foldedEta].SetLineColor(ROOT.kBlack)
        # histos_isolation_eta_folded_3x3[ETbin][foldedEta].SetLineWidth(2)
        # histos_isolation_eta_folded_3x3[ETbin][foldedEta].GetXaxis().SetTitle("3x3-1 Tower Sum [GeV]")
        # histos_isolation_eta_folded_3x3[ETbin][foldedEta].GetYaxis().SetTitle("Events / bin")
        # hist_title = 'ETbin = %d, |ieta| = %d' % (ETbin,foldedEta+1)
        # histos_isolation_eta_folded_3x3[ETbin][foldedEta].SetTitle(hist_title)
        # histos_isolation_eta_folded_3x3[ETbin][foldedEta].Draw("HIST")
        # saveas='%sphoton_isolation_hist_ETbin%s_ieta%s_%s.png' % (saveWhere,ETbin,foldedEta+1,suffix)
        # canvas.SaveAs(saveas)
        histos_isolation_ETbin_foldedEta_3x3[ETbin].SetBinContent(foldedEta+1,Mean_isolation_3x3)
        histos_isolation_ETbin_foldedEta_3x3[ETbin].SetBinError(foldedEta+1,MeanError_isolation_3x3)
        histos_isolation_ETbin_foldedEta_5x5[ETbin].SetBinContent(foldedEta+1,Mean_isolation_5x5)
        histos_isolation_ETbin_foldedEta_5x5[ETbin].SetBinError(foldedEta+1,MeanError_isolation_5x5)
        #############################################################################################
        # ### Mode ###
        rms = histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].GetRMS()
        if rms > 0.2:
          histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].Rebin(2)
          rms = histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].GetRMS()
        tf1 = ROOT.TF1("landaugausfunction", ROOT.langaufun, 0, 5, 4)
        peakpos = histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].GetXaxis().GetBinCenter(histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].GetMaximumBin())
        startwidth = rms / 5.0
        startmpv = peakpos
        startnorm = histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].Integral()
        startsigma = rms / 10.0
        tf1.SetParNames("LandauWidth","LandauMPV","Normalisation","GaussianSigma")
        tf1.SetParameters(startwidth, startmpv, startnorm, startsigma)
        histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].Fit(tf1, "0L", "", 0.6, 3.0)
        Mean_scaleFactor_3x3 = float(tf1.GetParameter(1))
        MeanError_scaleFactor_3x3 = float(tf1.GetParError(1))
        if math.isnan(Mean_scaleFactor_3x3) or math.isnan(MeanError_scaleFactor_3x3):
          Mean_scaleFactor_3x3 = -9999.9
          MeanError_scaleFactor_3x3 = 999.9
        if float(tf1.GetParameter(0))/float(tf1.GetParameter(3)) < 0.034 or float(MeanError_scaleFactor_3x3) > 0.03:
          tf1_alt = ROOT.TF1("gaus","[2]*TMath::Gaus(x,[0],[1])",0.0,3.0)
          startmean = peakpos
          startsigma = histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].GetRMS()
          startnorm = histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].Integral(histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].GetXaxis().FindBin(0.6),histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].GetXaxis().FindBin(3.0))
          tf1_alt.SetParNames("GausMean","GausSigma","GausNorm")
          tf1_alt.SetParameters(startmean,startsigma,startnorm)
          histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].Fit(tf1_alt,"0L","",startmean-0.2,startmean+0.2)
          val = float(tf1_alt.GetParameter(0))
          err = float(tf1_alt.GetParError(0))
          # if err < MeanError_scaleFactor_3x3 and not math.isnan(val) and not math.isnan(err):
          if (abs(val - peakpos) < abs(Mean_scaleFactor_3x3 - peakpos) or (MeanError_scaleFactor_3x3 > 0.05 and err < MeanError_scaleFactor_3x3)) and not math.isnan(val) and not math.isnan(err):
            Mean_scaleFactor_3x3 = val
            MeanError_scaleFactor_3x3 = err
            tf1 = tf1_alt
          # Try alternate fit range
          tf1_alt.SetParameters(startmean,startsigma,startnorm)
          histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].Fit(tf1_alt,"0L","",startmean-rms,startmean+rms)
          val = float(tf1_alt.GetParameter(0))
          err = float(tf1_alt.GetParError(0))
          if (abs(val - peakpos) < abs(Mean_scaleFactor_3x3 - peakpos) or (MeanError_scaleFactor_3x3 > 0.05 and err < MeanError_scaleFactor_3x3)) and not math.isnan(val) and not math.isnan(err):
            Mean_scaleFactor_3x3 = val
            MeanError_scaleFactor_3x3 = err
            tf1 = tf1_alt
        # sf_errors.append('ETbin:%d, foldedEta:%d, err:%f'%(ETbin,foldedEta,MeanError_scaleFactor_3x3))
        ### Draw mode plots ###
        histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].SetLineColor(ROOT.kBlack)
        histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].SetLineWidth(2)
        histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].GetXaxis().SetTitle("Gen. Photon pT / 3x3 ECAL ET")
        histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].GetYaxis().SetTitle("Events / bin")
        hist_title = 'ETbin = %d, |ieta| = %d' % (ETbin,foldedEta+1)
        histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].SetTitle(hist_title)
        tf1.Draw()
        tf1.SetLineColor(ROOT.kRed)
        tf1.SetLineWidth(2)
        histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].Draw("HIST")
        tf1.Draw("SAME")
        saveas='%sphoton_SF_hist_ETbin%s_ieta%s_%s.png' % (saveWhere,ETbin,foldedEta+1,suffix)
        canvas.SaveAs(saveas)
        #############################################################################################
        ### Mean ###
        # Mean_scaleFactor_3x3 =histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].GetMean()
        # MeanError_scaleFactor_3x3 =histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].GetMeanError()
        # histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].SetLineColor(ROOT.kBlack)
        # histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].SetLineWidth(2)
        # histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].GetXaxis().SetTitle("Gen. Photon pT / 3x3 ECAL ET")
        # histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].GetYaxis().SetTitle("Events / bin")
        # hist_title = 'ETbin = %d, |ieta| = %d' % (ETbin,foldedEta+1)
        # histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].SetTitle(hist_title)
        # histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].Draw("HIST")
        # saveas='%sphoton_SF_hist_ETbin%s_ieta%s_%s.png' % (saveWhere,ETbin,foldedEta+1,suffix)
        # canvas.SaveAs(saveas)
        #############################################################################################
        Mean_scaleFactor_5x5 =histos_scaleFactor_eta_folded_5x5[ETbin][foldedEta].GetMean()
        MeanError_scaleFactor_5x5 =histos_scaleFactor_eta_folded_5x5[ETbin][foldedEta].GetMeanError()
        histos_scaleFactor_ETbin_foldedEta_3x3[ETbin].SetBinContent(foldedEta+1,Mean_scaleFactor_3x3)
        histos_scaleFactor_ETbin_foldedEta_3x3[ETbin].SetBinError(foldedEta+1,MeanError_scaleFactor_3x3)
        histos_scaleFactor_ETbin_foldedEta_5x5[ETbin].SetBinContent(foldedEta+1,Mean_scaleFactor_5x5)
        histos_scaleFactor_ETbin_foldedEta_5x5[ETbin].SetBinError(foldedEta+1,MeanError_scaleFactor_5x5)
        if ETbin == 0 and foldedEta == 0:
            text_file.write("   float ecal[364] = {")
        else:
            text_file.write(", ")
        if Mean_scaleFactor_3x3 < 1.0 or math.isnan(Mean_scaleFactor_3x3):
            text_file.write("%f" % last_written[foldedEta])
        else:
            text_file.write("%f" % Mean_scaleFactor_3x3)
            last_written[foldedEta] = Mean_scaleFactor_3x3
        if ETbin == 12 and foldedEta == 27:
            text_file.write("};")

for ETbin in range(0,13):
  histos_scaleFactor_ETbin_foldedEta_3x3[ETbin].GetXaxis().SetTitle("Photon TPG iEta")
  histos_scaleFactor_ETbin_foldedEta_3x3[ETbin].GetXaxis().SetRangeUser(0,28) # Eta range
  histos_scaleFactor_ETbin_foldedEta_3x3[ETbin].GetYaxis().SetTitle("GenPt/TriggerEt")
  histos_scaleFactor_ETbin_foldedEta_3x3[ETbin].GetYaxis().SetTitleOffset(1.1)
  histos_scaleFactor_ETbin_foldedEta_3x3[ETbin].GetYaxis().SetRangeUser(0.7,2.1) # Scale factor
  histos_scaleFactor_ETbin_foldedEta_3x3[ETbin].SetTitle('GenPt/TPG_ECAL_ET vs TPG iEta')
  histos_scaleFactor_ETbin_foldedEta_3x3[ETbin].SetMarkerStyle(23)
  histos_scaleFactor_ETbin_foldedEta_3x3[ETbin].Draw("pE1")
  saveas='%sphoton_SF_%s_%s_etbin%d.png' % (saveWhere,squaresize,suffix,ETbin)
  canvas.SaveAs(saveas)

histos_orig = []
histos = []
for ETbin in range(0,13):
  if squaresize == '3x3':
    if suffix[-len('_iphi'):] == '_iphi':
      histos.append(histos_scaleFactor_ETbin_phi_3x3[ETbin])
    elif suffix[-len('_iphi_barrel'):] == '_iphi_barrel':
      histos.append(histos_scaleFactor_ETbin_phi_barrel_3x3[ETbin])
    elif suffix[-len('_iphi_endcap'):] == '_iphi_endcap':
      histos.append(histos_scaleFactor_ETbin_phi_endcap_3x3[ETbin])
    elif suffix[-len('_isolation'):] == '_isolation':
      histos.append(histos_isolation_ETbin_foldedEta_3x3[ETbin])
    elif suffix[-len('_unfolded'):] == '_unfolded':
      histos_orig.append(histos_scaleFactor_ETbin_eta_3x3[ETbin])
      hname_new = 'hist_ETbin%i_trueieta' % ETbin
      histos.append(ROOT.TH1F(hname_new,"",58,-29,29))
    else:
      histos.append(histos_scaleFactor_ETbin_foldedEta_3x3[ETbin])
  elif squaresize == '5x5':
    if suffix[-len('_iphi'):] == '_iphi':
      histos.append(histos_scaleFactor_ETbin_phi_5x5[ETbin])
    elif suffix[-len('_iphi_barrel'):] == '_iphi_barrel':
      histos.append(histos_scaleFactor_ETbin_phi_barrel_5x5[ETbin])
    elif suffix[-len('_iphi_endcap'):] == '_iphi_endcap':
      histos.append(histos_scaleFactor_ETbin_phi_endcap_5x5[ETbin])
    elif suffix[-len('_isolation'):] == '_isolation':
      histos.append(histos_isolation_ETbin_foldedEta_5x5[ETbin])
    elif suffix[-len('_unfolded'):] == '_unfolded':
      histos_orig.append(histos_scaleFactor_ETbin_eta_5x5[ETbin])
      hname_new = 'hist_ETbin%i_trueieta' % ETbin
      histos.append(ROOT.TH1F(hname_new,"",58,-29,29))
    else:
      histos.append(histos_scaleFactor_ETbin_foldedEta_5x5[ETbin])

if suffix[-len('_unfolded'):] == '_unfolded':
  for i in range(0,13):
    for ieta in range(-28,0):
      histos[i].SetBinContent(histos[i].GetXaxis().FindBin(float(ieta)+0.5),histos_orig[i].GetBinContent(ieta+29))
      histos[i].SetBinError(histos[i].GetXaxis().FindBin(float(ieta)+0.5),histos_orig[i].GetBinError(ieta+29))
    for ieta in range(1,29):
      histos[i].SetBinContent(histos[i].GetXaxis().FindBin(float(ieta)-0.5),histos_orig[i].GetBinContent(ieta+28))
      histos[i].SetBinError(histos[i].GetXaxis().FindBin(float(ieta)-0.5),histos_orig[i].GetBinError(ieta+28))

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
  histos[i].GetXaxis().SetTitle("Photon TP iEta")
  if suffix[-len('_iphi'):] == '_iphi' or suffix[-len('_iphi_barrel'):] == '_iphi_barrel' or suffix[-len('_iphi_endcap'):] == '_iphi_endcap':
    histos[i].GetXaxis().SetTitle("Photon TP iPhi")
  histos[i].GetXaxis().SetRangeUser(0,28) # Eta range
  if suffix[-len('_iphi'):] == '_iphi' or suffix[-len('_iphi_barrel'):] == '_iphi_barrel' or suffix[-len('_iphi_endcap'):] == '_iphi_endcap':
    histos[i].GetXaxis().SetRangeUser(0,72) # Phi range
  elif suffix[-len('_unfolded'):] == '_unfolded':
    histos[i].GetXaxis().SetRangeUser(-28,28)
  histos[i].GetYaxis().SetTitle("GenPt/TriggerEt")
  if suffix[-len('_isolation'):] == '_isolation':
    histos[i].GetYaxis().SetTitle("3x3-1 Tower Energy [GeV]")
  histos[i].GetYaxis().SetTitleOffset(1.1)
  histos[i].GetYaxis().SetRangeUser(0.7,2.1) # Scale factor
  if suffix[-len('_isolation'):] == '_isolation':
    histos[i].GetYaxis().SetRangeUser(0.0,6.0) # Isolation
    if suffix[-len('_fullrange_isolation'):] == '_fullrange_isolation':
      histos[i].GetYaxis().SetRangeUser(0.0,70.0) # To get the full range for ieta=27,28
  histos[i].SetTitle('GenPt/TPG_ECAL_ET vs TPG iEta')
  if suffix[-len('_iphi'):] == '_iphi' or suffix[-len('_iphi_barrel'):] == '_iphi_barrel' or suffix[-len('_iphi_endcap'):] == '_iphi_endcap':
    histos[i].SetTitle('GenPt/TPG_ECAL_ET vs TPG iPhi')
  elif suffix[-len('_isolation'):] == '_isolation':
    histos[i].SetTitle('3x3-1 vs TPG iEta')
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

legend1 = ROOT.TLegend(0.72, 0.6, 0.99, 0.99, "ECAL TPG Et", "brNDC")
if suffix[-len('_isolation'):] == '_isolation':
  legend1 = ROOT.TLegend(0.17, 0.55, 0.39, 0.85, "ECAL TPG Et", "brNDC") # Isolation
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
saveas='%sphoton_SF_%s_%s.png' % (saveWhere,squaresize,suffix)
canvas.SaveAs(saveas)
