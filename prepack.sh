#3)prepack

/opt/software/rosetta/2021.16.61629/main/source/bin/FlexPepDocking.static.linuxgccrelease -in:file:s 7BR3_PEP_start_min_0003.pdb -in:file:spanfile 7BR3_PEP.span -membrane:Membed_init -membrane::Mhbond_depth -score:weights membrane_highres  -scorefile ppk.sc -out:no_nstruct_label -out:prefix ppk. -flexPepDocking:flexpep_prepack -flexPepDocking:flexpep_score_only -ex1 -ex2aro -use_input_sc -unboundrot native.pdb -nstruct 10 > ppk.log

#here native is the unbound minimised receptor from 7BR3_PEP_start_min_0003.pdb
