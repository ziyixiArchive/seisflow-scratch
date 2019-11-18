"""
multiply 1000 for the evdp that's not correct.
"""
from os.path import join, basename
import obspy
from glob import glob
import tqdm

gcmtids_old = ['201006130332A',
               '200805071602A',
               '201006281207A',
               '201007042155A',
               '201002050648A',
               '200806292053A',
               '201005260853A',
               '200805191008A',
               '200910250617A',
               '200712251404A',
               '201001151108A',
               '200805071645A',
               '200909281922A',
               '200912020614A',
               '200812201029A',
               '201001141846A',
               '200910031536A',
               '201006111637A',
               '201002180113A',
               '200908122248A',
               '201007090041A',
               '201006111658A',
               '201002282207A',
               '200712070047A',
               '200902280035A',
               '201003300102A',
               '201103220718A',
               '200803142232A',
               '200809110020A',
               '201001170604A',
               '200802270654A',
               '200910262350A',
               '200809220731A',
               '201001250715A',
               '201101122132A',
               '201011300324A',
               '200910300703A',
               '201005031027A',
               '200810010938A',
               '200807211130A',
               '200806132343A',
               '200709061751A',
               '200909222259A',
               '201006272103A',
               '200912172041A',
               '200909031326A',
               '200807202130A',
               '200908050018A',
               '200805071616A',
               '201006050522A',
               '201002220521A',
               '200911031803A',
               '200708020237A',
               '201002280817A',
               '201003131246A',
               '200912280012A',
               '200803130841A',
               '200804161919A',
               '200710081710A',
               '200708010815A',
               '200806041703A',
               '201003140808A',
               '200807190239A',
               '201103111859A',
               '200906050330A',
               '201012222149A',
               '200903261919A',
               '200807231526A',
               '200806252337A',
               '200910100842A',
               '201002262031A',
               '200807080742A',
               '200708220726A',
               '201011071926A']

base_dir = "/scratch/05880/tg851791/sac_files_for_small_region/data_small_corrected"

for each_gcmtid in tqdm.tqdm(gcmtids_old):
    gcmtid_dir = join(base_dir, each_gcmtid)
    all_normal_sac_paths = glob(join(gcmtid_dir, "*"))
    all_normal_sac_paths.remove(join(gcmtid_dir, "extra"))
    all_normal_sac_paths.remove(join(gcmtid_dir, "PZ"))
    for each_sac_file in all_normal_sac_paths:
        data = obspy.read(each_sac_file)[0]
        data.stats.sac.evdp = data.stats.sac.evdp * 1000
        data.write(each_sac_file, format="SAC")

    all_abnormal_sac_paths = glob(join(gcmtid_dir, "extra", "*"))
    for each_sac_file in all_abnormal_sac_paths:
        data = obspy.read(each_sac_file)[0]
        data.stats.sac.evdp = data.stats.sac.evdp * 1000
        data.write(each_sac_file, format="SAC")
