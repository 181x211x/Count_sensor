import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import os

pushB = 0 # if the button B was pushed, pushB = 1
SeatSum = 6
middleY = 120
maxValue =0
comeIn = 0
goOut = 0

ResultImg = np.zeros((240,320,3),np.uint8)
ResultImg[:,:]= (255,255,255)

#pushB = 0 # if the button B was pushed, pushB = 1
Total = 0 # total number of people in the room

#define kernel for the dilation
bkernel = np.ones((3,3),np.uint8)


#カメラ映像の準備
cap = cv2.VideoCapture(0)

kernel = np.ones((5,5),np.uint8)


# define the center Y axis for 5 people
centerY = [[np.nan] for j in range(5)]
#print(centerY)

# define array oftime variable
frame = np.array([])
frame = np.append(frame,0)
#print(time)
t=0


# define array of total number of people
total = np.array([])
total = np.append(total,0)
#print(total)


# define array of the surface of object1
obj_surface = np.array([])
obj_surface = np.append(obj_surface,0)

# define detected object number
objNum=0

# define last surface
prev_surface = [500 for j in range(5)]

# value of one contour: if 2 people exist in one contour, value = 2
value = [1 for j in range(5)]

# define person[previons_state][current_state]
# state = 0: is inside
# state = 1: is outside
person = [[-1 for i in range(2)] for j in range(5)]

mx = [0 for j in range(5)]
my = [0 for j in range(5)]
prev_my = [0 for j in range(5)]

p_mx = [0 for j in range(5)]
p_my = [0 for j in range(5)]

Area = [0 for j in range(5)]
max_area = 0
old_max_area = 0

font = cv2.FONT_HERSHEY_DUPLEX
font2 = cv2.FONT_HERSHEY_TRIPLEX

time_before = time.time()


person_list2 = []
old_person_list2 = []



crash = []


n =0
#フレームの個数
s = 0
#比較回数
count = 0

min_id = 0

dist2 = []


first_id = 0
second_id = 0
third_id = 100

first_id2 = 0
second_id2 = 0
third_id2 = 0

crash1 = 0
crash2 = 0

tweet_frag = 0

crash_frag = 0





while True:
        # read one frame
    ret, frame1 = cap.read()
    petit1 = cv2.resize(frame1,(320,240))

    gray1 = cv2.cvtColor(petit1,cv2.COLOR_BGR2GRAY)

    cv2.imshow('camera capture',petit1)
    cv2.moveWindow('camera capture',20,55)


    k = cv2.waitKey(10)

    if k == 98:
                ret, frame2 = cap.read()
                petit2 = cv2.resize(frame2,(320,240))
                gray2 = cv2.cvtColor(petit2,cv2.COLOR_BGR2GRAY)
                height, width, channels = frame2.shape
                pushB +=1
                startTime = time.time()

    if pushB == 1:


                cv2.imshow('Detection Result',ResultImg)
                cv2.moveWindow('Detection Result',360,340)

                #背景差分をして動的物体を追跡する
                diffimg = cv2.absdiff(gray1,gray2)


                #cv2.imshow('Sabun',diffimg)
                ret, thresh = cv2.threshold(diffimg,60,255,cv2.THRESH_BINARY)

                #cv2.imshow('Thresh',thresh)
                #膨張処理をしてノイズを消す
                dilation = cv2.dilate(thresh,kernel,iterations = 1)

                cv2.imshow('Different image',dilation)
                cv2.moveWindow('Different image',20,340)

                img,contours, hierarchy = cv2.findContours(dilation,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

                person_list2 = []



                id = 0

                t +=1

                #前フレーム中にある輪郭の個数
                sum = s

                s = 0




                #print "t: " +str(t)
                frame = np.append(frame,t)

                total = np.append(total,Total)

                for j in range(5):
                    centerY[j].append(np.nan)
                #print(centerY[0])

                obj_surface = np.append(obj_surface,np.nan)
                cv2.line(petit1,(0,120),(319,120),(0,0,255),2)

                tb = time.time()
                for cnt in contours:
                    if cv2.contourArea(cnt) > 4000:


                        Area[id] = cv2.contourArea(cnt)



                        M = cv2.moments(cnt)
                        mx[id] = int(M['m10']/M['m00'])
                        my[id] = int(M['m01']/M['m00'])

                        #現フレームの人間リスト[id.x.y.面積]

                        person_list2.append([[id],mx[id],my[id],Area[id]])

                        #test.append([[id],mx[id],my[id],Area[id]])
                        #print("test",test)
                        t#est[id][0].append(100)
                        #print("test",test)
                        #print("test_len",len(test[id][0]))


                        s += 1

                        #比較回数
                        count = 0

                        #前フレームとの現フレームとのそれぞれの距離
                        a = np.array([mx[id], my[id]])




                        if len(old_person_list2) != 0:





                         #連続的物体追跡アルゴリズム
                         #前フレームそれぞれの距離を計算する
                         for p_id in range(sum):

                            b = np.array([old_person_list2[p_id][1], old_person_list2[p_id][2]])
                            u = b - a
                            dist = np.linalg.norm(u)
                            #print("dist",dist)

                            #距離が近い場合、前フレームのID番号入れる
                            if dist < 30:
                              person_list2[id][0] = old_person_list2[p_id][0]
                              count = 0


                            #新しい物体が存在した時,最小IDを入れる
                            if dist > 30:
                              count += 1
                              if count == sum:
                                 print("---------------新しい物体が見つかりました------------------")


                                 min_id = 0

                                 for x in range(sum):

                                  #前フレームで使われてな最小のID番号を代入する.
                                  #前フレームで衝突物体がない場合
                                  if len(old_person_list2[x][0]) == 1:
                                  	if old_person_list2[x][0][0] == min_id:
                                  		min_id += 1


                                  #衝突物体がある時
                                  elif len(old_person_list2[x][0]) >= 2:

                                  	sort_old_person2 = sorted(old_person_list2[x][0])

                                  	for y in range(len(old_person_list2[x][0])):

                                  		if sort_old_person2[y] == min_id:
                                  			min_id +=1






                                 person_list2[id][0][0] = min_id







                        obj_surface[-1] = cv2.contourArea(cnt)



                        #print "prev_s: "+str(prev_surface)+"current_s: " +str(cv2.contourArea(cnt))
                        prev_surface[id] = cv2.contourArea(cnt)
                        prev_my[id] = person_list2[id][2]

                        # find the rectangle realise the smallest serface
                        rect = cv2.minAreaRect(cnt)
                        box = cv2.boxPoints(rect)
                        box = np.int0(box)



                        # default: decide the start situation
                        if person[id][0] < 0 and person[id][1] < 0:
                            if my[id] <= 120:
                                person[id][0]= 1
                            else :
                                person[id][0]= 0
                            #print "a: " +str(id)+ " prev: " +str(person[id][0])+ "now: "+str(person[id][1])

                        #take the current situation
                        if my[id] <= 120:
                            person[id][1] = 1
                        else :
                            person[id][1] = 0
                        #print "b: "+str(id)+ " prev: " +str(person[id][0])+ " now: "+str(person[id][1])

                        cv2.drawContours(petit1,[box],0,(255,0,0),2)
                        cv2.circle(petit1,(mx[id],my[id]),3,(0,255,0),-1)




                        #if person's state changed in the prev and current situation
                        if  person[id][0] != person[id][1]:
                            if person[id][0] == 1 :
                                print ("-----------------one person goes out-----------------------")
                                #cv2.drawContours(petit1,[box],0,(0,0,255),2)
                                cv2.line(petit1,(0,120),(319,120),(0,255,0),2)
                                person[id][0] = 0
                                person[id][1] = -1
                                Total -=1
                                goOut += 1
                                tweet_frag = -1
                                #print str(Total)
                            else :
                                print ("-------------------one person comes in!----------------------------")
                                #cv2.drawContours(petit1,[box],0,(0,0,255),2)
                                cv2.line(petit1,(0,120),(319,120),(0,255,0),2)
                                person[id][0] = 1
                                person[id][1] = -1
                                Total +=1
                                comeIn +=1
                                tweet_frag = 1
                                #print str(Total)











                        #print str(id)
                        if id == 1:
                            objNum = 1

                        if id == 2:
                            objNum = 2

                        id +=1



                #----------------------------------------ここまでがidで回してる場所------------------------------------------------------




                if len(person_list2) != 0:

                 print("person_list2",person_list2)

                 max_area_person = (max(person_list2, key=(lambda x: x[3])))

                 max_area_id =  person_list2.index(max_area_person)


                 #print("max_area_id",max_area_id)



                 m_p = np.array([max_area_person[1], max_area_person[2]])


                 #衝突物体があるかどうか判定
                 for id_j in range(s):
                 	if len(person_list2[id_j][0]) >= 2:
                 		crash_frag = 1




                 #衝突物体が分離した時
                 if crash_frag == 1 and s == (sum + 1) and (old_max_area)*0.8 > max_area_person[3]:
                 	print("--------------------衝突物体が分離しました------------------------")
                 	first2 = 300
                 	second2 = 300
                 	dist2 = []
                 	crash_frag = 0

                 	for q in range(sum):
                 		if len(old_person_list2[q][0]) >=2:
                 			m = np.array([old_person_list2[q][1], old_person_list2[q][2]])




                 	for q_id in range(s):
                         		n = np.array([person_list2[q_id][1], person_list2[q_id][2]])

                         		print("sum",sum)
                         		print("s",s)
                         		print("m",m)


                         		u2 = m - n
                         		dist2 = np.linalg.norm(u2)
                         		print("dist2",dist2)

                         		if first2 > dist2:
                         		    second2 = first2
                         		    first2 = dist2


                         		    second_id2 = first_id2
                         		    first_id2 = q_id


                         		elif second2 > dist2:
                         		    second2 = dist2
                         		    second_id2 = q_id




                 	print("first_id2",first_id2)
                 	print("second_id2",second_id2)

                 	person_list2[first_id2][0] = []
                 	person_list2[second_id2][0] = []

                 	person_list2[first_id2][0].append(first_id[0])
                 	person_list2[second_id2][0].append(second_id[0])


















                 #id番号順にソート
                 person_list2 = sorted(person_list2)


                 #物体が衝突した場合
                 if s == (sum - 1):
                         print("-------------------物体が一つ減りました----------------------")
                         if (old_max_area)*(1.2) < max_area_person[3]:
                         	print("-----------------------物体が衝突した-------------------------")



                         	first = 300
                         	second = 300
                         	dist = []

                         	#衝突して出来た物体に距離が近い前フレームの二つの物体を衝突したとみなす

                         	for p_id in range(sum):
                         		o_p = np.array([old_person_list2[p_id][1], old_person_list2[p_id][2]])
                         		u = o_p - m_p
                         		dist = np.linalg.norm(u)

                         		print("dist2",dist)



                         		#二つの物体衝突
                         		if first > dist:
                         		    second = first
                         		    first = dist


                         		    second_id = first_id
                         		    first_id = old_person_list2[p_id][0]


                         		elif second > dist:
                         		    second = dist
                         		    second_id = old_person_list2[p_id][0]







                         	#二つの物体の衝突
                         	if len(person_list2[max_area_id][0]) == 1:
                         	 print("前フレームの"+str(first_id)+"と"+str(second_id)+"が衝突しました")
                         	 person_list2[max_area_id][0] = []
                         	 for firs in range(len(first_id)):
                         	 	person_list2[max_area_id][0].append(first_id[firs])
                         	 for sec in range(len(second_id)):
                         	 	person_list2[max_area_id][0].append(second_id[sec])






                         	#print("crash_after:",person_list2)


                         	print("first_id",first_id)
                         	print("second_id",second_id)

                 #print("crash",crash)
                 #番号を表示
                 for id_s in range(s):


                 	if len(person_list2[id_s][0]) == 1:
                 		cv2.putText(petit1,str(person_list2[id_s][0][0]),(person_list2[id_s][1],person_list2[id_s][2]),font,2.0,(0,255,0),4)
                 	elif len(person_list2[id_s][0]) == 2:
                 		cv2.putText(petit1,str(person_list2[id_s][0][0])+"+"+str(person_list2[id_s][0][1]),(person_list2[id_s][1]-70,person_list2[id_s][2]),font,2.0,(255,0,0),4)
                 	elif len(person_list2[id_s][0]) == 3:
                 		cv2.putText(petit1,str(person_list2[id_s][0][0])+"+"+str(person_list2[id_s][0][1])+"+"+str(person_list2[id_s][0][2]),(person_list2[id_s][1]-120,person_list2[id_s][2]),font,2.0,(0,0,255),4)












                 #前フレームの最大面積
                 old_max_area = max_area_person[3]


                old_person_list2 = []

                #前フレームの人間リスト[id.x.y.面積]
                for id_l in range(s):

                    old_person_list2.append(person_list2[id_l])


                    #人間リストのy座標をプロットする
                    if len(person_list2[id_l][0]) == 1:
                      centerY[id_l][-1] = person_list2[id_l][2]
                    elif len(person_list2[id_l][0]) == 2:
                    	centerY[3][-1] = person_list2[id_l][2]
                    elif len(person_list2[id_l][0]) == 3:
                    	centerY[4][-1] = person_list2[id_l][2]

                print("old_perspn_list:",old_person_list2)











                ResultImg[:,:]= (255,255,255)

                cv2.putText(ResultImg,"people come in: "+str(comeIn),(10,50),font2,0.6,(255,0,0))
                cv2.putText(ResultImg,"people go out: "+str(goOut),(10,20),font2,0.6,(255,0,0))
                cv2.putText(ResultImg,"total num of seats: "+str(SeatSum),(10,110),font2,0.6,(0,0,0))
                cv2.putText(ResultImg,"num of remaining seats: "+str(SeatSum-Total),(10,170),font2,0.6,(0,0,255))
                cv2.putText(ResultImg,"Sum of people inside: "+str(Total),(10,140),font2,0.6,(0,0,0))



                if id == 0 :
                    person = [[-1 for i in range(2)] for j in range(5)]

                cv2.imshow('Contours',petit1)
                cv2.moveWindow('Contours',360,55)
                ta = time.time()
                td = tb - ta
                time_length = abs(ta - startTime)
                cv2.putText(ResultImg,"Time duration: "+str(round(time_length,2))+" sec",(10,200),font2,0.6,(0,0,0))
                cv2.putText(ResultImg,"Frame's number: "+str(t),(10,230),font2,0.6,(0,0,0))
                #print(td)

    if k == 27:
        break

print ("t= "+ str(t))
time_after = time.time()
time_diff = time_after - time_before
print(time_diff)
print ("frame/sec = " + str(t/time_diff))

plt.subplot(2,1,1)
plt.plot(frame,centerY[0],'b--x')
#print(str(objNum))
#if objNum == 1:
plt.plot(frame,centerY[1],'g--x')

#if objNum == 2:
plt.plot(frame,centerY[2],'r--x')

#２つの衝突物体
plt.plot(frame,centerY[3],'y--x')

#３つの衝突物体
plt.plot(frame,centerY[4],'k--x')

plt.title("Movement of the detected oject")
plt.ylim(0,240)
plt.xlim(0,t)
plt.plot([0,t],[120,120],"r--")
#plt.plot([0,t],[100,100],"r--")
#plt.plot([0,t],[400,400],"r--")
plt.xlabel("frame")
plt.ylabel("Y axis of object(pixel)")

plt.subplot(2,1,2)
plt.bar(frame,total,align = "center")
plt.ylim(0,5)
plt.xlim(0,t)
plt.ylabel("Number of people in the room")


plt.show()

cap.release()
cv2.destroyAllWindows()
