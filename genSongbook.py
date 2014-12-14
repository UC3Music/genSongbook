#!/usr/bin/python

import os

f = open('songbook.tex', 'w')

s = """% songbook.tex
%\documentclass[11pt,a4paper]{article}  % article format
\documentclass[11pt,a4paper,openany]{book}  % book format
\usepackage[margin=0.7in]{geometry}
%\usepackage[utf8]{inputenc}   % tildes
\usepackage{graphics}
\usepackage[dvips]{graphicx}
\usepackage{hyperref}
\usepackage{verbatim}

% next if more than 100 chapters.
\usepackage{titletoc}
\\titlecontents{chapter}[2.5em]
{\\addvspace{0.5pc}\\bfseries}
{\contentslabel{2em}}
{}
{\\titlerule*[0.3pc]{.}\contentspage}

\hypersetup{
    pdftitle={Songbook (English) - Summer 2014},
    pdfsubject={Songbook (English) - Summer 2014},
    pdfauthor={jgvictores},
    pdfkeywords={songbook} {english} {summer} {2014},
    colorlinks,
    citecolor=black,
    filecolor=black,
    linkcolor=black,
    urlcolor=black,
    bookmarks
}

\makeatletter
\\renewcommand{\@makechapterhead}[1]{%
{\setlength{\parindent}{0pt} \\raggedright \\normalfont
\\bfseries S-\\thechapter.\ #1
\par\\nobreak\\vspace{10 pt}}}
\makeatother

\\begin{document}
\Large

\\title{Songbook (English)}
\\author{by -j} 
\date{Summer 2014}

\maketitle
\cleardoublepage
\\tableofcontents
\\newpage  % book format

%-- To force blank page: 
%\\newpage
%\\thispagestyle{empty}
%\\mbox{}
"""

for dirname, dirnames, filenames in os.walk('/opt/Dropbox/lyrics/english'):
    for filename in sorted(filenames):
        s += "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
        name, extension = os.path.splitext(filename)
        s += "\chapter{" + name + "}\n"
        s += "\\begin{verbatim}\n"
        song = open( os.path.join(dirname, filename) )
        s += song.read()
        s += "\\end{verbatim}\n"
        s += "\n"

s += """
\end{document}
"""

f.write(s)


