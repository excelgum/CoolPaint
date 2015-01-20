############################################################
##########Paint Project by: Anas Ahmed######################
############################################################

#imports some commands and stuff
from pygame import *
from random import *
from math import *
screen = display.set_mode((1024, 768)) #makes the screen surface
#Below are some basic instructions for the user to follow
print "[~][~][~][~]--BASIC INSTRUCTIONS--[~][~][~][~]"
print ""
print "Left Mouse Button for First Color"
print "Right Mouse Button for Second Color"
print "Scroll Up - Increase Size"
print "Scroll Down - Decrease Size"
print "POLYGON TOOL: -Left click to draw polygon, right click to complete"

init()#font initializer 
fnt = font.SysFont("Times New Roman",24) #Adds
fnt2 = font.SysFont("Times New Roman",20) #two different size fonts


back = image.load("images\\Back.jpg") #loads the image of background
screen.blit(back,(0,0))

size=10 #size of brush/eraser/pictures

fixed=False #two variables used for tools
hold=False #later on the code

tools = ["pencil", "eraser", "line", "spray", "rectangle","ellipse","brush",
         "circle","polygon","fill","checker"] #list of all the tools in paint program
tool="None" #contains string of current tool selected
buttons = [] #this will contains the button (rectangles) of all the tools
for i in range(11):
    buttons.append(Rect(20, 80+i*50, 40,40)) #adds all the buttons of each tools in a good format
    #each button position repreasents the position of its tool

    
c=0,0,0 #sets the first color (left click) to black
c2=255,255,255#and second color (right click) to white
mx,my= 0,0 #sets mx,my to 0,0 (needed for later on)

running=True #main program running loop status(turns on)

#COLOR RECT
color=image.load("images\\color.jpg") #loads
screen.blit(color,(1024-250,768-110))#and displays the color selection picture
colorRect=Rect(1024-250,768-110,200,100)#formats the color rectangle

points=[]#list of points for polygon tool
pictures=[] #list of the picture positions(kinda like buttons)
for i in range(6):
    pictures.append(Rect(65+i*110,675,100,80)) #formats all of the pictures
    picture=image.load("pictures\\pictures"+str(i)+".jpg")#and displays them
    #notice: the str(i) is the picture number of picture
    picture=transform.scale(picture,(100,80))#scales them to appropriate size
    screen.blit(picture,pictures[i])#draws the picture on screen

save= image.load("images/save.png") #draws the save/open button and makes a rect
screen.blit(save,(945,150)) #of their position
saveRect =Rect(945,150,48,48)
openfile= image.load("images/open.png")
screen.blit(openfile,(945,220))
openRect=Rect(945,220,48,48)

undofile= image.load("images/undo.jpg") #this does the same for the undo/redo buttons
screen.blit(undofile,(930,90))
undoRect=Rect(930,90,29,29)
redofile= image.load("images/redo.jpg")
screen.blit(redofile,(965,90))
redoRect=Rect(965,90,29,29)
canvasRect=Rect(100,50,800,600) #rectangle coordinates/h/w of canvas
draw.rect(screen,(255,255,255),canvasRect)#draws the canvas rect

load=image.load("images\\logo.jpg")#loads/displays the logo
screen.blit(load,(300,0))
fillRect=Rect(910,300,100,50)#rect for the fill/unfill for shapes
up=True #variable used to check if mouse is pressed down and lifted
undo=[] #list that contains all of the undo canvas shots
redo=[] #list that contains all of the redo canvas shots
fill= False# tells the status of fill/unfill of shapes
while running: #main loop
    for i in range(11): #goes through button list and 
        if buttons[i].collidepoint(mx,my) and mb[0]==1: #if mouse is on any button
            tool = tools[i] #and mouse button is clicked, that tool is gonna be selected
            
    for evnt in event.get():          
        if evnt.type == QUIT:
            running=False #closes the loop once the window is closed
        if evnt.type == MOUSEBUTTONDOWN:
            if evnt.button ==5:
                size+=10 #if mouse wheel turns away from you the size decreases
            if evnt.button ==4:
                size= max(10, size-10) #in contrast if it goes towards you size increases
                #smallest size can be 10
        
    for i in range(11):
        if tool == tools[i]: #goes through tools and 
            load=image.load("images\\"+tools[i]+"s"+".jpg")#if a certain tool is
        else:#selected it will load the selected picture of that tool
            load=image.load("images\\"+tools[i]+".jpg") #other wise it displays the
        screen.blit(load, buttons[i]) #regular picture
        
    omx,omy= mx,my #mx,my position of last loop
    mx, my = mouse.get_pos() #mouse position
    mb = mouse.get_pressed() #get mouse button statuses 
    
    if colorRect.collidepoint(mx,my) and mb[0]==1:
        c=screen.get_at((mx,my)) #if mouseclick on color picture ,
        #what ever the color is on that pixel, the color selected will become it
    if colorRect.collidepoint(mx,my) and mb[2]==1:
        c2=screen.get_at((mx,my)) #same for right mouse button
        
    #PENCIL TOOL
    if tool== "pencil" and canvasRect.collidepoint(mx,my):
        screen.set_clip(canvasRect)#make sure the stuff being drawn doesnt escape canvas
        if mb[0]==1: #draws a line from an old mouse position to new one
            draw.line(screen,c,(omx,omy),(mx,my))
        elif mb[2]==1:#same for if the right  mouse button is down
            draw.line(screen,c2,(omx,omy),(mx,my))
        screen.set_clip(None)
        
    #ERASER TOOL
    if tool== "eraser" and canvasRect.collidepoint(mx,my) and mb[0]==1 :
        #similar triangle stuff below
        A=mx-x #Base of big triangle
        B=my-y #height of big triangle
        L=(A**2+B**2)**0.5 #hypot of big triangle
        if L==0: #makes sure distance is not 0
            L=1
        h=1 #small hypot of triangles
        a=(h/L)*A #solves for the height/base of small triangle
        b=(h/L)*B
        for i in range(L):
            screen.set_clip(canvasRect)
            draw.circle(screen,(255,255,255),(x,y),size) #draws circle on x,y
            x+=a#x increases by small triangle base
            y+=b#y increases by small triangle height
            screen.set_clip(None)
            
    #Brush Tool 
    if tool== "brush" and canvasRect.collidepoint(mx,my):
        A=mx-x#exact same as eraser tool except with color
        B=my-y
        L=(A**2+B**2)**0.5
        if L==0:
            L=1
        h=1
        a=(h/L)*A
        b=(h/L)*B
        for i in range(L):
            screen.set_clip(canvasRect)
            if mb[0]==1:
                draw.circle(screen,c,(x,y),size)
            elif mb[2]==1:
                draw.circle(screen,c2,(x,y),size)
            x+=a
            y+=b
            screen.set_clip(None)
    x,y=mx,my #position of circles
    
    #Line Tool
    if tool== "line" and canvasRect.collidepoint(mx,my):
        if fixed==False and 1 in mb:#if the fixed point is off and mousebutton is clicked
            fx,fy=mx,my #fixed point is mx,my 
            fixed=True #the fixed status is turned on
            hold=True #the hold status is turned on
            copy1=screen.copy()#makes a copy of screen
        if hold==True and 1 in mb: #keeps the hold status on if mouse button is down
            hold=True
        else:
            hold=False#else if the mousebutton is up the hold status is turned off 
            fixed=False#and fixed status
        if fixed ==True and hold==True:#once both status is on
            screen.blit(copy1,(0,0))
            if mb[0]==1:
                draw.line(screen,c,(mx,my),(fx,fy))#it keeps drawing the line from fixed
            if mb[2]==1: #point to mouse position
                draw.line(screen,c2,(mx,my),(fx,fy))
    #Spray Tool             
    if tool== "spray" and canvasRect.collidepoint(mx,my):
        screen.set_clip(canvasRect)
        for i in range(40+size): #draws 40+ size dots
            x=randint(mx-10-size,mx+10+size) #at random
            y=randint(my-10-size,my+10+size) #position at a certain square region
            if hypot(mx-x,my-y)<10+size: #but only displays it if 
                if mb[0]==1:#they are within a certain distance from mouse position
                    draw.circle(screen,c,(x,y),0.001) #so it comes out as a circle
                elif mb[2]==1: #of random dots around the mouse
                    draw.circle(screen,c2,(x,y),0.001)
        screen.set_clip(None)

    #Rectangle Tool
    if tool== "rectangle" and canvasRect.collidepoint(mx,my):
        if fixed==False and 1 in mb: #almost same as line tool
            fx,fy=mx,my #but draws rectangles
            fixed=True
            hold=True
            copy1=screen.copy()
        if hold==True and 1 in mb:
            hold=True
        else:
            hold=False
            fixed=False
        if fixed ==True and hold==True:
            screen.blit(copy1,(0,0))
            if mb[0]==1:
                draw.rect(screen,c,(fx,fy,mx-fx,my-fy),w)
            elif mb[2]==1:
                draw.rect(screen,c2,(fx,fy,mx-fx,my-fy),w)
    #Ellipse Tool
    if tool== "ellipse" and canvasRect.collidepoint(mx,my):
        if fixed==False and 1 in mb:#almost same as line tool
            fx,fy=mx,my
            fixed=True
            hold=True
            copy1=screen.copy()
        if hold==True and 1 in mb:
            hold=True
        else:
            hold=False
            fixed=False
        if fixed ==True and hold==True:
            screen.blit(copy1,(0,0))#but draws an ellipse
            if mb[0]==1:
                color=c
            elif mb[2]==1:
                color=c2
            if fx>mx and fy>my:
                if fx-mx>4 and fy-my>4: #4 different ones
                    draw.ellipse(screen,color,(mx,my,fx-mx,fy-my),w)
            if fx>mx and fy<my:#which are at different quadrants around the mouse
                if fx-mx>4 and my-fy>4:#because the ellipse tool needs
                    draw.ellipse(screen,color,(mx,fy,fx-mx,my-fy),w)
            if fx<mx and fy>my:#a top left point and bottem right
                if mx-fx>4 and fy-my>4:
                    draw.ellipse(screen,color,(fx,my,mx-fx,fy-my),w)
            if fx<mx and fy<my:
               if mx-fx>4 and my-fy>4:
                   draw.ellipse(screen,color,(fx,fy,mx-fx,my-fy),w)
    #Pictures/Stamps               
    for i in range(6):
        if pictures[i].collidepoint(mx,my) and mb[0]==1:#checks what 
            tool="picture"#picture the mouse is clicking on
            number=str(i) #notes the number of pictures         
    if tool== "picture": #once the tool is picture
        if fixed==False and mb[0]==1: #almost same as line
            fixed=True
            hold=True
            copy1=screen.copy()
        if hold==True and mb[0]==1:
            hold=True
        else:
            hold=False
            fixed=False
            tool="none"
        if fixed ==True and hold==True:  
            screen.set_clip(canvasRect)#when the mouse is let go
            screen.blit(copy1,(0,0)) #it draws the picture on screen of that position
            load=image.load("pictures\\pictures"+number+".jpg")
            load=transform.scale(load,(100+size*10,80+size*8)) #changes size of it according
            screen.blit(load,(mx-40-size*5,my-50-size*4)) #to mousewheel
            screen.set_clip(None)
            
    #Circle Tool        
    if tool== "circle" and canvasRect.collidepoint(mx,my):
        if fixed==False and 1 in mb: #as soon as the mouse is not pressed anymore
            fx,fy=mx,my
            fixed=True
            hold=True
            copy1=screen.copy()
        if hold==True and 1 in mb:
            hold=True
        else:
            hold=False
            fixed=False
        if fixed ==True and hold==True:
            screen.set_clip(canvasRect)#it draws a circle from the fixed point with a radius 
            screen.blit(copy1,(0,0))#of distance from mousepoint to fixed point
            dist=hypot(fx-mx,fy-my)
            if dist>2:
                if mb[0]==1:
                    draw.circle(screen,c,(fx,fy),dist,w)#if left mouse button is clicked
                elif mb[2]==1:#it would draw it with the first color
                    draw.circle(screen,c2,(fx,fy),dist,w)#if right mouse button is clicked
            screen.set_clip(None)#it would draw it with second color
            
    #Checker Tool
    if tool== "checker" and canvasRect.collidepoint(mx,my):
        if mb[0]==1:#this tool gets the color at which the mouse is on
            c=screen.get_at((mx,my)) #with the screen.get_at command
        if mb[2]==1:
            c2=screen.get_at((mx,my))#same for right mousebutton
    #Polygon Tool         
    if tool== "polygon" and canvasRect.collidepoint(mx,my):
        if fixed==False and mb[0]==1:
            fx,fy=mx,my #once the fixed point if False and the mouse is clicked
            fixed=True#then it turns on and it makes a copy of the screen
            copy1=screen.copy()#and also keeps a record of its position at that time
        if fixed ==True: #when it turns on
            screen.blit(copy1,(0,0)) #it keeps pasting that copy and
            draw.line(screen,c,(mx,my),(fx,fy)) #drawing a line to mouse from it
            if mb[0]==1:
                points.append((fx,fy))#once the mouse clicks again
                fx,fy=mx,my#that point is added to a list and then again a new fixed
                copy1=screen.copy()#point is made and a screenshot is taken
            elif mb[2]==1: #it repeats this process until right mouse button is clicked
                fx,fy=mx,my #it then adds final point 
                points.append((fx,fy))#and then draws a polygon on the point list
                draw.polygon(screen,c,points,w)
                fixed=False#fixed is then false and everything is reset
                points=[]

    #Fill Tool
    if tool=="fill" and canvasRect.collidepoint(mx,my):
        if mb[0]==1 and screen.get_at((mx,my))!=c:#once the position of mouseclick
            col= screen.get_at((mx,my))#is not the color selected, it sets a col for the point of where its clicked
            points=[(mx,my)]#the points list contains the points to be colored
            while True:#main fill loop
                counter = 0#keeps track of how many points that have been colored in a single
                for i in range(len(points)):#it goes through every point
                    point=points[i]#checks 4 points above,below,right,left of it and if
                    #it is the main color then it changes it to the desire color and adds it to the list
                    up= point[0],point[1]-1#it then does that for each of the point
                    down=point[0],point[1]+1
                    right=point[0]+1,point[1]
                    left=point[0]-1,point[1]
                    
                    if screen.get_at(up) == col:#top
                        points.append(up)
                        draw.line(screen,c,up,up)
                        counter += 1  
                    if screen.get_at(right) == col:#right
                        points.append(right)
                        draw.line(screen,c,right,right)
                        counter+=1  
                    if screen.get_at(down) == col:#bottom
                        points.append(down)
                        draw.line(screen,c,down,down)
                        counter += 1
                    if screen.get_at(left) == col:#left
                        points.append(left)
                        draw.line(screen,c,left,left)
                        counter += 1
                display.flip()#this shows the fill in progress, no reason for this other then
                #make the fill command look cool
                
                while len(points)!= counter:#this deletes every point before until only the newly
                    points.remove(points[0])#added point is in the list
                    #which makes the fill tool work much faster
                    
                if counter == 0:#once there is no more points added in a single round of the list
                    points = []#that means there is no more points to fill
                    break #so it breaks the main fill loop and resets the points

    #Below adds text which displays many important details at appropriate places               
    if canvasRect.collidepoint(mx,my):         
        text = "%4d %4d" % (mx-100,my-50)#mouse position
        textPic = fnt.render(text,1,(255,255,255))   
        draw.rect(screen,(40,68,112),(900,50,130,35))
        screen.blit(textPic, (915,55))
    else:
        text = "Out of Canvas"#out of canvas if mouse is not in canvas
        textPic = fnt2.render(text,1,(255,255,255))  
        draw.rect(screen,(40,68,112),(900,50,130,35))
        screen.blit(textPic, (900,55))

    text = "Tool: "+tool #tools selected
    draw.rect(screen,(40,68,112),(900,370,150,25))
    textPic = fnt2.render(text,1,(255,255,255))
    screen.blit(textPic,(900,370))
    text = "Size: "+str(size)
    draw.rect(screen,(40,68,112),(900,400,150,25))
    textPic = fnt2.render(text,1,(255,255,255))
    screen.blit(textPic,(900,400))
    
    text = "Color1 " #Color 1 rgb values
    draw.rect(screen,(40,68,112),(900,440,150,25))
    textPic = fnt2.render(text,1,(255,255,255))
    screen.blit(textPic,(900,440))
    text = str(c[:3])
    draw.rect(screen,(40,68,112),(900,460,150,25))
    textPic = fnt2.render(text,1,(255,255,255))
    screen.blit(textPic,(900,460))
    text = "Color2 " #color 2 rgb values
    draw.rect(screen,(40,68,112),(900,490,150,25))
    textPic = fnt2.render(text,1,(255,255,255))
    screen.blit(textPic,(900,490))
    text = str(c2[:3])
    draw.rect(screen,(40,68,112),(900,510,150,25))
    textPic = fnt2.render(text,1,(255,255,255))
    screen.blit(textPic,(900,510))
    
    #UNDO/REDO Tool/Others
    #Below makes the variable up True once the mouse is pressed down and lifted
    if 1 in mb and up == True:
        up=False
    if up== False and 1 not in mb:
        ss= screen.subsurface(canvasRect).copy()#it adds that moment to 
        undo.append(ss)#the undo list
        up=True#makes up True
        if len(redo)>0 and canvasRect.collidepoint(mx,my):
            redo=[]#once the mouse starts drawing on canvas the redo list is reset
        if fillRect.collidepoint(mx,my):#this checks if the mouse has clicked
            if fill==False:#the fill/unfill button for shapes
                fill=True
            else:
                fill=False
            print fill
    if undoRect.collidepoint(mx,my) and evnt.type==MOUSEBUTTONDOWN and len(undo)>0:
        screen.blit(undo[-1],(100,50))#once the undo button is pressed
        redo.append(undo[-1])#it displays the last screencapture
        undo.remove(undo[-1])#adds it to redo list and deletes it from undo list
        #Below is a useless code which delays the mouse clicks so it
        #does not undo more than once
        for i in range(100):
            x=10
            x="Dog" 
    if redoRect.collidepoint(mx,my) and mb[0]==1 and len(redo)>0:
        screen.blit(redo[-1],(100,50))#the redo is opposite of undo
        undo.append(redo[-1])#it displays the last redo screencapture
        redo.remove(redo[-1])#removes it and adds it back to undo
        #Another useless code below
        for i in range(100):
            x=5
            x="Cat"
            
    #Save/Load Stuff        
    if saveRect.collidepoint(mx,my) and evnt.type==MOUSEBUTTONDOWN:#once the user clicks
        filename= raw_input("Please Enter The FileName: ")#the save button it ask for filename
        image.save(screen.subsurface(canvasRect),filename+".jpg")#to saves as and saves it
        print "Image has been saved successfully"#as jpeg picture
    if openRect.collidepoint(mx,my) and evnt.type==MOUSEBUTTONDOWN:#the open loads a 
        filename= raw_input("Please Enter The FileName to open: ")#picture that the user
        load=image.load(filename+".jpg")#enters to the canvas
        screen.blit(load,(100,50))
        print "Image has been opened succesfully"
    
    #Below are two rectangle drawn to show the two colors selected
    draw.rect(screen,c2,(950,575,50,50))#second color
    draw.rect(screen,(0,0,0),(950,575,50,50),4) 
    draw.rect(screen,c,(930,550,50,50))#first color
    draw.rect(screen,(0,0,0),(930,550,50,50),4)#and draws a border

    #FILL/UNFILL STATUS
    if fill==False:
        load=image.load("images\\rectangle1.jpg")#loads two differenct pictures 
        w=2#based on if the user wants shape filled/unfilled
    elif fill==True:
        load=image.load("images\\rectangle2.jpg")
        w=0
    screen.blit(load,(910,300))
    display.flip()#this displays anything that has been drawn in the main loop
    
    
del fnt #deletes fonts
del fnt2
quit() #and quits

#THE END
