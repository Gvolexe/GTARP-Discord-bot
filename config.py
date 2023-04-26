activitytype = 'Watching'                        #Accepted Values are Watching, Listening, Playing, or Streaming.
botstatusmessage = 'Innovation Roleplay'		#bot status name
guildID =1073604128019853312  					#kai ksana edo
servers =[1073604128019853312]
developerid = 831803232014958642                #id of developer
##############################################################TICKETS
TICKET_CHANNEL = 1074961082734620752 #channel where ticket will be sent
CATEGORY_ID1 = 1075775343371239504 #DONATE CATEGORY
CATEGORY_ID2 = 1075805084711133265 #OTHER CATEGORY
TEAM_ROLE1 = 1075775442700730420 #DONATE MANAGER ROLE
TEAM_ROLE2 = 1073604128103743498 #STAFF TEAM ROLE
LOG_CHANNEL = 1074955853997805569 #Log Channel
SAY_TITLE = "Innovation Rolepay" #say embeded title
ON_DUTY_ROLE = 1073930508930666557
             
statscooldownamount = 30                        #As the bot checks for guild updates using loops, enter a loopcooldown time here, I reccomend 30 seconds as preset, anything under 15 seconds will most likely get you ratelimited by dsicord.
embedcolor = 0x00000



#Server Member Count#
ServerMembersCheckEnabled = False                           #True for enabled, False for disabled
IDofChannelForServerMembers = 1069278368886968426            #ID of Voice channel to update with server member count
NameofStatsChannel1 = str("All Members: ")                  #Adjusts the name of the Voice channel, LEAVE THE SPACE!


#Role 1 Count #                                      
Role1CountCheckEnabled = True                             #True for enabled, False for disabled
IDofRole1 = 1073604128019853315                             #ID of the server role to keep track of
IDofChannelForRole1Check = 1073604129106174002              #ID of Voice channel to update with the Role1 count with the role specified above
NameofRole1Channel = str("🕺Civilians: ")                       #Adjusts the name of the Voice channel, LEAVE THE SPACE!

#Role 2 Count #
Role2CountCheckEnabled = True                                #True for enabled, False for disabled
IDofRole2 = 1073930508930666557                            #ID of the server role to keep track of
IDofChannelForRole2Check = 1073604129106174003              #ID of Voice channel to update with the Role2 count with the role specified above
NameofRole2Channel = str("Staff™ On Duty: ")                       #Adjusts the name of the Voice channel, LEAVE THE SPACE!

#Bot Count #
BotCountCheckEnabled = False                                  #True for enabled, False for disabled
IDofChannelForBotCheck = 000000000000000000                #ID of Voice channel to update with the bot count
NameofBotChannel = str("Bots: ")                           #Adjusts the name of the Voice channel, LEAVE THE SPACE!

#Bans Count #                                     
BansCountCheckEnabled = False                                #True for enabled, False for disabled  
IDofChannelForBansCheck = 000000000000000000               #ID of Voice channel to update with the server ban count
NameofBansChannel = str("Bans: ")                          #Adjusts the name of the Voice channel, LEAVE THE SPACE!