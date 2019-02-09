
from bs4 import BeautifulSoup
import requests
from fake_useragent import UserAgent


class Crawl:

    def __init__(self):
        self.main_url = "https://en.wikipedia.org/wiki/2018_FIFA_World_Cup_squads?fbclid=IwAR2QGPTk-Fs1n5fm7YAUaINFvnlEWzc6n-MQkaJbYBhtOeMPHo-CbBMqEFY"
        self.file_name = "F:\Python Projects\Fifa Web Scraper\html_page\\fifa.txt"


    def getHtmlPage_request(self):
        user_agent = UserAgent()
        header = {'User-Agent': user_agent.chrome}
        try:
            response = requests.get(self.main_url, headers=header)
            # we changing the encoding format to utf-8
            # so that, the charmap encoding error doesn't occur
            with open(self.file_name, 'w', encoding='utf-8') as file:
                # The content of response is being bytes
                # that's why to saved the content in a txt file as a string we have to decode to utf-8
                file.write(response.content.decode('utf-8')), file.close()

        except Exception as e:
            print("\nException occured in getHtmlPage() method\n",e)
        

class GetData:

    def __init__(self):
        self.country_name = []
        self.coach_name = []
        self.players_by_country = {}
        self.tables = ''
        self.teams_group = {}

        with open(Crawl().file_name, 'r', encoding='utf-8') as file:
            self.data = file.read(), file.close()

        self.soup = BeautifulSoup(str(self.data), 'lxml')


    def showData(self, value):
        # print out the COACH's by country
        if value == 3:
            count = 0
            for country in self.country_name:
                if count < len(self.coach_name):
                    print(country,' \t-> ', self.coach_name[count], '\n')
                    count = count + 1

        # print out the PLAYER's by team
        elif value == 2:
            for key in self.players_by_country.keys():
                print('--'*40) # print 40 '--'
                print('\n',key , ' =>')
                for v in self.players_by_country[key]:
                    print(' \t\t-> ',v)

        # print out the GROUP's of team's
        elif value == 1:
            for key in self.teams_group.keys():
                print('\n\n', key, ' =>')
                for v in self.teams_group[key]:
                    print(' \t\t-> ', v)


    # get group name and their team's also
    def getGroup(self, isShow):
        try:
            divs_of_group = self.soup.find('div', attrs={'class', 'toc'})
            li = divs_of_group.ul.find_all('li', attrs={'class', 'toclevel-1'})
            for group_li in li:
                group_name = group_li.a.span.next_sibling.next_sibling.string
                if group_name.find('Group') == -1:
                    continue
                else:
                    teams_li = group_li.ul.find_all('li', attrs={'class', 'toclevel-2'})
                    i = 0
                    teams = []
                    for team in teams_li:
                        if i < 4:
                            teams.append(team.a.span.next_sibling.next_sibling.string)
                            i+=1
                        else:
                            break
                    self.teams_group.update( {group_name : teams} )
            if isShow:
                self.showData(1)

        except Exception as e:
            print(e)
                       


     # get coach name...
    def getCoach(self, isShow):
        try:
            self.tables = self.soup.find_all('table', attrs={'class': 'plainrowheaders'})
            for table in self.tables:
                country_name_h3_tag = table.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling.previous_sibling
                self.country_name.append(country_name_h3_tag.span.text)
                coach_tag = country_name_h3_tag.next_sibling.next_sibling.find_all('a')
                for coach in coach_tag:
                    if coach.string is not None:
                        self.coach_name.append(coach.string)
            if isShow:
                self.showData(3)

        except Exception as e:
            print(e)


    # get players name by team...
    def getPlayers(self, isShow):
        self.getCoach(False)
        try:
            country_length = len(self.country_name)
            i = 0
            for table in self.tables:
                table_rows = table.find_all('tr', attrs={'class', 'nat-fs-player'})
                players_name = list()
                for row in table_rows:
                    players_name.append(row.th.a.string)
                if i < country_length:
                    self.players_by_country.update( {self.country_name[i] : players_name} )
                    i+=1
            if isShow:
                self.showData(2)

        except Exception as e:
            print(e)


    # take user input for showing data...
    def getData(self):
        print("Get all the following data:-> \n")
        print("Please, select an option to get result ... \n1.\tGROUP's \n2.\tPLAYER's \n3.\tCOACH's")
        options = input()

        if int(options) == 1:
            self.getGroup(True)
        elif int(options) == 2:
            self.getPlayers(True)
        elif int (options) == 3:
            self.getCoach(True)
        else:
            print("You entered wrong number. Try a number among the {1, 2, 3} \n")


