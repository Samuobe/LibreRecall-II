import os
from PIL import Image
from datetime import datetime
import pytesseract
import glob

user_path = os.path.expanduser("~")+"/"
data_path = user_path+".local/share/LibreRecall"
config_path = user_path+ ".config/LibreRecall"

working_path = "/usr/bin/LibreRecall"


if not os.path.isfile(config_path+"/time.conf"):
    with open(config_path+"/time.conf", "w") as f:
        f.write("30")
if not os.path.isfile(f"{config_path}/max_screens.conf"):
    with open(f"{config_path}/max_screens.conf", "w") as f:
        f.write("1000")


while True:
    with open(f"{config_path}/time.conf") as f:
        data = f.readlines()
    time_sleep = data[0]


    with open(f"{config_path}/max_screens.conf") as f:
        data = f.readlines()

    max_screens = int(data[0])

    user_path = os.path.expanduser("~")+"/"
    data_path = user_path+".local/share/LibreRecall"
    images_dir = data_path+"/images"


    os.system("flameshot full -p {}/NEW.png".format(images_dir))

    date_raw = datetime.now()

    date, time = str(date_raw).split(" ")
    time = time.split(".")[0]

    new_name = date+"_"+time

    image_data = pytesseract.image_to_string(Image.open('{}/NEW.png'.format(images_dir)))

    with open(images_dir+"/"+new_name+".txt", "w") as f:
        f.write(image_data)

    os.system(f"mv {images_dir}/NEW.png {images_dir}/{new_name}.png")

    image_list = glob.glob(f"{images_dir}/*.png")


    try:
        max_screens = max_screens + 1
        os.remove(f"{image_list[-max_screens]}") 
        txt_name = os.path.basename(image_list[-max_screens]).replace(".png", ".txt")
        txt_file = os.path.join(images_dir, txt_name)
        os.remove(txt_file)
    except:
        pass
    

    os.system("sleep {}".format(time_sleep))