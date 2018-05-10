import csv
import urllib2
import re

# Config

sourcefile = 'config/youtube.txt'
destfile = '_youtube/index.md'

dest = open(destfile, 'w')

with open(sourcefile, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        dest.write('# Round ' + row[0] + '\n')
        dest.write('**' + row[1] + ':** [YouTube Link](' + row[2] + ')\n')

contents = urllib2.urlopen("https://www.danlisa.com/scoring/season_standings.php?season_id=7666").read()
scripts = [m.start() for m in re.finditer("<script language='javascript'>",contents)]
scriptends = [m.start() for m in re.finditer("</script>",contents)]

ranges = []
for start in scripts:
    while scriptends[0] < start:
        scriptends = scriptends[1:]
    ranges.append([start,scriptends[0]])
    scriptends = scriptends[1:]

textscripts = []
for r in ranges:
    textscripts.append(contents[r[0]+30: r[1]])

results = []

for texty in textscripts:
    if texty.find("drivers")!=-1:
        x = texty.split("\n")
        for y in x:
            if y != '':
                a = [y[y.find("{")+1:y.find("}")]]
                for line in a:
                    d = {}
                    p = line.replace(", ","+ ")
                    newp = p.split(",")
                    for item in newp:
                        i = item.split(":")
                        d[i[0]]=i[1].replace("+ ",", ")
                    results.append(d)

print results