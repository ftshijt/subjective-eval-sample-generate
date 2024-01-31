import os
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dir")
    parser.add_argument("scp")
    args = parser.parse_args()

    scp_file = open(args.scp, "w", encoding="utf-8")
    for file in os.listdir(args.dir):
        scp_file.write("{} {}\n".format(file.split(".")[0], os.path.join(args.dir, file)))
