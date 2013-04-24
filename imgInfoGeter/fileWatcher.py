# -*- coding:gbk -*-
# auther : pdm
# email : ppppdm@gmail.com

import threading
import os


# using Polling , can work across platform




# if operation system is windows
# Use the FindFirstChangeNotification API
# src from http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html

def watchFileChange_2(path_to_watch, func_handle_change = None):
    import win32file
    import win32event
    import win32con
    
    #path_to_watch = os.path.abspath (".")
    
    #
    # FindFirstChangeNotification sets up a handle for watching
    #  file changes. The first parameter is the path to be
    #  watched; the second is a boolean indicating whether the
    #  directories underneath the one specified are to be watched;
    #  the third is a list of flags as to what kind of changes to
    #  watch for. We're just looking at file additions / deletions.
    #
    change_handle = win32file.FindFirstChangeNotification (
      path_to_watch,
      0,
      win32con.FILE_NOTIFY_CHANGE_FILE_NAME
    )
    
    #
    # Loop forever, listing any file changes. The WaitFor... will
    #  time out every half a second allowing for keyboard interrupts
    #  to terminate the loop.
    #
    try:
    
      old_path_contents = dict ([(f, None) for f in os.listdir (path_to_watch)])
      while 1:
        result = win32event.WaitForSingleObject (change_handle, 500)
    
        #
        # If the WaitFor... returned because of a notification (as
        #  opposed to timing out or some error) then look for the
        #  changes in the directory contents.
        #
        if result == win32con.WAIT_OBJECT_0:
          new_path_contents = dict ([(f, None) for f in os.listdir (path_to_watch)])
          added = [f for f in new_path_contents if not f in old_path_contents]
          deleted = [f for f in old_path_contents if not f in new_path_contents]
          if added:
              changes = []
              for i in added:
                changes.append((3, os.path.join(path_to_watch, i)))
                print("Added: ", ", ".join (added))
              t = threading.Thread(target=func_handle_change, args = (changes, ))
              t.start()
          if deleted: 
              print("Deleted: ", ", ".join (deleted))
    
          old_path_contents = new_path_contents
          win32file.FindNextChangeNotification (change_handle)
    
    finally:
      win32file.FindCloseChangeNotification (change_handle)


# Use the ReadDirectoryChanges API
# src from http://timgolden.me.uk/python/win32_how_do_i/watch_directory_for_changes.html


def watchFileChange(path_to_watch, func_handle_change = None):
    import win32file
    import win32con
    
    ACTIONS = {
               1 : "Created",
               2 : "Deleted",
               3 : "Updated",
               4 : "Renamed from something",
               5 : "Renamed to something"
               }
    
    # Thanks to Claudio Grondi for the correct set of numbers
    FILE_LIST_DIRECTORY = 0x0001
    
    #path_to_watch = "."
    hDir = win32file.CreateFile (
        path_to_watch,
        FILE_LIST_DIRECTORY,
        win32con.FILE_SHARE_READ | win32con.FILE_SHARE_WRITE | win32con.FILE_SHARE_DELETE,
        None,
        win32con.OPEN_EXISTING,
        win32con.FILE_FLAG_BACKUP_SEMANTICS,
        None
        )
    
    while 1:
        #
        # ReadDirectoryChangesW takes a previously-created
        # handle to a directory, a buffer size for results,
        # a flag to indicate whether to watch subtrees and
        # a filter of what changes to notify.
        #
        # NB Tim Juchcinski reports that he needed to up
        # the buffer size to be sure of picking up all
        # events when a large number of files were
        # deleted at once.
        #
        results = win32file.ReadDirectoryChangesW (
                                                   hDir,
                                                   1024,
                                                   True,
                                                   win32con.FILE_NOTIFY_CHANGE_FILE_NAME |
                                                   win32con.FILE_NOTIFY_CHANGE_DIR_NAME |
                                                   win32con.FILE_NOTIFY_CHANGE_ATTRIBUTES |
                                                   win32con.FILE_NOTIFY_CHANGE_SIZE |
                                                   win32con.FILE_NOTIFY_CHANGE_LAST_WRITE |
                                                   win32con.FILE_NOTIFY_CHANGE_SECURITY,
                                                   None,
                                                   None
                                                   )
        changes = []
        for action, file in results:
            full_filename = os.path.join (path_to_watch, file)
            print(full_filename, ACTIONS.get (action, "Unknown"))
            changes.append((action, full_filename))
        
        if func_handle_change:
            # if needed create a thread to handle results
            t = threading.Thread(target=func_handle_change, args = (changes, ))
            t.start()
            
    

if __name__=='__main__':
    print(__file__, 'test')
    import sys
    import InfoProcess
    
    def handle_change(changes):
        print(changes)
        for action, file in changes:
            print(action, file)
            if action == 3 and 'jpg' in file:
                print(file)
                InfoProcess.file_process(file)
    
    if sys.argv[1]:
        DIRECTORY_PATH = sys.argv[1]
    else:
        DIRECTORY_PATH = '.'
    watchFileChange_2(DIRECTORY_PATH, handle_change)
