from datetime import datetime as dt, timedelta as td
import random
import csv
import json
        
class InvalidInput(Exception):
    pass

class Chore:
    def __init__(self, chore, status= "not started yet", due_date = None, category ='general'):
        if not chore:
            raise InvalidInput ('chore name cant be empty!')
        self.chore = chore

        valid_status = ['not started yet', 'on progress', 'done']
        if status not in valid_status:
            raise InvalidInput ('invalid status!, status must be "not started yet", "on progress", or "done"')
        self.status = status
        if due_date is None:
            due_date = dt.now()+ td(days=2)
        self.due_date = due_date

        self.category = category
 

    def to_dict(self):
        data = {
            'chore': self.chore,
            'status' : self.status,
            'due_date': self.due_date.strftime("%Y-%m-%d"),
            'category': self.category
            }
        return data

class ChoreManager:
    def __init__(self, filename):
        self.filename = filename
        self.chores = []        

    def load_chores(self):
        self.chores.clear()
        try:
            with open (self.filename, 'r') as file:
                datas = json.load(file)
                for data in datas:
                    data = Chore(data['chore'], data['status'], dt.strptime(data['due_date'], "%Y-%m-%d"), data['category'])
                    self.chores.append(data)
        except FileNotFoundError:
            print("No chores to load! starting with empty list!")
        except ValueError:
            print("file's corrupted! starting fresh!")

    def save(self):
        dictdata = []
        for chore in self.chores:
            chore = chore.to_dict()
            dictdata.append(chore)
        try:
            with open (self.filename, 'w') as file:
                json.dump(dictdata, file, indent = 4)
                print("Saved to JSON!")
        except TypeError:
            print("Error! cant save to json!")

    def get_valid_day(self):
        while True:
            try:
                due = int(input('Due in how many days (e.g., 2, 3, or leave empty for default due = 2 days): '))
                if due <= 0 :
                    print('Due date cant be minus!')
                    continue
                return due
            except ValueError:
                print('Invalid input!, enter a number like 2, 4, etc')

    def get_valid_status(self):
        while True:
            status = input('Enter status for the chore ("not started", "on progress", or "done"): ').strip().lower()
            valid_status = ['not started yet', 'on progress', 'done']
            if status not in valid_status:
                print("Invalid input! status must be 'not started yet', 'on progress', or 'done'! ")
                continue    
            return status

    def add_chore(self):
        while True:
            chore_name= input('Enter a chore name: ').strip().lower()    
            if not chore_name:
                print('Chore name cant be empty!')
                continue
            duplicate = False
            for chore in self.chores:
                if chore_name == chore.chore:
                    duplicate = True
                    print(f'{chore_name.capitalize()} already exist! pick a more unique name!')
                    break
            if duplicate:        
                continue 
            status = self.get_valid_status()
            due_date = self.get_valid_day()
            final_due = dt.now() + td(days=due_date)
            category = input(f'Enter a category for the "{chore_name}" chore: ').strip().lower()
            new_chore_data = Chore(chore_name,status,final_due,category)
            self.chores.append(new_chore_data)
            return
               
    def update_chore_status(self):
        if not self.chores:
            print('no chores to update!')
            return
        while True:
            user_input = input("enter a chore name to update the status: ").strip().lower()
            found = False
            for chore in self.chores:
                if chore.chore == user_input:
                    found = True
                    while True:
                        new_status = self.get_valid_status()
                        chore.status = new_status
                        print('Status updated!')
                        return
            if not found:
                print("there's no such chore in the list!")
                continue

    def sort_by_due(self):
        sort_by_duedate = sorted(self.chores, key = lambda chore : chore.due_date )
        print("\n{:<20} {:<15} {:<15} {:<15}".format("Chore", "Status", "Due Date", "Category"))  
        print('=' * 65)          
        for i, chore in enumerate(sort_by_duedate, 1):
            print (f'{i}. {chore.chore.capitalize():<17}{chore.status:<15}{chore.due_date.strftime("%Y-%m-%d"):<15}{chore.category.capitalize():<15}')

    def filter_by_category(self):
        category = input("enter a category to filter(e.g, kitchen, living room): ").strip().lower()
        if not category:
            print('Category can not be empty! try again!')
            return
        print(f'\nChore in {category.capitalize():^55}: ')
        print('\n{:20} {:<20} {:<15}'. format("Chore", "Status", "Due Date"))
        found = False
        for i, chore in enumerate(self.chores, 1):
            if category == chore.category:
                print(f'{i}. {chore.chore:<17}{chore.status:<20}{chore.due_date.strftime("%Y-%m-%d"):<15}')
                found = True
        if not found:
            print(f"No chores in {category}!")

    def sort_by_status(self):
        status_order = {
            'not started yet' : 1, 
            'on progress' : 2,
            'done' : 3
            }
        sort_by_stat = sorted(self.chores, key = lambda chore: status_order[chore.status])
        print("\n{:<20} {:<15} {:<15} {:<15}".format("Chore", "Status", "Due Date", "Category"))  
        print('=' * 65)          
        for i, chore in enumerate(sort_by_stat, 1):
            print (f'{i}. {chore.chore.capitalize():<17}{chore.status:<15}{chore.due_date.strftime("%Y-%m-%d"):<15}{chore.category.capitalize():<15}')

    def sort_chores(self):
        print('Sort chores by: ')
        print('1. sort by due date')
        print('2. sort by status')
        print('3. back to main menu')
        while True:
            try: 
                sort_by = int(input('Choose a number between 1-3: '))
                if sort_by == 1:
                    self.sort_by_due()
                elif sort_by == 2:
                    self.sort_by_status()
                elif sort_by == 3:
                    break
                else:
                    print('Invalid input!, choose from 1 to 3 only!')
                    continue
            except ValueError:
                print('Invalid input!, enter a number like 1, 2 or 3!')
  
    def show_all_chores(self):
        if not self.chores:
            print('No chores yet! add some to get started!')
        else: 
            print("\n{:<20} {:<15} {:<15} {:<15}".format("Chore", "Status", "Due Date", "Category"))  
            print('=' * 65)          
            for i, chore in enumerate(self.chores, 1):
                print (f'{i}. {chore.chore.capitalize():<17}{chore.status:<15}{chore.due_date.strftime("%Y-%m-%d"):<15}{chore.category.capitalize():<15}')

    def save_to_csv(self):
        filename = 'choremanager.csv'
        try:
            with open (filename, 'w', newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    'chore',
                    'status',
                    'due date',
                    'category'
                ])

                for chore in self.chores:
                    writer.writerow([
                        chore.chore,
                        chore.status,
                        chore.due_date.strftime("%Y-%m-%d"),
                        chore.category
                    ])
                print(f' saved to CSV!')
        except Exception as e:
            print(f'Error saving to csv : {e}')

    def show_overdue(self):
        overdue = []
        today = dt.now()
        for c in self.chores:
            if c.due_date < today:
                overdue.append(c)
        if not overdue:
            print("No overdue chores! You're on top of things!")
            return
        print("{:^65}".format("Overdue Chores"))
        print('='*65)
        print("\n{:<20} {:<15} {:<15} {:<15}".format("Chore", "Status", "Due Date", "Category"))  
        for i, chore in enumerate(overdue, 1):     
                print (f'{i}. {chore.chore.capitalize():<17}{chore.status:<15}{chore.due_date.strftime("%Y-%m-%d"):<15}{chore.category.capitalize():<15}')
        return overdue

    def suggest_random_chore(self):
        if not self.chores:
            print('No chores to suggest! add some first.')
            return
        overdue = self.show_overdue()
        available = []
        for chore in self.chores:
            if chore not in overdue:
                if chore.status != 'done':
                    available.append(chore)
        if not available:
            print('No suggestion, all chores are done ^^!')
            return
        suggestion = random.choice(available)
        print("Suggested chore ")
        print('='*65)
        print("\n{:<20} {:<15} {:<15} {:<15}".format("Chore", "Status", "Due Date", "Category"))
        print(f'{suggestion.chore.capitalize():<20}{suggestion.status:<15}{suggestion.due_date.strftime("%Y-%m-%d"):<15}{suggestion.category.capitalize():<15}')

filename = "choremanager.json"
manager = ChoreManager(filename)
manager.load_chores()

#main menu
while True:
    print(f"\n=== Chore Tracker ===")
    print("1. Add chore")
    print("2. Update chore status")
    print("3. Show all chores")
    print("4. Suggest a random chore")
    print("5. Sort chores")
    print("6. Filter chores by category")
    print("7. Save to JSON")
    print("8. Export to CSV")
    print("9. Show overdue chores")
    print("10. Load chores")
    print("11. Exit")
    try:
        choice = int(input("Choose an option (1-11): "))
        if choice == 1:
            manager.add_chore()
        elif choice == 2:
            manager.update_chore_status()
        elif choice == 3:
            manager.show_all_chores()
        elif choice == 4:
            manager.suggest_random_chore()
        elif choice == 5:
            manager.sort_chores()
        elif choice == 6:
            manager.filter_by_category()
        elif choice == 7:
            manager.save()
        elif choice == 8:
            manager.save_to_csv()
        elif choice == 9:
            manager.show_overdue()
        elif choice == 10:
            manager.load_chores()
        elif choice == 11:
            manager.save()
            print(f"Goodbye! Your chores are saved.")
            break
        else:
            print("Oops! Please choose a number between 1 and 11.")
    except ValueError:
        print("Invalid input! Enter a number like '1' or '11'.")
