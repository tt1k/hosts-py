import pandas as pd
import requests
from datetime import datetime

github_url = [
  'github.githubassets.com',
  'central.github.com',
  'desktop.githubusercontent.com',
  'assets-cdn.github.com',
  'camo.githubusercontent.com',
  'github.map.fastly.net',
  'github.global.ssl.fastly.net',
  'gist.github.com',
  'github.io',
  'github.com',
  'api.github.com',
  'raw.githubusercontent.com',
  'user-images.githubusercontent.com',
  'favicons.githubusercontent.com',
  'avatars5.githubusercontent.com',
  'avatars4.githubusercontent.com',
  'avatars3.githubusercontent.com',
  'avatars2.githubusercontent.com',
  'avatars1.githubusercontent.com',
  'avatars0.githubusercontent.com',
  'avatars.githubusercontent.com',
  'codeload.github.com',
  'github-cloud.s3.amazonaws.com',
  'github-com.s3.amazonaws.com',
  'github-production-release-asset-2e65be.s3.amazonaws.com',
  'github-production-user-asset-6210df.s3.amazonaws.com',
  'github-production-repository-file-5c1aeb.s3.amazonaws.com',
  'githubstatus.com',
  'github.community',
  'media.githubusercontent.com'
]

def findIP(host:str):
    host_body = host.split(".")
    if len(host_body) == 2:
        host = "https://" + host + ".ipaddress.com"
    else:
        host = "https://" + host_body[len(host_body) - 2] + "." + host_body[len(host_body) - 1] + ".ipaddress.com/" + host
    response = requests.get(host)
    if response.status_code == 200:
        html_tables_data = pd.read_html(response.text)
        ip_table_data = []
        
        for table_data in html_tables_data:
            if list(table_data.head()) == ['Name', 'Type', 'Data']:
                ip_table_data = table_data                
        
        ip_type_data = list(ip_table_data.iloc[:, 1])
        ip_address_data = list(ip_table_data.iloc[:, 2])
        for idx, item in enumerate(ip_type_data):
            if item == "A":
                return ip_address_data[idx]
        return "failed"
    else:
        return "failed"

def findIPWrapper(host:str):
    result = "failed"
    try:
        result = findIP(host)
    except:
        try:
            result = findIP(host)
        except:
            print("[error]: {} is failed", host)
    return result

def main():
    hosts_content = ""
    
    for idx, url in enumerate(github_url):
        print("[process]: {}/{} {}".format(idx + 1, len(github_url), url))
        result = findIPWrapper(url)
        if result and len(result):
            host_content = result + " " * (30 - len(result)) + url + "\n"
            hosts_content += host_content

    readme_template = "# hosts-py\nhosts-py is a python version of [hosts-js](https://github.com/IcedOtaku/hosts-js)\n## hosts\nupdate at: {}\n```shell\n{}```\n## license\n[MIT](LICENSE)".format(datetime.now().strftime("%Y-%m-%d %H:%m:%S"), hosts_content)
    readme_file = open("README.md", "w")
    readme_file.write(readme_template)
    readme_file.close()

main()