# -*- coding: utf-8 -*-
#
# Copyright 2008 GAEO Team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""" GAEO view form helpers """

def country_select(id = "", name = "", **opts):
    """
    Create a select field that lists all country/region selection
      - id: the id of the select field
      - name: the name of the select field
      - opts:
          - class: class attribute
          - style: style attribute
    """
    countries = ["Afghanistan","Åland Islands","Albania","Algeria","American Samoa","Andorra","Angola",
            "Anguilla","Antarctica","Antigua and Barbuda","Argentina","Armenia","Aruba","Australia","Austria",
            "Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin",
            "Bermuda","Bhutan","Bolivia","Bosnia and Herzegovina","Botswana","Bouvet Island","Brazil",
            "British Indian Ocean Territory","Brunei Darussalam","Bulgaria","Burkina Faso","Burundi","Cambodia",
            "Cameroon","Canada","Cape Verde","Cayman Islands","Central African Republic","Chad","Chile","China",
            "Christmas Island","Cocos (Keeling) Islands","Colombia","Comoros","Congo",
            "Congo, The Democratic Republic of the","Cook Islands","Costa Rica","Côte d'Ivoire","Croatia","Cuba",
            "Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt",
            "El Salvador","Equatorial Guinea","Eritrea","Estonia","Ethiopia","Falkland Islands (Malvinas)",
            "Faroe Islands","Fiji","Finland","France","French Guiana","French Polynesia",
            "French Southern Territories","Gabon","Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guadeloupe","Guam","Guatemala","Guernsey","Guinea",
            "Guinea-Bissau","Guyana","Haiti","Heard Island and McDonald Islands","Holy See (Vatican City State)",
            "Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran, Islamic Republic of","Iraq",
            "Ireland","Isle of Man","Israel","Italy","Jamaica","Japan","Jersey","Jordan","Kazakhstan","Kenya",
            "Kiribati","Korea, Democratic People's Republic of","Korea, Republic of","Kuwait","Kyrgyzstan",
            "Lao People's Democratic Republic","Latvia","Lebanon","Lesotho","Liberia","Libyan Arab Jamahiriya",
            "Liechtenstein","Lithuania","Luxembourg","Macao","Macedonia, Republic of",
            "Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Martinique",
            "Mauritania","Mauritius","Mayotte","Mexico","Micronesia, Federated States of","Moldova",
            "Monaco","Mongolia","Montenegro","Montserrat","Morocco","Mozambique","Myanmar","Namibia","Nauru",
            "Nepal","Netherlands","Netherlands Antilles","New Caledonia","New Zealand","Nicaragua","Niger",
            "Nigeria","Niue","Norfolk Island","Northern Mariana Islands","Norway","Oman","Pakistan","Palau",
            "Palestinian Territory, Occupied","Panama","Papua New Guinea","Paraguay","Peru","Philippines",
            "Pitcairn","Poland","Portugal","Puerto Rico","Qatar","Reunion","Romania","Russian Federation",
            "Rwanda","Saint Barthélemy","Saint Helena","Saint Kitts and Nevis","Saint Lucia",
            "Saint Martin (French part)","Saint Pierre and Miquelon","Saint Vincent and the Grenadines","Samoa","San Marino",
            "Sao Tome and Principe","Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Singapore",
            "Slovakia","Slovenia","Solomon Islands","Somalia","South Africa",
            "South Georgia and the South Sandwich Islands","Spain","Sri Lanka","Sudan","Suriname",
            "Svalbard and Jan Mayen","Swaziland","Sweden","Switzerland","Syrian Arab Republic",
            "Taiwan","Tajikistan","Tanzania, United Republic of","Thailand","Timor-Leste",
            "Togo","Tokelau","Tonga","Trinidad and Tobago","Tunisia","Turkey","Turkmenistan",
            "Turks and Caicos Islands","Tuvalu","Uganda","Ukraine","United Arab Emirates","United Kingdom",
            "United States","United States Minor Outlying Islands","Uruguay","Uzbekistan","Vanuatu","Venezuela",
            "Viet Nam","Virgin Islands, British","Virgin Islands, U.S.","Wallis and Futuna","Western Sahara",
            "Yemen","Zambia","Zimbabwe"]
    html = '<select id="%s" name="%s">' % (id, name)
    for c in countries:
        html += '<option>%s</option>' % c
    html += '</select>'
    return html
    
def date_select(id = "", name = "", **opts):
    """
    Create a date select fields
    """
    import time
    now = time.localtime(time.time())
    
    field = {}
    html = ''
    
    default_date = opts.get('default', (now[0], now[1], now[2]))
    
    # Year Field
    # start year
    start_year = opts.get('start_year', now[0]-5)
    end_year = opts.get('end_year', now[0]+5)
    field['year'] = '<select id="%s_y" name="%s[y]">\n' % (id, name)
    for y in range(start_year, end_year):
        if default_date[0] == y:
            field['year'] += '<option selected>%d</option>\n' % y
        else:
            field['year'] += '<option>%d</option>\n' % y
    field['year'] += '</select>\n'
    if opts.has_key('year_label'):
        field['year'] = '<label for="%s_y">%s</label> %s' % (id, opts['year_label'], field['year'])
    
    # Month Field
    months = opts.get('months', [1,2,3,4,5,6,7,8,9,10,11,12])
    field['month'] = '<select id="%s_m" name="%s[m]">\n' % (id, name)
    for m in months:
        if default_date[1] == m:
            field['month'] += '<option selected>%d</option>\n' % m
        else:    
            field['month'] += '<option>%d</option>\n' % m
    field['month'] += '</select>\n'
    if opts.has_key('month_label'):
        field['month'] = '<label for="%s_m">%s</label> %s' % (id, opts['month_label'], field['name'])
    
    # Date Field
    field['date'] = '<select id="%s_d" name="%s[d]">\n' % (id, name)
    for d in range(1, 32):
        if default_date[2] == d:
            field['date'] += '<option selected>%d</option>\n' % d
        else:
            field['date'] += '<option>%d</option>\n' % d
    field['date'] += '</select>\n'
    if opts.has_key('date_label'):
        field['date'] = '<label for="%s_d">%s</label> %s' % (id, opts['date_label'], field['date'])
    
    # field order
    field_order = opts.get('order', ['year', 'month', 'date'])
    for o in field_order:
        html += field[o]
    
    return html
