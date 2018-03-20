// system include files
#include <memory>
#include <unordered_map>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/ESHandle.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "CommonTools/UtilAlgos/interface/TFileService.h"

#include "CalibFormats/CaloTPG/interface/CaloTPGTranscoder.h"
#include "CalibFormats/CaloTPG/interface/CaloTPGRecord.h"
#include "CalibFormats/HcalObjects/interface/HcalDbRecord.h"
#include "CalibFormats/HcalObjects/interface/HcalDbService.h"

#include "CondFormats/DataRecord/interface/HcalChannelQualityRcd.h"
#include "CondFormats/DataRecord/interface/L1CaloGeometryRecord.h"
#include "CondFormats/HcalObjects/interface/HcalChannelQuality.h"
#include "CondFormats/L1TObjects/interface/L1CaloGeometry.h"

#include "CondFormats/L1TObjects/interface/L1RCTParameters.h"
#include "CondFormats/DataRecord/interface/L1RCTParametersRcd.h"
#include "CondFormats/L1TObjects/interface/L1CaloHcalScale.h"
#include "CondFormats/DataRecord/interface/L1CaloHcalScaleRcd.h"

#include "DataFormats/EcalDigi/interface/EcalDigiCollections.h"

#include "DataFormats/Common/interface/SortedCollection.h"
#include "DataFormats/CaloTowers/interface/CaloTower.h"
#include "DataFormats/HcalDigi/interface/HcalDigiCollections.h"
#include "DataFormats/HcalDigi/interface/HcalTriggerPrimitiveDigi.h"
#include "DataFormats/HcalDetId/interface/HcalTrigTowerDetId.h"
#include "DataFormats/HcalDetId/interface/HcalDetId.h"
#include "DataFormats/L1CaloTrigger/interface/L1CaloCollections.h"

#include "Geometry/CaloGeometry/interface/CaloGeometry.h"
#include "Geometry/HcalTowerAlgo/interface/HcalGeometry.h"
#include "Geometry/HcalTowerAlgo/interface/HcalTrigTowerGeometry.h"
#include "Geometry/Records/interface/CaloGeometryRecord.h"

#include "DataFormats/HepMCCandidate/interface/GenParticle.h"

#include "L1Trigger/CaloLayer1Calibrations/interface/helpers.h"

#include "TH1D.h"
#include "TH2D.h"
#include "TString.h"
#include "TTree.h"

#include "TLorentzVector.h"
//
// class declaration
//

using namespace std;
using namespace edm;

class PionCalibrations : public edm::EDAnalyzer {
	public:
		explicit PionCalibrations(const edm::ParameterSet&);
		static const unsigned int N_TOWER_PHI;
		static const unsigned int N_TOWER_ETA;
		~PionCalibrations();

		static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);

	private:
		virtual void analyze(const edm::Event&, const edm::EventSetup&);

		// ----------member data ---------------------------
		edm::EDGetTokenT<HcalTrigPrimDigiCollection> digis_;
		edm::EDGetTokenT<EcalTrigPrimDigiCollection> Edigis_;
		edm::EDGetTokenT<std::vector<reco::GenParticle>> genSrc_;
		bool detid_;
		double threshold_;
		bool doClosure_;

		//The square sums
		vector<vector<unsigned int>> eTowerETCode;
		vector<vector<unsigned int>> eCorrTowerETCode;
		vector<vector<unsigned int>> hTowerETCode;
		vector<vector<unsigned int>> hCorrTowerETCode;


		int event_;


		TTree *pions_;
		double pion_pt_;
		double pion_et_;
		double pion_eta_;
		double pion_phi_;
		int pion_ieta_;
		int pion_iphi_;

		TTree *matched_;
		double gen_et_;
		double gen_pt_;
		double gen_eta_;
		double gen_phi_;
		int gen_ieta_;
		int gen_iphi_;
                double l1_center_e_;
                double l1_center_h_;
		double l1_summed33_;
		double l1_summed33_e_;
		double l1_summed33_h_;
		double l1_summed55_;
		double l1_summed55_e_;
		double l1_summed55_h_;
		double HoE_;
                double corr_center_e_;
                double corr_center_h_;
		double sumCorr33_;
		double sumCorr33_e_;
		double sumCorr33_h_;
		double sumCorr_;
		double sumCorr_e_;
		double sumCorr_h_;
		// int ETbin_;


		TTree *Htps_;
		TTree *Etps_;

		int tp_ieta_;
		int tp_iphi_;
		double tp_phi_;
		double tp_eta_;
		int tp_depth_;
		int tp_version_;
		int tp_soi_;
		double tp_et_;

		double etp_et_;
		int etp_ieta_;
		int etp_iphi_;
		double etp_phi_;
		double etp_eta_;
	
		vector<vector<double>> l1_square55_e_;
		vector<vector<double>> l1_square55_h_;

   float ecal[364] = {1.121683, 1.123691, 1.108489, 1.121521, 1.125255, 1.121693, 1.127835, 1.117779, 1.127152, 1.131185, 1.124344, 1.128536, 1.134725, 1.141772, 1.143249, 1.140299, 1.152531, 1.319443, 1.210847, 1.339125, 1.356573, 1.396528, 1.377966, 1.409579, 1.443289, 1.454007, 1.295642, 1.227788, 1.082900, 1.074461, 1.079962, 1.075127, 1.086775, 1.083590, 1.084558, 1.082557, 1.090276, 1.087614, 1.091867, 1.087652, 1.099034, 1.103327, 1.100456, 1.109527, 1.110784, 1.302258, 1.168732, 1.278368, 1.298565, 1.331746, 1.314623, 1.341301, 1.386985, 1.430218, 1.204316, 1.190891, 1.062883, 1.054139, 1.058559, 1.063505, 1.063059, 1.062662, 1.065150, 1.068217, 1.065320, 1.067348, 1.067776, 1.070561, 1.077374, 1.085696, 1.082619, 1.079525, 1.094581, 1.248178, 1.148441, 1.236617, 1.267048, 1.288578, 1.288512, 1.315666, 1.360049, 1.362456, 1.170797, 1.167626, 1.050682, 1.041363, 1.049212, 1.049985, 1.050699, 1.049319, 1.051826, 1.051975, 1.057911, 1.055179, 1.053420, 1.054771, 1.069557, 1.073795, 1.070160, 1.069165, 1.072477, 1.238395, 1.138875, 1.216007, 1.244247, 1.273514, 1.271499, 1.294721, 1.338348, 1.387534, 1.151556, 1.158395, 1.042771, 1.034424, 1.035937, 1.035207, 1.040111, 1.040705, 1.041693, 1.042686, 1.039497, 1.043452, 1.041545, 1.044947, 1.053061, 1.062762, 1.058935, 1.055335, 1.065606, 1.193257, 1.131426, 1.198880, 1.224663, 1.251683, 1.256435, 1.269958, 1.318988, 1.372872, 1.136677, 1.141251, 1.033837, 1.031071, 1.029707, 1.031193, 1.033072, 1.035870, 1.031507, 1.035295, 1.034799, 1.035418, 1.038483, 1.042567, 1.044793, 1.053306, 1.052018, 1.051434, 1.056204, 1.165940, 1.122919, 1.194796, 1.215185, 1.241700, 1.241192, 1.256956, 1.299124, 1.357881, 1.123170, 1.134848, 1.030442, 1.024761, 1.025480, 1.025364, 1.026802, 1.028792, 1.026702, 1.029903, 1.030029, 1.031292, 1.031683, 1.032099, 1.038992, 1.046039, 1.044969, 1.042792, 1.049454, 1.160109, 1.119586, 1.178622, 1.205947, 1.229264, 1.231618, 1.245986, 1.291842, 1.358345, 1.117718, 1.126883, 1.025564, 1.020994, 1.022154, 1.022523, 1.024304, 1.024387, 1.024369, 1.024698, 1.024857, 1.026679, 1.026999, 1.027745, 1.036174, 1.040190, 1.041848, 1.040525, 1.043341, 1.148116, 1.118444, 1.173695, 1.200880, 1.225635, 1.219548, 1.240240, 1.278999, 1.315860, 1.112813, 1.122397, 1.023703, 1.017579, 1.018104, 1.017659, 1.020570, 1.021379, 1.021771, 1.022549, 1.022039, 1.020696, 1.023734, 1.024919, 1.033031, 1.039501, 1.037120, 1.038029, 1.044373, 1.147821, 1.115866, 1.171247, 1.195742, 1.219918, 1.222375, 1.232918, 1.275971, 1.312366, 1.104763, 1.123853, 1.022729, 1.015033, 1.016055, 1.024841, 1.018966, 1.019355, 1.019383, 1.022111, 1.019620, 1.018730, 1.023090, 1.023060, 1.031683, 1.037654, 1.033611, 1.035408, 1.042514, 1.129705, 1.111494, 1.170215, 1.192696, 1.211153, 1.219209, 1.226238, 1.268898, 1.329354, 1.099919, 1.119065, 1.019639, 1.012224, 1.019498, 1.014690, 1.015372, 1.015029, 1.016340, 1.018439, 1.017241, 1.015631, 1.019250, 1.020679, 1.029578, 1.033115, 1.032704, 1.032550, 1.038186, 1.130066, 1.122241, 1.163237, 1.187682, 1.205797, 1.213205, 1.220996, 1.257875, 1.319851, 1.095214, 1.114397, 1.014848, 1.007609, 1.014595, 1.009661, 1.017298, 1.011264, 1.012152, 1.014643, 1.013504, 1.009988, 1.016762, 1.018233, 1.025658, 1.029184, 1.031794, 1.031796, 1.035437, 1.119702, 1.119120, 1.154691, 1.181214, 1.192774, 1.189330, 1.214413, 1.253684, 1.313831, 1.099976, 1.048771, 1.018860, 1.002584, 1.024954, 1.005857, 1.013041, 1.018629, 1.008655, 1.009616, 1.010172, 1.007577, 1.013120, 1.015258, 1.022823, 1.028055, 1.029566, 1.029339, 1.033359, 1.148478, 1.112274, 1.150181, 1.171471, 1.184794, 1.188237, 1.212775, 1.244559, 1.259219, 1.099976, 1.048771}; // Mode, 9_2_8
   // float ecal[364] = {1.197340, 1.198549, 1.168785, 1.173931, 1.191020, 1.209413, 1.196497, 1.209573, 1.195505, 1.231375, 1.235413, 1.244471, 1.283982, 1.325228, 1.334809, 1.353722, 1.428926, 2.126767, 1.450591, 1.589677, 1.580657, 1.629203, 1.564859, 1.577755, 1.625670, 1.594695, 1.424415, 1.321468, 1.135290, 1.151154, 1.125139, 1.130923, 1.135517, 1.148669, 1.147089, 1.154148, 1.183942, 1.187542, 1.191086, 1.190894, 1.249920, 1.258438, 1.273714, 1.287786, 1.342814, 2.053505, 1.313293, 1.461993, 1.451037, 1.465911, 1.438294, 1.455272, 1.501573, 1.477581, 1.339441, 1.245791, 1.129958, 1.107732, 1.102933, 1.100946, 1.120345, 1.124828, 1.126518, 1.136332, 1.145752, 1.175010, 1.179295, 1.188173, 1.211749, 1.224195, 1.234790, 1.239917, 1.353503, 2.008072, 1.252317, 1.365824, 1.378117, 1.403996, 1.356526, 1.385768, 1.434346, 1.415377, 1.298908, 1.216760, 1.102309, 1.097450, 1.090676, 1.084893, 1.091920, 1.109602, 1.103849, 1.112758, 1.126005, 1.137318, 1.120697, 1.142343, 1.150537, 1.201907, 1.168302, 1.188819, 1.228637, 1.936608, 1.224452, 1.326251, 1.342814, 1.353976, 1.325363, 1.359490, 1.399696, 1.364164, 1.276219, 1.195622, 1.076251, 1.069282, 1.066564, 1.074088, 1.070074, 1.084258, 1.086150, 1.076595, 1.092879, 1.114732, 1.101672, 1.105921, 1.119918, 1.145530, 1.167513, 1.147558, 1.191129, 1.809826, 1.202365, 1.287467, 1.304235, 1.317980, 1.291666, 1.317809, 1.374505, 1.342310, 1.254258, 1.175981, 1.061569, 1.053739, 1.050862, 1.052114, 1.057964, 1.073229, 1.058238, 1.066881, 1.063274, 1.090312, 1.075247, 1.088771, 1.097769, 1.135655, 1.119135, 1.123404, 1.172366, 1.741823, 1.173261, 1.258103, 1.279940, 1.279914, 1.276035, 1.291460, 1.347826, 1.321888, 1.237275, 1.159756, 1.058557, 1.043179, 1.038852, 1.040351, 1.047275, 1.056788, 1.051126, 1.058392, 1.051716, 1.085330, 1.061614, 1.073405, 1.081882, 1.109701, 1.103221, 1.100014, 1.149658, 1.650972, 1.163525, 1.237588, 1.259934, 1.268718, 1.254323, 1.276469, 1.335477, 1.298039, 1.226921, 1.151347, 1.046273, 1.035069, 1.033646, 1.034902, 1.037039, 1.055578, 1.043272, 1.044873, 1.045536, 1.067714, 1.058866, 1.060444, 1.067633, 1.101122, 1.083575, 1.089725, 1.133219, 1.530750, 1.150335, 1.220118, 1.237836, 1.251671, 1.239206, 1.262410, 1.317311, 1.279968, 1.221607, 1.145441, 1.039182, 1.033807, 1.026964, 1.030851, 1.035037, 1.046218, 1.034010, 1.038878, 1.038807, 1.061946, 1.047964, 1.052194, 1.061816, 1.089591, 1.077566, 1.075823, 1.118349, 1.441061, 1.144726, 1.205469, 1.228561, 1.240078, 1.224216, 1.249805, 1.307356, 1.275350, 1.210373, 1.139566, 1.033242, 1.027776, 1.025388, 1.025144, 1.029551, 1.045796, 1.031684, 1.032839, 1.032635, 1.060448, 1.040870, 1.047611, 1.060231, 1.075297, 1.066971, 1.073752, 1.113008, 1.383509, 1.129704, 1.198243, 1.222456, 1.234389, 1.224164, 1.243444, 1.294541, 1.265006, 1.178805, 1.135663, 1.029008, 1.023628, 1.019729, 1.022226, 1.024997, 1.036473, 1.027582, 1.028378, 1.029302, 1.047454, 1.035725, 1.038674, 1.047384, 1.068694, 1.060923, 1.063771, 1.100034, 1.333569, 1.126848, 1.185826, 1.209725, 1.224937, 1.212785, 1.236321, 1.284212, 1.256900, 1.115347, 1.114443, 1.023628, 1.017810, 1.014326, 1.015847, 1.018518, 1.028086, 1.020245, 1.020984, 1.022730, 1.038105, 1.027760, 1.028804, 1.041350, 1.059088, 1.051748, 1.053073, 1.087165, 1.252114, 1.119432, 1.174365, 1.196021, 1.210201, 1.200302, 1.226177, 1.270829, 1.244451, 1.048434, 1.049180, 1.018333, 1.014078, 1.010072, 1.010963, 1.013350, 1.020835, 1.014829, 1.016063, 1.016330, 1.026939, 1.021395, 1.022569, 1.033490, 1.047872, 1.042920, 1.044526, 1.072217, 1.185529, 1.108676, 1.161552, 1.183706, 1.197698, 1.189131, 1.212932, 1.255325, 1.225494, 1.048434, 1.049180}; // Mean, 9_2_8
   float hcal[364] = {1.306665, 1.298686, 1.299093, 1.304538, 1.309732, 1.318956, 1.316933, 1.318530, 1.321018, 1.337300, 1.327375, 1.335612, 1.344994, 1.351881, 1.341971, 1.346799, 1.342065, 1.226200, 1.233410, 1.249447, 1.236383, 1.246362, 1.244474, 1.248714, 1.253319, 1.248255, 1.332186, 1.309733, 1.281192, 1.275692, 1.276582, 1.281867, 1.285152, 1.297746, 1.296706, 1.296025, 1.299368, 1.313771, 1.309365, 1.314090, 1.319631, 1.329637, 1.321478, 1.316573, 1.305902, 1.180456, 1.205533, 1.222687, 1.200736, 1.205808, 1.206095, 1.210354, 1.211630, 1.213855, 1.291656, 1.286007, 1.258863, 1.255918, 1.256607, 1.260180, 1.262566, 1.278135, 1.275185, 1.273841, 1.276996, 1.292344, 1.283939, 1.293121, 1.301536, 1.310902, 1.299557, 1.299160, 1.281618, 1.151744, 1.183925, 1.200305, 1.162737, 1.168838, 1.172386, 1.207352, 1.179348, 1.175249, 1.251152, 1.258246, 1.239417, 1.233119, 1.237800, 1.243426, 1.244901, 1.256973, 1.255848, 1.254187, 1.256834, 1.271202, 1.270373, 1.273155, 1.279182, 1.286435, 1.275181, 1.275483, 1.257610, 1.132167, 1.163909, 1.179439, 1.135584, 1.143493, 1.139635, 1.162142, 1.146630, 1.140251, 1.210845, 1.231968, 1.213200, 1.211401, 1.211789, 1.220689, 1.221046, 1.236659, 1.237336, 1.227459, 1.235608, 1.244857, 1.243908, 1.247274, 1.254118, 1.261175, 1.251198, 1.245863, 1.226670, 1.108465, 1.139574, 1.154562, 1.097707, 1.113260, 1.113130, 1.111061, 1.103470, 1.125493, 1.176002, 1.202533, 1.185774, 1.182431, 1.187055, 1.192933, 1.190270, 1.200067, 1.200865, 1.201043, 1.197957, 1.216726, 1.215289, 1.219775, 1.244460, 1.230195, 1.220220, 1.214304, 1.187170, 1.081579, 1.115047, 1.126990, 1.062215, 1.073020, 1.072449, 1.072747, 1.093658, 1.065245, 1.137046, 1.160033, 1.166813, 1.159113, 1.158696, 1.168500, 1.176224, 1.177458, 1.176049, 1.177527, 1.194460, 1.180978, 1.180605, 1.182946, 1.190139, 1.191530, 1.193145, 1.185069, 1.150335, 1.059742, 1.091350, 1.101493, 1.040157, 1.045679, 1.036077, 1.043668, 1.044040, 1.033542, 1.100558, 1.134767, 1.138914, 1.138707, 1.137686, 1.138994, 1.137928, 1.141699, 1.185898, 1.154198, 1.138946, 1.158737, 1.151058, 1.153530, 1.160459, 1.166764, 1.156826, 1.150647, 1.124801, 1.038918, 1.067086, 1.084463, 1.007674, 1.017804, 1.014871, 1.014488, 1.017093, 1.033303, 1.068936, 1.090506, 1.121376, 1.113413, 1.119699, 1.120693, 1.119095, 1.131076, 1.122907, 1.133613, 1.114476, 1.142076, 1.104291, 1.132805, 1.133099, 1.142017, 1.146185, 1.126269, 1.091932, 1.016653, 1.086545, 1.060298, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.038077, 1.074598, 1.103010, 1.095256, 1.102633, 1.143426, 1.102720, 1.104560, 1.109598, 1.109057, 1.107692, 1.111018, 1.100855, 1.112122, 1.111549, 1.106951, 1.117613, 1.107565, 1.074493, 1.003659, 1.036376, 1.046378, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.018726, 1.058204, 1.076980, 1.073889, 1.076191, 1.077141, 1.075920, 1.091658, 1.091658, 1.079356, 1.090271, 1.079933, 1.079696, 1.080747, 1.091206, 1.082266, 1.081607, 1.069378, 1.041722, 1.000000, 1.016669, 1.018956, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.028275, 1.040284, 1.040510, 1.042076, 1.045636, 1.045923, 1.050276, 1.050721, 1.077816, 1.047166, 1.051137, 1.050572, 1.061542, 1.043422, 1.044104, 1.046123, 1.025588, 1.003596, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000526, 1.000110, 1.001580, 1.003231, 1.003303, 1.007173, 1.006385, 1.004558, 1.002023, 1.002172, 1.004252, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000}; // Mode, 9_2_8
   // float hcal[364] = {1.488772, 1.486679, 1.482133, 1.479425, 1.485548, 1.493674, 1.492273, 1.493985, 1.492969, 1.509587, 1.506320, 1.515023, 1.536133, 1.531514, 1.526063, 1.523588, 1.484326, 1.331186, 1.355782, 1.387601, 1.342361, 1.360238, 1.360894, 1.357810, 1.361534, 1.375109, 1.424183, 1.501489, 1.399359, 1.404418, 1.398637, 1.399352, 1.396019, 1.410175, 1.410339, 1.406340, 1.407406, 1.418949, 1.419240, 1.429573, 1.439777, 1.439575, 1.437873, 1.429671, 1.386724, 1.231026, 1.273743, 1.302278, 1.247894, 1.253293, 1.255920, 1.251581, 1.251463, 1.265636, 1.304193, 1.359426, 1.344773, 1.350364, 1.344524, 1.345861, 1.341056, 1.353025, 1.354453, 1.351831, 1.347695, 1.364280, 1.359560, 1.372041, 1.381087, 1.385518, 1.382776, 1.370359, 1.327976, 1.177840, 1.228646, 1.249099, 1.186989, 1.193231, 1.197696, 1.195938, 1.196179, 1.206994, 1.244052, 1.290444, 1.312420, 1.314244, 1.309209, 1.307359, 1.307022, 1.316532, 1.318803, 1.313482, 1.308246, 1.323321, 1.325338, 1.330967, 1.337016, 1.338398, 1.339131, 1.327637, 1.286923, 1.141686, 1.190420, 1.213207, 1.149381, 1.160818, 1.159674, 1.159706, 1.158536, 1.169460, 1.207328, 1.248669, 1.276808, 1.278511, 1.274205, 1.271484, 1.270841, 1.278961, 1.282849, 1.277440, 1.273669, 1.284206, 1.284441, 1.290392, 1.294976, 1.296487, 1.298681, 1.286720, 1.244613, 1.110049, 1.157259, 1.176192, 1.112071, 1.119705, 1.123068, 1.121734, 1.123006, 1.132017, 1.169278, 1.213867, 1.242737, 1.243424, 1.240171, 1.239669, 1.236894, 1.241291, 1.244473, 1.241839, 1.234634, 1.244791, 1.243586, 1.250908, 1.250071, 1.254379, 1.257426, 1.244129, 1.200212, 1.077383, 1.122736, 1.139789, 1.076388, 1.083750, 1.085063, 1.085238, 1.086152, 1.095831, 1.131103, 1.174074, 1.215358, 1.216519, 1.212013, 1.211151, 1.210772, 1.213001, 1.216205, 1.212945, 1.203300, 1.212112, 1.212353, 1.216219, 1.216911, 1.220303, 1.222827, 1.209306, 1.164908, 1.053285, 1.098127, 1.112139, 1.046242, 1.053812, 1.054951, 1.055403, 1.056634, 1.065248, 1.100811, 1.146619, 1.189579, 1.190152, 1.186635, 1.187759, 1.184085, 1.184657, 1.188523, 1.186424, 1.177457, 1.183637, 1.182490, 1.187512, 1.187172, 1.190456, 1.192421, 1.180374, 1.138839, 1.034745, 1.078450, 1.089012, 1.021600, 1.028598, 1.029529, 1.030437, 1.033001, 1.039217, 1.075602, 1.118267, 1.171107, 1.168946, 1.166512, 1.166769, 1.161480, 1.165436, 1.165121, 1.162166, 1.153355, 1.158267, 1.159683, 1.162556, 1.161758, 1.164033, 1.169004, 1.154110, 1.114707, 1.016696, 1.060155, 1.070569, 1.000000, 1.005364, 1.007959, 1.009434, 1.009694, 1.015478, 1.051155, 1.095691, 1.147927, 1.150166, 1.146134, 1.147374, 1.142142, 1.143955, 1.144191, 1.141270, 1.134016, 1.138813, 1.136992, 1.142244, 1.139741, 1.140879, 1.146482, 1.132095, 1.091087, 1.003826, 1.042366, 1.053090, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.023234, 1.031095, 1.075333, 1.124485, 1.126611, 1.122901, 1.121996, 1.119331, 1.121150, 1.122024, 1.116685, 1.110000, 1.112285, 1.113655, 1.114063, 1.112371, 1.111978, 1.116022, 1.101930, 1.061707, 1.000000, 1.024583, 1.031882, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.055449, 1.003816, 1.046213, 1.092452, 1.092536, 1.091150, 1.090404, 1.085964, 1.085791, 1.086160, 1.082304, 1.075379, 1.074526, 1.072966, 1.073412, 1.070047, 1.069312, 1.070556, 1.054325, 1.019816, 1.000000, 1.000000, 1.001951, 1.000000, 1.000000, 1.000000, 1.000000, 1.000301, 1.032098, 1.000000, 1.005659, 1.051117, 1.050717, 1.049425, 1.047891, 1.044951, 1.044487, 1.042311, 1.036290, 1.030471, 1.028289, 1.022935, 1.020965, 1.017667, 1.013806, 1.014022, 1.004382, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000, 1.000000}; // Mean, 9_2_8
   float hf[156] = {1.436933, 1.150784, 1.198317, 1.185131, 1.203083, 1.244493, 1.276614, 1.305569, 1.343967, 1.456317, 1.801191, 1.922477, 1.287897, 1.082326, 1.127774, 1.131999, 1.122464, 1.155969, 1.172212, 1.195422, 1.268606, 1.298257, 1.663198, 1.778371, 1.212180, 1.057017, 1.115133, 1.087006, 1.054219, 1.086285, 1.096476, 1.111732, 1.175957, 1.218147, 1.592375, 1.704887, 1.159324, 1.036555, 1.091943, 1.058415, 1.011008, 1.026250, 1.027465, 1.055655, 1.103695, 1.150204, 1.551786, 1.652949, 1.098260, 1.016998, 1.059197, 1.021185, 1.011008, 1.026250, 1.027465, 1.007086, 1.045239, 1.097873, 1.504194, 1.612279, 1.060359, 1.016998, 1.024919, 1.021185, 1.011008, 1.026250, 1.027465, 1.007086, 1.010229, 1.060789, 1.448109, 1.552224, 1.028576, 1.016998, 1.009009, 1.021185, 1.011008, 1.026250, 1.027465, 1.007086, 1.010229, 1.036400, 1.401057, 1.504891, 1.002432, 1.016998, 1.009009, 1.021185, 1.011008, 1.026250, 1.027465, 1.007086, 1.010229, 1.016859, 1.353666, 1.475716, 1.002432, 1.016998, 1.009009, 1.021185, 1.011008, 1.026250, 1.027465, 1.007086, 1.010229, 1.002650, 1.296711, 1.444925, 1.002432, 1.016998, 1.009009, 1.021185, 1.011008, 1.026250, 1.027465, 1.007086, 1.010229, 1.002650, 1.258159, 1.431994, 1.002432, 1.016998, 1.009009, 1.021185, 1.011008, 1.026250, 1.027465, 1.007086, 1.010229, 1.002650, 1.203263, 1.411718, 1.002432, 1.016998, 1.009009, 1.021185, 1.011008, 1.026250, 1.027465, 1.007086, 1.010229, 1.002650, 1.144271, 1.357477, 1.002432, 1.016998, 1.009009, 1.021185, 1.011008, 1.026250, 1.027465, 1.007086, 1.010229, 1.002650, 1.098340, 1.283960}; // Mode, 9_2_8
   // float hf[156] = {2.378339, 1.502094, 1.558828, 1.468909, 1.388092, 1.444754, 1.493556, 1.541491, 1.647650, 1.812072, 2.791145, 2.844066, 2.111653, 1.312496, 1.351124, 1.291042, 1.239054, 1.278956, 1.315620, 1.361558, 1.449292, 1.571425, 2.709180, 2.717564, 1.963179, 1.217324, 1.256356, 1.202818, 1.162660, 1.204208, 1.231526, 1.276481, 1.351362, 1.457253, 2.613049, 2.644112, 1.864273, 1.162345, 1.199680, 1.153738, 1.119396, 1.152063, 1.182551, 1.225995, 1.291988, 1.390649, 2.529912, 2.581591, 1.752451, 1.117623, 1.147027, 1.110546, 1.079779, 1.114737, 1.142444, 1.178901, 1.242175, 1.336171, 2.407025, 2.526142, 1.663160, 1.074331, 1.106646, 1.072905, 1.049034, 1.080200, 1.108287, 1.143216, 1.199594, 1.291001, 2.232567, 2.450402, 1.573166, 1.048392, 1.078650, 1.048091, 1.024573, 1.055920, 1.081953, 1.115248, 1.170655, 1.256432, 2.070575, 2.389922, 1.489765, 1.024323, 1.055465, 1.029036, 1.007379, 1.036369, 1.061089, 1.092431, 1.145947, 1.227190, 1.925361, 2.348549, 1.404872, 1.006701, 1.035613, 1.009332, 1.007379, 1.017418, 1.040979, 1.071060, 1.120826, 1.197973, 1.791211, 2.243741, 1.339055, 1.006701, 1.019214, 1.009332, 1.007379, 1.003242, 1.026977, 1.054007, 1.099699, 1.168445, 1.688074, 2.103020, 1.272889, 1.006701, 1.006044, 1.009332, 1.007379, 1.003242, 1.009030, 1.033555, 1.074019, 1.135660, 1.573541, 1.918549, 1.188140, 1.006701, 1.006044, 1.009332, 1.007379, 1.003242, 1.009030, 1.001923, 1.039081, 1.094883, 1.434509, 1.705331, 1.108268, 1.006701, 1.006044, 1.009332, 1.007379, 1.003242, 1.009030, 1.001923, 1.010006, 1.057960, 1.301315, 1.523940}; // Mean, 9_2_8
 };


unsigned int const PionCalibrations::N_TOWER_PHI = 72;
unsigned int const PionCalibrations::N_TOWER_ETA = 82; //41 towers! This includes HF  

PionCalibrations::PionCalibrations(const edm::ParameterSet& config) :
	edm::EDAnalyzer(),
	digis_(consumes<HcalTrigPrimDigiCollection>(config.getParameter<edm::InputTag>("triggerPrimitives"))),
	Edigis_(consumes<EcalTrigPrimDigiCollection>(config.getParameter<edm::InputTag>("eTriggerPrimitives"))),
	genSrc_(consumes<std::vector<reco::GenParticle>>(config.getParameter<edm::InputTag>("genSrc"))),
	detid_(config.getUntrackedParameter<bool>("useDetIdForUncompression", true)),
	threshold_(config.getUntrackedParameter<double>("threshold", 0.)),
	doClosure_(config.getUntrackedParameter<bool>("doClosure", false)),
	eTowerETCode(N_TOWER_PHI, vector<unsigned int>(N_TOWER_ETA)),
	eCorrTowerETCode(N_TOWER_PHI, vector<unsigned int>(N_TOWER_ETA)),
	hTowerETCode(N_TOWER_PHI, vector<unsigned int>(N_TOWER_ETA)),
	hCorrTowerETCode(N_TOWER_PHI, vector<unsigned int>(N_TOWER_ETA))
{
	edm::Service<TFileService> fs;


	Htps_ = fs->make<TTree>("Htps", "Trigger primitives");
	Htps_->Branch("event", &event_);
	Htps_->Branch("ieta", &tp_ieta_);
	Htps_->Branch("iphi", &tp_iphi_);
	Htps_->Branch("phi", &tp_phi_);
	Htps_->Branch("eta", &tp_eta_);
	Htps_->Branch("depth", &tp_depth_);
	Htps_->Branch("version", &tp_version_);
	Htps_->Branch("soi", &tp_soi_);
	Htps_->Branch("et", &tp_et_);


	Etps_ = fs->make<TTree>("Etps", "Trigger primitives");
	Etps_->Branch("event", &event_);
	Etps_->Branch("ieta", &etp_ieta_);
	Etps_->Branch("iphi", &etp_iphi_);
	Etps_->Branch("phi", &etp_phi_);
	Etps_->Branch("eta", &etp_eta_);
	Etps_->Branch("et", &etp_et_);

	pions_ = fs->make<TTree>("pions", "Pion quantities");
	pions_->Branch("event", &event_);
	pions_->Branch("et" , &pion_et_);
	pions_->Branch("pt" , &pion_pt_);
	pions_->Branch("eta" , &pion_eta_);
	pions_->Branch("phi" , &pion_phi_);
	pions_->Branch("ieta" , &pion_ieta_);
	pions_->Branch("iphi" , &pion_iphi_);

	matched_ = fs->make<TTree>("matched", "Matched quantities");
	matched_->Branch("event", &event_);
	matched_->Branch("gen_pt" , &gen_pt_);
	matched_->Branch("gen_et" , &gen_et_);
	matched_->Branch("gen_eta" , &gen_eta_);
	matched_->Branch("gen_phi" , &gen_phi_);
	matched_->Branch("gen_ieta" , &gen_ieta_);
	matched_->Branch("gen_iphi" , &gen_iphi_);
        matched_->Branch("l1_center_e" , &l1_center_e_);
        matched_->Branch("l1_center_h" , &l1_center_h_);
	matched_->Branch("l1_summed33" , &l1_summed33_);
	matched_->Branch("l1_summed33_e" , &l1_summed33_e_);
	matched_->Branch("l1_summed33_h" , &l1_summed33_h_);
	matched_->Branch("l1_summed55" , &l1_summed55_);
	matched_->Branch("l1_summed55_e" , &l1_summed55_e_);
	matched_->Branch("l1_summed55_h" , &l1_summed55_h_);
	// matched_->Branch("ETbin" , &ETbin_);
	matched_->Branch("HoERatio" , &HoE_);
        matched_->Branch("corr_center_e", &corr_center_e_);
        matched_->Branch("corr_center_h", &corr_center_h_); //corrH is defined to be hcalSF*(uncorrH+corrE)-corrE
	matched_->Branch("sumCorr33" , &sumCorr33_);
	matched_->Branch("sumCorr33_e" , &sumCorr33_e_);
	matched_->Branch("sumCorr33_h" , &sumCorr33_h_); //corrH is defined to be hcalSF*(uncorrH+corrE)-corrE
	matched_->Branch("sumCorr" , &sumCorr_);
	matched_->Branch("sumCorr_e" , &sumCorr_e_);
	matched_->Branch("sumCorr_h" , &sumCorr_h_); //corrH is defined to be hcalSF*(uncorrH+corrE)-corrE

	matched_->Branch("l1_square55_e", &l1_square55_e_);
	matched_->Branch("l1_square55_h", &l1_square55_h_);

}

PionCalibrations::~PionCalibrations() {}

	void
PionCalibrations::analyze(const edm::Event& event, const edm::EventSetup& setup)
{

	event_ = event.id().event();

	Handle<HcalTrigPrimDigiCollection> digis;
	if (!event.getByToken(digis_, digis)) {
		LogError("PionCalibrations") <<
			"Can't find hcal trigger primitive digi collection"<<std::endl;
		return;
	}

	Handle<EcalTrigPrimDigiCollection> Edigis;
	if (!event.getByToken(Edigis_, Edigis)) {
		LogError("PionCalibrations") <<
			"Can't find ecal trigger primitive digi collection" << std::endl;
		return;
	}

	edm::Handle<std::vector<reco::GenParticle> > objects;
	if (!event.getByToken(genSrc_, objects)) {
		LogError("PionCalibrations") <<
			"Can't find genParticle collection" << std::endl;
		return;
	}

	for(const auto& pion: *objects){
		pion_et_=pion.et();
		pion_pt_=pion.pt();
		pion_eta_=pion.eta();
		pion_phi_=pion.phi();
		pion_ieta_=convertTPGGenEta(pion.eta());
		pion_iphi_=convertGenPhi(pion.phi());
		pions_->Fill();
	}

	ESHandle<CaloTPGTranscoder> decoder;
	setup.get<CaloTPGRecord>().get(decoder);

	std::unordered_map<int, std::unordered_map<int, double>> new_ets;
	std::unordered_map<int, std::unordered_map<int, int>> new_counts;


	ESHandle<HcalTrigTowerGeometry> tpd_geo;
	setup.get<CaloGeometryRecord>().get(tpd_geo);
	
	for (unsigned int i = 0; i < hTowerETCode.size(); i++)
	{
		hTowerETCode[i].clear();
		hCorrTowerETCode[i].clear();
	}

	std::map<HcalTrigTowerDetId, HcalTriggerPrimitiveDigi> ttids;
	for (const auto& digi: *digis) {
		//	if (digi.id().version() == 1 || digi.id().ieta()>29) continue; //No HF
		ttids[digi.id()] = digi;
		HcalTrigTowerDetId id = digi.id();
		tp_et_ = decoder->hcaletValue(id, digi.t0());
		if (tp_et_ < threshold_) continue;
		tp_ieta_ = id.ieta();
		tp_iphi_ = id.iphi();
                // if (abs(tp_ieta_)>28) continue; //ignore HF for now in HCAL vecotr 
                // TPG iEta starts at 0 and goes to 55 for ECAL; FIXME in helpers? Will be different for hcal 
                // TPG iPhi starts at 1 and goes to 72.  Let's index starting at zero.
                // int ieta = TPGEtaRange(tp_ieta_);//avoid negative eta
                int ieta = HCALTPGEtaRange(tp_ieta_);//avoid negative eta
                int iphi =  tp_iphi_-1; //zero index
		tp_eta_ = convertTPGEta(ieta); //FIXME
		tp_phi_ = convertTPGPhi(iphi); //CHECKME/FIXME should require zero index
		tp_depth_ = id.depth();
		tp_version_ = id.version();
		tp_soi_ = digi.SOI_compressedEt();
                hTowerETCode[iphi][ieta] = tp_et_*2; //add "uncompressed et" e.g. divide this by two later for 0.5 GeV precision 
                hCorrTowerETCode[iphi][ieta] = tp_et_*2; //add "uncompressed et" e.g. divide this by two later for 0.5 GeV precision 
                
                // Fill hCorrTowerETCode with calibrated HCAL TP ET (times 2)
                // Make a first pass for HBHE in case nothing is found in ECAL
            		int ETbin = 0;
						    if (tp_et_ < 15) ETbin = floor(tp_et_/3) - 1;
							  else if (tp_et_ >= 15 && tp_et_ < 45) ETbin = floor(tp_et_/5) + 1;
							  else if (tp_et_ >= 45 && tp_et_ < 55) ETbin = 10;
							  else if (tp_et_ >= 55 && tp_et_ < 70) ETbin = 11;
							  else if (tp_et_ >= 70) ETbin = 12;
							  if (ETbin<0) ETbin=0;
							  else if (ETbin>12) ETbin=12;
								// ieta is in [0,81], but if in B/E we need to convert to [0,27] to reference hcal[], and if in HF we need to convert to [0,11] to reference hf[]
								// Start by computing foldedEta, mapping [0,81] to [0,40]
								int foldedEta = 0;
								ieta < 41 ? foldedEta = 40 - ieta : foldedEta = ieta - 41;
								// foldedEta < 28 -> barrel/encap; foldedEta > 28 -> HF (skip 28, which corresponds to iEta +-29)
								if (foldedEta < 28) hCorrTowerETCode[iphi][ieta] = tp_et_*2*hcal[ETbin*28+foldedEta];
								else if (foldedEta > 28) {
									foldedEta = foldedEta - 29; // Map [29,40] to [0,11]
									hCorrTowerETCode[iphi][ieta] = hCorrTowerETCode[iphi][ieta] = tp_et_*2*hf[ETbin*12+foldedEta];
								}

		Htps_->Fill();


	}//end for of hcal digis
	
	for (unsigned int i = 0; i < eTowerETCode.size(); i++)
	{
		eTowerETCode[i].clear();
		eCorrTowerETCode[i].clear();
	}
	for (const auto& Edigi: *Edigis) {
		double ecalet = Edigi.compressedEt(); //0.5 GeV LSB; Divide ecalet by two later to get actual tower ET
		etp_et_ = ecalet;
		etp_ieta_ = Edigi.id().ieta();
		etp_iphi_ = Edigi.id().iphi();
		// TPG iPhi starts at 1 and goes to 72.  Let's index starting at zero.
		// TPG iEta starts at 0 and goes to 55 for ECAL. (Will be different for hcal?)
		int iphi =  etp_iphi_ -1; //zero index
		int ieta = TPGEtaRange(etp_ieta_); // get rid of negative etas
		ieta += 13; // Shift from 0-55 to 13-68 (within 0-81)
		etp_phi_ = convertTPGPhi(iphi);//should require zero index
		etp_eta_ = convertTPGEta(ieta);//should not allow negatives Range 0-55 (only EBEE)
		eTowerETCode[iphi][ieta] = ecalet; //compressed et!!! easily save the et in a vector of ints (divide by 2 later) 
		eCorrTowerETCode[iphi][ieta] = ecalet; //compressed et!!! easily save the et in a vector of ints (divide by 2 later) 
				
		// ecalet = 2.0 * actual tower ET
		int ETbin = 0;
    if (ecalet < 30) ETbin = floor(ecalet*0.5/3) - 1;
	  else if (ecalet >= 30 && ecalet < 90) ETbin = floor(ecalet*0.5/5) + 1;
	  else if (ecalet >= 90 && ecalet < 110) ETbin = 10;
	  else if (ecalet >= 110 && ecalet < 140) ETbin = 11;
	  else if (ecalet >= 140) ETbin = 12;
	  if (ETbin<0) ETbin=0;
	  else if (ETbin>12) ETbin=12;
		int adj_ieta = ieta-13; // shift from 13-68 back to 0-55
		// ieta is in [0,55], but need to convert to [0,27] to reference ecal[]
		adj_ieta = ieta-28;
		if (adj_ieta < 0)
			adj_ieta = (-adj_ieta) - 1;
		eCorrTowerETCode[iphi][ieta] = ecalet*ecal[ETbin*28+adj_ieta]; 
		
		// Include ECAL TP ET in hCorrTowerETCode
		double hcalet = hTowerETCode[iphi][ieta]; // hcalet = 2.0 * actual tower ET
		double ecalet_corr = eCorrTowerETCode[iphi][ieta];
		int ETbin_forHCAL = 0;
    if (hcalet < 30) ETbin_forHCAL = floor(hcalet*0.5/3) - 1;
	  else if (hcalet >= 30 && hcalet < 90) ETbin_forHCAL = floor(hcalet*0.5/5) + 1;
	  else if (hcalet >= 90 && hcalet < 110) ETbin_forHCAL = 10;
	  else if (hcalet >= 110 && hcalet < 140) ETbin_forHCAL = 11;
	  else if (hcalet >= 140) ETbin_forHCAL = 12;
	  if (ETbin_forHCAL<0) ETbin_forHCAL=0;
	  else if (ETbin_forHCAL>12) ETbin_forHCAL=12;
		hCorrTowerETCode[iphi][ieta] = hcal[ETbin_forHCAL*28+adj_ieta]*(hcalet+ecalet_corr) - ecalet_corr;
		
		Etps_->Fill();
	}

	for (const auto& pion: *objects){
		HoE_=0;
		l1_summed55_=0;
		sumCorr_=0;
		l1_summed55_e_=0;
		sumCorr_e_=0;
		l1_summed55_h_=0;
		sumCorr_h_=0;
		
		l1_square55_e_.clear();
		l1_square55_h_.clear();
		for(unsigned int i = 0; i < 5; i++){
			vector<double> blank_e;
			blank_e.clear();
			vector<double> blank_h;
			blank_h.clear();
			for(unsigned int j = 0; j < 5; j++){
				blank_e.push_back(0.0);
				blank_h.push_back(0.0);
			}
			l1_square55_e_.push_back(blank_e);
			l1_square55_h_.push_back(blank_h);
		}

		gen_pt_=pion.pt();
		gen_eta_=pion.eta();
		gen_phi_=pion.phi();
		gen_ieta_=convertTPGGenEta(pion.eta());
		if(gen_ieta_ == -999){
			int unshifted_gen_ieta_ = convertHFGenEta(pion.eta());
			gen_ieta_ = HCALTPGEtaRange(unshifted_gen_ieta_);
		}
		else
			gen_ieta_ += 13;
		if(gen_ieta_==69 || gen_ieta_==12) continue; // ignore tower 29
		gen_iphi_=convertGenPhi(pion.phi());
                //iETA NEGATIVE
		// ETbin_=0;
		double TPGhCenter_=0;
		double cTPGhCenter_=0;
		double TPGeCenter_=0;
		double cTPGeCenter_=0;
		double TPGh3x3_=0;
		double cTPGh3x3_=0;
		double TPGe3x3_=0;
		double cTPGe3x3_=0;
		double TPG3x3_=0;
		double cTPG3x3_=0;
		double TPGh5x5_=0;
		double cTPGh5x5_=0;
		double TPGe5x5_=0;
		double cTPGe5x5_=0;
		double TPG5x5_=0;
		double cTPG5x5_=0;

		for (int i = -2; i < 3; ++i) {//eta
			for (int j = -2; j < 3; ++j) { //phi
				int tpgsquarephi= gen_iphi_+j;
				int tpgsquareeta= gen_ieta_+i;	

				if (tpgsquarephi==-1) {tpgsquarephi=71;}
				if (tpgsquarephi==-2) {tpgsquarephi=70;}
				if (tpgsquarephi==-3) {tpgsquarephi=69;}
				if (tpgsquarephi==-4) {tpgsquarephi=68;}
				if (tpgsquarephi==-5) {tpgsquarephi=67;}
				if (tpgsquarephi==72) {tpgsquarephi=0;}
				if (tpgsquarephi==73) {tpgsquarephi=1;}
				if (tpgsquarephi==74) {tpgsquarephi=2;}
				if (tpgsquarephi==75) {tpgsquarephi=3;}
				if (tpgsquarephi==76) {tpgsquarephi=4;}
				if (tpgsquareeta>81 || tpgsquareeta<0 || tpgsquareeta==69 || tpgsquareeta==12) {continue;}//No Eta values beyond 81; ignore 29
				if (gen_ieta_ > 12 && gen_ieta_ < 69 && (tpgsquareeta <= 12 || tpgsquareeta >= 69)){continue;}//If pion in HE, ignore HF towers
				if ((gen_ieta_ > 69 && tpgsquareeta <= 69) || (gen_ieta_ < 12 && tpgsquareeta >= 12)){continue;}//If pion in HF, ignore HE towers
				
				l1_square55_e_[j+2][i+2] = eTowerETCode[tpgsquarephi][tpgsquareeta]*0.5;
				l1_square55_h_[j+2][i+2] = hTowerETCode[tpgsquarephi][tpgsquareeta]*0.5;

				if (i == 0 && j == 0)
				{
					TPGhCenter_ = hTowerETCode[tpgsquarephi][tpgsquareeta];
					cTPGhCenter_ = hCorrTowerETCode[tpgsquarephi][tpgsquareeta];
					TPGeCenter_ = eTowerETCode[tpgsquarephi][tpgsquareeta];
					cTPGeCenter_ = eCorrTowerETCode[tpgsquarephi][tpgsquareeta];
				}
				if (std::abs(i) < 2 && std::abs(j) < 2)
				{
					TPGh3x3_ += hTowerETCode[tpgsquarephi][tpgsquareeta];		
					cTPGh3x3_ += hCorrTowerETCode[tpgsquarephi][tpgsquareeta];		
					TPGe3x3_ += eTowerETCode[tpgsquarephi][tpgsquareeta];		
					cTPGe3x3_ += eCorrTowerETCode[tpgsquarephi][tpgsquareeta];		
					TPG3x3_ += hTowerETCode[tpgsquarephi][tpgsquareeta];	
					TPG3x3_ += eTowerETCode[tpgsquarephi][tpgsquareeta];	
					cTPG3x3_ += hCorrTowerETCode[tpgsquarephi][tpgsquareeta];	
					cTPG3x3_ += eCorrTowerETCode[tpgsquarephi][tpgsquareeta];		
				}
				TPGh5x5_ += hTowerETCode[tpgsquarephi][tpgsquareeta];		
				cTPGh5x5_ += hCorrTowerETCode[tpgsquarephi][tpgsquareeta];		
				TPGe5x5_ += eTowerETCode[tpgsquarephi][tpgsquareeta];		
				cTPGe5x5_ += eCorrTowerETCode[tpgsquarephi][tpgsquareeta];		
				TPG5x5_ += hTowerETCode[tpgsquarephi][tpgsquareeta];	
				TPG5x5_ += eTowerETCode[tpgsquarephi][tpgsquareeta];	
				cTPG5x5_ += hCorrTowerETCode[tpgsquarephi][tpgsquareeta];	
				cTPG5x5_ += eCorrTowerETCode[tpgsquarephi][tpgsquareeta];		
			}
		}
		//FILL ISOLATION PROCEDURE
		//
	
		//LSB = 0.5 
		l1_center_h_=TPGhCenter_*0.5;
		corr_center_h_=cTPGhCenter_*0.5;
		l1_center_e_=TPGeCenter_*0.5;
		corr_center_e_=cTPGeCenter_*0.5;
		l1_summed33_h_=TPGh3x3_*0.5;
		sumCorr33_h_=cTPGh3x3_*0.5;
		l1_summed33_e_=TPGe3x3_*0.5;
		sumCorr33_e_=cTPGe3x3_*0.5;
		l1_summed33_=TPG3x3_*0.5;
		sumCorr33_=cTPG3x3_*0.5;
		l1_summed55_h_=TPGh5x5_*0.5;
		sumCorr_h_=cTPGh5x5_*0.5;
		l1_summed55_e_=TPGe5x5_*0.5;
		sumCorr_e_=cTPGe5x5_*0.5;
		l1_summed55_=TPG5x5_*0.5;
		sumCorr_=cTPG5x5_*0.5;
		HoE_=TPGh5x5_/TPGe5x5_;
		matched_->Fill();
	}

}

void
PionCalibrations::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
	//The following says we do not know what parameters are allowed so do no validation
	// Please change this to state exactly what you do use, even if it is no parameters
	edm::ParameterSetDescription desc;
	desc.setUnknown();
	descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(PionCalibrations);
