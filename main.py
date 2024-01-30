from ursina import *
from ursina.shaders import basic_lighting_shader
from ursina.prefabs.first_person_controller import FirstPersonController
from Block import *
from Chunk import *
from perlin_noise import PerlinNoise

#Create an instance of the ursina app
app = Ursina()

#Create player
player = FirstPersonController(
    mouse_sensitivity = Vec2(100,100),
    position = (0,10,0),
    
)

#Set background color and lighting
Sky(color = color.rgb(0, 0, 0) )
AmbientLight(color = color.rgba(100, 100, 100, 0.1))
DirectionalLight(parent=player, y=2, z=3, shadows=True)

#Set perlin noise map and terrain size
noise = PerlinNoise(octaves = 10, seed=2)
terrainSize = 400

#set chunkSize
chunkSize = 10

renderedChunks = []
renderedCoords = []

#Build Initial Chunks and add the Chunk object to renderedChunks array and Chunk coordinates to renderedCoords array
chunk1 = Chunk(chunkSize,0,0, noise, terrainSize)
chunk2 = Chunk(chunkSize,chunkSize,0, noise, terrainSize)
chunk3 = Chunk(chunkSize,0,chunkSize, noise, terrainSize)
chunk4 = Chunk(chunkSize,chunkSize,chunkSize, noise, terrainSize)

renderedChunks.append(chunk1)
renderedChunks.append(chunk2)
renderedChunks.append(chunk3)
renderedChunks.append(chunk4)

renderedCoords.append([chunk1.startX, chunk1.startZ])
renderedCoords.append([chunk2.startX, chunk2.startZ])
renderedCoords.append([chunk3.startX, chunk3.startZ])
renderedCoords.append([chunk4.startX, chunk4.startZ])

for x in renderedChunks:
    x.buildChunk()

#Chunk Generation
#On every update, check what chunk the player is in and based on that information, determine whether to delete/add new chunks
def update():
    currChunkPlayersIn = None
    for currChunk in renderedChunks:
        #Find what chunk the player is in
        inChunk = currChunk.checkChunkPosition(player.x, player.z)

        #If the player is in the current Chunk and the chunk the player is in changes, check what chunks to render
        if inChunk == True and currChunk != currChunkPlayersIn:
            currChunkPlayersIn = currChunk
            chunkX = currChunk.startX
            chunkZ = currChunk.startZ
            size = currChunk.chunkSize
            generateChunks(renderedChunks, renderedCoords, chunkX, chunkZ, size)
            deleteChunks(chunkX, chunkZ, size)

#Function that delete chunks when the player moves out of the render distance
def deleteChunks(currX, currZ, size):
    for chunk in renderedChunks:
        for x in range (currX - size * 2, currX + size * 2, size):
            if chunk.startX == x and chunk.startZ == currZ + size * 2:
                chunk.deleteChunk()
                renderedCoords.remove([chunk.startX, chunk.startZ])
                renderedChunks.remove(chunk)
        for x in range (currX - size * 2, currX + size * 2, size):
            if chunk.startX == x and chunk.startZ == currZ - size * 2:
                chunk.deleteChunk()
                renderedCoords.remove([chunk.startX, chunk.startZ])
                renderedChunks.remove(chunk)
        for z in range (currZ - size * 2, currZ + size * 2, size):
            if chunk.startX == currX - size * 2 and chunk.startZ == z:
                chunk.deleteChunk()
                renderedCoords.remove([chunk.startX, chunk.startZ])
                renderedChunks.remove(chunk)
        for z in range (currZ - size * 2, currZ + size * 2, size):
            if chunk.startX == currX + size * 2 and chunk.startZ == z:
                chunk.deleteChunk()
                renderedCoords.remove([chunk.startX, chunk.startZ])
                renderedChunks.remove(chunk)

#Function that generate neighboring chunks if they have yet to be rendered        
def generateChunks(renderedChunks, renderedCoords, chunkX, chunkZ, size):
    newrenderedChunks = []
    newrenderedCoords = []
    if [chunkX - size, chunkZ] not in renderedCoords:
        newRender = Chunk(size,chunkX - size, chunkZ, noise, terrainSize)
        newrenderedChunks.append(newRender)
        newrenderedCoords.append([chunkX - size, chunkZ])
    if [chunkX + size, chunkZ] not in renderedCoords:
        newRender = Chunk(size,chunkX + size,chunkZ, noise, terrainSize)
        newrenderedChunks.append(newRender)
        newrenderedCoords.append([chunkX + size, chunkZ])
    if [chunkX, chunkZ - size] not in renderedCoords:
        newRender = Chunk(size,chunkX, chunkZ - size, noise, terrainSize)
        newrenderedChunks.append(newRender)
        newrenderedCoords.append([chunkX, chunkZ - size])
    if [chunkX, chunkZ + size] not in renderedCoords:
        newRender = Chunk(size,chunkX, chunkZ + size, noise, terrainSize)
        newrenderedChunks.append(newRender)
        newrenderedCoords.append([chunkX, chunkZ + size])
    if [chunkX - size, chunkZ - size] not in renderedCoords:
        newRender = Chunk(size,chunkX - size, chunkZ - size, noise, terrainSize)
        newrenderedChunks.append(newRender)
        newrenderedCoords.append([chunkX - size, chunkZ - size])
    if [chunkX - size, chunkZ + size] not in renderedCoords:
        newRender = Chunk(size,chunkX - size, chunkZ + size, noise, terrainSize)
        newrenderedChunks.append(newRender)
        newrenderedCoords.append([chunkX - size, chunkZ + size])
    if [chunkX + size, chunkZ + size] not in renderedCoords:
        newRender = Chunk(size,chunkX + size, chunkZ + size, noise, terrainSize)
        newrenderedChunks.append(newRender)
        newrenderedCoords.append([chunkX + size, chunkZ + size])
    if [chunkX + size, chunkZ - size] not in renderedCoords:
        newRender = Chunk(size,chunkX + size, chunkZ - size, noise, terrainSize)
        newrenderedChunks.append(newRender)
        newrenderedCoords.append([chunkX + size, chunkZ - size])
    for chunk in newrenderedChunks:
        chunk.buildChunk()
    renderedChunks += newrenderedChunks
    renderedCoords += newrenderedCoords

#Run the app
app.run()