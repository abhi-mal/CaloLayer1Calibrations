from __future__ import division
#from decimal import *
from sys import argv, exit, stdout, stderr
import sys
import ROOT
import os
import math

if len(argv) != 6:
   print 'ERROR: Incorrect number of arguments provided'
   print 'Usage: python computeHCALcalibs_MC.py input<file or folder> suffix TPGVeto_cut start_index end_index_plus_1'
   exit(1)

suffix = argv[2]

TPGVeto_cut = float(argv[3])

start_index = int(argv[4])
end_index_plus_1 = int(argv[5])
if start_index < 0:
  print 'start_index must be nonnegative'
  exit(1)
if end_index_plus_1 < 0:
  print 'end_index_plus_1 must be nonnegative'
  exit(1)
if end_index_plus_1 < start_index:
  print 'end_index_plus_1 cannot be less than start_index'
  exit(1)

text_file = open("hcalcalibs_MC_"+suffix+"_filerange"+str(start_index)+"to"+str(end_index_plus_1)+".txt","w")
   
########### MAke Hist arrays #########
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
    histos_isolation_phi_3x3[i].append( ROOT.TH1F(hname_isolation_phi_3x3,"",100,0,5) )
    hname_isolation_phi_5x5 = "histos_isolation_phi_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_isolation_phi_5x5[i].append( ROOT.TH1F(hname_isolation_phi_5x5,"",100,0,5) )
    hname_scaleFactor_phi_3x3 = "histos_scaleFactor_phi_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_phi_3x3[i].append( ROOT.TH1F(hname_scaleFactor_phi_3x3,"",100,0,5) )
    hname_scaleFactor_phi_5x5 = "histos_scaleFactor_phi_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_phi_5x5[i].append( ROOT.TH1F(hname_scaleFactor_phi_5x5,"",100,0,5) )
    hname_isolation_phi_barrel_3x3 = "histos_isolation_phi_barrel_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_isolation_phi_barrel_3x3[i].append( ROOT.TH1F(hname_isolation_phi_barrel_3x3,"",4000,0,200) )
    hname_isolation_phi_barrel_5x5 = "histos_isolation_phi_barrel_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_isolation_phi_barrel_5x5[i].append( ROOT.TH1F(hname_isolation_phi_barrel_5x5,"",4000,0,200) )
    hname_scaleFactor_phi_barrel_3x3 = "histos_scaleFactor_phi_barrel_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_phi_barrel_3x3[i].append( ROOT.TH1F(hname_scaleFactor_phi_barrel_3x3,"",100,0,5) )
    hname_scaleFactor_phi_barrel_5x5 = "histos_scaleFactor_phi_barrel_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_phi_barrel_5x5[i].append( ROOT.TH1F(hname_scaleFactor_phi_barrel_5x5,"",100,0,5) )
    hname_isolation_phi_endcap_3x3 = "histos_isolation_phi_endcap_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_isolation_phi_endcap_3x3[i].append( ROOT.TH1F(hname_isolation_phi_endcap_3x3,"",4000,0,200) )
    hname_isolation_phi_endcap_5x5 = "histos_isolation_phi_endcap_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_isolation_phi_endcap_5x5[i].append( ROOT.TH1F(hname_isolation_phi_endcap_5x5,"",4000,0,200) )
    hname_scaleFactor_phi_endcap_3x3 = "histos_scaleFactor_phi_endcap_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_phi_endcap_3x3[i].append( ROOT.TH1F(hname_scaleFactor_phi_endcap_3x3,"",100,0,5) )
    hname_scaleFactor_phi_endcap_5x5 = "histos_scaleFactor_phi_endcap_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_phi_endcap_5x5[i].append( ROOT.TH1F(hname_scaleFactor_phi_endcap_5x5,"",100,0,5) )
  for j in range(0,56):
    hname_isolation_eta_3x3 = "histos_isolation_eta_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_isolation_eta_3x3[i].append( ROOT.TH1F(hname_isolation_eta_3x3,"",4000,0,200) )
    hname_isolation_eta_5x5 = "histos_isolation_eta_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_isolation_eta_5x5[i].append( ROOT.TH1F(hname_isolation_eta_5x5,"",4000,0,200) )
    hname_scaleFactor_eta_3x3 = "histos_scaleFactor_eta_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_eta_3x3[i].append( ROOT.TH1F(hname_scaleFactor_eta_3x3,"",100,0,5) )
    hname_scaleFactor_eta_5x5 = "histos_scaleFactor_eta_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_eta_5x5[i].append( ROOT.TH1F(hname_scaleFactor_eta_5x5,"",100,0,5) )
  for j in range(0,28):
    hname_isolation_eta_folded_3x3 = "histos_isolation_eta_folded_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_isolation_eta_folded_3x3[i].append( ROOT.TH1F(hname_isolation_eta_folded_3x3,"",4000,0,200) )
    hname_isolation_eta_folded_5x5 = "histos_isolation_eta_folded_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_isolation_eta_folded_5x5[i].append( ROOT.TH1F(hname_isolation_eta_folded_5x5,"",4000,0,200) )
    hname_scaleFactor_eta_folded_3x3 = "histos_scaleFactor_eta_folded_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_eta_folded_3x3[i].append( ROOT.TH1F(hname_scaleFactor_eta_folded_3x3,"",100,0,5) )
    hname_scaleFactor_eta_folded_5x5 = "histos_scaleFactor_eta_folded_5x5_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_eta_folded_5x5[i].append( ROOT.TH1F(hname_scaleFactor_eta_folded_5x5,"",100,0,5) )

# Converts tpgeta in [0,55] to foldedEta in [0,27]
def foldtpgeta(tpgeta):
  foldedEta = -1
  if tpgeta >= 28 and tpgeta < 56:
    foldedEta = tpgeta - 28
  elif tpgeta >= 0 and tpgeta < 28:
    foldedEta = 27 - tpgeta
  return foldedEta

n_events = 0
ETbincounts = [0]*15
phicounts = [0]*72
phicounts_passing = [0]*72
etacounts = [0]*56
etacounts_passing = [0]*56
foldedEtacounts = [0]*28
foldedEtacounts_passing = [0]*28

# Run on a single file
#infile = argv[1]
#ntuple_file = ROOT.TFile(infile)
infolder = argv[1]
if infolder[-1:] != '/':
  infolder += '/'
infiles = os.listdir(infolder)
#max_Nfiles = min(10,len(infiles))
max_Nfiles = min(end_index_plus_1-start_index,len(infiles)-start_index)
if max_Nfiles < 0:
  max_Nfiles = 0
print ('Running over %d files' % max_Nfiles)
for infile_index in range(start_index,start_index+max_Nfiles):
  infile = infiles[infile_index]
  if infile[-len('.root'):] != '.root':
    print "Skipping %s" % infile
  else:
    print "Running on file %s" % infile
    ntuple_file = ROOT.TFile(infolder+infile)
    # Indent what follows to start at the same level as ntuple_file
    ntuples = ntuple_file.Get("tree/matched")
    for event in ntuples:
      n_events += 1
      gen=event.gen_pt
      eta = event.gen_ieta
      phi = event.gen_iphi
      l1_center_h = event.l1_center_h
      l1_center_e = event.l1_center_e
      l1_summed33_e = event.l1_summed33_e
      l1_summed55_e = event.l1_summed55_e
      l1_summed33_h = event.l1_summed33_h
      l1_summed55_h = event.l1_summed55_h
      ETbin = -1
      if l1_center_h >= 3 and l1_center_h < 15:
        ETbin = int(math.floor(l1_center_h/3)) - 1
      elif l1_center_h >= 15 and l1_center_h < 45:
        ETbin = int(math.floor(l1_center_h/5)) + 1
      elif l1_center_h >= 45 and l1_center_h < 55:
        ETbin = 10
      elif l1_center_h >= 55 and l1_center_h < 70:
        ETbin = 11
      elif l1_center_h >= 70 and l1_center_h < 90:
        ETbin = 12
      elif l1_center_h >= 90:
        ETbin = 13
      ETbincounts[ETbin+1] += 1
      if ETbin>=0 and gen>0 and eta>=0 and eta<56 and phi>=0 and phi<72 and l1_center_e<125 and l1_center_h<125:
         foldedEta = foldtpgeta(eta)
         phicounts[phi] += 1
         etacounts[eta] += 1
         foldedEtacounts[foldedEta] += 1
         TPGVeto3x3 = 0.0
         TPGVeto5x5 = 0.0
         if l1_summed33_h > 3:
             TPGVeto3x3 = l1_center_h/l1_summed33_h
         if l1_summed55_h > 3:
             TPGVeto5x5 = l1_center_h/l1_summed55_h
         if foldedEta>=20 and foldedEta<28:
             TPGVeto3x3 *= 2
             TPGVeto5x5 *= 2
         resolution_3x3 = (l1_summed33_h-gen)/gen
         resolution_5x5 = (l1_summed55_h-gen)/gen
         if TPGVeto3x3>TPGVeto_cut and (l1_summed33_e-l1_center_e)<3*125 and (l1_summed33_h-l1_center_h)<3*125:
            isolation = l1_summed33_h - l1_center_h
            SF = gen/(event.sumCorr33_e+l1_summed33_h)
            histos_resolution_3x3[ETbin].Fill(resolution_3x3)
            histos_genpt_3x3[ETbin].Fill(event.gen_pt)
            histos_summed33e_3x3[ETbin].Fill(event.l1_summed33_h)
            histos_summed55e_3x3[ETbin].Fill(event.l1_summed55_h)
            histos_isolation_eta_3x3[ETbin][eta].Fill(isolation)
            histos_scaleFactor_eta_3x3[ETbin][eta].Fill(SF)
            histos_isolation_eta_folded_3x3[ETbin][foldedEta].Fill(isolation)
            histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].Fill(SF)
            histos_isolation_phi_3x3[ETbin][phi].Fill(isolation)
            histos_scaleFactor_phi_3x3[ETbin][phi].Fill(SF)
            if eta < 17:
              histos_isolation_phi_barrel_3x3[ETbin][phi].Fill(isolation)
              histos_scaleFactor_phi_barrel_3x3[ETbin][phi].Fill(SF)
            elif eta > 17 and eta < 26:
              histos_isolation_phi_endcap_3x3[ETbin][phi].Fill(isolation)
              histos_scaleFactor_phi_endcap_3x3[ETbin][phi].Fill(SF)
         if TPGVeto5x5>TPGVeto_cut and (l1_summed55_e-l1_center_e)<3*125 and (l1_summed55_h-l1_center_h)<3*125:
            phicounts_passing[phi] += 1
            etacounts_passing[eta] += 1
            foldedEtacounts_passing[foldedEta] += 1
            isolation = l1_summed55_h - l1_center_h
            SF = gen/(event.sumCorr_e+l1_summed55_h)
            histos_resolution_5x5[ETbin].Fill(resolution_5x5)
            histos_genpt_5x5[ETbin].Fill(event.gen_pt)
            histos_summed33e_5x5[ETbin].Fill(event.l1_summed33_h)
            histos_summed55e_5x5[ETbin].Fill(event.l1_summed55_h)
            histos_isolation_phi_3x3[ETbin][phi].Fill(isolation)
            histos_scaleFactor_phi_5x5[ETbin][phi].Fill(SF)
            histos_isolation_eta_5x5[ETbin][eta].Fill(isolation)
            histos_scaleFactor_eta_5x5[ETbin][eta].Fill(SF)
            histos_isolation_eta_folded_5x5[ETbin][foldedEta].Fill(isolation)
            histos_scaleFactor_eta_folded_5x5[ETbin][foldedEta].Fill(SF)
            if eta < 17:
              histos_isolation_phi_barrel_5x5[ETbin][phi].Fill(isolation)
              histos_scaleFactor_phi_barrel_5x5[ETbin][phi].Fill(SF)
            elif eta > 17 and eta < 26:
              histos_isolation_phi_endcap_5x5[ETbin][phi].Fill(isolation)
              histos_scaleFactor_phi_endcap_5x5[ETbin][phi].Fill(SF)

for ETbin in range(0,14):
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
        Mean_scaleFactor_3x3 =histos_scaleFactor_phi_barrel_3x3[ETbin][phi].GetMean()
        MeanError_scaleFactor_3x3 =histos_scaleFactor_phi_barrel_3x3[ETbin][phi].GetMeanError()
        Mean_scaleFactor_5x5 =histos_scaleFactor_phi_barrel_5x5[ETbin][phi].GetMean()
        MeanError_scaleFactor_5x5 =histos_scaleFactor_phi_barrel_5x5[ETbin][phi].GetMeanError()
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
        Mean_scaleFactor_3x3 =histos_scaleFactor_phi_endcap_3x3[ETbin][phi].GetMean()
        MeanError_scaleFactor_3x3 =histos_scaleFactor_phi_endcap_3x3[ETbin][phi].GetMeanError()
        Mean_scaleFactor_5x5 =histos_scaleFactor_phi_endcap_5x5[ETbin][phi].GetMean()
        MeanError_scaleFactor_5x5 =histos_scaleFactor_phi_endcap_5x5[ETbin][phi].GetMeanError()
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
        histos_isolation_ETbin_foldedEta_3x3[ETbin].SetBinContent(foldedEta+1,Mean_isolation_3x3)
        histos_isolation_ETbin_foldedEta_3x3[ETbin].SetBinError(foldedEta+1,MeanError_isolation_3x3)
        histos_isolation_ETbin_foldedEta_5x5[ETbin].SetBinContent(foldedEta+1,Mean_isolation_5x5)
        histos_isolation_ETbin_foldedEta_5x5[ETbin].SetBinError(foldedEta+1,MeanError_isolation_5x5)
        Mean_scaleFactor_3x3 =histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].GetMean()
        MeanError_scaleFactor_3x3 =histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].GetMeanError()
        Mean_scaleFactor_5x5 =histos_scaleFactor_eta_folded_5x5[ETbin][foldedEta].GetMean()
        MeanError_scaleFactor_5x5 =histos_scaleFactor_eta_folded_5x5[ETbin][foldedEta].GetMeanError()
        histos_scaleFactor_ETbin_foldedEta_3x3[ETbin].SetBinContent(foldedEta+1,Mean_scaleFactor_3x3)
        histos_scaleFactor_ETbin_foldedEta_3x3[ETbin].SetBinError(foldedEta+1,MeanError_scaleFactor_3x3)
        histos_scaleFactor_ETbin_foldedEta_5x5[ETbin].SetBinContent(foldedEta+1,Mean_scaleFactor_5x5)
        histos_scaleFactor_ETbin_foldedEta_5x5[ETbin].SetBinError(foldedEta+1,MeanError_scaleFactor_5x5)
        if ETbin > 0 or foldedEta > 0:
            text_file.write(", ")
        else:
            text_file.write("		float hcal[364] = {")
        text_file.write("%f" % Mean_scaleFactor_5x5)
        if ETbin == 13 and foldedEta == 27:
            text_file.write("};")


#
file=ROOT.TFile("outfile_HCAL_histos_"+suffix+"_filerange"+str(start_index)+"to"+str(end_index_plus_1)+".root","RECREATE")
file.cd()
#


for ETbin in range(0,14):
  histos_resolution_3x3[ETbin].Write()
  histos_resolution_5x5[ETbin].Write()
  histos_genpt_3x3[ETbin].Write()
  histos_genpt_5x5[ETbin].Write()
  histos_summed33e_3x3[ETbin].Write()
  histos_summed33e_5x5[ETbin].Write()
  histos_summed55e_3x3[ETbin].Write()
  histos_summed55e_5x5[ETbin].Write()
  histos_isolation_ETbin_phi_3x3[ETbin].Write()
  histos_isolation_ETbin_phi_5x5[ETbin].Write()
  histos_isolation_ETbin_phi_barrel_3x3[ETbin].Write()
  histos_isolation_ETbin_phi_barrel_5x5[ETbin].Write()
  histos_isolation_ETbin_phi_endcap_3x3[ETbin].Write()
  histos_isolation_ETbin_phi_endcap_5x5[ETbin].Write()
  histos_isolation_ETbin_eta_3x3[ETbin].Write()
  histos_isolation_ETbin_eta_5x5[ETbin].Write()
  histos_isolation_ETbin_foldedEta_3x3[ETbin].Write()
  histos_isolation_ETbin_foldedEta_5x5[ETbin].Write()
  histos_scaleFactor_ETbin_phi_3x3[ETbin].Write()
  histos_scaleFactor_ETbin_phi_5x5[ETbin].Write()
  histos_scaleFactor_ETbin_phi_barrel_3x3[ETbin].Write()
  histos_scaleFactor_ETbin_phi_barrel_5x5[ETbin].Write()
  histos_scaleFactor_ETbin_phi_endcap_3x3[ETbin].Write()
  histos_scaleFactor_ETbin_phi_endcap_5x5[ETbin].Write()
  histos_scaleFactor_ETbin_eta_3x3[ETbin].Write()
  histos_scaleFactor_ETbin_eta_5x5[ETbin].Write()
  histos_scaleFactor_ETbin_foldedEta_3x3[ETbin].Write()
  histos_scaleFactor_ETbin_foldedEta_5x5[ETbin].Write()
  for phi in range(0,72):
    histos_isolation_phi_3x3[ETbin][phi].Write()
    histos_isolation_phi_5x5[ETbin][phi].Write()
    histos_scaleFactor_phi_3x3[ETbin][phi].Write()
    histos_scaleFactor_phi_5x5[ETbin][phi].Write()
    histos_isolation_phi_barrel_3x3[ETbin][phi].Write()
    histos_isolation_phi_barrel_5x5[ETbin][phi].Write()
    histos_scaleFactor_phi_barrel_3x3[ETbin][phi].Write()
    histos_scaleFactor_phi_barrel_5x5[ETbin][phi].Write()
    histos_isolation_phi_endcap_3x3[ETbin][phi].Write()
    histos_isolation_phi_endcap_5x5[ETbin][phi].Write()
    histos_scaleFactor_phi_endcap_3x3[ETbin][phi].Write()
    histos_scaleFactor_phi_endcap_5x5[ETbin][phi].Write()
  for eta in range(0,56):
    histos_isolation_eta_3x3[ETbin][eta].Write()
    histos_isolation_eta_5x5[ETbin][eta].Write()
    histos_scaleFactor_eta_3x3[ETbin][eta].Write()
    histos_scaleFactor_eta_5x5[ETbin][eta].Write()
  for foldedEta in range(0,28):
    histos_isolation_eta_folded_3x3[ETbin][foldedEta].Write()
    histos_isolation_eta_folded_5x5[ETbin][foldedEta].Write()
    histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].Write()
    histos_scaleFactor_eta_folded_5x5[ETbin][foldedEta].Write()

print ''
print 'n_events = %d' % n_events
print ''
for ETbin in range(0,15):
  print 'n_events ETbin%d = %d' % (ETbin-1,ETbincounts[ETbin])
print ''
for phi in range(0,72):
  print 'phi = %d, events = %d, passsing_3x3veto = %d' % (phi,phicounts[phi],phicounts_passing[phi])
print ''
for eta in range(0,56):
  print 'eta = %d, events = %d, passing_3x3veto = %d' % (eta,etacounts[eta],etacounts_passing[eta])
print ''
for foldedEta in range(0,28):
  print 'foldedEta = %d, events = %d, passing_3x3veto = %d' % (foldedEta,foldedEtacounts[foldedEta],foldedEtacounts_passing[foldedEta])
