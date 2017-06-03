import xmltodict
import os.path
import sys
from xml.etree import ElementTree as et

# Read trasnslations from a xliff file and update base Localization of a xcode storyboard

trans_to_use = "target"  # choose which xliff translation to use (source ore target)

my_path = os.path.abspath(os.path.dirname(__file__))
storyboard_source_path = os.path.join(my_path, "Main.storyboard.original")
storyboard_dest_path = os.path.join(my_path, "Main.storyboard")
translation_path = os.path.join(my_path, "translation.xliff")


reload(sys) # just to be sure
sys.setdefaultencoding('utf-8')

def change_description(type, node):
    if type not in node.attrib:
            return
    key = node.attrib["id"]+"."+type
    value = node.attrib[type];
    if key in translations:
        value = translations[key]
    node.attrib[type] = value

def change_button_descriptions(node):
    for state in node:
        if state.tag == "state":
            key = node.attrib["id"] + "." + state.attrib["key"] + "Title"
            if "title" not in state.attrib:
                continue
            if key in translations:
                state.attrib["title"] = translations[key]


def change_segmentedButton_descriptions(node):
    segments =  node.find("segments")
    i = 0
    for segment in segments:
        key = node.attrib["id"] + "." + "segmentTitles["+str(i)+"]"
        i = i + 1
        if "title" not in segment.attrib:
            continue
        if key in translations:
            segment.attrib["title"] = translations[key]


def find_components(node):
    key = node.tag
    if              key == "tabBarController" or \
                    key == "tableViewController" or \
                    key == "barButtonItem" or \
                    key == "tabBarItem" or \
                    key == "navigationItem":
        change_description("title", node)

    if key == "tableViewSection":
        change_description("headerTitle", node)

    if key == "label":
        change_description("text", node)

    if key == "textField":
        change_description("placeholder", node)
        change_description("text", node)

    if key == "button":
        change_button_descriptions(node)

    if key == "segmentedControl":
        change_segmentedButton_descriptions(node)

    #TODO: implement other components

    for o in node:
        find_components(o)


with open(translation_path) as fd:   # read translations
    trans = xmltodict.parse(fd.read())
translations = dict()
for file in trans["xliff"]["file"]:
    if ".storyboard" in file["@original"]:
        for tr in file["body"]["trans-unit"]:
            # lexer = shlex.shlex(tr["note"], posix=True)
            # lexer.whitespace_split = True
            # lexer.whitespace = ';'
            # matches = dict(pair.replace(" ", "").split('=', 1) for pair in lexer)
            #
            # dest = tr["@id"] if matches["Class"] == 'UISegmentedControl' else tr["@id"].split(".")[1]
            # translations[tr["@id"]] = matches[dest]
            translations[tr["@id"]] = tr[trans_to_use]["#text"]


doc = et.parse(storyboard_source_path) # read storyboard
scenes = doc.getroot().find("scenes")
for scene in scenes:
    objects = scene.find("objects")
    for object in objects:
        find_components(object)

doc.write(storyboard_dest_path)
