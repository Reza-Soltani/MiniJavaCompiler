// test case 1
class Cls{
    static boolean d ;
    public static int test( int a , boolean b ) {
        int c ;
        c = 1 ;
        b = true ;
        return a + c ;
    }
    public class Cls2 {
        public static void main( ) {
            int b;
            b = 3;
            b = Cls.test( b, false );
            System.out.println(b);
        }
    }
}
EOF