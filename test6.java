// test case 1
class Cls{
    static boolean d ;
    static int x;
    public static int test1( int a , int b ) {
        return a + b ;
    }
}
class Cls3 extends Cls{
    static boolean d ;
    public static int test( int a , int b ) {
        return a * b;
    }
}
public class Cls2 {
    //this is main
    public static void main( ) {
        int b;
        int c;
        int d;
        b = 10;
        c = 20;
        d = Cls3.test(b, c);
        c = Cls.test1(b, c);
        System.out.println(d + c);
    }
}
EOF