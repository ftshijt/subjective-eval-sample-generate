import argparse
import random
import os


def pad_zero(num, place_holder=4):
    if len(str(num)) > place_holder:
        raise ValueError("number is exceeding the zero pad place holder.")
    return "0" * (place_holder - len(str(num))) + str(num)


def get_utt_id(wavscp, sample_per_sys):
    with open(wavscp, "r", encoding="utf-8") as f:
        info = f.read().strip().split("\n")
        if len(info) < sample_per_sys:
            raise ValueError("more samples to select than it has")

        utt_id_list = random.sample(info, sample_per_sys)
    return [utt.split(maxsplit=1)[0] for utt in utt_id_list]


def load_wavscp(wavscp, valid_utt_id, sys_code):
    with open(wavscp, "r", encoding="utf-8") as f:
        info = f.read().split("\n")
        wav_scp_info = {}
        for utt in info:
            if len(utt) == 0:
                continue
            utt_id, path_info = utt.split(maxsplit=1)
            if utt_id in valid_utt_id:
                wav_scp_info[path_info] = sys_code
    return wav_scp_info


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sys_scp", type=str, action="append")
    parser.add_argument("--target_dir", type=str)
    parser.add_argument("--sample_per_sys", type=int, default=30)
    parser.add_argument("--trap_utt", type=int, default=0)

    args = parser.parse_args()

    utt_id_all = get_utt_id(args.sys_scp[0], args.sample_per_sys + args.trap_utt)
    valid_utt_id = utt_id_all[:args.sample_per_sys]
    trap_utt_id = utt_id_all[args.sample_per_sys:]

    path_list = []
    trap_path_list = []
    back_info = {}
    for scp in args.sys_scp:
        sys_utt_info = load_wavscp(scp, valid_utt_id, sys_code=scp)
        path_list.extend(list(sys_utt_info.keys()))
        trap_utt_info = load_wavscp(scp, trap_utt_id, sys_code=scp)
        trap_path_list.extend(list(trap_utt_info.keys()))
        back_info.update(sys_utt_info)
        back_info.update(trap_utt_info)


    if not os.path.exists(args.target_dir):
        os.makedirs(args.target_dir)
    if not os.path.exists(os.path.join(args.target_dir, "test_wav")):
        os.makedirs(os.path.join(args.target_dir, "test_wav"))
    info_file = open(os.path.join(args.target_dir, "sys_info.txt"), "w", encoding="utf-8")
    score_file = open(os.path.join(args.target_dir, "score.csv"), "w", encoding="utf-8")

    final_list = path_list + trap_path_list

    random.shuffle(final_list)

    for i in range(len(final_list)):
        write_id = pad_zero(i)
        target_wav = os.path.join(args.target_dir, "test_wav", write_id + ".wav")
        if final_list[i] not in trap_path_list:
            os.system("sox {} {}".format(final_list[i], target_wav))
        else:
            rand = random.random()
            if rand < 0.25:
                os.system("sox {} {} synth whitenoise vol 0.9 remix -".format(final_list[i], target_wav))
            elif rand < 0.5:
                os.system("sox {} {} speed 5.0".format(final_list[i], target_wav))
            elif rand < 0.75:
                os.system("sox {} {} trim 0 `soxi -D {}`".format(final_list[i], target_wav, final_list[i]))
            else:
                os.system("sox {} {} vol 0.0001".format(final_list[i], target_wav))
        
        info_file.write("{} {} {}\n".format(write_id, back_info[final_list[i]], "trap" if final_list[i] in trap_path_list else "normal"))
        score_file.write("{},\n".format(write_id))

    info_file.close()
    score_file.close()
