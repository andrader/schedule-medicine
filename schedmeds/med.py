# import time
import datetime as dt
from json import dump, dumps
import json
from pathlib import Path
import pickle
import re
from time import sleep

from .parse_timedelta import parse_timedelta

class Med:
    def __init__(
        self, name, dose_interval, total_period=None, number_doses=None, history=[]
    ) -> None:

        self.name = name
        self.dose_interval = parse_timedelta(dose_interval)

        if total_period:
            self.total_period = parse_timedelta(total_period)
        elif number_doses:
            self.number_doses = int(number_doses)
        else:
            raise ValueError("")

        if history:
            self.history = history[:]
            self.start_time = self.history[0]
        else:
            self.start_time = dt.datetime.now()
            self.history = [self.start_time]

    def get_remaining_doses(self):

        end_time = self.start_time + self.total_period
        last_dose = self.history[-1]
        dose_interval = self.dose_interval

        available_tdelta = end_time - last_dose
        n_doses_remaining = available_tdelta // dose_interval

        return [last_dose + (i + 1) * dose_interval for i in range(n_doses_remaining)]

    def register_intake(self, dose_datetime="now"):
        if dose_datetime == "now":
            dose_datetime = dt.datetime.now()
        elif isinstance(dose_datetime, dt.datetime):
            pass
        else:
            dose_datetime = dt.datetime.fromisoformat(dose_datetime)
        
        if dose_datetime not in self.history:
            self.history.append(dose_datetime)
            return True
        else:
            return False

    def _str(self):
        nt = "\n\t"
        fmt = "%b %d, %H:%M"
        history = nt.join(t.strftime(fmt) for t in self.history)
        nexts = nt.join(t.strftime(fmt) for t in self.get_remaining_doses())

        s = (
            f"{self.name}:\n"
            f"interval={self.dose_interval}\n"
            f"total_period={str(self.total_period)}\n"
            f"history:\n\t{history}\n"
            f"next:\n\t{nexts}\n"
        )

        return s

    def __repr__(self) -> str:
        #return self.__str__()
        return f"Med({self.name})"
    
    def __str__(self):
        return self.__repr__()
    
        


if __name__ == "__main__":
    amox = Med("Amoxilina", dose_interval="8h", total_period="3d", 
        history=[
            dt.datetime.fromisoformat("2022-08-23 19:00"),
            dt.datetime.fromisoformat("2022-08-24 02:30"),
            dt.datetime.fromisoformat("2022-08-24 07:00")
        ])

    print(amox)

    
