from    channels.generic.websocket  import  AsyncWebsocketConsumer
import                                      json
from    .src.Match                  import  Match
import                                      random

Matches         = {}

waiting         = -1
waiting_room    = 0
mmatch          = None
players         = set()

class   TicTacToeGameConsumer( AsyncWebsocketConsumer ):

#-------------------------------------Receive------------------------------------#

    async def   connect( self ):
        # print("connect")
        self.__id               = self.scope["payload"]["id"]
        self.__room_id          = ""

        global waiting, waiting_room, mmatch, Matches

        await self.accept()

        if  self.__id in players:
            await self.send( json.dumps({
                "type"  : "already",
            }))
            await self.close(3001)
            return
        

        players.add( self.__id )

        if waiting == -1:
            waiting_room    += 1
            self.__room_id  = str(waiting_room)
            waiting         = self.__id
            mmatch          = Match( self.__room_id )

            await self.channel_layer.group_add(
                self.__room_id,
                self.channel_name 
            )
            mmatch.add_player( self.__id )
            return
        
        mmatch.add_player( self.__id )

        self.__room_id              = str(waiting_room)
        Matches[ self.__room_id ]   = mmatch
        # Create match in database
        
        mmatch                      = None
        waiting                     = -1

        await self.channel_layer.group_add(
            self.__room_id,
            self.channel_name 
        )

        await self.channel_layer.group_send(
              self.__room_id, {
                  "type"      : "start",
              }
        )

#-------------------------------------Disconnect------------------------------------#

    async def   disconnect( self, code=None ):
        global waiting

        if code == 3001 or self.__room_id not in Matches:
            if self.__id == waiting:
                waiting = -1
                players.remove( self.__id )

            await self.close()
            return 

        players.remove( self.__id )
        Matches[ self.__room_id ].remove_player( self.__id )

        await self.channel_layer.group_discard(
            self.__room_id,
            self.channel_name
        )

        await self.close()

        await self.channel_layer.group_send(
            self.__room_id, {
                "type"  : "abort",

                "state" : "ABORT",
            }
        )

        #save db
        #remove from Matches

#-------------------------------------Receive------------------------------------#


    async def receive( self, text_data=None ):

        text_data = json.loads(text_data)

        response = await self.__simulate( text_data["move"], int(text_data["player"]) )

        print( response,flush=True )
        await self.channel_layer.group_send(
            self.__room_id,
            {
                "type"      : "move",

                "status"    : response["status"] if "status" in response else "",
                "sub-win"   : response["sub-win"] if "sub-win" in response else "",
                "winner"    : response["winner"] if "winner" in response else "",
                "move"      : text_data["move"] if "move" in text_data else "",
                "player"    : text_data["player"] if "player" in text_data else "",
            }
        )

    #  ----------------------------------------------------------Events Send----------------------------------------------------------------------- #

    async def start( self, data ):
        await self.send( json.dumps( {
            "type"      : "start",

            "status"    : "PLAYING",
            "player-me" : self.__id,
            "choice-me" : "x" if self.__id == 1 else "o",
            "player-op" : 2 if self.__id == 1 else 1,
            "choice-op" : "o" if self.__id == 1 else "x",
            "turn"      : random.randint(0, 2),
        }))
        
        # create table on db

    async def move( self, data ):
        # data["stas"] = "DRAW"

        # if data["status"] == "WIN":

        await self.send( json.dumps( {
            "type"      : "move",

            "status"    : data["status"] if "status" in data else "",
            "move"      : data["move"] if "move" in data else "",
            "player"    : data["player"] if "player" in data else "",
            "sub-win"   : data["sub-win"] if "sub-win" in data else "",
            "winner"    : data["winner"] if "winner" in data else "",
        }))

    async def abort( self, data ):
        await self.send( json.dumps( {
            "type"      : "abort",

            "status"    : "ABORT",
        }))

        # Write win on db

    async def save_db( self, match_id, status, winner ):
        matc

    #  --------------------------------------------------------------Game-------------------------------------------------------------------------- #
        
    async def __simulate( self, move, player_id ):
        global Matches
        response = Matches[self.__room_id].simulate( move, player_id )

        return response
