

import os
import cv2


#根据输入的文件夹绝对路径，将该文件夹下的所有指定suffix的文件读取存入一个list,该list的第一个元素是该文件夹的名字
def readAllImg(path,*suffix):
    try:

        s = os.listdir(path)
        resultArray = []
        fileName = os.path.basename(path)
        resultArray.append(fileName)
        flag=0
        for i in s:
            if endwith(i, suffix):
                document = os.path.join(path, i)
                img = cv2.imread(document)
                resultArray.append(img)
                flag=flag+1

    except IOError:
        print ("Error")

    else:
        print ("读取成功")
        return resultArray

#输入一个字符串一个标签，对这个字符串的后续和标签进行匹配
def endwith(s,*endstring):
   resultArray = map(s.endswith,endstring)
   if True in resultArray:
       return True
   else:
       return False

if __name__ == '__main__':

  result = readAllImg("/home/hq/桌面/cat_dog/c-d-data/train1/cats",'.jpg')
  print (result[0])
  # cv2.namedWindow("Image")
  # cv2.imshow("Image", result[1])
  # cv2.waitKey(0)
  # cv2.destroyAllWindows()
