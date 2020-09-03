import ROOT as rt
import pandas as pd
import sys

result_dir = ""
result_file = "result"
#print sys.argv
#index = sys.argv[1]
#result_file += index

result = pd.read_csv(result_dir + result_file + ".csv", sep=',', header=0)

run_mod = "origin"
run_mod = "slope1"

reco_slope = 1.07421
aux_slope = 1.07002

study_gain = False
out_file = rt.TFile(result_file + "_" + run_mod + ".root","RECREATE")

Ebins = 200
Emin = 0.0
Emax = 1000.0

#==============global 1d hist =======================
weighted_time_h = rt.TH1F("weighted_time_h", "weighted simHit time", 100, 0.0, 500.0)
median_time_h = rt.TH1F("median_time_h", "median simHit time", 100, 0.0, 500.0)
fcByPE_h = rt.TH1F("fcByPE_h", "fcByPE for each TS", 100, 0.0, 1000.0)
PU_h = rt.TH1F("PU_h", "pileup", 100, 0.0, 100.0)
reco_h = rt.TH1F("reco_h", "reco energy", Ebins, Emin, Emax)
gen_h = rt.TH1F("gen_h", "truth energy", Ebins, Emin, Emax)

#==============reco vs gen 2d hist ==================
weighted_time_vs_gen_h = rt.TH2F("weighted_time_vs_gen_h", "weighted time vs gen", Ebins, Emin, Emax, 100, 0.0, 500.0)
reco_vs_gen_h = rt.TH2F("reco_vs_gen_h", "reco vs gen", Ebins, Emin, Emax, Ebins, Emin, Emax)
reco_err_vs_gen_h = rt.TH2F("reco_err_vs_gen_h", "|reco - gen|/gen vs gen", Ebins, Emin, Emax, 100, 0, 1)
aux_vs_gen_h = rt.TH2F("aux_vs_gen_h", "AUX vs gen", Ebins, Emin, Emax, Ebins, Emin, Emax)
aux_err_vs_gen_h = rt.TH2F("aux_err_vs_gen_h", "|aux - gen|/gen vs gen", Ebins, Emin, Emax, 100, 0, 1)
reco_vs_gen_depthG1_h = rt.TH2F("reco_vs_gen_depthG1_h", "reco vs gen, depth > 1", Ebins, Emin, Emax, Ebins, Emin, Emax)
reco_vs_gen_depthG1_HB_h = rt.TH2F("reco_vs_gen_depthG1_HB_h", "reco vs gen, depth > 1, HB", Ebins, Emin, Emax, Ebins, Emin, Emax)
reco_vs_gen_depthG1_HE_h = rt.TH2F("reco_vs_gen_depthG1_HE_h", "reco vs gen, depth > 1, HE", Ebins, Emin, Emax, Ebins, Emin, Emax)
reco_vs_gen_depthE1_HB_h = rt.TH2F("reco_vs_gen_depthE1_HB_h", "reco vs gen, depth = 1, HB", Ebins, Emin, Emax, Ebins, Emin, Emax)
reco_vs_gen_depthE1_HB_ietaS15_h = rt.TH2F("reco_vs_gen_depthE1_HB_ietaS15_h", "reco vs gen, depth = 1, |ieta| < 15, HB", Ebins, Emin, Emax, Ebins, Emin, Emax)
reco_vs_gen_depthE1_HE_h = rt.TH2F("reco_vs_gen_depthE1_HE_h", "reco vs gen, depth = 1, HE", Ebins, Emin, Emax, Ebins, Emin, Emax)

#==============ratio 1d hist ==========================
sum_amp_over_gen_h = rt.TH1F("sum_amp_over_gen_h", "sum 8 amplitudes / gen for gen > 10 GeV", 100, 0.0, 2500.0)
raw_energy_over_gen_h = rt.TH1F("raw_energy_over_gen_h", "raw reco energy / gen for gen > 10 GeV", 100, 0.0, 2500.0)
inv_gain_h = rt.TH1F("inv_gain_h", "1/gain for gen > 10 GeV", 100, 0.0, 2500.0)
ratio_h = rt.TH1F("ratio_h", "reco/gen for gen > 1 GeV", 100, 0.0, 2.0)
ratio_depthG1_h = rt.TH1F("ratio_depthG1_h", "reco/gen for gen > 1 GeV, depth > 1", 100, 0.0, 2.0)
ratio_depthG1_HB_h = rt.TH1F("ratio_depthG1_HB_h", "reco/gen for gen > 1 GeV, depth > 1, HB", 100, 0.0, 2.0)
ratio_depthG1_HE_h = rt.TH1F("ratio_depthG1_HE_h", "reco/gen for gen > 1 GeV, depth > 1, HE", 100, 0.0, 2.0)
ratio_depthE1_HB_h = rt.TH1F("ratio_depthE1_HB_h", "reco/gen for gen > 1 GeV, depth = 1, HB", 100, 0.0, 2.0)
ratio_depthE1_HB_ietaS15_h = rt.TH1F("ratio_depthE1_HB_ietaS15_h", "reco/gen for gen > 1 GeV, depth = 1, |ieta| < 15, HB", 100, 0.0, 2.0)
ratio_depthE1_HE_h = rt.TH1F("ratio_depthE1_HE_h", "reco/gen for gen > 1 GeV, depth = 1, HE", 100, 0.0, 2.0)

#============loop ieta hist for HB ====================
weighted_time_HB_ieta_list = []
reco_vs_gen_depthE1_HB_list = []
reco_vs_gen_depthG1_HB_list = []
for i in range(1,17):
    E1_hist = rt.TH2F("reco_vs_gen_depthE1_HB_iEta_" + str(i) + "_h", "reco vs gen, depth = 1, HB |ieta| " + str(i), Ebins, Emin, Emax, Ebins, Emin, Emax)
    reco_vs_gen_depthE1_HB_list.append(E1_hist)
    G1_hist = rt.TH2F("reco_vs_gen_depthG1_HB_iEta_" + str(i) + "_h", "reco vs gen, depth > 1, HB |ieta| " + str(i), Ebins, Emin, Emax, Ebins, Emin, Emax)
    reco_vs_gen_depthG1_HB_list.append(G1_hist)

    hist_list = []
    for j in range(1,6):
        time_hist = rt.TH1F("weighted_time_HB_iEta_" + str(i) + "_depth_" + str(j) + "_h", "weighted simHit time, HB |ieta| " + str(i) + ", depth " + str(j), 100, 0.0, 500.0)
        hist_list.append(time_hist)
    weighted_time_HB_ieta_list.append(hist_list)

#============loop ieta hist for HE ====================
weighted_time_HE_ieta_list = []
reco_vs_gen_depthE1_HE_list = []
reco_vs_gen_depthG1_HE_list = []
for i in range(16,30):
    E1_hist = rt.TH2F("reco_vs_gen_depthE1_HE_iEta_" + str(i) + "_h", "reco vs gen, depth = 1, HE |ieta| " + str(i), Ebins, Emin, Emax, Ebins, Emin, Emax)
    reco_vs_gen_depthE1_HE_list.append(E1_hist)
    G1_hist = rt.TH2F("reco_vs_gen_depthG1_HE_iEta_" + str(i) + "_h", "reco vs gen, depth > 1, HE |ieta| " + str(i), Ebins, Emin, Emax, Ebins, Emin, Emax)
    reco_vs_gen_depthG1_HE_list.append(G1_hist)

    hist_list = []
    for j in range(1,9):
        time_hist = rt.TH1F("weighted_time_HE_iEta_" + str(i) + "_depth_" + str(j) + "_h", "weighted simHit time, HE |ieta| " + str(i) + ", depth " + str(j), 100, 0.0, 500.0)
        hist_list.append(time_hist)
    weighted_time_HE_ieta_list.append(hist_list)

Nrows = result.shape[0]
#Nrows = 100000
print "total rows: ", Nrows
for i in range(Nrows):
    if i%100000 == 0: print "process %d rows" %i

    reco_corr = 1
    aux_corr = 1
    if run_mod == "slope1":
        reco_corr = reco_slope
        aux_corr = aux_slope

    gen_energy = result["raw truth energy"][i]
    reco_energy = result["reco energy"][i] / reco_corr
    aux_energy = result["AUX energy"][i] / aux_corr
    ieta = abs(result["ieta"] [i])
    depth = result["depth"] [i]
    sub_det = result["sub detector"] [i]
    PU = result["PU"] [i]
    gain = result["gain"] [i]
    weighted_time = result["weighted time"] [i]
    median_time = result["median time"] [i]
    raw_energy = reco_energy / gain

    sum_amplitude = 0
    if study_gain:
        for j in range(1,9):
            fcByPE_str = "TS" + str(j) + " fcByPE"
            fcByPE_h.Fill(result[fcByPE_str] [i])

            RC_str = "TS" + str(j) + " raw charge"
            ped_str = "TS" + str(j) + " ped noise"
            sum_amplitude += max((result[RC_str] [i] - result[ped_str] [i]), 0)

    weighted_time_h.Fill(weighted_time)
    median_time_h.Fill(median_time)
    PU_h.Fill(PU)
    reco_h.Fill(reco_energy)
    gen_h.Fill(gen_energy)
    weighted_time_vs_gen_h.Fill(gen_energy, weighted_time)
    reco_vs_gen_h.Fill(gen_energy, reco_energy)
    aux_vs_gen_h.Fill(gen_energy, aux_energy)

    if sub_det == 1:
        weighted_time_HB_ieta_list[ieta - 1][depth - 1].Fill(weighted_time)
        if depth == 1:
            reco_vs_gen_depthE1_HB_h.Fill(gen_energy, reco_energy)
            if ieta < 15: reco_vs_gen_depthE1_HB_ietaS15_h.Fill(gen_energy, reco_energy)
            reco_vs_gen_depthE1_HB_list[ieta - 1].Fill(gen_energy, reco_energy)
        else:
            reco_vs_gen_depthG1_h.Fill(gen_energy, reco_energy)
            reco_vs_gen_depthG1_HB_h.Fill(gen_energy, reco_energy)
            reco_vs_gen_depthG1_HB_list[ieta - 1].Fill(gen_energy, reco_energy)
    elif sub_det == 2:
        weighted_time_HE_ieta_list[ieta - 16][depth - 1].Fill(weighted_time)
        if depth == 1:
            reco_vs_gen_depthE1_HE_h.Fill(gen_energy, reco_energy)
            reco_vs_gen_depthE1_HE_list[ieta - 16].Fill(gen_energy, reco_energy)
        else:
            reco_vs_gen_depthG1_h.Fill(gen_energy, reco_energy)
            reco_vs_gen_depthG1_HE_h.Fill(gen_energy, reco_energy)
            reco_vs_gen_depthG1_HE_list[ieta - 16].Fill(gen_energy, reco_energy)
    else: print "strange sub_det: ", sub_det

    if gen_energy > 1:
        reco_err_vs_gen_h.Fill(gen_energy, abs(reco_energy-gen_energy)/gen_energy)
        aux_err_vs_gen_h.Fill(gen_energy, abs(aux_energy-gen_energy)/gen_energy)
        ratio = reco_energy / gen_energy
        ratio_h.Fill(ratio)
        if depth == 1:
            if sub_det == 1:
                ratio_depthE1_HB_h.Fill(ratio)
                if ieta < 15: ratio_depthE1_HB_ietaS15_h.Fill(ratio)
            elif sub_det == 2: ratio_depthE1_HE_h.Fill(ratio)
        else:
            ratio_depthG1_h.Fill(ratio)
            if sub_det == 1: ratio_depthG1_HB_h.Fill(ratio)
            elif sub_det == 2: ratio_depthG1_HE_h.Fill(ratio)
               
        if gen_energy > 10:
            sum_amp_over_gen_h.Fill(sum_amplitude / gen_energy)
            raw_energy_over_gen_h.Fill(raw_energy / gen_energy)
            inv_gain_h.Fill(1.0 / gain)

out_file.cd()
out_file.Write()
out_file.Close()
