import os
def handle_uploaded_file(file_path,uniquefilename):
    PROJECT_PATH = os.path.realpath(os.path.dirname(__file__))
    
    #file_path =  os.path.join(file_path, "/pictures")
    
    print "handle_uploaded_file"
    dest = open("pictures/"+ uniquepathname+"enduniquename"+file_path.name ,"wb")
    for chunk in file_path.chunks():
        dest.write(chunk)
    dest.close()