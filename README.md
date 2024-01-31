# subjective-eval-sample-generate
For subjective evaluation sample preparation


## Step1
Use Muskits-ESPnet to generate samples for evaluation (usually locate in `exp/svs_train_<model>/decode_<decode_tag>/<test_set>/wav`)

## Step2
Use `generate_scp.py` to generate a scp for the wave files
```
python generate_scp.py <wave_flle_folders> <target_scp_path>
```

## Step3
Use process_sub_test.py to generate the eval data
```
python process_sub_test.py \
    --target_dir <target_dir> \
    --sys_scp <the_first_system> \
    --sys_scp <the_second_system> ... \
    --sample_per_sys <number of samples selected for each system> \
    --trap_utt <number of trap utterances>
```

Remember to remove the generated sys_info.txt for the raters.

## Step4
Conduct subjective evaluation and formulate as:
```
- eval_folder
    - rater1
        - score.csv
    - rater2
        -score.csv
    ...
```

## Step5
Use `sub_test_parse.py` to generate the final results
```
python sub_test_parse.py --score_folder <eval_folder> --sys_info <target_dir>/sys_info.txt
```

We first generate the average score of the trap utterances (if over 2.5, could be issues in scoring)

Finally, we output the MOS score for each system and CI
