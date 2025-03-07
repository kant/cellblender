import bpy
import os
import subprocess

from cellblender import cellblender_main
#from cellblender import cellblender_operators
#from . import net

filePath = ''



def cleanup(filePath):
    pass


def execute_bionetgen(filepath,context):
    mcell = context.scene.mcell

    print ( " execute_bionetgen with " + os.path.join(os.path.dirname(__file__), "extensions", "bng2", "BNG2.pl") )

    if mcell.cellblender_preferences.bionetgen_location_valid:
      bngpath = mcell.cellblender_preferences.bionetgen_location
      print ("\nBioNetGen exe found: " + bngpath)
      destpath = os.path.dirname(__file__)
      exe_bng = "  ".join([bngpath, "--outdir", destpath, filepath])    # create command string for BNG execution
      print("*** Starting BioNetGen execution ***")
      print("    Command: " + exe_bng )
      #os.system(exe_bng)    # execute BNG
      subprocess.call([bngpath,"--outdir",destpath,filepath])

    elif os.path.exists ( os.path.join ( os.path.dirname(os.path.dirname(__file__)), "extensions", "mcell", "bng2", "BNG2.pl" ) ):
      bngpath =           os.path.join ( os.path.dirname(os.path.dirname(__file__)), "extensions", "mcell", "bng2", "BNG2.pl" )
      print ("\nBioNetGen exe found: " + bngpath)
      destpath = os.path.dirname(__file__)
      exe_bng = "    ".join([bngpath, "--outdir", destpath, filepath])    # create command string for BNG execution
      print("*** Started BioNetGen execution ***")
      #os.system(exe_bng)    # execute BNG
      subprocess.call([bngpath,"--outdir",destpath,filepath])
      return{'FINISHED'}
    
    else:
      print ("\nBioNetGen BNG2.pl not found. Searching ...")

      # Perform the search as done before
      filebasename = os.path.basename(filepath)
      filedirpath = os.path.dirname(filepath)    # dir of the bngl script file
      check_dir = filedirpath;
      n = 0
      while(n!=20):    # iterative search for BNG exe file (starts from the dir containing the bngl script file)
          bng_dir = check_dir  # current dir (+ any unchecked child dir) to be checked 
          checked = {}    # list of dirs for which search is complete
          i = 0
          for (dirpath, dirname, filename) in os.walk(bng_dir):    # Search over the current and previously unchecked child dirs 
              if (i == 0):
                  check_dir = os.path.dirname(dirpath)    #  mark the parent dir for next search (after current and child dirs are done) 
                  i = 1
              if dirpath in checked:  # escape any child dir if already been checked
                  continue
              bngpath = os.path.join(dirpath,"BNG2.pl")    # tentative path for the BNG exe. file
              print ( "Searching for BNG2.pl in " + bngpath )
              if os.path.exists(bngpath):    # if BNG exe.file found, proceed for BNG execution
                  print ("\nBioNetGen exe found: " + bngpath)
                  destpath = os.path.dirname(__file__)
                  exe_bng = "    ".join([bngpath, "--outdir", destpath, filepath])    # create command string for BNG execution
                  print("*** Started BioNetGen execution ***")
                  #os.system(exe_bng)    # execute BNG
                  subprocess.call([bngpath,"--outdir",destpath,filepath])
                  return{'FINISHED'}
              checked.update({dirpath:True})    # store checked directory in the list
          n +=1  
          if (n==20):    # too many iterations; BNG not found, stop further search
              print ("Error running BioNetGen. BNG2.pl not found....")
    return{'FINISHED'}


# We use per module class registration/unregistration
#def register():
#    bpy.utils.register_module(__name__)


#def unregister():
#    bpy.utils.unregister_module(__name__)

