#!/bin/bash

BASE=data/locale
POT=$BASE/daluang.pot

pybabel extract -F tools/babel.cfg . > $POT
msguniq $POT > $POT.uniq
mv $POT.uniq $POT

for po in $BASE/*/daluang.po
do
	msgmerge -q $po $POT > $po.new
	mv $po.new $po
done

