import requests
import sys
from bs4 import BeautifulSoup

def index_finder(parsed_data):
    index = 0
    for i in range(0, len(parsed_data)):
        if parsed_data[i].text.find("Anmeldung vom") != -1:
            return i
    

def save_termins(Schedules, td_advanced):
    for i in range(len(td_advanced)):
        if td_advanced[i].text.strip() == "-":
            Termin = {"Course ID" : td_advanced[i-1].text.strip(),
                "Day" : td_advanced[i+1].text.strip(),
                "Date" : td_advanced[i+2].text.strip(),
                "Time" : td_advanced[i+3].text.strip(),
                "Teacher" : td_advanced[i+4].text.replace(f"\n", "").strip(),
                "Possible participants" : td_advanced[i+5].text.strip(),
            "Applied participants" : td_advanced[i+6].text.strip(),
                "Assigned participants" : td_advanced[i+7].text.strip(),
                "Way of teaching" : td_advanced[i+8].text.strip(),
                }
            Schedules.append(Termin)


def print_termins(Schedules):
    for termin in Schedules:
        print(f"{termin['Date']} is taught by {termin['Teacher']}, and has ", sep = "", end = "")
        print(f"{int(termin['Possible participants'])-int(termin['Assigned participants'])} number of free places")


def schedule_search(url):

    r = requests.get(url)   
    soup = BeautifulSoup(r.text, 'html.parser')
    data_table = soup.find_all("table")
    tr_child = data_table[index_finder(data_table)].find_all('tr') 
    td_child = tr_child[index_finder(tr_child)].find_all('td')
    return td_child[index_finder(td_child)].find_all('td')



def main():
    Schedules = []
    while True:
        try:
            url = sys.argv[1]
            break
        except IndexError:
            url = input("Please enter the link of the desired course: ").strip()
            if url.find("https://www.kusss.jku.at/kusss/lvaregistrationlist.action?courseclass=") == -1:
                print("Invalid URL")
                continue
            else:
                break
        

    save_termins(Schedules, schedule_search(url))
    print_termins(Schedules)



if __name__ == "__main__":
    main()
