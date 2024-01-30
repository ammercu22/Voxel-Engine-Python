from Block import Block
from perlin_noise import PerlinNoise
from ursina import *

#Class that builds a chunk
class Chunk():
    def __init__(self, chunkSize, startX, startZ, noise, terrainSize):
        self.chunkSize = chunkSize
        self.startX = startX
        self.startZ = startZ
        self.blocks = []
        self.blocksPos = []
        self.currChunk = False
        self.noise = noise
        self.terrainSize = terrainSize
    #Function that builds a chunk of blocks. The functions determines y position of block based on perlin noise value. x and z positions are determined by for loop increment
    def buildChunk(self):
        for x in range(self.startX, self.startX + self.chunkSize):
            for z in range(self.startZ, self.startZ + self.chunkSize):
                frequency = 2.5
                noise = self.noise([frequency * x/self.terrainSize - 0.5, frequency * z/self.terrainSize - 0.5])
                y = round(noise, 1) * 10
                self.blocksPos.append([x,y,z])
        self.optimizeChunk()

    #Function that optimizes the chunk mesh so the performance of the app improves
    def optimizeChunk(self):
        for blockPos in self.blocksPos:
            x = blockPos[0]
            y = blockPos[1]
            z = blockPos[2]
            mesh = self.buildMesh(x,y,z)
            color = self.blockType(y)
            block = Block((x,y,z),mesh, color)
            self.blocks.append(block)

    #Function that deletes all blocks in the chunk
    def deleteChunk(self):
        for block in self.blocks:
            destroy(block)
        
    #Function that checks whether player is in this chunk or not
    def checkChunkPosition(self, playerX, playerZ):
        if(playerX >= self.startX and playerZ >= self.startZ and playerX < self.startX + self.chunkSize and playerZ < self.startZ + self.chunkSize):
            return True
        return False
    
    #Function that determines what type of block a block is based on y-value
    def blockType(self, y):
        blockColor = color.rgb(255,255,255)
        #ocean
        if y < -2:
            blockColor = color.rgb(0, 107, 255)
        #sand
        elif y >= -2 and y < 0:
            blockColor = color.rgb(255, 227, 170)
        #grass
        elif y >= 0 and y < 3:
            blockColor = color.rgb(38,148,71)
        #mountain
        else:
            blockColor = color.rgb(124,124,124)
        return blockColor
    
    #Function that builds the mesh of the block as well optimizes the block by deleting uneccessary faces of the block.
    def buildMesh(self, x, y, z):
        #default mesh with only bottom face removed
        ourMesh = Mesh(
                    vertices=[[0,0,0],#0
                        [1,0,0],#1
                        [1,0,1],#2
                        [0,0,1],#3
                        [0,1,0],#4
                        [1,1,0],#5
                        [1,1,1],#6
                        [0,1,1]#7
                        ],
                    triangles=[
                        [0,1,5,4],
                        [1,2,6,5],
                        [2,3,7,6],
                        [3,0,4,7],
                        [4,5,6,7]
                        ],
                    normals = [[-1,-1,-1],#0
                        [1,-1,-1],#1
                        [1,-1,1],#2
                        [-1,-1,1],#3
                        [-1,1,-1],#4
                        [1,1,-1],#5
                        [1,1,1],#6
                        [-1,1,1]#7
                    ],
                    uvs=[[0,0],[1,0],[1,1],[0,1], [0,0],[1,0],[1,1],[0,1]],
                    )
        #if there is a block to the left of currBlock, remove left face
        if [x-1, y, z] in self.blocksPos:
            ourMesh.triangles.remove([3,0,4,7])
        #if there is a block to the right of currBlock, remove right face
        if [x + 1, y, z] in self.blocksPos:
            ourMesh.triangles.remove([1,2,6,5])
        #if there is a block in front of currBlock, remove front face
        if [x, y, z - 1] in self.blocksPos:
            ourMesh.triangles.remove([0,1,5,4])
        #if there is a block in front of currBlock and above, remove Front face
        if [x, y + 1, z - 1] in self.blocksPos:
            ourMesh.triangles.remove([0,1,5,4])
        #if there is a block behind currBlock, remove back face
        if [x, y, z + 1] in self.blocksPos:
            ourMesh.triangles.remove([2,3,7,6])
        #if there is a block behind currBlock and above it, remove back face
        if [x, y + 1, z + 1] in self.blocksPos:
            ourMesh.triangles.remove([2,3,7,6])
        
        #generate newMesh based on modifications
        ourMesh.generate()

        return ourMesh
    
