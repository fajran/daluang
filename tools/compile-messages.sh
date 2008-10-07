#!/bin/bash

BASE=data/locale

for po in $BASE/*/daluang.po
do
	dir=`dirname $po`
	mkdir -p $dir/LC_MESSAGES/

	msgfmt $po -o $dir/LC_MESSAGES/daluang.mo
done

