# -*- coding:utf-8 -*-
# @Author: Thiago de Sousa Silveira forked from STUD's YEDDA Annotator Jie Yang.
# @Date: 2018-Apr-20
# @Contact: thiagosousasilveira@gmail.com
# @Last Modified time: 2018-03-05 17:41:03
# @Modifications from the YEDDAnnotator:
# Modified the interface: removed automatic labelling features and 2 buttons
# Removed features of intelligent annotation, modified the annotation method from selecting the annotated word to cursor pointing. 
# Overall, I modified the Example class in the YEDDA project -> TopicSegmentationAnnotator
#!/usr/bin/env python
# coding=utf-8

from Tkinter import *
from ttk import *
import tkFileDialog
import tkMessageBox
import tkFont
import re
from collections import deque
import pickle
import os.path
import platform
import tkMessageBox
import sys

#Topic Segmentation Annotator class
class TopicSegmentationAnnotator(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.Version = "YEDDA-V1.0 Annotator"
        self.OS = platform.system().lower()
        self.parent = parent
        self.fileName = ""
        self.debug = False
        self.colorAllChunk = True
        self.recommendFlag = True
        self.history = deque(maxlen=20)
        self.currentContent = deque(maxlen=1)
        self.pressCommand = {'a':"Artifical",
                             'b':"Event",
                             'c':"Fin-Concept",
                             'd':"Location",
                             'e':"Organization",
                             'f':"Person",
                             'g':"Sector",
                             'h':"Other"
                             }
        self.allKey = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.controlCommand = {'q':"unTag", 'ctrl+z':'undo'}
        self.labelEntryList = []
        self.shortcutLabelList = []
        # default GUI display parameter
        if len(self.pressCommand) > 20:
            self.textRow = len(self.pressCommand)
        else:
            self.textRow = 20
        self.textColumn = 5
        self.tagScheme = "BMES"
        self.onlyNP = False  ## for exporting sequence 
        self.keepRecommend = True

        #connection
        self.currentDocument = None
        
        self.seged = False  ## False for non-segmentated Chinese, True for English or Segmented Chinese
        self.configFile = "config"
        self.entityRe = r'\[\@.*?\#.*?\*\](?!\#)'
        self.tagRe = r'<<</?\w+[^>]*>>>\n'
        self.insideNestEntityRe = r'\[\@\[\@(?!\[\@).*?\#.*?\*\]\#'
        self.recommendRe = r'\[\$.*?\#.*?\*\](?!\#)'
        self.goldAndrecomRe = r'\[\@.*?\#.*?\*\](?!\#)'
        if self.keepRecommend:
            self.goldAndrecomRe = r'\[[\@\$)].*?\#.*?\*\](?!\#)'
        ## configure color
        self.entityColor = "SkyBlue1"
        self.insideNestEntityColor = "light slate blue"
        self.recommendColor = 'lightgreen'
        self.selectColor = 'light salmon'
        self.textFontStyle = "Times"
        self.initUI()
        
        
    def initUI(self):
      
        self.parent.title(self.Version)
        self.pack(fill=BOTH, expand=True)
        
        for idx in range(0,self.textColumn):
            self.columnconfigure(idx, weight =2)
        # self.columnconfigure(0, weight=2)
        self.columnconfigure(self.textColumn+2, weight=1)
        self.columnconfigure(self.textColumn+4, weight=1)
        for idx in range(0,16):
            self.rowconfigure(idx, weight =1)
        
        self.lbl = Label(self, text="File: no file is opened")
        self.lbl.grid(sticky=W, pady=4, padx=5)
        self.fnt = tkFont.Font(family=self.textFontStyle,size=self.textRow,weight="bold",underline=0)
        self.text = Text(self, font=self.fnt, selectbackground=self.selectColor)
        self.text.grid(row=1, column=0, columnspan=self.textColumn, rowspan=self.textRow, padx=10, sticky=E+W+S+N)

        self.sb = Scrollbar(self)
        self.sb.grid(row = 1, column = self.textColumn, rowspan = self.textRow, padx=0, sticky = E+W+S+N)
        self.text['yscrollcommand'] = self.sb.set 
        self.sb['command'] = self.text.yview 
        # self.sb.pack()

        abtn = Button(self, text="Load Next File", command=self.onNext,width=10)
        abtn.grid(row=1, column=self.textColumn +1,padx=4)

        exportbtn = Button(self, text="Save", command=self.saveFile)
        exportbtn.grid(row=2, column=self.textColumn + 1, pady=4)

        cbtn = Button(self, text="Quit", command=self.quit,width=5)
        cbtn.grid(row=3, column=self.textColumn + 1, pady=4, padx=2)

        self.cursorName = Label(self, text="Cursor: ", foreground="Blue", font=(self.textFontStyle, 14, "bold"))
        self.cursorName.grid(row=9, column=self.textColumn +1, pady=4)
        self.cursorIndex = Label(self, text=("row: %s\ncol: %s" % (0, 0)), foreground="red", font=(self.textFontStyle, 14, "bold"))
        self.cursorIndex.grid(row=10, column=self.textColumn + 1, pady=4)
       

        # lbl_entry = Label(self, text="Command:")
        # lbl_entry.grid(row = self.textRow +1,  sticky = E+W+S+N, pady=4,padx=4)
        # self.entry = Entry(self)
        # self.entry.grid(row = self.textRow +1, columnspan=self.textColumn + 1, rowspan = 1, sticky = E+W+S+N, pady=4, padx=80)
        # self.entry.bind('<Return>', self.returnEnter)

        # for press_key in self.pressCommand.keys():
        for idx in range(0, len(self.allKey)):
            press_key = self.allKey[idx]

            # self.text.bind(press_key, lambda event, arg=press_key:self.textReturnEnter(event,arg))
            self.text.bind(press_key, self.textReturnEnter)
            simplePressKey = "<KeyRelease-" + press_key + ">"
            self.text.bind(simplePressKey, self.deleteTextInput)
            if self.OS != "windows":
                controlPlusKey = "<Control-Key-" + press_key + ">"
                self.text.bind(controlPlusKey, self.keepCurrent)
                altPlusKey = "<Command-Key-" + press_key + ">"
                self.text.bind(altPlusKey, self.keepCurrent)


        self.text.bind('<Control-Key-z>', self.backToHistory)
        self.text.bind('<Button-2>', self.rightClick)
        self.text.bind('<Button-3>', self.rightClick)
        self.text.bind('<Double-Button-1>', self.doubleLeftClick)
        self.text.bind('<ButtonRelease-1>', self.singleLeftClick)

        self.setMapShow()

        # self.enter = Button(self, text="Enter", command=self.returnButton)
        # self.enter.grid(row=self.textRow +1, column=self.textColumn +1) 
    

    ## cursor index show with the left click
    def singleLeftClick(self, event):
        if self.debug:
            print "Action Track: singleLeftClick"
        cursor_index = self.text.index(INSERT) 
        row_column = cursor_index.split('.')
        cursor_text = ("row: %s\ncol: %s" % (row_column[0], row_column[-1]))
        self.cursorIndex.config(text=cursor_text)

    
    ## TODO: select entity by double left click
    def doubleLeftClick(self, event):
        if self.debug:
            print "Action Track: doubleLeftClick"
        pass     
        
    ## Disable right click default copy selection behaviour
    def rightClick(self, event):
        if self.debug:
            print "Action Track: rightClick"
        try:
            firstSelection_index = self.text.index(SEL_FIRST)
            cursor_index = self.text.index(SEL_LAST)
            content = self.text.get('1.0',"end-1c").encode('utf-8')
            self.writeFile(self.fileName, content, cursor_index)
        except TclError:
            pass

    def setInRecommendModel(self):
        self.recommendFlag = True
        self.RecommendModelFlag.config(text = str(self.recommendFlag))
        tkMessageBox.showinfo("Recommend Model", "Recommend Model has been activated!")


    def setInNotRecommendModel(self):
        self.recommendFlag = False 
        self.RecommendModelFlag.config(text = str(self.recommendFlag))
        content = self.getText()
        content = removeRecommendContent(content,self.recommendRe)
        self.writeFile(self.fileName, content, '1.0')
        tkMessageBox.showinfo("Recommend Model", "Recommend Model has been deactivated!")

    def readFile(self, filename):
        f = open(filename, "rU")
        text = f.read()
        self.fileName = filename
        return text

    def setFont(self, value):
        _family=self.textFontStyle
        _size = value
        _weight="bold"
        _underline=0
        fnt = tkFont.Font(family= _family,size= _size,weight= _weight,underline= _underline)
        Text(self, font=fnt)
    
    def setNameLabel(self, new_file):
        self.lbl.config(text=new_file)

    def setCursorLabel(self, cursor_index):
        if self.debug:
            print "Action Track: setCursorLabel"
        row_column = cursor_index.split('.')
        cursor_text = ("row: %s\ncol: %s" % (row_column[0], row_column[-1]))
        self.cursorIndex.config(text=cursor_text)

    def returnButton(self):
        if self.debug:
            print "Action Track: returnButton"
        self.pushToHistory()
        # self.returnEnter(event)
        #content = self.entry.get()
        self.clearCommand()
        self.executeEntryCommand(content)
        return content


    def returnEnter(self,event):
        if self.debug:
            print "Action Track: returnEnter"
        self.pushToHistory()
        content = self.entry.get()
        self.clearCommand()
        self.executeEntryCommand(content)
        return content


    def textReturnEnter(self,event):
        press_key = event.char
        if self.debug:
            print "Action Track: textReturnEnter"
        self.pushToHistory()
        print "event: ", press_key
        # content = self.text.get()
        self.clearCommand()
        self.executeCursorCommand(press_key.lower())
        # self.deleteTextInput()
        return press_key


    def backToHistory(self,event):
        if self.debug:
            print "Action Track: backToHistory"
        if len(self.history) > 0:
            historyCondition = self.history.pop()
            # print "history condition: ", historyCondition
            historyContent = historyCondition[0]
            # print "history content: ", historyContent
            cursorIndex = historyCondition[1]
            # print "get history cursor: ", cursorIndex
            self.writeFile(self.fileName, historyContent, cursorIndex)
        else:
            print "History is empty!"
        self.text.insert(INSERT, 'p')   # add a word as pad for key release delete

    def keepCurrent(self, event):
        if self.debug:
            print "Action Track: keepCurrent"
        print("keep current, insert:%s"%(INSERT))
        print "before:", self.text.index(INSERT)
        self.text.insert(INSERT, 'p')
        print "after:", self.text.index(INSERT)

    def clearCommand(self):
        if self.debug:
            print "Action Track: clearCommand"
        #self.entry.delete(0, 'end')


    def getText(self):
        textContent = self.text.get("1.0","end-1c")
        textContent = textContent.encode('utf-8')
        return textContent

    #save file
    def saveFile(self):
        fout = open(self.fileName+".ann","w")
        fout.write(self.currentDocument)
        fout.close()

    def onNext(self):

        #save previous file
        if self.currentDocument!=None:
            self.saveFile()

        ftypes = [('all files', '.*'), ('text files', '.txt'), ('ann files', '.ann')]
        dlg = tkFileDialog.Open(self, filetypes = ftypes)
        fl = dlg.show()
        if fl != '':
            self.text.delete("1.0",END)
            self.currentDocument = self.readFile(fl)
            self.text.insert(END, self.currentDocument)
            self.setNameLabel("File: " + fl)
            self.autoLoadNewFile(self.fileName, "1.0")
            # self.setDisplay()
            # self.initAnnotate()
            self.text.mark_set(INSERT, "1.0")
            self.setCursorLabel(self.text.index(INSERT))

    #Execute the tagging command
    def executeCursorCommand(self,command):
        if self.debug:
            print "Action Track: executeCursorCommand"
        content = self.getText()
        print("Command:"+command)

        if command not in self.pressCommand and command!="q":
            return

        try:
            #firstSelection_index = self.text.index(SEL_FIRST)
            cursor_index = self.text.index("insert")
            aboveHalf_content = self.text.get('1.0',cursor_index)
            followHalf_content = self.text.get(cursor_index, "end-1c")
            wholeText = self.text.get('1.0', 'end').split("\n")

            #check if the user selected a line with a tag
            line,column = cursor_index.split(".")
            line = int(line)-1
            intag = False
            if "<<<" in wholeText[line]:
                intag = True

            #if the user selected a line with a tag
            if intag==True:

                #select the tag or remove if that's the case
                if command=="q":
                    tag = "\n"
                else:
                    tag = "\n<<<"+self.pressCommand[command]+">>>\n"
                content = "\n".join(wholeText[:line]) + tag + "\n".join(wholeText[line+1:])
            else:

                if command=="q":
                    return

                #adjusting the tag
                tag = "<<<"+self.pressCommand[command]+">>>"
                if len(aboveHalf_content)>0 and aboveHalf_content[-1]!="\n":
                    tag = "\n"+tag
                if followHalf_content[0]!="\n":
                    tag = tag+"\n"

                #building the content
                content = aboveHalf_content + tag + followHalf_content

            self.currentDocument = content.encode("utf-8")

            self.writeFile(self.fileName, content, cursor_index)

        except TclError:
            print ("ERROR WHEN ADDING THE TAG!")

    #Execute the entry command on the text element
    def executeEntryCommand(self,command):
        if self.debug:
            print "Action Track: executeEntryCommand"
        if len(command) == 0:
            currentCursor = self.text.index(INSERT)
            newCurrentCursor = str(int(currentCursor.split('.')[0])+1) + ".0"
            self.text.mark_set(INSERT, newCurrentCursor)
            self.setCursorLabel(newCurrentCursor)
        else:
            command_list = decompositCommand(command)
            for idx in range(0, len(command_list)):
                command = command_list[idx]
                if len(command) == 2:
                    select_num = int(command[0])
                    command = command[1]
                    content = self.getText()
                    cursor_index = self.text.index(INSERT)
                    newcursor_index = cursor_index.split('.')[0]+"."+str(int(cursor_index.split('.')[1])+select_num)
                    # print "new cursor position: ", select_num, " with ", newcursor_index, "with ", newcursor_index
                    selected_string = self.text.get(cursor_index, newcursor_index).encode('utf-8')
                    aboveHalf_content = self.text.get('1.0',cursor_index).encode('utf-8')
                    followHalf_content = self.text.get(cursor_index, "end-1c").encode('utf-8')
                    if command in self.pressCommand:
                        if len(selected_string) > 0:
                            # print "insert index: ", self.text.index(INSERT) 
                            followHalf_content, newcursor_index = self.replaceString(followHalf_content, selected_string, command, newcursor_index)
                            content = self.addRecommendContent(aboveHalf_content, followHalf_content, self.recommendFlag)
                            # content = aboveHalf_content + followHalf_content
                    self.writeFile(self.fileName, content, newcursor_index)
            

    def deleteTextInput(self,event):
        if self.debug:
            print "Action Track: deleteTextInput"
        get_insert = self.text.index(INSERT)
        print "delete insert:",get_insert
        insert_list = get_insert.split('.')
        last_insert = insert_list[0] + "." + str(int(insert_list[1])-1)
        get_input = self.text.get(last_insert, get_insert).encode('utf-8')
        # print "get_input: ", get_input
        aboveHalf_content = self.text.get('1.0',last_insert).encode('utf-8')
        followHalf_content = self.text.get(last_insert, "end-1c").encode('utf-8')
        if len(get_input) > 0: 
            followHalf_content = followHalf_content.replace(get_input, '', 1)
        content = aboveHalf_content + followHalf_content
        self.writeFile(self.fileName, content, last_insert)

    def writeFile(self, fileName, content, newcursor_index):
        if self.debug:
                print "Action track: writeFile"

        if len(fileName) > 0:
            self.autoLoadNewFile(fileName, newcursor_index)
        else:
            print "Don't write to empty file!"        

    def autoLoadNewFile(self, fileName, newcursor_index):
        if self.debug:
            print "Action Track: autoLoadNewFile"
        if len(fileName) > 0:
            self.text.delete("1.0",END)
            #text = self.readFile(fileName)
            self.text.insert("end-1c", self.currentDocument)
            self.setNameLabel("File: " + fileName)
            self.text.mark_set(INSERT, newcursor_index)
            self.text.see(newcursor_index)
            self.setCursorLabel(newcursor_index)
            self.setColorDisplay()
            
    def setColorDisplay(self):
        if self.debug:
            print "Action Track: setColorDisplay"
        self.text.config(insertbackground='red', insertwidth=4, font=self.fnt)

        countVar = StringVar()
        currentCursor = self.text.index(INSERT)
        lineStart = currentCursor.split('.')[0] + '.0'
        lineEnd = currentCursor.split('.')[0] + '.end'
         
        if self.colorAllChunk:
            self.text.mark_set("matchStart", "1.0")
            self.text.mark_set("matchEnd", "1.0")
            self.text.mark_set("searchLimit", 'end-1c')
            self.text.mark_set("recommend_matchStart", "1.0")
            self.text.mark_set("recommend_matchEnd", "1.0")
            self.text.mark_set("recommend_searchLimit", 'end-1c')
        else:
            self.text.mark_set("matchStart", lineStart)
            self.text.mark_set("matchEnd", lineStart)
            self.text.mark_set("searchLimit", lineEnd)
            self.text.mark_set("recommend_matchStart", lineStart)
            self.text.mark_set("recommend_matchEnd", lineStart)
            self.text.mark_set("recommend_searchLimit", lineEnd)
        while True:
            self.text.tag_configure("catagory", background=self.entityColor)
            self.text.tag_configure("edge", background=self.entityColor)
            pos = self.text.search(self.entityRe, "matchEnd" , "searchLimit",  count=countVar, regexp=True)
            if pos =="":
                break
            self.text.mark_set("matchStart", pos)
            self.text.mark_set("matchEnd", "%s+%sc" % (pos, countVar.get()))
            
            first_pos = pos
            second_pos = "%s+%sc" % (pos, str(1))
            lastsecond_pos = "%s+%sc" % (pos, str(int(countVar.get())-1))
            last_pos = "%s + %sc" %(pos, countVar.get())

            self.text.tag_add("category", second_pos, lastsecond_pos)
            self.text.tag_add("edge", first_pos, second_pos)
            self.text.tag_add("edge", lastsecond_pos, last_pos)   
        ## color recommend type
        while True:
            self.text.tag_configure("recommend", background=self.recommendColor)
            recommend_pos = self.text.search(self.recommendRe, "recommend_matchEnd" , "recommend_searchLimit",  count=countVar, regexp=True)
            if recommend_pos =="":
                break
            self.text.mark_set("recommend_matchStart", recommend_pos)
            self.text.mark_set("recommend_matchEnd", "%s+%sc" % (recommend_pos, countVar.get()))
            
            first_pos = recommend_pos
            # second_pos = "%s+%sc" % (recommend_pos, str(1))
            lastsecond_pos = "%s+%sc" % (recommend_pos, str(int(countVar.get())))
            self.text.tag_add("recommend", first_pos, lastsecond_pos)
            
        
        ## color the most inside span for nested span, scan from begin to end again  
        if self.colorAllChunk:
            self.text.mark_set("matchStart", "1.0")
            self.text.mark_set("matchEnd", "1.0")
            self.text.mark_set("searchLimit", 'end-1c')
        else:
            self.text.mark_set("matchStart", lineStart)
            self.text.mark_set("matchEnd", lineStart)
            self.text.mark_set("searchLimit", lineEnd)
        while True:
            self.text.tag_configure("insideEntityColor", background=self.insideNestEntityColor)
            pos = self.text.search(self.insideNestEntityRe , "matchEnd" , "searchLimit",  count=countVar, regexp=True)
            if pos == "":
                break
            self.text.mark_set("matchStart", pos)
            self.text.mark_set("matchEnd", "%s+%sc" % (pos, countVar.get()))
            first_pos = "%s + %sc" %(pos, 2)
            last_pos = "%s + %sc" %(pos, str(int(countVar.get())-1))
            self.text.tag_add("insideEntityColor", first_pos, last_pos)
    
    def pushToHistory(self):
        if self.debug:
            print "Action Track: pushToHistory"
        currentList = []
        content = self.getText()
        cursorPosition = self.text.index(INSERT)
        # print "push to history cursor: ", cursorPosition
        currentList.append(content)
        currentList.append(cursorPosition)
        self.history.append(currentList)

    def pushToHistoryEvent(self,event):
        if self.debug:
            print "Action Track: pushToHistoryEvent"
        currentList = []
        content = self.getText()
        cursorPosition = self.text.index(INSERT)
        # print "push to history cursor: ", cursorPosition
        currentList.append(content)
        currentList.append(cursorPosition)
        self.history.append(currentList)

    ## update shortcut map
    def renewPressCommand(self):
        print("DISABLED!")
        # if self.debug:
        #     print "Action Track: renewPressCommand"
        # seq = 0
        # new_dict = {}
        # listLength = len(self.labelEntryList)
        # delete_num = 0
        # for key in sorted(self.pressCommand):
        #     label = self.labelEntryList[seq].get()
        #     if len(label) > 0:
        #         new_dict[key] = label
        #     else: 
        #         delete_num += 1
        #     seq += 1
        # self.pressCommand = new_dict
        # for idx in range(1, delete_num+1):
        #     self.labelEntryList[listLength-idx].delete(0,END)
        #     self.shortcutLabelList[listLength-idx].config(text="NON= ") 
        # with open(self.configFile, 'wb') as fp:
        #     pickle.dump(self.pressCommand, fp)
        # self.setMapShow()
        # tkMessageBox.showinfo("Remap Notification", "Shortcut map has been updated!\n\nConfigure file has been saved in File:" + self.configFile)


    ## show shortcut map
    def setMapShow(self):
        if not os.path.isfile(self.configFile):
            print("NO CONFIG FILE")
            exit(0)
        tags = open(self.configFile).readlines()
        self.pressCommand = dict()
        for tag in tags:
            key, tag = tag.split("\t")
            self.pressCommand[key] = tag.rstrip()
        # if os.path.isfile(self.configFile):
        #     with open (self.configFile, 'rb') as fp:
        #         self.pressCommand = pickle.load(fp)
        hight = len(self.pressCommand)
        width = 2
        row = 0
        mapLabel = Label(self, text ="Shortcuts map Labels", foreground="blue", font=(self.textFontStyle, 14, "bold"))
        mapLabel.grid(row=0, column = self.textColumn +2,columnspan=2, rowspan = 1, padx = 10)
        self.labelEntryList = []
        self.shortcutLabelList = []
        for key in sorted(self.pressCommand):
            row += 1
            # print "key: ", key, "  command: ", self.pressCommand[key]
            symbolLabel = Label(self, text =key.upper() + ": ", foreground="blue", font=(self.textFontStyle, 14, "bold"))
            symbolLabel.grid(row=row, column = self.textColumn +2,columnspan=1, rowspan = 1, padx = 1)
            self.shortcutLabelList.append(symbolLabel)

            labelEntry = Entry(self, foreground="blue", font=(self.textFontStyle, 14, "bold"), width=25)
            labelEntry.insert(0, self.pressCommand[key])
            labelEntry.grid(row=row, column = self.textColumn +3, columnspan=1, rowspan = 1)
            labelEntry.config(state='disabled')
            self.labelEntryList.append(labelEntry)
            # print "row: ", row


    def getCursorIndex(self):
        return self.text.index(INSERT)


    def generateSequenceFile(self):
        if (".ann" not in self.fileName) and (".txt" not in self.fileName): 
            out_error = "Export only works on filename ended in .ann or .txt!\nPlease rename file."
            print out_error
            tkMessageBox.showerror("Export error!", out_error)

            return -1
        fileLines = open(self.fileName, 'rU').readlines()
        lineNum = len(fileLines)
        new_filename = self.fileName.split('.ann')[0]+ '.anns'
        seqFile = open(new_filename, 'w')
        for line in fileLines:
            if len(line) <= 2:
                seqFile.write('\n')
                continue
            else:
                if not self.keepRecommend:
                    line = removeRecommendContent(line, self.recommendRe)
                wordTagPairs = getWordTagPairs(line, self.seged, self.tagScheme, self.onlyNP, self.goldAndrecomRe)
                for wordTag in wordTagPairs:
                    seqFile.write(wordTag)
                ## use null line to seperate sentences
                seqFile.write('\n')
        seqFile.close()
        print "Exported file into sequence style in file: ",new_filename
        print "Line number:",lineNum
        showMessage =  "Exported file successfully!\n\n"   
        showMessage += "Tag scheme: " +self.tagScheme + "\n\n"
        showMessage += "Keep Recom: " +str(self.keepRecommend) + "\n\n"
        showMessage += "Text Seged: " +str(self.seged) + "\n\n"
        showMessage += "Line Number: " + str(lineNum)+ "\n\n"
        showMessage += "Saved to File: " + new_filename
        tkMessageBox.showinfo("Export Message", showMessage)


def getWordTagPairs(tagedSentence, seged=True, tagScheme="BMES", onlyNP=False, entityRe=r'\[\@.*?\#.*?\*\]'):
    newSent = tagedSentence.strip('\n').decode('utf-8')
    filterList = re.findall(entityRe, newSent)
    newSentLength = len(newSent)
    chunk_list = []
    start_pos = 0
    end_pos = 0
    if len(filterList) == 0:
        singleChunkList = []
        singleChunkList.append(newSent)
        singleChunkList.append(0)
        singleChunkList.append(len(newSent))
        singleChunkList.append(False)
        chunk_list.append(singleChunkList)
        # print singleChunkList
        singleChunkList = []
    else:
        for pattern in filterList:
            # print pattern
            singleChunkList = []
            start_pos = end_pos + newSent[end_pos:].find(pattern)
            end_pos = start_pos + len(pattern)
            singleChunkList.append(pattern)
            singleChunkList.append(start_pos)
            singleChunkList.append(end_pos)
            singleChunkList.append(True)
            chunk_list.append(singleChunkList)
            singleChunkList = []
    ## chunk_list format:
    full_list = []
    for idx in range(0, len(chunk_list)):
        if idx == 0:
            if chunk_list[idx][1] > 0:
                full_list.append([newSent[0:chunk_list[idx][1]], 0, chunk_list[idx][1], False])
                full_list.append(chunk_list[idx])
            else:
                full_list.append(chunk_list[idx])
        else:
            if chunk_list[idx][1] == chunk_list[idx-1][2]:
                full_list.append(chunk_list[idx])
            elif chunk_list[idx][1] < chunk_list[idx-1][2]:
                print "ERROR: found pattern has overlap!", chunk_list[idx][1], ' with ', chunk_list[idx-1][2]
            else:
                full_list.append([newSent[chunk_list[idx-1][2]:chunk_list[idx][1]], chunk_list[idx-1][2], chunk_list[idx][1], False])
                full_list.append(chunk_list[idx])

        if idx == len(chunk_list) - 1 :
            if chunk_list[idx][2] > newSentLength:
                print "ERROR: found pattern position larger than sentence length!"
            elif chunk_list[idx][2] < newSentLength:
                full_list.append([newSent[chunk_list[idx][2]:newSentLength], chunk_list[idx][2], newSentLength, False])
            else:
                continue
    return turnFullListToOutputPair(full_list, seged, tagScheme, onlyNP)


def turnFullListToOutputPair(fullList, seged=True, tagScheme="BMES", onlyNP=False):
    pairList = []
    for eachList in fullList:
        if eachList[3]:
            contLabelList = eachList[0].strip('[@$]').rsplit('#', 1)
            if len(contLabelList) != 2:
                print "Error: sentence format error!"
            label = contLabelList[1].strip('*')
            if seged:
                contLabelList[0] = contLabelList[0].split()
            if onlyNP:
                label = "NP"
            outList = outputWithTagScheme(contLabelList[0], label, tagScheme)
            for eachItem in outList:
                pairList.append(eachItem)
        else:
            if seged:
                eachList[0] = eachList[0].split()
            for idx in range(0, len(eachList[0])):
                basicContent = eachList[0][idx]
                if basicContent == ' ': 
                    continue
                pair = basicContent + ' ' + 'O\n'
                pairList.append(pair.encode('utf-8'))
    return pairList


def outputWithTagScheme(input_list, label, tagScheme="BMES"):
    output_list = []
    list_length = len(input_list)
    if tagScheme=="BMES":
        if list_length ==1:
            pair = input_list[0]+ ' ' + 'S-' + label + '\n'
            output_list.append(pair.encode('utf-8'))
        else:
            for idx in range(list_length):
                if idx == 0:
                    pair = input_list[idx]+ ' ' + 'B-' + label + '\n'
                elif idx == list_length -1:
                    pair = input_list[idx]+ ' ' + 'E-' + label + '\n'
                else:
                    pair = input_list[idx]+ ' ' + 'M-' + label + '\n'
                output_list.append(pair.encode('utf-8'))
    else:
        for idx in range(list_length):
            if idx == 0:
                pair = input_list[idx]+ ' ' + 'B-' + label + '\n'
            else:
                pair = input_list[idx]+ ' ' + 'I-' + label + '\n'
            output_list.append(pair.encode('utf-8'))
    return output_list


def removeRecommendContent(content, recommendRe = r'\[\$.*?\#.*?\*\](?!\#)'):
    output_content = ""
    last_match_end = 0
    for match in re.finditer(recommendRe, content):
        matched =content[match.span()[0]:match.span()[1]]
        words = matched.strip('[$]').split("#")[0]
        output_content += content[last_match_end:match.span()[0]] + words
        last_match_end = match.span()[1]
    output_content += content[last_match_end:]
    return output_content

def decompositCommand(command_string):
    command_list = []
    each_command = []
    num_select = ''
    for idx in range(0, len(command_string)):
        if command_string[idx].isdigit():
            num_select += command_string[idx]
        else:
            each_command.append(num_select)
            each_command.append(command_string[idx])
            command_list.append(each_command)
            each_command = []
            num_select =''
    # print command_list
    return command_list

#main function for the annotation
def main():
    print("Annotator launched!")
    print(("OS:%s")%(platform.system()))
    root = Tk()
    root.geometry("1300x700+200+200")
    app = TopicSegmentationAnnotator(root)
    app.setFont(17)
    root.mainloop()  

if __name__ == '__main__':
    main()
