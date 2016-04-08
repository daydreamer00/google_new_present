from bs4 import BeautifulSoup as bs
import json
import copy
import datetime


json_base_filename = "json/Election_2016_"
json_sub_filenames = ["", "democratic", "republican"]
json_filenames = [json_base_filename+s+".json" for s in json_sub_filenames]

with open("google.html", "r") as f:
    html_doc = f.read()

soup = bs(html_doc, 'html.parser')
res_ol = soup.find_all(id="ires")[0].ol
res_div_template = res_ol.find_all('div', class_="g")[0]
res_ol.clear()

for s in json_filenames:
    json_str = ""
    with open(s, "r") as f:
        json_str = f.read()
    crawl_res = json.loads(json_str)
    timestamp = crawl_res["timestamp"]
    contents = crawl_res["content"]

    out_soup = copy.copy(soup)
    out_soup_res_ol = out_soup.find_all(id="ires")[0].ol
    timefield = out_soup.find(id="resultStats")
    timefield.string = "last updated time is "+ datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    keywordfield = out_soup.find(id="sbhost")

    keywords = s.split('/')[1] .split('.')[0]
    print keywords.split('_')
    keywordfield["value"] = ' '.join(keywords.split('_'))

    for content in contents:
        raw_html_tr = content["raw_html_tr"][0]
        title = content["title"][0]
        press = content["press"]
        time = content["time"]
        url = "https://www.google.com.hk"+content["url"][0]
        print url
        img_urls = content["img_url"]
        if len(img_urls):
            img_url = img_urls[0]
        else:
            img_url = ""

        tgt_html = content["tgt_html"]
        tgt_url = content["tgt_url"]
        abstract = content["abstract"][0]

        res_div = copy.copy(res_div_template)
        tds = res_div.table.tr.find_all('td')
        tds[0].h3.a["href"] = url
        tds[0].h3.a.string = title
        tds[0].find_all('div', class_="slp")[
                        0].span.string = press + " - " + time
        tds[0].find_all('div', class_="st")[0].string = abstract
        tds[1].a["href"] = img_url
        tds[1].a.img["src"] = img_url
        tds[1].find_all('div', class_="f")[0].string = press
        out_soup_res_ol.append(res_div)

    html_filename = "html/"+keywords+'.html'
    with open(html_filename, "w") as f:
        f.write(str(out_soup))
