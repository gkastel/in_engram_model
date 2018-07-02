
function la_run {
	echo $LAPARAMS
	#qsub -v "LAPARAMS=$LAPARAMS" submit_lamodel.sh
	#echo $LAPARAMS
	./lamodel $LAPARAMS 
}

for nltype in 0 1 2 3; do
	for clustered in 0 1; do
		for run in {0..20}  ; do

			LAPARAMS=" -P 1 -T 180 -S 1980$run -o setNlTypes=${nltype} -o INClustered=${clustered} -s single_${nltype}_${clustered}_G_${run} -G"
			la_run

		done
	done
done


