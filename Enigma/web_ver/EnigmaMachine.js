const charSetSize = 26

class Mapping {
    constructor(mapping) {
        this.mapping = mapping;
        this.mappingRev = this.reverseMap(mapping);
    }

    reverseMap(wiring) {
        let rev = {};
        for (var key in wiring) {
            rev[wiring[key]] = key;
        }
        return rev;
    }
    substitute() {}

    toString() {
        let ret = "{";
        for (let val in this.mapping) {
            ret += `"${val}": "${this.mapping[val]}", `;
        }
        return ret.trim() + "}";
    }
}


class Rotor extends Mapping {
    constructor(wiring) {
        super(wiring);
        this.position = 0;
    }

    rotate() {
        this.position += 1;
    }

    substitute(char, direction) {
        char = this.asciiToChar((this.charToASCII(char) + this.position) % charSetSize);
        return direction ? this.mapping[char] : this.mappingRev[char]
    }

    charToASCII(char) {
        return char.charCodeAt() - 65;
    }

    asciiToChar(ascii) {
        return String.fromCharCode(ascii + 65)
    }
}

class PlugBoard extends Mapping {
    constructor(connections) {
        super(connections);
    }

    substitute(char) {
        if (char in this.mapping) {
            return this.mapping[char];
        } else if (char in this.mappingRev) {
            return this.mappingRev[char];
        }
        return char;
    }
}

class Reflector extends Mapping {
    constructor(mapping) {
        super(mapping);
    }

    substitute(char) {
        return this.mapping[char];
    }
}

class EngimaMachine {
    constructor(rf, r1, r2, r3, pb) {
        this.pb = pb;
        this.r1 = r1; // right
        this.r2 = r2; // middle
        this.r3 = r3; // left
        this.rf = rf;
    }

    keyPress(char) {
        char = char.toUpperCase();
        let oldChar = char
        if (char.length === 1 && char.match(/[a-z]/i)) {
            char = this.pb.substitute(char);
            console.log(`${oldChar} --> ${char}`);
            oldChar = char;
            char = this.r1.substitute(char, true);
            console.log(`${oldChar} --> ${char}`);
            oldChar = char;
            char = this.r2.substitute(char, true);
            console.log(`${oldChar} --> ${char}`);
            oldChar = char;
            char = this.r3.substitute(char, true);
            console.log(`${oldChar} --> ${char}`);
            oldChar = char;
            char = this.rf.substitute(char);
            console.log(`${oldChar} --> ${char}`);
            oldChar = char;
            char = this.r3.substitute(char, false);
            console.log(`${oldChar} --> ${char}`);
            oldChar = char;
            char = this.r2.substitute(char, false);
            console.log(`${oldChar} --> ${char}`);
            oldChar = char;
            char = this.r1.substitute(char, false);
            console.log(`${oldChar} --> ${char}`);
            oldChar = char;
            char = this.pb.substitute(char);
            console.log(`${oldChar} --> ${char}`);
        }
        this.stepRotors()
        return char
    }

    stepRotors() {
        this.r1.rotate()
        if (this.r1.position == 5) {
            this.r1.position = 0;
            this.r2.rotate();
        }
        if (this.r2.position == 26) {
            this.r2.position = 0;
            this.r3.rotate();
        }
        if (this.r3.position == 26) {
            this.r3.position = 0;
        }
    }
}
let alp = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
let r1A = "JGDQOXUSCAMIFRVTPNEWKBLZYH";
let r2A = "NTZPSFBOKMWRCJDIVLAEYUXHGQ";
let r3A = "JVIUBHTCDYAKEQZPOSGXNRMWFL";
let rfA = "EJMZALYXVBWFCRQUONTSPIKHGD";

let r1Map = {};
let r2Map = {};
let r3Map = {};
let rfMap = {};
let pbMap = {};

for (let i = 0; i < charSetSize; i++) {
    r1Map[alp.charAt(i)] = r1A.charAt(i);
    r2Map[alp.charAt(i)] = r2A.charAt(i);
    r3Map[alp.charAt(i)] = r3A.charAt(i);
    if (alp.charAt(i) in rfMap) {
        rfA[rfMap[alp.charAt(i)]] = alp.charAt(i);
    } else {
        rfMap[alp.charAt(i)] = rfA.charAt(i);
    }
    if (i < 10) {
        pbMap[alp.charAt(i)] = alp.charAt(25 - i);
    }
}

let rf = new Reflector(rfMap);

let r1_1 = new Rotor(r1Map);
let r2_1 = new Rotor(r2Map);
let r3_1 = new Rotor(r3Map);

let r1_2 = new Rotor(r1Map);
let r2_2 = new Rotor(r2Map);
let r3_2 = new Rotor(r3Map);

let pb = new PlugBoard(pbMap);

let myMachine1 = new EngimaMachine(rf, r1_1, r2_1, r3_1, pb);
let myMachine2 = new EngimaMachine(rf, r1_2, r2_2, r3_2, pb);