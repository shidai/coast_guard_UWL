"""
Given a PSRCHIVE archive clean it up.

Patrick Lazarus, Nov. 11, 2011
"""
import optparse
import sys
import types
import re
import shutil
import os
import tempfile
import argparse
import warnings

import numpy as np
import scipy.stats
import matplotlib.pyplot as plt

from coast_guard import config
from coast_guard import utils
from coast_guard import clean_utils
from coast_guard import errors
from coast_guard import cleaners
from coast_guard import colour
#import config
#import utils
#import clean_utils
#import errors
#import cleaners
#import colour

#def main():
#    print ""
#    print "         clean.py"
#    print "     Patrick  Lazarus"
#    print ""
#    file_list = args.files + args.from_glob
#    to_exclude = args.excluded_files + args.excluded_by_glob
#    to_clean = utils.exclude_files(file_list, to_exclude)
#    print "Number of input files: %d" % len(to_clean)
#    
#    
#    # Read configurations
#    for infn in to_clean:
#        inarf = utils.ArchiveFile(infn)
#        config.cfg.load_configs_for_archive(inarf)
#        outfn = utils.get_outfn(args.outfn, inarf)
#        shutil.copy(inarf.fn, outfn)
#        
#        outarf = utils.ArchiveFile(outfn)
#        ar = outarf.get_archive()
#        
#        try:
#            for name, cfgstrs in args.cleaner_queue:
#                # Set up the cleaner
#                cleaner = cleaners.load_cleaner(name)
#                print(infn, args.outfn, cfgstrs, name)
#                for cfgstr in cfgstrs:
#                    cleaner.parse_config_string(cfgstr)
#                    print(infn, args.outfn, cfgstr)
#                cleaner.run(ar)
#        except:
#            # An error prevented cleaning from being successful
#            # Remove the output file because it may confuse the user
#            #if os.path.exists(outfn):
#            #    os.remove(outfn)
#            raise
#        finally:
#            print(outfn)
#            ar.unload(outfn)
#            print "Cleaned archive: %s" % outfn
#        
#    
#class CleanerArguments(utils.DefaultArguments):
#    def __init__(self, *args, **kwargs):
#        super(CleanerArguments, self).__init__(add_help=False, \
#                                                *args, **kwargs)
#        self.add_argument('-h', '--help', nargs='?', dest='help_topic', \
#                            metavar='CLEANER', \
#                            action=self.HelpAction, type=str, \
#                            help="Display this help message. If provided "
#                                "with the name of a cleaner, display "
#                                "its help.")
#
#    class HelpAction(argparse.Action):
#        def __call__(self, parser, namespace, values, option_string):
#            if values is None:
#                parser.print_help()
#            else:
#                cleaner = cleaners.load_cleaner(values)
#                print cleaner.get_help(full=True)
#            sys.exit(1)
#
#    class ListCleanersAction(argparse.Action):
#        def __call__(self, parser, namespace, values, option_string):
#            colour.cprint("Available Cleaners:", \
#                            bold=True, underline=True) 
#            for name in sorted(cleaners.registered_cleaners):
#                cleaner = cleaners.load_cleaner(name)
#                print cleaner.get_help()
#            sys.exit(1)
#
#    class AppendCleanerAction(argparse.Action):
#        def __call__(self, parser, namespace, values, option_string):
#            # Append the name of the cleaner and an empty list for
#            # configuration strings
#            getattr(namespace, self.dest).append((values, []))
#
#    class ConfigureCleanerAction(argparse.Action):
#        def __call__(self, parser, namespace, values, option_string):
#            # Append configuration string to most recently added
#            # cleaner
#            getattr(namespace, 'cleaner_queue')[-1][1].append(values)
#
#
#if __name__=="__main__":
#    parser = CleanerArguments(usage="%(prog)s [OPTIONS] FILES ...", \
#                        description="Given a list of PSRCHIVE file names " \
#                                    "clean RFI from each one.")
#    parser.set_defaults(cleaner_queue=[])
#    parser.add_argument('files', nargs='*', \
#                        help="Files to clean.")
#    parser.add_argument('-o', '--outname', dest='outfn', type=str, \
#                        help="The output (reduced) file's name. " \
#                            "(Default: '%%(name)s_%%(yyyymmdd)s_%%(secs)05d_cleaned.ar')", \
#                        default="%(name)s_%(yyyymmdd)s_%(secs)05d_cleaned.ar")
#    parser.add_file_selection_group()
#    parser.add_argument('-F', '--cleaner', dest='cleaner_queue', \
#                        action=parser.AppendCleanerAction, type=str, \
#                        help="A string that matches one of the names of " \
#                             "the available cleaning functions.")
#    parser.add_argument('-c', dest='cfgstr', \
#                        action=parser.ConfigureCleanerAction, type=str, \
#                        help="A string of Cleaner configurations to " \
#                            "apply to the cleaner most recently added " \
#                            "to the queue.")
#    parser.add_argument('--list-cleaners', nargs=0, \
#                        action=parser.ListCleanersAction, \
#                        help="List available cleaners and descriptions, then exit.")
#    args = parser.parse_args()
#    main()

def run_coastguard (calname, cal_dz):
    #calname = sys.argv[1]
    #cal_dz = sys.argv[2]
    
    print calname
    inarf = utils.ArchiveFile(calname)
    config.cfg.load_configs_for_archive(inarf)
    outfn = utils.get_outfn(cal_dz, inarf)
    shutil.copy(inarf.fn, outfn)
    
    outarf = utils.ArchiveFile(outfn)
    ar = outarf.get_archive()
    
    cleaner = cleaners.load_cleaner('preclean')   # hard coded, need to be fixed
    #for cfgstr in cfgstrs:
    #    cleaner.parse_config_string(cfgstr)
    cleaner.run(ar)
    
    cleaner = cleaners.load_cleaner('surgical')   # hard coded, need to be fixed
    cleaner.run(ar)

    print(type(outfn))
    ar.unload(str(outfn))
    print "Cleaned archive: %s" % outfn

filename = sys.argv[1]
print filename
run_coastguard(filename, filename+'.cg')
