"""Generate three fully synthetic demonstrations; fixed seed chosen for clear illustrative scenarios."""
import csv, random
from pathlib import Path
from datetime import datetime, timedelta

FIELDS=['build_id','build_time','specimen_id','strength_mpa','machine_id','powder_lot','oxygen_ppm','laser_power_w','scan_speed_mm_s','heat_treatment','notes']
def generate(folder=Path(__file__).parent):
    folder=Path(folder);folder.mkdir(parents=True,exist_ok=True)
    for name in ['stable_capable','mean_shift','stable_incapable']:
        rng=random.Random(42)
        rows=[]
        for b in range(1,41):
            shifted=name=='mean_shift' and b>=26
            low=name=='stable_incapable'
            mu=925 if low else (890 if shifted else 1000)
            sigma=22 if low else 15
            # Context covariates are artificial scenario annotations, not causal evidence.
            oxygen=round(rng.gauss(260 if shifted else 65,8),1)
            power=round(rng.gauss(280,2),1)
            speed=round(rng.gauss(1000,12),1)
            timestamp=(datetime(2026,9,1,8)+timedelta(hours=12*(b-1))).isoformat()
            for j in range(1,6):
                rows.append(dict(zip(FIELDS,[f'B{b:03d}',timestamp,f'B{b:03d}-C{j}',round(rng.gauss(mu,sigma),2),'LPBF-01','POWDER-A',oxygen,power,speed,'HT-A','Synthetic demonstration; no production data'])))
        p=folder/(name+'.csv')
        with p.open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(rows)
        print(f'{p.name}: {len(rows)} coupons, 40 builds, 5 coupons/build; seed=42')
if __name__=='__main__':generate()
