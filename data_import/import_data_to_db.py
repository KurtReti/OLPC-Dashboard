import os
import traceback

from datetime import datetime

import csv
# activity.csv
import thefuzz.fuzz

from apps.db_models.account import Account
from apps.db_models.activity import Activity
from apps.db_models.app import App
from apps.db_models.app_category_association import AppCategoryAssociation
from apps.db_models.category import Category
from apps.db_models.developer import Developer
from apps.db_models.device import Device
from apps.db_models.device_ownership import DeviceOwnership
from apps.db_models.naplan import Naplan
from apps.db_models.school import School
from database import Session, create_tables, drop_tables
from thefuzz import process, fuzz

drop_tables()
create_tables()

session = Session()

# school-locations.csv
schools_file = input("Please enter schools filepath: ")
schools = []
i = 0
with open(schools_file) as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)

    for row in reader:
        school = {}
        school["school_id"] = row[header.index("ACARA School ID")]
        school["school_name"] = row[header.index("School Name")]
        school["suburb"] = row[header.index("Suburb")]
        school["state"] = row[header.index("State")]
        school["postcode"] = '{:04d}'.format(int(row[header.index("Postcode")]))
        school["school_sector"] = row[header.index("School Sector")]
        school["school_type"] = row[header.index("School Type")]
        school["longitude"] = row[header.index("Longitude")]
        school["latitude"] = row[header.index("Latitude")]

        schools.append(school)

session.bulk_insert_mappings(
    School,
    schools
)
session.commit()

schools_info = session.query(School.id, School.school_id, School.school_name, School.state).all()
schools_by_school_id = {school_id: id for id, school_id, _, _ in schools_info}
schools_by_school_name = [(school_name, school_id, state, id) for id, school_id, school_name, state in schools_info]

# snlookups#####.txt
devices_file = input("Please enter devices filepath: ")
devices = []
i = 0
with open(devices_file) as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    header = next(reader)
    for row in reader:
        devices.append({"serial": row[header.index("serial")], "hash": row[header.index("hash")]})

session.bulk_insert_mappings(
    Device,
    devices
)
session.commit()

device_ids = session.query(Device.id, Device.serial, Device.hash).all()
devices_by_hash = {hash: id for id, serial, hash in device_ids}

devices_by_serial = {serial: id for id, serial, hash in device_ids}

# naplan.log
naplan_file = input("Please enter naplan filepath: ")
naplans = []
with open(naplan_file, encoding='UTF-8') as csvfile:
    reader = csv.reader(csvfile, delimiter='#')
    for row in reader:
        if row[-1] == "empty":
            continue
        naplan = {}
        naplan["year"] = row[1]
        naplan["areaOfStudy"] = row[8]
        naplan["grade"] = row[9]
        naplan["averageScore"] = row[10]
        naplan["numStudents"] = row[11]
        if int(row[0]) not in schools_by_school_id:
            print(row, "school does not exist in ACARA data")
            continue
        naplan["schoolid"] = schools_by_school_id[int(row[0])]
        naplans.append(naplan)

session.bulk_insert_mappings(
    Naplan,
    naplans
)
session.commit()

# sfmigrations_accnt########.txt
accounts_file = input("Please enter accounts filepath: ")
accounts_done = set()
accounts = []
id_asset_to_account_id = {}
skip_matching = input("Skip manual matching: ")

with open(accounts_file) as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    header = next(reader)
    for row in reader:
        account_id = row[header.index("account_id")]
        id_asset_to_account_id[row[header.index("id_accnt")]] = account_id
        account_name = row[header.index("account_name")]
        if account_id in accounts_done:
            continue
        match = False
        smatch = process.extract([account_name, None, None, None], schools_by_school_name, processor=lambda x: x[0],
                                 scorer=fuzz.partial_token_sort_ratio, limit=10)
        if smatch[0][1] == 100 and smatch[0][0][2] == row[header.index("shipping_state")]:
            school_id = smatch[0][0][3]
            match = True
        elif not skip_matching:
            print()
            for i, r in enumerate(smatch):
                print(i, r)
            match = input(f"Select match match for {account_name} {row[header.index('shipping_state')]}: ")
            if match:
                school_id = smatch[int(match)][0][3]
        if not match:
            accounts_done.add(account_id)
            continue

        account_name = smatch[0]
        account = {}
        account["schoolid"] = school_id
        account["account_id"] = account_id
        accounts.append(account)
        accounts_done.add(account_id)

session.bulk_insert_mappings(
    Account,
    accounts
)
session.commit()

account_ids = session.query(Account.id, Account.account_id).all()
account_id_to_id = {account_id: id for id, account_id in account_ids}

# appCategory##########.txt
apps_file = input("Please enter apps filepath: ")
apps_to_skip = []
categories = {}
developers = {}

with open(apps_file, encoding='UTF-8') as csvfile:
    reader = csv.reader(csvfile, delimiter='#')
    for row in reader:
        if row[-1] == "empty":
            continue
        developer = row[1]
        if developer.upper() not in developers:
            developers[developer.upper()] = {"name": developer}

        for category in set(row[3].replace("&amp;", "and").split(",")):
            if category not in categories:
                categories[category] = {"name": category}

session.bulk_insert_mappings(
    Developer,
    developers.values()
)
session.bulk_insert_mappings(
    Category,
    categories.values()
)

session.commit()

developer_ids = session.query(Developer.id, Developer.name).all()
developers = {name.upper(): id for id, name in developer_ids}

category_ids = session.query(Category.id, Category.name).all()
category_ids = {name: id for id, name in category_ids}

app_category_associations = {}
apps = []
with open(apps_file, encoding='UTF-8') as csvfile:
    reader = csv.reader(csvfile, delimiter='#')
    for row in reader:
        if row[-1] == "empty":
            continue
        try:
            app = {}
            app["appid"] = row[0]
            developer = row[1]
            app["developerid"] = developers[developer.upper()]
            app["appName"] = row[2]
            for category in set(row[3].replace("&amp;", "and").split(",")):
                if app["appid"] not in app_category_associations:
                    app_category_associations[app["appid"]] = []

                app_category_associations[app["appid"]].append(category_ids[category])
            app["rating"] = float(row[4])
            app["numDownloads"] = row[5]
            apps.append(app)
        except:
            print(row)
            traceback.print_exc()
            apps_to_skip.append(row[0])
            continue

session.bulk_insert_mappings(
    App,
    apps
)

session.commit()

app_ids = session.query(App.id, App.appid).all()
app_ids = {aid: id for id, aid in app_ids}
app_category_associations_ = []
for aid, id in app_ids.items():
    for categoryid in app_category_associations[aid]:
        app_category_associations_.append({"appid": id, "categoryid": categoryid})

session.bulk_insert_mappings(
    AppCategoryAssociation,
    app_category_associations_
)

session.commit()

# sfmigrations_asset####.txt
device_ownership_file = input("Please enter device ownership filepath: ")
device_ownerships = []

with open(device_ownership_file) as csvfile:
    reader = csv.reader(csvfile, delimiter='\t')
    header = next(reader)
    for row in reader:
        if row[header.index("serial_number")] not in devices_by_serial:
            continue
        try:
            deviceid = devices_by_serial[row[header.index("serial_number")]]
            device_ownership = {}
            device_ownership["deviceid"] = deviceid
            device_ownership["accountid"] = account_id_to_id[id_asset_to_account_id[row[header.index("id_asset")]]]
            device_ownerships.append(device_ownership)
        except:
            traceback.print_exc()
            pass

session.bulk_insert_mappings(
    DeviceOwnership,
    device_ownerships
)
session.commit()
activities_file = input("Please enter activities filepath: ")
activities = []
with open(activities_file) as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader)
    for row in reader:
        if row[header.index("appid")] not in app_ids:
            continue
        if row[header.index("uid")] not in devices_by_hash:
            continue
        activity = {}
        activity["deviceid"] = devices_by_hash[row[header.index("uid")]]
        activity["appid"] = app_ids[row[header.index("appid")]]
        activity["started"] = datetime.fromtimestamp(int(row[header.index("started")]))
        activity["duration"] = row[header.index("duration")]
        activities.append(activity)
session.bulk_insert_mappings(
    Activity,
    activities
)
session.commit()
