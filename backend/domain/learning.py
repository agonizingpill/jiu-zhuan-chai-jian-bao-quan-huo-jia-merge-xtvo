import numpy as np
from sklearn.cluster import Birch
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

THRESHOLD = 6.0  # 复测含湿率超标线 %

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

def features(rows):
    return [[r['initial'],r['length'],r['perforation']] for r in rows]

def risk(data):
    targets=data['targets']
    if not targets: return {'state':'ready','scores':{}}
    samples=data['samples']
    labels=[1 if row['retest']>THRESHOLD else 0 for row in samples]
    if len(set(labels))<2: return {'state':'unestimable'}
    scale=StandardScaler().fit(features(samples))
    model=LogisticRegression(max_iter=1000)
    model.fit(scale.transform(features(samples)),labels)
    probs=model.predict_proba(scale.transform(features(targets)))
    pos=list(model.classes_).index(1)
    scores={row['code']:round(float(prob[pos]),4) for row,prob in zip(targets,probs)}
    return {'state':'ready','scores':scores}
