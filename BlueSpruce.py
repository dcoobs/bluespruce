#!/usr/bin/python
# 2018 Drew Coobs
# University of Illinois at Urbana-Champaign
#
# Modified version of Shea Craig's 'Spruce-for-Munki' (https://github.com/sheagcraig/Spruce-for-Munki)


import os
import sys
from bluespruce_tools import *

TOP_REPO_PATH = str(sys.argv[1])
IGNORED_FILES = ('.DS_Store',)

def get_manifests():
    manifest_dir = os.path.join(REPO_PATH, "manifests")
    manifests = {}
    for dirpath, dirnames, filenames in os.walk(manifest_dir):
        for dirname in dirnames:
            if dirname.startswith("."):
                dirnames.remove(dirname)

        for filename in filenames:
            if filename not in IGNORED_FILES and not filename.startswith("."):
                manifest_filename = os.path.join(dirpath, filename)
                try:
                    manifests[manifest_filename] = FoundationPlist.readPlist(
                        manifest_filename)
                except FoundationPlist.NSPropertyListSerializationException as err:
                    robo_print("Failed to open manifest '{}' with error "
                               "'{}'.".format(manifest_filename, err.message),
                               LogLevel.WARNING)
    return manifests
    
def get_manifest_items(manifests):
    """Determine all used items.
    First, gets the names of all managed_[un]install, optional_install,
    and managed_update items, including in conditional sections.
    Then looks through those items' pkginfos for 'requires' entries, and
    adds them to the list.
    Finally, it looks through all pkginfos looking for 'update_for'
    items in the used list; if found, that pkginfo's 'name' is added
    to the list.
    """
    collections = ("managed_installs", "managed_uninstalls",
                   "optional_installs", "managed_updates")
    
    for manifest in manifests:
    	used_items = set ()
        for collection in collections:
            items = manifests[manifest].get(collection)
            if items:
				used_items.update(items)
        conditionals = manifests[manifest].get("conditional_items", [])
        for conditional in conditionals:
            for collection in collections:
                items = conditional.get(collection)
                if items:
                    used_items.update(items)
        if used_items:
            print manifest + ":"
            for software in used_items:
                print software
            print ""

for dirpath, dirnames, filenames in os.walk(TOP_REPO_PATH):
    for dirname in dirnames:
        if dirname.startswith("manifests"):
        	#print dirpath
        	REPO_PATH = dirpath
        	REPO_MANIFESTS = get_manifests()
        	get_manifest_items(REPO_MANIFESTS)