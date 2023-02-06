# import module
import subprocess

# traverse the info
Id = subprocess.check_output(['systeminfo']).decode('utf-8').split('\n')
new = []

# arrange the string into clear info
for item in Id:
	new.append(str(item.split("\r")[:-1]))
for i in new:
    with open('SystemInfo.txt','a') as f:
        f.writelines(i[2:-2])
print("DONE SAVED as SystemInfo.txt ")