from __future__ import division
#from decimal import *
from sys import argv, exit, stdout, stderr
import sys
import ROOT
import os
import math

if len(argv) != 6:
   print 'ERROR: Incorrect number of arguments provided'
   print 'Usage: python computeECALcalibs.py input<file or folder> suffix TPGVeto_cut start_index end_index_plus_1'
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

# [foldedEta+28*ETbin]
# 100X
ecalCalibs_p90_mode = [1.128436, 1.102229, 1.128385, 1.127897, 1.142444, 1.115476, 1.104283, 1.124583, 1.115929, 1.115196, 1.130342, 1.127173, 1.130640, 1.125474, 1.126652, 1.143535, 1.148905, 1.309035, 1.156021, 1.292685, 1.314302, 1.327634, 1.341229, 1.364885, 1.411117, 1.432419, 1.288526, 1.082139, 1.078545, 1.072734, 1.075464, 1.081920, 1.078434, 1.072281, 1.079780, 1.082043, 1.094741, 1.074544, 1.082784, 1.084089, 1.086375, 1.099718, 1.092858, 1.092855, 1.105166, 1.256155, 1.126301, 1.215671, 1.226302, 1.268900, 1.281721, 1.310629, 1.356976, 1.386428, 1.220159, 1.066925, 1.052366, 1.053986, 1.055250, 1.051033, 1.055017, 1.062249, 1.059624, 1.065355, 1.062623, 1.054089, 1.060477, 1.074504, 1.075570, 1.078549, 1.071588, 1.080279, 1.078463, 1.211087, 1.103915, 1.186517, 1.194161, 1.234868, 1.250080, 1.274639, 1.327394, 1.362218, 1.161404, 1.062366, 1.044640, 1.043507, 1.046185, 1.042067, 1.042425, 1.044121, 1.050677, 1.051604, 1.046070, 1.040140, 1.052732, 1.055652, 1.057201, 1.062982, 1.059512, 1.054542, 1.063873, 1.189094, 1.091948, 1.165298, 1.177338, 1.213632, 1.223587, 1.259376, 1.312025, 1.330172, 1.160220, 1.059058, 1.032947, 1.033877, 1.036016, 1.036056, 1.037819, 1.036489, 1.040341, 1.035373, 1.042736, 1.030510, 1.039291, 1.043943, 1.051946, 1.049653, 1.045154, 1.048874, 1.043392, 1.146608, 1.083743, 1.161479, 1.164940, 1.197187, 1.229915, 1.238886, 1.289410, 1.344620, 1.078591, 1.051894, 1.025813, 1.028301, 1.026054, 1.032050, 1.029899, 1.032383, 1.033763, 1.034211, 1.033892, 1.023902, 1.034960, 1.039866, 1.039984, 1.042478, 1.041047, 1.044143, 1.038748, 1.146814, 1.069148, 1.134356, 1.147952, 1.175102, 1.202532, 1.234549, 1.285897, 1.280056, 1.055845, 1.050155, 1.025370, 1.024465, 1.023378, 1.024989, 1.026322, 1.025140, 1.026122, 1.028451, 1.029161, 1.020083, 1.031555, 1.032971, 1.036222, 1.042410, 1.038053, 1.036796, 1.037195, 1.123576, 1.071556, 1.129229, 1.129561, 1.170449, 1.190240, 1.218357, 1.270482, 1.302586, 1.047321, 1.049100, 1.018591, 1.019825, 1.020823, 1.019265, 1.021761, 1.021521, 1.024053, 1.024121, 1.024979, 1.015315, 1.026035, 1.028734, 1.030409, 1.031414, 1.030694, 1.033450, 1.035642, 1.103688, 1.066969, 1.117955, 1.135950, 1.163170, 1.180714, 1.228736, 1.254963, 1.307361, 1.047123, 1.047264, 1.017483, 1.016714, 1.018925, 1.017087, 1.020438, 1.018852, 1.020796, 1.022534, 1.023495, 1.013378, 1.024097, 1.026067, 1.029037, 1.030731, 1.028759, 1.032480, 1.034680, 1.101491, 1.069770, 1.110644, 1.129222, 1.147881, 1.176695, 1.219110, 1.253033, 1.308691, 1.040706, 1.046607, 1.015432, 1.014445, 1.016057, 1.014908, 1.019115, 1.016567, 1.020411, 1.019852, 1.020255, 1.010779, 1.023433, 1.023674, 1.027479, 1.027385, 1.027332, 1.027537, 1.029061, 1.091079, 1.063278, 1.108876, 1.122727, 1.171282, 1.172058, 1.211259, 1.245839, 1.303968, 1.033863, 1.047743, 1.014370, 1.013304, 1.013397, 1.014261, 1.013673, 1.013183, 1.018534, 1.016581, 1.017015, 1.008220, 1.019515, 1.021560, 1.024502, 1.025611, 1.025905, 1.025863, 1.027252, 1.085230, 1.063040, 1.112256, 1.116617, 1.140393, 1.159214, 1.191434, 1.240601, 1.268525, 1.033247, 1.042853, 1.010174, 1.009843, 1.011520, 1.011041, 1.012957, 1.009075, 1.013178, 1.013301, 1.015033, 1.005133, 1.017533, 1.018564, 1.020319, 1.022634, 1.022429, 1.022338, 1.025613, 1.077639, 1.057895, 1.107098, 1.111157, 1.136106, 1.161737, 1.179259, 1.232736, 1.290141, 1.018941, 1.014733, 1.000302, 1.007651, 1.000751, 1.007791, 1.008949, 1.005394, 1.009599, 1.010180, 1.010865, 1.001827, 1.012447, 1.015231, 1.019545, 1.020611, 1.022404, 1.019032, 1.023113, 1.065127, 1.054688, 1.102754, 1.106151, 1.125574, 1.134480, 1.180965, 1.231939, 1.277289, 1.018941, 1.014733]
ecalCalibs_p90_mean = [1.214616, 1.184566, 1.222971, 1.189968, 1.209363, 1.201344, 1.212175, 1.223355, 1.212855, 1.237464, 1.256875, 1.270687, 1.300410, 1.289956, 1.314086, 1.352848, 1.378704, 2.103519, 1.425477, 1.568024, 1.544551, 1.563197, 1.512150, 1.549315, 1.636618, 1.656023, 1.443768, 1.364712, 1.178209, 1.159928, 1.159752, 1.193284, 1.222675, 1.218985, 1.202997, 1.192405, 1.203933, 1.243594, 1.229832, 1.237334, 1.261827, 1.305156, 1.267918, 1.331946, 1.343738, 1.986180, 1.297301, 1.376641, 1.386528, 1.404260, 1.401590, 1.429997, 1.493357, 1.503775, 1.315366, 1.264375, 1.163160, 1.138775, 1.142929, 1.136622, 1.130476, 1.158521, 1.188314, 1.173087, 1.209723, 1.236633, 1.184082, 1.211771, 1.226227, 1.283882, 1.275583, 1.243621, 1.298739, 1.892864, 1.212160, 1.330858, 1.319224, 1.339079, 1.332969, 1.351645, 1.428475, 1.411062, 1.262488, 1.227752, 1.088865, 1.105674, 1.112628, 1.103358, 1.129211, 1.143489, 1.134313, 1.139677, 1.164709, 1.182617, 1.155275, 1.147404, 1.171681, 1.206954, 1.212163, 1.207594, 1.220839, 1.952976, 1.170470, 1.265225, 1.277545, 1.291627, 1.281019, 1.318931, 1.386636, 1.379424, 1.244968, 1.182945, 1.074381, 1.070706, 1.063579, 1.077103, 1.082230, 1.098034, 1.085221, 1.093360, 1.091430, 1.115988, 1.113864, 1.106688, 1.123885, 1.156501, 1.145817, 1.154014, 1.191194, 1.776690, 1.157634, 1.241204, 1.235664, 1.246856, 1.257261, 1.280560, 1.344529, 1.340593, 1.214913, 1.142016, 1.057844, 1.050848, 1.055569, 1.053260, 1.058694, 1.074351, 1.064378, 1.066611, 1.074693, 1.089660, 1.084618, 1.092510, 1.095764, 1.116577, 1.105888, 1.111282, 1.152120, 1.765630, 1.125810, 1.206133, 1.198447, 1.240100, 1.229493, 1.257869, 1.324719, 1.310431, 1.190095, 1.106146, 1.047357, 1.046957, 1.043133, 1.050240, 1.049827, 1.062415, 1.056579, 1.059805, 1.056674, 1.081937, 1.069120, 1.073311, 1.075508, 1.103073, 1.091515, 1.104368, 1.139142, 1.575131, 1.116582, 1.177973, 1.195169, 1.212386, 1.214669, 1.243525, 1.309034, 1.277102, 1.174375, 1.090832, 1.044191, 1.039655, 1.038347, 1.041051, 1.043026, 1.056320, 1.048155, 1.050673, 1.057468, 1.073748, 1.058454, 1.058829, 1.070269, 1.093005, 1.077175, 1.080575, 1.106738, 1.467335, 1.110757, 1.172432, 1.175909, 1.192434, 1.199520, 1.227928, 1.293876, 1.272600, 1.173298, 1.083375, 1.037658, 1.032608, 1.042060, 1.036280, 1.036688, 1.046866, 1.039650, 1.043631, 1.048155, 1.070561, 1.049325, 1.052548, 1.057455, 1.074119, 1.068514, 1.081279, 1.109176, 1.401287, 1.099330, 1.154956, 1.165266, 1.188638, 1.189690, 1.220172, 1.280919, 1.258995, 1.161779, 1.073910, 1.031563, 1.028391, 1.029243, 1.035597, 1.033458, 1.044123, 1.037258, 1.039085, 1.042862, 1.062072, 1.041861, 1.046822, 1.052384, 1.070918, 1.061712, 1.063213, 1.099451, 1.350373, 1.089681, 1.148962, 1.150329, 1.176517, 1.183580, 1.210320, 1.273026, 1.247781, 1.130466, 1.067846, 1.024723, 1.024659, 1.025188, 1.025933, 1.028416, 1.036474, 1.028336, 1.031804, 1.034320, 1.050423, 1.036706, 1.040698, 1.046823, 1.061832, 1.054128, 1.058563, 1.088040, 1.288414, 1.083274, 1.137434, 1.141760, 1.162618, 1.171059, 1.203678, 1.262926, 1.237894, 1.062471, 1.055771, 1.019820, 1.018217, 1.017924, 1.020576, 1.021526, 1.030224, 1.022908, 1.024268, 1.026418, 1.039652, 1.028332, 1.031682, 1.037941, 1.050454, 1.044391, 1.045787, 1.072765, 1.220564, 1.077411, 1.127124, 1.132386, 1.152589, 1.163197, 1.191127, 1.247500, 1.224775, 1.018745, 1.014756, 1.014620, 1.013373, 1.013060, 1.014255, 1.015292, 1.021775, 1.017473, 1.018126, 1.019103, 1.027449, 1.021685, 1.023951, 1.028949, 1.041233, 1.035741, 1.036553, 1.059225, 1.147778, 1.068311, 1.115394, 1.118935, 1.139147, 1.151670, 1.181052, 1.234872, 1.206892, 1.018745, 1.014756]

ecal_calibs = ecalCalibs_p90_mode

########### MAke Hist arrays #########
histos_resolution_3x3 = []
histos_genpt_3x3 = []
histos_summed33e_3x3 = []
histos_summed55e_3x3 = []
histos_isolation_phi_3x3 = []
histos_isolation_phi_barrel_3x3 = []
histos_isolation_phi_endcap_3x3 = []
histos_isolation_eta_3x3 = []
histos_isolation_eta_folded_3x3 = []
histos_scaleFactor_phi_3x3 = []
histos_scaleFactor_phi_barrel_3x3 = []
histos_scaleFactor_phi_endcap_3x3 = []
histos_scaleFactor_eta_3x3 = []
histos_scaleFactor_eta_folded_3x3 = []
for i in range(0,14):
  hname_resolution_3x3 = "histos_resolution_3x3_ETbin%d" % i # Each histogram must have a unique name
  histos_resolution_3x3.append(ROOT.TH1F(hname_resolution_3x3,"",100,-1,4))
  hname_genpt_3x3 = "histos_genpt_3x3_ETbin%d" % i
  histos_genpt_3x3.append(ROOT.TH1F(hname_genpt_3x3,"",200,0,200))
  hname_summed33e_3x3 = "histos_summed33e_3x3_ETbin%d" % i
  histos_summed33e_3x3.append(ROOT.TH1F(hname_summed33e_3x3,"",200,0,200))
  hname_summed55e_3x3 = "histos_summed55e_3x3_ETbin%d" % i
  histos_summed55e_3x3.append(ROOT.TH1F(hname_summed55e_3x3,"",200,0,200))
  histos_isolation_phi_3x3.append([])
  histos_isolation_phi_barrel_3x3.append([])
  histos_isolation_phi_endcap_3x3.append([])
  histos_isolation_eta_3x3.append([])
  histos_isolation_eta_folded_3x3.append([])
  histos_scaleFactor_phi_3x3.append([])
  histos_scaleFactor_phi_barrel_3x3.append([])
  histos_scaleFactor_phi_endcap_3x3.append([])
  histos_scaleFactor_eta_3x3.append([])
  histos_scaleFactor_eta_folded_3x3.append([])
  for j in range(0,72):
    hname_isolation_phi_3x3 = "histos_isolation_phi_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_isolation_phi_3x3[i].append( ROOT.TH1F(hname_isolation_phi_3x3,"",4000,0,200) )
    hname_scaleFactor_phi_3x3 = "histos_scaleFactor_phi_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_phi_3x3[i].append( ROOT.TH1F(hname_scaleFactor_phi_3x3,"",100,0,5) )
    hname_isolation_phi_barrel_3x3 = "histos_isolation_phi_barrel_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_isolation_phi_barrel_3x3[i].append( ROOT.TH1F(hname_isolation_phi_barrel_3x3,"",4000,0,200) )
    hname_scaleFactor_phi_barrel_3x3 = "histos_scaleFactor_phi_barrel_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_phi_barrel_3x3[i].append( ROOT.TH1F(hname_scaleFactor_phi_barrel_3x3,"",100,0,5) )
    hname_isolation_phi_endcap_3x3 = "histos_isolation_phi_endcap_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_isolation_phi_endcap_3x3[i].append( ROOT.TH1F(hname_isolation_phi_endcap_3x3,"",4000,0,200) )
    hname_scaleFactor_phi_endcap_3x3 = "histos_scaleFactor_phi_endcap_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_phi_endcap_3x3[i].append( ROOT.TH1F(hname_scaleFactor_phi_endcap_3x3,"",100,0,5) )
  for j in range(0,56):
    hname_isolation_eta_3x3 = "histos_isolation_eta_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_isolation_eta_3x3[i].append( ROOT.TH1F(hname_isolation_eta_3x3,"",4000,0,200) )
    hname_scaleFactor_eta_3x3 = "histos_scaleFactor_eta_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_eta_3x3[i].append( ROOT.TH1F(hname_scaleFactor_eta_3x3,"",100,0,5) )
  for j in range(0,28):
    hname_isolation_eta_folded_3x3 = "histos_isolation_eta_folded_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_isolation_eta_folded_3x3[i].append( ROOT.TH1F(hname_isolation_eta_folded_3x3,"",4000,0,200) )
    hname_scaleFactor_eta_folded_3x3 = "histos_scaleFactor_eta_folded_3x3_%d_%d" % (i, j) # Each histogram must have a unique name
    histos_scaleFactor_eta_folded_3x3[i].append( ROOT.TH1F(hname_scaleFactor_eta_folded_3x3,"",100,0,5) )

# Converts tpgeta in [0,55] to foldedEta in [0,27]
def foldtpgeta(tpgeta):
  foldedEta = -1
  if tpgeta >= 28 and tpgeta < 56:
    foldedEta = tpgeta - 28
  elif tpgeta >= 0 and tpgeta < 28:
    foldedEta = 27 - tpgeta
  return foldedEta

def findETbin(ET):
  ETbin = -1
  if ET >= 3 and ET < 15:
    ETbin = int(math.floor(ET/3)) - 1
  elif ET >= 15 and ET < 45:
    ETbin = int(math.floor(ET/5)) + 1
  elif ET >= 45 and ET < 55:
    ETbin = 10
  elif ET >= 55 and ET < 70:
    ETbin = 11
  elif ET >= 70 and ET < 90:
    ETbin = 12
  elif ET >= 90:
    ETbin = 13
  return ETbin

events_inspected = 0
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
# max_Nfiles = min(1,len(infiles)) # Test on single file
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
      events_inspected += 1
      gen=event.gen_pt
      eta = event.gen_ieta
      foldedEta = foldtpgeta(eta)
      phi = event.gen_iphi
      l1_center_h = event.l1_center_h
      l1_center_e = event.l1_center_e
      l1_summed33_e = event.l1_summed33_e
      l1_summed55_e = event.l1_summed55_e
      l1_summed33_h = event.l1_summed33_h
      l1_summed55_h = event.l1_summed55_h
      l1_corrCenter_h = event.corr_center_h
      l1_corrCenter_e = event.corr_center_e
      l1_sumCorr33_e = event.sumCorr33_e
      l1_sumCorr55_e = event.sumCorr_e
      l1_sumCorr33_h = event.sumCorr33_h
      l1_sumCorr55_h = event.sumCorr_h
      l1_square55_e = event.l1_square55_e
      l1_square55_h = event.l1_square55_h
      
      ETbin = findETbin(l1_center_e)
      # ETbin = -1
      # if l1_center_e >= 3 and l1_center_e < 15:
      #   ETbin = int(math.floor(l1_center_e/3)) - 1
      # elif l1_center_e >= 15 and l1_center_e < 45:
      #   ETbin = int(math.floor(l1_center_e/5)) + 1
      # elif l1_center_e >= 45 and l1_center_e < 55:
      #   ETbin = 10
      # elif l1_center_e >= 55 and l1_center_e < 70:
      #   ETbin = 11
      # elif l1_center_e >= 70 and l1_center_e < 90:
      #   ETbin = 12
      # elif l1_center_e >= 90:
      #   ETbin = 13
      
      if ETbin>=0 and gen>0 and gen<125 and eta>=0 and eta<56 and phi>=0 and phi<72:
         phicounts[phi] += 1
         etacounts[eta] += 1
         foldedEtacounts[foldedEta] += 1
         TPGVeto3x3 = 0.0
         TPGVeto5x5 = 0.0
         if foldedEta>=26 and foldedEta<28:
             l1_center_e *= 2.0
         if l1_summed33_e > 3:
             TPGVeto3x3 = l1_center_e/l1_summed33_e
         if l1_summed55_e > 3:
             TPGVeto5x5 = l1_center_e/l1_summed55_e
         resolution_3x3 = (l1_summed33_e-gen)/gen
         resolution_5x5 = (l1_summed55_e-gen)/gen
         
         if TPGVeto3x3>TPGVeto_cut:
            phicounts_passing[phi] += 1
            etacounts_passing[eta] += 1
            foldedEtacounts_passing[foldedEta] += 1
            
            sum_of_square_e = 0
            sum_of_square_e_corr = 0
            for i in range(1,4): # iPhi displacement + 2
              for j in range(1,4): # iEta displacement + 2
                sum_of_square_e += l1_square55_e.at(i).at(j)
                foldedEta_tower = foldtpgeta(eta+j-2)
                ETbin_for_calibLookup = max(min(findETbin(l1_square55_e.at(i).at(j)),12),0)
                ECAL_calib_factor = -99999.9
                if foldedEta_tower < 28 and foldedEta_tower >= 0:
                  ECAL_calib_factor = ecal_calibs[foldedEta_tower+28*ETbin_for_calibLookup]
                sum_of_square_e_corr += l1_square55_e.at(i).at(j)*ECAL_calib_factor
            
            SF = gen/sum_of_square_e
            
            isolation = sum_of_square_e - l1_center_e
            histos_resolution_3x3[ETbin].Fill(resolution_3x3)
            histos_genpt_3x3[ETbin].Fill(event.gen_pt)
            histos_summed33e_3x3[ETbin].Fill(l1_summed33_e)
            histos_summed55e_3x3[ETbin].Fill(l1_summed55_e)
            histos_isolation_eta_3x3[ETbin][eta].Fill(isolation)
            histos_scaleFactor_eta_3x3[ETbin][eta].Fill(SF)
            histos_isolation_eta_folded_3x3[ETbin][foldedEta].Fill(isolation)
            histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].Fill(SF)
            histos_isolation_phi_3x3[ETbin][phi].Fill(isolation)
            histos_scaleFactor_phi_3x3[ETbin][phi].Fill(SF)
            if foldedEta < 17:
              histos_isolation_phi_barrel_3x3[ETbin][phi].Fill(isolation)
              histos_scaleFactor_phi_barrel_3x3[ETbin][phi].Fill(SF)
            elif foldedEta > 17 and foldedEta < 26:
              histos_isolation_phi_endcap_3x3[ETbin][phi].Fill(isolation)
              histos_scaleFactor_phi_endcap_3x3[ETbin][phi].Fill(SF)


#
file=ROOT.TFile("outfile_ECAL_histos_"+suffix+"_filerange"+str(start_index)+"to"+str(end_index_plus_1)+".root","RECREATE")
file.cd()
#


for ETbin in range(0,14):
  histos_resolution_3x3[ETbin].Write()
  histos_genpt_3x3[ETbin].Write()
  histos_summed33e_3x3[ETbin].Write()
  histos_summed55e_3x3[ETbin].Write()
  for phi in range(0,72):
    histos_isolation_phi_3x3[ETbin][phi].Write()
    histos_scaleFactor_phi_3x3[ETbin][phi].Write()
    histos_isolation_phi_barrel_3x3[ETbin][phi].Write()
    histos_scaleFactor_phi_barrel_3x3[ETbin][phi].Write()
    histos_isolation_phi_endcap_3x3[ETbin][phi].Write()
    histos_scaleFactor_phi_endcap_3x3[ETbin][phi].Write()
  for eta in range(0,56):
    histos_isolation_eta_3x3[ETbin][eta].Write()
    histos_scaleFactor_eta_3x3[ETbin][eta].Write()
  for foldedEta in range(0,28):
    histos_isolation_eta_folded_3x3[ETbin][foldedEta].Write()
    histos_scaleFactor_eta_folded_3x3[ETbin][foldedEta].Write()

print 'events_inspected = %d' % events_inspected
for phi in range(0,72):
  print 'phi = %d, events = %d, passsing_3x3veto = %d' % (phi,phicounts[phi],phicounts_passing[phi])
print ''
for eta in range(0,56):
  print 'eta = %d, events = %d, passing_3x3veto = %d' % (eta,etacounts[eta],etacounts_passing[eta])
print ''
for foldedEta in range(0,28):
  print 'foldedEta = %d, events = %d, passing_3x3veto = %d' % (foldedEta,foldedEtacounts[foldedEta],foldedEtacounts_passing[foldedEta])
