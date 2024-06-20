import gzip,json,os
for i in range(24):
    if not os.path.exists("./replay/thhxhj_"+str(i+1).zfill(2)+".rpy"):
        continue
    with gzip.open("./replay/thhxhj_"+str(i+1).zfill(2)+".rpy", 'rb') as f:
         jsondict = json.loads(gzip.decompress(f.read()).decode(), strict=False)
    print(i,jsondict["metadata"])