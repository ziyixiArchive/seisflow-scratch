from glob import glob
from os.path import join, basename
import pickle

small_region_dir = "/mnt/research/seismolab2/japan_slab/cmts/small_region"
old_dir = "/mnt/research/seismolab2/japan_slab/cmts/Japan_slab_from_used_EARA2014"

mapper_path = "/mnt/research/seismolab2/japan_slab/cmts/small_region_mapper.pkl"

all_small_paths = glob(join(small_region_dir, "*"))
all_small_gcmtid = set([basename(item) for item in all_small_paths])
all_old_paths = glob(join(old_dir, "*"))
all_old_gcmtid = set([basename(item) for item in all_old_paths])

mapper_new = all_small_gcmtid-all_old_gcmtid
mapper_old = all_small_gcmtid - mapper_new
out = {
    "new": mapper_new,
    "old": mapper_old
}

with open(mapper_path, 'wb') as handle:
    pickle.dump(out, handle, protocol=pickle.HIGHEST_PROTOCOL)

print(len(mapper_new), len(mapper_old))
