"""
Copyright (C) 2023 bkf2020

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, version 3 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from bs4 import BeautifulSoup
import re
import requests
import os

def get_problem_text(year, test, num):
    URL = "https://artofproblemsolving.com/wiki/index.php/" + str(year) + "_" + test + "_Problems/Problem_" + str(num)
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, 'html.parser')
    text = soup.find("div", class_="mw-parser-output")
    try:
        text.find("div", class_="toc").decompose()
    except:
        with open("log.txt", "a") as f:
            f.write("Warning: No table of contents for " + str(year) + " " + str(test) + " Problem # " + str(num) + "\n")
        pass

    to_remove = []
    to_remove.append(text.find("span", {"id": re.compile("(?i)See_Also")}))
    try:
        for avoid in text.find("span", {"id": re.compile("(?i)See_Also")}).parent.next_siblings:
            to_remove.append(avoid)
    except:
        with open("log.txt", "a") as f:
            f.write("Warning: See also link missing for, please revise later " + str(year) + " " + str(test) + " Problem # " + str(num) + "\n")
        pass

    try:
        for remove in to_remove:
            remove.extract()
    except:
        pass

    to_remove = []
    for img in text.find_all("img"):
        try:
            span_alt = soup.new_tag("span")
            span_alt.append(img['alt'])
            img.insert_after(span_alt)
            to_remove.append(img)
        except:
            with open("log.txt", "a") as f:
                f.write("Warning: May be issues with images for " + str(year) + " " + str(test) + " Problem # " + str(num) + "\n")
            pass

    try:
        for remove in to_remove:
            remove.decompose()
    except:
        with open("log.txt", "a") as f:
            f.write("Warning: images may not have been removed properly for " + str(year) + " " + str(test) + " Problem # " + str(num) + "\n")
        pass

    return text.get_text()

try:
    os.mkdir("problems")
    os.mkdir("problems/AMC_8")
    os.mkdir("problems/AMC_10")
    os.mkdir("problems/AMC_12")
    os.mkdir("problems/AIME")
    open("log.txt", 'x')
except:
    pass

tests = ["AMC_8", "AMC_10", "AMC_12", "AIME"]
test_types = {}
test_types["AMC_8"] = [""]
test_types["AMC_10"] = ["A", "B"]
test_types["AMC_12"] = ["A", "B"]
test_types["AIME"] = ["I", "II"]

for test in tests:
    for year in range(2010, 2024):
        if(year == 2023 and (test == "AMC_10" or test == "AMC_12")):
            continue
        if(year == 2021 and (test == "AMC_8")):
            continue
        
        try:
            os.mkdir("problems/" + test + "/" + str(year))
        except:
            pass

        for test_type in test_types[test]:
            ending = 26
            if(test == "AIME"):
                ending = 16
            for num in range(1, ending):
                try:
                    os.mkdir("problems/" + test + "/" + str(year) + "/" + test_type)
                    open("problems/" + test + "/" + str(year) + "/" + test_type + "/" + str(num) + ".txt", 'x')
                except:
                    pass
                with open("problems/" + test + "/" + str(year) + "/" + test_type + "/" + str(num) + ".txt", "w") as f:
                    print("Creating " + test + test_type + str(year) + " Problem #" + str(num))
                    try:
                        if(test == "AIME"):
                            f.write(get_problem_text(year, test + "_" + test_type, num))
                        else:
                            f.write(get_problem_text(year, test + test_type, num))
                    except:
                        with open("log.txt", "a") as f:
                            f.write("Something wrong with " + test + test_type + str(year) + " Problem #" + str(num) + "\n")
