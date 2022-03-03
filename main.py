from webbot import Browser
from time import sleep
import itertools

web = Browser()

web.go_to('https://rsk0315.github.io/playground/passwordle.html')

driver = web.driver

HASH_MAP_present = set([])
HASH_MAP_correct = {}

def submit_word(word):

    print("submit:", word)
    web.type(word, id='input')
    web.click("enter")

def hash_word(word):

    web.execute_script("k=0;hash('" + word + "').then(val=> {k = val})")

    ans = web.execute_script("return k")
    while ans == {} or ans == "{}":
        ans = web.execute_script("return k")
        sleep(0.001)

    return ans

def readout_values(row):

    # value = web.find_elements(id="attempt"+str(row))[0].get_attribute('innerHTML')

    s = driver.find_element_by_id("attempt-"+str(row))
    return [i.split("\">")[0] for i in driver.execute_script("return arguments[0].innerHTML;",s).split("tile tile-")[1:]]

def get_latest_readout():

    for i in range(9, -1, -1):

        r = readout_values(i)
        if r[0] != 'empty': return r

    return None

def get_char_map(hash):

    idx=-1
    for i in get_latest_readout():
        idx+=1

        if i == 'correct':
            HASH_MAP_correct[idx] = hash[idx]

        elif i == 'present':

            HASH_MAP_present.add(hash[idx])

def try_word(word):
    hash = hash_word(word)
    submit_word(word)
    get_char_map(hash)

sleep(1)

try_word("passwordlesolver")

print(HASH_MAP_correct)
print(HASH_MAP_present)

letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
digits = '0123456789';
punctuation = '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~';
# let s = letters.repeat(7) + digits.repeat(4) + punctuation.repeat(3);
# let length = 14;
# let res = Array.from({length}, (() => s[randomInt(s.length)])).join('');

for string in map(''.join, itertools.product(letters+digits+punctuation, repeat=14)):
    # if sum({i in string for i in letters})>7: pass
    # if sum({i in string for i in digits})>4: pass
    # if sum({i in string for i in digits})>3: pass

    print(string, end="\r")

    hash = hash_word(string.replace("\\", "\\\\").replace("\'", "\\'"))
    valid = True

    for match_loc in HASH_MAP_correct.keys():
        if hash[match_loc] != HASH_MAP_correct[match_loc]:
            valid = False
            break

    if valid:
        for character in HASH_MAP_present:
            if character not in hash:
                valid = False
                break

    if valid:
        try_word(string)
