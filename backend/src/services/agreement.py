import numpy as np
from src.services.deming import deming_fit
def agreement_analysis(x,y,lambda_ratio=1,bootstrap_count=500,seed=73):
    x=np.asarray(x,dtype=float);y=np.asarray(y,dtype=float)
    if len(x)!=len(y) or len(x)<20:raise ValueError("一致性与bootstrap分析至少需要20对独立样本")
    intercept,slope=deming_fit(x,y,lambda_ratio)
    diff=y-x;means=(x+y)/2
    bias=float(diff.mean());sd=float(diff.std(ddof=1));lower=bias-1.96*sd;upper=bias+1.96*sd
    rng=np.random.default_rng(seed);boot=[];failed=0
    for _ in range(bootstrap_count):
        ix=rng.integers(0,len(x),len(x));d=diff[ix];b=float(d.mean());s=float(d.std(ddof=1))
        try:
            a,m=deming_fit(x[ix],y[ix],lambda_ratio)
            boot.append([a,m,b,b-1.96*s,b+1.96*s])
        except ValueError:failed+=1
    if len(boot)<.9*bootstrap_count:raise ValueError("bootstrap中不可识别样本过多，请检查重复或退化观测")
    cis=np.quantile(np.asarray(boot),[.025,.975],axis=0).T.tolist()
    low=diff[means<=np.median(means)];high=diff[means>np.median(means)]
    sd_low=float(np.std(low,ddof=1)) if len(low)>1 else 0
    sd_high=float(np.std(high,ddof=1)) if len(high)>1 else 0
    spread_ratio=max(sd_low,sd_high)/max(min(sd_low,sd_high),1e-12) if max(sd_low,sd_high)>1e-12 else 1
    warning=spread_ratio>1.8
    return {"intercept":intercept,"slope":slope,"intercept_ci":cis[0],"slope_ci":cis[1],"bias":bias,"sd_difference":sd,"loa_lower":lower,"loa_upper":upper,"bias_ci":cis[2],"lower_ci":cis[3],"upper_ci":cis[4],"correlation":float(np.corrcoef(x,y)[0,1]),"spread_ratio":spread_ratio,"heteroscedastic_warning":warning,"bootstrap_success":len(boot),"bootstrap_failed":failed,"bootstrap_seed":seed,"n":len(x)}
