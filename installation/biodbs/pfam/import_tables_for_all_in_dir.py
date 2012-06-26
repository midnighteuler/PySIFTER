#!/usr/bin/env python
import Queue
import threading
import sys, os, fnmatch
import time
import tempfile
#import _mysql as mysql
#import _mysql_exceptions as mysql_exceptions

mysql_server_address = 'localhost'
mysql_user = 'root'
mysql_password  = 'mysql1234'
mysql_db = 'sifter_db'

sys.path.append(os.path.realpath(os.getcwd())) # Adds invoking directory
#from global_settings import *

class ProcessingThread(threading.Thread):
	"""Thread for running sequence alignments on a given input homolog cluster."""
	def __init__(self, thread_queue):
		threading.Thread.__init__(self)
		self.thread_queue = thread_queue
	
	def thread_operation(self, thread_data):
		input_file_name, output_prefix = thread_data
		self.output_prefix = output_prefix
		
		print "Importing table:", input_file_name
		try:
			
			cmd1 = "zcat " + input_file_name + ".sql.gz" \
				+ " | mysql -u " + mysql_user \
				+ " --password=" + mysql_password \
				+ " " + mysql_db
			
			print "Loading schema: " + input_file_name
			print cmd1
			os.system(cmd1)
			
			fd, tmppipe = tempfile.mkstemp(prefix = 'tmpmysqlpipe') # just gets a usable tmp name
			os.unlink(tmppipe)
			#tmppipe = 'asdf'
			cmd2 = "mkfifo "+tmppipe+" && zcat " + input_file_name + ".txt.gz > " + tmppipe + " & " \
					+ "mysql -u " + mysql_user \
					+ " --password=" + mysql_password \
					+ " --database=" + mysql_db \
					+ ' -e "LOAD DATA LOCAL INFILE \''+tmppipe+'\' into table '+self.output_prefix+'"' \
					+ " && rm " + tmppipe
			
			print "Loading data for: " + input_file_name
			print cmd2
			os.system(cmd2)
			
			
			
			#db.query("load data local infile '"+db_data_location+"/pfamA.txt' into table pfamA;")
			print "Done."
		except Exception as e:
			print >> sys.stderr, "Error importing table!"
			print >> sys.stderr, "Error: ", e
			exit(1)
		
		
		print "Finished importing table for:", input_file_name
	
	def flag_start(self):
		f = open(self.output_prefix + ".mysql.processing", 'w')
		f.close()
	
	def unflag_start(self):
		os.remove(self.output_prefix + ".mysql.processing")
	
	def flag_finish(self):
		self.unflag_start()
		f = open(self.output_prefix + ".mysql.processed", 'w')
		f.close()
	
	def run(self):
		while True:
			# Spawn a thread with data from the queue
			thread_data = self.thread_queue.get()
			self.output_prefix = thread_data[1]
			
			# Run thread's function on the data
			try:
				self.flag_start()
				self.thread_operation(thread_data)
				self.flag_finish()
			except:
				self.unflag_start()
				print "Unexpected thread error:", sys.exc_info()[0]
				print "Thread data:", thread_data
			
			# Send signal that this task finished
			self.thread_queue.task_done()

def main():
	if len(sys.argv) < 3 or not(os.path.isdir(sys.argv[1])) or not(os.path.isdir(sys.argv[2])):
		print "Use: python "+os.path.basename(sys.argv[0])+" <source_directory> <output_directory> [optional: num_threads, default=4]"
		exit(1)
	
	source_directory = sys.argv[1]
	output_directory = sys.argv[2]
	num_threads 	 = 4
	if len(sys.argv) > 3:
		num_threads	 = sys.argv[3]
	
	input_file_match = '*.sql.gz'
	
	homolog_clusters_to_process = []
	for f_name in os.listdir(source_directory):
		if fnmatch.fnmatch(f_name, input_file_match):
			wild_loc = input_file_match.find('*')
			cluster_family = f_name[wild_loc:-(len(input_file_match) - wild_loc - 1)]
			
			input_file_name = source_directory + "/" + cluster_family
			output_prefix = cluster_family
			
			# If not flagged as already successfully processed, then add it to those to be handled
			if not(os.path.isfile(output_prefix + ".mysql.processing")) and not(os.path.isfile(output_prefix + ".mysql.processed")):
				homolog_clusters_to_process.append((input_file_name, output_prefix))
			
	thread_queue = Queue.Queue()
	for i in range(num_threads):
		t = ProcessingThread(thread_queue)
		t.setDaemon(True)
		t.start()
	 
	for thread_data in homolog_clusters_to_process:
		thread_queue.put(thread_data)
	
	# Wait on the queue until everything has been processed		 
	thread_queue.join()

if __name__ == '__main__':
	#start = time.time()
	main()
	#print "Elapsed Time: %s" % (time.time() - start)

