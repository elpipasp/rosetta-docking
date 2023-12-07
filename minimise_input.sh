#output
#10A_start_AP_AP.span -->use mv 10A_start_AP_AP.span 7BR3_PEP.span

#10A_start_AP_APA.span --> remove

#mv 10A_start_AP_AP.pdb 7BR3_PEP_start.pdb -->used for minimisation

#2) minimization

/opt/software/rosetta/2021.16.61629/main/source/bin/FlexPepDocking.static.linuxgccrelease \
-database /opt/software/rosetta/2021.16.61629/main/database/ \
-s 7BR3_PEP_start.pdb \
-in:file:spanfile 7BR3_PEP.span \
-membrane:Membed_init \
-membrane:Mhbond_depth \
-score:weights membrane_highres \
-ex1 \
-ex2aro \
-flexPepDocking:flexpep_score_only \
-scorefile min.score.sc \
-nstruct 10 \
-out:suffix _min

#output
#10 minimised structures 
#min.score.sc

#-->lowest score: 7BR3_PEP_start_min_0003.pdb
