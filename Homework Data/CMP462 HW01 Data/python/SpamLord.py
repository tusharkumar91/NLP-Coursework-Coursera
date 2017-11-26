import sys
import os
import re
import pprint

my_first_pat1 = '(\w+)@(\w+).edu'

"""
TODO
This function takes in a filename along with the file object (actually
a StringIO object at submission time) and
scans its contents against regex patterns. It returns a list of
(filename, type, value) tuples where type is either an 'e' or a 'p'
for e-mail or phone, and value is the formatted phone number or e-mail.
The canonical formats are:
     (name, 'p', '###-###-#####')
     (name, 'e', 'someone@something')
If the numbers you submit are formatted differently they will not
match the gold answers

NOTE: ***don't change this interface***, as it will be called directly by
the submit script

NOTE: You shouldn't need to worry about this, but just so you know, the
'f' parameter below will be of type StringIO at submission time. So, make
sure you check the StringIO interface if you do anything really tricky,
though StringIO should support most everything.
"""
def process_file(name, f):
    # note that debug info should be printed to stderr
    # sys.stderr.write('[process_file]\tprocessing file: %s\n' % (path))
    resEmail = []
    res = []
    resEmail = process_file_email(name, f)
    f.seek(0,0)
    resPhone = process_file_phone(name, f)
    return resEmail + resPhone;


def process_file_phone(name, f):
    res = []
    for line in f:
        ''' First pattern : (123)123-1234'''
        my_first_pat = '\(([0-9]{3})\)\s*([0-9]{3})-([0-9]{4})'
        matches = re.findall(my_first_pat,line)
        for m in matches:
            phone = '%s-%s-%s' % m
            res.append((name,'p',phone))
        
        
        '''Second Pattern : +1 123-123-1234 or +1 123 123 1234 or +1 123 123-1234'''
        my_second_pat = '(\+1\s*)*([0-9]{3})[\s+-]([0-9]{3})[\s+-]([0-9]{4})'
        matches = re.findall(my_second_pat,line)
        for m in matches:
            phone = '%s-%s-%s' % (m[1], m[2], m[3])
            res.append((name,'p',phone))
    return res

'''
Utility function to encapsulate the processing required for extracting email 
addreses from the input files provided.
There is some hardcoded logic specifically for emails in this section which
should be cleaned up before code push'''
def process_file_email(name, f):
    res = []
    for line in f:
        #Code to replace few special characters with generic email characters
        line = line.replace("-", '')
        line = line.replace("&ldquo;", "'")
        line = line.replace("&rdquo;", "'")
        line = line.replace("&#x40;", '@')
        line = line.replace(" dot " ,".")
        line = line.replace(" dt " ,".")
        #print line

        '''First pattern
        This is for texts of pattern abc.def@stanford.edu'''
        my_first_pat = '(\w+\.)*(\w+)\s*@\s*(\w+)(\.\w+)*.(edu|EDU)'
        matches = re.findall(my_first_pat,line)
        for m in matches:
            email = '%s%s@%s%s.%s' % m
            res.append((name,'e',email))
        
        '''
        Second pattern                                                                                                                                                                                  
        This is for texts of pattern abc.def at stanford edu'''
        my_second_pat = '(\w+\.)*(\w+)\s+at\s+((\w+)\s*[\.;\s]*(\w+))\s*[\.;\s]\s*(edu|EDU|com)\W'
        matches = re.findall(my_second_pat,line)
        for m in matches:
            #print "matched"
            illegalStrFound = False
            for x in m:
                if x == "Server":
                    illegalStrFound = True
            if(not illegalStrFound):
                l2 = m[2].replace(';','.')
                l2 = m[2].replace(' ','.')
                email = '%s%s@%s.%s' % (m[0], m[1], l2, m[5])
                email = email.replace(";", ".")
                res.append((name,'e',email))

        '''
        Third Pattern
        This is for texts of pattern abc WHERE stanford DOM edu'''
        my_third_pat = '(\w+\.)*(\w+)\s*WHERE\s*(\w+)\s*DOM\s*(edu|EDU)'
        matches = re.findall(my_third_pat,line)
        for m in matches:
            email = '%s%s@%s.%s' % m
            res.append((name,'e',email))

        '''
        Fourth Pattern
        For texts of pattern ('stanford.edu' , 'abc.def')'''
        my_fourth_pat = "(\w+)(\.\w+)*.(edu|EDU)','(\w+)(\.\w+)*"
        matches = re.findall(my_fourth_pat,line)
        for m in matches:
            tempEmail = '%s%s.%s@%s%s' % m
            emailSplit = tempEmail.split("@")
            email = "" + emailSplit[1] + "@" + emailSplit[0]
            res.append((name,'e',email))

        
        '''
        Fifth Pattern
        For texts of pattern email me abc followed by @stanford.edu'''
        my_fifth_pat = "(\w+)(\.\w+)* \(followed by \s*[\'\"]@\s*(\w+)(\.\w+)*.(edu|EDU)[\'\"]"
        matches = re.findall(my_fifth_pat,line)
        for m in matches:
            email = '%s%s@%s%s.%s' % m
            res.append((name,'e',email))

    return res

"""
You should not need to edit this function, nor should you alter
its interface as it will be called directly by the submit script
"""
def process_dir(data_path):
    # get candidates
    guess_list = []
    for fname in os.listdir(data_path):
        if fname[0] == '.':
            continue
        path = os.path.join(data_path,fname)
        f = open(path,'r')
        f_guesses = process_file(fname, f)
        guess_list.extend(f_guesses)
    return guess_list

"""
You should not need to edit this function.
Given a path to a tsv file of gold e-mails and phone numbers
this function returns a list of tuples of the canonical form:
(filename, type, value)
"""
def get_gold(gold_path):
    # get gold answers
    gold_list = []
    f_gold = open(gold_path,'r')
    for line in f_gold:
        gold_list.append(tuple(line.strip().split('\t')))
    return gold_list

"""
You should not need to edit this function.
Given a list of guessed contacts and gold contacts, this function
computes the intersection and set differences, to compute the true
positives, false positives and false negatives.  Importantly, it
converts all of the values to lower case before comparing
"""
def score(guess_list, gold_list):
    guess_list = [(fname, _type, value.lower()) for (fname, _type, value) in guess_list]
    gold_list = [(fname, _type, value.lower()) for (fname, _type, value) in gold_list]
    guess_set = set(guess_list)
    gold_set = set(gold_list)

    tp = guess_set.intersection(gold_set)
    fp = guess_set - gold_set
    fn = gold_set - guess_set

    pp = pprint.PrettyPrinter()
    #print 'Guesses (%d): ' % len(guess_set)
    #pp.pprint(guess_set)
    #print 'Gold (%d): ' % len(gold_set)
    #pp.pprint(gold_set)
    print 'True Positives (%d): ' % len(tp)
    pp.pprint(tp)
    print 'False Positives (%d): ' % len(fp)
    pp.pprint(fp)
    print 'False Negatives (%d): ' % len(fn)
    pp.pprint(fn)
    print 'Summary: tp=%d, fp=%d, fn=%d' % (len(tp),len(fp),len(fn))

"""
You should not need to edit this function.
It takes in the string path to the data directory and the
gold file
"""
def main(data_path, gold_path):
    guess_list = process_dir(data_path)
    gold_list =  get_gold(gold_path)
    score(guess_list, gold_list)

"""
commandline interface takes a directory name and gold file.
It then processes each file within that directory and extracts any
matching e-mails or phone numbers and compares them to the gold file
"""
if __name__ == '__main__':
    if (len(sys.argv) == 1):
        main('../data/dev', '../data/devGOLD')
    elif (len(sys.argv) == 3):
        main(sys.argv[1],sys.argv[2])
    else:
        print 'usage:\tSpamLord.py <data_dir> <gold_file>'
        sys.exit(0)
