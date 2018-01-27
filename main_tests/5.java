class calc {
    public static boolean isprime(int x) {
        int i;
        int t;
        boolean ret;
        ret = true;
        for (i = 2; i < x; i += 1) {
            t = x;
            while (0 < t) {
                t = t - i;
            }
            if (t == 0) {
                ret = false;
            } else {

            }
        }
        return ret;
    }
}

public class Main {
    public static void main( ) {
        int i;
        for (i = 2; i < 11; i += 1) {
            System.out.println(i);
            System.out.println(calc.isprime(i));
        }
    }
}
EOF