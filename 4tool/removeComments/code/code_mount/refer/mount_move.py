import os


class Mount_move:

    def __init__(self):
        pass

    def Mount_Move(self, imgOri_read, imgFin_read, excel_read, zip_read):
        pass
        try:
            os.system("sudo mount /dev/sda1 /mnt/mydev")
        except:
            pass
        else:
            pass

        path = imgOri_read.split("/")
        time = path[len(path) - 2]

        if not os.path.exists("/mnt/mydev/%s" % time):
            try:
                os.system("sudo mkdir /mnt/mydev/%s" % time)
                pass
            except Exception as e:
                pass
                return False
        else:
            pass

        save_path = "/mnt/mydev/%s" % time
        save_ori = "/mnt/mydev"

        if not os.path.exists("/mnt/mydev/test.zip"):
            try:
                os.system("sudo cp %s %s" % (zip_read, save_ori))
                pass
            except Exception as e:
                pass
            except:
                return False
        else:
            pass

        try:
            os.system("sudo cp %s %s" % (imgOri_read, save_path))
            os.system("sudo cp %s %s" % (imgFin_read, save_path))
            os.system("sudo cp %s %s" % (excel_read, save_path))
            pass
        except Exception as e:
            pass
        except:
            return False

        try:
            os.system("sudo umount /mnt/mydev")
        except Exception as e:
            pass
            return False

        pass

        return True


if __name__ == '__main__':
    mMove = Mount_move()

    imgOri = "/home/orangepi/Desktop/qt0922/img/2024-01-30/2024_01_30_09_28_45-1.jpeg"  
    imgFin = "/home/orangepi/Desktop/qt0922/img/2024-01-30/2024_01_30_09_28_45-2.jpeg"  
    excel_read = "/home/orangepi/Desktop/qt0922/img/2024-01-30/2024-01-30.xlsx"  
    zip_read = "/home/orangepi/Desktop/qt0922/res/test.zip"  

    flag = mMove.Mount_Move(imgOri, imgFin, excel_read, zip_read)

    pass
