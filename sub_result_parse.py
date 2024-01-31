import argparse
from mean_opinion_score import get_ci95, get_ci95_default, get_mos
import os
import numpy as np

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--score_folder", type=str)
    parser.add_argument("--sys_info", type=str)
    args = parser.parse_args()

    sys_record = open(args.sys_info, "r", encoding="utf-8")
    sys_record = sys_record.read().strip().split("\n")
    info_dict = {}
    sys_info = {}
    for sys in sys_record:
        print(sys)
        details = sys.split(" ")
        info_dict[int(details[0])] = details[1], details[2]
        if details[2] != "trap" and details[1] not in sys_info.keys():
            sys_info[details[1]] = []
    print(info_dict)

    for folder in os.listdir(args.score_folder):
        if folder == ".DS_Store":
            continue
        print(folder)
        trap_score = []
        target_file = open(os.path.join(args.score_folder, folder, "score.csv.csv"), "r", encoding="utf-8")
        for line in target_file.readlines():
            line = line.strip().split(",")
            system, details = info_dict[int(line[0])]
            # if details == "trap" or int(line[0]) in [133,36,42,143,136,85,23,91,16,6,14,54,21,70,56,131,126,107,32,19,141,18,24,44,34,149,142,69,38,118,27,78,89,113,30,129,13,50,92,26,76,132,120,59,125,116,137,4,108,81,58,119,95,77,109,97,72,94,104,39,112,111,57,102,83,122,11,37,139,]:
            if details == "trap":
                trap_score.append(int(line[1]))
            else:
                sys_info[system].append(line[1])

        print("{} trap score: {}".format(folder, sum(trap_score) / len(trap_score)))

    for sys in sys_info.keys():
        ratings = np.array([sys_info[sys]], dtype=np.float32)
        # print(ratings)
        mos = get_mos(ratings)
        ci = get_ci95_default(ratings)
        print("sys: {}, mos: {}, ci: {}".format(sys, mos, ci))
    