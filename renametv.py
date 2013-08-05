#!/usr/bin/python2
__VERSION__ = '0.1'
import os				# For running system commands.
import argparse			# For argument parsing.
import re				# For regular expressions
import pickle			# For storing directory mappings

#TODO: Save a json file of the filenames, what they started as and ended as. Implement a "reversal" function that'll return files to their original names.

### Parsing command arguments
parser = argparse.ArgumentParser(description='Sync your development code trees.')
parser.add_argument('directory', metavar='DIRECTORY', type=str,
					help='Directory of the selected TV show.')
parser.add_argument('-a', '--auto', action='store_const', const=True, required=False, default=False,
					help='Automatically generate filenames based on file order.')
parser.add_argument('-sl', '--seasonlength', action='store_const', const=True, required=False, default=2,
					help='Set length of season number representation. Ex: "2"=>"S01", "3" => "S001". [Default is 2]')
parser.add_argument('-el', '--episodelength', action='store_const', const=True, required=False, default=2,
					help='Set length of episode number representation. Ex: "2"=>"E01", "3" => "E001". [Default is 2]')
parser.add_argument('-v', '--version', action='version', version='%(prog)s '+__VERSION__)

# Parsing argument values into the 'args' namespace object.
args = parser.parse_args()

def autoRename(dir):
	s_rg = re.compile('[0-9]{1,2}')
	ext_rg = re.compile('\..+')
	list = {}
	for top_dirname, top_dirnames, top_filenames in os.walk(dir):
		if top_dirname == dir:
			continue
		season = top_dirname.replace(dir+"/","")
		m = s_rg.search(season)
		if m:
			season_num = str(m.group()).zfill(args.seasonlength)
			list[season_num] = {}
			num = 1
			for filename in top_filenames:
				ep_str = str("{0:0"+str(args.episodelength)+"d}").format(num)
				ext = ext_rg.search(filename).group()
				new_name = "S"+season_num+"E"+ep_str+ext
				list[season_num][filename] = new_name
				os.rename(top_dirname+"/"+filename,top_dirname+"/"+new_name)
				num+=1

	print "All done renaming!"
	print "Here's the renaming map ..."
	print list
	print "Saving directory map ..."
	fh = open(args.directory+'.map','wb')
	pickle.dump(list,fh)
	fh.close()
	print "Saved as "+args.directory+'.map'+"!"
	return True

### rename.tv logic.
tree = list()
# -a flag "required" right now, until an alternative method is developed.
if args.auto:
	autoRename(args.directory)
else:
	print "Not yet."