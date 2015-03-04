#!/bin/bash

: ${FOX_EXEC:='../bin/fox-assembly-1.0-SNAPSHOT.jar'}
LOCK=./fox.lock

echo "[`date`] Task submitted for execution"
lockfile -5 -r-1 -l 6000 $LOCK
echo "[`date`] Start foxPSL"
echo "============================================================"
java -Xmx5000m -cp $FOX_EXEC com.signalcollect.psl.CommandLinePslInferencer --filename $@
rm -f $LOCK
echo "============================================================"
echo "[`date`] FoxPSL finished"
