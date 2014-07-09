#!/usr/bin/perl

chdir "/var/www/streetview" or die "chdir";

@files = <*.jpg>;

$file = $files[rand($#files)];

while (<>) {
	$query .= $_;
}

print "Content-type: text/html\n\n";

#@vars = split(/&/, $ENV{'QUERY_STRING'});
@vars = split(/&/, $query);

for $v (@vars) {
	($key, $val) = split(/=/, $v, 2);
	$val =~ s/%20/ /g;
	$val =~ s/%2C/,/g;

	$val =~ s/[^A-Za-z0-9._,: -]//g;

	$var{$key} = $val;
}

if ($var{'session'} eq "") {
	$var{'session'} = time + rand();
} else {
	open(OUT, ">>/home/enf/survey-log");
	$time = time;
	print OUT "$var{'intersection'} $var{'action'} $var{'session'} $ENV{'REMOTE_ADDR'} $time\n";
	close(OUT);
}

print <<EOF

<html>
<head><title>Walking preference survey</title></head>
<body>
<table width="100%">
<tr>
<td width="650">
<img width="640" height="640" src="http://trafficways.org/streetview/$file">
</td>
<td align="center">
Would you enjoy walking here?
<p>
<form action="http://trafficways.org/cgi-bin/survey.cgi" method="post">
        <input type="hidden" name="session" value="$var{'session'}" />
        <input type="hidden" name="intersection" value="$file" />
        <input type="submit" name="action" value="Yes" />
        <input type="submit" name="action" value="Maybe" />
        <input type="submit" name="action" value="No" />
        <input type="submit" name="action" value="Skip" />
</form>
</td>
</tr>
</table>
<p>
You can stop whenever you want or keep answering for as long as you want.
<p>
Contact: <a href="http://twitter.com/enf">Eric Fischer</a>
</body>

EOF
;

if (0) {
	for $e (keys(%ENV)) {
		print "$e => $ENV{$e}<br>\n";
	}
}

exit 0;
