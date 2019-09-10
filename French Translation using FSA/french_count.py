import sys
from fst import FST
from fsmutils import composewords

kFRENCH_TRANS = {0: "zero", 1: "un", 2: "deux", 3: "trois", 4:
                 "quatre", 5: "cinq", 6: "six", 7: "sept", 8: "huit",
                 9: "neuf", 10: "dix", 11: "onze", 12: "douze", 13:
                 "treize", 14: "quatorze", 15: "quinze", 16: "seize",
                 20: "vingt", 30: "trente", 40: "quarante", 50:
                 "cinquante", 60: "soixante", 100: "cent"}

kFRENCH_AND = 'et'

group2_9=[2,3,4,5,6,7,8,9]
group2_6=[2,3,4,5,6]
group1_6=[1,2,3,4,5,6]
group1_9=[1,2,3,4,5,6,7,8,9]
group7_9=[7,8,9]

def prepare_input(integer):
    assert isinstance(integer, int) and integer < 1000 and integer >= 0, \
      "Integer out of bounds"
    return list("%03i" % integer)

def french_count():
    f = FST('french')

    f.add_state('1')
    f.add_state('2')
    f.add_state('3')
    f.add_state('4')
    f.add_state('5')
    f.add_state('6')
    f.add_state('7')
    f.add_state('8')
    f.add_state('9')
    f.add_state('10')
    f.add_state('11')
    f.add_state('12')
    f.add_state('13')
    f.add_state('14')
    f.add_state('15')
    
    f.initial_state = '1'

    for ii in xrange(10):
        if ii in group2_9:
            f.add_arc('1', '2', [str(ii)], [kFRENCH_TRANS[ii]+" cent"])
            f.add_arc('3', '7', [str(ii)], [kFRENCH_TRANS[ii]])        
        if ii in group2_6:
            f.add_arc('2', '3', [str(ii)], [kFRENCH_TRANS[ii*10]])
            f.add_arc('15', '3', [str(ii)], [kFRENCH_TRANS[ii*10]])
            
            
        if ii in group1_6:
            f.add_arc('4', '5', [str(ii)], [kFRENCH_TRANS[ii+10]])
            f.add_arc('11', '12', [str(ii)], [kFRENCH_TRANS[ii+10]])
        if ii in group7_9:
            f.add_arc('4', '6', [str(ii)], ["dix " + kFRENCH_TRANS[ii]])
            f.add_arc('11', '12', [str(ii)], ["dix " + kFRENCH_TRANS[ii]]) 
            if ii == 9:
                f.add_arc('2', '4', [str(ii)], ["quatre vingt"])
                f.add_arc('15', '4', [str(ii)], ["quatre vingt"])
                
                
        if ii in group1_9:
            f.add_arc('9', '10', [str(ii)], [kFRENCH_TRANS[ii]])
            f.add_arc('13', '14', [str(ii)], [kFRENCH_TRANS[ii]])       
        
        if ii==8:
            f.add_arc('2', '9', [str(ii)], ["quatre vingt"])
            f.add_arc('15', '9', [str(ii)], ["quatre vingt"])
            
        if ii==7:
            f.add_arc('2', '11', [str(ii)], ["soixante"])
            f.add_arc('15', '11', [str(ii)], ["soixante"])
            
        if ii==1:
            f.add_arc('1', '2', [str(ii)], ["cent"])
            f.add_arc('2', '4', [str(ii)], ())
            f.add_arc('15', '4', [str(ii)], ())
            f.add_arc('3', '8', [str(ii)], ["et un"])  
            f.add_arc('11', '12', [str(ii)], ["et onze"])   
        if ii==0:
            f.add_arc('1', '15', [str(ii)], ())
            f.add_arc('15', '13', [str(ii)], ())
            f.add_arc('3', '7', [str(ii)], ())
            f.add_arc('2', '9', [str(ii)], ())
            f.add_arc('9', '10', [str(ii)], ())
            f.add_arc('4', '5', [str(ii)], ["dix"])
            f.add_arc('11', '12', [str(ii)], ["dix"])
            f.add_arc('13', '14', [str(ii)], [kFRENCH_TRANS[ii]])
            
            
        
    f.set_final('5')
    f.set_final('6')
    f.set_final('7')
    f.set_final('8')
    f.set_final('9')
    f.set_final('10')
    f.set_final('12')
    f.set_final('14')

    return f

if __name__ == '__main__':
    string_input = raw_input()
    user_input = int(string_input)
    f = french_count()
    if string_input:
        print user_input, '-->',
        print " ".join(f.transduce(prepare_input(user_input)))
    
    #for l in range(0,1000):
        #print str(f.transduce(prepare_input(l)))
        
