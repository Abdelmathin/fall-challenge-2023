import os

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def find(dirname, res = None):
	if not res:
		res = {}
	try:
		for basename in os.listdir(dirname):

			if basename in [".git", ".", ".."]:
				continue
			filename = os.path.realpath(dirname + '/' + basename)
			if not (find(filename, res)):
				res[filename] = basename
	except:
		return ({})
	return (res)


for filename in find(ROOT_DIR):
	if ("__pycache__" in filename):
		pycache = filename.split("__pycache__")[0] + "__pycache__"
		try:
			os.system('rm -rf "' + pycache + '"')
		except:
			pass

langfiles = {
	"Java"   : os.listdir(ROOT_DIR + "/sources/Java"),
	"Python" : ["constants.py", "entities.py", "utils.py", "drone.py", "seabed_security.py", "main.py"]
}

def getext(lang):
	lang = lang.lower()
	return ({"python" : "py"}.get(lang, lang))

def get_line_comment(lang):
	lang = lang.lower()
	return ({"python" : "#"}.get(lang, "//"))

def normContent(content, lang_options):
	content = content
	for start, end in [["'''", "'''"], ["/*", "*/"]]:
		while (True):
			if start in content:
				comment = content[content.index(start) + len(start):]
				if end in comment:
					comment = start + comment[:comment.index(end)] + end
					content = content.replace(comment, "")
					continue
			break
	_new_content = ""
	for line in content.split("\n"):
		_line     = line.strip()
		_continue = False
		if not _line or _line.startswith("#") or _line.startswith("//"):
			line = "\n"
		if (_line.startswith("package com.")):
			line = "\n"
		for file in lang_options["files"]:
			import_line = ("from " + file.split(".")[0] + " import")
			if (_line.startswith(import_line)):
				line = "\n"
		if (_line.startswith("import ") or _line.startswith("from ")):
			lang_options["imports"] = lang_options["imports"] + line + "\n"
			line = "\n"
		_new_content += line + "\n"
	return (_new_content)

def trimAll(content):
	while ("\n\n" in content):
		content = content.replace("\n\n", "\n")
	content = content.replace("class Player", "class <<Pla-yer>>")
	content = content.replace("GamePlayer", "Player")
	content = content.replace("Player", "GamePlayer")
	content = content.replace("class <<Pla-yer>>", "class Player")
	return (content.strip())

for lang, files in langfiles.items():
	lang_ext     = getext(lang)
	answer_file  = ROOT_DIR + "/Answer/Answer." + lang_ext
	lang_options = {"imports" : "", "lang" : lang, "files" : files}
	with open(answer_file, "w") as fp:
		for basename in files:
			filename = ROOT_DIR + "/sources/" + lang + "/" + basename
			if not filename.endswith(".py") and (not filename.endswith(".java")):
				continue
			content = normContent(open(filename).read(), lang_options)
			fp.write(content + "\n")

	old_content = open(answer_file).read()
	new_content = lang_options["imports"] + "\n" + old_content
	with open(answer_file, "w") as fp:
		fp.write(trimAll(new_content))
