import requests
import time

def main():
    link = "https://pcpartpicker.com/user/kotikpoo000/saved/d8TWZL";
    parseLink(link)

def parseLink(link):
    url = requests.get(link)
    htmltext = url.text.encode('utf-8').strip();
    moment=time.strftime("%b_%d_%Y__%H:%M:%S",time.localtime())
    file = open("pcParts_" + moment+ ".txt", "w")
    file.write(link)
    file.write("\n")
    arr = get_parts(htmltext)
    for x in arr:
        file.write(x)
        file.write("\n")
    file.write("cost = $" + str(get_price(htmltext)))
    file.close()

def get_price(htmltext):
    str = "total-price part-list-totals"
    i = htmltext.index("$", htmltext.index(str))
    end = htmltext.index("<", i)
    return float(htmltext[i+1:end])

def get_parts(htmltext):
    str = "var product_name_map = {"
    i = htmltext.index(str)
    iend = i+len(str);
    l = htmltext.index("};", i)
    parts = htmltext[iend+1:l]
    parts = parts.replace('\u002D','-').replace('\u0022','\"').split(',')
    for i in range(len(parts)):
        parts[i] = parts[i].strip().split("\"")[1]
    return parts

if __name__ == "__main__": main()
