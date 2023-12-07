#4) refingment

/opt/software/rosetta/2021.16.61629/main/source/bin/FlexPepDocking.static.linuxgccrelease @options listed below

-flexPepDocking:receptor_chain A
-flexPepDocking:peptide_chain P
-in:file:s ppk.min.7BR3_PEP.pdb
-in:file:spanfile 7BR3_PEP.span
-membrane:Membed_init
-membrane:Mhbond_depth
-score:weights membrane_highres
-scorefile REFINE_score.sc
-flexPepDocking:pep_refine
-flexPepDocking:flexpep_score_only
-nstruct 5
-ex1
-ex2aro
-use_input_sc
-unboundrot native.pdb
-out:prefix ref.dock.

#create 5 structures anf get the lowest score for next input
