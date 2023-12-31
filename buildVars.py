# -*- coding: UTF-8 -*-

# Build customizations
# Change this file instead of sconstruct or manifest files, whenever possible.

# Full getext (please don't change)
_ = lambda x : x

# Add-on information variables
addon_info = {
	# for previously unpublished addons, please follow the community guidelines at:
	# https://bitbucket.org/nvdaaddonteam/todo/raw/master/guideLines.txt
	# add-on Name, internal for nvda
	"addon_name" : "IBMTTS",
	# Add-on summary, usually the user visible name of the addon.
	# Translators: Summary for this add-on to be shown on installation and add-on information.
	"addon_summary" : _("IBMTTS driver"),
	# Add-on description
	# Translators: Long description to be shown for this add-on on add-on information from add-ons manager
	"addon_description" : _("""This is the IBMTTS synthesizer driver for NVDA."""),
	# version
	"addon_version" : "23.12.1",
	# Author(s)
	"addon_author" : u"David CM <dhf360@gmail.com>, x0 and others",
	# URL for the add-on documentation support
	"addon_url" : "https://github.com/davidacm/NVDA-IBMTTS-Driver",
	# Documentation file name
	"addon_docFileName" : "readme.html",
	# Minimum NVDA version supported (e.g. "2018.3.0")
	"addon_minimumNVDAVersion" : "2019.3.0",
	# Last NVDA version supported/tested (e.g. "2018.4.0", ideally more recent than minimum version)
	"addon_lastTestedNVDAVersion" : "2024.2.0",
	# Add-on update channel (default is stable or None)
	"addon_updateChannel" : None,
	# Add-on license such as GPL 2
	"addon_license": "GPL 2",
	# URL for the license document the ad-on is licensed under
	"addon_licenseURL": "https://www.gnu.org/licenses/old-licenses/gpl-2.0.html",
	# URL for the add-on repository where the source code can be found
	"addon_sourceURL": "https://github.com/davidacm/NVDA-IBMTTS-Driver",
}


from os import path

# Define the python files that are the sources of your add-on.
# You can use glob expressions here, they will be expanded.
pythonSources = [path.join("addon", "synthDrivers", "*.py"),
	path.join("addon", "globalPlugins", "*.py"),
	path.join('addon', 'installTasks.py')]

# Files that contain strings for translation. Usually your python sources
i18nSources = pythonSources + ["buildVars.py"]
pythonSources.append(path.join("addon", "synthDrivers", "ibmtts", "*.*"))

# Files that will be ignored when building the nvda-addon file
# Paths are relative to the addon directory, not to the root directory of your addon sources.
excludedFiles = []


# Base language for the NVDA add-on
baseLanguage = "en"

# Markdown extensions for add-on documentation
# Most add-ons do not require additional Markdown extensions.
# If you need to add support for markup such as tables, fill out the below list.
# Extensions string must be of the form "markdown.extensions.extensionName"
# e.g. "markdown.extensions.tables" to add tables.
markdownExtensions = []
