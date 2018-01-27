class Cls{
    static int a ;
    static boolean d ;
    public static int test( int a , int b , int c , int d) {
        a = 10;
        b = 20;
        c = 30;
        while (a < b) {
            a = a + 1;
            b = b - 1;
        }
        for (a = 1; b < d; a += 2) {
            System.out.println(10);
            System.out.println(10);
            System.out.println(10);
            System.out.println(10);
        }
        return a + b;
    }
}

class Cls3 extends Cls{
    static int d;
}

public class Cls2 {
    public static void main( ) {
        System.out.println(Cls3.d);
    }
}
EOF