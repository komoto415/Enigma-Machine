class Mapping {
    constructor(mapping) {
        this.mapping = mapping
        this.mappingRev = this.reverseMap(mapping)
    }

    reverseMap(wiring) {
        let rev = {};
        for (var key in wiring) {
            rev[wiring[key]] = key;
        }
        return rev
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
        super(wiring)
        this.position = 0;
    }

    rotate() {
        this.position += 1;
    }

    substitute(char, direction) {
        char = this.asciiToChar((this.charToASCII(char) + this.position) % 26);
        return direction ? this.mapping[char] : this.mappingRev[char];
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

    substitute(char, direction) {
        if (char in this.mapping && direction) {
            return this.mapping[char]
        } else if (char in this.mappingRev && !direction) {
            return this.mappingRev[char]
        }
        return char
    }
}

class Reflector extends Mapping {
    constructor(mapping) {
        super(mapping)
    }

    substitute(char, direction) {
        return direction ? this.mapping[char] : this.mappingRev[char];
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
            char = this.pb.substitute(char, true);
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
            char = this.rf.substitute(char, true);
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
            char = this.pb.substitute(char, false);
            console.log(`${oldChar} --> ${char}`);
        }
        this.stepRotors()
        return char
    }

    stepRotors() {
        this.r1.rotate()
        if (this.r1.position == 26) {
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
// let alp = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
// let r1A = "JGDQOXUSCAMIFRVTPNEWKBLZYH";
// let r2A = "NTZPSFBOKMWRCJDIVLAEYUXHGQ";
// let r3A = "JVIUBHTCDYAKEQZPOSGXNRMWFL";
// let rfA = "EJMZALYXVBWFCRQUONTSPIKHGD";

// let r1Map = {};
// let r2Map = {};
// let r3Map = {};
// let rfMap = {};
// for (let i = 0; i < 26; i++) {
//     r1Map[alp.charAt(i)] = r1A.charAt(i);
//     r2Map[alp.charAt(i)] = r2A.charAt(i);
//     r3Map[alp.charAt(i)] = r3A.charAt(i);
//     rfMap[alp.charAt(i)] = rfA.charAt(i);
// }

// let rf = new Reflector(rfMap);
// let r1 = new Rotor(r1Map);
// let r2 = new Rotor(r2Map);
// let r3 = new Rotor(r3Map);
// let pb = new PlugBoard({
//     A: "X",
//     B: "N",
//     Q: "M",
//     D: "Z",
//     K: "A",
//     F: "L",
//     G: "Y",
//     H: "X",
//     I: "V",
//     J: "P",
// });


// let myMachine = new EngimaMachine(rf, r1, r2, r3, pb);

// let ch1 = myMachine.keyPress("A");
// console.log();
// let ch2 = myMachine.keyPress("A");
// console.log(ch1, ch2);