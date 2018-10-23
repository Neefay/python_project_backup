from modules.export_project import export
from modules.dropbox import upload
from modules.helpers import read_json

print("+++++++++++++++++++++++++++");
print("BELLIGERENCE BACKUP ROUTINE")
print("+++++++++++++++++++++++++++");

config = read_json("config.json")

if (config):
	print("	OK: Configuration file read.");

archive = export(config)

if archive:
	if upload(archive, config):
		print("\n")
		print("END: The project was sucessfully backed up.")
		print("===========================================\n");
		input("Press any key to continue...")