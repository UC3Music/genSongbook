#!/usr/bin/env python

import sys, os

import mmap  # Thanks Steven @ http://stackoverflow.com/questions/4940032/search-for-string-in-txt-file-python

import subprocess

import readline

readline.set_completer_delims(' \t\n;')
readline.parse_and_bind("tab: complete")
readline.parse_and_bind("set match-hidden-files off")

import argparse

import re

inputSymbol = ''
outputSymbol = ''

def query(question, default, skipQuery=False):
    if skipQuery:
        return default
    sys.stdout.write(question + " [" + default + "] ? ")
    choice = input()
    if choice == '':
        return default
    return choice

def processBlockWithParenthesis(matchobj):
    # Print for debugging purposes: what is being treated
    print("--- " + matchobj.group(0))
    #Treat exceptions that are simply skipped and return
    if matchobj.group(0).find("capo") != -1:
        return matchobj.group(0)
    if matchobj.group(0).find("drop") != -1:
        return matchobj.group(0)
    if matchobj.group(0).find("bpm)") != -1:
        return matchobj.group(0)
    if matchobj.group(0).find("(all") != -1:
        return matchobj.group(0)
    # Remove parenthesis
    betweenParenthesis = matchobj.group(0).replace("(","").replace(")","")
    # Actual process
    betweenParenthesis = re.sub(inputSymbol, outputSymbol, betweenParenthesis)
    # Print for debugging purposes
    print("+++ " + "(" + betweenParenthesis + ")")
    # Return with parenthesis
    return "(" + betweenParenthesis + ")"

class MyArgumentDefaultsHelpFormatter(argparse.HelpFormatter):

    def _split_lines(self, text, width):
        return text.splitlines()

    def _get_help_string(self, action):
        help = action.help
        if '%(default)' not in action.help:
            if action.default is not argparse.SUPPRESS:
                defaulting_nargs = [argparse.OPTIONAL, argparse.ZERO_OR_MORE]
                if action.option_strings or action.nargs in defaulting_nargs:
                    help += ' (default: "%(default)s")'
        return help

if __name__ == '__main__':

    print("----------------------------------------")
    print("Welcome to song-directory-replace-symbol")
    print("----------------------------------------")

    parser = argparse.ArgumentParser(formatter_class = MyArgumentDefaultsHelpFormatter)

    parser.add_argument('--input',
                        help='path of the default song input directory',
                        default='examples/')
    parser.add_argument('--output',
                        help='path of the default song output directory',
                        default='out/')
    parser.add_argument('--inSymbol',
                        help='input symbol',
                        default='C')
    parser.add_argument('--outSymbol',
                        help='output symbol',
                        default='Do')
    parser.add_argument('--yes',
                        help='accept all, skip all queries',
                        nargs='?',
                        default='NULL')  # required, see below
    args = parser.parse_args()

    skipQueries = False
    if args.yes is not 'NULL':  # if exists and no contents, replaces 'NULL' by None
        print("Detected --yes parameter: will skip queries")
        skipQueries = True

    # Query the path of the song input directory
    inputDirectory = query("Please specify the path of the song input directory", args.input, skipQueries)
    print("Will use song input directory: " + inputDirectory)

    # Query the path of the song output directory
    outputDirectory = query("Please specify the path of the song output directory", args.output, skipQueries)

    # Query the input symbol
    inputSymbol = query("Please specify the input symbol", args.inSymbol, skipQueries)

    # Query the output symbol
    outputSymbol = query("Please specify the output symbol", args.outSymbol, skipQueries)

    if os.path.isdir(outputDirectory):
        yesNo = query('Path "' + outputDirectory + '" already exists, are you sure (confirm with "y" or "yes" without quotes)', 'yes', skipQueries)
        if yesNo != "yes" and yesNo != "y":
            print("Ok, bye!")
            quit()
        else:
            print("Will use (existing) song output directory: " + outputDirectory)
    else:
        os.makedirs(outputDirectory)
        print("Will use (newly created) song output directory: " + outputDirectory)

    print("----------------------")

    #sys.stdout.write(s)  #-- Screen output for debugging.

    rep = ""
    for dirname, dirnames, filenames in os.walk(inputDirectory):
        for filename in sorted(filenames):
            #debug
            print(filename)
            songIn = open( os.path.join(dirname, filename), encoding="utf8" )
            songOut = open(os.path.join(outputDirectory, filename), "w", encoding="utf8")
            contents = songIn.read()
            contents = re.sub("\([^)]*\)", processBlockWithParenthesis, contents) # line that really does it
            songOut.write(contents)
            songOut.close()
            songIn.close()
