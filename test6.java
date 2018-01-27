// test case 1
class Cls{
    static boolean d ;
    static int x;
    public static int test( int a , boolean b ) {
        return a + b ;
    }
}
class Cls3 extends Cls{
    static boolean d ;
    public static int test( int a , boolean b ) {
        int c;
        c = -132;
        if ( c == b && c < b ){
            c = 10;
        }
        else{
            if ( c == a){
                c = 5;
            }
            else{
                for (c = 1; c + 2 + 4 == a; a += 1){
                    while( true ){
                        a = b;
                      //  c = Cls.test(a, b);
                        }
                }
            }
        }
        b = true ; /* comment */
        return a + c ;
    }
}
public class Cls2 {
    //this is main
    public static void main( ) {
        int b;
        b = 2 + -3;
        b = Cls3.test( b, false );
        System.out.println(b);
    }
}
EOF