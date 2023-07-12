import random

class Player:
    def __init__(self, name, bowling, batting, fielding, running, experience):
        self.name = name
        self.bowling = bowling
        self.batting = batting
        self.fielding = fielding
        self.running = running
        self.experience = experience

    def __str__(self):
        return self.name

class Teams:
    def __init__(self, name, players):
        self.name = name
        self.players = players
        self.captain = None
        self.batting_order = []
        
    def select_captain(self):
        # Select a captain based on certain criteria
        captain = [player for player in self.players if player.experience > 0.9 and player.batting > 0.7 and player.fielding > 0.7]
        self.captain = random.choice(captain) if captain else random.choice(self.players)

    def send_next_player(self):
        # Get the next player in the batting order
        return self.batting_order.pop(0) if self.batting_order else None

    def choose_bowler(self):
        # Choose a bowler based on their bowling skill
        bowlers = [player for player in self.players if player.bowling > 0.6]
        return random.choice(bowlers) if bowlers else random.choice(self.players)

    def set_batting_order(self):
        # Set the batting order based on players' batting skill
        self.batting_order = sorted(self.players, key=lambda x: x.batting, reverse=True)

class Field:
    def __init__(self, field_size, fan_ratio, pitch_conditions, home_advantage):
        self.field_size = field_size
        self.fan_ratio = fan_ratio
        self.pitch_conditions = pitch_conditions
        self.home_advantage = home_advantage

class Umpire:
    def __init__(self, team_a, team_b):
        self.scores = {team_a.name : 0, team_b.name : 0}
        self.wickets = {team_b.name : 0, team_a.name : 0}
        self.currentBats = False
        self.striker = {"striker": None, "non_striker" : None}
        self.order = None
        self.overs = 0
        self.balls = 1
        self.maxOver = 10

    def simulate_ball(self, batting_team, bowling_team, batsman, bowler, field):
        commentary = ""
        runs_scored = 0

        batting_skill = batsman.batting
        bowling_skill = bowler.bowling
        out_probability = 1 - min(batting_skill, bowling_skill + 0.2)
       
    
        if random.random() < out_probability:
            # Batsman is out
            self.currentBats = True
            self.wickets[batting_team.name] += 1
            commentary = f"{batsman.name} is OUT!"

        else:
            run = [0, 1, 2, 3, 4, 6, "wide_ball", "no_ball"]

            # Assign weights based on field conditions
            run_weights = (40, 50, 60, 10, 30, 20, 10, 10) if field.field_size == "large" or field.pitch_conditions == "dry" else (20, 60, 40, 10, 40, 30, 10, 10)
            runs_scored = random.choices(run, weights=run_weights, k=1)

            if runs_scored[0] == "wide_ball":
                # Wide ball, add 1 run to the score
                self.balls -= 1
                self.scores[batting_team.name] += 1
                commentary = "wide ball!" 

            elif runs_scored[0] == "no_ball":
                # No ball, add 1 run to the score
                self.balls -= 1
                if self.currentBats:
                    self.currentBats = False
                self.scores[batting_team.name] += 1
                commentary = "No ball!"
            else:
                # Runs scored, update the score
                self.scores[batting_team.name] += runs_scored[0]
                commentary = f"{batsman.name} scores {runs_scored[0]} run(s)!"
                
            if runs_scored[0] == 1 or runs_scored[0] == 3:
                # Switch strike if 1 or 3 runs are scored
                temp = self.striker["non_striker"]
                self.striker["non_striker"] = self.striker["striker"]
                self.striker["striker"] = temp

        return commentary

class Ball:
    def __init__(self, batsman, bowler, batting_team, bowling_team):
        self.batsman = batsman
        self.bowler = bowler
        self.batting_team = batting_team
        self.bowling_team = bowling_team

class Commentator:
    def __init__(self, umpire,field):
        self.field = field
        self.umpire = umpire

    def provide_commentary(self, ball):
        batting_team = ball.batting_team
        bowler = ball.bowler
        batsman = ball.batsman

        outcome = self.umpire.simulate_ball(ball.batting_team, ball.bowling_team, batsman, bowler, self.field)

        commentary = f"{batsman.name} is facing {bowler.name} from {batting_team.name}.\n"
        commentary += f"{outcome}\n"
        commentary += f"{batting_team.name} is now at {self.umpire.scores[batting_team.name]}/{self.umpire.wickets[batting_team.name]} in {self.umpire.overs}.{self.umpire.balls} overs."
        return commentary

class Match:
    def __init__(self, team_a, team_b, field):
        self.team_a = team_a
        self.team_b = team_b
        self.field = field
        self.umpire = Umpire(team_a, team_b)
        self.commentator = Commentator(self.umpire, field)
    
    def start_match(self):
        # Select captains and batting order for both teams
        self.team_a.select_captain()
        self.team_b.select_captain()
        self.team_a.set_batting_order()
        self.team_b.set_batting_order()

        # Perform toss to determine which team will bat first
        toss = [self.team_a, self.team_b]
        batting_team = random.choice(toss)
        bowling_team = self.team_b if batting_team == self.team_a else self.team_a

        # Start the match by playing
        self.playing(batting_team, bowling_team, 0)

        # End the match and declare the winner
        self.end_match()


    def playing(self, batting_team, bowling_team, order):
        if order >= 2:
            return
        else:
            if order == 0:
                self.umpire.order = bowling_team
                print(f"{batting_team.name} - Captain: {batting_team.captain}")
                print(f"{bowling_team.name} - Captain: {bowling_team.captain}\n")

            print(f"Batting Order: {batting_team.name}\n")
            for i, player in enumerate(batting_team.batting_order, start=1):
                print(f"{i}. {batting_team.name} {player.name}")
            print()

            self.umpire.striker["striker"] = batting_team.send_next_player()
            self.umpire.striker["non_striker"] = batting_team.send_next_player()

            overs = 0
            while overs < self.umpire.maxOver:
                current_bowler = bowling_team.choose_bowler()

                while self.umpire.balls < 7:
                    if order == 1:
                        if self.umpire.scores[batting_team.name] >= self.umpire.scores[bowling_team.name]:
                            return
                    
                    if self.umpire.currentBats is True:
                        self.umpire.striker["striker"] = batting_team.send_next_player()
                        self.umpire.currentBats = False

                    if self.umpire.striker["striker"] is None or self.umpire.wickets[batting_team.name] >= 11:
                        self.umpire.overs = 0
                        self.umpire.balls = 1
                        return self.playing(bowling_team, batting_team, order + 1)  
                     
                    balls = Ball(self.umpire.striker["striker"], current_bowler, batting_team, bowling_team)
                    commentary = self.commentator.provide_commentary(balls)
                    print(commentary)

                    self.umpire.balls += 1

                self.umpire.balls = 1
                overs += 1
                self.umpire.overs = overs

            if self.umpire.overs >= self.umpire.maxOver:
                self.umpire.overs = 0
                self.umpire.balls = 1
                return self.playing(bowling_team, batting_team, order + 1)

    def end_match(self):
        # Display match result and the winner
        print("Match ended!")
        print(f"{self.team_a.name} - Total Score: {self.umpire.scores[self.team_a.name]}/{self.umpire.wickets[self.team_a.name]}")
        print(f"{self.team_b.name} - Total Score: {self.umpire.scores[self.team_b.name]}/{self.umpire.wickets[self.team_b.name]}")
        
        if self.umpire.scores[self.team_a.name] > self.umpire.scores[self.team_b.name]:
            print(f"{self.team_a.name} won the match!")
        elif self.umpire.scores[self.team_a.name] < self.umpire.scores[self.team_b.name]:
            print(f"{self.team_b.name} won the match!")
        else:
            if self.umpire.scores[self.team_a.name] == self.umpire.scores[self.team_b.name] and self.umpire.overs == self.umpire.maxOver and self.umpire.balls == 6:
                print("The match ended in a tie.")
            elif self.umpire.maxOver == 0:
                print("The match ended in a tie.")
            else:
                print(f"{self.umpire.order.name} won the match!")


if __name__ == "__main__":
    team_a = []

    # name, bowling, batting, fielding, running, experience
    player1 = Player("Faf du Plessis", 0.3, 0.9, 0.8, 0.9, 0.9) 
    player2 = Player("Virat Kohli", 0.4, 10, 0.9, 0.9, 0.9)
    player3 = Player("Glenn Maxwell", 0.8, 0.9, 0.8, 0.7, 0.9)
    player4 = Player("Mahipal Lomror", 0.8, 0.7, 0.6, 0.6, 0.6)
    player5 = Player("Dinesh Karthik", 0.3, 0.7, 0.6, 0.6, 0.7)
    player6 = Player("Wanindu Hasaranga", 0.8, 0.6, 0.7, 0.8, 0.6)
    player7 = Player("Shahbaz Ahmed", 0.8, 0.7, 0.7, 0.6, 0.5)
    player8 = Player("Harshal Patel", 0.8, 0.7, 0.7, 0.6, 0.6)
    player9 = Player("Karn Sharma", 0.8, 0.8, 0.6, 0.6, 0.8)
    player10 = Player("Mohammed Siraj", 0.9, 0.6, 0.7, 0.7, 0.7)
    player11 = Player("Josh Hazlewood", 0.8, 0.7, 0.6, 0.7, 0.6)
    team_a.append(player1)
    team_a.append(player2)
    team_a.append(player3)
    team_a.append(player4)
    team_a.append(player5)
    team_a.append(player6)
    team_a.append(player7)
    team_a.append(player8)
    team_a.append(player9)
    team_a.append(player10)
    team_a.append(player11)

    team_b = []
    # name, bowling, batting, fielding, running, experience
    player1 = Player("MS Dhoni", 0.6, 0.8, 0.8, 0.9, 10) 
    player2 = Player("Devon Conway", 0.5, 0.9, 0.7, 0.7, 0.9)
    player3 = Player("Ruturaj Gaikwad", 0.5, 0.8, 0.7, 0.8, 0.8)
    player4 = Player("Ben Stokes", 0.7, 0.8, 0.7, 0.6, 0.8)
    player5 = Player("Ambati Rayudu", 0.4, 0.8, 0.6, 0.6, 0.9)
    player6 = Player("Shivam Dube", 0.3, 0.8, 0.6, 0.8, 0.7)
    player7 = Player("Moeen Ali", 0.8, 0.8, 0.8, 0.7, 0.9)
    player8 = Player("Ravindra Jadeja", 0.9, 0.8, 0.5, 0.6, 0.7)
    player9 = Player("Deepak Chahar", 0.8, 0.9, 0.7, 0.5, 0.7)
    player10 = Player("Mitchell Santner", 0.8, 0.7, 0.6, 0.6, 0.7)
    player11 = Player("Rajvardhan Hangargekar", 0.7, 0.5, 0.8, 0.7, 0.7)
    team_b.append(player1)
    team_b.append(player2)
    team_b.append(player3)
    team_b.append(player4)
    team_b.append(player5)
    team_b.append(player6)
    team_b.append(player7)
    team_b.append(player8)
    team_b.append(player9)
    team_b.append(player10)
    team_b.append(player11)

    # Create teams
    # Teams (name, team)

    team_a = Teams("RCB", team_a)
    team_b = Teams("CSK", team_b)
    
    # Create field
    # Fields ( field_size = (medium, large), fan_ratio, pitch_conditions = (dry, hard), home_advantage )
    field = Field("large", 0.8, "dry", 0.1)

    # Create match
    # Match ( team_a, team_b, field )
    match = Match(team_a, team_b, field)

    # Start the match
    match.start_match()
