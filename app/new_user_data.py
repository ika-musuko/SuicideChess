def new_user_data(display_name: str, e_mail: str):

    return {
          "displayName" : display_name
        , "draws" : 0
        , "email" : e_mail
        , "emailNotifications" : True
        , "currentGames" : []
        , "gameHistories" : []
        , "losses" : 0
        , "rank" : 0
        , "wins" : 0
    }

