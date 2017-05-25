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

#include "L1Trigger/CaloL1-Calibrations/interface/helpers.h"

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
	
		// float ecal[252] = {1.208190, 1.193831, 1.193843, 1.214704, 1.192821, 1.220908, 1.218467, 1.223580, 1.217246, 1.237422, 1.242979, 1.251475, 1.270360, 1.316498, 1.304969, 1.313628, 1.412251, 2.141862, 1.416868, 1.528588, 1.537433, 1.530344, 1.513922, 1.553387, 1.567000, 1.541610, 1.457139, 1.487300, 1.127397, 1.140318, 1.153732, 1.177768, 1.152771, 1.155775, 1.160308, 1.158241, 1.169187, 1.174276, 1.170810, 1.188320, 1.200725, 1.209210, 1.213054, 1.235987, 1.312487, 1.937033, 1.270815, 1.359124, 1.394787, 1.368162, 1.364445, 1.395063, 1.434056, 1.420153, 1.346325, 1.402988, 1.089261, 1.084059, 1.090366, 1.089138, 1.090491, 1.103439, 1.092586, 1.096681, 1.112075, 1.115814, 1.114636, 1.118974, 1.139433, 1.152043, 1.155630, 1.157002, 1.205450, 1.854968, 1.225174, 1.299449, 1.353789, 1.316810, 1.314123, 1.349183, 1.395382, 1.381582, 1.317593, 1.384600, 1.071482, 1.067483, 1.067462, 1.066326, 1.071064, 1.077144, 1.073465, 1.072841, 1.086271, 1.104900, 1.081486, 1.086756, 1.096188, 1.114686, 1.122217, 1.129874, 1.168171, 1.812662, 1.202279, 1.279068, 1.326350, 1.295637, 1.290608, 1.324722, 1.369783, 1.361360, 1.299822, 1.372281, 1.061298, 1.057444, 1.055856, 1.055508, 1.056166, 1.074645, 1.066611, 1.061034, 1.065241, 1.084247, 1.077634, 1.076026, 1.082194, 1.097146, 1.109076, 1.121422, 1.142658, 1.769411, 1.183381, 1.252022, 1.315308, 1.265650, 1.268436, 1.305292, 1.349661, 1.337928, 1.285204, 1.357143, 1.050072, 1.047984, 1.048092, 1.045895, 1.049023, 1.070026, 1.054519, 1.058549, 1.056486, 1.078440, 1.063950, 1.065979, 1.077038, 1.091099, 1.080287, 1.101142, 1.130997, 1.661993, 1.181250, 1.230554, 1.275224, 1.256848, 1.264708, 1.297300, 1.342283, 1.332615, 1.279686, 1.355711, 1.048233, 1.049490, 1.046896, 1.044864, 1.044078, 1.057606, 1.049355, 1.054238, 1.055968, 1.070471, 1.059268, 1.057748, 1.068407, 1.096938, 1.077940, 1.084436, 1.123254, 1.699847, 1.164002, 1.231507, 1.277487, 1.251166, 1.249815, 1.280204, 1.329053, 1.321746, 1.273126, 1.349214, 1.038026, 1.032367, 1.035255, 1.039838, 1.042236, 1.062323, 1.047012, 1.048638, 1.048305, 1.068980, 1.050191, 1.051813, 1.064593, 1.083348, 1.064224, 1.076602, 1.115396, 1.625167, 1.165931, 1.218367, 1.249837, 1.242801, 1.241377, 1.276845, 1.319916, 1.315425, 1.269162, 1.345198, 1.117350, 1.117560, 1.117560, 1.118255, 1.119337, 1.125571, 1.121147, 1.121547, 1.123242, 1.128062, 1.123738, 1.125514, 1.128207, 1.135966, 1.132615, 1.136350, 1.155429, 1.319682, 1.190906, 1.211385, 1.204970, 1.224400, 1.225175, 1.246255, 1.277491, 1.270270, 1.277960, 1.309594}; // 90% center/3x3, TPGe3x3 > 3 GeV
  // float ecal[364] = {1.231476, 1.208928, 1.213153, 1.213960, 1.208616, 1.218808, 1.222724, 1.215649, 1.221270, 1.243319, 1.254309, 1.262624, 1.324735, 1.331397, 1.328709, 1.345573, 1.446714, 2.284350, 1.516291, 1.651486, 1.655905, 1.632875, 1.602305, 1.648992, 1.653671, 1.615318, 1.486803, 1.509237, 1.201642, 1.186684, 1.186886, 1.208589, 1.185878, 1.223606, 1.225812, 1.234239, 1.226761, 1.226034, 1.245328, 1.244821, 1.245654, 1.304492, 1.291312, 1.292491, 1.408760, 2.090021, 1.376684, 1.479732, 1.471061, 1.474819, 1.469846, 1.505578, 1.523535, 1.506533, 1.396857, 1.439003, 1.161093, 1.165547, 1.175403, 1.218569, 1.166175, 1.194218, 1.173935, 1.187290, 1.192620, 1.212291, 1.198332, 1.221390, 1.232138, 1.260660, 1.259603, 1.270620, 1.354314, 1.945932, 1.291009, 1.381277, 1.425722, 1.407875, 1.401803, 1.430035, 1.453640, 1.450941, 1.355950, 1.414619, 1.108466, 1.128219, 1.136266, 1.156532, 1.146742, 1.137908, 1.155059, 1.145168, 1.149653, 1.162492, 1.156848, 1.174114, 1.175858, 1.193243, 1.190897, 1.219790, 1.277702, 1.938356, 1.263141, 1.342024, 1.381876, 1.347431, 1.345460, 1.377356, 1.427490, 1.403457, 1.338620, 1.396308, 1.089261, 1.084059, 1.090366, 1.089138, 1.090491, 1.103439, 1.092586, 1.096681, 1.112075, 1.115814, 1.114636, 1.118974, 1.139433, 1.152043, 1.155630, 1.157002, 1.205450, 1.854968, 1.225174, 1.299449, 1.353789, 1.316810, 1.314123, 1.349183, 1.395382, 1.381582, 1.312940, 1.375910, 1.071482, 1.067483, 1.067462, 1.066326, 1.071064, 1.077144, 1.073465, 1.072841, 1.086271, 1.104900, 1.081486, 1.086756, 1.096188, 1.114686, 1.122217, 1.129874, 1.168171, 1.812662, 1.202279, 1.279068, 1.326350, 1.295637, 1.290608, 1.324722, 1.369783, 1.361360, 1.295710, 1.360797, 1.059307, 1.055601, 1.055856, 1.055508, 1.056166, 1.070942, 1.066611, 1.061034, 1.065241, 1.082664, 1.077634, 1.076026, 1.082194, 1.097146, 1.109076, 1.116869, 1.140673, 1.665281, 1.183381, 1.249896, 1.274068, 1.265650, 1.266800, 1.305292, 1.346499, 1.334355, 1.281359, 1.349975, 1.050072, 1.044950, 1.048092, 1.045895, 1.049023, 1.064790, 1.054519, 1.058549, 1.054929, 1.071934, 1.063950, 1.065979, 1.077038, 1.085691, 1.080287, 1.098893, 1.129038, 1.507060, 1.177441, 1.230554, 1.229544, 1.253509, 1.261211, 1.296229, 1.338864, 1.331946, 1.276401, 1.346700, 1.044311, 1.045929, 1.045077, 1.044864, 1.042537, 1.054683, 1.048072, 1.049351, 1.053590, 1.067867, 1.059268, 1.056406, 1.067372, 1.092129, 1.075204, 1.082284, 1.119690, 1.487062, 1.164002, 1.221148, 1.211224, 1.244501, 1.245543, 1.275679, 1.320096, 1.317911, 1.259098, 1.331564, 1.036808, 1.032367, 1.033880, 1.038856, 1.039717, 1.056261, 1.043021, 1.046883, 1.046279, 1.062554, 1.047007, 1.051813, 1.061384, 1.077448, 1.064224, 1.074008, 1.110445, 1.412303, 1.161879, 1.209506, 1.201349, 1.237743, 1.239527, 1.274067, 1.311268, 1.309720, 1.206784, 1.281713, 1.034101, 1.028891, 1.030929, 1.032736, 1.032742, 1.048121, 1.035785, 1.037995, 1.038169, 1.051801, 1.042632, 1.043239, 1.051890, 1.064413, 1.058864, 1.066784, 1.097950, 1.340684, 1.151049, 1.192593, 1.188888, 1.221928, 1.222114, 1.261393, 1.297003, 1.294559, 1.098475, 1.090355, 1.024943, 1.022789, 1.023820, 1.023892, 1.025377, 1.037568, 1.029187, 1.028533, 1.030980, 1.041339, 1.031896, 1.034638, 1.040421, 1.055346, 1.048091, 1.054738, 1.080429, 1.271459, 1.140331, 1.178228, 1.174513, 1.207549, 1.215407, 1.249970, 1.286625, 1.284373, 1.000000, 1.000000, 1.018917, 1.016861, 1.017496, 1.017913, 1.019881, 1.027723, 1.020904, 1.022598, 1.024026, 1.031355, 1.025531, 1.027109, 1.033275, 1.043459, 1.039817, 1.044024, 1.063082, 1.203810, 1.127773, 1.158036, 1.153636, 1.179192, 1.181573, 1.203633, 1.236527, 1.223226, 1.000000, 1.000000}; // 90% center/3x3, TPGe3x3 > 3 GeV, genPhoPt < 125 GeV, min SF = 1.000000
   
   // float ecal[364] = {1.119974, 1.137018, 1.130883, 1.129678, 1.130041, 1.127207, 1.124656, 1.133294, 1.135318, 1.129183, 1.132421, 1.127110, 1.131243, 1.137500, 1.125751, 1.128942, 1.150045, 1.430908, 1.204760, 1.346070, 1.336213, 1.370062, 1.393691, 1.506774, 1.532985, 1.523253, 1.440226, 1.514107, 1.083458, 1.088212, 1.089936, 1.093921, 1.090387, 1.088164, 1.090377, 1.093799, 1.088938, 1.084879, 1.091404, 1.089761, 1.090559, 1.101873, 1.091828, 1.089970, 1.104742, 1.350578, 1.179811, 1.263306, 1.257441, 1.328798, 1.384993, 1.407375, 1.453402, 1.451094, 1.410557, 1.405290, 1.064812, 1.065712, 1.063012, 1.057444, 1.062879, 1.066116, 1.070599, 1.066663, 1.069633, 1.067560, 1.065884, 1.072179, 1.068451, 1.070914, 1.069204, 1.068418, 1.082723, 1.285564, 1.156553, 1.206729, 1.224918, 1.314733, 1.326699, 1.394201, 1.394864, 1.407732, 1.361271, 1.377775, 1.046928, 1.048195, 1.047900, 1.046159, 1.047827, 1.048260, 1.050228, 1.050648, 1.051581, 1.053247, 1.052816, 1.058339, 1.055687, 1.058953, 1.060128, 1.058107, 1.062246, 1.237738, 1.146385, 1.199365, 1.210367, 1.289966, 1.302556, 1.336799, 1.383672, 1.358862, 1.349935, 1.365479, 1.040894, 1.037608, 1.036712, 1.039901, 1.040222, 1.042710, 1.038373, 1.045120, 1.045232, 1.043503, 1.045144, 1.047226, 1.048568, 1.048010, 1.041316, 1.046387, 1.058259, 1.215451, 1.132300, 1.187170, 1.205522, 1.276262, 1.272435, 1.357533, 1.350847, 1.419551, 1.326225, 1.350992, 1.031939, 1.032265, 1.030075, 1.030722, 1.032947, 1.033734, 1.029981, 1.035661, 1.036366, 1.034582, 1.038130, 1.038495, 1.041036, 1.040277, 1.042074, 1.037345, 1.042986, 1.204778, 1.121578, 1.167640, 1.181280, 1.241490, 1.249574, 1.322658, 1.380270, 1.312183, 1.314694, 1.433279, 1.024938, 1.025509, 1.023756, 1.024768, 1.028016, 1.024053, 1.025151, 1.029714, 1.031280, 1.028153, 1.029108, 1.034672, 1.035088, 1.035485, 1.035425, 1.030921, 1.035286, 1.183772, 1.121352, 1.173454, 1.189430, 1.229655, 1.232626, 1.279408, 1.311512, 1.320535, 1.250878, 1.383151, 1.019513, 1.019618, 1.019204, 1.018834, 1.022974, 1.022908, 1.020755, 1.024202, 1.026904, 1.023369, 1.023972, 1.027892, 1.033798, 1.027385, 1.029245, 1.028285, 1.034477, 1.165892, 1.119740, 1.153680, 1.149763, 1.211771, 1.219994, 1.305724, 1.296463, 1.303058, 1.299991, 1.382124, 1.015691, 1.016185, 1.014119, 1.015780, 1.019400, 1.019295, 1.015197, 1.022786, 1.021406, 1.021086, 1.022585, 1.024652, 1.029811, 1.026212, 1.025407, 1.027974, 1.029525, 1.175521, 1.117686, 1.151020, 1.158437, 1.208777, 1.236807, 1.265954, 1.345086, 1.285469, 1.276712, 1.373093, 1.010777, 1.014901, 1.012442, 1.012455, 1.014412, 1.015092, 1.013139, 1.018499, 1.022926, 1.018472, 1.021256, 1.021942, 1.027232, 1.024771, 1.024256, 1.022187, 1.028147, 1.161713, 1.100158, 1.137876, 1.142112, 6434.497940, 1.205765, 1.232275, 1.331629, 1.291962, 1.240671, 1.240007, 1.010994, 1.010082, 1.010540, 1.009084, 1.012683, 1.011982, 1.011589, 1.013616, 1.016348, 1.014766, 1.014374, 1.020283, 1.023327, 1.020288, 1.024421, 1.019464, 1.023091, 1.144736, 1.105701, 1.135751, 1.132751, 1.182500, 1.188998, 1.231027, 1.334055, 1.275021, 1.119245, 1.198556, 1.006412, 1.007943, 1.007441, 1.005918, 1.008423, 1.006728, 1.008028, 1.011924, 1.013576, 1.009289, 1.013604, 1.017471, 1.021669, 1.017841, 1.021837, 1.019624, 1.020834, 1.135556, 1.099984, 1.130754, 1.127277, 1.169267, 1.186532, 1.243116, 1.320536, 1.249596, 1.000000, 1.000000, 1.004021, 1.003420, 1.004326, 1.002428, 1.005777, 1.004605, 1.004239, 1.009848, 1.012610, 1.008506, 1.023180, 1.013259, 1.021146, 1.012670, 1.021540, 1.019173, 1.023531, 1.151531, 1.100064, 1.130605, 1.125264, 1.156489, 1.181470, 1.218039, 1.266191, 1.239087, 1.000000, 1.000000}; // fit peak, 90% center/3x3, TPGe3x3 > 3 GeV, genPhoPt < 125 GeV, min SF = 1.000000

    float hcal[364] = {1.291597, 1.281512, 1.282797, 1.283375, 1.287817, 1.300540, 1.295717, 1.294555, 1.305190, 1.325019, 1.327609, 1.339178, 1.357170, 1.378408, 1.382951, 1.400904, 1.397638, 1.292991, 1.308859, 1.331983, 1.305646, 1.322441, 1.329798, 1.340836, 1.362193, 1.374412, 1.445627, 1.454658, 1.260286, 1.256308, 1.258914, 1.259544, 1.262581, 1.276044, 1.273759, 1.273611, 1.283693, 1.300846, 1.301984, 1.315088, 1.329091, 1.346360, 1.347310, 1.358521, 1.349223, 1.232584, 1.271552, 1.291969, 1.254593, 1.266586, 1.273881, 1.268912, 1.259153, 1.244947, 1.252983, 1.255522, 1.243070, 1.239731, 1.238269, 1.245139, 1.245133, 1.255732, 1.256336, 1.255902, 1.265544, 1.281294, 1.281555, 1.293771, 1.309039, 1.322110, 1.320160, 1.325785, 1.309535, 1.196610, 1.246161, 1.263598, 1.201962, 1.210998, 1.204896, 1.190002, 1.159601, 1.131034, 1.132322, 1.120736, 1.227814, 1.222941, 1.225455, 1.227074, 1.229010, 1.241908, 1.240778, 1.240301, 1.247685, 1.262508, 1.265829, 1.274698, 1.286061, 1.296581, 1.288525, 1.294280, 1.269369, 1.165258, 1.218063, 1.235784, 1.153559, 1.165755, 1.149996, 1.124426, 1.085695, 1.059916, 1.077493, 1.228656, 1.209842, 1.208001, 1.207907, 1.210234, 1.210352, 1.222297, 1.220610, 1.220366, 1.225283, 1.241171, 1.242011, 1.248464, 1.257960, 1.265013, 1.254345, 1.254297, 1.223682, 1.140593, 1.187742, 1.205950, 1.099010, 1.100099, 1.090908, 1.048935, 1.021541, 1.101607, 1.156529, 1.177498, 1.190112, 1.185285, 1.187130, 1.188578, 1.187478, 1.197028, 1.197187, 1.196109, 1.199080, 1.208884, 1.210051, 1.216120, 1.223826, 1.231199, 1.215691, 1.212695, 1.181808, 1.118545, 1.164088, 1.167916, 1.050711, 1.039242, 1.021400, 1.007655, 1.073926, 1.088175, 1.087068, 1.104320, 1.168920, 1.167729, 1.169431, 1.169104, 1.166411, 1.175946, 1.176562, 1.175118, 1.175507, 1.182185, 1.183441, 1.194450, 1.190980, 1.201834, 1.185047, 1.176638, 1.144747, 1.095652, 1.125623, 1.131356, 1.050711, 1.013966, 1.053482, 1.073566, 1.061255, 1.061593, 1.053950, 1.033547, 1.148153, 1.146960, 1.148922, 1.149890, 1.145633, 1.154464, 1.152721, 1.153451, 1.153909, 1.156378, 1.161108, 1.162272, 1.186698, 1.162670, 1.160943, 1.171636, 1.100933, 1.073922, 1.098163, 1.098157, 1.028963, 1.076060, 1.066764, 1.041274, 1.044568, 1.021103, 1.053950, 1.033547, 1.131788, 1.128602, 1.128919, 1.130866, 1.128219, 1.133883, 1.134694, 1.132352, 1.131551, 1.142822, 1.139099, 1.143659, 1.137190, 1.127117, 1.121801, 1.101760, 1.069957, 1.055335, 1.073439, 1.078128, 1.045000, 1.045738, 1.036112, 1.030923, 1.020008, 1.001194, 1.053950, 1.033547, 1.114288, 1.111364, 1.115670, 1.115167, 1.111187, 1.116740, 1.122936, 1.116716, 1.114636, 1.121486, 1.119196, 1.119832, 1.118741, 1.109098, 1.098190, 1.072062, 1.036983, 1.042310, 1.055170, 1.053083, 1.029483, 1.023241, 1.015916, 1.010982, 1.020008, 1.001194, 1.053950, 1.033547, 1.096107, 1.094318, 1.094461, 1.095799, 1.092779, 1.098089, 1.096621, 1.094021, 1.109458, 1.089356, 1.092147, 1.072745, 1.079362, 1.046206, 1.028233, 1.030930, 1.036983, 1.022429, 1.034229, 1.027596, 1.000937, 1.009525, 1.000591, 1.010982, 1.020008, 1.001194, 1.053950, 1.033547, 1.065893, 1.065980, 1.067038, 1.067688, 1.087256, 1.067462, 1.062706, 1.058481, 1.056351, 1.048031, 1.041856, 1.039252, 1.023064, 1.006270, 1.028233, 1.030930, 1.036983, 1.010061, 1.000471, 1.014502, 1.000937, 1.009525, 1.000591, 1.010982, 1.020008, 1.001194, 1.053950, 1.033547, 1.034171, 1.033233, 1.033035, 1.030568, 1.027063, 1.027074, 1.023781, 1.019656, 1.016014, 1.006120, 1.001311, 1.039252, 1.023064, 1.006270, 1.028233, 1.030930, 1.036983, 1.010061, 1.020159, 1.036169, 1.000937, 1.009525, 1.000591, 1.010982, 1.020008, 1.001194, 1.053950, 1.033547}; // 20% center/5x5, TPGh3x3 > 3 GeV, no genPhoPt cap but cut on saturated towers, min SF = 1.000000, using above ECAL calibs

   // float ecal[364] = {1.119974, 1.137018, 1.130883, 1.129678, 1.130041, 1.127207, 1.124656, 1.133294, 1.135318, 1.129183, 1.132421, 1.127110, 1.131243, 1.137500, 1.125751, 1.128942, 1.150045, 1.430908, 1.204760, 1.346070, 1.336213, 1.370062, 1.393691, 1.506774, 1.532985, 1.523253, 1.440226, 1.471771, 1.083458, 1.088212, 1.089936, 1.093921, 1.090387, 1.088164, 1.090377, 1.093799, 1.088938, 1.084879, 1.091404, 1.089761, 1.090559, 1.101873, 1.091828, 1.089970, 1.104742, 1.350578, 1.179811, 1.263306, 1.257441, 1.328798, 1.384993, 1.407375, 1.453402, 1.451094, 1.360005, 1.405290, 1.064812, 1.065712, 1.063012, 1.057444, 1.062879, 1.066116, 1.070599, 1.066663, 1.069633, 1.067560, 1.065884, 1.072179, 1.068451, 1.070914, 1.069204, 1.068418, 1.082723, 1.285564, 1.156553, 1.206729, 1.224918, 1.314733, 1.326699, 1.394201, 1.394864, 1.407732, 1.293633, 1.377775, 1.046928, 1.048195, 1.047900, 1.046159, 1.047827, 1.048260, 1.050228, 1.050648, 1.051581, 1.053247, 1.052816, 1.058339, 1.055687, 1.058953, 1.060128, 1.058107, 1.062246, 1.237738, 1.146385, 1.199365, 1.210367, 1.289966, 1.302556, 1.336799, 1.383672, 1.364472, 1.349935, 1.365479, 1.040894, 1.037608, 1.036712, 1.039901, 1.040222, 1.042710, 1.038373, 1.045120, 1.045232, 1.043503, 1.045144, 1.047226, 1.048568, 1.048010, 1.041316, 1.046387, 1.058259, 1.215451, 1.132300, 1.187170, 1.205522, 1.276262, 1.272435, 1.295975, 1.350847, 1.335878, 1.285139, 1.350992, 1.031939, 1.032265, 1.030075, 1.030722, 1.032947, 1.033734, 1.029981, 1.035661, 1.036366, 1.034582, 1.038130, 1.038495, 1.041036, 1.040277, 1.042074, 1.037345, 1.042986, 1.204778, 1.121578, 1.167640, 1.181280, 1.241490, 1.249574, 1.302296, 1.327019, 1.312183, 1.272538, 1.348591, 1.024938, 1.025509, 1.023756, 1.024768, 1.028016, 1.024053, 1.025151, 1.029714, 1.031280, 1.028153, 1.029108, 1.034672, 1.035088, 1.035485, 1.035425, 1.030921, 1.035286, 1.183772, 1.121352, 1.173454, 1.189430, 1.229655, 1.232626, 1.278129, 1.311512, 1.308012, 1.250878, 1.336074, 1.019513, 1.019618, 1.019204, 1.018834, 1.022974, 1.022908, 1.020755, 1.024202, 1.026904, 1.023369, 1.023972, 1.027892, 1.033798, 1.027385, 1.029245, 1.028285, 1.034477, 1.165892, 1.119740, 1.153680, 1.149763, 1.211771, 1.219994, 1.253516, 1.296463, 1.303058, 1.257639, 1.327970, 1.015691, 1.016185, 1.014119, 1.015780, 1.019400, 1.019295, 1.015197, 1.022786, 1.021406, 1.021086, 1.022585, 1.024652, 1.029811, 1.026212, 1.025407, 1.027974, 1.029525, 1.175521, 1.117686, 1.151020, 1.158437, 1.208777, 1.245628, 1.244515, 1.291418, 1.285469, 1.243252, 1.345496, 1.010777, 1.014901, 1.012442, 1.012455, 1.014412, 1.015092, 1.013139, 1.018499, 1.022926, 1.018472, 1.021256, 1.021942, 1.027232, 1.024771, 1.024256, 1.022187, 1.028147, 1.161713, 1.100158, 1.137876, 1.142112, 1.206308, 1.205765, 1.232275, 1.286246, 1.284886, 1.185941, 1.240007, 1.010994, 1.010082, 1.010540, 1.009084, 1.012683, 1.011982, 1.011589, 1.013616, 1.016348, 1.014766, 1.014374, 1.020283, 1.023327, 1.020288, 1.024421, 1.019464, 1.023091, 1.144736, 1.105701, 1.135751, 1.132751, 1.182500, 1.188998, 1.231027, 1.272445, 1.266766, 1.093305, 1.138539, 1.006412, 1.007943, 1.007441, 1.005918, 1.008423, 1.006728, 1.008028, 1.011924, 1.013576, 1.009289, 1.013604, 1.017471, 1.021669, 1.017841, 1.021837, 1.019624, 1.020834, 1.135556, 1.099984, 1.130754, 1.127277, 1.169267, 1.186532, 1.228943, 1.257746, 1.249596, 1.093305, 1.138539, 1.004021, 1.003420, 1.004326, 1.002428, 1.005777, 1.004605, 1.004239, 1.009848, 1.012610, 1.008506, 1.018630, 1.013259, 1.021146, 1.012670, 1.021540, 1.019173, 1.023531, 1.151531, 1.100064, 1.130605, 1.125264, 1.156489, 1.154959, 1.189941, 1.214844, 1.205538, 1.093305, 1.138539};  // fit peak, 90% center/3x3, TPGe3x3 > 3 GeV, genPhoPt < 125 GeV, SF = previous ETbin if < 1.0

    float ecal[364] = {1.133697, 1.119895, 1.127760, 1.120438, 1.111321, 1.131770, 1.126366, 1.130121, 1.126248, 1.125295, 1.127509, 1.124112, 1.131514, 1.148924, 1.146992, 1.138944, 1.154706, 1.351246, 1.209015, 1.343579, 1.368864, 1.397803, 1.390908, 1.394737, 1.439349, 1.450554, 1.288842, 1.236903, 1.078986, 1.080180, 1.080860, 1.079164, 1.079363, 1.085803, 1.081386, 1.084655, 1.081019, 1.082388, 1.088255, 1.087620, 1.095829, 1.115744, 1.102700, 1.097075, 1.117831, 1.316309, 1.174570, 1.281812, 1.301583, 1.327936, 1.317972, 1.329966, 1.379509, 1.451907, 1.202233, 1.193462, 1.067255, 1.064075, 1.060464, 1.056978, 1.062377, 1.061599, 1.063850, 1.065371, 1.066544, 1.064967, 1.076133, 1.066445, 1.079169, 1.083226, 1.085574, 1.078102, 1.089445, 1.235013, 1.150481, 1.236963, 1.263722, 1.284811, 1.277534, 1.312254, 1.353577, 1.429436, 1.171081, 1.172389, 1.045821, 1.049098, 1.050133, 1.046918, 1.053127, 1.053656, 1.052224, 1.054733, 1.047217, 1.056562, 1.054675, 1.057090, 1.064064, 1.076368, 1.067108, 1.067868, 1.080114, 1.216609, 1.141740, 1.216064, 1.240056, 1.272236, 1.266259, 1.285827, 1.333892, 1.396892, 1.153392, 1.159349, 1.043509, 1.040801, 1.039127, 1.038962, 1.040874, 1.043949, 1.041735, 1.045202, 1.044021, 1.043237, 1.044957, 1.046660, 1.058565, 1.061833, 1.056960, 1.058766, 1.065459, 1.207345, 1.135126, 1.203372, 1.223568, 1.257782, 1.244557, 1.269892, 1.313600, 1.381417, 1.140392, 1.144151, 1.032269, 1.029050, 1.030727, 1.030727, 1.032815, 1.032184, 1.037632, 1.036599, 1.034422, 1.037938, 1.042326, 1.039035, 1.047522, 1.053118, 1.051634, 1.050375, 1.056386, 1.177276, 1.122984, 1.184841, 1.206548, 1.240543, 1.240177, 1.256047, 1.303232, 1.335247, 1.126565, 1.135591, 1.030340, 1.023872, 1.024977, 1.026665, 1.028715, 1.029948, 1.032865, 1.031472, 1.030127, 1.031639, 1.031714, 1.034336, 1.039320, 1.047492, 1.047051, 1.045407, 1.052633, 1.155296, 1.126580, 1.176436, 1.212955, 1.229291, 1.226654, 1.258844, 1.290744, 1.354554, 1.118667, 1.129083, 1.026177, 1.021493, 1.022767, 1.023279, 1.024706, 1.025576, 1.027332, 1.027000, 1.026312, 1.026944, 1.030317, 1.032960, 1.038325, 1.045684, 1.043835, 1.046049, 1.046835, 1.161249, 1.120149, 1.172018, 1.202624, 1.223290, 1.219953, 1.240973, 1.281014, 1.338996, 1.111352, 1.124672, 1.021949, 1.016972, 1.018520, 1.020075, 1.023947, 1.024434, 1.024970, 1.023038, 1.023018, 1.023847, 1.025500, 1.028170, 1.034746, 1.038430, 1.040342, 1.042286, 1.042799, 1.150780, 1.116239, 1.176811, 1.199827, 1.221165, 1.223723, 1.233687, 1.273851, 1.334961, 1.105516, 1.123147, 1.020437, 1.013971, 1.017537, 1.016826, 1.020896, 1.021701, 1.021546, 1.022459, 1.021985, 1.021496, 1.024698, 1.024682, 1.033849, 1.037750, 1.041666, 1.037548, 1.042530, 1.124719, 1.110664, 1.166700, 1.195160, 1.210646, 1.205186, 1.234344, 1.264987, 1.323697, 1.099575, 1.122952, 1.017982, 1.012279, 1.019388, 1.019961, 1.016965, 1.018341, 1.017801, 1.019825, 1.018833, 1.019401, 1.022601, 1.023796, 1.030081, 1.037605, 1.034517, 1.035854, 1.036862, 1.121790, 1.122138, 1.163052, 1.185218, 1.204535, 1.197473, 1.223921, 1.259298, 1.237624, 1.095748, 1.115451, 1.013335, 1.007707, 1.015009, 1.015322, 1.012268, 1.011976, 1.018199, 1.015594, 1.013581, 1.013906, 1.019176, 1.020486, 1.028147, 1.032391, 1.044336, 1.033833, 1.035390, 1.125158, 1.114276, 1.156454, 1.178585, 1.192407, 1.190635, 1.223090, 1.255910, 1.297804, 1.050954, 1.047782, 1.011027, 1.007707, 1.004533, 1.005139, 1.008786, 1.009758, 1.014314, 1.015866, 1.011791, 1.011187, 1.020216, 1.016498, 1.025190, 1.029789, 1.031748, 1.032661, 1.032969, 1.152500, 1.108120, 1.150314, 1.172864, 1.185308, 1.174683, 1.212146, 1.244137, 1.253710, 1.050954, 1.047782};  // 9_0_2, fit peak, 90% center/3x3, TPGe3x3 > 3 GeV, genPhoPt < 125 GeV, SF = previous ETbin if < 1.0
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
	}
	for (unsigned int i = 0; i < hCorrTowerETCode.size(); i++)
	{
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
                if (abs(tp_ieta_)>28) continue; //ignore HF for now in HCAL vecotr 
                // TPG iEta starts at 0 and goes to 55 for ECAL; FIXME in helpers? Will be different for hcal 
                // TPG iPhi starts at 1 and goes to 72.  Let's index starting at zero.
                int ieta = TPGEtaRange(tp_ieta_);//avoid negative eta
                int iphi =  tp_iphi_-1; //zero index
		tp_eta_ = convertTPGEta(ieta); //FIXME
		tp_phi_ = convertTPGPhi(iphi); //CHECKME/FIXME should require zero index
		tp_depth_ = id.depth();
		tp_version_ = id.version();
		tp_soi_ = digi.SOI_compressedEt();
                hTowerETCode[iphi][ieta] = tp_et_*2; //add "uncompressed et" e.g. divide this by two later for 0.5 GeV precision 
                // hCorrTowerETCode[iphi][ieta] = tp_et_*2; //add "uncompressed et" e.g. divide this by two later for 0.5 GeV precision 
                
                //Make a first pass at filling hCorrTowerETCode, in case nothing is found in ECAL
            		int ETbin = 0;
						    if (tp_et_ < 15) ETbin = floor(tp_et_/3) - 1;
							  else if (tp_et_ >= 15 && tp_et_ < 45) ETbin = floor(tp_et_/5) + 1;
							  else if (tp_et_ >= 45 && tp_et_ < 55) ETbin = 10;
							  else if (tp_et_ >= 55 && tp_et_ < 70) ETbin = 11;
							  else if (tp_et_ >= 70) ETbin = 12;
							  if (ETbin<0) ETbin=0;
							  else if (ETbin>12) ETbin=12;
								// ieta is in [0,55], but need to convert to [0,27] to reference hcal[]
								int adj_ieta = ieta-28;
								if (adj_ieta < 0)
									adj_ieta = (-adj_ieta) - 1;
								hCorrTowerETCode[iphi][ieta] = tp_et_*2*hcal[ETbin*28+adj_ieta]; //add "uncompressed et" e.g. divide this by two later for 0.5 GeV precision

                if ( ieta<0 ||iphi<0 ||ieta>55){
                        cout<<"Original iEta: "<< tp_ieta_ <<" is transformed to "<<ieta<<" for saving to vector; Real Eta: "<<tp_eta_<<endl;
                        cout<<"Original iPhi: "<< tp_iphi_ <<" is transformed to "<<iphi<<" for saving to vector; Real Phi: "<<tp_phi_<<endl;
                }


		Htps_->Fill();


	}//end for of hcal digis
	
	for (unsigned int i = 0; i < eTowerETCode.size(); i++)
	{
		eTowerETCode[i].clear();
	}
	for (unsigned int i = 0; i < eCorrTowerETCode.size(); i++)
	{
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
		etp_phi_ = convertTPGPhi(iphi);//should require zero index
		etp_eta_ = convertTPGEta(ieta);//should not allow negatives Range 0-55 (only EBEE)
		if ( ieta<0 ||iphi<0 ||ieta>55){
			cout<<"Original iEta: "<< etp_ieta_ <<" is transformed to "<<ieta<<" for saving to vector; Real Eta: "<<etp_eta_<<endl;
			cout<<"Original iPhi: "<< etp_iphi_ <<" is transformed to "<<iphi<<" for saving to vector; Real Phi: "<<etp_phi_<<endl;
		}
		eTowerETCode[iphi][ieta] = ecalet; //compressed et!!! easily save the et in a vector of ints (divide by 2 later) 
		
		// Older binning scheme
		// int temp = floor((ecalet*0.5)/5);
		// int ptbin = temp -1;
		// if (ptbin<0) ptbin=0; 
		// else if (ptbin>8) ptbin=8;
		
		// ecalet = 2.0 * actual tower ET
		int ETbin = 0;
    if (ecalet < 30) ETbin = floor(ecalet*0.5/3) - 1;
	  else if (ecalet >= 30 && ecalet < 90) ETbin = floor(ecalet*0.5/5) + 1;
	  else if (ecalet >= 90 && ecalet < 110) ETbin = 10;
	  else if (ecalet >= 110 && ecalet < 140) ETbin = 11;
	  else if (ecalet >= 140) ETbin = 12;
	  if (ETbin<0) ETbin=0;
	  else if (ETbin>12) ETbin=12;
		// ieta is in [0,55], but need to convert to [0,27] to reference ecal[]
		int adj_ieta = ieta-28;
		if (adj_ieta < 0)
			adj_ieta = (-adj_ieta) - 1;
		eCorrTowerETCode[iphi][ieta] = ecalet*ecal[ETbin*28+adj_ieta]; 
		
		double hcalet = hTowerETCode[iphi][ieta];
		double ecalet_corr = eCorrTowerETCode[iphi][ieta];
		int ETbin_withHCAL = 0;
    if (ecalet_corr+hcalet < 30) ETbin_withHCAL = floor((ecalet_corr+hcalet)*0.5/3) - 1;
	  else if (ecalet_corr+hcalet >= 30 && ecalet_corr+hcalet < 90) ETbin_withHCAL = floor((ecalet_corr+hcalet)*0.5/5) + 1;
	  else if (ecalet_corr+hcalet >= 90 && ecalet_corr+hcalet < 110) ETbin_withHCAL = 10;
	  else if (ecalet_corr+hcalet >= 110 && ecalet_corr+hcalet < 140) ETbin_withHCAL = 11;
	  else if (ecalet_corr+hcalet >= 140) ETbin_withHCAL = 12;
	  if (ETbin_withHCAL<0) ETbin_withHCAL=0;
	  else if (ETbin_withHCAL>12) ETbin_withHCAL=12;
		hCorrTowerETCode[iphi][ieta] = hcal[ETbin_withHCAL*28+adj_ieta]*(hcalet+ecalet_corr) - ecalet_corr;
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
		if (std::abs(pion.eta())>2.868) continue; //ignore HF pions for now go up to ieta 29 boundary, include 28. 
		//cout<<"GenParticle PdgId: "<< pion.pdgId() <<endl;
		gen_pt_=pion.pt();
		gen_eta_=pion.eta();
		gen_phi_=pion.phi();
		//cout<<"Pion Eta: "<<gen_eta_<<endl;
		gen_ieta_=convertTPGGenEta(pion.eta());
		//cout<<"iEta: "<<gen_ieta_<<endl; 
		gen_iphi_=convertGenPhi(pion.phi());
		//cout<<"GenParticle Pt: "<< gen_pt_ <<" Eta: "<<gen_eta_<<" Phi: "<<gen_phi_<<" iEta: "<<gen_ieta_<<" iPhi: "<<gen_iphi_ <<endl;
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

		for (int j = -2; j < 3; ++j) {//eta
			for (int k = -2; k < 3; ++k) { //phi
				int tpgsquarephi= gen_iphi_+k;
				int tpgsquareeta= gen_ieta_+j;	

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
				if (tpgsquareeta>55 || tpgsquareeta<0) {continue;}//No Eta values beyond FIX ME IN NEXT ITERATION
				if (k == 0 && j == 0)
				{
					TPGhCenter_ = hTowerETCode[tpgsquarephi][tpgsquareeta];
					cTPGhCenter_ = hCorrTowerETCode[tpgsquarephi][tpgsquareeta];
					TPGeCenter_ = eTowerETCode[tpgsquarephi][tpgsquareeta];
					cTPGeCenter_ = eCorrTowerETCode[tpgsquarephi][tpgsquareeta];
				}
				if (std::abs(k) < 2 && std::abs(j) < 2)
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
