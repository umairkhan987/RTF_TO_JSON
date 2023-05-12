import re
import json
import copy


def get_cleaned_text(text_to_read):

    text_to_read = re.sub(r"49454e44ae426082 ", "", text_to_read)
    text_to_read = re.sub(r"776c2c5e26197f0345c3725f1620e35f0000000049454e44ae426082", "", text_to_read)

    text_to_read = re.sub(r"\\f4\\fs16\\b1\\charscalex120\\cf9\s[A-Z][0-9]{2}(\.[0-9]{1,2})*", "", text_to_read)
    text_to_read = re.sub(r"\n{\\shptxt\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\sl-192\\par}}}", "",
                          text_to_read)
    text_to_read = re.sub(
        r"\\par\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\qr\\sl240\\slmult1\\f4\\fs16\\b1\\charscalex125\\cf9 K28\\par\\pard\\plain\\s11\\ls197\\ilvl0\\nooverflow\\nocwrap\\lnbrkrule\\li2114\\fi-115\\sl-212\\tx2115\\f16\\fs18\\b0\\charscalex85\\cf4\s",
        "",
        text_to_read)
    text_to_read = re.sub(
        r"\\par\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\qr\\sl240\\slmult1\\f4\\fs16\\b1\\charscalex115\\cf9\sM89",
        "",
        text_to_read)
    text_to_read = re.sub(
        r"\\par\\pard\\plain\\s9\\nooverflow\\nocwrap\\lnbrkrule\\li500\\ri2505\\sl228\\slmult1\\sb6  \\f4\\fs19\\b1\\charscalex115\\cf4",
        "", text_to_read)
    text_to_read = re.sub(
        r"\\par\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\qr\\sl240\\slmult1\\sb19\\f4\\fs16\\b1\\charscalex115\\cf9 T81.5",
        "", text_to_read)
    text_to_read = re.sub(
        r"\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li[^\s]*\\sl240\\slmult1\\sb1\\f4\\fs16\\b1\\charscalex125\\cf9\sW36",
        "", text_to_read)
    text_to_read = re.sub(
        r"\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li[^\s]*\\sl240\\slmult1\\sb1\\f4\\fs16\\b1\\charscalex125\\cf9\sX75",
        "", text_to_read)

    return text_to_read


def get_and_remove(regex, text, count=None):
    found = re.search(regex, text).group()
    if count:
        text = re.sub(regex, "", text, count=count)
    else:
        text = re.sub(regex, "", text)
    return found, text


def check_line_has_valid_text(text):
    text = copy.deepcopy(text)
    if "trow" in text:
        return True
    if re.search(r"<table>.+?<\/table>", text):
        return True
    if re.search(r"\\f4\\fs16\\b1[^\s]*\s[A-Z][0-9]{2}\\par}",text):
        return False
    elif "\par" in text:
        text = re.sub(r"\\[^\s]*", "", text)
        text = text.replace("{","")
        text = text.strip()
        if text:
            return True
        else:
            return False
    return False


def page_splitter(pages):
    # replace text in pages
    pages[2] = re.sub(r"\\f4\\fs18\\b0\\charscalex95\\cf2 postoperative\\par",
                      r"\\f4\\fs18\\b0\\charscalex95\\cf2 postoperative\\par" + repr(re.search(
                          r"\\f16\\fs18\\b1\\i1\\charscalex95\\cf2 Includes: \\f4\\fs18\\b0\\i0 removal .+flap\\par",
                          pages[3]).group()), pages[2])
    pages[3] = re.sub(r"\\f16\\fs18\\b1\\i1\\charscalex95\\cf2 Includes: \\f4\\fs18\\b0\\i0 removal .+flap\\par", "",
                      pages[3])

    split_page = pages[28].split("28\\tab", 1)
    pages[27] += split_page[0]
    pages[28] = split_page[1]

    split_page = pages[30].split("30\\tab", 1)
    pages[29] += split_page[0]
    pages[30] = split_page[1]

    split_page = pages[37].split("37\\tab", 1)
    pages[36] += split_page[0]
    pages[37] = split_page[1]

    pages[44] = re.sub(r"uncinectomy\\par\\pard\\plain\\s6\\nooverflow\\nocwrap",
                       r"uncinectomy " + repr(re.search(r"\\row.+?(\n.+?)?\\f7\\fs18\\b0", pages[45]).group()),
                       pages[44])
    pages[45] = re.sub(r"\\row.+?(\n.+?)?\\f7\\fs18\\b0", "", pages[45])

    found, new_text = get_and_remove(r"\\pard.+(\n.+)*48\\tab", pages[48])
    pages[47] += found
    pages[48] = new_text

    split_page = pages[55].split("55\\tab")
    pages[55] = split_page[0]
    pages.insert(56, split_page[1])

    split_page = pages[57].split("56\\tab", 1)
    pages[56] += split_page[0]
    pages[57] = split_page[1]

    split_page = pages[78].split("77\\tab", 1)
    pages[77] += split_page[0]
    pages[78] = split_page[1]

    split_page = pages[81].split("80\\tab", 1)
    pages[80] += split_page[0]
    pages[81] = split_page[1]

    split_page = pages[95].split("94\\tab", 1)
    pages[94] += split_page[0]
    pages[95] = split_page[1]

    split_page = pages[127].split("126\\tab", 1)
    pages[126] += split_page[0]
    pages[127] = split_page[1]

    found, pages[137] = get_and_remove(r"\\pard\\.+?transplantation\\par", pages[137])
    pages[136] += found

    split_page = pages[142].split("141\\tab", 1)
    pages[141] += split_page[0]
    pages[142] = split_page[1]

    split_page = pages[146].split("145\\tab", 1)
    pages[145] += split_page[0]
    pages[146] = split_page[1]

    split_page = pages[153].split("152\\tab", 1)
    pages[152] += split_page[0]
    pages[153] = split_page[1]

    split_page = pages[156].split("155\\tab", 1)
    pages[155] += split_page[0]
    pages[156] = split_page[1]

    split_page = pages[168].split("167\\tab", 1)
    pages[167] += split_page[0]
    pages[168] = split_page[1]

    split_page = pages[187].split("186\\tab", 1)
    pages[186] += split_page[0]
    pages[187] = split_page[1]

    split_page = pages[197].split("196\\tab", 1)
    pages[196] += split_page[0]
    pages[197] = split_page[1]

    split_page = pages[212].split("211\\tab", 1)
    pages[211] += split_page[0]
    pages[212] = split_page[1]

    split_page = pages[286].split("285\\tab", 1)
    pages[285] += split_page[0]
    pages[286] = split_page[1]

    split_page = pages[287].split("286\\tab", 1)
    pages[286] += split_page[0]
    pages[287] = split_page[1]

    split_page = pages[310].split("309\\tab", 1)
    pages[309] += split_page[0]
    pages[310] = split_page[1]

    return pages


def replace_text(index, x):
    line_by_line = x.split('\n')
    text_to_read = [line for line in line_by_line if check_line_has_valid_text(line)]

    if index == 7:
        text_to_read[13] = text_to_read[13].strip("776c2c5e26197f0345c3725f1620e35f0000000049454e44ae426082")
        split_text = text_to_read[6].split("\\par\\")
        text_to_read[6] = "{\\" + split_text[1]
        found, text_to_read[22] = get_and_remove(r"\\f7\\fs19\\b0.+?\\cell}", text_to_read[22])
        text_to_read[12] += found
        found, text_to_read[23] = get_and_remove(r"\\pard.+\\cell}", text_to_read[23])
        text_to_read[4] = found + text_to_read[4] + split_text[0]
        text_to_read[22] = "\\f16\\fs18\\b1\\i1\\up0 Note:\\tab \\f4\\fs18\\b0\\i0 Performed\\expnd-5\\expndtw-25  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 for\\expnd-5\\expndtw-26  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 management\\expnd-5\\expndtw-25  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 of:\\cell}\\row" + text_to_read[22]

    if index == 8:
        text_to_read[10] += "\\f16\\fs18\\b1"

    if index == 9:
        found, text_to_read[14] = get_and_remove(r"\\pard.+\\cell}", text_to_read[14])
        text_to_read[9] += found

    if index == 13:
        found, text_to_read[28] = get_and_remove(r"\\pard.+", text_to_read[28])
        text_to_read[16] = found + text_to_read[16]
        text_to_read[29] = text_to_read[17] + text_to_read[29]
        text_to_read[27] += text_to_read[31]
        text_to_read[17] = text_to_read[31] = ""
        found, text_to_read[15] = get_and_remove(r"f7\\fs19\\b0\\i0.+tx6155", text_to_read[15])
        text_to_read[28] = "\\" + found + text_to_read[28]
        text_to_read[23] = "\\tab \\f16\\fs18\\b1\\i1\\up0 Includes:\\expnd-1\\expndtw-7  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 administration\\expnd-5\\expndtw-26  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 into\\expnd-5\\expndtw-25  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 spinal\\expnd-5\\expndtw-26  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 nerves:\\cell}\\" \
                           + text_to_read[23] + "\\f4\\fs18\\b0\\i0\\up9\\charscalex100 \\'95\\expnd-1\\expndtw-3  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0\\charscalex105 plexus"
        text_to_read[27] = text_to_read[27].replace("sympathetic\cell}", "sympathetic nervous system\cell}")

    if index == 15:
        text_to_read[6] += "\\f7\\fs19\\b0\\"

    if index == 16:
        found, text_to_read[20] = get_and_remove(r"\\f4\\fs18\\b0\\charscalex95\\cf2 reoperation \\column", text_to_read[20])
        text_to_read[20] = text_to_read[20].replace("ganglionectomy", "ganglionectomy reoperation")

    if index == 18:
        found, text_to_read[18] = get_and_remove(r"\\sb169\\f7\\fs19\\b0.+?\\column", text_to_read[18])
        text_to_read[7] += found
        found, text_to_read[18] = get_and_remove(r"\\tx109\\f4\\fs18\\b0.+?\\column", text_to_read[18])
        text_to_read[7] += found
        found, text_to_read[18] = get_and_remove(r"{\\pard.+?\\column", text_to_read[18])
        text_to_read[7] += text_to_read[18]
        text_to_read[18] = found

    if index == 19:
        text_to_read[6] += text_to_read[21]
        text_to_read[7] += text_to_read[24]
        text_to_read[18] = text_to_read[30]
        text_to_read[32], text = text_to_read[32].split("\\column")
        text_to_read[32] += text_to_read[6] + text_to_read[7] + text_to_read[11] + text_to_read[12]
        text_to_read[6] = text_to_read[7] = text_to_read[21] = text_to_read[24] = text_to_read[30] = text_to_read[11] = text_to_read[12] = ""
        first_text, text_to_read[17] = text_to_read[17].split("\\column")
        text_to_read[32] += text_to_read[16] + first_text + text

    if index == 22:
        text_to_read[9] += "\\f16\\fs18\\b1\\"

    if index == 23:
        found, text_to_read[4] = get_and_remove(r"\\tab\s\\f12\\fs22.+?\\column", text_to_read[4])
        text_to_read[4] += "".join(text_to_read[8:16]) + found
        text_to_read[8:16] = ""

    if index == 24:
        found, text_to_read[44] = get_and_remove(r"^\\pard\\.+?\\par", text_to_read[44])
        text_to_read[38] = found

    if index == 25:
        t_187 = text_to_read[7]
        text_to_read[35] = text_to_read[35].replace("f7", "\\f7", 1)
        found, text_to_read[36] = get_and_remove(r"f12\\fs19\\b1.+", text_to_read[36])
        text_to_read[37] = t_187 + found + text_to_read[37]
        text_to_read[49] = "\\f12\\fs19\\b1\\i0\\up0\\cf5{\\chcbpat2 188\\tab }\\tab \\f12\\fs19\\b1\\i0\\cf2 Destruction procedures on iris,\\expnd-5\\expndtw-24  \\f12\\fs19\\b1\\i0\\expnd0\\expndtw0 ciliary\\cell}\\row \\f12\\fs19\\b1\\i0\\dn8\\charscalex100 body or anterior\\expnd5\\expndtw23  \\f12\\fs19\\b1\\i0\\expnd0\\expndtw0 chamber\\cell}\\row"
        text_to_read[49] += text_to_read[25]
        text_to_read[50] = "{\\pard\\plain\\intbl\\s10\\nooverflow\\nocwrap\\lnbrkrule\\sl240\\slmult1\\sb8\\f10\\fs20\\b0\\i0\\par\\pard\\plain\\intbl\\s10\\nooverflow\\nocwrap\\lnbrkrule\\li90\\sl-194\\f7\\fs19\\b0\\charscalex115\\cf2 Destruction of lesion of iris or ciliary body\\cell}" + text_to_read[50]
        text_to_read[7] = text_to_read[25] = ""
        text_to_read[53] += "\\f16\\fs18\\b1\\"

    if index == 26:
        t_42698_05 = text_to_read.pop(20)
        text_to_read[17] = text_to_read.pop(32)
        text_to_read[34] += t_42698_05

    if index == 27:
        include, text_to_read[16] = get_and_remove(r"^\\pard.+?\\par", text_to_read[16])
        text_to_read[19], other_proc = get_and_remove(r"{\\pard.+\\tab", text_to_read[19])
        text_to_read[21], t_208 = get_and_remove(r"{\\pard.+?\\tab", text_to_read[21])
        text_to_read[24], text = get_and_remove(r"{\\pard.+?\\tab", text_to_read[24])
        t_208 += text
        text_to_read[30], poster_tag = get_and_remove(r"{\\pard.+?\\tab", text_to_read[30])
        text_to_read[32], text = get_and_remove(r"{\\pard.+?\\tab", text_to_read[32])
        poster_tag += text
        text_to_read[35], text = get_and_remove(r"{\\pard.+?\\tab", text_to_read[35])
        poster_tag += text
        poster_tag += "".join(text_to_read[40:44])
        text_to_read[40: 44] = ""
        poster_tag += text_to_read[43] + text_to_read[46] + text_to_read[50] + text_to_read[51] + text_to_read[54] + text_to_read[57]
        text_to_read[43] = text_to_read[46] = text_to_read[50] = text_to_read[51] = text_to_read[54] = text_to_read[57] = ""
        exclude, text_to_read[67] = get_and_remove(r"}\\par.+?\\f4\\fs20\\b0", text_to_read[67])
        text_to_read[59], t_42812 = get_and_remove(r"{\\pard.+\\tab", text_to_read[59])
        poster_tag += t_42812 + "".join(text_to_read[60:67]) + exclude
        text_to_read[60: 67] = ""
        text_to_read[60] = text_to_read[60].replace("776c2c5e26197f0345c3725f1620e35f0000000049454e44ae426082", "")
        excision, text_to_read[4] = get_and_remove(r"\s\\f12\\fs22\\b1\\i0\\char.+\\column", text_to_read[4])
        text_to_read[60] = excision + text_to_read[60]
        text_to_read.append(other_proc + t_208 + poster_tag)
        text_to_read[5] = include

    if index == 28:
        found, text_to_read[4] = get_and_remove(r"\s\\f12\\fs22\\b1\\i0\\char.+\\column", text_to_read[4])
        text_to_read[6] = found + text_to_read[6]

    if index == 29:
        ocular_tag, text_to_read[21] = get_and_remove(r"\\pard.+?\\column", text_to_read[21])
        revision_tag, text_to_read[21] = get_and_remove(r"\\par.+?\\par\\", text_to_read[21])
        text, text_to_read[22] = get_and_remove(r"^\\pard.+?\\column", text_to_read[22])
        text_to_read[21] += text
        text_to_read[22] = revision_tag + text_to_read[22]
        text_to_read[29] = ocular_tag
        incision_tag, text_to_read[28] = get_and_remove(r"\\f12\\fs22\\b1.+", text_to_read[28])
        text_to_read[42], text = get_and_remove(r"\\pard.+\\column", text_to_read[42])
        text_to_read[42] += incision_tag + text
        text_to_read[43] += "\\f7\\fs19\\b0\\"

    if index == 30:
        text_to_read[0] = text_to_read[1] = ""
        repair_tag, text_to_read[4] = get_and_remove(r"\\tab.+\\column", text_to_read[4])
        text_to_read[6] = text_to_read[24]
        text_to_read[24] = ""
        t_30 = "".join(text_to_read[9:11]) + "".join(text_to_read[14:16])
        text_to_read[18] += text_to_read[22]
        text_to_read[9] = text_to_read[10] = text_to_read[14] = text_to_read[15] = text_to_read[22] = ""
        text_to_read[24] = "\\f12\\fs22\\b1" + repair_tag
        text_to_read[34], _ = get_and_remove(r"{\\pard.+?\\f12\\fs22\\b1\\i0", text_to_read[34])
        text_to_read[34] += t_30
        found, new_text = get_and_remove(r"{\\pard.+?par", text_to_read[20])
        text_to_read[34] += found + "alysis " + text_to_read[19] + new_text + text_to_read[23]
        text_to_read[19] = text_to_read[20] = text_to_read[23] = ""
        text_to_read[34] += "\\f7\\fs19\\b0\\"

    if index == 31:
        text_to_read[0] = text_to_read[1] = ""
        text_to_read[5] = text_to_read.pop(16)
        text_to_read[18] += "\\f16\\fs18\\b1\\"

    if index == 32:
        text_to_read[19] = text_to_read.pop(63)
        text_to_read[62] += "\\f16\\fs18\\b1\\"

    if index == 33:
        found, text_to_read[32] = get_and_remove(r"^\\pard.+?\\column", text_to_read[32])
        text_to_read[4] = found
        found, text_to_read[32] = get_and_remove(r"\\sb98\s\s\\f4\\fs18\\b0.+?\\column", text_to_read[32])
        text_to_read[31] += found
        text_to_read[35] = text_to_read.pop(53)
        text_to_read[53] = text_to_read[53].replace("776c2c5e26197f0345c3725f1620e35f0000000049454e44ae426082", "")
        text_to_read[53] += "\\f16\\fs18\\b1\\"

    if index == 34:
        found, text_to_read[4] = get_and_remove(r"\s\\f12\\fs22\\b1.+?\\par\\pard\\", text_to_read[4])
        text_to_read[5] = found + text_to_read[5]

    if index == 36:
        t_36 = text_to_read[10] + text_to_read[11] + text_to_read[14]
        text_to_read[10] = text_to_read[11] = text_to_read[14] = ""
        t_90111_00 = text_to_read[18] + text_to_read[19]
        text_to_read[18] = text_to_read[19] = ""
        # text_to_read[34] += t_36 + t_90111_00
        other_proc, text_to_read[34] = get_and_remove(r"\\f12\\fs22\\b1\\cf2.+?\\par", text_to_read[34])
        text_to_read[34], _ = get_and_remove(r"\\pard.+\)\\par", text_to_read[34])
        text_to_read.append(other_proc + t_36 + t_90111_00)
        text_to_read[35] += "\\f16\\fs18\\b1\\"

    if index == 39:
        text_to_read[10] = "".join(text_to_read[39:41])
        text_to_read[39:41] = ""
        text_to_read[10] += "".join(text_to_read[40:47])
        text_to_read[40:47] = ""
        t_41557 = text_to_read[12] + text_to_read[13]
        text_to_read[12] = text_to_read[13] = ""
        found, text_to_read[15] = get_and_remove(r"\\f7\\fs19.+", text_to_read[15])
        t_41557 += found + text_to_read[16] + text_to_read[19] + text_to_read[20] + text_to_read[23] + text_to_read[24]
        text_to_read[16] = text_to_read[19] = text_to_read[20] = text_to_read[23] = text_to_read[24] = ""
        text_to_read[40], code_also = text_to_read[40].split("\\column")
        text, text_to_read[41] = get_and_remove(r"^\\par.+?\\par\\", text_to_read[41])
        code_also += text
        text_to_read[41] = t_41557 + code_also + text_to_read[41]

    if index == 40:
        other_proc, text_to_read[3] = get_and_remove(r"\\tab.+?\\column", text_to_read[3])
        text_to_read[5] = other_proc + text_to_read[5]

    if index == 43:
        text_to_read[4] = text_to_read[20]
        t_41686_01 = text_to_read[7] + text_to_read[8] + text_to_read[11]
        t_41672_00 = text_to_read[15] + text_to_read[16] + text_to_read[19]
        other_proc, text_to_read[77] = get_and_remove(r"^\\pard.+?\\column", text_to_read[77])
        other_proc = text_to_read[76] + other_proc
        found, text_to_read[75] = get_and_remove(r"\\f4\\fs10\\b0.+", text_to_read[75])
        text_to_read[73] += found + other_proc + t_41686_01 + t_41672_00
        text_to_read[75] = text_to_read[75].replace("\\cf5 376\\", "")
        found, text_to_read[75] = get_and_remove(r"\\f14\\fs15\\b0.+?\\par", text_to_read[75])
        text_to_read[77] = text_to_read[77].replace("\\column", found, 1)
        found, text_to_read[75] = get_and_remove(r"\\column.+\\par\\", text_to_read[75])
        text_to_read[77] = text_to_read[77].replace("\\column", found)
        text_to_read[20] = text_to_read[7] = text_to_read[8] = text_to_read[15] = text_to_read[11] = text_to_read[16] = text_to_read[19] = text_to_read[76] = ""

    if index == 44:
        found, text_to_read[10] = get_and_remove(r"\\column.+", text_to_read[10])
        text_to_read[11] += found

    if index == 47:
        found, text_to_read[17] = get_and_remove(r"\\tab.+", text_to_read[17])
        text_to_read[49] += text_to_read[8] + text_to_read[11]
        text_to_read[49] += text_to_read[14] + text_to_read[15] + found + text_to_read[18] + text_to_read[22] + text_to_read[23]
        text_to_read[8] = text_to_read[11] = text_to_read[14] = text_to_read[15] = text_to_read[18] = text_to_read[22] = text_to_read[23] = ""
        text_to_read[31], text = get_and_remove(r"\\f12\\fs22\\b1.+", text_to_read[31])
        t_413 = "".join(text_to_read[27:31])
        t_413 += text
        text_to_read[27:31] = ""
        text_to_read.append(t_413)

    if index == 49:
        t_41804 = text_to_read.pop(21)
        found, text_to_read[21] = get_and_remove(r"\\f7\\fs19.+", text_to_read[21])
        t_41804 += found
        text_to_read[21] += t_41804

    if index == 51:
        text_to_read[24], text = get_and_remove(r"\\pard.+?\\column", text_to_read[24])
        text_to_read[53] += text

    if index == 55:
        text_to_read[3] = ""
        text_to_read[8] = ""
        text_to_read[13] = ""
        text_to_read[18] = ""
        text_to_read[23] = ""
        text_to_read[28] = "{\\pard\\plain\\intbl\\s10\\nooverflow\\nocwrap\\lnbrkrule\\li100\\ri215\\sl228\\slmult1\\sb85\\f7\\fs19\\b0\\charscalex115\\cf2 Surgical removal of unspecified number of teeth requiring removal of bone\\cell}"
        text_to_read[29] = ""

    if index == 56:
        text_to_read[0] = text_to_read[1] = text_to_read[2] = ""
        text_to_read[11], t_97414 = get_and_remove(r"{\\pard.+?\\tab", text_to_read[11])
        found, text_to_read[22] = get_and_remove(r"\\f7\\fs19.+", text_to_read[22])
        text_to_read[10] += found + text_to_read[11]
        found, text_to_read[12] = get_and_remove(r"{\\pard.+?\\cell}", text_to_read[12])
        text_to_read[10] += found
        found, text_to_read[28] = get_and_remove(r"^\\pard.+?\\par", text_to_read[28])
        text_to_read[10] += found + text_to_read[13]
        text_to_read[13] = text_to_read[11] = ""
        text_to_read[18] = text_to_read[18].replace("ENDODONTICSup10", "ENDODONTICS")
        _, text_to_read[18] = get_and_remove(r"\\cf5.+", text_to_read[18])
        text_to_read[19] = text_to_read[19].replace("\\cf2", "\\cf2 462")
        found, text_to_read[10] = get_and_remove(r"^{\\pard.+?\\par", text_to_read[10])
        text_to_read[21] += found
        text_to_read[23] = "{\\pard\\plain\\intbl\\f7\\fs19\\b0\\expnd-1\\expndtw-4\\charscalex115\\cf2 " + t_97414 + text_to_read[23]
        text_to_read[24] = "{\\pard\\" + text_to_read[12] + text_to_read[24]
        text_to_read[12] = ""
        text_to_read[27] += "\\f7\\fs19\\b0"

    if index == 58:
        _, text_to_read[11] = get_and_remove(r"{\\pard.+?\\column", text_to_read[11])
        found, text_to_read[17] = get_and_remove(r"{\\pard.+?\\par", text_to_read[17])
        tag, text_to_read[16] = get_and_remove(r"{\\pard.+?\\par", text_to_read[16])
        text_to_read[15] += tag + found

    if index == 59:
        t_472 = text_to_read[13] + text_to_read[14] + text_to_read[18]
        text_to_read[13] = text_to_read[14] = text_to_read[18] = ""
        text_to_read[15], text_to_read[42] = get_and_remove(r"^\\pard.+?\\column", text_to_read[42])
        t_97651 = text_to_read[22] + text_to_read[23]
        t_97652 = text_to_read[27] + text_to_read[28] + text_to_read[31]
        t_97653, text_to_read[33] = get_and_remove(r"\\tab.+?\\par", text_to_read[33])
        t_97653 += text_to_read[34]
        t_97655, text_to_read[36] = get_and_remove(r"\\tab\s\\f7.+", text_to_read[36])
        t_97656 = text_to_read[40] + text_to_read[41]
        t_97655 += text_to_read[37]
        text_to_read[44] = re.sub(r"\\f4\\fs22\\b0.+\\column", repr(t_472 + t_97651 + t_97652 + t_97653 + t_97655 + t_97656), text_to_read[44])
        text_to_read[22] = text_to_read[23] = text_to_read[34] = text_to_read[27] = text_to_read[31] = text_to_read[28] = text_to_read[37] = text_to_read[40] = text_to_read[41]= ""

    if index == 61:
        code_also, text_to_read[11] = text_to_read[11].split("\\column")
        text_to_read[12] += text_to_read[7] + text_to_read[8] + code_also
        text_to_read[7] = text_to_read[8] = ""

    if index == 62:
        text_to_read[4], text_to_read[13] = get_and_remove(r"^\\pard.+?\\par", text_to_read[13])
        text_to_read[14] = text_to_read[32]
        text_to_read[41] = "".join(text_to_read[42: 45])
        text_to_read[45] = text_to_read.pop(83)
        text_to_read[32] = text_to_read[42] = text_to_read[43] = text_to_read[44] = ""

    if index == 63:
        found, text_to_read[13] = get_and_remove(r"{\\pard.+?\\par", text_to_read[13])
        text_to_read[12] = text_to_read[12].replace("}\\par", found)
        found, text_to_read[14] = get_and_remove(r"\\pard.+?\\column", text_to_read[14])
        text_to_read[11] = found + text_to_read[11]

    if index == 66:
        text_to_read[32], found = get_and_remove(r".+?\\par", text_to_read[32])
        text_to_read[6] += found
        found, text_to_read[50] = text_to_read[50].split("\\column", 1)
        text_to_read[17] += found
        found, text_to_read[17] = get_and_remove(r"}\\par.+", text_to_read[17])
        text_to_read[19] = found + text_to_read[19]
        text_to_read[23], t_536 = get_and_remove(r"{\\pard.+?\\cell}", text_to_read[23])
        found, text_to_read[26] = get_and_remove(r"\\column.+?\\par\\pard", text_to_read[26], count=1)
        text_to_read[23] = found.replace("REOPERA", "REOPERATION")
        found, text_to_read[24] = get_and_remove(r"\\f12\\fs.+", text_to_read[24])
        text_to_read[26] = text_to_read[26].replace("\\tab", found)
        found, text_to_read[25] = get_and_remove(r"{\\pard.+?\\cell}", text_to_read[25])
        text_to_read[26] = text_to_read[26].replace("776c2c5e26197f0345c3725f1620e35f0000000049454e44ae426082", "")
        text_to_read[26] = text_to_read[26].replace("\\f7\\fs22\\b0", found, 1)
        text_to_read[27] += text_to_read[51]
        text_to_read[28] += text_to_read[52] + text_to_read[53]
        text_to_read[29] += text_to_read[54]
        text_to_read[30] += text_to_read[55]
        text_to_read[51] = text_to_read[52] = text_to_read[52] = text_to_read[53] = text_to_read[54] = text_to_read[55] = ""
        found, text_to_read[42] = text_to_read[42].split("\\column")
        text_to_read[31] += found
        text_to_read[32] = "\\f16\\fs18\\b1\\i1\\expnd0\\expndtw0\\up0\\charscalex90 Excludes:\\expnd-2\\expndtw-8  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 replacement\\expnd-3\\expndtw-16  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 or\\expnd-3\\expndtw-17  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 removal\\expnd-3\\expndtw-16  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 of\\expnd-3\\expndtw-17  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw-2 tracheostomy\\cell}" + text_to_read[32]

        found, text_to_read[18] = get_and_remove(r"f7\\fs19.+", text_to_read[18])
        text_to_read[43] = "\\" + found + text_to_read[43]
        text_to_read[48] = "\\" + t_536 + text_to_read[48]
        note, text_to_read[47] = get_and_remove(r"}f4\\fs18\\b0.+?\\cell}\\row", text_to_read[47])
        text_to_read[22] += note
        text_to_read[47] += text_to_read[22]
        text_to_read[48] = text_to_read[48].replace("\\irow7", "f12\\fs19\\b1\\i0\\cf2 Tracheostomy\\cell}\\row" + text_to_read[24])
        text_to_read[49] = text_to_read[49].replace("\\par\\", "\\" + text_to_read[25])
        text_to_read[22] = text_to_read[25] = text_to_read[24] = ""

    if index == 67:
        found, text_to_read[22] = get_and_remove(r"{\\pard.+?\\cell}", text_to_read[22])
        text_to_read[11] += found
        text_to_read[22] = "\\" + text_to_read[22]
        found, text_to_read[22] = get_and_remove(r"\\f4\\fs18\\b0.+?\\column", text_to_read[22])
        text_to_read[11] += found
        found, text_to_read[23] = get_and_remove(r"\\f4\\fs18\\b0\\charscalex95\\cf2\sbron.+?\\column",
                                                 text_to_read[23])
        text_to_read[23] = text_to_read[23].replace("rigid", "rigid " + found)

    if index == 69:
        open_chest, text_to_read[3] = get_and_remove(r"\\f4\\fs18\\b0.+?\\par", text_to_read[3], count=1)
        found, text_to_read[26] = get_and_remove(r"{\\pard.+?\\column", text_to_read[26])
        include, text_to_read[3] = get_and_remove(r"\\f16\\fs18\\b1.+", text_to_read[3])
        text_to_read[5] = text_to_read[5].replace("\\column", found + include)
        text_to_read[4] += text_to_read[25]
        inclusion, text_to_read[7] = get_and_remove(r"\\f4\\fs18\\b0.+", text_to_read[7])
        text_to_read[5] += "\\f4\\fs18\\b0\\charscalex95\\cf2 Drainage of cyst or abscess\\par" + inclusion
        text_to_read[18] += text_to_read[36]
        text_to_read[19] += text_to_read[37]
        text_to_read[20] += text_to_read[38]
        text_to_read[21] += text_to_read[39]
        text_to_read[22] += text_to_read[40]
        text_to_read[25] = "\\f7\\fs19\\b0\\expnd0\\expndtw2\\charscalex115\\cf2 38438-01    \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 Lobectomy of\\expnd-4\\expndtw-18  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 lung\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li2688\\sl-216\\f4\\fs18\\b0\\cf2 Pneumonectomy:\\par\\pard\\plain\\s9\\ls510\\ilvl0\\nooverflow\\nocwrap\\lnbrkrule\\li2801\\fi-113\\ri1894\\sl232\\slmult1\\sb2\\tx2804\\f4\\fs18\\b0\\charscalex85\\cf2 completion, following previous removal of portion \\f4\\fs18\\b0\\i0\\charscalex95 of\\expnd0\\expndtw1  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 lung\\par\\pard\\plain\\s9\\ls510\\ilvl0\\nooverflow\\nocwrap\\lnbrkrule\\li2803\\fi-115\\sl-217\\tx2804\\f4\\fs18\\b0\\charscalex95\\cf2 partial\\par" + \
                           "\\f7\\fs19\\b0\\charscalex115\\cf2 38441-00 Radical lobectomy\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li2688\\sl-220\\f4\\fs18\\b0\\charscalex95\\cf2 Radical partial pneumonectomy\\par"
        text_to_read[27] = text_to_read[6] + text_to_read[27]
        found, text_to_read[7] = get_and_remove(r"{\\pard.+?\\column", text_to_read[7])
        text_to_read[28] = found + text_to_read[28]
        found, text_to_read[28] = get_and_remove(r"\\f4\\fs18.+", text_to_read[28])
        text_to_read[5] += found
        text_to_read[23] += "\\f7\\fs19\\b0\\charscalex115\\cf2 90170-00\\tab Lung volume reduction\\expnd2\\expndtw11  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 surgery\\par"
        text_to_read[36] = text_to_read[37] = text_to_read[38] = text_to_read[39] = text_to_read[40] = text_to_read[6] = ""
        found, text_to_read[17] = get_and_remove(r"\\f14\\fs15.+?\\column", text_to_read[17])
        text_to_read[34] += found

    if index == 71:
        text_to_read[14] += text_to_read[16]
        found, text_to_read[5] = get_and_remove(r"f7\\fs19\\b0.+?\\par", text_to_read[5])
        text_to_read[22] = "\\" + found + text_to_read[22]
        text_to_read[31] = text_to_read[15] +  text_to_read[31]
        text_to_read[22] = "\\f12\\fs19\\b1\\expnd1\\expndtw4\\charscalex111\\cf5{\\chcbpat2  \\expnd0\\expndtw0\\charscalex105 566\\tab }\\expnd0\\expndtw0\\charscalex105 \\tab \\f12\\fs19\\b1\\i0\\cf2 Other repair procedures on chest wall, mediastinum or\\expnd0\\expndtw-1  \\f12\\fs19\\b1\\i0\\expnd0\\expndtw0 diaphragm\\par" + text_to_read[22]
        text_to_read[11] = text_to_read[15] = text_to_read[16] = ""

    if index == 77:
        t_38760_01, text_to_read[3] = get_and_remove(r"\\tx7790\\f7\\fs19\\b0.+?\\column", text_to_read[3])
        text_to_read[14] += text_to_read[35]
        t_616 = "".join(text_to_read[39:43])
        found, text_to_read[43] = get_and_remove(r"{\\pard.+?\\column", text_to_read[43])
        t_616 += found
        text_to_read[35] = text_to_read[36] = text_to_read[39:43] = ""
        t_617 = text_to_read[43] + text_to_read[47] + text_to_read[48] + text_to_read[52] + text_to_read[53] + text_to_read[56]
        text_to_read[43] = text_to_read[47] = text_to_read[48] = text_to_read[52] = text_to_read[53] = text_to_read[56] = ""
        found, text_to_read[3] = get_and_remove(r"\\f14\\fs15\\b0.+?\\column", text_to_read[3])
        text_to_read[62] = text_to_read[62].replace("\\column", found.replace("\\column", ""), 1)
        text_to_read[62] = text_to_read[62].replace("\\column", t_38760_01 + found, 1)
        text_to_read[68] = text_to_read[68].replace("\\column", t_616) + t_617 + "\\f16\\fs18\\b1"
        found, text_to_read[60] = get_and_remove(r"^\\pard.+?\\par", text_to_read[60])
        text_to_read[68] = text_to_read[68].replace("septal\\cell}", "septal\\cell}" + found)

    if index == 79:
        found, text_to_read[9] = get_and_remove(r"{\\pard.+?\\par", text_to_read[9])
        text_to_read[7] += found

    if index == 80:
        text_to_read[0:2] = ""
        found, text_to_read[23] = get_and_remove(r"^\\pard.+?\\par", text_to_read[23])
        text_to_read[2] = text_to_read[2].replace("\\tab", found)
        t_637, text_to_read[4] = get_and_remove(r"{\\pard.+?\\par", text_to_read[4])
        t_637 += text_to_read[5]
        found, text_to_read[7] = get_and_remove(r"\\f7\\fs19.+?\\par", text_to_read[7])
        t_637 += found + text_to_read[8] + text_to_read[10] + text_to_read[14] + text_to_read[18] + text_to_read[19] + text_to_read[22]
        found, text_to_read[23] = get_and_remove(r"\\pard.+?,\\par", text_to_read[23])
        text_to_read[7] = text_to_read[7].replace("\\tab", found)
        found, text_to_read[2] = get_and_remove(r"\\f12\\fs22.+", text_to_read[2])
        text_to_read.append(found + t_637 + "\\f16\\fs18\\b1")
        text_to_read[23], _ = get_and_remove(r"\\column.+", text_to_read[23])
        text_to_read[5] = text_to_read[8] = text_to_read[10] = text_to_read[14] = text_to_read[18] = text_to_read[19] = text_to_read[22] = ""

    if index == 82:
        found, text_to_read[4] = get_and_remove(r"f7\\fs19\\b0.+", text_to_read[4])
        t_644, text_to_read[10] = get_and_remove(r"f12\\fs19.+", text_to_read[10])
        text, text_to_read[11] = get_and_remove(r"}f7\\fs19\\b0.+?\\column", text_to_read[11])
        t_644 += text.replace("}\\", "\\")
        text, text_to_read[11] = get_and_remove(r"\\sb97\\f7\\fs19.+?\\par", text_to_read[11])
        text_to_read[11] = text + text_to_read[11]
        t_38600, text_to_read[11] = get_and_remove(r"\\slmult1\\f7\\fs19\\b0.+?\\par", text_to_read[11])
        text_to_read[3] += t_38600
        text_to_read[28] += text_to_read[21] + "\\" + found
        t_646, text_to_read[28] = get_and_remove(r"\\f12\\fs19\\.+?\\cell}", text_to_read[28])
        found, text_to_read[8] = get_and_remove(r"f7\\fs19.+", text_to_read[8])
        text_to_read[33] = "\\" + found + text_to_read[33]
        text_to_read[35] = "\\" + t_644 + text_to_read[35]
        text_to_read[36] = "\\f7\\fs19\\b0\\i0\\expnd0\\expndtw2\\dn8 38647-00\\cell}" + text_to_read[36]
        t_38463_02, text_to_read[38] = get_and_remove(r"f7\\fs19.+", text_to_read[38])
        found, text_to_read[39] = get_and_remove(r"f7\\fs19.+", text_to_read[39])
        t_38463_02 = t_38463_02 + "\\" + found
        text_to_read[39] += t_38463_02
        text_to_read[45] = "{\\pard\\plain" + t_646 + "\\f12\\fs19\\b1\\cf2 Other excision procedures on pericardium\\cell}\\row"
        found, text_to_read[26] = get_and_remove(r"f7\\fs19.+?\\column", text_to_read[26], count=1)
        text_to_read[48] += "\\" + found
        text_to_read[50] = text_to_read[50].replace("776c2c5e26197f0345c3725f1620e35f0000000049454e44ae426082", "")
        _, text_to_read[26] = get_and_remove(r"\\par\\plain.+?\\par", text_to_read[26])
        _, text_to_read[35] = get_and_remove(r"f7\\fs19.+?\\cell}", text_to_read[35])
        text, text_to_read[37] = text_to_read[37].split("\\column")
        found, text_to_read[28] = get_and_remove(r"\\f11\\fs18\\b0.+?\\par{", text_to_read[28])
        text_to_read[44] += found + text
        text_to_read[21] = ""
        asc = re.search(r"\\f14\\fs15\\b0.+?\\par", text_to_read[11]).group()
        text_to_read[3] = text_to_read[3].replace("\\sb103", asc)

    if index == 85:
        t_90203_02, text_to_read[4] = get_and_remove(r"\\f7\\fs19\\b0.+?\\column", text_to_read[4], count=1)
        found, text_to_read[6] = get_and_remove(r"\\sb24\s\s\\f4\\fs18\\b0.+?\\par", text_to_read[6])
        text_to_read[6] = text_to_read[6].replace("Stabilisation", "Stabilisation " + found)
        text_to_read[8] = t_90203_02 + text_to_read[8]

    if index == 88:
        t_655, text_to_read[4] = get_and_remove(r"\\tab\s\\f12\\fs19.+?\\column", text_to_read[4])
        text_to_read[10] = t_655 + text_to_read[10]

    if index == 89:
        found, text_to_read[4] = get_and_remove(r"\\tab\s\\f7.+?\\column", text_to_read[4])
        text_to_read[6] = text_to_read[6].replace("not", found + " not")
        found, text_to_read[4] = get_and_remove(r"\\f14\\fs15\\b0.+?\\par", text_to_read[4], count=1)
        text_to_read[6] = text_to_read[6].replace("of \\column", "of " + found)
        found, text_to_read[4] = get_and_remove(r"\\f14\\fs15\\b0.+?\\par", text_to_read[4])
        text_to_read[6] = text_to_read[6].replace("procedure,", "procedure," + found)

    if index == 92:
        text_to_read[4] += text_to_read[12]
        text_to_read[5] += text_to_read[13]
        text_to_read[6] += text_to_read[14]
        text_to_read[12:15] = ""
        found, text_to_read[8] = get_and_remove(r"\\par\\plain.+?\\sb134", text_to_read[8])
        text_to_read[12] = text_to_read[12].replace("\\column", found, 1)

    if index == 93:
        text_to_read[4] = text_to_read[4].replace("\\tx1647\\f4\\fs18\\b0", "")
        found, text_to_read[4] = get_and_remove(r"\\tab\s\\cf5.+?\\column", text_to_read[4])
        text_to_read[6] = "\\f12\\fs19\\b1" + found + text_to_read[6]
        found, text_to_read[5] = get_and_remove(r"\\f14\\fs15\\b0\\charscalex110.+?\\par", text_to_read[5])
        text_to_read[6] = text_to_read[6].replace("coronary \\column", "coronary " + found)

    if index == 94:
        found, text_to_read[17] = get_and_remove(r"{\\pard.+?\\par", text_to_read[17])
        text_to_read[15] += found

    if index == 95:
        text_to_read[0:3] = ""
        text_to_read[4] = ""
        text_to_read[19] = "\\f12\\fs28\\b1\\charscalex95\\cf3 ARTERIES\\par\\" + text_to_read[19]
        found = re.search(r"\\f7\\fs19\\b0.+?\\cell}", text_to_read[19]).group()
        text_to_read[19] = re.sub(r"\\f7\\fs19\\b0.+?\\cell}", r"\\", text_to_read[19])
        text_to_read[3] += found
        text_to_read[19] = text_to_read[19].replace("}f12", "}\\f12")
        text_to_read[8] += text_to_read[20] + "\\f4\\fs18\\b0\\cf2 division\\tab \\f4\\fs18\\b0\\i0\\up2\\charscalex90 of patent\\expnd-4\\expndtw-21  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 ductus\\expnd-2\\expndtw-10  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 arteriosus ligation"
        text_to_read[20] = "{\\pard\\plain\\f12\\fs19\\b1\\cf5{\\chcbpat2 694\\tab }\\tab \\f12\\fs19\\b1\\i0\\cf2 Arterial\\expnd0\\expndtw2  \\f12\\fs19\\b1\\i0\\expnd0\\expndtw0 catheterisation\\cell}\\row"
        text_to_read[20] += "\\f14\\fs15\\b0\\i0\\up11\\charscalex100\\cf4 \\uc1\\u61553 ?\\f7 0042\\par\\pard\\plain\\intbl\\s10\\nooverflow\\nocwrap\\lnbrkrule\\li829\\sl154\\slmult1\\sb3\\tx4174\\tx5195\\f4\\fs18\\b0\\dn8\\cf2 ligation\\tab \\f7\\fs19\\b0\\i0\\up0\\charscalex105 13303-00\\tab Umbilical \\f7\\fs19\\b0\\i0\\expnd0\\expndtw2 artery\\expnd-1\\expndtw-7  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 catheterisation/\\par\\pard\\plain\\intbl\\s10\\nooverflow\\nocwrap\\lnbrkrule\\li4174\\sl-164\\tx5195\\f14\\fs15\\b0\\up4\\charscalex115\\cf4 \\uc1\\u61553 ?\\f7 1615\\tab \\f7\\fs19\\b0\\i0\\up0\\cf2 cannulation in\\expnd1\\expndtw5  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 neonate\\cell}\\row"
        text_to_read[16], _ = get_and_remove(r"{\\pard.+?\\column", text_to_read[16])

    if index == 96:
        text_to_read[0:2] = ""
        text_to_read[50] += "".join(text_to_read[54: 86])
        text_to_read[54: 86] = ""
        exclude, text_to_read[52] = get_and_remove(r"\s\\charscalex100.+", text_to_read[52])
        text_to_read[52] += "".join(text_to_read[2: 37])
        text_to_read[2: 37] = ""
        text_to_read[15] += "".join(text_to_read[20:28])
        text_to_read[20: 28] = ""
        text_to_read[18] += "".join(text_to_read[3:15])
        text_to_read[3: 15] = ""
        text_to_read[6] += exclude

    if index == 100:
        t_32763_08 = "".join(text_to_read[10:12])
        text_to_read[10:12] = ""
        t_32763_00 = text_to_read.pop(14)
        text = text_to_read.pop(13)
        t_32763_00 = text + t_32763_00
        t_712 = text_to_read[16] + text_to_read[17]
        t_32763_09 = text_to_read[21] + text_to_read[22]
        text_to_read[20] = text_to_read[41] + text_to_read[20]
        t_32763_10 = text_to_read[26] + text_to_read[27] + text_to_read[30]
        t_32763_10 += "".join(text_to_read[33:41])
        text_to_read[16] = text_to_read[17] = text_to_read[21] = text_to_read[22] = text_to_read[41] = text_to_read[26] = text_to_read[27] = text_to_read[30] = ""
        text_to_read[33:41] = ""
        text_to_read[35], text = text_to_read[35].split("\\column")
        text_to_read[35] += t_32763_08 + t_32763_00
        text_to_read.append(t_712 + text)
        text_to_read.append(t_32763_09 + t_32763_10)
        text_to_read[18] = text_to_read[18].replace("776c2c5e26197f0345c3725f1620e35f0000000049454e44ae426082}} ", "")

    if index == 101:
        text_to_read[19] += text_to_read[45]
        text_to_read[20] += text_to_read[46]
        text_to_read[21] += text_to_read[47]
        text_to_read[22] += text_to_read[48]
        text_to_read[23] += text_to_read[49]
        t_32708_00 = text_to_read[24]
        t_32708_01 = text_to_read[25]
        t_32708_02 = text_to_read[26]
        t_32708_03 = text_to_read[27]
        t_32708_04 = text_to_read[28]
        text_to_read[45] = text_to_read[46] = text_to_read[47] = text_to_read[48] = ""
        text_to_read[24:29] = ""
        found, text_to_read[17] = get_and_remove(r"f7\\fs19\\b0\\i0.+?\\par", text_to_read[17])
        text_to_read[36] += "\\" + found
        text_to_read[45] = t_32708_00 + text_to_read[45]
        text_to_read[46] = t_32708_01 + text_to_read[46]
        text_to_read[47] = t_32708_02 + text_to_read[47]
        text_to_read[48] = t_32708_03 + text_to_read[48]
        text_to_read[49] = t_32708_04 + text_to_read[49]
        text_to_read[18] += "\\f16\\fs18\\b1\\i1\\charscalex90\\cf2 Excludes: \\f4\\fs18\\b0\\i0 composite [vein and synthetic] graft \\f4\\fs18\\b0\\i0\\charscalex100 (32754-02 \\f5\\fs18\\b1\\i0 [713]\\f4\\b0 )\\par"
        text_to_read[49] = text_to_read[49].replace("\\cell}", " procedure using synthetic material  \\cell}")
        text_to_read[44] = ""

    if index == 103:
        found, text_to_read[7] = get_and_remove(r"{\\pard.+?\\par", text_to_read[7])
        text_to_read[5] += found
        found, text_to_read[39] = get_and_remove(r"\\f7\\fs19\\b0.+?\\par", text_to_read[39])
        text_to_read[37] += found
        text_to_read[36] = text_to_read[40].split("\\column")[0] + "\\f12\\fs19\\b1\\i0\\cf2 Other procedures on\\expnd1\\expndtw7  \\f12\\fs19\\b1\\i0\\expnd0\\expndtw0 arteries\\par" + text_to_read[36]
        text_to_read[21] = text_to_read[40] = ""

    if index == 104:
        text_to_read[0:2] = ""
        text_to_read[1] = "\\f7\\fs19\\b0\\charscalex115\\cf2 35330-00 Percutaneous insertion of inferior vena\\par" + text_to_read[1]
        text_to_read[15] += text_to_read[40]
        text_to_read[16] += text_to_read[41]
        text_to_read[17] += text_to_read[42]
        text_to_read[18] += text_to_read[43]
        text_to_read[19] += text_to_read[44]
        text_to_read[20] += text_to_read[45]
        text_to_read[21] += text_to_read[46]
        text_to_read[22] += text_to_read[47]
        text_to_read[23] += text_to_read[48]
        text_to_read[24] += text_to_read[49]
        text_to_read[7] = text_to_read[8] = ""
        text_to_read[40:50] = ""
        dest, text_to_read[40] = get_and_remove(r"\\f12\\fs22.+", text_to_read[40])
        text_to_read[25] += text_to_read[40]
        dest = dest + text_to_read[41]
        text_to_read[28] = dest + text_to_read[28]
        text_to_read[40] = text_to_read[41] = ""
        text = "{\\pard\\plain\\intbl\\s10\\nooverflow\\nocwrap\\lnbrkrule\\li169\\ri244\\sl-400\\sb7\\tx1190\\f7\\fs19\\b0\\expnd-1\\expndtw-3\\charscalex115\\cf2 34106-15\\tab \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 Interruption of brachial vein 34106-16\\tab Interruption of radial vein \\f7\\fs19\\b0\\i0\\expnd-1\\expndtw-3 34106-17\\tab \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 Interruption of ulnar vein \\f7\\fs19\\b0\\i0\\expnd1\\expndtw5 34800-00 \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 Interruption of vena cava \\f7\\fs19\\b0\\i0\\expnd-1\\expndtw-4 34103-17\\tab \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 Interruption of iliac\\expnd2\\expndtw9  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 vein\\cell}\\"
        text_to_read.insert(34, text)
        text_to_read[41] = "{\\pard\\plain\\f7\\fs19\\b0\\i0\\up0 34106-19\\tab Interruption of other\\expnd2\\expndtw10  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 vein\\cell}"

    if index == 106:
        text_to_read.pop(6)
        text_to_read[13] = ""
        text_to_read[13] = text_to_read[57] + "\\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 Direct closure of other upper limb vein\\par \\f7\\fs19\\b0\\i0\\expnd0\\expndtw2 33833-04 \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 Direct closure of renal\\expnd7\\expndtw37  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 vein\\par"
        text_to_read[16], found = get_and_remove(r"{\\pard.+?\\par", text_to_read[16])
        text_to_read[17], text = get_and_remove(r"{\\pard.+?\\par", text_to_read[17])
        text_to_read[17] += found + text
        text_to_read[18], found = get_and_remove(r"{\\pard.+?\\par", text_to_read[18])
        text_to_read[19], text = get_and_remove(r"{\\pard.+?\\par", text_to_read[19])
        text_to_read[19] += found + text
        text_to_read[20] = text_to_read[57] = ""
        found, text_to_read[62] = get_and_remove(r"\\sl-230\\f7\\fs19\\b0.+?\\cell}", text_to_read[62])
        text_to_read[27] = text_to_read[75] + text_to_read[27] + found
        text_to_read[43] = "\\f7\\fs19\\b0\\expnd0\\expndtw2\\charscalex110\\cf2 33833-06\\par" + text_to_read[43]
        found, text_to_read[55] = get_and_remove(r"{\\pard.+?\\par", text_to_read[55])
        text, text_to_read[56] = get_and_remove(r"{\\pard.+?\\par", text_to_read[56])
        text_to_read[55] = found + text + text_to_read[55]
        text_to_read[56] = text_to_read[56].replace("interpositi", "interposition")
        text_to_read[28] += text_to_read[63]
        text_to_read[63] = """\\f7\\fs19\\b0\\charscalex105\\cf2 33839-05\\cell}{\\pard\\plain\\intbl\\s10\\nooverflow\\nocwrap\\lnbrkrule\\li97\\sl240\\slmult1\\sb86\\f7\\fs19\\b0\\charscalex115\\cf2 Repair of portal vein by interposition graft\\cell}"""
        text_to_read[75] = ""
        text_to_read[27] = text_to_read[27].replace("sl-198", " anastomosis ")

    if index == 107:
        text_to_read.pop(0)
        found, text_to_read[19] = get_and_remove(r"^\\pard.+?\\par", text_to_read[19])
        text_to_read[3] += found
        found, text_to_read[3] = get_and_remove(r"\\f14\\fs15\\b0.+?\\column", text_to_read[3])
        text_to_read[22] = text_to_read[22].replace("in \\column", "in " + found)
        text_to_read[22] = text_to_read[22].replace("/ \\column", "/ " + found)

    if index == 109:
        text_to_read[5] += text_to_read[7] + text_to_read[8]
        t_45033_03 = text_to_read[6]
        t_45033_06, text_to_read[15] = get_and_remove(r"}f7\\fs19.+", text_to_read[15])
        text_to_read[24] = text_to_read[24].replace("\\cell}", " or thrombosis after intra-abdominal vascular procedure \\cell}")
        text_to_read[29] = t_45033_03 + text_to_read[29]
        found, text_to_read[12] = get_and_remove(r"}f7.+", text_to_read[12])
        text_to_read[35] = found.replace("}f7", "\\f7") + text_to_read[35]
        text_to_read[38] = t_45033_06.replace("}f7", "\\f7") + text_to_read[38]
        _, text_to_read[45] = get_and_remove(r"\\sl-98\\f7\\fs19\\b0.+?\\column", text_to_read[45])
        text_to_read[45] = text_to_read[45].replace("\cell}f7", "\\f7")
        text_to_read[44] = "\\f7\\fs19\\b0\\i0\\up0 34115-00\\cell}" + text_to_read[44]
        text_to_read[7] = text_to_read[8] = text_to_read[6] = text_to_read[25] = ""

    if index == 113:
        found, text_to_read[4] = get_and_remove(r"\\f4\\fs18\\b0.+?\\column", text_to_read[4], count=1)
        text_to_read[4] = text_to_read[4].replace("0030\\par", "0030\\par transplantation " + found)
        _, text_to_read[4] = get_and_remove(r"\\f7\\fs19\\b0\\charscalex115\\cf2\str.+?\\par", text_to_read[4])

    if index == 115:
        text_to_read[6] = text_to_read[6].replace("\\f7\\fs22\\b0", "")
        found = re.search(r"\\f14\\fs15\\b0.+?\\par", text_to_read[3]).group()
        text_to_read[6] = text_to_read[6].replace("\\column", found, 1)

    if index == 116:
        found, text_to_read[7] = get_and_remove(r"sl-174.+?\\column", text_to_read[7])
        text_to_read[7] = text_to_read[7].replace("\\sl-83", found)
        found, text_to_read[4] = get_and_remove(r"\\f12\\fs22\\b1\\i0\\char.+?\\par", text_to_read[4])
        text_to_read[8] = found + text_to_read[8]

    if index == 117:
        text_to_read[4] = "\\f12\\fs22\\b1\\cf2 EXAMINATION\\par" + text_to_read[4]
        t_30532_00 = text_to_read.pop(17)
        _, text_to_read[17] = get_and_remove(r"^\\pard.+?\\par", text_to_read[17])
        text_to_read[22] = text_to_read[22].replace("\\ri-14", t_30532_00)

    if index == 123:
        text_to_read[3], inclusion = text_to_read[3].split("\\column")
        found, inclusion = get_and_remove(r"\\f16\\fs18.+?\\par", inclusion)
        text_to_read[9] = inclusion + found
        text_to_read[17] += text_to_read[12]
        text_to_read[12] = ""
        text = """\\f4\\fs18\\b0\\i0\\charscalex90 may\\expnd-3\\expndtw-15  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 be\\expnd-3\\expndtw-14  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 performed\\expnd-3\\expndtw-14  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 as\\expnd-3\\expndtw-14  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 the\\expnd-3\\expndtw-14  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 second\\expnd-3\\expndtw-14  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 stage\\expnd-3\\expndtw-14  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 of\\expnd-3\\expndtw-14  \\f4\\fs18\\b0\\i0\\expnd-4\\expndtw-19 a \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0\\charscalex95 two-stage\\expnd0\\expndtw-2  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 surgery\\par"""
        found = re.search(r"\\f11\\fs18.+\\sb54", text_to_read[10]).group()
        text_to_read[18] = text_to_read[18].replace("\\column", text + found, 1)

    if index == 125:
        text_to_read[3], inclusion = text_to_read[3].split("\\column")
        text_to_read[10] += inclusion
        text_to_read[13] = text_to_read[13].replace("removal", " removal procedures on small intestine ")
        text = text_to_read[32]
        text_to_read[32] = text_to_read[33] = ""
        found, text_to_read[11] = get_and_remove(r"{\\pard.+?\\column", text_to_read[11])
        text_to_read[39] = found + text_to_read[39]
        text_to_read[39] = text_to_read[39].replace("\\cell}\\row", " prosthesis \\cell}")
        text_to_read[40] = text_to_read[40].replace("\\column", text)
        text_to_read[40] = text_to_read[40].replace("intestinef7", "intestine\\f7")
        found, text_to_read[29] = get_and_remove(r"}f7.+", text_to_read[29])
        text_to_read[55] = found.replace("}f7", "\\f7") + text_to_read[55]
        _, text_to_read[40] = get_and_remove(r"\\f7\\fs19\\b0\\charscalex110\\cf2.+?\\par", text_to_read[40])

    if index == 126:
        _, text_to_read[0] = get_and_remove(r"\\f4\\fs18\\b0.+?\\par", text_to_read[0])
        t_30382_01 = text_to_read[19]
        t_30382_00 = text_to_read[20]
        t_30375_19, text_to_read[21] = get_and_remove(r"{\\pard.+?\\cell}", text_to_read[21])
        text_to_read[19] = text_to_read[20] = ""
        text_to_read[23] = text_to_read[23].replace("intestinef7", " intestine\\f7")
        text_to_read[38] = t_30382_01 + text_to_read[38]
        text_to_read[42] = t_30382_00 + text_to_read[42]
        text_to_read[46] = t_30375_19 + text_to_read[46]
        text_to_read[7] = text_to_read[24] + text_to_read[7]
        text_to_read[24] = ""
        text_to_read[23] = text_to_read[23].replace("single", "single anastomoses ")

    if index == 127:
        text_to_read.pop(0)
        text_to_read.pop(0)
        found, text_to_read[2] = get_and_remove(r"\\tab.+?\\par", text_to_read[2])
        found = "\\f12\\fs22\\b1" + found + text_to_read[17] + text_to_read[18] + text_to_read[19] + text_to_read[20] + text_to_read[8] + text_to_read[21]
        t_32023_02 = text_to_read[11]
        text_to_read[11] = found
        text, text_to_read[27] = get_and_remove(r"^\\pard.+?\\par", text_to_read[27])
        found, text_to_read[9] = get_and_remove(r"{\\pard.+?\\cell}", text_to_read[9])
        text_to_read[11] += found + text_to_read[22] + text_to_read[23] + text +  t_32023_02 + text_to_read[24]
        text_to_read[17] = text_to_read[18] = text_to_read[19] = text_to_read[20] = text_to_read[8] = text_to_read[21] = \
            text_to_read[22] = text_to_read[23] = text_to_read[24] = ""
        text_to_read[13] += text_to_read[25]
        text_to_read[14] += text_to_read[26]
        text_to_read[25] = text_to_read[26] = ""

    if index == 128:
        inclusion, text_to_read[9] = get_and_remove(r"\\sl-221\s\s\\column\s\\par.+", text_to_read[9])
        found, text_to_read[19] = get_and_remove(r"\\pard.+?\\column", text_to_read[19])
        split_text = text_to_read[19].split("\\column")
        text_to_read[18] += found + inclusion.replace("\\sb94", split_text[0])
        text_to_read[18] += text_to_read[10] + split_text[1]
        text_to_read[10] = text_to_read[19] = ""

    if index == 129:
        text_to_read[6] = re.sub(r"f4\\fs18\\b0\\charscalex85\\cf2\s\s\\column\s","", text_to_read[6])

    if index == 131:
        text_to_read[26] += text_to_read[30] + text_to_read[31] + text_to_read[34] + text_to_read[35] + text_to_read[39]
        text_to_read[30] = text_to_read[31] = text_to_read[34] = text_to_read[35] = text_to_read[39] = ""
        text_to_read[31], text_to_read[41] = get_and_remove(r"^\\pard.+?\\par", text_to_read[41])

    if index == 135:
        text_to_read[29], text_to_read[40] = get_and_remove(r"^\\pard.+?\\par", text_to_read[40])
        text_to_read[40], _ = get_and_remove(r"\\sl-220\\f4\\fs18\\b0.+\\f4\\b0\s\)\\par", text_to_read[40])

    if index == 136:
        found, text_to_read[4] = get_and_remove(r"\\tab\s\\f12\\fs22\\b1.+?\\column", text_to_read[4])
        text_to_read[15] = text_to_read[15].replace("\\column", found, 1)
        text = text_to_read[6] + text_to_read[7] + text_to_read[9] + text_to_read[10] + text_to_read[12] + text_to_read[13]
        text_to_read.append(text)
        text_to_read[6] = text_to_read[7] = text_to_read[9] = text_to_read[10] = text_to_read[12] = text_to_read[13] = ""

    if index == 137:
        t_30451_01, text_to_read[12] = get_and_remove(r"f7\\fs19\\b0\\i0\\dn.+", text_to_read[12])
        text_to_read[13] = text_to_read[13].replace("(DACP)", "Duodenoscope-assisted cholangiopancreatoscopy (DACP)").replace("}f12", "}\\f12")
        t_961, text_to_read[13] = get_and_remove(r"\\f12\\fs19.+?\\par", text_to_read[13])
        t_90348_00 = text_to_read[14]
        found, text_to_read[9] = get_and_remove(r"}f7.+", text_to_read[9])
        text_to_read[22] = found.replace("}f7", "\\f7") + text_to_read[22]
        found, text_to_read[10] = get_and_remove(r"}f7.+", text_to_read[10])
        text_to_read[23] = found.replace("}f7", "\\f7") + text_to_read[23]
        text_to_read[25] = "\\" + t_30451_01 + text_to_read[25]
        text_to_read[26] = t_961 + text_to_read[26]
        text_to_read[27] = t_90348_00 + text_to_read[27]
        text_to_read[14] = ""

    if index == 138:
        text_to_read.pop(0)
        text_to_read[0] = ""
        found, text_to_read[3] = get_and_remove(r"\\tab\s\\f12\\fs22.+?\\par", text_to_read[3])
        t_30440_01, text_to_read[14] = get_and_remove(r"\\f7\\fs19.+", text_to_read[14])
        text_to_read[15] = text_to_read[15].replace("\\sb162", t_30440_01)
        text_to_read[17] += text_to_read[37]
        text_to_read[18] += text_to_read[38]
        text_to_read[20] = found + text_to_read[20]
        text_to_read[26] = text_to_read[10] + text_to_read[26]
        text_to_read[37] = text_to_read[38] = text_to_read[10] = ""

    if index == 140:
        text_to_read[4] += text_to_read[17]
        text_to_read[5] += text_to_read[18]
        text_to_read[3] += text_to_read[16]
        _, text_to_read[7] = get_and_remove(r"\\f2\\fs18\\b1.+?\\par", text_to_read[7])
        text_to_read[8] = text_to_read[15] + text_to_read[19] + text_to_read[8] + text_to_read[20]
        text_to_read[9] += text_to_read[21]
        text_to_read[10] += text_to_read[22]
        text_to_read[11] += text_to_read[23]
        t_30586_00 = text_to_read[12]
        text_to_read[12] = """\\f12\\fs19\\b1\\expnd1\\expndtw4\\charscalex111\\cf5{\\chcbpat2  \\expnd0\\expndtw0\\charscalex105 979\\tab }\\expnd0\\expndtw0\\charscalex105 \\tab \\f12\\fs19\\b1\\i0\\cf2 Other excision procedures on pancreas or pancreatic\\expnd1\\expndtw4  \\f12\\fs19\\b1\\i0\\expnd0\\expndtw0 duct\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li1333\\fi-1022\\ri1707\\sl228\\slmult1\\sb177\\f7\\fs19\\b0\\expnd0\\expndtw2\\charscalex115\\cf2 90294-01 \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 Endoscopic excision of lesion of pancreas or pancreatic\\expnd1\\expndtw4  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 duct\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li1333\\fi-1022\\ri2200\\sl228\\slmult1\\sb179\\f7\\fs19\\b0\\charscalex115\\cf2 30578-00 Excision of lesion of pancreas or pancreatic duct\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li1333\\sl240\\slmult1\\sb51\\f16\\fs18\\b1\\i1\\cf2 Includes: \\f4\\fs18\\b0\\i0 exploration\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li1333\\fi-1022\\ri2230\\sl228\\slmult1\\sb178\\tx1333\\f7\\fs19\\b0\\charscalex115\\cf2 30577-00\\tab Major pancreatic or\\expnd-5\\expndtw-23  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 retropancreatic dissection\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li1333\\sl-220\\sb51\\tx2070\\f16\\fs18\\b1\\i1\\cf2 Note:\\tab \\f4\\fs18\\b0\\i0 Performed\\expnd0\\expndtw-2  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 for:\\par\\pard\\plain\\s9\\ls245\\ilvl0\\nooverflow\\nocwrap\\lnbrkrule\\li2183\\fi-113\\sl-216\\tx2185\\f4\\fs18\\b0\\charscalex95\\cf2 abscess formation\\par"""
        text_to_read[12] += """\\pard\\plain\\s9\\ls245\\ilvl0\\nooverflow\\nocwrap\\lnbrkrule\\li2183\\fi-113\\sl-220\\tx2185\\f4\\fs18\\b0\\charscalex95\\cf2 pancreatic necrosis\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\sl240\\slmult1\\sb10\\f4\\fs16\\b0\\i0\\par\\pard\\plain\\s6\\nooverflow\\nocwrap\\lnbrkrule\\li312\\sl240\\slmult1\\f12\\fs22\\b1\\charscalex95\\cf2 REPAIR\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\sl240\\slmult1\\f12\\fs19\\b1\\i0\\par\\pard\\plain\\s8\\nooverflow\\nocwrap\\lnbrkrule\\li312\\sl240\\slmult1\\tx1106\\tx1333\\f12\\fs19\\b1\\expnd1\\expndtw4\\charscalex111\\cf5{\\chcbpat2  \\expnd0\\expndtw2\\charscalex105 980\\tab }\\expnd0\\expndtw2\\charscalex105 \\tab \\f12\\fs19\\b1\\i0\\expnd0\\expndtw0\\cf2 Anastomosis of\\expnd1\\expndtw4  \\f12\\fs19\\b1\\i0\\expnd0\\expndtw0 pancreas\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li1333\\sl-220\\sb43\\tx2070\\f16\\fs18\\b1\\i1\\cf2 Note:\\tab \\f4\\fs18\\b0\\i0 Performed\\expnd0\\expndtw-2  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 for:\\par\\pard\\plain\\s9\\ls245\\ilvl0\\nooverflow\\nocwrap\\lnbrkrule\\li2183\\fi-113\\sl-216\\tx2185\\f4\\fs18\\b0\\charscalex95\\cf2 pancreatic cyst\\par\\pard\\plain\\s9\\ls245\\ilvl0\\nooverflow\\nocwrap\\lnbrkrule\\li2183\\fi-113\\sl-216\\tx2185\\f4\\fs18\\b0\\charscalex95\\cf2 pancreatitis\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li1333\\sl-216\\f16\\fs18\\b1\\i1\\cf2 Excludes: \\f4\\fs18\\b0\\i0 cholecystopancreatostomy\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li2183\\sl-216\\f4\\fs18\\b0\\cf2 (30460-02\\expnd1\\expndtw6  \\f5\\fs18\\b1\\i0\\expnd0\\expndtw0 [969]\\f4\\b0 )\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li2183\\fi-114\\ri2774\\sl232\\slmult1\\sb1\\f4\\fs18\\b0\\charscalex85\\cf2 choledochopancreatostomy \\f4\\fs18\\b0\\i0\\charscalex100 (30460-06 \\f5\\fs18\\b1\\i0 [969]\\f4\\b0 )\\par"""
        text_to_read[12] += t_30586_00
        text_to_read[13] = text_to_read[24] + text_to_read[13] + text_to_read[25]
        text = """\\f7\\fs19\\b0\\expnd1\\expndtw3\\charscalex110\\cf2 30589-00   \\expnd9\\expndtw45  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 Pancreaticojejunostomy\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li1333\\sl-220\\sb49\\f16\\fs18\\b1\\i1\\cf2 Excludes: \\f4\\fs18\\b0\\i0 that with:\\par\\pard\\plain\\s9\\ls245\\ilvl0\\nooverflow\\nocwrap\\lnbrkrule\\li2183\\fi-113\\ri2195\\sl232\\slmult1\\sb1\\tx2185\\f4\\fs18\\b0\\charscalex90\\cf2 anastomosis\\expnd-2\\expndtw-12  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 to\\expnd-2\\expndtw-11  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 Roux-en-Y\\expnd-2\\expndtw-11  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 loop\\expnd-2\\expndtw-11  \\f4\\fs18\\b0\\i0\\expnd-2\\expndtw-9 of \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0\\charscalex100 jejunum (30587-00\\expnd-2\\expndtw-10  \\f5\\fs18\\b1\\i0\\expnd0\\expndtw0 [980]\\f4\\b0 )\\par\\pard\\plain\\s9\\ls245\\ilvl0\\nooverflow\\nocwrap\\lnbrkrule\\li2183\\fi-113\\ri2726\\sl232\\slmult1\\tx2185\\f4\\fs18\\b0\\charscalex85\\cf2 pancreaticoduodenectomy \\f4\\fs18\\b0\\i0\\charscalex100 (30584-00 \\f5\\fs18\\b1\\i0 [978]\\f4\\b0 )\\par"""
        text_to_read.append(text)
        text_to_read[17] = text_to_read[18] = text_to_read[16] = text_to_read[15] = text_to_read[19] = text_to_read[20] \
            = text_to_read[21] = text_to_read[22] = text_to_read[23] = text_to_read[24] = text_to_read[25] = ""
        text_to_read[11] += """\\f16\\fs18\\b1\\i1\\cf2 Includes: \\f4\\fs18\\b0\\i0 choledochoenterostomy gastrojejunostomy pancreaticojejunostomy preservation of pylorus\\cell}"""

    if index == 141:
        found, text_to_read[5] = get_and_remove(r"}f7.+", text_to_read[5])
        text, text_to_read[6] = get_and_remove(r"}f14.+", text_to_read[6])
        text_to_read[22] = found.replace("}f7", "\\f7") + text_to_read[22]
        text_to_read[23] = text.replace("}f14", "\\f14") + text_to_read[23]
        text_to_read[23] += """\\f16\\fs18\\b1\\i1\\charscalex95\\cf2 Note:\\tab \\f4\\fs18\\b0\\i0\\charscalex90 Performed\\expnd-4\\expndtw-18  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 for\\expnd-3\\expndtw-17  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 control\\expnd-3\\expndtw-17  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 of\\expnd-3\\expndtw-17  \\f4\\fs18\\b0\\i0\\expnd-1\\expndtw-3 postoperative \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0\\charscalex95 haemorrhage\\cell}"""

    if index == 142:
        found, text_to_read[5] = get_and_remove(r"\\sl-116\s\s\\f4\\fs18\\b0.+?\\column", text_to_read[5])
        text_to_read[5] = text_to_read[5].replace("peritonitis", " peritonitis " + found)

    if index == 145:
        t_90329_02, text_to_read[10] = get_and_remove(r"}f7.+", text_to_read[10])
        found, text_to_read[49] = get_and_remove(r"\\pard.+?\\column", text_to_read[49])
        text_to_read[13] = found + text_to_read[13]
        text_to_read[5] += text_to_read[7]
        t_45570_00 = text_to_read[6]
        t_90329_03, text_to_read[12] = get_and_remove(r"{\\pard.+?\\column", text_to_read[12])
        found, text_to_read[14] = get_and_remove(r"{\\pard.+?\\par", text_to_read[14])
        text_to_read[13] = text_to_read[13].replace("\\column", found)
        t_43867_01 = text_to_read[29]
        text_to_read[33] = t_45570_00 + text_to_read[33]
        text_to_read[39] = t_90329_03 + text_to_read[39]
        text_to_read[56] = t_43867_01 + text_to_read[56]
        _, text_to_read[40] = get_and_remove(r"^\\pard.+?\\par", text_to_read[40])
        text_to_read[7] = text_to_read[6] = text_to_read[29] = ""

    if index == 146:
        text_to_read.pop(0)

    if index == 149:
        text_to_read[15] += "\\f7\\fs19\\b0\\charscalex115\\cf2 Endoscopic fragmentation of calculus of kidney\\par"
        text_to_read[15] += """\\f16\\fs18\\b1\\i1\\cf2 Includes: \\f4\\fs18\\b0\\i0 cystoscopy\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li2180\\sl-216\\f4\\fs18\\b0\\charscalex95\\cf2 fragmentation by:\\par\\pard\\plain\\s9\\ls548\\ilvl0\\nooverflow\\nocwrap\\lnbrkrule\\li2180\\sl-216\\tx2296\\f4\\fs18\\b0\\charscalex95\\cf2 electrohydraulic\\expnd-2\\expndtw-10  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 shockwaves\\par\\pard\\plain\\s9\\ls548\\ilvl0\\nooverflow\\nocwrap\\lnbrkrule\\li2180\\sl-216\\tx2296\\f4\\fs18\\b0\\charscalex90\\cf2 laser\\par\\pard\\plain\\s9\\ls548\\ilvl0\\nooverflow\\nocwrap\\lnbrkrule\\li2180\\ri1461\\sl232\\slmult1\\sb2\\tx2296\\f4\\fs18\\b0\\charscalex95\\cf2 ultrasound manipulation \\f4\\fs18\\b0\\i0\\charscalex85 retrograde \\f4\\fs18\\b0\\i0\\expnd-1\\expndtw-3 pyeloscopy \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0\\charscalex95 ureteroscopy\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li2180\\sl-215\\f4\\fs18\\b0\\charscalex95\\cf2 urethral dilation\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li1443\\sl-220\\sb49\\f16\\fs18\\b1\\i1\\cf2 Excludes: \\f4\\fs18\\b0\\i0 percutaneous fragmentation\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li2294\\sl-216\\f4\\fs18\\b0\\cf2 (36639-01\\expnd2\\expndtw9  \\f5\\fs18\\b1\\i0\\expnd0\\expndtw0 [1041]\\f4\\b0 )\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li2294\\fi-114\\ri823\\sl232\\slmult1\\sb1\\f4\\fs18\\b0\\charscalex90\\cf2 that\\expnd-2\\expndtw-12  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 with\\expnd-2\\expndtw-12  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 extraction\\expnd-2\\expndtw-12  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 of\\expnd-2\\expndtw-12  \\f4\\fs18\\b0\\i0\\expnd-1\\expndtw-3 calculus \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0\\charscalex100 (36656-03 \\f5\\fs18\\b1\\i0 [1041]\\f4\\b0 )\\par"""
        text_to_read[16] += """\\f7\\fs19\\b0\\charscalex115\\cf2 Endoscopic extraction of calculus of kidney\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li1443\\sl-220\\sb51\\f16\\fs18\\b1\\i1\\cf2 Includes: \\f4\\fs18\\b0\\i0 cystoscopy\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li2180\\ri1309\\sl232\\slmult1\\sb1\\f4\\fs18\\b0\\charscalex95\\cf2 manipulation \\f4\\fs18\\b0\\i0\\charscalex85 retrograde pyeloscopy \\f4\\fs18\\b0\\i0\\charscalex95 ureteroscopy\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li2180\\sl-216\\f4\\fs18\\b0\\charscalex95\\cf2 urethral dilation\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li1443\\sl-220\\sb49\\f16\\fs18\\b1\\i1\\cf2 Excludes: \\f4\\fs18\\b0\\i0 percutaneous extraction\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li2294\\sl-216\\f4\\fs18\\b0\\cf2 (30450-01\\expnd2\\expndtw9  \\f5\\fs18\\b1\\i0\\expnd0\\expndtw0 [1041]\\f4\\b0 )\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li2294\\fi-114\\ri1309\\sl232\\slmult1\\sb2\\f4\\fs18\\b0\\charscalex90\\cf2 that with\\expnd-6\\expndtw-31  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw-2 fragmentation \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0\\charscalex100 (36656-03\\expnd0\\expndtw1  \\f5\\fs18\\b1\\i0\\expnd0\\expndtw0 [1041]\\f4\\b0 )\\par"""
        text_to_read[13] += """\\f4\\fs18\\b0\\cf2 extraction\\expnd-5\\expndtw-25  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 of\\expnd-5\\expndtw-25  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 calculus\\expnd-5\\expndtw-25  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 (30450-01\\expnd-5\\expndtw-24  \\f5\\fs18\\b1\\i0\\expnd0\\expndtw0 [1041]\\f4\\b0 )\\par\\pard\\plain\\intbl\\s10\\ls262\\ilvl0\\nooverflow\\nocwrap\\lnbrkrule\\li1904\\fi-114\\sl-216\\tx1906\\f4\\fs18\\b0\\charscalex95\\cf2 fragmentation:\\par\\pard\\plain\\intbl\\s10\\ls262\\ilvl1\\nooverflow\\nocwrap\\lnbrkrule\\li2017\\fi-113\\ri1171\\sl232\\slmult1\\sb1\\tx2019\\f4\\fs18\\b0\\charscalex90\\cf2 and\\expnd-3\\expndtw-16  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 extraction\\expnd-3\\expndtw-15  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 of\\expnd-3\\expndtw-15  \\f4\\fs18\\b0\\i0\\expnd-1\\expndtw-3 calculus \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0\\charscalex100 (36639-02 \\f5\\fs18\\b1\\i0 [1041]\\f4\\b0 )\\par\\pard\\plain\\intbl\\s10\\ls262\\ilvl1\\nooverflow\\nocwrap\\lnbrkrule\\li2018\\fi-114\\sl-217\\tx2019\\f4\\fs18\\b0\\charscalex95\\cf2 calculus (36639-01\\expnd2\\expndtw11  \\f5\\fs18\\b1\\i0\\expnd0\\expndtw0 [1041]\\f4\\b0 )\\par"""

    if index == 150:
        text_to_read[4], text_to_read[10] = get_and_remove(r"^\\pard.+?\\par", text_to_read[10])

    if index == 151:
        found,  text_to_read[22] = get_and_remove(r"{\\pard.+?\\par", text_to_read[22])
        text = text_to_read[18] + text_to_read[19] + found + text_to_read[21] + text_to_read[22]
        text_to_read[17] = text_to_read[28] + text_to_read[29] + text_to_read[33] + text_to_read[34] + text_to_read[38] \
                           + text_to_read[42] + text_to_read[43] + text_to_read[47]
        text_to_read[18] = text
        text_to_read[19] = text_to_read[21] = text_to_read[22] = text_to_read[28] = text_to_read[29] \
            = text_to_read[33] = text_to_read[34] = text_to_read[38] = text_to_read[42] = text_to_read[43] = text_to_read[47] = ""

        found, text_to_read[3] = get_and_remove(r"\\f14\\fs15.+?\\par", text_to_read[3])
        text_to_read[25] += found
        text_to_read[29], text_to_read[49] = get_and_remove(r"^\\pard.+?\\par", text_to_read[49])

    if index == 152:
        found, text_to_read[3] = get_and_remove(r"\\column\\par.+", text_to_read[3])
        text = text_to_read[4] + text_to_read[5]
        text_to_read[4] = text_to_read[5] = ""
        t_13100_06, text_to_read[8] = get_and_remove(r"}f7.+", text_to_read[8])
        t_13100_07, text_to_read[10] = get_and_remove(r"\\f7\\fs19.+", text_to_read[10])
        text_to_read[10] += """\\f7\\fs19\\b0\\charscalex110\\cf2 36558-01\\cell}{\\pard\\plain\\intbl\\s10\\nooverflow\\nocwrap\\lnbrkrule\\li33\\sl-320\\tx5134\\f7\\fs19\\b0\\charscalex115\\cf2 Excision of\\expnd-1\\expndtw-3  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 renal\\expnd0\\expndtw-1  \\f7\\fs19\\b0\\i0\\expnd1\\expndtw3 cyst"""
        text_to_read[10] += text
        t_90353_01, text_to_read[12] = get_and_remove(r"}f7.+?\\par", text_to_read[12])
        text, text_to_read[6] = get_and_remove(r"}f7.+", text_to_read[6])
        found, text_to_read[22] = get_and_remove(r"\\column.+", text_to_read[22])
        text_to_read[23] = text.replace("}f7", "\\f7") + text_to_read[23]
        text_to_read[24] = "\\f12\\fs19\\b1\\i0\\expnd0\\expndtw0 1061\\charscalex100 \\tab }\\cell}" + text_to_read[24] + t_13100_06.replace("}f7", "\\f7")
        text_to_read[26] = t_13100_07 + text_to_read[26]
        text_to_read[26] = text_to_read[26].replace("long", " long term ")
        text_to_read[26] += """"\\f4\\fs18\\b0\\charscalex90\\cf2 Intermittent peritoneal dialysis [IPD] \\f4\\fs18\\b0\\i0\\charscalex100 Tidal dialysis\\par"""
        code_also = text_to_read[27]
        text = """\\f7\\fs19\\b0\\cf2 13100-08\\tab \\f7\\fs19\\b0\\i0\\charscalex105 Continuous peritoneal \\f7\\fs19\\b0\\i0\\charscalex100 dialysis, long term \\f4\\fs18\\b0\\i0\\charscalex90 Continuous\\expnd-3\\expndtw-15  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 ambulatory\\expnd-3\\expndtw-14  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 peritoneal\\expnd-3\\expndtw-15  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 dialysis\\expnd-3\\expndtw-14  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 [CAPD] \\f4\\fs18\\b0\\i0\\charscalex95 Continuous\\expnd-4\\expndtw-19  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 cycling\\expnd-4\\expndtw-18  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 peritoneal\\expnd-4\\expndtw-18  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 dialysis\\expnd-4\\expndtw-18  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 [CCPD]\\par\\pard\\plain\\s8\\nooverflow\\nocwrap\\lnbrkrule\\li1432\\fi-1022\\ri2373\\sl213\\slmult1\\sb179\\tx1205\\tx1432\\f12\\fs19\\b1\\expnd1\\expndtw4\\charscalex111\\cf5{\\chcbpat2  \\expnd0\\expndtw0\\charscalex100 1062\\tab }\\expnd0\\expndtw0\\charscalex100 \\tab \\f12\\fs19\\b1\\i0\\cf2 Procedures for establishment or maintenance of peritoneal\\expnd-2\\expndtw-9  \\f12\\fs19\\b1\\i0\\expnd0\\expndtw0 dialysis\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li1432\\fi-1022\\ri1986\\sl228\\slmult1\\sb178\\tx1432\\f7\\fs19\\b0\\expnd-1\\expndtw-4\\charscalex115\\cf2 13112-00\\tab \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 Establishment of peritoneal dialysis by abdominal puncture and insertion of temporary\\expnd0\\expndtw2  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 catheter\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li1432\\fi-1022\\ri2286\\sl228\\slmult1\\sb179\\tx1432\\f7\\fs19\\b0\\charscalex115\\cf2 90351-00\\tab Removal of temporary catheter for peritoneal\\expnd0\\expndtw2  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 dialysis\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li1432\\fi-1021\\ri2262\\sl228\\slmult1\\sb179\\tx1432\\f7\\fs19\\b0\\charscalex115\\cf2 13109-00\\tab Insertion and fixation of indwelling peritoneal catheter for long term peritoneal\\expnd0\\expndtw2  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 dialysis\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li1431\\sl240\\slmult1\\sb51\\f16\\fs18\\b1\\i1\\cf2 Includes: \\f4\\fs18\\b0\\i0 Tenckhoff catheter\\par"""
        text_to_read[27] = text + """\\f7\\fs19\\b0\\charscalex115\\cf2 13109-01\\tab Replacement of indwelling peritoneal catheter for peritoneal\\expnd1\\expndtw5  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 dialysis\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li1545\\fi-114\\ri1733\\sl232\\slmult1\\f4\\fs18\\b0\\charscalex85\\cf2 Removal and reinsertion of indwelling peritoneal \\f4\\fs18\\b0\\i0\\charscalex95 catheter for chronic peritoneal dialysis\\par"""
        text_to_read[27] += """\\f7\\fs19\\b0\\charscalex115\\cf2 13110-00\\tab Removal of indwelling peritoneal catheter for peritoneal\\expnd1\\expndtw3  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 dialysis\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li1431\\sl240\\slmult1\\sb51\\f16\\fs18\\b1\\i1\\cf2 Excludes: \\f4\\fs18\\b0\\i0 that with replacement (13109-01 \\f5\\fs18\\b1\\i0 [1062]\\f4\\b0 )\\par"""
        text = """\\f12\\fs19\\b1\\expnd1\\expndtw4\\charscalex111\\cf5{\\chcbpat2  \\expnd0\\expndtw0\\charscalex100 1063\\tab }\\expnd0\\expndtw0\\charscalex100 \\tab \\f12\\fs19\\b1\\i0\\cf2 Other interventions for renal\\expnd5\\expndtw26  \\f12\\fs19\\b1\\i0\\expnd0\\expndtw0 dialysis\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li411\\sl-228\\sb163\\tx1432\\f7\\fs19\\b0\\charscalex115\\cf2 13104-00\\tab Education and training for home\\expnd3\\expndtw14  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 dialysis\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li1432\\sl-216\\f4\\fs18\\b0\\charscalex95\\cf2 Education and training for:\\par\\pard\\plain\\s9\\ls266\\ilvl0\\nooverflow\\nocwrap\\lnbrkrule\\li1547\\fi-115\\sl-216\\tx1548\\f4\\fs18\\b0\\charscalex95\\cf2 haemodialysis\\par\\pard\\plain\\s9\\ls266\\ilvl0\\nooverflow\\nocwrap\\lnbrkrule\\li1547\\fi-115\\sl-220\\tx1548\\f4\\fs18\\b0\\charscalex85\\cf2 peritoneal\\expnd-2\\expndtw-8  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 dialysis\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li411\\sl240\\slmult1\\sb168\\f7\\fs19\\b0\\expnd0\\expndtw2\\charscalex115\\cf2 90353-00   \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 Test for haemodialysis\\expnd-3\\expndtw-13  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 adequacy\\par"""
        text_to_read[28] = text + code_also + t_90353_01.replace("}f7", "\\f7") + text_to_read[28]

    if index == 153:
        text_to_read.pop(0)
        text_to_read.pop(0)
        text_to_read[20], text_to_read[21] = text_to_read[20].split("\\column")
        found, text_to_read[10] = get_and_remove(r"{\\pard.+?\\par", text_to_read[10])
        text, text_to_read[15] = get_and_remove(r"{\\pard.+?\\par", text_to_read[15])
        text_2, text_to_read[15] = get_and_remove(r"^\\pard.+?\\column", text_to_read[15])
        text_to_read[20] += text_to_read[4] + text_to_read[5] + found + text_to_read[9] + text_to_read[10] + text + text_to_read[14] + text_2
        text_to_read[4] = text_to_read[5] = text_to_read[9] = text_to_read[10] = text_to_read[14]= ""
        found, text_to_read[27] = get_and_remove(r"^\\pard.+?\\par", text_to_read[27])
        text_to_read[22] = found + text_to_read[22]
        text_to_read[24], text_to_read[26] = get_and_remove(r"{\\pard.+?\\par", text_to_read[26])

    if index == 154:
        excision, text_to_read[11] = get_and_remove(r"\\f12\\fs22\\b1.+?\\par", text_to_read[11])
        text_to_read[11] = text_to_read[11].replace("\\tx1773", excision)
        text_to_read[13] = text_to_read[13].replace("ureterf7", "ureter\\f7")
        replacement, text_to_read[13] = get_and_remove(r"\\f4\\fs18.+", text_to_read[13])
        found, text_to_read[6] = get_and_remove(r"}f7.+", text_to_read[6])
        text_to_read[16] = found.replace("}f7", "\\f7") + text_to_read[16]

    if index == 155:
        text_to_read[4] += text_to_read[31]
        text_to_read[5] += text_to_read[32]
        text_to_read[6] += text_to_read[33]
        text_to_read[34], found = get_and_remove(r"\\f12\\fs19.+", text_to_read[34])
        text_to_read[7] += found
        text_to_read[9] += text_to_read[34]
        text_to_read[23] += """\\f7\\fs19\\b0\\dn13\\cf2 36803-01         Endoscopic  dilation\\expnd2\\expndtw12  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 of \\expnd1\\expndtw6  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 ureter\\f16\\fs18\\b1\\i1\\cf2 Includes:\\expnd-5\\expndtw-26  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 cystoscopy urethral dilation\\f7\\fs19\\b0\\up1\\charscalex115\\cf2 36621-00\\tab Closure of\\expnd-1\\expndtw-7  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 cutaneous\\expnd-1\\expndtw-3  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 ureterostomy"""
        found, _ = get_and_remove(r"\\column.+", text_to_read[29])
        text_to_read[29] = text_to_read[43] + found
        text = """\\f16\\fs18\\b1\\i1\\dn11 Excludes: \\f4\\fs18\\b0\\i0 replacement\\expnd-1\\expndtw-5  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 of:\\cell}\\f4\\fs18\\b0\\i0\\up0 \\'95\\expnd-7\\expndtw-33  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 cystostomy\\expnd-6\\expndtw-32  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 tube\\expnd-6\\expndtw-32  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 (36800-02\\expnd-6\\expndtw-32  \\f5\\fs18\\b1\\i0\\expnd0\\expndtw0 [1092]\\f4\\b0 )\\cell}\\f4\\fs18\\b0\\i0\\up0\\charscalex100 \\'95\\expnd-6\\expndtw-28  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 ureterostomy\\expnd-6\\expndtw-28  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 tube\\expnd-6\\expndtw-28  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 (90367-00\\expnd-6\\expndtw-28  \\f5\\fs18\\b1\\i0\\expnd0\\expndtw0 [1069]\\f4\\b0 )\\cell}\\f7\\fs19\\b0\\i0\\expnd1\\expndtw4\\up0 36800-03 \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 Endoscopic removal of indwelling\\expnd1\\expndtw3  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 urinary catheter\\cell}\\f16\\fs18\\b1\\i1\\up0\\charscalex95 Excludes:\\expnd-1\\expndtw-3  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 that\\expnd-3\\expndtw-14  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 with\\expnd-3\\expndtw-14  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 replacement\\expnd-3\\expndtw-14  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 (36800-01\\expnd-3\\expndtw-14  \\f5\\fs18\\b1\\i0\\expnd0\\expndtw0 [1090]\\f4\\b0 )\\par"""
        text_to_read[39] += text
        text_to_read[39] += """\\f12\\fs19\\b1\\i0\\cf5{\\chcbpat2 1091\\tab }\\tab \\f12\\fs19\\b1\\i0\\cf2 Implantation or removal of\\expnd2\\expndtw10  \\f12\\fs19\\b1\\i0\\expnd0\\expndtw0 electronic bladder stimulator\\par"""
        text_to_read[40] = """\\f7\\fs19\\b0\\i0\\up0 90359-00 Implantation of electronic\\expnd-1\\expndtw-6  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 bladder stimulator\\par""" + text_to_read[40]
        text_to_read[43] = text_to_read[31] = text_to_read[32] = text_to_read[33] = text_to_read[34] = ""

    if index == 156:
        text_to_read.pop(0)
        text_to_read.pop(0)
        t_36842_00, text_to_read[6] = get_and_remove(r"\\f7\\fs19.+", text_to_read[6])
        text_to_read[7] = text_to_read[7].replace("\\sb178", t_36842_00)
        t_36845_06, text_to_read[8] = get_and_remove(r"}f7.+?\\par", text_to_read[8])
        incision, text_to_read[9] = get_and_remove(r"\\f12\\fs22\\b1.+?\\par", text_to_read[9])
        text_to_read[9] = text_to_read[9].replace("\\sb98", incision)
        t_30075_10 = text_to_read[10]
        text_to_read[10] = text_to_read[34] + """\\f12\\fs19\\b1\\i0\\cf2 Cystolithotomy\\par"""
        found, text_to_read[12] = get_and_remove(r"{\\pard.+?\\par", text_to_read[12])
        text_to_read[11] = text_to_read[11].replace("\\sb168", found)
        text_to_read[24] = t_36845_06.replace("}f7", "\\f7") + text_to_read[24]
        text_to_read[27] = t_30075_10.replace("}f7", "\\f7") + text_to_read[27]
        text_to_read[34] = ""
        found, text_to_read[33] = get_and_remove(r"{\\pard.+?\\par", text_to_read[33])
        text_to_read[31] += found

    if index == 159:
        text_to_read[4] = text_to_read[33] + text_to_read[4]
        t_35523_00, text_to_read[9] = get_and_remove(r"}f7.+", text_to_read[9])
        include, text_to_read[15] = get_and_remove(r"\\sb92\\f16\\fs18\\b1.+?\\par", text_to_read[15])
        text_to_read[9] += include
        t_1116 = text_to_read[12]
        t_37372_00 = text_to_read[22]
        t_37800_00, text_to_read[24] = get_and_remove(r"{\\pard.+?\\column", text_to_read[24])
        text_to_read[25] = text_to_read[10] + text_to_read[34] + text_to_read[35]
        text_to_read[25] += text_to_read[11] + text_to_read[36] + "\\f12\\fs22\\b1\\charscalex95\\cf2 DESTRUCTION\\par" + t_1116 + text_to_read[37]
        text = "".join(text_to_read[26:33])
        text_to_read[26] = text_to_read[13]
        text_to_read[33] = text_to_read[12] = text_to_read[22] = text_to_read[10] = text_to_read[34] = \
            text_to_read[35] = text_to_read[36] = text_to_read[37] = text_to_read[13] = ""
        text_to_read[27:33] = ""
        found, text_to_read[15] = get_and_remove(r"{\\pard.+?\\column", text_to_read[15])
        text_to_read[32] += text_to_read[14] + found
        text_to_read[33] = text_to_read[33].replace("\\column", text).replace("}f12", "\\f12").replace("\\sb84", t_35523_00.replace("}f7", "\\f7")).replace("sphincterf16", "sphincter\\f16")
        text_to_read[14] = text_to_read[11] = ""
        text_to_read[35] = t_37372_00 + text_to_read[35]
        text_to_read[36] = t_37800_00 + text_to_read[36]
        text_to_read[34] += "\\f7\\fs19\\b0\\i0\\expnd0\\expndtw2\\up0 37369-00 \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 Excision of prolapse of\\expnd-5\\expndtw-25  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 urethra\\cell}"

    if index == 161:
        found, text_to_read[9] = get_and_remove(r"{\\pard.+?\\par", text_to_read[9])
        text_to_read[7] += found

    if index == 162:
        text_to_read[29], text_to_read[31] = get_and_remove(r"{\\pard.+?\\par", text_to_read[31])

    if index == 163:
        text_to_read.pop(0)
        text_to_read.pop(0)
        text_to_read[2] = "\\f12\\fs22\\b1\\cf2 APPLICATION, INSERTION, REMOVAL\\par" + text_to_read[2]
        t_37604_02 = text_to_read.pop(7)
        _, text_to_read[17] = get_and_remove(r"^\\pard.+?\\par", text_to_read[17])
        text_to_read[22] = text_to_read[22].replace("sb179", t_37604_02)
        text_to_read[25] = text_to_read[25].replace("\\f4\\fs20\\b0", "")

    if index == 165:
        text_to_read[20] = text_to_read[5] + text_to_read[20]
        text_to_read[12], text = text_to_read[12].split("\\sb168")
        found, text_to_read[24] = get_and_remove(r"\\sb8\\f7\\fs19\\.+", text_to_read[24])
        text_to_read[14] = text + found + text_to_read[14]
        found, text_to_read[24] = get_and_remove(r"{\\pard.+?\\cell}", text_to_read[24])
        text, text_to_read[24] = get_and_remove(r"\\row.+?\\par\\", text_to_read[24])
        text_to_read[19] += text_to_read[9] + found + text_to_read[10] + text_to_read[11] + text.replace("}f7", "}\\f7")
        text_to_read[5] = text_to_read[9] = text_to_read[10] = text_to_read[11] = ""

    if index == 166:
        found, text_to_read[28] = text_to_read[28].split("\\column")
        text_to_read[4] = found +  text_to_read[4]
        text_to_read[13], text_to_read[27] = get_and_remove(r"\\tx5949\\f4\\fs18\\b0.+?\\cell}", text_to_read[27])
        text_to_read[13] = "{\\pard\\plain" + text_to_read[13]
        found, text_to_read[32] = get_and_remove(r"{\\pard.+?\\column", text_to_read[32])
        text_to_read[16] += text_to_read[31] + found
        found, text_to_read[17] = get_and_remove(r"{\\pard.+?\\column", text_to_read[17])
        text_to_read[16] = text_to_read[16].replace("\\sb162", found)
        text_to_read[27] = text_to_read[27].replace("}f7", "}\\f7")
        text_to_read[31] = "\\f12\\fs22\\b1\\charscalex95\\cf2 INCISION\\par"

    if index == 167:
        found, text_to_read[104] = get_and_remove(r"\\f12\\fs22\\b1.+?\\par", text_to_read[104])
        text_to_read[104] = text_to_read[104].replace("\\sb78", found)
        text_to_read[4] = "".join(text_to_read[90:107])
        text_to_read[90:107] = ""
        text_to_read.pop(90)

    if index == 168:
        text_to_read.pop(0)

    if index == 169:
        text = text_to_read[9] + text_to_read[10] + text_to_read[14]
        found, text_to_read[19] = get_and_remove(r"{\\pard.+?\\cell}", text_to_read[19])
        t_35710_00 = text_to_read[18] + found
        text_to_read[78] = text_to_read[78].replace("\\column  \\f16", text + t_35710_00 + "\\f16")
        text_to_read[9] = text_to_read[10] = text_to_read[14] = text_to_read[18] = ""

    if index == 171:
        text_to_read[38] = text_to_read[19] + text_to_read[38]
        text_to_read[26] = text_to_read[6] + text_to_read[26]
        text_to_read[6] = text_to_read[19] = ""

    if index == 172:
        incision, text_to_read[3] = get_and_remove(r"\\f12\\fs22\\b1\\c.+?\\par", text_to_read[3])
        exclude, text_to_read[3] = get_and_remove(r"\\f4\\fs18.+", text_to_read[3])
        text_to_read[8] += exclude + incision
        text_to_read[24] = text_to_read[9] + text_to_read[24]
        text_to_read[25] = text_to_read[10] + text_to_read[25]
        text_to_read[26] = text_to_read[11] + text_to_read[26]
        text_to_read[27] = text_to_read[12] + text_to_read[27]
        text_to_read[28] = text_to_read[13] + text_to_read[28]
        text_to_read[29] = text_to_read[14] + text_to_read[29]
        found, text_to_read[16] = get_and_remove(r"{\\pard.+?\\column", text_to_read[16])
        text_to_read[31] = text_to_read[15] + found + text_to_read[31]
        text_to_read[22], found = get_and_remove(r"\\f7\\fs19.+", text_to_read[22])
        text_to_read[20] += found
        found, text_to_read[31] = get_and_remove(r"\\f16\\fs18\\b1.+?\\column", text_to_read[31])
        text_to_read[23] += found
        text_to_read[9] = text_to_read[10] = text_to_read[11] = text_to_read[12] = text_to_read[13] = text_to_read[14] = text_to_read[15] = text_to_read[17] = ""

    if index == 174:
        inclusion, text_to_read[5] = get_and_remove(r"{\\pard.+?\\par", text_to_read[5])
        inclusion = inclusion.replace("Strassman", "Repair of bicornuate uterus Strassman")
        text_to_read[3] += inclusion
        found, text_to_read[7] = get_and_remove(r"{\\pard.+?\\par", text_to_read[7])
        text_to_read[5] += found
        t_35618_00, text_to_read[9] = get_and_remove(r"}f7.+", text_to_read[9])
        text_to_read[44] = text_to_read[12] + text_to_read[44]
        text_to_read[46] = text_to_read[14] + text_to_read[46]
        text_to_read[55] = text_to_read[24] + text_to_read[55]
        text_to_read[30] += text_to_read[60]
        text_to_read[31] += text_to_read[61]
        text_to_read[32] += text_to_read[62] + text_to_read[63]
        text_to_read[40] = t_35618_00.replace("}f7", "\\f7") + text_to_read[40]
        found, text_to_read[49] = get_and_remove(r"{\\pard.+?\\par", text_to_read[49])
        text_to_read[47] += found
        found, text_to_read[27] = get_and_remove(r"}f7.+", text_to_read[27])
        text_to_read[58] = found.replace("}f7", "\\f7") + text_to_read[58]
        text_to_read[59] = text_to_read[59].replace("cell}f11", "f11")
        text_to_read[12] = text_to_read[14] = text_to_read[24] = text_to_read[61] = text_to_read[62] = \
            text_to_read[60] = text_to_read[63] = ""

    if index == 175:
        text_to_read[10] = text_to_read[10].replace("\\sb2\\f12\\fs19\\b1\\i0", "")

    if index == 176:
        text_to_read[4] += """\\f4\\fs18\\b0\\dn7\\charscalex95\\cf2 Donald-Fothergill\\f4\\fs18\\b0\\dn4\\cf2 Le\\expnd-3\\expndtw-16  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 Fort\\tab \\f4\\fs18\\b0\\i0\\dn2 procedure\\f4\\fs18\\b0\\dn7\\cf2 Manchester\\tab"""
        found, text_to_read[25] = get_and_remove(r"{\\pard.+?\\par", text_to_read[25])
        text_to_read[6] += found
        found, text_to_read[26] = get_and_remove(r"{\\pard.+?cell}", text_to_read[26])
        text_to_read[7] += found
        text_to_read[9] = text_to_read[9].replace("vaginal", "vaginal approach")
        text_to_read[10] = ""
        found, text_to_read[27] = get_and_remove(r"{\\pard.+?cell}", text_to_read[27])
        text_to_read[11] += found
        text_to_read[15] += text_to_read[28]
        text_to_read[28] = ""
        _, text_to_read[22] = get_and_remove(r"{\\pard.+?cell}", text_to_read[22])
        text_to_read[24] = text_to_read[24].replace("proceduref4", "procedure\\f4")
        text_to_read[26] = "\\" + text_to_read[26].replace("}f12", "}\\f12")
        found, text_to_read[24] = get_and_remove(r"\\f4\\fs18\\b0\\i0\\up10.+", text_to_read[24])
        text_to_read[24] +=  """\\f7\\fs19\\b0\\i0\\up0\\charscalex105 35565-00 Vaginal\\expnd1\\expndtw7  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 reconstruction\\par\\f16\\fs18\\b1\\i1\\up0 Note:\\tab \\f4\\fs18\\b0\\i0 Performed\\expnd-1\\expndtw-4  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 for:\\f4\\fs18\\b0\\i0\\up0 \\'95 congenital\\expnd-4\\expndtw-20  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 absence\\cell}""" + found
        text_to_read[27] = "{\\pard\\plain\\" + text_to_read[27]
        text_to_read[27] += "\\f12\\fs22\\b1\\i0 DESTRUCTION\\cell}"
        found, text_to_read[32] = get_and_remove(r"{\\pard.+?\\par", text_to_read[32])
        text_to_read[30] += found

    if index == 177:
        text_to_read[3] = text_to_read[3].replace("\\sb5", text_to_read[4])
        text_to_read[9], text_to_read[11] = get_and_remove(r"{\\pard.+?\\par", text_to_read[11])
        _, text_to_read[10] = get_and_remove(r"{\\pard.+?\\par", text_to_read[10])
        text_to_read[4] = ""

    if index == 178:
        found, text_to_read[4] = get_and_remove(r"\\f14\\fs15.+?\\par", text_to_read[4])
        text_to_read[7] = text_to_read[7].replace("\\column", found, 1)

    if index == 180:
        text_to_read[3] = text_to_read[3].replace("\\f1\\fs18\\b1\\charscalex120\\cf5 1333\\par", "")
        text_to_read[3] = text_to_read[3].replace("form.\\par", "form.\\par\\f1\\fs18\\b1")
        text_to_read[5:10] = ""
        text_to_read[9] = text_to_read[10] = ""

    if index == 182:
        text_to_read[19], found = text_to_read[19].split("\\column", 1)
        text_to_read[19] += text_to_read[16] + text_to_read[17] + text_to_read[18] + found
        text_to_read[16] = text_to_read[17] = text_to_read[18] = ""
        text_to_read[22] = text_to_read[8] + text_to_read[22]
        text_to_read[23] = text_to_read[9] + text_to_read[23]
        text_to_read[24] = text_to_read[10] + text_to_read[24]
        text_to_read[25] = text_to_read[11] + text_to_read[25]
        text_to_read[8] = text_to_read[9] = text_to_read[10] = text_to_read[11] = ""
        text = """\\f4\\fs18\\b0\\charscalex95\\cf2 Needling of hydrocephalic head\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li1009\\sl240\\slmult1\\sb168\\f7\\fs19\\b0\\charscalex110\\cf2 90477-00 Other procedures to assist delivery\\par"""
        text_to_read.append(text)

    if index == 186:
        found, text_to_read[27] = get_and_remove(r"{\\pard.+?\\par", text_to_read[27])
        text_to_read[9] += found
        text_to_read[14] = text_to_read[28] + text_to_read[14]
        found, text_to_read[14] = get_and_remove(r"^\\cell.+?\\par", text_to_read[14])
        text_to_read[26] = text_to_read[26].replace("fixationf7", "fixation\\f7")
        text_to_read[28] = """\\f12\\fs19\\b1\\i0\\up0\\charscalex100\\cf5{\\chcbpat2 1367\\tab }\\tab \\f12\\fs19\\b1\\i0\\cf2 Reduction of fracture of mandibular\\expnd3\\expndtw17  \\f12\\fs19\\b1\\i0\\expnd0\\expndtw0 or\\cell}\\f12\\fs19\\b1\\i0\\up0 maxillary alveolar\\expnd3\\expndtw13  \\f12\\fs19\\b1\\i0\\expnd0\\expndtw0 ridge\\par"""

    if index == 187:
        note, text_to_read[69] = get_and_remove(r"^\\par.+?\\column", text_to_read[69])
        text_to_read[67] += text_to_read[69]
        text_to_read[68] += note
        text_to_read[69] = ""

    if index == 190:
        found, text_to_read[6] = get_and_remove(r"\\f7\\fs19\\b0.+", text_to_read[6])
        text_to_read[11] = text_to_read[11].replace("48651-00\\tab", "\\f7\\fs19\\b0\\expnd1\\expndtw5\\charscalex115\\cf2 48651-00 \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0")
        other_proc = text_to_read[12]
        text_to_read[13] += text_to_read[21]
        text_to_read[14] += text_to_read[22]
        text_to_read[15] += text_to_read[23] + found
        found, text_to_read[17] = get_and_remove(r"\\f14\\fs15\\b0\\up5.+", text_to_read[17])
        text_to_read[20] = other_proc + text_to_read[20].replace("}f12", "\\f12") + found
        text_to_read[12] = text_to_read[21] = text_to_read[22] = text_to_read[23]= ""
        text_to_read[21] = """\\f11\\fs18\\b0\\i1\\cf2 Code also when performed:\\par\\pard\\plain\\s9\\ls566\\ilvl0\\nooverflow\\nocwrap\\lnbrkrule\\li2193\\fi-113\\ri1949\\sl232\\slmult1\\sb1\\tx2195\\f4\\fs18\\b0\\charscalex90\\cf2 procurement\\expnd-4\\expndtw-19  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 of\\expnd-4\\expndtw-18  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 fat\\expnd-4\\expndtw-19  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 for\\expnd-4\\expndtw-19  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 graft\\expnd-4\\expndtw-18  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 via\\expnd-4\\expndtw-19  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 separate\\expnd-4\\expndtw-18  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 incision \\f4\\fs18\\b0\\i0\\charscalex95 (45018-04\\expnd1\\expndtw3  \\f5\\fs18\\b1\\i0\\expnd0\\expndtw0 [1666]\\f4\\b0 )\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li1059\\sl-228\\sb169\\f7\\fs19\\b0\\charscalex110\\cf2 35400-00 Vertebroplasty, 1 vertebral body\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li2193\\fi-114\\ri1791\\sl232\\slmult1\\sb1\\f4\\fs18\\b0\\charscalex90\\cf2 Injection of polymethylmethacrylate [PMMA] into \\f4\\fs18\\b0\\i0\\charscalex95 1 vertebral body\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li2080\\sl240\\slmult1\\sb50\\f16\\fs18\\b1\\i1\\cf2 Includes: \\f4\\fs18\\b0\\i0 bilateral (bipedicular) injection\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li1059\\sl-238\\sb158\\f7\\fs19\\b0\\charscalex110\\cf2 35400-01 Vertebroplasty, \\f13\\fs19\\b0\\i0 \\uc1\\u61619 ?\\f0  \\f7\\fs19\\b0\\i0 2 vertebral bodies\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li2193\\fi-114\\ri1791\\sl232\\slmult1\\sb1\\f4\\fs18\\b0\\charscalex90\\cf2 Injection of polymethylmethacrylate [PMMA] into \\f4\\fs18\\b0\\i0\\charscalex95 2 or more vertebral bodies\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li2080\\sl240\\slmult1\\sb50\\f16\\fs18\\b1\\i1\\cf2 Includes: \\f4\\fs18\\b0\\i0 bilateral (bipedicular) injection\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li2080\\fi-1021\\ri2431\\sl228\\slmult1\\sb177\\tx2080\\f7\\fs19\\b0\\charscalex115\\cf2 50616-00\\tab Revision of spinal procedure with adjustment of spinal\\expnd2\\expndtw12  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 fixation\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li2080\\fi-1021\\ri1665\\sl228\\slmult1\\sb180\\tx2080\\f7\\fs19\\b0\\charscalex115\\cf2 50616-01\\tab Revision of spinal procedure with removal of spinal\\expnd1\\expndtw6  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 fixation\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li2080\\fi-1021\\ri1919\\sl228\\slmult1\\sb179\\tx2079\\f7\\fs19\\b0\\charscalex115\\cf2 50616-02\\tab Revision of spinal procedure with bone graft\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li1058\\sl240\\slmult1\\sb170\\f7\\fs19\\b0\\charscalex115\\cf2 50620-00 Other revision of spinal procedure\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li2080\\sl-220\\sb49\\f16\\fs18\\b1\\i1\\cf2 Includes: \\f4\\fs18\\b0\\i0 fusion\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li2766\\ri3896\\qc\\sl-220\\f4\\fs18\\b0\\charscalex95\\cf2 osteotomy\\par"""

    if index == 192:
        t_1404 = text_to_read[9]
        t_48957, text_to_read[10] = get_and_remove(r"\\f7\\fs19.+", text_to_read[10])
        _, text_to_read[11] = get_and_remove(r"\\slmult1\\f7\\fs19\\b0.+?\\sb10", text_to_read[11])
        text_to_read[12] += text_to_read[28]
        text_to_read[13] += text_to_read[29]
        found, text_to_read[15] = get_and_remove(r"{\\pard.+\\cell}", text_to_read[15])
        text_to_read[14] += found
        text_to_read[13] = text_to_read[13].replace("\\row", text_to_read[14])
        found, text_to_read[31] = get_and_remove(r"\\pard.+\\cell}", text_to_read[31])
        text_to_read[14] = text_to_read[30] + found
        text_to_read[23] = t_1404 + text_to_read[23]
        text_to_read[24] = t_48957 + text_to_read[24]
        found, text_to_read[26] = get_and_remove(r"\\pard.+\\cell}", text_to_read[26])
        text_to_read[4] += found
        text_to_read[9] = text_to_read[28] = text_to_read[29] = text_to_read[30] = ""

    if index == 195:
        _, text_to_read[3] = get_and_remove(r"^\\pard.+?\\par\\plain", text_to_read[3])
        text = text_to_read[5] + text_to_read[19] + text_to_read[6] + text_to_read[20] + text_to_read[7] + text_to_read[21] + text_to_read[8] + text_to_read[9]
        text_to_read[3] = text_to_read[3].replace("\\column", text, 1)
        text_to_read[15] += text_to_read[25].replace("}f12", "}\\f12")
        _, text_to_read[16] = get_and_remove(r"{\\pard.+?\\column", text_to_read[16])
        found, _ = get_and_remove(r"^\\pard.+?\\column", text_to_read[27])
        text_to_read[22] += found + """\\f12\\fs19\\b1\\i0\\cf2 Other incision procedures on\\expnd1\\expndtw4  \\f12\\fs19\\b1\\i0\\expnd0\\expndtw0 forearm\\par"""
        text_to_read[23] += """\\f7\\fs19\\b0\\charscalex115\\cf2 Tenolysis of flexor or extensor tendon of forearm or wrist\\par"""
        found, text_to_read[16] = get_and_remove(r"\\f12\\fs19.+?forearm\s", text_to_read[16])
        text_to_read[26] = text_to_read[26].replace("\\tab", found)
        found, text_to_read[16] = get_and_remove(r"\\f7\\fs19\\b0.+?joint", text_to_read[16])
        text_to_read[26] = text_to_read[26].replace("\\sb168", found, 1)
        found, text_to_read[16] = get_and_remove(r"Ostectomy of radius\\par", text_to_read[16])
        text_to_read[26] = text_to_read[26].replace("\\sb168", "\\f7\\fs19\\b0 " + found, 1)
        found, text_to_read[16] = get_and_remove(r"\\f7\\fs19.+?fixation", text_to_read[16], count=1)
        text_to_read[26] = text_to_read[26].replace("\\sb168", found, 1)
        found, text_to_read[16] = get_and_remove(r"Ostectomy of ulna\\par", text_to_read[16], count=1)
        text_to_read[26] = text_to_read[26].replace("\\sb168", "\\f7\\fs19\\b0 " + found, 1)
        found, text_to_read[16] = get_and_remove(r"\\f7\\fs19\\b0.+?fixation", text_to_read[16], count=1)
        text_to_read[26] = text_to_read[26].replace("\\sb168", found, 1)
        found, text_to_read[16] = get_and_remove(r"Amputation through forearm\\par", text_to_read[16], count=1)
        text_to_read[26] = text_to_read[26].replace("\\sb168", "\\f7\\fs19\\b0 " + found, 1)
        found, text_to_read[16] = get_and_remove(r"^\\par.+\)\\par", text_to_read[16])
        text_to_read[26] += found
        text_to_read[5] = text_to_read[19] = text_to_read[6] = text_to_read[20] = text_to_read[7] = text_to_read[21] \
            = text_to_read[8] = text_to_read[9] = text_to_read[25] = text_to_read[27] = ""

    if index == 196:
        text_to_read.pop(0)
        _, text_to_read[1] = text_to_read[1].split("\\column")
        text_to_read[3] += text_to_read[15]
        text_to_read[8] += text_to_read[16]
        text_to_read[9] += text_to_read[17]
        text_to_read[10] = text_to_read[10].replace("\\column", text_to_read[18], 1)
        text_to_read[13] = text_to_read[4] + text_to_read[13]
        text_to_read[14] = text_to_read[5] + text_to_read[14]
        text_to_read[15] = text_to_read[6] + text_to_read[7]
        text_to_read[16] = text_to_read[17] = text_to_read[18] = text_to_read[4] = text_to_read[5] = text_to_read[6] =\
            text_to_read[7]= ""

    if index == 197:
        text_to_read.pop(0)
        text_to_read.pop(0)
        text_to_read[1] += "".join(text_to_read[21:26])
        text_to_read[21:26] = ""
        repair_tag = text_to_read[2]
        repair_tag, text = repair_tag.split("\\column ")
        text_to_read[2] = "".join(text_to_read[22:36])
        text_to_read[22:36] = ""
        text_to_read[3] = "".join(text_to_read[23:27]) + text
        text_to_read[23:27] = ""
        text = "".join(text_to_read[16:18])
        text_to_read[16:18] = ""
        text_to_read[21] = text_to_read[21].replace("\\column", repair_tag)
        text_to_read[15] = text + "\\f7\\fs19\\b0"


    if index == 198:
        text_to_read.pop(0)
        text_to_read.pop(0)
        text_to_read[6] = text_to_read[5] + text_to_read[6]
        text_to_read[15] = text_to_read[2] + text_to_read[15]
        text_to_read[16] = text_to_read[3] + text_to_read[16]
        text_to_read[17] = text_to_read[4] + text_to_read[17]
        found, text_to_read[10] = get_and_remove(r"}f12\\fs19.+", text_to_read[10])
        text_to_read[23] = found.replace("}f12", "\\f12") + text_to_read[23]
        text_to_read[24] = "\\f7\\fs19\\b0\\charscalex110\\cf2 49218-01\\cell}" + text_to_read[24]
        text_to_read[17] += """\\f7\\fs19\\b0\\charscalex115\\cf2 49221-02\\tab Arthroscopic release of adhesions of\\expnd2\\expndtw11  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 wrist\\par"""
        text_to_read[11] = text_to_read[2] = text_to_read[3] = text_to_read[5] = text_to_read[4] = ""
        text_to_read[10] += " 46393-00 [1471])\\par"

    if index == 199:
        exclude, text_to_read[4] = get_and_remove(r"^\\par.+?\\sb178", text_to_read[4])
        text_to_read[3] += exclude
        text_to_read[0] = text_to_read[1] = ""
        text_to_read[5] += text_to_read[18]
        text_to_read[6] += text_to_read[19]
        text_to_read[7] += text_to_read[20]
        text_to_read[8] += text_to_read[21]
        text_to_read[9] += text_to_read[22]
        text_to_read[10] += text_to_read[23]
        text_to_read[11] += text_to_read[24]
        text_to_read[4] += "".join(text_to_read[13:17])
        text_to_read[18] = text_to_read[19] = text_to_read[20] = text_to_read[21] = text_to_read[22] = text_to_read[23] \
            = text_to_read[24] = text_to_read[13] = text_to_read[14] = text_to_read[15] = text_to_read[16] = ""
        found, text_to_read[11] = get_and_remove(r"\\f4\\fs18.+", text_to_read[11])
        text_to_read[12] += found
        include, text_to_read[28] = get_and_remove(r"\\pard.+\\column", text_to_read[28])
        text_to_read[26] = include + text_to_read[26]

    if index == 201:
        text_to_read[14] = text_to_read[83]
        include, text_to_read[15] = get_and_remove(r"\\f16\\fs18.+", text_to_read[15])
        found, text_to_read[18] = get_and_remove(r"\\f7\\fs19.+", text_to_read[18])
        include += found + text_to_read[22] + text_to_read[23] + text_to_read[27] + text_to_read[28] + text_to_read[32] \
                   + text_to_read[33] + text_to_read[35] + text_to_read[36] + text_to_read[39]
        text_to_read[88] = include
        found, text_to_read[21] = get_and_remove(r"{\\pard.+?\\par", text_to_read[21])
        text_to_read[20] = text_to_read[20].replace("\\sb168", found)
        text_to_read[83] = text_to_read[22] = text_to_read[23] = text_to_read[27] = text_to_read[28] = text_to_read[32] \
            = text_to_read[33] = text_to_read[35] = text_to_read[36] = text_to_read[39] = ""
        found, text_to_read[26] = get_and_remove(r"{\\pard.+?\\par", text_to_read[26])
        text_to_read[21] += found
        found, text_to_read[31] = get_and_remove(r"{\\pard.+?\\par", text_to_read[31])
        text_to_read[26] += found
        found, text_to_read[84] = get_and_remove(r"\\f4\\fs18.+?\\par", text_to_read[84])
        text_to_read[54] += found
        t_1463 = text_to_read[43] + text_to_read[44] + text_to_read[48] + text_to_read[49] + text_to_read[52]
        text_to_read[43] = text_to_read[44] = text_to_read[48] = text_to_read[49] = text_to_read[52] = ""
        found, text_to_read[54] = get_and_remove(r"\\f7\\fs19.+", text_to_read[54])
        t_1463 += found + text_to_read[55] + text_to_read[58] + text_to_read[59] + text_to_read[62] + text_to_read[66] \
                  + text_to_read[67] + text_to_read[70] + text_to_read[73] + text_to_read[74]
        text_to_read[55] = text_to_read[58] = text_to_read[59] = text_to_read[62] = text_to_read[66] = \
            text_to_read[67] = text_to_read[70] = text_to_read[73] = text_to_read[74] = ""
        found, text_to_read[82] = get_and_remove(r"\\f16\\fs18.+", text_to_read[82])
        text_to_read[82] = text_to_read[82].replace("\\tab", " phalanx of hand")
        text_to_read[83] = """\\f16\\fs18\\b1\\i1\\charscalex90\\cf2 Includes: \\f4\\fs18\\b0\\i0 procurement of graft material\\expnd-5\\expndtw-26  \\f4\\fs18\\b0\\i0\\expnd-1\\expndtw-4 through \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0\\charscalex95 same\\expnd0\\expndtw-1  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 incision\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li2687\\sl-213\\sb113\\f11\\fs18\\b0\\i1\\charscalex95\\cf2 Code\\expnd-4\\expndtw-20  \\f11\\fs18\\b0\\i1\\expnd0\\expndtw0 also\\expnd-4\\expndtw-20  \\f11\\fs18\\b0\\i1\\expnd0\\expndtw0 when\\expnd-4\\expndtw-19  \\f11\\fs18\\b0\\i1\\expnd0\\expndtw0 performed:\\par\\pard\\plain\\s9\\ls326\\ilvl2\\nooverflow\\nocwrap\\lnbrkrule\\li2801\\fi-114\\ri22\\sl232\\slmult1\\sb1\\tx2803\\f4\\fs18\\b0\\charscalex85\\cf2 procurement of graft material through separate \\f4\\fs18\\b0\\i0\\charscalex95 incision (47726-00\\expnd1\\expndtw6  \\f5\\fs18\\b1\\i0\\expnd0\\expndtw0 [1563]\\f4\\b0 )\\par"""
        text_to_read[84] = """\\f7\\fs19\\b0\\charscalex110\\cf2 48230-00\\cell}{\\pard\\plain\\intbl\\s10\\nooverflow\\nocwrap\\lnbrkrule\\li90\\sl-229\\f7\\fs19\\b0\\charscalex115\\cf2 Bone graft to scaphoid\\cell}\\"""
        text_to_read[84] += """\\f7\\fs19\\b0\\charscalex110\\cf2 48233-00\\cell}{\\pard\\plain\\intbl\\s10\\nooverflow\\nocwrap\\lnbrkrule\\li90\\sl228\\slmult1\\sb93\\f7\\fs19\\b0\\charscalex115\\cf2 Bone graft to scaphoid with internal fixation\\cell}\\f7\\fs19\\b0\\charscalex110\\cf2 48236-00\\cell}{\\pard\\plain\\intbl\\s10\\nooverflow\\nocwrap\\lnbrkrule\\li90\\sl-220\\sb89\\f7\\fs19\\b0\\charscalex115\\cf2 Bone graft to scaphoid with internal fixation and osteotomy\\cell}"""
        t_46306, text_to_read[97] = get_and_remove(r"^\\pard.+?\\par", text_to_read[97])
        t_1464 = text_to_read[78] + text_to_read[79] + found + t_46306
        text_to_read[78] = text_to_read[79] = ""
        text_to_read[88] += t_1463.replace("\\f4\\fs18\\b0\\cf2 incision\\par", "") + t_1464
        _, text_to_read[88] = get_and_remove(r"\\f12\\fs19\\b1\\up7.+?\\tab", text_to_read[88])

    if index == 202:
        text_to_read[0:4] = ""
        text_to_read[38] = text_to_read[6] + text_to_read[38]
        text_to_read[39] = text_to_read[8] + text_to_read[39]
        found, text_to_read[47] = get_and_remove(r"\\f7\\fs19.+?\\cell}", text_to_read[47])
        text_to_read[17] += found
        text_to_read[20] += text_to_read[51]
        text_to_read[21] += text_to_read[52]
        text_to_read[22] = text_to_read[22].replace("\\column", text_to_read[53])
        text_to_read[47] = text_to_read[47].replace("}f16", "\\f16")
        text_to_read[6] = text_to_read[8] = text_to_read[51] = text_to_read[52] = text_to_read[53] = ""
        text_to_read[27] = text_to_read[28] = text_to_read[29] = text_to_read[31] = ""

    if index == 203:
        found, text_to_read[15] = get_and_remove(r"^\\pard.+?\\column", text_to_read[15])
        text_to_read[4] = found + text_to_read[4]

    if index == 205:
        text_to_read[3] += text_to_read[21]
        found, text_to_read[5] = get_and_remove(r"}f7.+-00", text_to_read[5])
        text_to_read[19] = found.replace("}f7", "\\f7") + text_to_read[19]
        found, text_to_read[8] = get_and_remove(r"}f7.+\\par", text_to_read[8])
        text_to_read[22] = found.replace("}f7", "\\f7") + text_to_read[22]
        text_to_read[15] = text_to_read[15].replace("\\f4\\fs16\\b0\\i0\\par", "")
        found, text_to_read[4] = get_and_remove(r"}f12.+", text_to_read[4])
        text_to_read[18] = found.replace("}f12", "\\f12") + text_to_read[18]
        text_to_read[21] = ""

    if index == 207:
        text_to_read[1] = "".join(text_to_read[4:9])
        text_to_read[4:9] = ""

    if index == 208:
        text_to_read[4], _ = get_and_remove(r"\\f12\\fs19.+", text_to_read[4])
        text_to_read[4] = "{\\pard\\plain" + text_to_read[4]
        text = text_to_read[15]
        text_to_read[15] = ""
        found, _ = get_and_remove(r"\\f12\\fs19.+", text_to_read[43])
        text_to_read[16] += found
        text_to_read[17] += text_to_read[44]
        text_to_read[18] += text_to_read[45]
        text_to_read[19] += text_to_read[46]
        text_to_read[20] += text_to_read[47]
        text_to_read[21] += text_to_read[48]
        text_to_read[22] += text_to_read[49]
        text_to_read[23] += text_to_read[50]
        text_to_read[53] = text_to_read[26] + text_to_read[53]
        text_to_read[54] = text_to_read[27] + text_to_read[54]
        text_to_read[55] = text_to_read[28] + text_to_read[55]
        found, text_to_read[7] = get_and_remove(r"}f7\\fs19.+?\\par", text_to_read[7])
        text_to_read[33] = found.replace("}f7", "\\f7") + text_to_read[33]
        found, text_to_read[8] = get_and_remove(r"}f7\\fs19.+", text_to_read[8])
        text_to_read[34] = found.replace("}f7", "\\f7") + text_to_read[34]
        text_to_read[35], found = get_and_remove(r"{\\pard.+?\\par", text_to_read[35])
        text_to_read[36] = text_to_read[36].replace("Ostectomy of fibula", found + " Ostectomy of fibula ")
        text_to_read[40] += text.replace("\\column", text_to_read[41].replace("}f12", "\\f12"))
        found, _ = get_and_remove(r"^\\pard.+?\\par", text_to_read[42])
        text_to_read[7] = text_to_read[7].replace("\\cell", found, 1)
        text_to_read[44] = text_to_read[46] = text_to_read[45] = text_to_read[47] = text_to_read[48] = \
            text_to_read[49] = text_to_read[50] = text_to_read[26] = text_to_read[27] = text_to_read[28] = \
            text_to_read[41] = text_to_read[43] = text_to_read[42] = ""

    if index == 209:
        text_to_read.pop(0)
        text_to_read.pop(0)
        text_to_read[0] = text_to_read[0].replace("\\f4\\fs18\\b0", "")
        text_to_read[11] = text_to_read[2] + text_to_read[11]
        text_to_read[4] += text_to_read[15] + text_to_read[16]
        text_to_read[5] += "".join(text_to_read[17:21])
        text_to_read[27], _ = get_and_remove(r"{\\pard.+\\column", text_to_read[27])
        text_to_read[6] += "".join(text_to_read[21:28])
        text_to_read[6] += "".join(text_to_read[8:14])
        text_to_read[2] = text_to_read[15] = text_to_read[16] = ""
        text_to_read[17:27] = ""
        text_to_read[8:14] = ""
        found, text_to_read[6] = get_and_remove(r"\\column.+?\\column", text_to_read[6])
        text_to_read[6] += """\\sl-196\\tx222\\f4\\fs18\\b0\\charscalex95\\cf2 shaft\\cell}""" + found
        text_to_read[6] += """\\f7\\fs19\\b0\\charscalex115\\cf2 47566-05 Open reduction of fracture of fibula with internal fixation\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li1342\\sl-218\\f4\\fs18\\b0\\cf2 Open reduction of fracture of fibula:\\par{\\pard\\plain\\intbl\\s10\\ls340\\ilvl0\\nooverflow\\nocwrap\\lnbrkrule\\li216\\fi-115\\sl-196\\tx217\\f4\\fs18\\b0\\charscalex95\\cf2 head\\cell}{\\pard\\plain\\intbl\\s10\\ls341\\ilvl0\\nooverflow\\nocwrap\\lnbrkrule\\li216\\fi-115\\sl-196\\tx217\\f4\\fs18\\b0\\cf2 NOS\\cell}{\\pard\\plain\\intbl\\s10\\ls342\\ilvl0\\nooverflow\\nocwrap\\lnbrkrule\\li216\\fi-115\\sl-196\\tx217\\f4\\fs18\\b0\\charscalex95\\cf2 proximal\\cell}{\\pard\\plain\\intbl\\s10\\ls343\\ilvl0\\nooverflow\\nocwrap\\lnbrkrule\\li216\\fi-115\\sl-209\\tx217\\f4\\fs18\\b0\\charscalex95\\cf2 shaft with internal fixation \\cell}{\\pard\\plain\\intbl\\s10\\nooverflow\\nocwrap\\lnbrkrule\\li100\\sl-217\\sb14\\f16\\fs18\\b1\\i1\\cf2 Excludes: \\f4\\fs18\\b0\\i0 distal fibula (47600-01, 47603-01 \\f5\\fs18\\b1\\i0 [1539]\\f4\\b0 )\\cell}"""
        text_to_read[8] = text_to_read[11] = ""

    if index == 210:
        text_to_read[8] += " 49554-00 [1523])\\par"
        text_to_read[9] = text_to_read[3] + text_to_read[9]
        text_to_read[10] = text_to_read[4] + text_to_read[10]
        text_to_read[11] = text_to_read[5] + text_to_read[11]
        text_to_read[3] = text_to_read[4] = text_to_read[5] = ""

    if index == 211:
        text_to_read[0] = "".join(text_to_read[25:39])
        text_to_read[25:39] = ""
        text_to_read[1] = "".join(text_to_read[26:43])
        text_to_read[26:43] = ""
        _, text_to_read[3] = get_and_remove(r"^\\pard.+?\\column", text_to_read[3])
        text_to_read.append(text_to_read[22])
        text_to_read[22] = ""
        _, text_to_read[23] = get_and_remove(r"\\par.+\\column", text_to_read[23])

    if index == 212:
        found, text_to_read[30] = get_and_remove(r"{\\pard.+?\\cell}", text_to_read[30])
        text_to_read[6] = found + text_to_read[6]
        text_to_read[18] = text_to_read[39] + text_to_read[42] + text_to_read[44]
        text_to_read[19] += text_to_read[47]
        text_to_read[39] = text_to_read[42] = text_to_read[44] = text_to_read[47] = ""
        text_to_read[29] = text_to_read[29].replace("INCISIONf12","INCISION\\f12")
        text_to_read[30] = "{\\pard\\plain\\" + text_to_read[30] + """\\f7\\fs19\\b0\\i0\\up0 48409-15\\tab Osteotomy of tarsal bone with\\expnd4\\expndtw22  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 i internal fixation\\cell}"""
        found, text_to_read[13] = get_and_remove(r"}f4.+?\\par", text_to_read[13])
        text_to_read[32] += found.replace("}f4", "\\f4")
        found, text_to_read[14] = get_and_remove(r"}f7.+", text_to_read[14])
        text_to_read[36] = found.replace("}f7", "\\f7") + text_to_read[36]
        found, text_to_read[15] = get_and_remove(r"}f7.+", text_to_read[15])
        text_to_read[37] = found.replace("}f7", "\\f7") + text_to_read[37]
        found, text_to_read[37] = get_and_remove(r"\\f4\\fs18.+", text_to_read[37])
        text_to_read[36] += found
        _, text_to_read[34] = get_and_remove(r"^\\pard.+?\\par", text_to_read[34])

    if index == 213:
        found, text_to_read[57] = get_and_remove(r"^\\pard.+?\\par", text_to_read[57])
        text_to_read[2] += found
        found, text_to_read[65] = get_and_remove(r"^\\pard.+?\\par", text_to_read[65])
        text_to_read[58] += found

    if index ==214:
        text_to_read[25] = text_to_read[25].replace("\\sb162", text_to_read[24])
        text_to_read[24] = text_to_read[39]
        text_to_read[39] = ""
        found, text_to_read[20] = get_and_remove(r"}f7.+?\\par", text_to_read[20])
        text_to_read[38] = found.replace("}f7", "{\\pard\\plain\\f7") + text_to_read[38]

    if index == 215:
        text_to_read.pop(0)

    if index == 218:
        text_to_read[29] = text_to_read[29].replace("elsewhere", "elsewhere classified ")
        _, text_to_read[14] = get_and_remove(r"\\f7\\fs19\\b0\\charscalex115\\cf2\sclass.+", text_to_read[14])

    if index == 219:
        t_1563, text_to_read[4] = get_and_remove(r"\\f12\\fs19\\b1.+?\\column", text_to_read[4], count=1)
        found, text_to_read[4] = get_and_remove(r"\\f14\\fs15\\b0.+?\\par", text_to_read[4], count=1)
        t_1563 += found
        text_to_read[6] = t_1563 + text_to_read[6]

    if index == 220:
        text_to_read[9], text_to_read[11] = get_and_remove(r"{\\pard.+?\\par", text_to_read[11])

    if index == 221:
        text = "".join(text_to_read[5:13])
        text_to_read[13] = text_to_read[13].replace("\\sb3", text)
        text_to_read[5] = text_to_read[6] = text_to_read[7] = text_to_read[8] = text_to_read[9] = text_to_read[10] = \
            text_to_read[11] = text_to_read[12] = ""

    if index == 228:
        found, text_to_read[19] = get_and_remove(r"^\\pard.+?\\column", text_to_read[19])
        text_to_read[13] = found + text_to_read[13]

    if index == 230:
        found, text_to_read[41] = get_and_remove(r"\\f7\\fs19\\b0.+?\\cell}", text_to_read[41])
        text_to_read[12] = text_to_read[12].replace("\\sb168", found)
        text_to_read[12] += """\\f7\\fs19\\b0\\charscalex115\\cf2 Removal of synthetic skin graft\\expnd4\\expndtw19  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 to\\expnd1\\expndtw4  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 burn"""
        text_to_read[14] = text_to_read[21] = ""
        found, text_to_read[47] = get_and_remove(r"{\\pard.+?\\cell}", text_to_read[47])
        text_to_read[22] += found
        found, text_to_read[31] = get_and_remove(r"{\\pard.+?\\par", text_to_read[31])
        text_to_read[29] += found
        text_to_read[40] = """\\f7\\fs19\\b0\\i0 47915-00\\tab Wedge resection of ingrown\\expnd3\\expndtw15  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 toenail\\cell}\\f16\\fs18\\b1\\i1\\up0 Includes: \\f4\\fs18\\b0\\i0 removal\\expnd-5\\expndtw-25  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 of:\\par\\pard\\plain\\intbl\\s10\\ls368\\ilvl0\\nooverflow\\nocwrap\\lnbrkrule\\li6043\\fi-115\\sl-191\\tx6044\\f4\\fs18\\b0\\charscalex95\\cf2 segment of\\expnd0\\expndtw-1  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 nail\\cell}\\f4\\fs18\\b0\\i0\\up0\\charscalex100 \\'95\\expnd-6\\expndtw-30  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0\\charscalex105 ungual\\expnd-6\\expndtw-32  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 fold\\expnd-6\\expndtw-32  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 and\\expnd-6\\expndtw-32  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 portion\\expnd-6\\expndtw-31  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 of\\expnd-6\\expndtw-32  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 nail\\expnd-6\\expndtw-32  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 bed\\cell}"""
        text_to_read[40] += """\\f7\\fs19\\b0\\i0\\up0 47918-00\\tab Radical excision of ingrown toenail\\expnd5\\expndtw24  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 bed\\cell}"""
        text_to_read[40] += """\\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 burn\\tab \\f12\\fs19\\b1\\i0\\up0\\cf5{\\chcbpat2 1633\\tab }\\tab \\f12\\fs19\\b1\\i0\\cf2 Excision of sweat\\expnd-2\\expndtw-12  \\f12\\fs19\\b1\\i0\\expnd0\\expndtw0 glands\\cell}"""
        text_to_read[41] = text_to_read[13] + text_to_read[41].replace("}f4", "\\f4")
        text_to_read[13] = ""
        text_to_read[41] = text_to_read[41].replace("tx4170f7", "tx4170\\f7") + """\\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 Partial excision of axillary sweat\\expnd-3\\expndtw-15  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 glands\\par\\pard\\plain\\intbl\\s10\\nooverflow\\nocwrap\\lnbrkrule\\li5191\\sl-187\\f4\\fs18\\b0\\charscalex95\\cf2 Wedge excision of axillary sweat glands\\cell}"""
        t_1635, text_to_read[25] = get_and_remove(r"\\f12\\fs19\\b1\\expnd1.+", text_to_read[25])
        text_to_read[47] = "{\\pard\\plain\\" + text_to_read[47] + t_1635 + """\\f12\\fs19\\b1\\i0\\cf2 Repair of wound of skin\\expnd0\\expndtw-2  \\f12\\fs19\\b1\\i0\\expnd0\\expndtw0 and\\cell}\\f12\\fs19\\b1\\i0\\up0\\cf2 subcutaneous\\expnd0\\expndtw-2  \\f12\\fs19\\b1\\i0\\expnd0\\expndtw0 tissue\\cell}"""
        text_to_read[47] += """\\f4\\fs18\\b0\\i0\\up0\\charscalex90 Repair\\expnd-2\\expndtw-10  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 of\\expnd-2\\expndtw-10  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 laceration\\expnd-2\\expndtw-11  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 of\\expnd-2\\expndtw-10  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 skin\\expnd-2\\expndtw-10  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 and\\expnd-2\\expndtw-11  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 subcutaneous\\expnd-2\\expndtw-10  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 tissue"""
        text_to_read[48] = """\\f16\\fs18\\b1\\i1\\up0 Includes: \\f4\\fs18\\b0\\i0 use\\expnd-2\\expndtw-9  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 of:\\cell}""" + text_to_read[48]

    if index == 231:
        asc, text_to_read[2] = get_and_remove(r"\\f14\\fs15.+?\\par", text_to_read[2])
        found, text_to_read[18] = get_and_remove(r"^\\pard.+?\\par", text_to_read[18])
        text_to_read[2] += found
        text_to_read[17] += asc
        _, text_to_read[18] = get_and_remove(r"\\pard.+\\sl240", text_to_read[18])

    if index == 232:
        text_to_read[4], text_to_read[6] = get_and_remove(r"{\\pard.+?\\par", text_to_read[6])
        found, text_to_read[27] = get_and_remove(r"^\\pard.+?\\par", text_to_read[27])
        text_to_read[14] += found
        text_to_read[35], text_to_read[37] = get_and_remove(r"{\\pard.+?\\par", text_to_read[37])
        text_to_read[32] = text_to_read[41]
        text_to_read[41] = ""

    if index == 233:
        found, text_to_read[45] = get_and_remove(r"\\f7\\fs19.+", text_to_read[45])
        text_to_read[46] = text_to_read[46].replace("\\sb168", found)
        text_to_read[45] = text_to_read.pop(58)

    if index == 237:
        found, text_to_read[23] = text_to_read[23].split("\\column")
        text_to_read[17] = found + text_to_read[17]
        text_to_read[14], found = get_and_remove(r"{\\pard.+?\\par", text_to_read[14])
        text_to_read[23] = found
        text_to_read[22] += text_to_read[14]
        text_to_read[14] = ""

    if index == 239:
        text_to_read[14] = text_to_read[9] + text_to_read[14]
        text_to_read[15] = text_to_read[10] + text_to_read[15]
        text_to_read[10] = text_to_read[9] = ""

    if index == 240:
        found, text_to_read[8] = get_and_remove(r"\\f4\\fs18\\b0\\charscalex95\\cf2\sstent.+?\\column", text_to_read[8])
        text_to_read[8] = text_to_read[8].replace("\\column", found, 1)

    if index == 241:
        found, text_to_read[17] = get_and_remove(r"^\\pard.+?\\column", text_to_read[17])
        text_to_read[20] = text_to_read[20].replace("blepharoptosis", "blepharoptosis " + found, 1)

    if index == 242:
        text_to_read[14] = text_to_read[7] + text_to_read[14]
        text_to_read[7] = ""

    if index == 244:
        text_to_read.pop(1)

    if index == 245:
        text_to_read[0] = text_to_read[1] = text_to_read[2] = ""
        _, text_to_read[4] = get_and_remove(r"^\\pard.+?\\column", text_to_read[4])
        text_to_read[6] = "".join(text_to_read[20:28])
        text_to_read[20] = text_to_read[21] = text_to_read[22] = text_to_read[23] = text_to_read[24] = text_to_read[25]\
            = text_to_read[26] = text_to_read[27] = ""
        text_to_read[7] += text_to_read[29] + text_to_read[30]
        text_to_read[30] = text_to_read[29] = ""
        found, text_to_read[9] = get_and_remove(r"{\\pard.+?\\par", text_to_read[9])
        text_to_read[8] = found + text_to_read[28] + text_to_read[8]
        text_to_read[28] = ""

    if index == 246:
        text_to_read.pop(0)
        text_to_read[7] = text_to_read[7].replace("internal", "internal fixation, bilateral ")
        text_to_read[9] = text_to_read[9].replace("internal", "internal fixation, unilateral ")
        text_to_read[11] = text_to_read[11].replace("internal", "internal fixation, bilateral ")
        text = """\\f12\\fs19\\b1\\expnd1\\expndtw3\\up5\\charscalex111\\cf5{\\chcbpat2  \\expnd0\\expndtw0\\charscalex110 1705\\tab }\\expnd0\\expndtw0\\charscalex110 \\tab \\f12\\fs19\\b1\\i0\\cf2 Osteotomy\\expnd-4\\expndtw-22  \\f12\\fs19\\b1\\i0\\expnd0\\expndtw0 or\\expnd-4\\expndtw-22  \\f12\\fs19\\b1\\i0\\expnd0\\expndtw0 ostectomy\\expnd-4\\expndtw-22  \\f12\\fs19\\b1\\i0\\expnd0\\expndtw0 of\\expnd-4\\expndtw-22  \\f12\\fs19\\b1\\i0\\expnd0\\expndtw0 mandible\\expnd-4\\expndtw-21  \\f12\\fs19\\b1\\i0\\expnd0\\expndtw0 or\\f12\\fs19\\b1\\up4\\charscalex110\\cf2 maxilla\\f4\\fs18\\b0\\charscalex95\\cf2 Mandibular or maxillary osteoplasty by osteotomy or\\par\\pard\\plain\\intbl\\s10\\nooverflow\\nocwrap\\lnbrkrule\\li569\\qc\\sl-225\\tx4537\\tx5558\\f4\\fs18\\b0\\up1\\charscalex95\\cf2 ostectomy\\f16\\fs18\\b1\\i1\\cf2 Includes:\\expnd-3\\expndtw-14  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 bone\\expnd-6\\expndtw-29  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 graft\\f4\\fs18\\b0\\dn4\\charscalex90\\cf2 transposition\\expnd-4\\expndtw-19  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 of\\expnd-4\\expndtw-18  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 nerves\\expnd-4\\expndtw-19  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 and\\expnd-4\\expndtw-18  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 vessels\\f11\\fs18\\b0\\i1\\up3\\cf2 Code\\expnd-5\\expndtw-27  \\f11\\fs18\\b0\\i1\\expnd0\\expndtw0 also\\expnd-5\\expndtw-27  \\f11\\fs18\\b0\\i1\\expnd0\\expndtw0 when\\expnd-5\\expndtw-27  \\f11\\fs18\\b0\\i1\\expnd0\\expndtw0 performed:\\f4\\fs18\\b0\\cf2 genioplasty\\expnd-6\\expndtw-28  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 (45761\\expnd-5\\expndtw-27  \\f5\\fs18\\b1\\i0\\expnd0\\expndtw0 [1702]\\f4\\b0 )\\f4\\fs18\\b0\\charscalex95\\cf2 procurement of bone for graft from other\\expnd0\\expndtw1  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 site\\par\\pard\\plain\\intbl\\s10\\nooverflow\\nocwrap\\lnbrkrule\\li747\\qc\\sl-219\\tx4716\\tx5737\\f4\\fs18\\b0\\charscalex105\\cf2 (47726-00\\expnd-4\\expndtw-18  \\f5\\fs18\\b1\\i0\\expnd0\\expndtw0 [1563]\\f4\\b0 )"""
        t_45726_03 = text_to_read[12]
        text_to_read[12] = text
        text_to_read[12] += """\\f16\\fs18\\b1\\i1\\charscalex90\\cf2 Excludes: \\f4\\fs18\\b0\\i0 complex combinations\\expnd-4\\expndtw-20  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 of\\expnd-2\\expndtw-10  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 osteotomy/\\f4\\fs18\\b0\\up13\\charscalex90\\cf2 ostectomy procedures on\\expnd-6\\expndtw-30  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 mandible\\expnd-2\\expndtw-10  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 or\\f4\\fs18\\b0\\cf2 maxilla (45731,\\expnd-6\\expndtw-28  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 45735-00,\\expnd-3\\expndtw-14  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 45741-00,f4\\fs18\\b0\\cf2 45747-00 \\f5\\fs18\\b1\\i0 [1707]\\f4\\b0 )\\par\\pard\\plain\\intbl\\s10\\nooverflow\\nocwrap\\lnbrkrule\\li1791\\sl-266\\tx5136\\tx6157\\f4\\fs18\\b0\\up10\\charscalex95\\cf2 multiple\\expnd-6\\expndtw-28  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 (more\\expnd-5\\expndtw-27  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 than\\expnd-5\\expndtw-27  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 two)\\expnd-6\\expndtw-28  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 procedures\\expnd-5\\expndtw-27  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 on:f4\\fs18\\b0\\cf2 mandible\\expnd-3\\expndtw-16  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 (45731-00\\expnd-3\\expndtw-16  \\f5\\fs18\\b1\\i0\\expnd0\\expndtw0 [1707]\\f4\\b0 )\\f4\\fs18\\b0\\cf2 maxilla (45731-01\\expnd0\\expndtw-2  \\f5\\fs18\\b1\\i0\\expnd0\\expndtw0 [1707]\\f4\\b0 )\\par\\pard\\plain\\intbl\\s10\\nooverflow\\nocwrap\\lnbrkrule\\li1791\\sl-261\\tx5136\\tx5929\\tx6157\\f4\\fs18\\b0\\up8\\charscalex95\\cf2 that\\expnd-3\\expndtw-16  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 with\\expnd-3\\expndtw-15  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 internal\\expnd-3\\expndtw-16  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 fixation\\expnd-3\\expndtw-15  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 (45723,\\f4\\fs18\\b0\\up9\\cf2 45729\\expnd1\\expndtw3  \\f5\\fs18\\b1\\i0\\expnd0\\expndtw0 [1706]\\f4\\b0 )"""
        text_to_read[12] += """\\f7\\fs19\\b0\\expnd0\\expndtw2\\dn9\\cf2 45720-00        \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 Osteotomy   of\\expnd6\\expndtw31  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 mandible, \\expnd3\\expndtw13  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 unilateral"""
        text_to_read[12] += """\\f7\\fs19\\b0\\expnd0\\expndtw2\\charscalex105\\cf2 45726-00       \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 Osteotomy  of\\expnd3\\expndtw13  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 mandible,\\expnd8\\expndtw38  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 bilateral"""
        text = """\\f7\\fs19\\b0\\up9\\cf2 45720-01\\tab Osteotomy   of \\expnd1\\expndtw5  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 maxilla, \\expnd5\\expndtw25  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 unilateral\\f7\\fs19\\b0\\cf2 45726-01\\tab Osteotomy   of\\expnd8\\expndtw42  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 maxilla, \\expnd4\\expndtw21  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 bilateral\\f4\\fs18\\b0\\i0\\dn10\\charscalex100 Le\\expnd-5\\expndtw-23  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 Fort\\expnd-4\\expndtw-22  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 I\\expnd-4\\expndtw-22  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 osteotomy\\f7\\fs19\\b0\\charscalex105\\cf2 45720-02       Ostectomy  of\\expnd7\\expndtw35  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 mandible,\\expnd8\\expndtw38  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 unilateral\\f7\\fs19\\b0\\charscalex105\\cf2 45726-02\\tab Ostectomy  of\\expnd8\\expndtw41  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 mandible,\\expnd9\\expndtw43  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 bilateral\\f7\\fs19\\b0\\charscalex110\\cf2 45720-03     Ostectomy  of\\expnd0\\expndtw1  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 maxilla,\\expnd3\\expndtw17  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 unilateral"""
        text_to_read[12] += text + t_45726_03
        _, text_to_read[20] = get_and_remove(r"\\f7\\fs19.+?cell}", text_to_read[20])
        text_to_read[20] = "\\" + text_to_read[20].replace("tx5929f4", "tx5929\\f4")
        text_to_read[21] = """\\f7\\fs19\\b0\\i0\\expnd0\\expndtw2\\up0 45723-00 \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 Osteotomy of mandible with internal fixation,\\expnd1\\expndtw7  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 unilateral\\f7\\fs19\\b0\\i0\\expnd0\\expndtw2\\up0 45729-00 \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 Osteotomy of mandible with\\expnd-3\\expndtw-13  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 internal\\cell}\\f7\\fs19\\b0\\charscalex115\\cf2 fixation,\\expnd1\\expndtw7  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 bilateral\\f7\\fs19\\b0\\i0\\up0 45723-01\\tab Osteotomy of maxilla with\\expnd1\\expndtw6  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 internal fixation, unilateral\\par\\f7\\fs19\\b0\\i0\\up0\\charscalex110 45729-01\\tab Osteotomy of maxilla with\\expnd1\\expndtw6  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 internal fixation, bilateral\\par\\f4\\fs18\\b0\\i0\\up0\\charscalex95 Le\\expnd-2\\expndtw-8  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 Fort\\expnd-1\\expndtw-7  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 I\\expnd-2\\expndtw-8  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 osteotomy\\expnd-1\\expndtw-7  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 with\\expnd-1\\expndtw-7  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 internal\\expnd-2\\expndtw-8  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 fixation\\par\\f7\\fs19\\b0\\i0\\up0\\charscalex105 45723-02\\tab Ostectomy of mandible with\\expnd-4\\expndtw-19  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 internal fixation, unilateral\\par"""
        text_to_read[21] += """\\f7\\fs19\\b0\\i0\\charscalex110 45729-02\\tab Ostectomy of mandible with\\expnd4\\expndtw18  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 internal fixation, bilateral\\par\\f7\\fs19\\b0\\i0\\up0\\charscalex100 45723-03\\tab Ostectomy of maxilla with\\expnd0\\expndtw1  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 internal fixation, unilateral\\par\\f7\\fs19\\b0\\i0\\up0\\charscalex100 45729-03\\tab Ostectomy of maxilla with internal fixation, bilateral\\par"""
        text_to_read[21] += """\\f12\\fs19\\b1\\i0\\expnd-1\\expndtw-3\\up0\\charscalex100\\cf5{\\chcbpat2 1707\\tab }\\tab \\f12\\fs19\\b1\\i0\\expnd0\\expndtw0\\cf2 Osteotomy\\expnd5\\expndtw25  \\f12\\fs19\\b1\\i0\\expnd0\\expndtw0 or\\expnd5\\expndtw25  \\f12\\fs19\\b1\\i0\\expnd0\\expndtw0 ostectomy\\expnd5\\expndtw26  \\f12\\fs19\\b1\\i0\\expnd0\\expndtw0 of\\expnd5\\expndtw25  \\f12\\fs19\\b1\\i0\\expnd0\\expndtw0 mandible\\expnd5\\expndtw25  \\f12\\fs19\\b1\\i0\\expnd0\\expndtw0 or\\par\\f12\\fs19\\b1\\i0\\up0 maxilla, procedures in\\expnd6\\expndtw30  \\f12\\fs19\\b1\\i0\\expnd0\\expndtw0 combination\\par\\f4\\fs18\\b0\\i0\\up0\\charscalex85 Mandibular or maxillary osteoplasties by osteotomy \\f4\\fs18\\b0\\i0\\charscalex100 or\\expnd-5\\expndtw-24  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 ostectomy,\\expnd-5\\expndtw-23  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 procedures\\expnd-5\\expndtw-23  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 in\\expnd-5\\expndtw-23  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 combination\\par\\pard\\plain\\intbl\\s10\\nooverflow\\nocwrap\\lnbrkrule\\li33\\sl-227\\sb4\\tx6156\\f16\\fs18\\b1\\i1 Includes: \\f4\\fs18\\b0\\i0 bone\\expnd-5\\expndtw-24  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 graft\\par\\pard\\plain\\intbl\\s10\\nooverflow\\nocwrap\\lnbrkrule\\li6893\\sl-194\\f4\\fs18\\b0\\charscalex95\\cf2 transposition of nerves and vessels\\par\\pard\\plain\\intbl\\s10\\nooverflow\\nocwrap\\lnbrkrule\\li33\\sl-292\\tx1054\\tx6156\\tx6893\\f16\\fs18\\b1\\i1\\up0 Note:\\tab \\f4\\fs18\\b0\\i0\\charscalex90 This\\expnd-2\\expndtw-11  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 block\\expnd-2\\expndtw-10  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 includes\\expnd-2\\expndtw-10  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 multiple\\expnd-2\\expndtw-11  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 osteotomies\\par\\pard\\plain\\intbl\\s10\\nooverflow\\nocwrap\\lnbrkrule\\li1054\\fi-1022\\ri14\\sl127\\slmult1\\sb80\\tx1053\\tx6893\\f4\\fs18\\b0\\i0\\up10\\charscalex90 or multiple ostectomies or a combination \\f4\\fs18\\b0\\i0\\dn10\\charscalex100 Le\\expnd-5\\expndtw-23  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 Fort\\expnd-4\\expndtw-22  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 I\\expnd-4\\expndtw-22  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 osteotomy\\tab \\f4\\fs18\\b0\\i0\\up0\\charscalex90 of\\expnd-3\\expndtw-13  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 both\\expnd-3\\expndtw-14  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 procedures\\expnd-3\\expndtw-13  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 on\\expnd-3\\expndtw-13  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 mandible\\expnd-3\\expndtw-14  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 or\\expnd-3\\expndtw-13  \\f4\\fs18\\b0\\i0\\expnd-1\\expndtw-3 maxilla\\par\\pard\\plain\\intbl\\s10\\nooverflow\\nocwrap\\lnbrkrule\\ri2019\\qr\\sl-140\\f4\\fs18\\b0\\charscalex90\\cf2 or both bones\\par"""
        text_to_read[21] += """\\f11\\fs18\\b0\\i1\\dn5 Code also when\\expnd-5\\expndtw-23  \\f11\\fs18\\b0\\i1\\expnd0\\expndtw0 performed:\\par\\pard\\plain\\intbl\\s10\\nooverflow\\nocwrap\\lnbrkrule\\li33\\sl-286\\tx1054\\tx6156\\f4\\fs18\\b0\\i0\\up14\\charscalex100 \\'95 genioplasty \\f4\\fs18\\b0\\i0\\charscalex105 (45761\\expnd-4\\expndtw-19  \\f5\\fs18\\b1\\i0\\expnd0\\expndtw0 [1702]\\f4\\b0 )\\par\\pard\\plain\\intbl\\s10\\ls406\\ilvl2\\nooverflow\\nocwrap\\lnbrkrule\\li6271\\fi-115\\sl-150\\tx6272\\f4\\fs18\\b0\\charscalex95\\cf2 procurement\\expnd-3\\expndtw-14  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 of\\expnd-3\\expndtw-14  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 bone\\expnd-3\\expndtw-13  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 for\\expnd-3\\expndtw-14  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 graft\\expnd-3\\expndtw-14  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 from\\expnd-3\\expndtw-13  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 other\\expnd-3\\expndtw-14  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 site\\par\\pard\\plain\\intbl\\s10\\nooverflow\\nocwrap\\lnbrkrule\\li33\\sl-294\\tx6269\\f4\\fs18\\b0\\i0\\up10 (47726-00\\expnd-1\\expndtw-7  \\f5\\fs18\\b1\\i0\\expnd0\\expndtw0 [1563]\\f4\\b0 )\\par\\pard\\plain\\intbl\\s10\\nooverflow\\nocwrap\\lnbrkrule\\li6156\\sl-176\\f16\\fs18\\b1\\i1\\charscalex95\\cf2 Excludes: \\f4\\fs18\\b0\\i0 midfacial osteotomies (45753-00 \\f5\\fs18\\b1\\i0 [1709]\\f4\\b0 )\\f4\\fs18\\b0\\cf2 that with internal fixation (45732,\\par\\pard\\plain\\intbl\\s10\\nooverflow\\nocwrap\\lnbrkrule\\li957\\sl-220\\f4\\fs18\\b0\\cf2 45738-00, 45744-00, 45752-00 \\f5\\fs18\\b1\\i0 [1708]\\f4\\b0 )\\cell}"""
        text_to_read[26] = ""

    if index == 247:
        text_to_read.pop(0)
        found, text_to_read[19] = get_and_remove(r"\\f7\\fs19.+", text_to_read[19])
        text_to_read[18] += found
        _, text_to_read[26] = get_and_remove(r"\\column\s\s\\f3.+", text_to_read[26])
        text_to_read[26] += text_to_read[15] + text_to_read[16] + text_to_read[20] + text_to_read[21] + text_to_read[24]
        text_to_read[15] = text_to_read[19]
        text_to_read[19] = text_to_read[16] = text_to_read[20] = text_to_read[21] = text_to_read[24] = ""

    if index == 248:
        text_to_read[8], text_to_read[10] = get_and_remove(r"{\\pard.+?\\par", text_to_read[10])

    if index == 251:
        text_to_read[15] = text_to_read[24]
        text_to_read[24] = ""

    if index == 253:
        text_to_read.pop(0)
        text_to_read.pop(0)
        _, text_to_read[1] = get_and_remove(r"^\\pard.+?\\column", text_to_read[1])

    if index == 255:
        text_to_read[5] = text_to_read[5].replace("15003-00", "\\f7\\fs19\\b0\\charscalex115\\cf2 15003-00")
        found, text_to_read[11] = get_and_remove(r"{\\pard.+?\\par", text_to_read[11])
        text_to_read[9] += found
        found, text_to_read[13] = get_and_remove(r"{\\pard.+?\\par", text_to_read[13])
        text_to_read[11] += found
        t_15320, text_to_read[14] = get_and_remove(r"{\\pard.+?\\par", text_to_read[14])
        found, text_to_read[15] = get_and_remove(r"\\column.+?\\column", text_to_read[15])
        text_to_read[13] += found
        found, text_to_read[28] = get_and_remove(r"^\\pard.+?\\par", text_to_read[28])
        text_to_read[19] = found + text_to_read[19]
        text_to_read[26] = t_15320 + text_to_read[26]
        found, text_to_read[15] = get_and_remove(r"}f12.+?\\par", text_to_read[15])
        text_to_read[27] = found.replace("}f12", "\\f12") + text_to_read[27]

    if index == 259:
        text_to_read[19] = "".join(text_to_read[7:17])
        text_to_read[7:17] = ""

    if index == 260:
        found = re.search(r"\\f16\\fs18\\b1.+?\\par", text_to_read[6]).group()
        text_to_read[4] += found

    if index == 261:
        text_to_read.pop(0)
        text_to_read.pop(0)
        text_to_read.pop(0)

    if index == 262:
        t_11021_01 = text_to_read[5]
        t_11021_02 = text_to_read[6]
        exclude, text_to_read[7] = get_and_remove(r"{\\pard.+?\\column", text_to_read[7])
        text_to_read[10] = t_11021_01 + text_to_read[10]
        text_to_read[11] = t_11021_02 + text_to_read[11].replace("\\row", exclude)
        text_to_read[5] = text_to_read[6] = ""

    if index == 263:
        text_to_read[11] += text_to_read[29]
        text_to_read[12] += text_to_read[30]
        text_to_read[13] += text_to_read[31]
        text_to_read[14] += text_to_read[32]
        text_to_read[15] += text_to_read[33]
        text_to_read[16] += text_to_read[34]
        text_to_read[17] += text_to_read[35]
        text_to_read[18] += text_to_read[36]
        text_to_read[19] += text_to_read[37]
        text_to_read[20] += text_to_read[38]
        text_to_read[29] = text_to_read[30] = text_to_read[31] = text_to_read[32] = text_to_read[33] = \
            text_to_read[34] = text_to_read[35] = text_to_read[36] = text_to_read[37] = text_to_read[38] = ""
        found, text_to_read[28] = get_and_remove(r"^\\pard.+?\\par", text_to_read[28])
        text_to_read[22] += found
        text = """\\f16\\fs18\\b1\\i1\\charscalex90\\cf2 Excludes:\\expnd-4\\expndtw-19  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 dental\\expnd-5\\expndtw-25  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 diagnostic\\expnd-5\\expndtw-25  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 tests,\\expnd-5\\expndtw-25  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 measures\\expnd-5\\expndtw-25  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 or\\expnd-5\\expndtw-25  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 investigations \\f4\\fs18\\b0\\i0\\charscalex95 (see blocks \\f5\\fs18\\b1\\i0 [451] \\f4\\fs18\\b0\\i0 and\\expnd0\\expndtw1  \\f5\\fs18\\b1\\i0\\expnd0\\expndtw0 [452]\\f4\\b0 )\\par"""
        text_to_read.append(text)

    if index == 264:
        text = "".join(text_to_read[19:74])
        text_to_read[19:74] = ""
        text_to_read[76] += text
        text_to_read[58] += text_to_read[77]
        text_to_read[77] = """\\f4\\fs18\\b0\\charscalex90\\cf2 simple harmonic acceleration \\f4\\fs18\\b0\\i0\\charscalex95 spontaneous nystagmus trapezoids\\par"""

    if index == 265:
        t_11503_18 = text_to_read[21] + text_to_read[22] + text_to_read[26] + text_to_read[30] + text_to_read[31]
        found, text_to_read[18] = get_and_remove(r"\\f4\\fs18\\b0.+", text_to_read[18])
        text_to_read[34] = text_to_read[34].replace("fluids\\par", "fluids\\par " + found + t_11503_18)
        text_to_read[21] = text_to_read[22] = text_to_read[26] = text_to_read[30] = text_to_read[31] = ""

    if index == 267:
        _, text_to_read[6] = get_and_remove(r"\\f1\\fs18.+?\\column", text_to_read[6])

    if index == 268:
        found, text_to_read[15] = get_and_remove(r"{\\pard.+?\\par", text_to_read[15])
        text_to_read[7] += text_to_read[12] + text_to_read[13] + found + text_to_read[14] + text_to_read[15] + text_to_read[16]
        text_to_read[8] += text_to_read[17]
        text_to_read[9] += text_to_read[18]
        text_to_read[10] += text_to_read[19].replace("\\row", text_to_read[11])
        text_to_read[12] = text_to_read[13] = text_to_read[14] = text_to_read[15] = text_to_read[16] = \
            text_to_read[17] = text_to_read[18] = text_to_read[19] = text_to_read[11] = ""

    if index == 269:
        text = "".join(text_to_read[17:38])
        text_to_read[4] += text
        text_to_read[17:38] = ""

    if index == 274:
        text = """\\f7\\fs19\\b0\\charscalex115\\cf2 92002-00\\tab Alcohol\\expnd0\\expndtw2  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 rehabilitation\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li2801\\sl-220\\sb49\\f16\\fs18\\b1\\i1\\charscalex95\\cf2 Includes: \\f4\\fs18\\b0\\i0 assessment\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li3538\\ri8983\\sl232\\slmult1\\sb1\\f4\\fs18\\b0\\charscalex85\\cf2 counselling \\f4\\fs18\\b0\\i0\\charscalex95 education\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li1780\\sl240\\slmult1\\sb159\\f7\\fs19\\b0\\charscalex115\\cf2 92003-00 Alcohol detoxification\\par"""
        text_to_read[3] += text

    if index == 275:
        text_to_read.pop(0)
        text_to_read.pop(0)

    if index == 278:
        text_to_read[6], _ = get_and_remove(r"\\f7\\fs19.+", text_to_read[6])
        found, text_to_read[6] = get_and_remove(r"\\f7\\fs19\\b0.+?\\par", text_to_read[6])
        t_1877, text_to_read[6] = get_and_remove(r"\\f12\\fs19\\b1.+?\\par", text_to_read[6])
        text_to_read[23] = found + text_to_read[23].replace("\\sb154", t_1877)
        found, text_to_read[6] = get_and_remove(r"\\f7\\fs19.+", text_to_read[6])
        text_to_read[23] = text_to_read[23].replace("\\sb169", text_to_read[10]).replace("\\sb168", found)
        text_to_read[23] = text_to_read[23].replace("\\sb176", text_to_read[19])
        text_to_read[10] = text_to_read[6] = text_to_read[19] = ""

    if index == 282:
        t_96195_02, text_to_read[3] = get_and_remove(r"\\tab\s\\f7.+?\\column", text_to_read[3])
        found = re.search(r"\s\\f14\\fs15\\b0.+?\\par", text_to_read[15]).group()
        text_to_read[15] = text_to_read[15].replace("protocol", "protocol" + t_96195_02 + found, 1)
        text_to_read[15] = text_to_read[15].replace("organ", "organ" + text_to_read[4])
        text_to_read[4], text_to_read[17] = get_and_remove(r"^\\pard.+?\\par", text_to_read[17])
        _, text_to_read[3] = get_and_remove(r"\\f14\\fs15\\b0.+?\\par", text_to_read[3])

    if index == 283:
        text_to_read[3] = text_to_read[3].replace("13020-00", "\\f7\\fs19\\b0\\charscalex115\\cf2 13020-00")
        text_to_read[11] = text_to_read[5] + text_to_read[11]
        text_to_read[12] = text_to_read[6] + text_to_read[12]
        found, text_to_read[7] = get_and_remove(r"{\\pard.+?\\column", text_to_read[7])
        text_to_read[13] = found + text_to_read[13]
        found, text_to_read[7] = get_and_remove(r"\\sb115.+?\\par", text_to_read[7])
        text_to_read[13] = text_to_read[13].replace("\\expnd1\\expndtw3", found)
        text_to_read[9] = text_to_read[9].replace("NOS", "NOS Manual external cardiac massage")
        text_to_read[5] = text_to_read[6] = ""

    if index == 285:
        text_to_read[60], text_to_read[70] = get_and_remove(r"^\\pard.+?\\par", text_to_read[70])
        found, text_to_read[57] = get_and_remove(r"{\\pard.+?cell}", text_to_read[57])
        text = "".join(text_to_read[48:57]) + found
        text_to_read[69] += text
        text_to_read[48:57] = ""

    if index == 286:
        text_to_read[3] = text_to_read[53]
        text_to_read[53] = ""
        text = "".join(text_to_read[55:87])
        text_to_read.append(text)
        text_to_read[55:87] = ""

    if index == 287:
        text_to_read.pop(0)
        text_to_read.pop(0)
        found, text_to_read[2] = get_and_remove(r"}f7.+?\\par", text_to_read[2])
        text_to_read[32] = found.replace("}f7", "\\f7") + text_to_read[32]
        found, text_to_read[3] = get_and_remove(r"}f7.+?\\par", text_to_read[3])
        text_to_read[33] = found.replace("}f7", "\\f7") + text_to_read[33]
        found, text_to_read[4] = get_and_remove(r"}f7.+?\\par", text_to_read[4])
        text_to_read[34] = found.replace("}f7", "\\f7") + text_to_read[34]
        found, text_to_read[5] = get_and_remove(r"}f7.+?\\par", text_to_read[5])
        text_to_read[35] = found.replace("}f7", "\\f7") + text_to_read[35]
        text_to_read[10] = text_to_read[13] = text_to_read[16] = ""
        text_to_read[47] = text_to_read[21] + text_to_read[47]
        text_to_read[48] = text_to_read[23] + text_to_read[48]
        text_to_read[21] = text_to_read[23] = ""
        text_to_read[34] = text_to_read[34].replace("\\cell}", " not specified as ultrabrief \\cell}")
        found, text_to_read[43] = get_and_remove(r"{\\pard.+?\\par", text_to_read[43])
        text_to_read[41] += found
        text_to_read[49] = """{\\pard\\plain\\intbl\\s10\\nooverflow\\nocwrap\\lnbrkrule\\ri75\\qc\\sl240\\slmult1\\sb124\\f7\\fs19\\b0\charscalex110\\cf2 92195-00\\cell}""" + text_to_read[49]
        text_to_read[50] = text_to_read[26] + text_to_read[50]
        text_to_read[51] = text_to_read[27] + text_to_read[51]
        text_to_read[52] = text_to_read[28] + text_to_read[52]
        text_to_read[53] = text_to_read[29] + text_to_read[53]
        text_to_read[26] = text_to_read[27] = text_to_read[28] = text_to_read[29] = ""
        text_to_read[54] = text_to_read[54].replace("elsewhere", "elsewhere specified (see Alphabetic Index: Removal/ suture)")

    if index == 288:
        text_to_read[4] = text_to_read[25] + text_to_read[4]
        text_to_read[25] = text_to_read[5] = ""
        text_to_read[7:14] = ""
        text_to_read[17], _ = get_and_remove(r"\\f16\\fs18\\b1.+", text_to_read[17])
        text_to_read[9:17] = ""

    if index == 291:
        text = "".join(text_to_read[8:16]) + text_to_read[18] + text_to_read[19] + text_to_read[22] + text_to_read[23]
        text_to_read[4] = text_to_read[4].replace("\\column", text, 1)
        text_to_read[18] = text_to_read[19] = text_to_read[22] = text_to_read[23] = ""
        text_to_read[8:16] = ""

    if index == 293:
        text_to_read[4] = """<table> <tr> <th>Extension</th> <th>Description</th> </tr> <tr> <td>-01</td> <td>New prescription</td> </tr> <tr> <td>-02</td> <td>Repeat prescription</td> </tr> <tr> <td>-09</td> <td>Unspecified or not known wheather new or repeart prescription</td> </tr> </table>"""
        text_to_read[6] = text_to_read[6].replace("\\f7\\fs20\\b0", "")
        text_to_read[5] = text_to_read[5].replace("\\f7\\fs20\\b0", "")
        text_to_read[6] += """\\f7\\fs19\\b0\\charscalex115\\cf2 90762-00\\tab Treatment planning of pharmacotherapy, primary\\expnd0\\expndtw2  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 course\\par\\f7\\fs19\\b0\\charscalex115\\cf2 90762-01\\tab Treatment planning of pharmacotherapy, secondary\\expnd0\\expndtw1  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 course\\par"""

    if index == 294:
        text_to_read.pop(0)
        text_to_read.pop(0)
        text_to_read.pop(0)
        text_to_read.pop(0)

    if index == 295:
        text_to_read[14], text_to_read[30] = get_and_remove(r"^\\pard.+?\\par", text_to_read[30])

    if index == 296:
        text_to_read[4] = text_to_read[20] + text_to_read[4]
        text_to_read[13], found = get_and_remove(r"{\\pard.+\\sb106", text_to_read[13])
        text_to_read[6] += found
        text_to_read[21] = text_to_read[7] + text_to_read[21]
        text_to_read[22] = text_to_read[8] + text_to_read[22]
        text_to_read[23] = text_to_read[9] + text_to_read[23]
        text_to_read[24] = text_to_read[10] + text_to_read[24]
        text_to_read[25] = text_to_read[11] + text_to_read[25]
        text_to_read[26] = text_to_read[12] + text_to_read[26]
        text_to_read[27] = text_to_read[13] + text_to_read[27]
        text_to_read[20] = text_to_read[7] = text_to_read[8] = text_to_read[9] = text_to_read[10] = text_to_read[11] = \
            text_to_read[12] = text_to_read[13] = ""
        text = "".join(text_to_read[16:20])
        text_to_read[16:20] = ""
        text_to_read[20] += """\\f4\\fs18\\b0\\charscalex95\\cf2 Ultrasound in conjunction with endoscopy\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li1362\\sl-213\\sb112\\f11\\fs18\\b0\\i1\\cf2 Code also:\\par\\pard\\plain\\s9\\ls451\\ilvl0\\nooverflow\\nocwrap\\lnbrkrule\\li1477\\fi-115\\sl-220\\tx1478\\f4\\fs18\\b0\\charscalex95\\cf2 endoscopic procedure(s) (see Alphabetic\\expnd-4\\expndtw-18  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 Index)\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li341\\sl240\\slmult1\\sb168\\f7\\fs19\\b0\\charscalex115\\cf2 90908-01 High intensity focused ultrasound [HIFUS]\\par"""
        new_text = """\\f7\\fs19\\b0\\expnd1\\expndtw3\\charscalex115\\cf2 55808-00 \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 Ultrasound of shoulder or upper arm 55812-00\\tab Ultrasound of chest or abdominal\\expnd3\\expndtw17  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 wall\\par"""
        text_to_read[23] = text_to_read[23].replace("\\sl412", new_text + text)

    if index == 297:
        text_to_read[5] += text_to_read[20]
        found, text_to_read[10] = get_and_remove(r"{\\pard.+?\\par", text_to_read[10])
        text_to_read[8] += found
        text_to_read[11] += text_to_read[24]
        text_to_read[19] = text_to_read[28]
        text_to_read[23] = text_to_read[23].replace("bone", " 1956 Computerised tomography of facial bone")
        text_to_read[24] += """\\f7\\fs19\\b0\\charscalex115\\cf2 56022-00 Computerised tomography of facial bone\\cell}"""
        text_to_read[20] = text_to_read[28] = ""

    if index == 298:
        text_to_read.pop(0)
        text_to_read.pop(0)
        text_to_read[2] = """\\f7\\fs19\\b0\\charscalex115\\cf2 56036-00 Computerised tomography of facial\\par""" + text_to_read[2]
        t_56101_00, text_to_read[2] = get_and_remove(r"}f7\\fs19.+?\\par", text_to_read[2])
        t_56107_00, text_to_read[3] = get_and_remove(r"}f7\\fs19.+?\\par", text_to_read[3])
        found, text_to_read[4] = get_and_remove(r"\\f4\\fs18\\b0.+?\\par", text_to_read[4])
        text_to_read[3] = text_to_read[3].replace("\\sb99", found)
        found, text_to_read[4] = get_and_remove(r"\\f7\\fs19\\b0\\charscalex110\\cf2.+?\\par", text_to_read[4])
        text_to_read[3] = text_to_read[3].replace("\\sb168", found)
        text_to_read[4] = text_to_read[4].replace("Includes:", "Includes: upper abdomen ").replace("Excludes:", "Excludes: computerised tomography for spiral angiography (57350 [1966])")
        text_to_read[5] += text_to_read[17]
        text_to_read[6] += text_to_read[18]
        text_to_read[7] += text_to_read[19]
        text_to_read[8] += text_to_read[20]
        text_to_read[9] += text_to_read[21]
        text_to_read[10] += text_to_read[22]
        text_to_read[13] = t_56101_00.replace("}f7", "\\f7") + text_to_read[13]
        text_to_read[14] = t_56107_00.replace("}f7", "\\f7") + text_to_read[14]
        text_to_read[6] = text_to_read[6].replace("chest\\cell", "chest without, then with , intravenous contrast medium \\cell}")
        text_to_read[8] = text_to_read[6].replace("abdomen\\cell", "abdomen without, then with , intravenous contrast medium \\cell}")
        text_to_read[10] = text_to_read[10].replace("and\\cell", "and abdomen without, then with , intravenous contrast medium \\cell}")
        text_to_read[17] = text_to_read[18] = text_to_read[19] = text_to_read[20] = text_to_read[21] = text_to_read[22] = ""
        text_to_read.append("""\\f7\\fs19\\b0\\expnd1\\expndtw3\\charscalex115\\cf2 56234-00 \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 Computerised tomography of spine with intravenous contrast medium, multiple regions\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li1485\\fi-114\\ri1980\\qj\\sl232\\slmult1\\f4\\fs18\\b0\\charscalex90\\cf2 Computerised\\expnd-4\\expndtw-21  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 tomography\\expnd-4\\expndtw-21  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 of\\expnd-4\\expndtw-21  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 multiple\\expnd-4\\expndtw-21  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 regions\\expnd-4\\expndtw-21  \\f4\\fs18\\b0\\i0\\expnd-2\\expndtw-8 of \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 spine,\\expnd-3\\expndtw-15  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 without,\\expnd-3\\expndtw-14  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 then\\expnd-3\\expndtw-14  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 with,\\expnd-3\\expndtw-15  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 intravenous\\expnd-3\\expndtw-14  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 contrast \\f4\\fs18\\b0\\i0\\charscalex95 medium\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li1372\\fi-1021\\ri2180\\sl228\\slmult1\\sb176\\tx1372\\f7\\fs19\\b0\\charscalex115\\cf2 90912-00\\tab Computerised tomography of spine, unspecified\\expnd1\\expndtw3  \\f7\\fs19\\b0\\i0\\expnd0\\expndtw0 region\\par""")

    if index == 300:
        t_57350_07, text_to_read[4] = get_and_remove(r"\\f7\\fs19.+?\\par", text_to_read[4], count=1)
        text_to_read[5] = t_57350_07 + text_to_read[5]

    if index == 301:
        text_to_read[3] += """\\f7\\fs19\\b0\\cf2 57918-00\\tab Radiography of salivary gland \\f4\\fs18\\b0\\i0\\charscalex95 Radiography of salivary calculus \\f4\\fs18\\b0\\i0\\charscalex100 Sialography\\par"""
        text_to_read[12] = text_to_read[4] + text_to_read[12]
        text_to_read[4], text_to_read[8] = get_and_remove(r"\\sb168\\f7\\fs19.+?\\par", text_to_read[8], count=1)
        text_to_read[13] = text_to_read[6] + text_to_read[13]
        text_to_read[14] = text_to_read[7] + text_to_read[14]
        text_to_read[7], text_to_read[8] = get_and_remove(r"\\sb97\\f7\\fs19.+?\\par", text_to_read[8])
        found, text_to_read[8] = get_and_remove(r"\\f12\\fs19.+?\\par", text_to_read[8])
        text_to_read[15] = found + text_to_read[15]
        text_to_read[6] = ""

    if index == 303:
        found, text_to_read[57] = get_and_remove(r"{\\pard.+?\\cell}", text_to_read[57])
        text_to_read[8] += found
        found, text_to_read[18] = get_and_remove(r"}f7.+", text_to_read[18])
        text_to_read[66] = found.replace("}f7", "\\f7") + text_to_read[66]
        found, text_to_read[19] = get_and_remove(r"}f7.+", text_to_read[19])
        text_to_read[67] = found.replace("}f7", "\\f7") + text_to_read[67]
        text_to_read[19] = text_to_read[19].replace("kidney", "kidney ureter ")
        text_to_read[69] = text_to_read[22] + text_to_read[69]
        text_to_read[70] = text_to_read[25] + text_to_read[70]
        found, text_to_read[78] = get_and_remove(r"{\\pard.+?\\cell}", text_to_read[78])
        text_to_read[34] += found
        text_to_read[57] = "{\\pard\\plain\\" + text_to_read[57]
        text_to_read[78] = "{\\pard\\plain\\" + text_to_read[78]
        text_to_read[39] = text_to_read[79] + text_to_read[39]
        text_to_read[79] = """{\\pard\\f12\\fs19\\b1\\i0\\dn14\\charscalex100\\cf5{\\chcbpat2 1985\\tab }\\tab \\f12\\fs19\\b1\\i0\\cf2 Arthrography\\cell}"""
        text_to_read[81] += """\\f16\\fs18\\b1\\i1\\up0 Includes: \\f4\\fs18\\b0\\i0 contrast\\expnd-3\\expndtw-17  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 study\\cell}\\f4\\fs18\\b0\\i0\\up14\\charscalex95 preliminary plain\\expnd-1\\expndtw-5  \\f4\\fs18\\b0\\i0\\expnd0\\expndtw0 film\\cell}"""
        found, text_to_read[43] = get_and_remove(r"}f12.+", text_to_read[43])
        text_to_read[82] = found.replace("}f12", "\\f12") + text_to_read[82]
        text_to_read[22] = text_to_read[25] = ""

    if index == 304:
        text_to_read.pop(0)

    if index == 305:
        text_to_read[16] = text_to_read[16].replace("\\sb168", text_to_read[15])
        found, text_to_read[18] = get_and_remove(r"{\\pard.+?\\par", text_to_read[18])
        text_to_read[16] += found
        text_to_read[15] = ""

    if index == 307:
        found, text_to_read[4] = get_and_remove(r"}f7.+", text_to_read[4])
        text_to_read[22] = "{\\pard" + found.replace("}f7", "\\f7") + text_to_read[22]
        found, text_to_read[7] = get_and_remove(r"}f7.+", text_to_read[7])
        text_to_read[25] = found.replace("}f7", "\\f7") + text_to_read[25]
        found, text_to_read[8] = get_and_remove(r"}f7.+", text_to_read[8])
        text_to_read[26] = found.replace("}f7", "\\f7") + text_to_read[26]
        found, text_to_read[9] = get_and_remove(r"\\f7\\fs19.+", text_to_read[9])
        text_to_read[27] = found + text_to_read[27]
        text_to_read[23] = "{\\pard\\f7\\fs19\\b0\\i0\\expnd0\\expndtw0\\up6 61383-00\\cell}" + text_to_read[23]
        found, text_to_read[36] = get_and_remove(r"^\\pard.+?\\par", text_to_read[36])
        text_to_read[3] += found

    if index == 308:
        text_to_read[22] = text_to_read[8] + text_to_read[22]
        text_to_read[23] = text_to_read[9] + text_to_read[23]
        text_to_read[26] = text_to_read[10] + text_to_read[26]
        text_to_read[28] = text_to_read[11] + text_to_read[28]
        text_to_read[30] = text_to_read[12] + text_to_read[30]
        text_to_read[31] = text_to_read[13] + text_to_read[31]
        text_to_read[32] += """\\f7\\fs19\\b0\\charscalex115\\cf2 tomography [SPECT]\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li1323\\fi-1022\\ri1591\\sl228\\slmult1\\sb177\\f7\\fs19\\b0\\charscalex115\\cf2 90905-03 Localised study not elsewhere classified, with positron emission tomography [PET]\\par\\pard\\plain\\s1\\nooverflow\\nocwrap\\lnbrkrule\\li1323\\sl-220\\sb51\\f16\\fs18\\b1\\i1\\cf2 Includes: \\f4\\fs18\\b0\\i0 administration of:\\par\\pard\\plain\\s9\\ls467\\ilvl1\\nooverflow\\nocwrap\\lnbrkrule\\li2175\\fi-115\\sl-220\\tx2176\\f4\\fs18\\b0\\charscalex95\\cf2 radioactive tracer\\par"""
        text_to_read[8] = text_to_read[9] = text_to_read[10] = text_to_read[11] = text_to_read[12] = text_to_read[13] = ""

    if index == 309:
        text_to_read[5] += text_to_read[10]
        found, text_to_read[8] = get_and_remove(r"{\\pard.+\\cell}", text_to_read[8])
        text_to_read[7] += text_to_read[11] + text_to_read[12] + found + text_to_read[13]
        text_to_read[10] = text_to_read[11] = text_to_read[12] = text_to_read[13] = ""

    return text_to_read

