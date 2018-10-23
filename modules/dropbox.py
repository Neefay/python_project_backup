import os, dropbox, humanize

def upload(file_path, config):
	MODULE_PATH = os.path.join(os.path.dirname(__file__))

	print("\n========================");
	print("UPLOADING ARCHIVE TO DROPBOX")
	print("\n")

	if (not (os.path.exists(file_path))):
		print("	ERROR: Project archive does not exist.")
		return False

	dropbox_token = config["dropbox"]["token"]
	dest_folders = ["Backups", "Belligerence"]

	dest_folders_joined = ("/" + ("/".join(dest_folders)) + "/")
	final_dest_path = (dest_folders_joined + file_path)

	file_size = os.path.getsize(file_path)
	CHUNK_SIZE = (2*1024*1024)

	print("	ATTEMPT: Uploading file:", file_path, "(" + humanize.naturalsize(file_size) + ")")
	print("	         Dropbox folder:", final_dest_path)

	try:
		with open(file_path, "rb") as f:

			dbx = dropbox.Dropbox(dropbox_token, timeout = 999999)

			if (file_size <= CHUNK_SIZE):
				print(dbx.files_upload(f.read(CHUNK_SIZE), final_dest_path))

			else:
				print("	ATTEMPT: Initializing upload session...");
				upload_session_start_result = dbx.files_upload_session_start(f.read(CHUNK_SIZE))
				cursor = dropbox.files.UploadSessionCursor(session_id = upload_session_start_result.session_id, offset = f.tell())
				commit = dropbox.files.CommitInfo(path = final_dest_path)

				while (f.tell() < file_size):
					upload_progress = ((file_size * f.tell()) / 100)
					print("	UPLOAD PROGRESS: [", str(upload_progress)[:2] + "%", "]")

					if ((file_size - f.tell()) <= CHUNK_SIZE):
					 	print(dbx.files_upload_session_finish(f.read(CHUNK_SIZE), cursor, commit))

					else:
						dbx.files_upload_session_append(f.read(CHUNK_SIZE), cursor.session_id, cursor.offset)
						cursor.offset = f.tell()
			f.close()
			print("	SUCCESS: The project archive was successfully uploaded.")
			return True

	except Exception as err:
		print("ERROR: Failed to upload - ", err)
		return False