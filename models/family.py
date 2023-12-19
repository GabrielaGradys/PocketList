import json
from dataclasses import dataclass
from datetime import datetime, date


def my_encoder(obj):
    if hasattr(obj, "to_dict"):
        return obj.to_dict()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")


@dataclass
class Age:
    birthdate: datetime
    years: int = None
    months: int = None
    days: int = None
    
    def __init__(self, birthdate):
        self.birthdate = birthdate
        today = datetime.today()
        day_difference = datetime.today().day - self.birthdate.day

        self.years = today.year - self.birthdate.year
        self.months = today.month - self.birthdate.month
        self.days = today.day - self.birthdate.day

        if day_difference < 0:
            self.months -= 1
            days_in_previous_month = (
                    today - datetime(today.year, today.month, 1)).days
            self.days += days_in_previous_month

        if self.months < 0:
            self.years -= 1
            self.months += 12

    def __repr__(self):
        if self.years < 8:
            return f"{self.years} ({self.months};{self.days})"
        return f"{self.years}"


@dataclass
class FamilyMember:
    name: str
    birthdate: str | date

    @property
    def age(self):
        return Age(self.birthdate)

    @property
    def status(self):
        return "dorosły" if self.age.years > 18 else "nastolatek" if \
            self.age.years > 12 else "dziecko"

    def __post_init__(self):
        if isinstance(self.birthdate, str):
            dates_formats = ["%Y-%m-%d", "%d-%m-%Y", "%d.%m.%Y", "%d %m %Y"]
            for date_format in dates_formats:
                try:
                    self.birthdate = datetime.strptime(self.birthdate, date_format).date()
                    return
                except ValueError:
                    continue
            raise ValueError(
                f"Date string '{self.birthdate}' does not match any known format")

    def to_dict(self):
        return {
            "name": self.name,
            "birthdate": str(self.birthdate)
        }

    def __repr__(self):
        return f"{self.name} ({self.age})"


class Family:

    def __init__(self):
        data = json.loads(open("data/family.json", "r").read())
        self.members = {key: FamilyMember(**val) for key, val in data.items()}

    def add_member(self, member=None):
        if not isinstance(member, FamilyMember):
            try:
                member = FamilyMember(**member)
            except Exception as e:
                print(f"Exception occurred while adding data.{e}")
                data = {}
                for parameter in FamilyMember.__dataclass_fields__:
                    data[parameter] = input(f"Pass the {parameter}:")
                member = FamilyMember(**data)

        self.members[member.name] = member
        self.save_family()

    def save_family(self):
        data = json.dumps(self.members, default=my_encoder)
        with open("data/family.json", "w") as file:
            file.write(data)
