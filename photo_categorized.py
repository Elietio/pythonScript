import shutil
import os
import time
import exifread


class ReadFailException(Exception):
    pass


img_ext = ['jpg', 'png', 'jpeg', 'gif', 'bmp', 'raw']


def get_date_dir(fullname, md):
    try:
        fd = open(fullname, 'rb')
    except:
        raise ReadFailException("unopen file[%s]\n" % fullname)
    data = exifread.process_file(fd)
    if data:
        try:
            t = data['EXIF DateTimeOriginal']
            return str(t).replace(":", "-")[:10] if md == 'd' else str(t).replace(":", "-")[:7]
        except:
            pass
    # 如果无法读取到exif信息，则使用文件系统信息的时间
    state = os.stat(fullname)
    return time.strftime("%Y-%m-%d", time.localtime(state[-2])) if md == 'd' else time.strftime("%Y-%m", time.localtime(
        state[-2]))


def classify_pictures(srcdir, tardir, subdir, md):
    for root, dirs, files in os.walk(srcdir, True):
        for photoname in files:
            fullname = os.path.join(root, photoname)
            print("classify %s" % photoname)
            ext = os.path.splitext(fullname)[-1][1:]
            if ext.lower() not in img_ext:
                print("%s not image" % photoname)
                continue
            dir = get_date_dir(fullname, md)
            print("photo time %s" % dir)
            if subdir:
                dir = dir + '\\' + ext
            pwd = tardir + '\\' + dir
            dst = pwd + '\\' + photoname
            if fullname == dst:
                continue
            if not os.path.exists(pwd):
                os.makedirs(pwd)
            shutil.copy(fullname, dst)
            # os.remove(fullname)


def photo_categorized():
    srcdir = input('请输入需要操作的目录(Enter默认当前):')
    if len(srcdir) < 1:
        srcdir = os.getcwd()
    if os.path.isdir(srcdir):
        print(srcdir)
    else:
        print("not a directory")
        return
    tardir = input('请输入保存的目录(Enter默认当前):')
    if len(tardir) < 1:
        tardir = os.getcwd()
    if os.path.isdir(tardir):
        print(tardir)
    else:
        print("not a directory")
        return
    yn = input('是否按文件类型归类子目录(y/n):')
    if yn in ['y', 'Y']:
        subdir = True
    elif yn in ['n', 'N']:
        subdir = False
    else:
        print('input wrong!')
        return
    md = input('按月或天归类(m/d):')
    if md in ['m', 'M']:
        md = 'm'
    elif md in ['d', 'D']:
        md = 'd'
    else:
        print('input wrong!')
        return
    classify_pictures(srcdir, tardir, subdir, md)


if __name__ == '__main__':
    photo_categorized()
