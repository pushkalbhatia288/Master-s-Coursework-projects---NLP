#!/usr/bin/env python
import argparse
import sys
import codecs
if sys.version_info[0] == 2:
  from itertools import izip
else:
  izip = zip
from collections import defaultdict as dd
import re
import os.path
import gzip
import tempfile
import shutil
import atexit

# Use word_tokenize to split raw text into words
from string import punctuation

import nltk
from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer

scriptdir = os.path.dirname(os.path.abspath(__file__))

reader = codecs.getreader('utf8')
writer = codecs.getwriter('utf8')

def prepfile(fh, code):
  if type(fh) is str:
    fh = open(fh, code)
  ret = gzip.open(fh.name, code if code.endswith("t") else code+"t") if fh.name.endswith(".gz") else fh
  if sys.version_info[0] == 2:
    if code.startswith('r'):
      ret = reader(fh)
    elif code.startswith('w'):
      ret = writer(fh)
    else:
      sys.stderr.write("I didn't understand code "+code+"\n")
      sys.exit(1)
  return ret

def addonoffarg(parser, arg, dest=None, default=True, help="TODO"):
  ''' add the switches --arg and --no-arg that set parser.arg to true/false, respectively'''
  group = parser.add_mutually_exclusive_group()
  dest = arg if dest is None else dest
  group.add_argument('--%s' % arg, dest=dest, action='store_true', default=default, help=help)
  group.add_argument('--no-%s' % arg, dest=dest, action='store_false', default=default, help="See --%s" % arg)



class LimerickDetector:

    def __init__(self):
        """
        Initializes the object to have a pronunciation dictionary available
        """
        #print "text"
        self._pronunciations = nltk.corpus.cmudict.dict()
    

    def num_syllables(self, word):
        """
        Returns the number of syllables in a word.  If there's more than one
        pronunciation, take the shorter one.  If there is no entry in the
        dictionary, return 1.
        """
        
        
        if word not in self._pronunciations:
            #print word,
            return 1
        check=0
        check1=[]
        a = self._pronunciations[word]
        
        #print a        
        #print word
        for count in range(0,len(a)):
            for x in a[count]:
                for x1 in x:
                    #print x1, "x1"
                    if x1.isdigit():
                        #print "appended"
                        check+=1
            check1.append(check)
            check=0        
    
        #print check1
        #print min(check1)
            
            
            
            
        # TODO: provide an implementation!

        return min(check1)
        
    def apostrophe_tokenize(self, li):
        
        li=li.lower()
        lis=[]
        li=li.strip()
        str1=""
        for x in li:
            if x != ' ':
                str1+=x
            else:
                lis.append(str1)
                str1=""
        lis.append(str1)        
        #print lis
        return lis
    
        
    def guess_syllables(self, wordtest):
        
        wordtest=wordtest.lower()
        syllable=0
        vowelset='aeiouy'
        vowelset1='aeiou'
        tempstr=""
        #print len(wordtest)
        if len(wordtest)<=3:
                return 1
        
        if wordtest[0] in vowelset:
                #print "Increased", wordtest[0]
                syllable+=1
        for x in range(1, len(wordtest)):
                if wordtest[x] in vowelset and wordtest[x-1] not in vowelset:
                    #print "Increased", wordtest[x]
                    syllable+=1
        
        if wordtest.endswith("fully") or (wordtest.endswith("ue") and wordtest[len(wordtest)-3] not in vowelset) :
                    if wordtest == "fully":
                        return 2
                    else:
                        #print wordtest[len(wordtest)-3] 
                        syllable-=1
                    
        
        if wordtest.endswith("e") and wordtest[len(wordtest)-2] != "l":
                if wordtest[len(wordtest)-2] not in vowelset1:
                    syllable-=1
        
                    
        for x in range(1, len(wordtest)-1):
                 if wordtest[x]== "y" and wordtest[x+1] in vowelset1 and wordtest[x-1] in vowelset1:
                    syllable+=1
                    
        if "ia" in wordtest:
                syllable+=1
        
        if wordtest.endswith("ism"):
            syllable+=1
            if wordtest.endswith("uism"):
                syllable+=1    
                
        if wordtest.endswith("ed"):
            syllable-=1       
        
        if wordtest.startswith("natural"):
            syllable-=1
        
        if wordtest.endswith("es"):
                tempstr=wordtest[0:len(wordtest)-2]
                #print tempstr
                if tempstr.endswith("sh") or tempstr.endswith("ph") or tempstr.endswith("ck") or tempstr.endswith("ch") or tempstr.endswith("th") or tempstr.endswith("wh") or tempstr.endswith("ng") or tempstr[len(tempstr)-1]==tempstr[len(tempstr)-2] or tempstr.endswith("l") or tempstr.endswith("x") or tempstr.endswith("z") or tempstr.endswith("c") :
                    syllable=syllable
                else:
                    syllable-=1
   
        
        

        return syllable

    
    def rhymes(self,a,b):
    
        a=a.lower()
        b=b.lower()
        if a not in self._pronunciations or b not in self._pronunciations :
            return False
        
        a1 = self._pronunciations[a]
        b1 = self._pronunciations[b]
        
        
        
        #print a1, "dddddddddddDD"
        #print b1, "ssssssssssSSSSSSS"
        
        astr=""
        bstr=""
        final=0
        flag=0
        
        vow={1:'A', 2:'E', 3:'I', 4:'O' , 5:'U'}
        
        arrA=[]
        arrB=[]
        #print a1
        #print b1
        for outerlis in range(0,len(a1)):
            for elem in range(0,len(a1[outerlis])):
                #print a1[outerlis][elem], "-------------"
                if a1[outerlis][elem][0] not in vow.values():
                    continue
                    
                else:
                    #print "hello", a1[outerlis][elem]
                    for i in range(elem,len(a1[outerlis])):
                        astr = astr + a1[outerlis][i]
                    arrA.append(astr)
                    astr=""
                    #print arrA
                    break
                
         
        for outerlis1 in range(0,len(b1)):
            for elem in range(0,len(b1[outerlis1])):
                #print b1[outerlis1][elem], "-------------"
                if b1[outerlis1][elem][0] not in vow.values():
                    continue
                    
                else:
                    #print "hello", a1[outerlis][elem]
                    for i in range(elem,len(b1[outerlis1])):
                        bstr = bstr + b1[outerlis1][i]
                    arrB.append(bstr)
                    bstr=""
                    #print arrB
                    break
                    
        for astr in arrA:
            for bstr in arrB:
                if (len(bstr)>len(astr)):
                    if bstr.endswith(astr):
                        #print "Rhymes"
                        flag=1
                        return 1
                    else:
                        flag=0
                                
                elif (len(astr)>len(bstr)):
                    if astr.endswith(bstr):
                        #print "Rhymes"
                        flag=1
                        return 1
                    else:
                        flag=0
                                
                else:
                    if astr==bstr:
                        #print "Rhyme"
                        flag=1
                        return 1
                    else:
                        flag=0
       
        if flag==0:
            #print "False"
            return False         
                           


    def is_limerick(self, text):
        text=text.lower()
        text=text.strip()
        
        #tokenizer = RegexpTokenizer(r'[\w\']+')
        
        lisA=[]
        lisB=[]
        
        
        # starts here
        
        syll={}
        # check for rhyme
        eachline = text.splitlines()
        while '' in eachline:
            eachline.remove('')
        
            
        #eachline.remove("")
        #print eachline
        if len(eachline)==5:
            listData = re.sub(r"[^\w\s']",'',eachline[0])
            #print listData
            wor=word_tokenize(listData)
            #print wor
            lisA.append(wor[len(wor)-1])
            listData1 = re.sub(r"[^\w\s']",'',eachline[1])
            wor=word_tokenize(listData1)
            #print wor
            lisA.append(wor[len(wor)-1])
            listData2 = re.sub(r"[^\w\s']",'',eachline[4])
            wor=word_tokenize(listData2)
            #print wor
            lisA.append(wor[len(wor)-1])
            listData3 = re.sub(r"[^\w\s']",'',eachline[2])
            wor=word_tokenize(listData3)
            #print wor
            lisB.append(wor[len(wor)-1])
            listData4 = re.sub(r"[^\w\s']",'',eachline[3])
            wor=word_tokenize(listData4)
            #print wor
            lisB.append(wor[len(wor)-1])    
            #print lisA
            #print lisB
            a1=self.rhymes(lisA[0],lisA[1])
            a2=self.rhymes(lisA[1],lisA[2])
            b1=self.rhymes(lisB[0],lisB[1])
            
            #print a1,a2,b1
            
            sum1=0
            #store syllables
            for x in range(0,len(eachline)):
                listDa = re.sub(r"[^\w\s']",'',eachline[x])
                wor1=word_tokenize(listDa)
                for w in wor1:
                    sum1+=self.num_syllables(w)
                    #print sum1
                if sum1 <4:
                    return False
                else:
                    syll[x]=sum1
                    sum1=0         
            #print syll
            
            if abs(syll[0]-syll[1])<=2 and abs(syll[2]-syll[3])<=2 and abs(syll[0]-syll[4])<=2 and abs(syll[1]-syll[1])<=2 :
                if syll[0]> syll[2] and syll[0]>syll[3] and syll[1]>syll[2] and syll[1]>syll[3] and syll[4]>syll[2] and syll[4]>syll[3]:
                    constraint=1
            
                       
            
            for x in lisA:
                for y in lisB:
                    #print x, y, "---"
                    if self.rhymes(x,y):
                        #print "rhymes"
                        return False
                                           
            if a1 and a2 and b1 and constraint==1 :
                #print lisA, lisB
                return True
        
        return False
        #ends here
          
          
            
        #print self.rhymes("mess","process")
        #print self.num_syllables("graue")
        #print self.guess_syllables("graue")
        
         #FOR APOSTROPHE FUNCTION
       
        '''eachline=text.splitlines()
        while '' in eachline:
            eachline.remove('')
        for abc in range(0,len(eachline)):
            listData = re.sub(r"[^\w\s']",'',eachline[abc])
            wor = self.apostrophe_tokenize(listData)
            print wor   '''        
            
            
        #eachline = text.split('\n')
        #for wor in range(0,len(eachline)-1): 
         #   #print eachline[wor], "yyyyy"
          #  wor=tokenizer.tokenize(eachline[wor])
           # self.num_syllables(wor[len(wor)-1])
            
           
        """
        Takes text where lines are separated by newline characters.  Returns
        True if the text is a limerick, False otherwise.

        A limerick is defined as a poem with the form AABBA, where the A lines
        rhyme with each other, the B lines rhyme with each other, and the A lines do not
        rhyme with the B lines.


        Additionally, the following syllable constraints should be observed:
          * No two A lines should differ in their number of syllables by more than two.
          * The B lines should differ in their number of syllables by no more than two.
          * Each of the B lines should have fewer syllables than each of the A lines.
          * No line should have fewer than 4 syllables

        (English professors may disagree with this definition, but that's what
        we're using here.)


        """
        
        
        # TODO: provide an implementation!
        #return False


# The code below should not need to be modified
def main():
  parser = argparse.ArgumentParser(description="limerick detector. Given a file containing a poem, indicate whether that poem is a limerick or not",
                                   formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  addonoffarg(parser, 'debug', help="debug mode", default=False)
  parser.add_argument("--infile", "-i", nargs='?', type=argparse.FileType('r'), default=sys.stdin, help="input file")
  parser.add_argument("--outfile", "-o", nargs='?', type=argparse.FileType('w'), default=sys.stdout, help="output file")




  try:
    args = parser.parse_args()
  except IOError as msg:
    parser.error(str(msg))

  infile = prepfile(args.infile, 'r')
  outfile = prepfile(args.outfile, 'w')

  ld = LimerickDetector()
  #LimerickDetector.apostrophe_tokenize("I know you Can't")
  lines = ''.join(infile.readlines())
  outfile.write("{}\n-----------\n{}\n".format(lines.strip(), ld.is_limerick(lines)))

if __name__ == '__main__':
  main()
