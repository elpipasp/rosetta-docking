#5)docking
/opt/software/rosetta/2021.16.61629/main/source/bin/FlexPepDocking.static.linuxgccrelease @options_flexDock > flexDock.log
#generate 100 structures to use as template for further docking to explore conformations

-database /opt/software/rosetta/2021.16.61629/main/database/ 
-in:file:s ppk.min.7BR3_PEP.pdb
-in:file:spanfile 7BR3_PEP.span
-membrane:Membed_init
-membrane:Mhbond_depth
-score:weights membrane_highres
-scorefile score.sc
-flexPepDocking:lowres_preoptimize
-flexPepDocking:pep_refine
-ex1
-ex2aro
-nstruct 100
-use_input_sc
-out:prefix flex.

#The output 100 will be scored. Selected 10 best scoring poses and template inputs for futher docking --> 1000 dockings for each pose. Total 10,000 structures to be clusterd 
