"""
District Social Justice Office addresses — Kerala.

Source: https://hpwc.kerala.gov.in/social-justice-offices/
(Kerala State Handicapped Persons Welfare Corporation Limited — official
government site, cross-linking to sjd.kerala.gov.in, the Social Justice
Department itself.)

These are the addresses as published by the government. They are used to
generate real map coordinates via geocode_offices.py — this file itself
has no coordinates, deliberately, so nobody mistakes hand-typed guesses
for verified data.

District names below match the exact strings used in the <select> options
in templates/index.html — this is the join key used at lookup time, so if
the dropdown options ever change, update this dict's keys to match.
"""

DISTRICT_SOCIAL_JUSTICE_OFFICES = {
    "Thiruvananthapuram": {
        "address": "District Social Justice Office, Institution Complex, Near Vocational Training Centre & KSSM, Poojappura, Thiruvananthapuram",
        "phone": "0471-2343241",
    },
    "Kollam": {
        "address": "District Social Justice Office, Kollam Civil Station, Kollam",
        "phone": "0474-2790971",
    },
    "Pathanamthitta": {
        "address": "District Social Justice Office, Mannil Regency Building, Ground Floor, Pathanamthitta",
        "phone": "0468-2325168",
    },
    "Alappuzha": {
        "address": "District Social Justice Office, Building of Federation of Blind, Near General Hospital, Palace Ward, Iron Bridge P.O., Alappuzha",
        "phone": "0477-2253870",
    },
    "Kottayam": {
        "address": "District Social Justice Office, Kottayam Mini Civil Station, Thirunakkara, Kottayam",
        "phone": "0481-2563980",
    },
    "Idukki": {
        "address": "District Social Justice Office, Mini Civil Station, Thodupuzha P.O., Idukki 685584",
        "phone": "0486-2228160",
    },
    "Ernakulam": {
        "address": "District Social Justice Office, Ernakulam Civil Station, Kakkanad, Ernakulam 682030",
        "phone": "0484-2425377",
    },
    "Thrissur": {
        "address": "District Social Justice Office, Thrissur Mini Civil Station, Chembukkavu P.O., Thrissur",
        "phone": "0487-2321702",
    },
    "Palakkad": {
        "address": "District Social Justice Office, Palakkad Civil Station, Palakkad 678001",
        "phone": "0491-2505791",
    },
    "Malappuram": {
        "address": "District Social Justice Office, Civil Station, Malappuram 676505",
        "phone": "0483-2735324",
    },
    "Kozhikode": {
        "address": "District Social Justice Office, Kozhikode Civil Station, Kozhikode 673020",
        "phone": "0495-2371911",
    },
    "Wayanad": {
        "address": "District Social Justice Office, Civil Station, Kalpetta, Wayanad 673122",
        "phone": "04936-205307",
    },
    "Kannur": {
        "address": "District Social Justice Office, Civil Station, F Block, Kannur 670002",
        "phone": "0497-2997811",
    },
    "Kasaragod": {
        # Govt site spells this "Kasargod" — kept as "Kasaragod" here to match
        # the spelling used in templates/index.html's district dropdown.
        "address": "District Social Justice Office, Civil Station, Vidyanagar, Kasaragod 671123",
        "phone": "0499-4255074",
    },
}

# KSHPWC has ONE statewide head office, not one per district. Several
# schemes (ADIP, self-employment loans, skill training, NHFDC loans)
# route here regardless of the applicant's district. Only needs a single
# manual OSM lookup, unlike the 14 above.
#
# Source: https://hpwc.kerala.gov.in/social-justice-offices/ (footer)
KSHPWC_HEAD_OFFICE = {
    "address": "Kerala State Handicapped Persons Welfare Corporation Limited, Poojappura, Thiruvananthapuram – 695 012",
    "phone": "0471-2347768",
}