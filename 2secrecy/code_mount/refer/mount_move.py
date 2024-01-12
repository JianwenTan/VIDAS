# encoding: utf-8
import os


class Mount_move:

    def __init__(self):
        pass

    def Mount_Move(self, imgOri_read, imgFin_read, excel_read, zip_read):
        print("挂载正在执行！")
        try:
            os.system("sudo mount /dev/sda1 /mnt/mydev")
        except:
            print("**挂载错误：")
        else:
            print("挂号在测")

        path = imgOri_read.split("/")
        time = path[len(path) - 2]

        if not os.path.exists("/mnt/mydev/%s" % time):
            try:
                os.system("sudo mkdir /mnt/mydev/%s" % time)
                print("/mnt/mydev/%s创建成功" % time)
            except Exception as e:
                print("**文件创建错误：", e)
                return False
        else:
            print("/mnt/mydev/%s已经存在" % time)

        save_path = "/mnt/mydev/%s" % time
        save_ori = "/mnt/mydev"

        if not os.path.exists("/mnt/mydev/test.zip"):
            try:
                os.system("sudo cp %s %s" % (zip_read, save_ori))
                print("/mnt/mydev/test.zip复制成功！")
            except Exception as e:
                print("**软件复制错误：", e)
            except:
                return False
        else:
            print("/mnt/mydev/test.zip已经存在")

        try:
            os.system("sudo cp %s %s" % (imgOri_read, save_path))
            os.system("sudo cp %s %s" % (imgFin_read, save_path))
            os.system("sudo cp %s %s" % (excel_read, save_path))
            print("表格和图像复制成功！")
        except Exception as e:
            print("**复制错误：", e)
        except:
            return False

        try:
            os.system("sudo umount /mnt/mydev")
        except Exception as e:
            print("**取消挂在错误：", e)
            return False

        print("挂载执行结束！")

        return True


if __name__ == '__main__':
    mMove = Mount_move()

    imgOri = "/home/orangepi/Desktop/qt0922/img/2024-01-30/2024_01_30_09_28_45-1.jpeg"  # 原图
    imgFin = "/home/orangepi/Desktop/qt0922/img/2024-01-30/2024_01_30_09_28_45-2.jpeg"  # 检测图
    excel_read = "/home/orangepi/Desktop/qt0922/img/2024-01-30/2024-01-30.xlsx"  # 表格
    zip_read = "/home/orangepi/Desktop/qt0922/res/test.zip"  # 压缩包

    flag = mMove.Mount_Move(imgOri, imgFin, excel_read, zip_read)

    #   True表示成功，False表示失败
    print("操作标志：", flag)
