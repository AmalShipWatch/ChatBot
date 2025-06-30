import threading
from typing import List, Dict
from datetime import date, datetime, timedelta
import random

# In-memory storage for demo (thread-safe)
class DataStorage:
    def __init__(self):
        self._lock = threading.Lock()
        self._data = []
        self._initialized = False

    def generate_dummy_data(self):
        data = []
        report_types = ['At Sea', 'Arrival',  'Arrival At Berth', 'In Port', 'Departure From Berth', 'In Port', 'Departure']

        def random_start_date():
            return datetime.now().date() - timedelta(days=random.randint(5, 15))

        # Ensure two different start dates
        start_date1 = random_start_date()
        while True:
            start_date2 = random_start_date()
            if start_date2 != start_date1:
                break

        # Create date ranges
        date_list1 = [start_date1 + timedelta(days=i) for i in range(5)]
        date_list2 = [start_date2 + timedelta(days=i) for i in range(5)]

        for dt in date_list1:
            data.append({
                'Vessel_name': 'Navig8 Messi',
                'Date': dt.strftime('%Y-%m-%d'),
                'Laden_Ballst': 'Laden',
                'Report_Type': report_types[0]
            })

        for i, dt in enumerate(date_list2):
            data.append({
                'Vessel_name': 'Navig8 Guard',
                'Date': dt.strftime('%Y-%m-%d'),
                'Laden_Ballst': 'Ballast',
                'Report_Type': report_types[i+2]
            })

        return data

    def initialize(self):
        with self._lock:
            if not self._initialized:
                self._data = self.generate_dummy_data()
                self._initialized = True

    def add_entry(self, entry: Dict):
        with self._lock:
            vessel_name = entry['Vessel_name']
            entry_date = entry['Date']
            # Convert date string to date for comparison
            if isinstance(entry_date, str):
                try:
                    entry_date_obj = datetime.strptime(entry_date, "%Y-%m-%d").date()
                except Exception:
                    entry_date_obj = entry_date
            else:
                entry_date_obj = entry_date
            # Check for existing entry for this vessel and date
            updated = False
            for row in self._data:
                if row['Vessel_name'] == vessel_name:
                    # Ensure row['Date'] is a date
                    if isinstance(row['Date'], str):
                        try:
                            row['Date'] = datetime.strptime(row['Date'], "%Y-%m-%d").date()
                        except Exception:
                            pass
                    if row['Date'] == entry_date_obj:
                        # Update the entry fields
                        row['Laden_Ballst'] = entry.get('Laden_Ballst', row.get('Laden_Ballst'))
                        row['Report_Type'] = entry.get('Report_Type', row.get('Report_Type'))
                        updated = True
                        break
            if not updated:
                # Add as new entry
                entry['Date'] = entry_date_obj
                self._data.append(entry)
            # Sort vessel entries by date (descending)
            vessel_entries = [row for row in self._data if row['Vessel_name'] == vessel_name]
            vessel_entries.sort(key=lambda x: x['Date'], reverse=False)
            self._data = [row for row in self._data if row['Vessel_name'] != vessel_name]
            self._data.extend(vessel_entries)

    def get_data(self) -> List[Dict]:
        with self._lock:
            return list(self._data)

    def clear(self):
        with self._lock:
            self._data = []
            self._initialized = False

storage = DataStorage()
storage.initialize()
