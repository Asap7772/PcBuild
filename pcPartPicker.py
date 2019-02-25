import requests
import time
import re

# link = "https://pcpartpicker.com/list/rqrZKB";

class pcPartPicker(object):
    def checkLink(self, link):
        regex = re.compile(
                r'^(?:http|ftp)s?://' # http:// or https://
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
                r'localhost|' #localhost...
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
                r'(?::\d+)?' # optional port
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        return re.match(regex, link) is not None

    def parseLink(self, link):
        # error checking
        if(not self.checkLink(link)):
            link = 'https://' + link;
            if(not self.checkLink(link)):
                return "N/A";
        try:
            string = '';
            url = requests.get(link)
            htmltext = url.text.encode('utf-8').strip();
            moment=time.strftime("%b_%d_%Y__%H:%M:%S",time.localtime())
            path = "buildsRequested/"
            file = open(path + "pcParts_" + moment+ ".txt", "w")
            file.write(link)
            file.write("\n")
            string = string + "Link to Build:" + link + '\n\nParts Included:' + '\n===============\n'
            arr = self.get_parts(htmltext)
            i = 1;
            for x in arr:
                file.write(x)
                file.write("\n")
                string = string + str(i) + ") " + x + '\n'
                i = i+1;
            file.write("cost = $" + str(self.get_price(htmltext)))
            string = string + "\ncost = $" + str(self.get_price(htmltext))
            file.close()
            return string.replace('\n', '<br>')
        except requests.exceptions.ConnectionError, e:
            return "N/A";
        except ValueError, e:
            return "N/A";

    def get_price(self, htmltext):
        str = "total-price part-list-totals"
        i = htmltext.index("$", htmltext.index(str))
        end = htmltext.index("<", i)
        return float(htmltext[i+1:end])

    def get_parts(self, htmltext):
        str = "var product_name_map = {"
        i = htmltext.index(str)
        iend = i+len(str);
        l = htmltext.index("};", i)
        parts = htmltext[iend+1:l]
        parts = parts.replace('\u002D','-').replace('\u0022','\"').split(',')
        for i in range(len(parts)):
            parts[i] = parts[i].strip().split("\"")[1]
        return parts
