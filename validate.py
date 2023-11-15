import os
import sys
import glob


def get_expected_files(stage, iteration=1):
    if stage==1 and iteration==1:
        expected_files = [
            "pwg-{jobid:04d}-xg1-stat.dat",
            "pwgcounters-st1-{jobid:04d}.dat",
            "pwg-xg1-xgrid-btl-{jobid:04d}.dat",
            "pwg-xg1-xgrid-rm-{jobid:04d}.dat"
            ]
    elif stage==1 and iteration>1:
        expected_files = [
            f"pwg-{{jobid:04d}}-xg{iteration}-stat.dat",
            f"pwg-xg{iteration}-xgrid-btl-{{jobid:04d}}.dat",
            f"pwg-xg{iteration}-xgrid-rm-{{jobid:04d}}.dat",
            f"pwg-xg{iteration}-xgrid-btl-{{jobid:04d}}.top",
            f"pwg-xg{iteration}-xgrid-rm-{{jobid:04d}}.top"
            ]
    elif stage==2: 
        expected_files = [
            "pwg-st2-xgrid-btl-{jobid:04d}.top",
            "pwg-st2-xgrid-rm-{jobid:04d}.top",
            "pwggrid-btl-{jobid:04d}.dat",
            "pwggrid-rm-{jobid:04d}.dat",
            "pwgbtlupb-{jobid:04d}.dat",
            "pwgrmupb-{jobid:04d}.dat",
            "pwgcounters-st2-{jobid:04d}.dat",
            "pwg-{jobid:04d}-st2-stat.dat"
            ]
    elif stage==3:
        expected_files = [
            "mint_upb_btlupb_rat.top",
            "mint_upb_btlupb.top",
            "mint_upb_rmupb.top",
            #"pwgfullgrid-btl-{jobid:04d}.dat",
            #"pwgfullgrid-rm-{jobid:04d}.dat",
            "pwgubound-{jobid:04d}.dat",
            "pwgcounters-st3-{jobid:04d}.dat",
            "pwg-{jobid:04d}-st3-stat.dat",
            "pwghistnorms.top",
            "pwgborngrid-stat.dat"
        ]
    elif stage==4:
        expected_files = [
            "pwgevents-{jobid:04d}.lhe",
            "pwg-{jobid:04d}-st4-stat.dat",
            "pwgcounters-st4-{jobid:04d}.dat",
            "pwgboundviolations-{jobid:04d}.dat",
            ]
    elif stage==5:
        expected_files = []
        # TODO
    return expected_files
    
def check_stage_output(settings, nbatches, stage, iteration, workdir, any_exist=False):
    expected_files = get_expected_files(stage, iteration)
    
    missing_ids = []
    for n in range(nbatches):
        for f in expected_files:
            f_formatted = f.format(jobid=n)
            f_dir = os.path.join(settings['run_dir'], f_formatted)
            if os.path.exists(f_dir) and any_exist:
                # any_exist --> return true as soon as one file exists
                return True, []
            if not os.path.exists(f_dir) and not any_exist:
                #print(f_formatted)
                # all_exist --> return list of missing files
                missing_ids.append(n)
                break

    if any_exist:
        # any_exist --> return false if none exist
        return False, []    
    else:
        # all_exist --> return true if all exist
        if len(missing_ids) == 0:
            return True, []
        else:
            return False, missing_ids

