#!/usr/bin/env python3

# TODO:
# calendar should start on the week that contains 1 january
# calendar should end on the week that contains 31 december
# week numbers should be correct

# from: https://tex.stackexchange.com/questions/220980/organiser-refills-inlays-using-latex
import calendar
import sys

########## CUSTOMIZATIONS ##########

## Year
year = int(sys.argv[1]) if len(sys.argv) > 1 else 2023

# Labels
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
#months = [calendar.LocaleTextCalendar().formatmonthname(year,i,1).split(' ')[0] for i in range(1,13)]

labels = {
   'label_week':       'Week',
   'label_monday':     'Monday',
   'label_tuesday':    'Tuesday',
   'label_wednesday':  'Wednesday',
   'label_thursday':   'Thursday',
   'label_friday':     'Friday',
   'label_saturday':   'Saturday',
   'label_sunday':     'Sunday',
}

## Morning starttime
starttime="8"

## Evening time
stoptime="20"

## Starttime sunday
# Min \starttime+1
# Max \stoptime-2

sundaybegin="14"

## Rule width thick
thickrulewidth="2pt"

## Midrule width
midrulewidth="0.67pt"

## Thinrule width
thinrulewidth=".335pt"

## Extra space
extrarowheight="3.25pt"

#
####################################
#

days = {
    0: 'pymond',
    1: 'pytue',
    2: 'pywed',
    3: 'pythur',
    4: 'pyfr',
    5: 'pysat',
    6: 'pysun'
}

#Collect all mondays in a list
mondays = []

for month in range( 1, 13 ):

   for week in calendar.monthcalendar(year,month):

      if not week[0] == 0:
         mondays.append( [week[0], 0] )

# If year doesn't end with a friday, append January to months
if calendar.monthcalendar(year, 12)[-1][-1] == 0:
    months.append( months[0] )

Nweeks = len(mondays)

# Add length of corresponding month to each monday
month = 1
for week in range( Nweeks ):

   Ndaysinmonth = calendar.monthrange( year, month )[1]

   # First week
   if week == 0:
      mondays[week][1] = Ndaysinmonth

   # Increasing day in month => same month
   elif mondays[week][0] > mondays[week-1][0]:
      mondays[week][1] = Ndaysinmonth

   # Next month
   else:
      mondays[week][1] = calendar.monthrange( year, month+1 )[1]
      month+=1

head = r'''
   \documentclass[%
      BCOR=2cm,%  Space for hole puncher
      DIV=30,%   Size of textbody
      paper=a4,%  A4 paper
      fontsize=12pt%    Fontsize
   ]{scrbook}
   %
   %%%%%%%%%% PACKAGES %%%%%%%%%%
   %
   \usepackage{tabularx,booktabs,multirow}
   %\usepackage{pgfpages}
   \usepackage{helvet} % font package
   \renewcommand{\familydefault}{\sfdefault} % use sans serif font by default
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
      \multicolumn{6}{l}{\printmonthleft \hfill {label_week} \the\week}\\[.2em]\midrule[\rulew]
      \addlinespace[.5em]
      \multicolumn{2}{l}{\printday{\the\datemonday}{label_monday}}     &%
      \multicolumn{2}{l}{\printday{\the\datetuesday}{label_tuesday}}   &%
      \multicolumn{2}{l}{\printday{\the\datewednesday}{label_wednesday}}\\[2cm]
       & & & & & \\\lendt
      \tabledataleft
       & & & & & \\\lendt
   \end{tabularx}
   %
   \vfill
   % \footer % disable `––– year –––` footer
   %
   \clearpage
   \enlargethispage{1cm}
   %
   %%%%%%%%%% RIGHT TABLE %%%%%%%%%%
   %
   \noindent
   \begin{tabularx}{\linewidth}{lXlXlX}
      % \multicolumn{6}{l}{{label_week} \the\week \hfill \printmonthright}\\[.2em]\midrule[\rulew]
      \multicolumn{6}{l}{{pyyear} \hfill \printmonthright}\\[.2em]\midrule[\rulew]
      \addlinespace[.5em]
      \multicolumn{2}{l}{\printday{\the\datethursday}{label_thursday}}  &%
      \multicolumn{2}{l}{\printday{\the\datefriday}{label_friday}}     &%
      \multicolumn{2}{l}{\printday{\the\datesaturday}{label_saturday}}  \\[2cm]
      & & & & & \\\lendt
      \tabledatarightupper
      & & & & & \\\lsunt{\mrulew}
      \addlinespace[-.15em]
      \the\sundaybegin & & \the\sundaybegin & & \multicolumn{2}{l}{\multirow{4}{*}[1.5em]{\printday{\the\datesunday}{label_sunday}}}\\\lsun{\trulew}
      \tabledatarightinter
      & & & & & \\\lsun{\mrulew}
      \the\sundaystop & & \the\sundaystop & & & \\\lsunt{\trulew}
      \tabledatarightlower
      & & & & & \\\lendt
   \end{tabularx}
   %
   \vfill
   % \footer % disable `––– year –––` footer
   \clearpage'''

for key in labels:
    table = table.replace(key, labels[key])

foot = r'''\end{document}'''

head = head.replace("pyyear",           str(year)      )
head = head.replace("pystarttime",      starttime      )
head = head.replace("pystoptime",       stoptime       )
head = head.replace("pysundaybegin",    sundaybegin    )
head = head.replace("pyextrarowheight", extrarowheight )
head = head.replace("pyrulewidth",      thickrulewidth )
head = head.replace("pymidrulewidth",   midrulewidth   )
head = head.replace("pythinrulewidth",  thinrulewidth  )

print(head)

week_num = 1
if mondays[0][0] != 1: week_num += 1

currentmonth = 0
for week in range(Nweeks):

   table_temp = table
   trigger = 0

   for weekday in range(7):

      date = mondays[week][0] + weekday

      # If it's monday 1 st, increase currentmonth unless it's January 1 st.
      if date == 1 and not (mondays[0][0] == 1 and currentmonth == 0):
         currentmonth += 1
         trigger = 1

      # If next month
      if date > mondays[week][1]:

         date = date - mondays[week][1]

         if trigger == 0:
            currentmonth += 1
            trigger = 1

         # Print right page
         if weekday > 2:
            table_temp = table_temp.replace('pymonthright', months[currentmonth])

         # Print left page
         else:
            table_temp = table_temp.replace('pymonthleft', months[currentmonth])

      else:

         # Print left page
         if weekday == 2:
            table_temp = table_temp.replace('pymonthleft', months[currentmonth])

         # Print right page
         elif weekday == 6:
            table_temp = table_temp.replace('pymonthright', months[currentmonth])

      table_temp = table_temp.replace(days[weekday], str(date))

   table_temp = table_temp.replace("pyweek", str(week_num))
   table_temp = table_temp.replace("pyyear", str(year))
   
   print(table_temp)
   week_num += 1

print(foot)