from fifa_script.fifa import GetData
import xlsxwriter

class Extract:

    def __init__(self):
        self.data = GetData()
        self.data.getPlayers(False)
        self.data.getCoach(False)
        self.data.getGroup(False)
        self.workbook = xlsxwriter.Workbook('Report.xlsx')


    def createWorkSheet(self):
        self.teams = self.data.teams_group
        i = 0
        for group_name in self.teams.keys():
            self.workSheet = self.workbook.add_worksheet(group_name)
            self.designSheet()

            j = 0
            k = 0
            for team_name in self.teams[group_name]:
                players = self.data.players_by_country[team_name]

                if i < len(self.data.coach_name):
                    coach = self.data.coach_name[i]
                    if j < 4:
                        self.dataToSheet(group_name, team_name, coach, players, k, k+1)
                        j+=1
                    i+=1
                k+=3
        self.workbook.close()


    def designSheet(self):
        self.workSheet.set_column('A:B', 30)
        self.workSheet.set_column('D:E', 30)
        self.workSheet.set_column('G:H', 30)
        self.workSheet.set_column('J:K', 30)
        self.workSheet.set_row(0, 30)
        self.workSheet.set_row(1, 30)
        marge_format = self.workbook.add_format({'bold':1, 'border':1, 'align':'center', 'valign':'vcenter', 'fg_color':'yellow', 'font_size':14})
        self.workSheet.write('A1', 'Team Name', marge_format)
        self.workSheet.write('B1', 'Coach Name', marge_format)
        self.workSheet.write('D1', 'Team Name', marge_format)
        self.workSheet.write('E1', 'Coach Name', marge_format)
        self.workSheet.write('G1', 'Team Name', marge_format)
        self.workSheet.write('H1', 'Coach Name', marge_format)
        self.workSheet.write('J1', 'Team Name', marge_format)
        self.workSheet.write('K1', 'Coach Name', marge_format)
        self.workSheet.set_row(3, 30)
        self.workSheet.merge_range(3,0,3,1, 'Players Name', marge_format)
        self.workSheet.merge_range(3,3,3,4, 'Players Name', marge_format)
        self.workSheet.merge_range(3,6,3,7, 'Players Name', marge_format)
        self.workSheet.merge_range(3,9,3,10, 'Players Name', marge_format)

    
    def dataToSheet(self, groupName, teamName, coachName, players, first_col, last_col):
        data_style = self.workbook.add_format({'border':1, 'align':'center', 'valign':'vcenter', 'fg_color':'green', 'font_color': 'white'})
        try:

            if first_col == 0 and last_col == 1:
                self.workSheet.write('A2', teamName, data_style)
                self.workSheet.write('B2', coachName, data_style)
            elif first_col == 3 and last_col == 4:
                self.workSheet.write('D2', teamName, data_style)
                self.workSheet.write('E2', coachName, data_style)
            elif first_col == 6 and last_col == 7:
                self.workSheet.write('G2', teamName, data_style)
                self.workSheet.write('H2', coachName, data_style)
            elif first_col == 9 and last_col == 10:
                self.workSheet.write('J2', teamName, data_style)
                self.workSheet.write('K2', coachName, data_style)

            i = 4
            for player in players:
                self.workSheet.set_row(i, 20)
                #print(i,' ', first_col, ' ', i, ' ', last_col)
                self.workSheet.merge_range(i, first_col, i, last_col, player, data_style)
                i+=1
        except Exception as e:
            print(e)

