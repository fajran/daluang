<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"><head><title>Daluang</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<link rel="stylesheet" type="text/css" href="/+res/style.css"/>
</head><body>
<h1>Search result</h1>

% if result:

<p>Search result for <strong>${ keywords }</strong>:</p>

<ul>
% for item in result:
<li><a href="/${ lang }/article/${ item[1] }/">${ item[1] }</a></li>
% endfor
</ul>

% else:

<p>Daluang could not found anything about <strong>${ keywords }</strong>.</p>

% endif

</body></html>
