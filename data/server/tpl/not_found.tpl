<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml"><head><title>${_("Content not found!")}</title>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<link rel="stylesheet" type="text/css" href="/+res/style.css"/>
</head><body>
<h1${_('>Not found')}</h1>

<p>${_("Daluang doesn't have an article called <strong>%s</strong>") % article }</strong>.</p>

<p>${_("Suggestions:")}</p>

<ul>
<li><a href="/${ lang }/search/${ article }/">${_("Search content for <strong>%s</strong>") % article}</a></p>
<li><a href="http://${ lang }.wikipedia.org/wiki/${ article }">${_("Open online version of <strong>%s</strong>") % article}</a></p>
<li><a href="http://${ lang }.wikipedia.org/wiki/Special:Search/${ article }">${_("Search wikipedia for <strong>%s</strong>") % article }</a></p>
</ul>

</body></html>
