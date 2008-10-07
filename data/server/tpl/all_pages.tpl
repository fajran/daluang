<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"><head><title>All Pages - ${ lang } - Daluang</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<link rel="stylesheet" type="text/css" href="/+res/style.css"/>
</head><body>
<h1>All Pages - ${ lang }</h1>

<div id="allpages" class="${ pages['type'] }">

% if pages['type'] == 'titles':
<ul>
<%
	size = len(pages['titles'])
	s3 = int(size / 3)
%>
	<table><tr>
	<td>
	% for title in pages['titles'][0:s3]:
	<li><a href="/${ code }/article/${ title }/">${ title }</a></li>
	% endfor
	</td>
	<td>
	% for title in pages['titles'][s3+1:s3*2]:
	<li><a href="/${ code }/article/${ title }/">${ title }</a></li>
	% endfor
	</td>
	<td>
	% for title in pages['titles'][s3*2+1:]:
	<li><a href="/${ code }/article/${ title }/">${ title }</a></li>
	% endfor
	</td>
	</tr></table>
</ul>
% endif

% if pages['type'] == 'groups':
<ul>
	% for group in pages['groups']:
	<li>
	<a href="/${ code }/special/all?start=${ group['start'][0] }&end=${ group['end'][0] }">${ group['start'][1] }</a>
	to
	<a href="/${ code }/special/all?start=${ group['start'][0] }&end=${ group['end'][0] }">${ group['end'][1] }</a>
	</li>
	% endfor
</ul>
% endif

</div>

</body></html>
