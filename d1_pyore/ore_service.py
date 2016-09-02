'''A service to extract PIDs from resource maps stored on disk.

Supports operations:

  /document/<PID>        Returns document given an identifier
  /all/<document>        Returns all aggregated PIDs from a document
  /data/<document>       Returns all targets of CITO:documents from a document
  /metadata/<document>   Returns all targets of CITO:isDocumentedBy

'''

import logging
import argparse





# -- MAIN --
if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="DataONE Diagnostic: Echo Credentials")
  
  parser.add_argument('-v', '--verbose', 
    action='count', 
    default=0,
    help='Set logging level, multiples for more verbose.')
  
  parser.add_argument('-s', '--source',
    default=default_target,
    help="Root folder of resource map documents (cwd)")
   
  args = parser.parse_args()
  
  #Setup logging verbosity
  levels = [logging.WARNING, logging.INFO, logging.DEBUG]
  level = levels[min(len(levels)-1,args.verbose)]
  logging.basicConfig(level=level,
                      format="%(asctime)s %(levelname)s %(message)s")
    