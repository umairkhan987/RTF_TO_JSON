import copy
import re
import time
import json
from sly import Lexer, Parser
from helpers.utils import get_cleaned_text, page_splitter, check_line_has_valid_text, replace_text

page_split = """89504e470d0a1a0a0000000d4948445200000020000000200806000000737a7a
f400000006624b474400ff00ff00ffa0bda793000000097048597300000ec400
000ec401952b0e1b00000568494441545885c557314c5b57143d9f4f90bdc443
10165608699c30e423d9e5ff35716b4f207b2a911209476a9b566dc764e9501b
dc854c3163159266b3135109069ca55490866cef930c30188704084b486a0914
997c2bf6e9e0ff3f36186318da2bbdc1efbe7feff17bf7bd732e48e298632210
0830100890e4c471e3b4a27993009c01a099e33249cb7719c02800618e7500ac
13637fd0aa208d12ff502c167f5d5a5a6ad7751d4208e8ba0e5dd70100aaaa42
5555689a064dd3a028cabb13274e0c03f8ed5020876c5137c999a9a929badd6e
9ac1e872b9180c06d9d5d5c5aeae2e068341ba5c2edbef76bb39353545927f92
3cd328c7410e89e4b7f97c7e3b1a8d12007d3e1f53a91473b91ccbe5f22ac98d
aa1ad828954aabcbcbcb4ca552f4f97c04c0ebd7af339fcf6f93fcd68cd91400
89e4a34c26438fc7435996198fc76918c63ac94192ed0d8ab09de4a06118ebb1
588cb22cd3e3f1f0f1e3c724f9a81e887a006e64321902a0a228144290e43d92
274d7f1bc9cf498a2a00c29c6b33d7b848de1742f0e2c58b04c04c264373271a
02e8cee7f3db9d9d9d5414858542619364bfe99349de2459a06955002c2b986b
64f39b8142a1f04e51147a3c1eeb386a6aa23a790bc999a1a121cab24c5dd759
95fc02c97992cc66b34c24128c44229c9b9be3dcdc1c239108138904b3d9ac05
649ee4790b841082b22c331a8d9295c294ea01f86972729200188fc7ad6db792
7f28954a4c269374381c76b5cfcece727676d6feed743a393636c652a944921f
aa40dc8fc5620460dd8e1ff702900cc378d7d1d141bfdf4fc330d6cc339749ce
974a25f6f7f7db890e02608d8181010bc4bc19c36518c6bacfe7a3dbed66b158
dcb476c102707661618100984ea7c94ab583e42d924c2693fb92340200806363
63d671dc34630da6522902e0f3e7cfc9ca1b630318bc7bf72e013097cb91e429
b3a20bd96cb666db9b05e0743aad9a2898b1da9797970980e3e3e324f91549b4
980fa2268480cbe582d7eb5d05f00f805e00ce743a8d8f1f3f1ef65cefb39d9d
1d3c7cf810009c001400efbd5eef9acbe5821002a8f0095a014c00b8aceb3a34
4d832449d6dc6700acc5c7b2aa6fc701bc6e6969695555d5e2906f009c97cc7b
8ca74f9fe2f4e9d33877ee5c4d90442251a9d63ae6f7fb01002f5ebca8eb9724
09c3c3c33573af5ebdc2c6c6062e5dba044992ec23f8ff8c9577fcadaaaa0c85
4224f9c69c1324190e87eb16190e2942008c4422d64d1066cc8d6030484dd348
f22dc989160057003c505515420890fc64ce7d0f009aa61dfbcf557dfb1d802b
e572f993aeeb505515007e0770c53a02a1691ab6b6b6b0b2b27216c029008b00
76ae5dbb0687c371e4e40e870357af5e05801d004b00da575656bab7b6b62c60
02006a000076e57e09a00820d6d3d383d1d1d12303b87dfb367a7a7a00e01733
d617d6ada806d0cc53fcecbf788a9b22a33b77ee34242387c3c16432594d4617
9a25238b8eff6a40c7cfc80a1d8f8c8c301c0edb741c0e87393232b2978eade4
7be9788607d0718d20e9ededad27486ef17041728bbb82a4bf50286cee1124dd
d539eb4ab2e9e9695b92993b31ce5a49d6c7fd92ac8fbb92ec24c97b42082a8a
722449668bd2e9e969767676b2b5b595c3c3c356610eb2c2940789d253ac88d2
b5783c6e8b523379d3a2d40271239fcf6f0f0d0d1100fd7e3fd3e9345fbe7cc9
72b9fc9ae49b2a006fcae5f2eb5c2ec7743a6dcbf268346a6dfb8d7ac91b01a8
694c262727d9d1d151d398844221bb31098542073526337bcf7cef68a6356b41
a5354b2c2e2ed6b4660b0b0b0080bebebebdadd9fbb6b636ab352b370ade0c00
7b2d806eec36a75f0702810e0078f2e4c9268007d86d4ed7d064737a94ee9800
56cdf10700af244983a6ef6f003f1f21966dff021f267bea93f4d36300000000
49454e44ae426082"""

EMPTY_FORMATING = r"{*}*\\[^\s']+"
CHAP_14_TABLE = """ <h3>First character</h3><table> <tr> <th>ASA Class</th> <th>Description</th> </tr> <tr> <td>1</td> <td>A normal healthy patient</td> </tr> <tr> <td>2</td> <td>A patient with mild systemic disease </td> </tr> <tr> <td>3</td> <td>Patient with severe systemic disease that limits activity</td> </tr> <tr> <td>4</td> <td>Patient with severe systemic disease that is a constant threat to life</td> </tr> <tr> <td>5</td> <td>A moribund patient who is not expected to survive longer than 24 hours without surgical intervention</td> </tr> <tr> <td>6</td> <td>A declared brain-dead patient whose organs are being removed for donor purposes</td> </tr> <tr> <td>9</td> <td>No documentation of ASA score</td> </tr> </table> <h3>Second character</h3> <table> <tr> <th>Emergency modifier</th> <th>character</th> <th>Description</th> </tr> <tr> <td>E</td> <td>0</td> <td>procedure being performed as an emergency</td> </tr> <tr> <td></td> <td>9</td> <td>nonemergency or not known </td> </tr> </table> <p>Emergency modifier '0' is not valid for use with ASA score 6. </p> """

custom_character = {
    "\\'96": "–",
    "\\'97": "—",
    "\\'f6": "ö",
    "\\'df": "ß",
    "\\'86": "†",
    "\\'2a": "*",
    "\\'92": "’",
    "\\'91": "‘",
    "\\'e9": "é",
    "\\'E9": "é",
    "\\'F6": "ö",
    "\\'FC": "ü",
    "\\'E7": "ç",
    "\\'93": '"',
    "\\'94": '"',
    "\\'F8": "ø",
    "\\uc1\\u8209 ?": "‑",
    "\\uc1\\u61619 ?": "≥",
    "\\uc1\\u8805 ?": "≥",
    "\\uc1\\u61603 ?": "≤",
    "\\uc1\\u61621 ?":"☆",
    "\\uc1\\u61553 ?":"ACS_VALUE_START"
}


class MyLexer(Lexer):
    tokens = {CHAPTER, CHAPTER_TEXT, TOPIC, TOPIC_CHILD, TOPIC_CHILD_LIST, TOPIC_CHILD_LIST_CODE,CHILD_INCLUSION,
              CODE_FIRST, SPECIAL_NOTE, SPECIAL_INCLUSION, TABLE, CHAPTER_NOTE, INCLUDES,EXCLUDES, CODE_ALSO, NOTE,
              INCLUSION
              }
    literals = {}

    @_(r"\\f12\\fs28\\b1.*?CHAPTER.+?(\\f6\\fs32\\b1)")
    def CHAPTER(self, t):
        match = [m for m in re.finditer(r"\\f6\\fs32\\b1", t.value)]
        match = match[0] if match else None
        if match:
            self.index -= (len(t.value) - match.end()) + len(match.group())
            t.value = t.value[:match.start()]
        return self.remove_empty_formating(t)

    @_(r"\\f6\\fs32\\b1\\.+?(\\f12\\fs28\\b1|\\f16\\fs18\\b1|\\f4\\fs18\\b0)")
    def CHAPTER_TEXT(self,t):
        match = [m for m in re.finditer(r"\\f12\\fs28\\b1|\\f16\\fs18\\b1|\\f4\\fs18\\b0", t.value)]
        match = match[0] if match else None
        if match:
            self.index -= (len(t.value) - match.end()) + len(match.group())
            t.value = t.value[:match.start()]
        t = self.check_custom_character(t)
        t = self.remove_empty_formating(t)
        if not t.value:
            return None
        return t

    @_(r"\\f12\\fs28\\b1.+?(\n.+?)*((\\f12\\fs22\\b1)|(\\f16\\fs18\\b1)|(\\f12\\fs19\\b1)|(\\f7\\fs19\\b0)|(\\f4\\fs18\\b0))")
    def INCLUSION(self, t):
        regex = r"(\\f12\\fs22\\b1)|(\\f16\\fs18\\b1)|(\\f12\\fs19\\b1)|(\\f7\\fs19\\b0)|(\\f4\\fs18\\b0)"
        match = [m for m in re.finditer(regex, t.value)]
        match = match[0] if match else None
        if match:
            self.index -= (len(t.value) - match.end()) + len(match.group())
            t.value = t.value[:match.start()]
        t = self.check_custom_character(t)
        t = self.remove_empty_formating(t)
        return t

    @_(r"\\f12\\fs22\\b1.+?(\n.+?)*((\\f12\\fs19\\b1)|(\\f1\\fs18\\b1)|(\\f4\\fs26\\b0)|(\\f12\\fs29\\b1)|(\\f12\\fs2\\b1)|(\\f16\\fs18\\b1)|(\\f7\\fs19\\b0)|(\\f11\\fs18\\b0)|(\\f3\\fs14\\b0)|(\\f4\\fs18\\b0))")
    def TOPIC(self, t):
        regex = r"(\\f12\\fs19\\b1)|(\\f1\\fs18\\b1)|(\\f4\\fs26\\b0)|(\\f12\\fs29\\b1)|(\\f16\\fs18\\b1)|(\\f7\\fs19\\b0)|(\\f11\\fs18\\b0)|(\\f4\\fs18\\b0)"
        match = [m for m in re.finditer(regex, t.value)]
        match = match[0] if match else None
        if match:
            self.index -= (len(t.value) - match.end()) + len(match.group())
            t.value = t.value[:match.start()]
        t = self.check_custom_character(t)
        t = self.remove_empty_formating(t)
        return t if t.value else None

    @_(r"(\\f12\\fs19\\b1.+?(\n.+?)*((\\f7\\fs19\\b0)|(\\f4\\fs18\\b0)|(\\f16\\fs18\\b1)|(\\f11\\fs18\\b0)|(\\f2\\fs18\\b1)))|(\\f12\\fs19\\b1.+[\d]+\\tab.+)")
    def TOPIC_CHILD(self, t):
        t.value = self.remove_extra_substring(r"\\f1\\fs18.+?(\\tab\s|\\par\\)", t.value)
        regex = r"(\\f7\\fs19\\b0)|(\\f4\\fs18\\b0)|(\\f16\\fs18\\b1)|(\\f11\\fs18\\b0)|(\\f11\\fs18\\b0)|(\\f2\\fs18\\b1)"
        match = [m for m in re.finditer(regex, t.value)]
        match = match[0] if match else None
        if match:
            self.index -= (len(t.value) - match.end()) + len(match.group())
            t.value = t.value[:match.start()]
        t = self.check_custom_character(t)
        t = self.remove_empty_formating(t)
        return t

    @_(r"\\f7\\fs19\\b0\\[a-z0-9]+\\cf2\s[0-9-]+\\cell")
    def TOPIC_CHILD_LIST_CODE(self, t):
        t = self.remove_empty_formating(t)
        return t

    @_(r"((\\f7\\fs19\\b0\\|[\d]{5}-[\d]{2}).+?(\n.+?)*((\\f4\\fs18\\b0)|(\\f16\\fs18\\b1)|(\\f12\\fs19\\b1)|(\\f11\\fs18\\b0\\i1)|(\\f7\\fs19[^\s]+\s[\d]{5}-([\d]{2}|XX))|(\\f7\\fs20\\b0)|(\\f12\\fs22\\b1)|(\\f7\\fs14\\b0)|(\\f7\\fs13\\b0)|(\\f12\\fs28\\b1)|(\\f7\\fs22\\b0)|(\\f4\\fs6\\b0)|(\\f3\\fs14\\b0)|(\\f7\\fs19[^\s]+\s-[\d]{2})))")
    def TOPIC_CHILD_LIST(self, t):
        t.value = self.remove_extra_substring(r"\\f1\\fs18.+?(\\tab|\\par|\\cell}|\n)", t.value)
        if t.value.startswith("\\f7"):
            t.value = t.value[len("\\f7"):]
        regex = r"(\\f7\\fs19[^\s]+\s[\d]{5}-([\d]{2}|XX))|(\\f4\\fs18\\b0)|(\\f16\\fs18\\b1)|(\\f12\\fs19\\b1)|(\\f11\\fs18\\b0\\i1)|(\\f7\\fs20\\b0)|(\\f12\\fs22\\b1)|(\\f7\\fs14\\b0)|(\\f7\\fs13\\b0)|(\\f12\\fs28\\b1)|(\\f4\\fs6\\b0)|(\\f3\\fs14\\b0)|(\\f7\\fs19[^\s]+\s-[\d]{2})"
        match = [m for m in re.finditer(regex, t.value)]
        match = match[0] if match else None
        if match:
            self.index -= (len(t.value) - match.end()) + len(match.group())
            t.value = t.value[:match.start()]
        t = self.check_custom_character(t)
        t = self.split_multiple_list(t)
        t = self.remove_empty_formating(t)
        return t if t.value else None

    @_(r"(\\f16\\fs18\\b1\\i1[^\s]*\sIncludes:.+?(\n.+?)*((\\f11\\fs18\\b0)|(\\f16\\fs18\\b1)|(\\f7\\fs19\\b0)|(\\f12\\fs19\\b1)|(\\f4\\fs16\\b0)|(\\f12\\fs22\\b1)|(\\f4\\fs20\\b0)|(\\f4\\fs26\\b0)|(\\f2\\fs18\\b1)|(\\f3\\fs14\\b0)|(\\f12\\fs28\\b1)))")
    def INCLUDES(self, t):
        t.value = self.remove_extra_substring(r"\\f1\\fs18.+?((\\tab)|(\\par\\pard)|(\\cell)|\n|\\column)", t.value)
        t.value = t.value[len("\\f16"):]
        regex = r"(\\f11\\fs18\\b0)|(\\f16\\fs18\\b1)|(\\f7\\fs19\\b0)|(\\f12\\fs19\\b1)|(\\f4\\fs16\\b0)|(\\f12\\fs22\\b1)|(\\f4\\fs20\\b0)|(\\f4\\fs26\\b0)|(\\f2\\fs18\\b1)|(\\f12\\fs28\\b1)"
        match = [m for m in re.finditer(regex, t.value)]
        match = match[0] if match else None
        if match:
            self.index -= (len(t.value) - match.end()) + len(match.group())
            t.value = t.value[:match.start()]
        t = self.check_custom_character(t)
        t.value = t.value.replace("Includes:", "", 1)
        t = self.convert_list_to_html(t)
        t = self.remove_empty_formating(t)
        return t

    @_(r"<table>.+?<\/table>")
    def TABLE(self, t):
        return t

    @_(r"\\f16\\fs18\\b1.+Note:.+?REDUCTION.+?(\n.+?)+\\f12\\fs28\\b1")
    def CHAPTER_NOTE(self, t):
        regex = r"\\f12\\fs28\\b1"
        match = [m for m in re.finditer(regex, t.value)]
        match = match[0] if match else None
        if match:
            self.index -= (len(t.value) - match.end()) + len(match.group())
            t.value = t.value[:match.start()]
        t = self.check_custom_character(t)
        t = self.remove_empty_formating(t)
        t.value = t.value.replace("Note:", "", 1).strip()
        return t


    @_(r"\\f16\\fs18\\b1.+Note.+Australian Classification.+(\n.+)*tooth\)\.\\par|\\f5\\fs18\\b1.+assigned.\\par|\\f16\\fs18\\b1.+Note:.+assigned.\\par")
    def SPECIAL_NOTE(self, t):
        t = self.check_custom_character(t)
        t = self.remove_empty_formating(t)
        t.value = t.value.replace("Note:", "", 1).strip()
        return t

    @_(r"\\f16\\fs18\\b1[^\s]*\sNote:.+?(\n.+?)*(\\f7\\fs19\\b0|\\f12\\fs19\\b1|\\f1\\fs18\\b1|\\f12\\fs22\\b1|\\f3\\fs14\\b0|\\f11\\fs18\\b0\\i1\\cf2\sCode\salso|\\f11\\fs18\\b0\\i1\\cf2\sCode\sfirst|\\f12\\fs28\\b1)")
    def NOTE(self, t):
        t.value = self.remove_extra_substring(r"\\f1\\fs18.+?((\\tab)|(\\par\\pard)|(\\cell))", t.value)
        t.value = t.value[len("\\f16"):]
        match = [m for m in re.finditer(r"\\f7\\fs19\\b0|\\f12\\fs19\\b1|\\f16\\fs18\\b1|\\f12\\fs22\\b1|\\f11\\fs18\\b0\\i1\\cf2\sCode\salso|\\f11\\fs18\\b0\\i1\\cf2\sCode\sfirst|\\f12\\fs28\\b1|<table>", t.value)]
        match = match[0] if match else None
        if match:
            self.index -= (len(t.value) - match.end()) + len(match.group())
            t.value = t.value[:match.start()]
        t = self.check_custom_character(t)
        t = self.convert_list_to_html(t)
        t = self.remove_empty_formating(t)
        t.value = t.value.replace("Note:", "", 1).strip()
        return t

    @_(r"\\f11\\fs18\\b0\\i1[^\s]*\s(C|c)ode\sfirst.+?(\n.+?)*(\\f18\\fs18\\b1\\i1|\\f4\\fs20\\b0|\\f7\\fs19\\b0|\\f16\\fs18\\b1|\\f12\\fs22\\b1|\\f12\\fs19\\b1|\\f4\\fs22\\b0|\\f12\\fs28\\b1)")
    def CODE_FIRST(self, t):
        regex = r"\\f18\\fs18\\b1\\i1|\\f4\\fs20\\b0|\\f7\\fs19\\b0|\\f16\\fs18\\b1|\\f12\\fs22\\b1|\\f12\\fs19\\b1|\\f12\\fs28\\b1"
        match = [m for m in re.finditer(regex, t.value)]
        match = match[0] if match else None
        if match:
            self.index -= (len(t.value) - match.end()) + len(match.group())
            t.value = t.value[:match.start()]
        t = self.check_custom_character(t)
        t = self.convert_list_to_html(t)
        t = self.remove_empty_formating(t)
        return t


    @_(r"\\f11\\fs18\\b0\\i1[^\s]*\s(C|c)ode.+?also.+?(\n.+?)*(\\f18\\fs18\\b1\\i1|\\f4\\fs20\\b0|\\f7\\fs19\\b0|\\f16\\fs18\\b1|\\f12\\fs22\\b1|\\f12\\fs19\\b1|\\f4\\fs22\\b0|\\f12\\fs28\\b1|\\f11\\fs18\\b0\\i1\\cf2\sCode\sfirst|\\f11\\fs18\\b0\\i1\\cf2\sCode\salso)")
    def CODE_ALSO(self, t):
        t.value = self.remove_extra_substring(r"\\f1\\fs18.+?((\\tab)|(\\par\\pard)|(\\cell))", t.value)
        t.value = t.value[len("\\f11"):]
        regex = r"\\f18\\fs18\\b1\\i1|\\f4\\fs20\\b0|\\f7\\fs19\\b0|\\f16\\fs18\\b1|\\f12\\fs22\\b1|\\f12\\fs19\\b1|\\f12\\fs28\\b1|\\f11\\fs18\\b0\\i1\\cf2\sCode\sfirst|\\f11\\fs18\\b0\\i1\\cf2\sCode\salso"
        match = [m for m in re.finditer(regex, t.value)]
        match = match[0] if match else None
        if match:
            self.index -= (len(t.value) - match.end()) + len(match.group())
            t.value = t.value[:match.start()]
        t = self.check_custom_character(t)
        t = self.convert_list_to_html(t)
        t = self.remove_empty_formating(t)
        return t


    @_(r"(\\f16\\fs18\\b1\\i1[^\s]*\sExcludes:.+?(\n.+?)*((\\f7\\fs19\\b0)|(\\f12\\fs22\\b1)|(\\f12\\fs19\\b1)|(\\f4\\fs16\\b0)|(\\f4\\fs20\\b0)|(\\f4\\fs12\\b0)|(\\f4\\fs23\\b0)|(\\f3\\fs14\\b0)|(\\f16\\fs18\\b1[^'s]*\sNote:)))|(\\f16\\fs18\\b1\\i1[^\s]+\sExcludes:.+\n)")
    def EXCLUDES(self, t):
        t.value = self.remove_extra_substring(r"\\f2\\fs18.+?(\\par)|\\f1\\fs18.+?(\\tab|\\par|\\cell}|\n)", t.value)
        t.value = t.value[len("\\f16"):]
        regex = r"(\\f7\\fs19\\b0)|(\\f12\\fs22\\b1)|(\\f12\\fs19\\b1)|(\\f4\\fs16\\b0)|(\\f4\\fs20\\b0)|(\\f4\\fs12\\b0)|(\\f12\\fs28\\b1)|(\\f16\\fs18\\b1[^'s]*\sNote:)"
        match = [m for m in re.finditer(regex, t.value)]
        match = match[0] if match else None
        if match:
            self.index -= (len(t.value) - match.end()) + len(match.group())
            t.value = t.value[:match.start()]
        t = self.check_custom_character(t)
        t.value = t.value.replace("Excludes:", "", 1)
        t = self.convert_list_to_html(t)
        t = self.remove_empty_formating(t)
        return t

    @_(r"\\f4\\fs18\\b0.+therapy\).\\par")
    def SPECIAL_INCLUSION(self, t):
        t = self.check_custom_character(t)
        t = self.convert_list_to_html(t)
        t = self.remove_empty_formating(t)
        return t if t.value else None


    @_(r"(\\f4\\fs18\\b0.+?(\n.+?)*((\\f11\\fs18\\b0\\i1\\cf2\sCode\s(also|first))|(\\f16\\fs18\\b1)|(\\f7\\fs19\\b0)|(\\f12\\fs19\\b1)|(\\f4\\fs20\\b0)|(\\f12\\fs22\\b1)|(\\f12\\fs28\\b1)|(\\f3\\fs14\\b0)|(\\f4\\fs32\\b0)|(\\f11\\fs18\\b0)))")
    def CHILD_INCLUSION(self, t):
        t.value = self.remove_extra_substring(r"\\f1\\fs18.+?(\\tab\s|\\column|\\cell|\n|\\par)", t.value)
        regex = r"(\\f11\\fs18\\b0\\i1\\cf2\sCode\s(also|first))|(\\f16\\fs18\\b1)|(\\f7\\fs19\\b0)|(\\f12\\fs19\\b1)|(\\f4\\fs20\\b0)|(\\f12\\fs22\\b1)|(\\f4\\fs26\\b0)|(\\f12\\fs28\\b1)|(\\f11\\fs18\\b0)"
        match = [m for m in re.finditer(regex, t.value)]
        match = match[0] if match else None
        if match:
            self.index -= (len(t.value) - match.end()) + len(match.group())
            t.value = t.value[:match.start()]
        t = self.check_custom_character(t)
        t = self.convert_list_to_html(t)
        t = self.remove_empty_formating(t)
        return t if t.value else None


    @_(r"\\.+?(cf4|tx3368|tx3934|\\f[0-9]{2}|\\f[0-9]|\\fs17|\\par|[A-Z][0-9]{1,}|\\expnd0)", )
    def IGNORING(self, t):
        x = re.search(r'[A-Z][0-9]{1,}$', t.value)
        if x:
            self.index-= len(x.group())
        elif re.search(r'\\tx3368$|\\tx3934$', t.value):
            self.index -= len("\\tx3368")
        elif re.search(r'\\f[0-9]{2}$', t.value):
            self.index -= len("\\f31")
        elif re.search(r'\\f[0-9]$', t.value):
            self.index -= len("\\f3")
        elif t.value.endswith("\\fs17"):
            self.index -= len("\\fs17")
        elif t.value.endswith("\\expnd0"):
            self.index-=len("\\expnd0")
        elif t.value.endswith("\\par"):
            self.index -= len("\\par")
        elif t.value.endswith("\\cf4"):
            self.index -= len("\\cf4")

        return None

    def check_custom_character(self, t):
        for key, value in custom_character.items():
            if key in t.value:
                t.value = t.value.replace(key, value)
        return t

    def remove_empty_formating(self, t):
        t.lineno = self.index
        t.value = re.sub(EMPTY_FORMATING, "", t.value)
        t.value = t.value.replace("\n"," ")
        t.value = t.value.replace("{", " ")
        t.value = t.value.strip()
        return t

    def remove_extra_substring(self, regex, text):
        match = list(filter(None, re.split(regex, text)))
        return "".join(match)

    def split_multiple_list(self, t):
        match = [m for m in re.finditer(r"[\d]{5}-[\d]{2}", t.value)]
        match = match[1] if len(match) > 1 else None
        if match:
            self.index -= (len(t.value) - match.end()) + len(match.group()) + 5
            t.value = t.value[:match.start()]
        return t

    def error(self, t):
        self.index += 1

    def convert_list_to_html(self, t):
        value = re.split(r"\\ls[0-9]*|\\'95", t.value)
        first = value.pop(0)
        new_value = ""
        for index, v in enumerate(value):
            # if not '\n' in v:
            if index == 0:
                new_value += " <ul>"
            new_value += f"<li> {v} </li>"
            if len(value) == index + 1:
                new_value += "</ul> "
        t.value = first + new_value
        return t


class MyParser(Parser):
    tokens = MyLexer.tokens

    def __init__(self, variables: dict = None):
        self.variables = variables or {}
        self.stack = []
        self.children_sample_json = {"text": "", "inclusionTerm": [], "includes": [], "excludes": [], "CodeAlso": [],
                                     "CodeFirst": [], "CodeAdditional": [], "notes": [], "children": []}

    @property
    def last_item_on_stack(self):
        return self.stack

    @_('CHAPTER CHAPTER_TEXT')
    def expr(self, p):
        self.stack.append({'Chapter': p[0], 'text': p[1]})
        return p[0]

    @_('CHAPTER CHAPTER_TEXT SPECIAL_NOTE')
    def expr(self, p):
        self.stack.append({'Chapter': p[0], 'text': p[1], "notes": [p[2]], "children": [{}]})
        return p[0]

    @_('CHAPTER CHAPTER_TEXT CHAPTER_NOTE')
    def expr(self, p):
        self.stack.append({'Chapter': p[0], 'text': p[1], "notes": [p[2]]})
        return p[0]

    @_('CHAPTER CHAPTER_TEXT SPECIAL_INCLUSION NOTE EXCLUDES')
    def expr(self, p):
        self.stack.append({'Chapter': p[0], 'text': p[1], "inclusionTerm": [p[2]], "notes": [p[3]], "excludes": [p[4]]})
        return p[0]

    @_("INCLUSION")
    def expr(self, p):
        data = self.handle_block_start(p)
        self.stack.append(data)
        return p[0]

    @_("INCLUSION CHILD_INCLUSION")
    def expr(self, p):
        data = self.handle_block_start(p, extra={"inclusionTerm": [p[1]]})
        self.stack.append(data)
        return p[0]

    @_("INCLUSION INCLUDES")
    def expr(self, p):
        data = self.handle_block_start(p, extra={"includes": [p[1]]})
        self.stack.append(data)
        return p[0]

    @_("INCLUSION EXCLUDES")
    def expr(self, p):
        data = self.handle_block_start(p, extra={"excludes": [p[1]]})
        self.stack.append(data)
        return p[0]

    @_("INCLUSION NOTE")
    def expr(self, p):
        data = self.handle_block_start(p, extra={"notes": [p[1]]})
        self.stack.append(data)
        return p[0]

    @_("INCLUSION note_exclude")
    def expr(self, p):
        data = self.handle_block_start(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_("INCLUSION include_exclude")
    def expr(self, p):
        data = self.handle_block_start(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_("INCLUSION inclusion_include_exclude")
    def expr(self, p):
        data = self.handle_block_start(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC')
    def expr(self, p):
        data = self.handle_topics(p)
        self.stack.append(data)
        return p[0]

    @_('TOPIC CHILD_INCLUSION')
    def expr(self, p):
        data = self.handle_topics(p, extra={"inclusionTerm": [p[1]]})
        self.stack.append(data)
        return p[0]

    @_('TOPIC EXCLUDES')
    def expr(self, p):
        data = self.handle_topics(p, extra={"excludes": [p[1]]})
        self.stack.append(data)
        return p[0]

    @_('TOPIC INCLUDES')
    def expr(self, p):
        data = self.handle_topics(p, extra={"includes": [p[1]]})
        self.stack.append(data)
        return p[0]

    @_('TOPIC SPECIAL_NOTE EXCLUDES')
    def expr(self, p):
        child = {"notes": [p[1], CHAP_14_TABLE], "excludes": [p[2]]}
        data = self.handle_topics(p, extra=child)
        self.stack.append(data)
        return p[0]

    @_('TOPIC NOTE')
    def expr(self, p):
        data = self.handle_topics(p, extra={"notes": [p[1]]})
        self.stack.append(data)
        return p[0]

    @_('TOPIC include_code_also')
    def expr(self, p):
        data = self.handle_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC include_exclude')
    def expr(self, p):
        data = self.handle_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC note_code_also')
    def expr(self, p):
        data = self.handle_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC inclusion_include_exclude')
    def expr(self, p):
        data = self.handle_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC inclusion_include_note_exclude')
    def expr(self, p):
        data = self.handle_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD')
    def expr(self, p):
        data = self.handle_child_topics(p)
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD CHILD_INCLUSION')
    def expr(self, p):
        data = self.handle_child_topics(p, extra={"inclusionTerm": [p[1]]})
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD EXCLUDES')
    def expr(self, p):
        data = self.handle_child_topics(p, extra={"excludes": [p[1]]})
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD INCLUDES')
    def expr(self, p):
        data = self.handle_child_topics(p, extra={"includes": [p[1]]})
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD NOTE')
    def expr(self, p):
        data = self.handle_child_topics(p, extra={"notes": [p[1]]})
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD CODE_ALSO')
    def expr(self, p):
        data = self.handle_child_topics(p, extra={"CodeAlso": [p[1]]})
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD CODE_FIRST')
    def expr(self, p):
        data = self.handle_child_topics(p, extra={"CodeFirst": [p[1]]})
        self.stack.append(data)
        return p[0]

    @_("TOPIC_CHILD SPECIAL_NOTE")
    def expr(self, p):
        data = self.handle_child_topics(p)
        child = data['children'][-1]
        child = child['children'][-1]
        child = child['children'][-1]
        child["notes"] = [p[1], CHAP_14_TABLE]
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD include_exclude')
    def expr(self, p):
        data = self.handle_child_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD inclusion_include')
    def expr(self, p):
        data = self.handle_child_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD inclusion_exclude')
    def expr(self, p):
        data = self.handle_child_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD inclusion_note')
    def expr(self, p):
        data = self.handle_child_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD include_note')
    def expr(self, p):
        data = self.handle_child_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD note_table')
    def expr(self, p):
        data = self.handle_child_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD note_exclude')
    def expr(self, p):
        data = self.handle_child_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD code_first_exclude')
    def expr(self, p):
        data = self.handle_child_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD include_code_also')
    def expr(self, p):
        data = self.handle_child_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD inclusion_code_also')
    def expr(self, p):
        data = self.handle_child_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD exclude_code_also')
    def expr(self, p):
        data = self.handle_child_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD code_also_exclude')
    def expr(self, p):
        data = self.handle_child_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD note_code_also')
    def expr(self, p):
        data = self.handle_child_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD inclusion_exclude_note')
    def expr(self, p):
        data = self.handle_child_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD inclusion_code_exclude')
    def expr(self, p):
        data = self.handle_child_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD code_also_code_first_exclude')
    def expr(self, p):
        data = self.handle_child_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD include_code_also_exclude')
    def expr(self, p):
        data = self.handle_child_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD note_code_also_exclude')
    def expr(self, p):
        data = self.handle_child_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD include_note_exclude')
    def expr(self, p):
        data = self.handle_child_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD include_note_code_also')
    def expr(self, p):
        data = self.handle_child_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD inclusion_note_exclude')
    def expr(self, p):
        data = self.handle_child_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD inclusion_note_code_also')
    def expr(self, p):
        data = self.handle_child_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD inclusion_note_code_first')
    def expr(self, p):
        data = self.handle_child_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD inclusion_include_code')
    def expr(self, p):
        data = self.handle_child_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD inclusion_include_exclude')
    def expr(self, p):
        data = self.handle_child_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD inclusion_include_code_exclude')
    def expr(self, p):
        data = self.handle_child_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD inclusion_include_note_exclude')
    def expr(self, p):
        data = self.handle_child_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD inclusion_include_note_code_also')
    def expr(self, p):
        data = self.handle_child_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD inclusion_include_note_code_also_exclude')
    def expr(self, p):
        data = self.handle_child_topics(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST')
    def expr(self, p):
        data = self.handle_child_block_list(p)
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST_CODE TOPIC_CHILD_LIST')
    def expr(self, p):
        child = {"code": p[0]}
        data = self.handle_child_block_list(p, extra=child)
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST_CODE TOPIC_CHILD_LIST CHILD_INCLUSION')
    def expr(self, p):
        child = {"code": p[0], "inclusionTerm": [p[2]]}
        data = self.handle_child_block_list(p, extra=child)
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST_CODE TOPIC_CHILD_LIST CODE_ALSO')
    def expr(self, p):
        child = {"code": p[0], "CodeAlso": [p[2]]}
        data = self.handle_child_block_list(p, extra=child)
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST_CODE TOPIC_CHILD_LIST INCLUDES')
    def expr(self, p):
        child = {"code": p[0], "includes": [p[2]]}
        data = self.handle_child_block_list(p, extra=child)
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST_CODE TOPIC_CHILD_LIST EXCLUDES')
    def expr(self, p):
        child = {"code": p[0], "excludes": [p[2]]}
        data = self.handle_child_block_list(p, extra=child)
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST_CODE TOPIC_CHILD_LIST NOTE')
    def expr(self, p):
        child = {"code": p[0], "notes": [p[2]]}
        data = self.handle_child_block_list(p, extra=child)
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST_CODE TOPIC_CHILD_LIST inclusion_exclude')
    def expr(self, p):
        child = {"code": p[0], **p[2]}
        data = self.handle_child_block_list(p, extra=child)
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST_CODE TOPIC_CHILD_LIST inclusion_note')
    def expr(self, p):
        child = {"code": p[0], **p[2]}
        data = self.handle_child_block_list(p, extra=child)
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST_CODE TOPIC_CHILD_LIST include_note')
    def expr(self, p):
        child = {"code": p[0], **p[2]}
        data = self.handle_child_block_list(p, extra=child)
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST_CODE TOPIC_CHILD_LIST inclusion_include')
    def expr(self, p):
        child = {"code": p[0], **p[2]}
        data = self.handle_child_block_list(p, extra=child)
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST_CODE TOPIC_CHILD_LIST include_exclude')
    def expr(self, p):
        child = {"code": p[0], **p[2]}
        data = self.handle_child_block_list(p, extra=child)
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST_CODE TOPIC_CHILD_LIST include_code_also')
    def expr(self, p):
        child = {"code": p[0], **p[2]}
        data = self.handle_child_block_list(p, extra=child)
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST_CODE TOPIC_CHILD_LIST code_also_exclude')
    def expr(self, p):
        child = {"code": p[0], **p[2]}
        data = self.handle_child_block_list(p, extra=child)
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST_CODE TOPIC_CHILD_LIST inclusion_code_also')
    def expr(self, p):
        child = {"code": p[0], **p[2]}
        data = self.handle_child_block_list(p, extra=child)
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST_CODE TOPIC_CHILD_LIST inclusion_include_exclude')
    def expr(self, p):
        child = {"code": p[0], **p[2]}
        data = self.handle_child_block_list(p, extra=child)
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST_CODE TOPIC_CHILD_LIST inclusion_include_note')
    def expr(self, p):
        child = {"code": p[0], **p[2]}
        data = self.handle_child_block_list(p, extra=child)
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST_CODE TOPIC_CHILD_LIST inclusion_code_exclude')
    def expr(self, p):
        child = {"code": p[0], **p[2]}
        data = self.handle_child_block_list(p, extra=child)
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST_CODE TOPIC_CHILD_LIST inclusion_include_code')
    def expr(self, p):
        child = {"code": p[0], **p[2]}
        data = self.handle_child_block_list(p, extra=child)
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST_CODE TOPIC_CHILD_LIST inclusion_code_first_exclude')
    def expr(self, p):
        child = {"code": p[0], **p[2]}
        data = self.handle_child_block_list(p, extra=child)
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST_CODE TOPIC_CHILD_LIST inclusion_include_note_exclude')
    def expr(self, p):
        child = {"code": p[0], **p[2]}
        data = self.handle_child_block_list(p, extra=child)
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST_CODE TOPIC_CHILD_LIST inclusion_include_note_code_also')
    def expr(self, p):
        child = {"code": p[0], **p[2]}
        data = self.handle_child_block_list(p, extra=child)
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST_CODE TOPIC_CHILD_LIST inclusion_include_code_exclude')
    def expr(self, p):
        child = {"code": p[0], **p[2]}
        data = self.handle_child_block_list(p, extra=child)
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST_CODE TOPIC_CHILD_LIST inclusion_include_note_code_also_exclude')
    def expr(self, p):
        child = {"code": p[0], **p[2]}
        data = self.handle_child_block_list(p, extra=child)
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST INCLUDES')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra={"includes": [p[1]]})
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST EXCLUDES')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra={"excludes": [p[1]]})
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST CODE_ALSO')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra={"CodeAlso": [p[1]]})
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST CODE_FIRST')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra={"CodeFirst": [p[1]]})
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST CHILD_INCLUSION')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra={"inclusionTerm": [p[1]]})
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST NOTE')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra={"notes": [p[1]]})
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST inclusion_exclude')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST include_exclude')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST inclusion_include')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST note_exclude')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST include_note')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST code_also_code_first')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST code_also_exclude')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST inclusion_code_also')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST inclusion_code_first')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST inclusion_note')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST note_code_also')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST include_code_also')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST include_code_first')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST inclusion_code_exclude')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST code_also_code_first_exclude')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST inclusion_code_first_exclude')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST include_code_also_code_first')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST inclusion_note_exclude')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST include_note_exclude')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST include_note_code_also')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST inclusion_note_code_also')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST include_code_also_exclude')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST inclusion_include_note')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST inclusion_include_exclude')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST inclusion_include_code')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST note_code_also_exclude')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST inclusion_include_code_first')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST inclusion_include_code_exclude')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST inclusion_include_code_also_code_also_exclude')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST inclusion_include_code_first_exclude')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST inclusion_include_note_code')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST inclusion_include_note_exclude')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST include_note_code_also_exclude')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_('TOPIC_CHILD_LIST inclusion_include_note_code_also_exclude')
    def expr(self, p):
        data = self.handle_child_block_list(p, extra=p[1])
        self.stack.append(data)
        return p[0]

    @_("CODE_ALSO EXCLUDES")
    def code_also_exclude(self, p):
        return {'CodeAlso': [p[0]], 'excludes': [p[1]]}

    @_("INCLUDES EXCLUDES")
    def include_exclude(self, p):
        return {'includes': [p[0]], 'excludes': [p[1]]}

    @_("INCLUDES CODE_ALSO")
    def include_code_also(self, p):
        return {'includes': [p[0]], 'CodeAlso': [p[1]]}

    @_("INCLUDES CODE_FIRST")
    def include_code_first(self, p):
        return {'includes': [p[0]], 'CodeFirst': [p[1]]}

    @_("EXCLUDES CODE_ALSO")
    def exclude_code_also(self, p):
        return {'excludes': [p[0]], 'CodeAlso': [p[1]]}

    @_("CHILD_INCLUSION INCLUDES")
    def inclusion_include(self, p):
        return {'inclusionTerm': [p[0]], 'includes': [p[1]]}

    @_("CHILD_INCLUSION EXCLUDES")
    def inclusion_exclude(self, p):
        return {'inclusionTerm': [p[0]], 'excludes': [p[1]]}

    @_("CHILD_INCLUSION CODE_ALSO")
    def inclusion_code_also(self, p):
        return {'inclusionTerm': [p[0]], 'CodeAlso': [p[1]]}

    @_("CHILD_INCLUSION CODE_FIRST")
    def inclusion_code_first(self, p):
        return {'inclusionTerm': [p[0]], 'CodeFirst': [p[1]]}

    @_("CHILD_INCLUSION NOTE")
    def inclusion_note(self, p):
        return {'inclusionTerm': [p[0]], 'notes': [p[1]]}

    @_("INCLUDES NOTE")
    def include_note(self, p):
        return {'includes': [p[0]], 'notes': [p[1]]}

    @_("CODE_ALSO CODE_FIRST")
    def code_also_code_first(self, p):
        return {'CodeAlso': [p[0]], 'CodeFirst': [p[1]]}

    @_("NOTE EXCLUDES")
    def note_exclude(self, p):
        return {'notes': [p[0]], 'excludes': [p[1]]}

    @_("CODE_FIRST EXCLUDES")
    def code_first_exclude(self, p):
        return {'CodeFirst': [p[0]], 'excludes': [p[1]]}

    @_("NOTE TABLE")
    def note_table(self, p):
        return {'notes': [p[0], p[1]]}

    @_("NOTE CODE_ALSO")
    def note_code_also(self, p):
        return {'notes': [p[0]], 'CodeAlso': [p[1]]}

    @_("CHILD_INCLUSION INCLUDES NOTE")
    def inclusion_include_note(self, p):
        return {'inclusionTerm': [p[0]], 'includes': [p[1]], 'notes': [p[2]]}

    @_("CHILD_INCLUSION NOTE EXCLUDES")
    def inclusion_note_exclude(self, p):
        return {'inclusionTerm': [p[0]], 'notes': [p[1]], 'excludes': [p[2]]}

    @_("CHILD_INCLUSION EXCLUDES NOTE")
    def inclusion_exclude_note(self, p):
        return {'inclusionTerm': [p[0]], 'excludes': [p[1]], "notes": [p[2]]}

    @_("INCLUDES NOTE EXCLUDES")
    def include_note_exclude(self, p):
        return {'includes': [p[0]], 'notes': [p[1]], 'excludes': [p[2]]}

    @_("INCLUDES NOTE CODE_ALSO")
    def include_note_code_also(self, p):
        return {'includes': [p[0]], 'notes': [p[1]], 'CodeAlso': [p[2]]}

    @_("CHILD_INCLUSION NOTE CODE_FIRST")
    def inclusion_note_code_first(self, p):
        return {'inclusionTerm': [p[0]], 'notes': [p[1]], 'CodeFirst': [p[2]]}

    @_("CHILD_INCLUSION CODE_FIRST EXCLUDES")
    def inclusion_code_first_exclude(self, p):
        return {'inclusionTerm': [p[0]], 'CodeFirst': [p[1]], 'excludes': [p[2]]}

    @_("CODE_ALSO CODE_FIRST EXCLUDES")
    def code_also_code_first_exclude(self, p):
        return {'CodeAlso': [p[0]], 'CodeFirst': [p[1]], 'excludes': [p[2]]}

    @_("CHILD_INCLUSION NOTE CODE_ALSO")
    def inclusion_note_code_also(self, p):
        return {'inclusionTerm': [p[0]], 'notes': [p[1]], 'CodeAlso': [p[2]]}

    @_("INCLUDES CODE_ALSO EXCLUDES")
    def include_code_also_exclude(self, p):
        return {'includes': [p[0]], 'CodeAlso': [p[1]], 'excludes': [p[2]]}

    @_("INCLUDES CODE_ALSO CODE_FIRST")
    def include_code_also_code_first(self, p):
        return {'includes': [p[0]], 'CodeAlso': [p[1]], 'CodeFirst': [p[2]]}

    @_("NOTE CODE_ALSO EXCLUDES")
    def note_code_also_exclude(self, p):
        return {'notes': [p[0]], 'CodeAlso': [p[1]], 'excludes': [p[2]]}

    @_("CHILD_INCLUSION INCLUDES EXCLUDES")
    def inclusion_include_exclude(self, p):
        return {'inclusionTerm': [p[0]], 'includes': [p[1]], 'excludes': [p[2]]}

    @_("CHILD_INCLUSION INCLUDES CODE_ALSO")
    def inclusion_include_code(self, p):
        return {'inclusionTerm': [p[0]], 'includes': [p[1]], 'CodeAlso': [p[2]]}

    @_("CHILD_INCLUSION INCLUDES CODE_FIRST")
    def inclusion_include_code_first(self, p):
        return {'inclusionTerm': [p[0]], 'includes': [p[1]], 'CodeFirst': [p[2]]}

    @_("CHILD_INCLUSION CODE_ALSO EXCLUDES")
    def inclusion_code_exclude(self, p):
        return {'inclusionTerm': [p[0]], 'CodeAlso': [p[1]], 'excludes': [p[2]]}

    @_("CHILD_INCLUSION INCLUDES CODE_ALSO EXCLUDES")
    def inclusion_include_code_exclude(self, p):
        return {'inclusionTerm': [p[0]], 'includes': [p[1]], 'CodeAlso': [p[2]], 'excludes': [p[3]]}

    @_("CHILD_INCLUSION INCLUDES CODE_ALSO CODE_ALSO EXCLUDES")
    def inclusion_include_code_also_code_also_exclude(self, p):
        return {'inclusionTerm': [p[0]], 'includes': [p[1]], 'CodeAlso': [p[2], p[3]], 'excludes': [p[4]]}

    @_("CHILD_INCLUSION INCLUDES CODE_FIRST EXCLUDES")
    def inclusion_include_code_first_exclude(self, p):
        return {'inclusionTerm': [p[0]], 'includes': [p[1]], 'CodeFirst': [p[2]], 'excludes': [p[3]]}

    @_("CHILD_INCLUSION INCLUDES NOTE CODE_ALSO")
    def inclusion_include_note_code(self, p):
        return {'inclusionTerm': [p[0]], 'includes': [p[1]], 'notes': [p[2]], 'CodeAlso': [p[3]]}

    @_("CHILD_INCLUSION INCLUDES NOTE EXCLUDES")
    def inclusion_include_note_exclude(self, p):
        return {'inclusionTerm': [p[0]], 'includes': [p[1]], 'notes': [p[2]], 'excludes': [p[3]]}

    @_("INCLUDES NOTE CODE_ALSO EXCLUDES")
    def include_note_code_also_exclude(self, p):
        return {'includes': [p[0]], 'notes': [p[1]], 'CodeAlso': [p[2]], 'excludes': [p[3]]}

    @_("CHILD_INCLUSION INCLUDES NOTE CODE_ALSO")
    def inclusion_include_note_code_also(self, p):
        return {'inclusionTerm': [p[0]], 'includes': [p[1]], 'notes': [p[2]], 'CodeAlso': [p[3]]}

    @_("CHILD_INCLUSION INCLUDES NOTE CODE_ALSO EXCLUDES")
    def inclusion_include_note_code_also_exclude(self, p):
        return {'inclusionTerm': [p[0]], 'includes': [p[1]], 'notes': [p[2]], 'CodeAlso': [p[3]], 'excludes': [p[4]]}

    def handle_block_start(self,p,extra={}):
        data = self.stack.pop()
        value = copy.deepcopy(self.children_sample_json)
        value['text'] = p[0]
        value = self.get_asc_code(value)
        value.update(extra)
        if data.get('children', []):
            data['children'].append(value)
        else:
            data['children'] = [value]
        return data

    def handle_topics(self, p, extra={}):
        try:
            data = self.stack.pop()
            child = {}
            child = data['children'][-1]
            # d = self.get_block_json(p[0], 'code')
            d = {"text": p[0]}
            d.update(extra)
            if child and child.get('children', []):
                child['children'].append(d)
            else:
                child['children'] = [d]
        except Exception as e:
            print("block_title_except")
            pass
        return data

    def handle_child_topics(self, p, extra={}):
        try:
            data = self.stack.pop()
            child = data['children'][-1]
            if child.get("children"):
                child = child['children'][-1]
            else:
                child["children"] = [{"children": []}]
                child = child['children'][-1]

            d = self.get_block_json(p[0], 'code')
            d = self.get_asc_code(d)
            d.update(extra)
            if child and child.get('children', []):
                child['children'].append(d)
            else:
                child['children'] = [d]
        except Exception as e:
            print("block_title_except")
            pass
        return data

    def handle_child_block_list(self, p,extra={}):
        data = self.stack.pop()
        try:
            child = data['children'][-1]
            child = child['children'][-1]
            child = child['children'][-1]
            if extra.get("code", {}):
                d = {"text": p[1]}
            else:
                d = self.get_child_list_json(p[0], 'code')
            d = self.get_asc_code(d)
            d.update(extra)
            if child and child.get('children', []):
                child['children'].append(d)
            else:
                child['children'] = [d]
        except Exception as e:
            print("block_list_except")
            return data
        return data

    def handle_block(self, p,extra={}):
        data = self.stack.pop()
        child = self.get_block_json(p[0])
        child.update(extra)
        if data.get('blocks', []):
            data['blocks'].append(child)
        else:
            data['blocks'] = [child]
        return data

    def get_asc_code(self, d):
        value = d['text']
        match = re.search(r'ACS_VALUE_START.+[\d]{4}', value)
        if not match:
            return d
        name = value[match.start():match.end()]
        name = name.strip("ACS_VALUE_START").strip()
        text = re.sub(r"ACS_VALUE_START.+[\d]{4}", "", value).strip()
        if "," in name:
            name = [n.strip() for n in re.split(r",|\s{1,}", name) if n]
        else:
            name = [name]
        d["ASC"] = name
        d["text"] = text
        return d

    def get_block_json(self,value,key='name'):
        match = re.search(r'^[\d]+', value)
        name = value[match.start():match.end()]
        text = value[match.end() + 1:]
        text = text.strip()
        return {key: name, 'text': text}

    def get_child_list_json(self,value,key='code'):
        match = re.search(r'[\d]{5}-([\d]{2}|XX)|(^-[\d]{2})', value)
        name = value[match.start():match.end()]
        text = value[match.end() + 1:]
        text = text.strip()
        return {key: name, 'text': text}

    @_('expr expr')
    def expr(self, p):
        return p[0]


def get_column_width(index,column):
    try:
        col_width_extraction = re.search(r"colw[0-9]*", re.search(rf"colno{index + 1}\\colw[0-9]*", column).group())
        return int(re.search(r"\d+",col_width_extraction.group()).group())
    except Exception as e:
        return 0


def get_col_margin(index,column):
    try:
        col_margin_extraction = re.search("colsr[0-9]*",re.search(rf"colno{index + 1}[^\s]+?\\colsr[0-9]*", column).group())
        return int(re.search(r"\d+", col_margin_extraction.group()).group())
    except Exception as e:
        return 0


custom_check_index = [7, 8, 9, 13, 15, 16, 18, 19, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 36, 38, 39, 40,
                      43, 44, 47, 49, 51, 55, 56, 58, 59, 61, 62, 63, 66, 67, 69, 71, 77, 79, 80, 82, 85, 87, 88, 89,
                      92, 93, 94, 95, 96, 100, 101, 103, 104, 105, 106, 107, 109, 113, 115, 116, 117, 123, 125, 126,
                      127, 128, 129, 131, 135, 136, 137, 138, 140, 141, 142, 145, 146, 149, 150, 151, 152, 153, 154,
                      155, 156, 159, 161, 162, 163, 165, 166, 167, 168, 169, 171, 172, 174, 175, 176, 177, 178, 180,
                      182, 186, 187, 190, 192, 195, 196, 197, 198, 199, 201, 202, 203, 205, 207, 208, 209, 210, 211,
                      212, 213, 214, 215, 218, 219, 220, 221, 222, 228, 230, 231, 232, 233, 236, 237, 239, 240, 241,
                      242, 244, 245, 246, 247, 248, 251, 253, 255, 259, 260, 261, 262, 263, 264, 265, 267, 268, 269,
                      274, 275, 278, 282, 283, 285, 286, 287, 288, 291, 293, 294, 295, 296, 297, 298, 300, 301, 303,
                      304, 305, 307, 308, 309]

ignore_trowd = [0, 3, 12, 14, 16, 19, 20, 23, 24, 26, 27, 29, 30, 31, 32, 33, 36, 37, 38, 39, 42, 43, 45, 46, 47, 48,
                49, 50, 51, 52, 57, 59, 61, 62, 64, 65, 70, 77, 80, 96, 97, 98, 100, 107, 117, 118, 119, 120, 121, 131,
                132, 133, 134, 135, 136, 139, 150, 151, 153, 157, 162, 163, 167, 169, 175, 177, 181, 187, 191, 193, 197,
                200, 201, 204, 206, 211, 213, 215, 216, 218, 219, 220, 221, 231, 232, 233, 236, 241, 243, 245, 247, 248,
                251, 254, 256, 264, 265, 269, 270, 278, 280, 281, 284, 285, 286, 291, 295, 300, 302]

ignore_trowd_column = {63: [2, 3]}


def split_table_data(table, z, is_inner=False):
    splitted = table.split('\\trowd')
    if not is_inner:
        z[0] += splitted[0]
    rows = splitted[1:]
    for index, row in enumerate(rows):
        # cell_count = row.count("\\cell}")
        # cells = row.split("\\cell}")
        cells = re.split(r"\\cell}|\\tab\s\\", row)
        cell_count = len(cells) - 1

        if cell_count in (4, 3):
            z[0] += f"{cells[0]}" + "\\cell}" + f"{cells[1]}" + "\\cell}"
            z[1] += "".join([cell + "\\cell}" for cell in cells[2:]])
            # z[1] += f"{cells[2]}" + "\\cell}" + f"{cells[3]}" + "\\cell}"
        # elif cell_count == 3:
        #     z[0] += f"{cells[0]}" + "\\cell}" + f"{cells[1]}" + "\\cell}"
        #     z[1] += f"{cells[2]}" + "\\cell}"
        elif cell_count == 2:
            z[0] += f"{cells[0]}" + "\\cell}"
            z[1] += f"{cells[1]}" + "\\cell}"
        elif cell_count == 5:
            z[0] += f"{cells[0]}" + "\\cell}" + f"{cells[1]}" + "\\cell}"
            z[1] += f"{cells[2]}" + "\\cell}" + f"{cells[3]}" + "\\cell}" + f"{cells[4]}" + "\\cell}"
        # elif cell_count == 1:
            z[0] += f"{cells[0]}" + "\\cell}"


def split_column(text, page_index):
    z = ['', '']
    text = copy.deepcopy(text)
    columns = re.split(r"\\par\\sect\\sectd\\sbknone\\|\\pard\\sect\\sectd\\sbknone\\", text)

    if "\\trowd" in columns[0] and ignore_trowd_column.get(page_index, None) and 0 not in ignore_trowd_column[page_index] or\
            "\\trowd" in columns[0] and page_index not in ignore_trowd:
        split_table_data(columns[0], z)
    else:
        z[0] = columns[0]
    columns = columns[1:]

    for col_index, column in enumerate(columns, start=1):
        column_spaces = []
        split_trowd = ['', '']
        total_columns = int(re.search(r"\d+", column.split("\\", 1)[0]).group())
        total = 0
        column = "\\" + column
        for index in range(total_columns):
            width = get_column_width(index, column)
            margin = get_col_margin(index, column)
            column_spaces.append(width + margin)
            total += width + margin
        column = re.sub(r"\\cols[^\s]*\\par[^\\]*", r"\\par", column)
        data = column.split('\\column')
        for index, d in enumerate(data):

            if "\\trowd" in d and ignore_trowd_column.get(page_index, None):
                if col_index not in ignore_trowd_column[page_index]:
                    data[index] = d.split('\\trowd')[0]
                    split_table_data(d, split_trowd, is_inner=True)
            elif "\\trowd" in d and page_index not in ignore_trowd:
                # x = ['', '']
                # column_text = copy.deepcopy(d)
                data[index] = d.split('\\trowd')[0]
                split_table_data(d, split_trowd, is_inner=True)
                # try:
                #     data[index] = re.split(r"\\row\\",d)[1]
                # except Exception:
                #     data[index]=''
                # data[index] = '\\column '.join(x)

        if total_columns == 3:
            add_a = column_spaces[0] + column_spaces[1]
            add_b = column_spaces[1] + column_spaces[2]
            if add_a > add_b:
                z[0] += " \\column " + data[0]
                z[1] += " \\column " + data[1] + data[2]
            else:
                z[0] += " \\column " + data[0] + data[1]
                z[1] += " \\column " + data[2]
        elif total_columns == 2:
            if column_spaces[0] < 4000:
                z[0] += " \\column " + data[0] + data[1]
            else:
                z[0] += " \\column " + data[0]
                z[1] += " \\column " + data[1]
        elif total_columns == 4:
            add_a = column_spaces[0] + column_spaces[1] + column_spaces[2]
            add_b = column_spaces[3]
            if column_spaces[0] > 6000:
                z[0] += " \\column " + data[0]
                z[1] += " \\column " + data[1] + data[2] + data[3]

            elif add_a < add_b:
                z[0] += " \\column " + data[0] + data[1] + data[2]
                z[1] += " \\column " + data[3]
            elif (add_a - add_b) < 500:
                z[0] += " \\column " + data[0] + data[1] + data[2]
                z[1] += " \\column " + data[3]
            else:
                z[0] += " \\column " + data[0] + data[1]
                z[1] += " \\column " + data[2] + data[3]
        elif total_columns == 1:
            if column_spaces[0] > 6000:
                z[0] += "\\column" + data[0]

        if split_trowd[0]:
            z[0] += split_trowd[0]
            z[1] += split_trowd[1]

    x = ' \\column '.join(z)
    return x


def main():
    write_tokens = False

    lexer = MyLexer()
    print('-------------------------------------------------------')
    filename = input('Please Enter valid file path with filename: \n')
    try:
        with open(filename + '.rtf', 'r') as file:
            text = file.read()
    except Exception as e:
        print(e)
        return

    print('File is valid')
    print('-------------------------------------------------------')
    file_output = input('Please Enter output filename: \n')
    print('-------------------------------------------------------')
    print('Please Wait While Lex/Yac tokenizer is working')
    print('-------------------------------------------------------')

    start_time = time.time()

    pages = text.split(page_split)
    pages = pages[36:346]

    pages = page_splitter(pages)

    for index, page in enumerate(pages):
        if index in custom_check_index:
            x = split_column(page, index)
            text_to_read = replace_text(index, x)
            text_to_read ='\n'.join(text_to_read)
            x = text_to_read
        else:
            x = split_column(page, index)
        pages[index] = x

    text = f' \n {page_split} '.join(pages)
    line_by_line = text.split('\n')
    text_to_read = '\n'.join([line for line in line_by_line if check_line_has_valid_text(line)])

    text_to_read = get_cleaned_text(text_to_read)

    tokens = lexer.tokenize(text_to_read)
    if write_tokens:
        tokens_new = []
        tokens_prev = []
        for t in tokens:
            tokens_new.append(str(t))
            tokens_prev.append(t)
        with open('achi_tokens.json', 'w', encoding="utf-8") as file:
            json.dump(tokens_new, file, indent=4, ensure_ascii=False)
        tokens = (t for t in tokens_prev)

    parser = MyParser()
    parser.parse(tokens)
    with open(f"{file_output}.json", 'w', encoding="utf-8") as file:
        json.dump(parser.last_item_on_stack, file, indent=4, ensure_ascii=False)
    print('-------------------------------------------------------')
    print('Your file is completed with time:{0} Seconds '.format(str(time.time() - start_time)))


if __name__ == '__main__':
    main()
