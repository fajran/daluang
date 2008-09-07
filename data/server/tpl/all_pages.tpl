<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"><head><title>All Pages - ${ lang } - Daluang</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<link rel="stylesheet" type="text/css" href="/+res/style.css"/>
</head><body>
<h1>All Pages - ${ lang }</h1>

% if prev_index >= 0 or next_index >= 0:
<ul class="prevnext">
% if prev_index >= 0:
	<li><a href="/${ code }/special/all?start=${ prev_index }">&laquo; Prev</a></li>
% endif
% if next_index >= 0:
	<li><a href="/${ code }/special/all?start=${ next_index }">Next &raquo;</a></li>
% endif
</ul>
% endif

<ul>
% for title in titles[0:100]:
<li><a href="/${ code }/article/${ title }/">${ title }</a></li>
% endfor
</ul>

% if prev_index >= 0 or next_index >= 0:
<ul class="prevnext">
% if prev_index >= 0:
	<li><a href="/${ code }/special/all?start=${ prev_index }">&laquo; Prev</a></li>
% endif
% if next_index >= 0:
	<li><a href="/${ code }/special/all?start=${ next_index }">Next &raquo;</a></li>
% endif
</ul>
% endif

</body></html>
