# NVDA configHelper.
# Copyright (C) 2022 David CM

import config

def getDictObjFromPath(initObj, path):
	""" this function helps to get a value from nested dictionaries.
	params
	@initObj: the initial object.
	@path: a list with the path to get the final object.
	"""
	for k in path:
		initObj = initObj[k]
	return initObj

def getConfigValue(path, optName, generalProfile=False):
	""" this function helps to accessing config values.
	params
	@path: the path to the option.
	@optName: the option name
	@generalProfile: if true, the general profile will be used, instead of the current profile.
	@returns: the current value, if Exists. Or an exception if the path is not valid.
	"""
	obj = config.conf.profiles[0] if generalProfile else config.conf
	return getDictObjFromPath(obj, path)[optName]


def setConfigValue(path, optName, value, generalProfile=False):
	""" this function helps to accessing and set config values.
	params
	@path: the path to the option.
	@optName: the option name
	@value: the value to set.
	@generalProfile: if true, the general profile will be used, instead of the current profile.
	"""
	obj = config.conf.profiles[0] if generalProfile else config.conf
	getDictObjFromPath(obj, path)[optName] = value


def boolValidator(val):
	if isinstance(val, bool):
		return val
	return eval(val)


def registerGeneralOption(path, option, defaultValue):
	obj = config.conf.profiles[0]
	for k in path:
		if k not in obj:
			obj[k] = {}
		obj = obj[k]
		if (option not in obj):
			obj[option] = defaultValue


def registerConfig(clsSpec, path=None):
	AF = clsSpec(path)
	specObj = getDictObjFromPath(config.conf.spec, AF.__path__[0:-1])
	specObj[AF.__path__[-1]] = AF.__createSpec__()
	# for general profile options
	for k in clsSpec.__getConfigOpts__():
		v = getattr(clsSpec, k)
		if isinstance(v, tuple) and v[1]:
			registerGeneralOption(AF.__path__, k, getattr(AF, k))
	return AF

fakeValidator = lambda x: x
class OptConfig:
	""" just a helper descriptor to create the main class to accesing config values.
	the option name will be taken from the declared variable.
	"""
	def __init__(self, desc):
		"""
		params:
		@desc: the spec description. Can be a string (with the description of configobj) or a tuble with the configobj first, and the second value is a flag that if it's true, the option will be assigned to the default profile only.
		"""
		self.generalProfile = False
		self.validator = fakeValidator
		if isinstance(desc, tuple):
			self.generalProfile = desc[1]
			try:
				self.validator = desc[2]
			except:
				pass
			desc = desc[0]
		self.desc = desc

	def __set_name__(self, owner, name):
		self.name = name

	def __get__(self, obj, type=None):
		if obj:
			try:
				return self.validator(getConfigValue(obj.__path__, self.name, self.generalProfile))
			except KeyError:
				return getConfigValue(obj.__path__, self.name)
		if self.generalProfile:
			return (self.desc, self.generalProfile)
		return self.desc

	def __set__(self, obj, value):
		setConfigValue(obj.__path__, self.name, value, self.generalProfile)


class BaseConfig:
	""" this class will help to get and set config values.
	the idea behind this is to generalize the config path and config names.
	sometimes, a mistake in the dict to access the values can produce an undetectable bug.
	"""
	__path__ = None
	def __init__(self, path=None):
		if not path:
			path = self.__class__.__path__
		if not path:
			raise Exception("Path for the config is not defined")
		if isinstance(path, list):
			self.__path__ = path
		else:
			self.__path__ = [path]

	@classmethod
	def __getConfigOpts__(cls, c=None):
		if c: cls = c
		return [k for k in cls.__dict__ if not k.startswith("__")]

	def __createSpec__(self):
		""" this method creates a config spec with the provided attributes in the class
		"""
		s = {}
		for k in self.__class__.__getConfigOpts__():
			v = getattr(self.__class__, k)
			if isinstance(v, tuple): v = v[0]
			s[k] = v
		return s


def configSpec(pathOrCls):
	""" a decorator to help with the generation of the class config spec.
	adds a get and set descriptor for eatch attribute in the config class.
	except the attributes starting with "__".
	params:
	@pathOrCls: the config path,
	or if the decorator is called without params, then the decorated class.
	path as an argument in the decorator has a higher priority than the __path__ declared in the class.
	"""
	def configDecorator(cls):
		class ConfigSpec(BaseConfig):
			pass
		for k in ConfigSpec.__getConfigOpts__(cls):
			v = getattr(cls, k)
			d = OptConfig(v)
			d.__set_name__(ConfigSpec, k)
			setattr(ConfigSpec, k, d)
		ConfigSpec.__path__ = path
		return ConfigSpec
	if isinstance(pathOrCls, str):
		path = pathOrCls
		return configDecorator
	else:
		path = pathOrCls.__path__
		return configDecorator(pathOrCls)
