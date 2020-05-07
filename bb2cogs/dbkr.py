import dbkrpy
import discord
from discord.ext import commands

class UpdateGuild(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjYyMjcxMDM1NDgzNjcxNzU4MCIsImlhdCI6MTU4ODU2OTY0MSwiZXhwIjoxNjIwMTI3MjQxfQ.dydae2BLTlu44JyLGGKUPTWjelpGwAOL05Te7ASNRL-LseO4blUMX1NyXxDvcNij8kK3iqQqX8Ltpy_J8z7omd9LB0UZPRJ3Rjj8c5NzlwZIitISRvmEjqIrWlZeggiZ18AUdcppcQbDW8XK7AzbQ4WXGd9gMshSbPzyLSs8gB4'
        dbkrpy.DBKRPython(self.client,self.token)

def setup(client):
    client.add_cog(UpdateGuild(client))