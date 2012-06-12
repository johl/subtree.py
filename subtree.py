#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
from git import Git, Repo

try:
  shutil.rmtree("Wikibase")
  shutil.rmtree("WikidataClient")
  shutil.rmtree("WikidataRepo")
  shutil.rmtree("WikibaseLib")
except Exception, e:
  pass
Git().clone("https://gerrit.wikimedia.org/r/p/mediawiki/extensions/WikidataClient.git")
Git().clone("https://gerrit.wikimedia.org/r/p/mediawiki/extensions/WikidataRepo.git")
Git().clone("https://gerrit.wikimedia.org/r/p/mediawiki/extensions/WikibaseLib.git")
repo = Repo('WikidataClient')
print str(len(repo.submodules)) + " submodules found. Merging..."
print "Hold on. This may take some time"
for module in repo.submodules:
  Git().clone(module.url, "extensions/" + module.name)
  module_repo = Repo("extensions/" + module.name)
  git = repo.git
  git.merge(module_repo.head, s="ours", no_commit=True)
  git.read_tree("master", prefix=module.name +"/")
  git.commit(m="merging " + module.name + " into extensions/" + module.name)
  print "Merging " + module.name + " into extensions/" + module.name
