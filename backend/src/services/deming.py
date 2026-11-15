import math
import numpy as np
def deming_fit(x,y,lambda_ratio):
    # lambda = variance(error in Y) / variance(error in X), not observed Var(Y)/Var(X).
    if not math.isfinite(lambda_ratio) or lambda_ratio<=0:raise ValueError("lambda必须为正的有限测量误差方差比")
    x=np.asarray(x,dtype=float);y=np.asarray(y,dtype=float)
    if len(x)!=len(y) or len(x)<3 or not np.isfinite(x).all() or not np.isfinite(y).all():raise ValueError("需要至少3对有限测量值")
    dx=x-x.mean();dy=y-y.mean()
    sxx=float(dx@dx);syy=float(dy@dy);sxy=float(dx@dy)
    if sxx<1e-12 or syy<1e-12:raise ValueError("参考或候选测量值为常量，回归不可识别")
    if abs(sxy)<1e-12*math.sqrt(sxx*syy):raise ValueError("协方差接近零，Deming方向与逆校准不可识别")
    delta=syy-lambda_ratio*sxx
    rad=math.hypot(delta,2*math.sqrt(lambda_ratio)*sxy)
    slope=(delta+rad)/(2*sxy) if delta>=0 else (2*lambda_ratio*sxy)/(rad-delta)
    intercept=float(y.mean()-slope*x.mean())
    if not math.isfinite(slope) or abs(slope)<1e-8:raise ValueError("回归斜率接近零，禁止逆校准")
    return intercept,float(slope)
def inverse_calibrate(value,intercept,slope,x_range,y_range):
    if not math.isfinite(value) or not y_range[0]<=value<=y_range[1]:raise ValueError("候选读数超出本次实际观测Y范围，禁止外推")
    estimate=(value-intercept)/slope
    if not x_range[0]<=estimate<=x_range[1]:raise ValueError("逆校准值超出本次实际观测X范围，禁止外推")
    return float(estimate)
