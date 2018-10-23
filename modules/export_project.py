import os, datetime, zipfile
from datetime import date
from os import path

def export(config):
	MODULE_PATH = os.path.join(os.path.dirname(__file__))

	print("\n========================");
	print("EXPORTING PROJECT INTO ARCHIVE")
	print("\n")

	project_folder = config["project"]["path"]

	if (not (os.path.isdir(project_folder))):
		print("	ERROR: Invalid Project folder.")
		return False

	db_name = config["db"]["name"]
	db_user = config["db"]["user"]
	db_pass = config["db"]["password"]
	db_dump = config["db"]["file"]

	try:
		if (os.system(f"mysqldump --user={db_user} --password={db_pass} {db_name} > {db_dump}") > 0):
			raise
	except Exception:
		print("	ERROR: Failed to connect to the database.");
		print("\nABORTED.\n")
		return False

	print("	OK: Database exported.");

	zip_name = config["project"]["zip"]
	included_folders = config["project"]["folders"]
	excluded_folders = config["project"]["excluded_folders"]
	root_files = config["project"]["root_files"]

	date_format = date.today().strftime('%d %m %Y')
	zip_name = zip_name + " - " + date_format
	zip_name_final = (zip_name + ".backup.zip")

	try:
		zf = zipfile.ZipFile(zip_name_final, "w")
	except Exception as err:
		print("	ERROR: Failed to create archive:", err)
		print("\nABORTED.\n")
		return False

	try:
		zf.write(db_dump)
		os.remove(db_dump)
	except Exception as err:
		print("	ERROR:", err)
		print("\nABORTED.\n")
		return False

	starting_dir = os.getcwd()
	os.chdir(project_folder)

	try:
		for file in root_files:
			zf.write(file)

		for folder in included_folders:
			for dirname, dirs, files in os.walk(folder, topdown = True):
				dirs[:] = [d for d in dirs if d not in excluded_folders]
				zf.write(dirname)
				for filename in files:
					zf.write(os.path.join(dirname, filename))
		zf.close()
	except Exception as err:
		print("	ERROR:", err)
		print("\nABORTED.\n")
		return False

	print("	SUCCESS: Project added to the archive (" + zip_name_final + ").");

	os.chdir(starting_dir)

	return zip_name_final