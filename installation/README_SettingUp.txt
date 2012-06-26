# Description: Instructions for setting up protein function prediction prototype.
#
# Author: Michael L. Souza
# Date: Jan. 25, 2012
#

The following are used at the time of writing:
 Python 2.7.2
 Python Libraries:
 Read/Write access to a MySQL server.
	The database to use is specified in global_settings.py
	For setup need to be able to create/drop tables, and insert/update/select from tables.
 
Setting up databases:
	Download/import Pfam (MySQL):
		See biodbs/pfam/download_pfam_mysql_files.sh
		Edit the top of biodbs/pfam/import_tables_for_all_in_dir.py
	Download/hmmpress Pfam (Flatfiles):
		$ wget ftp://ftp.sanger.ac.uk/pub/databases/Pfam/releases/Pfam26.0/Pfam-A.hmm.gz && gunzip Pfam-A.hmm.gz
		$ /path/to/hmmr3/hmmpress /path/to/Pfam-A.hmm
	
	Set up GO and GO Annotations:
		$ wget http://www.geneontology.org/external2go/ec2go
		$ wget http://archive.geneontology.org/latest-termdb/go_daily-termdb-tables.tar.gz

Specifying initial configuration options:
	Edit the file settings/SifterAnalysisProject_default_settings.cfg

Command line:
	Run tool with "--help"

Examples:
	See Examples/ and PySIFTER/Tests/
	

------------------------------------------------------------------------

