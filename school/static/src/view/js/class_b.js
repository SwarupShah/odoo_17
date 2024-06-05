/* @odoo-module */
import {A} from './class_a'
class B extends A {
    setup() {
        super.setup();
        console.log("Class B setup");
    }

    methodB() {
        console.log("Method B from class B");
    }

    methodA() {
        super.methodA();
        console.log("Overridden Method A in class B");
    }

    method_proto(){
      let a = {
         b: 99
      }
     console.log(a)
    }
}


let b = new B()

b.method_proto()

//b.methodB()
//b.methodA()

