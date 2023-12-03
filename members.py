from error_handling import AlreadyExists
from read_write import read_data, write_data, create_unique
import re

FILE_NAME = 'members.json'

class LibraryMember:
    members_list = read_data(FILE_NAME)

    @classmethod
    def add_member(cls, name, phone, district):

        pattern = r'^\d{10}$'

        if not bool(re.match(pattern, str(phone))):
            return

        if not cls.members_list:
            cls.members_list = read_data(FILE_NAME)

        for x in cls.members_list:
            if str(phone) in cls.members_list[x]['phone']:
                raise AlreadyExists    
    
        member_id = create_unique(name, district, str(phone))

        if member_id in cls.members_list:
            raise AlreadyExists

        rslt = {'name': name, 'phone': phone, 'district': district}

        cls.members_list[member_id] = rslt

        write_data(cls.members_list, FILE_NAME)
        print("Member Added")