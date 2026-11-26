import numpy as np
from sklearn.cluster import Birch
from sklearn.preprocessing import StandardScaler

def matrix(rows):
    return [[r[k] for k in ('length','perforation')] for r in rows]

def calculate(data):
    samples=data['samples']; target=data['target']
    scale=StandardScaler().fit(matrix(samples))
    vector=scale.transform(matrix(samples))
    model=Birch(threshold=.25,n_clusters=None)
    for batch in np.array_split(vector,3): model.partial_fit(batch)
    groups=model.predict(vector)
    query=scale.transform(matrix([target]))
    kind=model.predict(query)[0]
    members=[i for i,label in enumerate(groups) if kind==label]
    if not members: raise ValueError('无相同孔形簇')
    match=min(members,key=lambda i:float(np.linalg.norm(query[0]-vector[i])))
    return {'pair':samples[match]['code'],'size':len(members),'clusters':len(set(groups)),'n_samples':len(samples)}
