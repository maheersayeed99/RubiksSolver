/// <reference path="vector.ts" />

enum Color { green, blue, orange, red, white, yellow }
enum Side{F,B,L,R,U,D}
enum Edge{top,right,bot,left}

var edgeIndicesMap = new Map<Edge,Vector2[]>()                                          // edge means the facets along a whole edge
edgeIndicesMap.set(Edge.top,[new Vector2(2,0),new Vector2(1,0),new Vector2(0,0),])
edgeIndicesMap.set(Edge.right,[new Vector2(2,2),new Vector2(2,1),new Vector2(2,0),])
edgeIndicesMap.set(Edge.bot,[new Vector2(0,2),new Vector2(1,2),new Vector2(2,2),])
edgeIndicesMap.set(Edge.left,[new Vector2(0,0),new Vector2(0,1),new Vector2(0,2),])

var side2NormalMap = new Map<Side,Vector3>();               // Given the side, return the normal vector
side2NormalMap.set(Side.F,new Vector3(0,0,-1))
side2NormalMap.set(Side.B,new Vector3(0,0,1))
side2NormalMap.set(Side.L,new Vector3(-1,0,0))
side2NormalMap.set(Side.R,new Vector3(1,0,0))
side2NormalMap.set(Side.U,new Vector3(0,1,0))
side2NormalMap.set(Side.D,new Vector3(0,-1,0))

function normal2Side(v:Vector3):Side{                       // Given the normal vecotr, return the side
    for(var i = 0; i < 6; i++){
        if(v == side2NormalMap.get(i)){
            return i;
        }
    }
}

class Action{
    side:Side
    counterClockWise:boolean

    constructor(side: Side, reverse: boolean){
        this.side = side
        this.counterClockWise = reverse
    }

    rotateActionToSide(side: Side, action: Action) {
        var destNormal = side2NormalMap.get(side)
        var actionNormal = side2NormalMap.get(action.side)

        var plane = destNormal.cross(actionNormal)
        var angle = Math.acos(destNormal.dot(actionNormal))


        var rotationBetween;

        var relLook = new Vector3(0,0,-1).rot(rotationBetween)
        var newside;//=get side from vector
        action.side = newside;


    }
}

class Face{                                 // i think this is what he calls a facet of a piece
    color:Color
    side:Side

    constructor(color: Color,side: Side){
        this.color = color
        this.side = side
    }
}

class Block{                                // this should be a whole cubie
    faces:Face[]

    constructor(faces:Face[]){
        this.faces = faces
    }

    isEdge(){
        return this.faces.length == 2       // edge piece?
    }

    isSameBlock(other:Block) {
        if(this.isEdge() != other.isEdge()){
            return false
        }else{
            for(var face of this.faces){
                var result = other.faces.find((tface) => {
                    return tface.color == face.color
                })
                if(result == undefined){
                    return false
                }
            }
            return true
        }
    }

    isSameBlockAndSameOrientation() {

    }
}

class Cube {                                            // whole cube

    vals: Color[][][]               // this is the cube

    constructor() {
        this.vals = new Array(6)

        for (var i = 0; i < this.vals.length; i++) {
            this.vals[i] = [
                [i, i, i],
                [i, i, i],
                [i, i, i],
            ]
        }


        /*
        [0,0,0]
        [0,0,0]
        [0,0,0]

        [1,1,1]
        [1,1,1]
        [1,1,1]

        etc

        */
    }

    solve() {                           // Solve algorithm
        this.topEdges()
        this.topCorners()
        this.middleEdges()
        this.bottomCross()
        this.bottomEdges()
        this.positionBottomCorners()
        this.orientBottomCorners()
    }


    /*
                000 001 002
                010 011 012
                020 021 022
    100 101 102 200 201 202 300 301 302 400 401 402
    110 111 112 210 211 212 310 311 312 410 411 412
    120 121 122 220 221 222 320 321 322 420 421 422
                600 601 602
                610 611 612
                620 621 622


                000 001 002
                010 011 012
                020 021 022
    100 101 102 200 201 202 300 301 302 400 401 402
    110 111 112 210 211 212 310 311 312 410 411 412
    120 121 122 220 221 222 320 321 322 420 421 422
                600 601 602
                610 611 612
                620 621 622
    */

    getBlock(v:Vector3):Block{                      // attach piece to cube coordinates
        var faces:Face[] = []                       
        var normals:Vector3[] = []                  // make vector of normals
        for(var i = 0; i < 3;i++){
            if(v.vals[i] != 0){
                var normal = new Vector3(0,0,0)     // for each non zero value in input, append a vector to norm that is only 
                normal.vals[i] = v.vals[i]          // non zero in the current slot
                normals.push(normal)                // ex: input = 5, 0, 3
            }                                       // output = [[5,0,0],[0,0,3]]
        }

        var faces:Face[] = []
        for(var i = 0; i < normals.length; i++){        // should have one facet for each normal
            var side:Side = normal2Side(normal)         // get Side from normal

            for(var j = 0; j < normals.length;j++){
                var cubeface = this.vals[side]
                if(i == j){
                    continue
                }

            }
        }
        
        

        return new Block(faces)
    }

    findBlock(block:Block):Vector3{
        return null
    }

    topEdges(){
        var uruf = [new Action(Side.U, true), new Action(Side.R, true), new Action(Side.U, false), new Action(Side.F, true),]//edge correct place but oriendted wrong
        var frdrff = [new Action(Side.F, true), new Action(Side.R, true), new Action(Side.D, true),
            new Action(Side.R, false), new Action(Side.F, false), new Action(Side.F, false),]//edge at the bottom
        var rdrff = [new Action(Side.R, true), new Action(Side.D, true), new Action(Side.R, false),
            new Action(Side.F, false), new Action(Side.F, false),]//edge at the side

        //detect case and apply algorithm
    }

    topCorners(){
        var rdrd = [new Action(Side.R, true), new Action(Side.D, true), new Action(Side.R, false), new Action(Side.D, false)]//corner at bot or correct spot but oriented wrong
        var fdf = [new Action(Side.F, false), new Action(Side.D, false), new Action(Side.F, true),]//bottom and oriented wrong
        var rddrdrdr = [new Action(Side.R, true), new Action(Side.D, false), new Action(Side.D, false), new Action(Side.R, false),
            new Action(Side.D, false), new Action(Side.R, true), new Action(Side.D, true), new Action(Side.R, false),]//bottom and oriented wrong

    }

    middleEdges(){
        var ululufuf = [new Action(Side.U, true), new Action(Side.L, true), new Action(Side.U, false), new Action(Side.L, false),
            new Action(Side.U, false), new Action(Side.F, false), new Action(Side.U, true), new Action(Side.F, true),]//top to left
        var ururufuf = [new Action(Side.U, false), new Action(Side.R, false), new Action(Side.U, true), new Action(Side.R, true),
            new Action(Side.U, true), new Action(Side.U, true), new Action(Side.U, false), new Action(Side.U, false),]//top to right
        var ururufufuuururufuf = ururufuf.slice().concat([new Action(Side.U, false), new Action(Side.U, false),], ururufuf.slice())//oriented wrong

    }

    bottomCross(){
        var fruruf = [new Action(Side.F, false), new Action(Side.R, false), new Action(Side.U, false),
            new Action(Side.R, true), new Action(Side.U, true), new Action(Side.F, true),]//progress topstate
        //detect 1 of the following and orient to correct alignment
        //dot
        //L
        //line
        //cross
    }

    bottomEdges(){
        var rururuuru = [new Action(Side.R, false), new Action(Side.U, false), new Action(Side.R, true), new Action(Side.U, false), new Action(Side.R, false),
            new Action(Side.U, false), new Action(Side.U, false), new Action(Side.U, true), new Action(Side.U, false),]//swap edges
    }

    positionBottomCorners(){
        var urulurul = [new Action(Side.U, false), new Action(Side.R, false), new Action(Side.U, true), new Action(Side.L, true),
            new Action(Side.U, false), new Action(Side.R, true), new Action(Side.U, true), new Action(Side.L, false),]//position corners
        //detect 0,1 or 4 blocks are right

    }

    orientBottomCorners(){
        var rdrd = [new Action(Side.R, true), new Action(Side.D, true), new Action(Side.R, false), new Action(Side.D, false)]//rotate corner
    }

    scramble(n) {
        this.executeActions(this.generateRandomActions(n))
    }

    rotateCap(side: Side, counterclockwise: boolean){
        this.rotateCapTop(side,counterclockwise)
        this.rotateCapSides(side, counterclockwise)
    }

    F(counterclockwise:boolean) {
        this.rotateCap(Side.F,counterclockwise)
    }

    B(counterclockwise: boolean) {
        this.rotateCap(Side.B, counterclockwise)
    }

    L(counterclockwise: boolean) {
        this.rotateCap(Side.L, counterclockwise)
    }

    R(counterclockwise: boolean) {
        this.rotateCap(Side.R, counterclockwise)
    }

    U(counterclockwise: boolean) {
        this.rotateCap(Side.U, counterclockwise)
    }

    D(counterclockwise: boolean) {
        this.rotateCap(Side.D, counterclockwise)
    }

    generateRandomActions(n):Action[]{
        var sides = [Side.F, Side.B, Side.L, Side.R, Side.U, Side.D]
        var actions: Action[] = []
        for (var i = 0; i < n; i++) {
            var side = Math.floor(Math.random() * 6)
            var reversed = Math.random() > 0.5
            actions.push(new Action(sides[side], reversed))
        }
        return actions
    }

    

    executeActions(actions:Action[]){
        for(var action of actions){
            this.rotateCap(action.side,action.counterClockWise)
        }
    }

    private rotateCapTop(side: Side, reversed: boolean) {
        var cap = this.vals[side]
        var rot = reversed ? Math.PI / 2 : -Math.PI / 2;
        var vecs = [
            new Vector2(-1, 1),
            new Vector2(0, 1),
            new Vector2(1, 1),
            new Vector2(1, 0),
            new Vector2(1, -1),
            new Vector2(0, -1),
            new Vector2(-1, -1),
            new Vector2(-1, 0),
        ]
        var vec1 = new Vector2(1, 1)
        for (var v of vecs) {
            v.rot(-rot).round()
            v.y = -v.y
            v.add(vec1)//negative rotation because need to look back
        }

        var newFront = [
            [getxy(cap, vecs[0]), getxy(cap, vecs[1]), getxy(cap, vecs[2]),],
            [getxy(cap, vecs[7]), cap[1][1], getxy(cap, vecs[3]),],
            [getxy(cap, vecs[6]), getxy(cap, vecs[5]), getxy(cap, vecs[4]),],
        ]
        this.vals[side] = newFront
    }

    private rotateCapSides(side: Side, counterclockwise: boolean) {//otherwise use 3d model with normals
        if(counterclockwise){
            this.rotateCapSides(side,false)
            this.rotateCapSides(side,false)
            this.rotateCapSides(side,false)
        }else{
            switch(side){
                // enum Color { green, blue, orange, red, white, yellow }
                // enum Side { F, B, L, R, U, D }
                case Side.F: {
                    this.rotateSides(this.vals,
                        Side.U,Edge.bot,
                        Side.R,Edge.left,
                        Side.D,Edge.top,
                        Side.L,Edge.right
                    )
                    break;
                }
                case Side.B: {
                    this.rotateSides(this.vals,
                        Side.U,Edge.top,
                        Side.L,Edge.left,
                        Side.D,Edge.bot,
                        Side.R,Edge.right
                    )
                    break;
                }
                case Side.L: {
                    this.rotateSides(this.vals,
                        Side.U,Edge.left,
                        Side.F,Edge.left,
                        Side.D,Edge.left,
                        Side.B,Edge.right
                    )
                    break;
                }
                case Side.R: {
                    this.rotateSides(this.vals,
                        Side.U,Edge.right,
                        Side.B,Edge.left,
                        Side.D,Edge.right,
                        Side.F,Edge.right
                    )
                    break;
                }
                case Side.U: {
                    this.rotateSides(this.vals,
                        Side.B,Edge.top,
                        Side.R,Edge.top,
                        Side.F,Edge.top,
                        Side.L,Edge.top
                    )
                    break;
                }
                case Side.D: {
                    this.rotateSides(this.vals,
                        Side.F,Edge.bot,
                        Side.R,Edge.bot,
                        Side.B,Edge.bot,
                        Side.L,Edge.bot
                    )
                    break;
                }
            }
        }
    }
    // enum Side{F,B,L,R,U,D}
    // enum Edge{top,right,bot,left}
    private rotateSides(cube:Color[][][],top:Side,topsideEdge:Edge,right:Side,rightsideEdge:Edge,bot:Side,botside:Edge,left:Side,leftside:Edge){
        //move top to copy of right
        var newright = this.srcEdgeToCopyEdge(this.vals[top],topsideEdge,this.vals[right],rightsideEdge)

        //move right to copy of bot
        var newbot = this.srcEdgeToCopyEdge(this.vals[right],rightsideEdge,this.vals[bot],botside)

        //move bot to copy of left
        var newleft = this.srcEdgeToCopyEdge(this.vals[bot],botside,this.vals[left],leftside)

        //move left to copy of top
        var newtop = this.srcEdgeToCopyEdge(this.vals[left],leftside,this.vals[top],topsideEdge)

        //replace originals with the copys
        this.vals[top] = newtop
        this.vals[right] = newright
        this.vals[bot] = newbot
        this.vals[left] = newleft

    }

    private srcEdgeToCopyEdge(src:Color[][],srcEdge:Edge,dstToCopy:Color[][],dstEdge:Edge):Color[][]{
        var copy = copy2Darray(dstToCopy)
        var srcIndices = edgeIndicesMap.get(srcEdge) as Vector2[]
        var dstIndices = edgeIndicesMap.get(dstEdge) as Vector2[]
        for(var i = 0; i < srcIndices.length; i++){
            setxy(copy,dstIndices[i],getxy(src,srcIndices[i]))
        }
        return copy;
    }

    rotateSidesUsingMath(side: Side, counterclockwise: boolean){
        var normal = side2NormalMap.get(side)
        var top 
    }

    getColorFromNormal(normal:Vector3,offset:Vector3):Color{
        return null;
    }

    setColorFromNormal(normal:Vector3,offset:Vector3,color:Color){

    }

    

    draw(ctxt:CanvasRenderingContext2D){
        var locs = [
            new Vector2(150, 150), 
            new Vector2(450, 150), 
            new Vector2(0, 150), 
            new Vector2(300, 150), 
            new Vector2(150, 0),
            new Vector2(150, 300),
        ]
        for(var i = 0; i < 6; i++){
            this.drawSide(ctxt,locs[i],i)
        }
    }

    drawSide(ctxt: CanvasRenderingContext2D,v:Vector2,side:Side){
        var size = 50
        for(var x = 0; x < 3; x++){
            for(var y = 0; y < 3; y++){
                ctxt.fillStyle = Color[this.vals[side][y][x]]
                ctxt.fillRect(x * size + v.x,y * size + v.y,size,size)
            }
        }
    }
}

function getxy(arr,v:Vector2){
    return arr[v.y][v.x]
}

function setxy(arr,v:Vector2,val){
    arr[v.y][v.x] = val
}

function copy2Darray(array:any[][]){
    var copy = new Array(array.length)
    for(var y = 0; y < array.length; y++){
        copy[y] = new Array(array[y].length)
        for(var x = 0; x < array[y].length; x++){
            copy[y][x] = array[y][x]
        }
    }
    return copy
}