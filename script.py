# from: https://tex.stackexchange.com/questions/220980/organiser-refills-inlays-using-latex
import numpy as np
import calendar
import sys

weeks = 52
mondays = np.zeros((weeks,2)) # [ [ 0.  0.], ... ]
days = {0: 'pymond', 1: 'pytue', 2: 'pywed', 3: 'pythur', 4: 'pyfr', 5: 'pysat', 6: 'pysun'}
months = {0: 'January',1: 'February',2: 'March',3: 'April',4: 'May',5: 'June',6: 'July',7: 'August',8: 'September',9: 'October',10: 'November',11: 'December', 12: 'January'}

########## CUSTOMISATIONS ##########
#
## Year
year=2019
## Morning starttime
starttime=8
## Evening time
stoptime=20
## Starttime sunday
# Min \starttime+1
# Max \stoptime-2
sundaybegin=14
## Thick rule width thick
thickrulewidth="2pt"
## Mid rule width
midrulewidth="0.67pt"
## Thin rule width
thinrulewidth=".335pt"
## Extra space
extrarowheight="3.25pt"
#
####################################
#




#Get mondays
#e.g.: [[  7.   7.], [ 14.  14.], [ 21.  21.], [ 28.  28.], [  4.   4.], [ 11.  11.], ... ]
k=0
for month in xrange(12):
    month+=1 # month: 1..12
    monthcal = calendar.monthcalendar(year,month) #
    # print month, monthcal
    for weekinmonth in xrange(len(monthcal)):
        if monthcal[weekinmonth][0] == 0: pass
        else:
            if k < weeks:
                mondays[k] = monthcal[weekinmonth][0]
            k+=1


# Get monthrange
j=0
for i in xrange(weeks):
    monthrange = calendar.monthrange(year,j+1)[1]
    if i == 0: mondays[i,1] = monthrange
    elif mondays[i,0] > mondays[i-1,0]: mondays[i,1] = monthrange
    else:
        mondays[i,1] = calendar.monthrange(year,j+2)[1]
        j+=1

# print mondays
# sys.exit(0)


head = r'''
    \documentclass[%
        BCOR=2cm,%  Space for hole puncher
        DIV=30,%    Size of textbody
        paper=a4,%  A4 paper
        fontsize=12pt%     Fontsize
    ]{scrbook}
    %
    %%%%%%%%%% PACKAGES %%%%%%%%%%
    %
    \usepackage{tabularx,booktabs,multirow}
    \usepackage{helvet} % font package
    \renewcommand{\familydefault}{\sfdefault} % use sans serif font by default
    % Wrong page order. Needed for two-side printing: {2,3}, {4,1}, {6,7}, {8,5}, ...
    %\usepackage{pgfpages}
    %\pgfpagesuselayout{2 on 1}[odd numbered pages right,a4paper,landscape,border shrink=0mm]
    %%%%%%%%%% COUNTER %%%%%%%%%%
    %
    \newcount\counter
    \newcount\startdate
    \newcount\starttime
    \newcount\stoptime
    \newcount\sundaybegin
    \newcount\week
    \newcount\datemonday
    \newcount\datetuesday
    \newcount\datewednesday
    \newcount\datethursday
    \newcount\datefriday
    \newcount\datesaturday
    \newcount\datesunday
    %
    %%%%%%%%%% CUSTOMISATIONS %%%%%%%%%%
    %
    %% Morning starttime
    \starttime=pystarttime
    %% Evening time
    \stoptime=pystoptime
    %% Starttime sunday
    % Min \starttime+1
    % Max \stoptime-2
    \sundaybegin=pysundaybegin
    %% Rule width thick
    \newcommand{\rulew}{pyrulewidth}
    %% Midrule width 
    \newcommand{\mrulew}{pymidrulewidth}
    %% thinrule width 
    \newcommand{\trulew}{pythinrulewidth}
    %% Extra space
    \setlength{\extrarowheight}{pyextrarowheight}
    %
    %%%%%%%%%% DEFINITIONS %%%%%%%%%%
    %
    \newcommand{\lendt}{\cmidrule[\rulew](l){1-2}\cmidrule[\rulew](l){3-4}\cmidrule[\rulew](l){5-6}}
    \newcommand{\lend}[1]{\cmidrule[#1](l){1-2}\cmidrule[#1](l){3-4}\cmidrule[#1](l){5-6}}
    \newcommand{\lsun}[1]{\cmidrule[#1](l){1-2}\cmidrule[#1](l){3-4}}
    \newcommand{\lsunt}[1]{\cmidrule[#1](l){1-2}\cmidrule[#1](l){3-4}\cmidrule[\rulew](l){5-6}}
    \newcommand{\printday}[2]{{\LARGE \textbf{#1}}\,\, \large \textbf{#2}}
    \newcommand{\neutralline}{& & & & &}
    \newcommand{\footer}{\centering\rule{7cm}{\cmidrulewidth} \raisebox{-0.5ex}{pyyear} \rule{7cm}{\cmidrulewidth}}
    \newcommand{\printmonthleft}{{\LARGE \textbf{pymonthleft}}}
    \newcommand{\printmonthright}{{\LARGE \textbf{pymonthright}}}
    %
    \advance\stoptime1
    \begin{document}
    \thispagestyle{empty}
    \mbox{}
    \clearpage
    '''

table = r'''
    %% Weeknumber
    \week=pyweek
    \renewcommand{\printmonthleft}{{\LARGE \textbf{pymonthleft}}}
    \renewcommand{\printmonthright}{{\LARGE \textbf{pymonthright}}}
     %% Dates
    \datemonday=pymond
    \datetuesday=pytue
    \datewednesday=pywed
    \datethursday=pythur
    \datefriday=pyfr
    \datesaturday=pysat
    \datesunday=pysun
    %
    %
    %%%%%%%%%% TABLE CONTENT LEFT SIDE %%%%%%%%%%
    %
    \long\def\addto#1#2{\expandafter\def\expandafter#1\expandafter{#1#2}}
    %
    \def\tabledataleft{} \counter=\the\starttime
    \loop
        \edef\tabline{\the\counter &  & \the\counter & & \the\counter & }
        \expandafter\addto\expandafter\tabledataleft\expandafter{\neutralline \\\lend{\mrulew}}
        \expandafter\addto\expandafter\tabledataleft\expandafter{\tabline \\\lend{\trulew}}
        \advance \counter 1
        \ifnum \counter<\the\stoptime
    \repeat 
    %
    %%%%%%%%%% TABLE CONTENT RIGHT SIDE %%%%%%%%%%
    %
    \def\tabledatarightupper{} \counter=\the\starttime
    \loop
        \edef\tabline{\the\counter &  & \the\counter & & & }
        \expandafter\addto\expandafter\tabledatarightupper\expandafter{\neutralline \\\lend{\mrulew}}
        \expandafter\addto\expandafter\tabledatarightupper\expandafter{\tabline \\\lend{\trulew}}
        \advance \counter 1
        \ifnum \counter<\the\sundaybegin
    \repeat 
    %
    \advance\sundaybegin1
    \def\tabledatarightinter{} \counter=\the\sundaybegin
    \newcount\sundaystop
    \sundaystop=\the\sundaybegin
    \advance\sundaystop1
    \loop
        \edef\tabline{\the\counter &  & \the\counter & & & }
        \expandafter\addto\expandafter\tabledatarightinter\expandafter{\neutralline \\\lsun{\mrulew}}
        \expandafter\addto\expandafter\tabledatarightinter\expandafter{\tabline \\\lsun{\trulew}}
        \advance \counter 1
        \ifnum \counter<\the\sundaystop
    \repeat 
    \advance\sundaybegin-1
    \advance\sundaystop1
    %
    \def\tabledatarightlower{} \counter=\the\sundaystop
    \loop
        \edef\tabline{\the\counter &  & \the\counter & & & }
        \expandafter\addto\expandafter\tabledatarightlower\expandafter{\neutralline \\\lend{\mrulew}}
        \expandafter\addto\expandafter\tabledatarightlower\expandafter{\tabline \\\lend{\trulew}}
        \advance \counter 1
        \ifnum \counter<\the\stoptime
    \repeat 
    \advance\sundaystop-1
    %
    \pagestyle{empty}
    \enlargethispage{1cm}
    %
    %%%%%%%%%% LEFT TABLE %%%%%%%%%%
    %
    \noindent
    \begin{tabularx}{\linewidth}{lXlXlX}
        \multicolumn{6}{l}{\printmonthleft \hfill Week \the\week}\\[.2em]\midrule[\rulew]
        \addlinespace[.5em]
        \multicolumn{2}{l}{\printday{\the\datemonday}{Monday}}      &%
        \multicolumn{2}{l}{\printday{\the\datetuesday}{Tuesday}}    &%
        \multicolumn{2}{l}{\printday{\the\datewednesday}{Wednesday}}\\[2cm]
         & & & & & \\\lendt
        \tabledataleft
         & & & & & \\\lendt
    \end{tabularx}
    %
    \vfill
    %\footer
    %
    \clearpage
    \enlargethispage{1cm}
    %
    %%%%%%%%%% RIGHT TABLE %%%%%%%%%%
    %
    \noindent
    \begin{tabularx}{\linewidth}{lXlXlX}
        \multicolumn{6}{l}{pyyear \hfill \printmonthright}\\[.2em]\midrule[\rulew]
        \addlinespace[.5em]
        \multicolumn{2}{l}{\printday{\the\datethursday}{Thursday}}  &%
        \multicolumn{2}{l}{\printday{\the\datefriday}{Friday}}      &%
        \multicolumn{2}{l}{\printday{\the\datesaturday}{Saturday}}  \\[2cm]
        & & & & & \\\lendt
        \tabledatarightupper
        & & & & & \\\lsunt{\mrulew}
        \addlinespace[-.15em]
        \the\sundaybegin & & \the\sundaybegin & & \multicolumn{2}{l}{\multirow{4}{*}[1.5em]{\printday{\the\datesunday}{Sunday}}}\\\lsun{\trulew}
        \tabledatarightinter
        & & & & & \\\lsun{\mrulew}
        \the\sundaystop & & \the\sundaystop & & & \\\lsunt{\trulew}
        \tabledatarightlower
        & & & & & \\\lendt
    \end{tabularx}
    %
    \vfill
    %\footer
    \clearpage'''

foot = r'''\end{document}'''

head = head.replace("pyyear",  str(year).replace('.0',''))
head = head.replace("pystarttime",  str(starttime).replace('.0',''))
head = head.replace("pystoptime",   str(stoptime).replace('.0',''))
head = head.replace("pysundaybegin",str(sundaybegin).replace('.0',''))
head = head.replace("pyextrarowheight", extrarowheight)
head = head.replace("pyrulewidth",  thickrulewidth)
head = head.replace("pymidrulewidth", midrulewidth)
head = head.replace("pythinrulewidth", thinrulewidth)

print head

week=1
if mondays[0,0] != 1:week+=1
k=0
for i in xrange(len(mondays[:,0])):
    table_temp = table
    trigger=0
    for j in xrange(7):
        date = mondays[i,0] + j
        if date==1 and i!=0:
            k+=1
            trigger=1
        else:pass
        #if k==6 or k==7:
#        print date,'/', mondays[i,1], months[k], j, k, trigger
#        raw_input()
        if date > mondays[i,1]:
            date = (mondays[i,0] + j)%mondays[i,1]
            if j > 2:
                if k<12 and trigger == 0:
                    k+=1
                    trigger=1
                table_temp = table_temp.replace('pymonthright', months[k])
            else:
                if k<12 and trigger == 0:
                    k+=1
                    trigger=1
                table_temp = table_temp.replace('pymonthleft', months[k])
        else:
            if j == 2:
                table_temp = table_temp.replace('pymonthleft', months[k])
#                trigger = 0
            elif j == 6:
                table_temp = table_temp.replace('pymonthright', months[k])

        table_temp = table_temp.replace(days[j], str(date).replace('.0',''))

    table_temp = table_temp.replace("pyweek", str(week).replace('.0',''))
    table_temp = table_temp.replace("pyyear", str(year).replace('.0',''))
    print table_temp
    week+=1


print foot
