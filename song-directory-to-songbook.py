#!/usr/bin/env python

import sys, os

import mmap  # Thanks Steven @ http://stackoverflow.com/questions/4940032/search-for-string-in-txt-file-python

import subprocess

import readline

readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.parse_and_bind("set match-hidden-files off")

import argparse

def query(question, default, skipQuery=False):
    if skipQuery:
        return default
    sys.stdout.write(question + " [" + default + "] ? ")
    choice = raw_input()
    if choice == '':
        return default
    return choice

if __name__ == '__main__':

    print("-------------------------------------")
    print("Welcome to song-directory-to-songbook")
    print("-------------------------------------")

    parser = argparse.ArgumentParser()

    parser.add_argument('--input',
                        help='specify the path of the default song (input) directory',
                        default='/home/yo/Dropbox/chords/0-GUITAR/english')
    parser.add_argument('--output',
                        help='specify the (output) pdf file [without extension]',
                        default='songbook')
    parser.add_argument('--template',
                        help='specify the LaTeX template file [specifies language, etc]',
                        default='template/english.tex')
    parser.add_argument('--manifest',
                        help='[optional] specify the path of a file-avoiding manifest file',
                        default='')
    parser.add_argument('--yes',
                        help='[optional] accept all, skip all queries',
                        nargs='?',
                        default='absent')  # required, see below
    args = parser.parse_args()

    skipQueries = False
    if args.yes is not 'absent':  # if exists and no contents, replaces 'absent' by None
        print("Detected --yes parameter: will skip queries")
        skipQueries = True

    # Query the path of the song (input) directory
    inputDirectory = query("Please specify the path of the song (input) directory", args.input, skipQueries)
    print("Will use song (input) directory: " + inputDirectory)

    # Query the path of the song (input) directory
    outputFile = query("Please specify the (output) pdf file [without extension]", args.output, skipQueries)
    print("Will use the (output) pdf file [without extension]: " + outputFile)

    # Query the path of the template file
    templateFile = query("Please specify the path of the LaTeX template file [specifies language, format]", args.template, skipQueries)
    print("Will use template file: " + templateFile)

    # Query (optional) the path of a file-avoiding manifest file
    manifestFile = query("[optional] Please specify the path of a file-avoiding manifest file", args.manifest, skipQueries)
    if manifestFile == "":
        print("Not using file-avoiding manifest file.")
    else:
        print("Will use file-avoiding manifest file: " + manifestFile)
        manifestFileFd = open(manifestFile, 'r')
        manifestMmap = mmap.mmap(manifestFileFd.fileno(), 0, access=mmap.ACCESS_READ)
        manifestFileFd.close()

    print("----------------------")

    templateFileFd = open(templateFile, 'r')
    s = templateFileFd.read()
    #sys.stdout.write(s)  #-- Screen output for debugging.

    rep = ""
    for dirname, dirnames, filenames in os.walk(inputDirectory):
        for filename in sorted(filenames):
            name, extension = os.path.splitext(filename)
            if manifestFile != "":
                if manifestMmap.find(name) != -1:
                    print "Skipping:", name
                    continue
            rep += "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n"
            rep += "\\chapter{" + name + "}\n"  #-- Note that we use \\ instead of \.
            songName = name.split(" - ")[-1]
            rep += "\\index{{song}}{" + songName + "}\n"
            rep += "\\begin{alltt}\n"
            song = open( os.path.join(dirname, filename) )
            rep += song.read()
            song.close()
            rep += "\\end{alltt}\n"
            rep += "\n"
    #sys.stdout.write(rep)  #-- Screen output for debugging.

    rep = rep.replace("(","\\textbf{(")
    rep = rep.replace(")",")}")

    rep = rep.replace("[","\\textit{[")
    rep = rep.replace("]","]}")

    rep = rep.replace("{{song}}","[song]")

    s = s.replace("genSongbook",rep)

    outName = outputFile + ".tex"
    outFd = open(outName, 'w')
    outFd.write(s)
    outFd.close()

    #http://stackoverflow.com/questions/6818102/detect-and-handle-a-latex-warning-error-generated-via-an-os-system-call-in-pytho
    #pdftex_process = subprocess.Popen(['pdflatex', '-interaction=nonstopmode', '%s'%topic], shell=False, stdout=subprocess.PIPE)
    pdftex_process = subprocess.call(['pdflatex', outputFile])
    pdftex_process = subprocess.call(['pdflatex', outputFile])
