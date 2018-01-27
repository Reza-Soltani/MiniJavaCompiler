class A {
    static int a;
    static int b;

    public static int f(int x) {
        a = 10;
        b = 20;
        return x * a + b;
    }
}

public class Main {
    public static void main( ) {
        int i;
        for (i = 0; i < 10; i += 1) {
            System.out.println(A.f(i));
        }

    }
}
EOF