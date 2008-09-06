<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"><head><title>Daluang</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<link rel="stylesheet" type="text/css" href="/+res/style.css"/>
<link rel="stylesheet" type="text/css" href="/+res/index.css"/>
</head><body><div id="c">

% if languages:
<h1>Available Languages</h1>

<ul id="lang">
% for item in languages:
<li><a href="/${ item['code'] }/">${ item['lang'] }</a></li>
% endfor
</ul>

% else:
<h1>No data available</h1>

<p>Please install some data.</p>
% endif

</div></body></html>
