import re
import requests
import csv
import html


def get_emails_from_url(orgid):
    url = 'https://stuactonline.tamu.edu/app/organization/profile/public/id/' + str(orgid)
    r = requests.get(url)
    lines = r.text.split('\n')

    org_name = []
    emails = []
    leader_name = ''

    for line in lines:
        org_name += re.findall(r'<title.*?>.*?</title.*?>', line, re.IGNORECASE)
        emails += re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', line)

        if 'Public Contact Name:' in line:
            leader_name = re.findall(r'<dd.*?>.*?</dd.*?>', line, re.IGNORECASE)
            leader_name = re.sub("<.*?>", "", leader_name[0])  # Remove HTML tags

    name_split = ''
    org_type = ''

    if len(org_name) > 0:
        org_name = re.sub("<.*?>", "", org_name[0])  # Remove HTML tags
        name_split = org_name.split(' - ')
        org_type = name_split[-2]

    if len(emails) > 0:
        return orgid, leader_name, html.unescape(name_split[0].strip()), emails[0], org_type

    return orgid, leader_name, html.unescape(name_split[0].strip()), None, org_type


org_data_list = []

min_org_id = 1
max_org_id = 2300

for i in range(min_org_id, max_org_id+1):
    out = get_emails_from_url(i)
    if out[2].strip() != 'Organizations' and out[-1] == 'Public Profile':
        print('Success:', out)
        org_data_list.append(out)
    else:
        print('Fail:', out)

print('Success Rate:', str(round(100 * len(org_data_list) / (1 + max_org_id - min_org_id), 2)) + '%')

with open('organizations_phonebook.csv', 'w') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['ID', 'Leader Name', 'Name', 'Email', 'Type'])
    for row in org_data_list:
        csv_out.writerow(row)

