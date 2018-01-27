class A {
    public static int fact(int val) {
        int ret;
        ret = 1;
        while (0 < val) {
            ret = ret * val;
            val = val - 1;
        }
        return ret;
    }
}

public class Main {
    public static void main( ) {
        System.out.println(A.fact(6));
    }
}
EOF