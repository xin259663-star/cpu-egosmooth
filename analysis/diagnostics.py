"""Post-hoc descriptors from frozen arrays. No fitting, smoothing or selection."""
from pathlib import Path
import numpy as np, csv, json, hashlib, argparse
ROOT=Path(__file__).resolve().parents[2]
OUT=ROOT/'outputs/CEP_Revision_v1/analysis'
BASE=None
DT=.5
MIN_SEG=.05  # inherited numerical-validity rule, NOT a physical constraint
def geometry(h,p):
    q=np.concatenate([h[:,-1:],p],axis=1).astype(np.float64)
    a=q[:,1:-1]-q[:,:-2];b=q[:,2:]-q[:,1:-1];c=q[:,2:]-q[:,:-2]
    la=np.linalg.norm(a,axis=-1);lb=np.linalg.norm(b,axis=-1);lc=np.linalg.norm(c,axis=-1)
    valid=np.all((la>=MIN_SEG)&(lb>=MIN_SEG)&(lc>1e-12),axis=1)
    k=np.divide(2*np.abs(a[...,0]*b[...,1]-a[...,1]*b[...,0]),la*lb*lc,out=np.full_like(la,np.nan),where=(la*lb*lc)>1e-12)
    curv=np.max(k,axis=1);lat=np.max(((la+lb)/(2*DT))**2*k,axis=1)
    u=h[:,-1]-h[:,-2];v=p[:,0]-h[:,-1]
    vh=(np.linalg.norm(u,axis=1)>=MIN_SEG)&(np.linalg.norm(v,axis=1)>=MIN_SEG)
    heading=np.degrees(np.abs(np.arctan2(u[:,0]*v[:,1]-u[:,1]*v[:,0],np.sum(u*v,axis=1))))
    return {'max_abs_curvature':(curv,valid),'max_lateral_acceleration_proxy':(lat,valid),'boundary_heading_discontinuity':(heading,vh)}
def existing(h,p,gt,raw):
    err=np.linalg.norm(p-gt,axis=-1)
    z=np.concatenate([h[:,-3:],p],axis=1)
    shape=np.linalg.norm(np.diff(z,n=3,axis=1)/DT**3,axis=-1).mean(axis=1)
    speed=np.linalg.norm((p[:,0]-h[:,-1])/DT-(h[:,-1]-h[:,-2])/DT,axis=-1)
    accel=np.linalg.norm((p[:,1]-2*p[:,0]+h[:,-1])/DT**2-(h[:,-1]-2*h[:,-2]+h[:,-3])/DT**2,axis=-1)
    return {'ADE':err.mean(axis=1),'FDE':err[:,-1],'Shape':shape,'boundary_speed_mismatch':speed,'boundary_acceleration_mismatch':accel,'endpoint_shift':np.linalg.norm(p[:,-1]-raw[:,-1],axis=-1)}
def main():
    OUT.mkdir(parents=True,exist_ok=True)
    path=BASE/'preflight/heldout_payloads/log_primary/heldout.npz'
    hashes={str(path.relative_to(BASE)):hashlib.sha256(path.read_bytes()).hexdigest()}
    with np.load(path,allow_pickle=False) as x:h=x['history_xy'].astype(float);gt=x['future_xy'].astype(float);ids={k:x[k].copy() for k in ['log_token','scene_token','anchor_sample_token','window_index']}
    dirs=sorted((BASE/'predictions/log_primary').iterdir());dirs=[d for d in dirs if d.is_dir() and (d/'raw_predictions.npz').exists()]
    assert len(dirs)==50 and len(h)==2901
    data={m:{s:[] for s in ['Raw','Fixed SG','Selected']} for m in ['max_abs_curvature','max_lateral_acceleration_proxy','boundary_heading_discontinuity']}
    checks={s:{} for s in ['Raw','Fixed SG','Selected']};logids=[];rows=[]
    for d in dirs:
        preds={}
        for s,fn in [('Raw','raw'),('Fixed SG','fixed_sg'),('Selected','selected')]:
            f=d/(fn+'_predictions.npz');hashes[str(f.relative_to(BASE))]=hashlib.sha256(f.read_bytes()).hexdigest()
            with np.load(f,allow_pickle=False) as z:
                for k,other in [('log_token','log_token'),('scene_token','scene_token'),('sample_token','anchor_sample_token'),('window_index','window_index')]:assert np.array_equal(z[k],ids[other]),(d.name,k)
                preds[s]=z['prediction'].astype(float)
            assert preds[s].shape==(2901,6,2) and np.isfinite(preds[s]).all()
        diag={s:geometry(h,p) for s,p in preds.items()};logids.extend(ids['log_token'])
        for m in data:
            mask=np.logical_and.reduce([diag[s][m][1] for s in preds])
            for s in preds:
                vals=np.where(mask,diag[s][m][0],np.nan);data[m][s].append(vals)
                rows.append({'run_id':d.name,'metric':m,'strategy':s,'valid_windows':int(mask.sum()),'total_windows':2901,'mean':float(np.nanmean(vals)),'median':float(np.nanmedian(vals)),'p95':float(np.nanquantile(vals,.95))})
        for s,p in preds.items():
            for m,v in existing(h,p,gt,preds['Raw']).items():checks[s].setdefault(m,[]).append(v)
    allrows=[];paired=[];logs=np.array(logids)
    for m,ss in data.items():
        vals={s:np.concatenate(v) for s,v in ss.items()};n=int(np.isfinite(vals['Raw']).sum())
        for s,v in vals.items():allrows.append({'metric':m,'unit':{'max_abs_curvature':'m^-1','max_lateral_acceleration_proxy':'m s^-2','boundary_heading_discontinuity':'degree'}[m],'strategy':s,'valid_pairs':n,'total_pairs':145050,'mean':float(np.nanmean(v)),'median':float(np.nanmedian(v)),'p95':float(np.nanquantile(v,.95))})
        for a,b in [('Fixed SG','Raw'),('Selected','Fixed SG'),('Selected','Raw')]:
            delta=vals[a]-vals[b]
            effects=[float(np.nanmean(delta[logs==l])) for l in np.unique(logs)]
            paired.append({'metric':m,'comparison':a+' minus '+b,'mean_delta':float(np.nanmean(delta)),'positive_rate':float(np.nanmean(np.where(np.isfinite(delta),delta>0,np.nan))),'negative_log_count':sum(v<0 for v in effects),'log_count':len(effects)})
    def save(name,rs):
        with (OUT/name).open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=list(rs[0]));w.writeheader();w.writerows(rs)
    save('new_descriptor_summary.csv',allrows);save('new_descriptor_paired.csv',paired);save('new_descriptor_run_summary.csv',rows)
    means={s:{m:float(np.concatenate(v).mean()) for m,v in mm.items()} for s,mm in checks.items()}
    # Published precision, not replacement of original estimates.
    for s,target in {'Raw':[.8019,1.7214,1.878],'Fixed SG':[.8008,1.7201,1.047],'Selected':[.7994,1.7210,1.009]}.items():
        for m,v in zip(['ADE','FDE','Shape'],target):assert abs(means[s][m]-v)<(.000051 if m!='Shape' else .00051),(s,m,means[s][m],v)
    (OUT/'input_sha256.json').write_text(json.dumps(hashes,indent=2)+'\n',encoding='utf-8')
    report={'runs':50,'windows_per_run':2901,'run_windows':145050,'logs':len(np.unique(logs)),'all_identifier_checks':'PASS','published_means_rounding_check':'PASS','existing_metrics_recomputed':means,'dt_seconds':DT,'minimum_segment_numerical_validity_m':MIN_SEG,'constraint_violation_frequency':'NOT ESTIMATED: no vehicle-specific physical limits','new_summary':allrows,'paired_summary':paired}
    (OUT/'analysis_QA.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8');print(json.dumps(report,indent=2))
if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input-root',required=True,help='13_heldout_evaluation directory containing frozen payload and primary predictions')
    parser.add_argument('--output-dir',default=None,help='Directory for CSV summaries, input digests and QA JSON')
    args=parser.parse_args();BASE=Path(args.input_root).resolve()
    import os
    if os.name=='nt' and not str(BASE).startswith('\\\\?\\'):BASE=Path('\\\\?\\'+str(BASE))
    if args.output_dir:OUT=Path(args.output_dir).resolve()
    main()
