import subprocess
from glob import glob
from os.path import basename, join

import numpy as np
import obspy
import pandas as pd
from tqdm import tqdm

CEA_NETWORKS = ["AH", "BJ", "BU", "CQ", "FJ", "GD", "GS", "GX", "GZ", "HA", "HB", "HE", "HI", "HL", "HN",
                "JL", "JS", "JX", "LN", "NM", "NX", "QH", "SC", "SD", "SH", "SN", "SX", "TJ", "XJ", "XZ", "YN", "ZJ"]


def modify_time(time_str):
    if(type(time_str) != str):
        return obspy.UTCDateTime("2099-09-01")
    else:
        return obspy.UTCDateTime(time_str)


def load_cmpaz_info(cea_correction_file):
    correction_data = pd.read_csv(cea_correction_file, sep="|", comment="#", names=[
        "network", "station", "eventno", "mean", "std", "median", "mad", "starttime", "endtime"])
    correction_data["starttime"] = correction_data["starttime"].apply(
        modify_time)
    correction_data["endtime"] = correction_data["endtime"].apply(
        modify_time)
    return correction_data


def func_correct_cea(cmpaz, network, station, event_time, correction_data):
    # after 2013-09-01T11:52:00Z, all the stations have been corrected
    trunc_datetime = obspy.UTCDateTime("2013-09-01T11:52:00Z")
    if(event_time > trunc_datetime):
        return cmpaz
    else:
        info_for_this_station = correction_data.loc[(
            correction_data.network == network) & (correction_data.station == station) & (correction_data.starttime <= event_time) & (correction_data.endtime >= event_time)]
        if(len(info_for_this_station) == 0):
            return None
        elif(len(info_for_this_station) == 1):
            median_value = info_for_this_station["median"].values[0]
            if(np.isnan(median_value)):
                if_has_been_corrected = (
                    info_for_this_station["endtime"].values[0] == obspy.UTCDateTime("2099-09-01"))
                if(if_has_been_corrected):
                    return cmpaz
                else:
                    return None
            return cmpaz+median_value
        else:
            return None


def main(cea_correction_file, base_dir, output_dir):
    # load cmpaz file
    correction_data = load_cmpaz_info(cea_correction_file)
    # find all events
    all_events_path = glob(join(base_dir, "*"))
    # find all the sac files
    for each_event_path in tqdm(all_events_path):
        all_sac_files = glob(join(each_event_path, "*"))
        all_sac_files.remove(join(each_event_path, "extra"))
        all_sac_files.remove(join(each_event_path, "PZ"))

        # handle output directory structure
        gcmtid = basename(each_event_path)
        output_each_event_path = join(output_dir, gcmtid)
        command = f"mkdir {output_each_event_path}"
        subprocess.call(command, shell=True)
        command = f"cp -r {each_event_path}/extra {output_each_event_path}/extra"
        subprocess.call(command, shell=True)
        command = f"cp -r {each_event_path}/PZ {output_each_event_path}/PZ"
        subprocess.call(command, shell=True)

        # handle each sac file, and save to the output directory
        for each_sac_file in all_sac_files:
            data = obspy.read(each_sac_file)[0]
            if (data.stats.channel[-1] == "Z"):
                cmpinc = 0
                cmpaz = 0
            elif(data.stats.channel[-1] == "N"):
                cmpinc = 90
                cmpaz = 0
            elif(data.stats.channel[-1] == "E"):
                cmpinc = 90
                cmpaz = 90
            else:
                print(each_sac_file)
                continue

            network = data.stats.network
            station = data.stats.station
            if (network in CEA_NETWORKS):
                # we just make an approximation of the event time
                event_time = data.stats.starttime
                cmpaz_corrected = func_correct_cea(
                    cmpaz, network, station, event_time, correction_data)
                if (cmpaz_corrected == None):
                    # save to the extra folder
                    data.stats.sac.cmpinc = cmpinc
                    data.stats.sac.cmpaz = cmpaz
                    save_path = join(output_each_event_path,
                                     "extra", basename(each_sac_file))
                    data.write(save_path, format="SAC")
                else:
                    cmpaz = np.mod(cmpaz_corrected, 360)
                    data.stats.sac.cmpinc = cmpinc
                    data.stats.sac.cmpaz = cmpaz
                    save_path = join(output_each_event_path,
                                     basename(each_sac_file))
                    data.write(save_path, format="SAC")


if __name__ == "__main__":
    cea_correction_file = "./cmpaz_segment.txt"
    base_dir = "/scratch/05880/tg851791/sac_files_for_small_region/data_small"
    output_dir = "/scratch/05880/tg851791/sac_files_for_small_region/data_small_corrected"
    main(cea_correction_file, base_dir, output_dir)
