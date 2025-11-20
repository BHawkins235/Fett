import typer
from typing_extensions import Annotated
import math
import os
from datetime import datetime
from PIL import Image, ExifTags
from PIL.ExifTags import GPSTAGS
import subprocess
import json
'''
Meta data bounty hunter(get it becasue Boba Fett....)
	Can get metadata from:
		files
		images 


	$ Get-ItemProperty [Filepath]	| format-list


'''

app = typer.Typer()




#change python version 
@app.command()
def image(path: str):


	try:
	    image = Image.open(path)
	    exif_data = image._getexif()


	    if exif_data:
	        # Loop through all EXIF tags and print their names and values
	        for tag_id, value in exif_data.items():
	            tag_name = ExifTags.TAGS.get(tag_id, tag_id)
	            print(f"{tag_name}: {value}")

	        # Access specific tags, e.g., DateTimeOriginal
	        date_taken = exif_data.get(ExifTags.TAGS["DateTimeOriginal"])
	        if date_taken:
	            print(f"Date Taken: {date_taken}")

	        # Access GPS information (if present)
	        gps_info = exif_data.get_ifd(ExifTags.GPSInfo)

	        if gps_info:
	            print("GPS Information:")
	            for gps_tag_id, gps_value in gps_info.items():
	                gps_tag_name = ExifTags.GPSTAGS.get(gps_tag_id, gps_tag_id)
	                print(f"  {gps_tag_name}: {gps_value}")
	    else:
	        print("No EXIF data found in the image.")

	except FileNotFoundError:
	    print("Image file not found.")
	except Exception as e:
	    print(f"An error occurred: {e}")
#add in a way to get the owner from metadata 
@app.command()

def file(path: str):

	powershell_command = f"Get-ItemProperty {path} | format-list"

	if os.path.exists(path):
		try:
		    result = subprocess.run(
		        ["powershell", "-Command", powershell_command],
		        capture_output=True,
		        text=True,
		        check=True
		    )
		    print("PowerShell command executed successfully:")
		    print(result.stdout)
		except subprocess.CalledProcessError as e:
		    print(f"Error executing PowerShell command: {e}")
		
		except FileNotFoundError:
		    print("PowerShell executable not found. Ensure PowerShell is installed and in your system's PATH.")
	else:
		print("This file path does not exist")




	'''try:
					stats = os.stat(path)
			
					uid = stats.st_uid
					print(uid)
					
					
					print(f"File Size: {stats.st_size} bytes")
					print(f"Creation Date: {datetime.fromtimestamp(stats.st_ctime)}")
					print(f"Modification Date: {datetime.fromtimestamp(stats.st_mtime)}")
					print(f"Last Access Date: {datetime.fromtimestamp(stats.st_atime)}")
					
					#implement a way to get the user id and data 
					print(f"This is the user info")
			
				except FileNotFoundError:
					print("File at cannot be found")'''




if __name__ == "__main__":
	app()

