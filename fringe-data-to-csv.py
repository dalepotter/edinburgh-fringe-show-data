import csv
import json
import requests

FRINGE_API = "https://tickets.edfringe.com/solr/select?q=*%3A*&facet=true&fl=sf_meta_id%2Cname%2Cgroup_name%2Cname_prefix%2Cdescription%2Ccalendar_data%2Cvenue_name%2Cvenue_number%2Cvenue_url%2Cevent_url%2Ccategory%2Csubcategories%2Clarge_image_url%2Ctimes%2Cname_sort_s%2Cvenue_name_sort_s%2Csuitability%2Csuitability_restriction%2Cduration%2Cscore%2Cis_accessible%2Cvenue_space_wheelchair_audience_access%2Cvenue_space_level_access%2Cvenue_space_hearing_loop%2Cvenue_space_wheelchair_accessible_toilet%2Ccaptioning%2Caudio_description%2Csigned_performance%2Crelaxed_performance%2Cnon_english_accessible%2Cdate_summary%2Cfriends%2Cis_cancelled&qf=name%5E10%20keywords%20group_name%20description&facet.field=category&facet.field=subcategories&facet.field=suitability&facet.field=group_country&f.subcategories.facet.limit=100&json.nl=map&sort=name_sort_s%20asc&defType=edismax&start={0}&wt=json&json.wrf=jQuery1110036043487745473946_1502960704766"


def clean_response(input_str):
    """Clean a response to make it valid JSON (i.e. remove 'jQuery' wrapper).

    Args:
        input_str (str): A raw string response from the Edinburgh Fringe SOLR search API.

    Returns:
        str: A string which should be valid JSON.
    """
    pos_json_start = input_str.find('(') + 1
    pos_json_end = input_str.rfind(')')
    return input_str[pos_json_start:pos_json_end]


with open('shows.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=' ',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for start_num in range(0, 100, 10):
        url = FRINGE_API.format(start_num)
        resp = requests.get(url)

        valid_json = clean_response(resp.text)
        json_dict = json.loads(valid_json)
        for show in json_dict['response']['docs']:
            writer.writerow([show['name']])  # Write name as a proof oc concept.
