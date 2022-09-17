#!/usr/bin/bash
for f in data/*.md; do
	rpath=${f#data/};
	if ! test -f "pdf/${rpath%.md}.pdf"; then
		echo "${rpath%.md}";
		sed -Ei 's/^(title: )/sub\1/;s/^course: /title: /;s/^year: /date: /' ${f};
		pandoc ${f} -o pdf/${rpath%.md}.pdf;
	fi;
done;
